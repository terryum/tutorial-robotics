import assert from "node:assert/strict";
import { test } from "node:test";
import worker from "./worker.mjs";

const origin = "https://book.example";
const route = `${origin}/api/book-feedback`;
const issueUrl = "https://github.com/terryum/tutorial-robotics/issues/123";
const page = "docs/ko/lessons/core-01.md";
const feedback = { page, message: "그래프 단위를 한 번 더 설명해 주세요." };

function makeEnv(overrides = {}) {
  const limiter = { limit: async () => ({ success: true }) };
  return {
    GITHUB_ISSUES_TOKEN: "test-only",
    FEEDBACK_CLIENT_LIMITER: limiter,
    FEEDBACK_SITE_LIMITER: limiter,
    ...overrides,
  };
}

function post(payload, headers = {}) {
  return new Request(route, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...headers },
    body: JSON.stringify(payload),
  });
}

test("a guest can submit without either optional identity field or a GitHub session", async ({ mock }) => {
  const github = mock.method(globalThis, "fetch", async (url, init) => {
    assert.equal(url, "https://api.github.com/repos/terryum/tutorial-robotics/issues");
    assert.equal(init.method, "POST");
    assert.equal(init.headers.Authorization, "Bearer test-only");
    assert.equal(init.redirect, "error");
    const { title, body } = JSON.parse(init.body);
    assert.equal(title, "[교재 피드백] lessons/core-01.md");
    assert.ok(body.includes(`https://github.com/terryum/tutorial-robotics/blob/main/${page}`));
    assert.ok(body.includes("제출자: 익명"));
    assert.ok(body.includes(feedback.message));
    return Response.json({ html_url: issueUrl }, { status: 201 });
  });
  const response = await worker.fetch(post(feedback, { Origin: origin }), makeEnv());
  assert.equal(response.status, 201);
  assert.deepEqual(await response.json(), { url: issueUrl });
  assert.equal(github.mock.callCount(), 1);
});

test("a self-reported handle stays literal and optional email is stored only in private KV", async ({ mock }) => {
  const email = "Reader+feedback@example.org";
  const put = mock.fn(async () => {});
  const github = mock.method(globalThis, "fetch", async (_, init) => {
    const { title, body } = JSON.parse(init.body);
    const [key, value, options] = put.mock.calls[0].arguments;
    assert.equal(value, email);
    assert.deepEqual(options, { expirationTtl: 2_592_000 });
    assert.match(key, /^[0-9a-f-]{36}$/);
    assert.ok(body.includes(key));
    assert.ok(body.includes("GitHub 아이디(본인 기재): `reader-name`"));
    assert.ok(!`${title}\n${body}`.toLowerCase().includes(email.toLowerCase()));
    assert.ok(body.includes("[이메일 비공개]"));
    assert.ok(body.includes("    ```"));
    assert.ok(body.includes("    @\u200bowner <script> [test](https://example.org)"));
    return Response.json({ html_url: issueUrl }, { status: 201 });
  });
  const request = post({
    ...feedback,
    message: [
      feedback.message,
      "",
      "```",
      "@owner <script> [test](https://example.org)",
      email.toUpperCase(),
    ].join("\r\n"),
    github: "@reader-name",
    email,
  });
  const response = await worker.fetch(request, makeEnv({ FEEDBACK_CONTACTS: { put } }));
  assert.equal(response.status, 201);
  assert.equal(put.mock.callCount(), 1);
  assert.equal(github.mock.callCount(), 1);
});

test("a missing or failed private contact store prevents publishing a reply without its contact", async ({ mock }) => {
  const upstream = mock.method(globalThis, "fetch");
  for (const FEEDBACK_CONTACTS of [undefined, { async put() { throw new Error("private"); } }]) {
    const response = await worker.fetch(
      post({ ...feedback, email: "reader@example.org" }),
      makeEnv({ FEEDBACK_CONTACTS }),
    );
    assert.equal(response.status, 503);
    assert.deepEqual(await response.json(), { error: "contact_unavailable" });
  }
  assert.equal(upstream.mock.callCount(), 0);
});

test("the request rejects cross-origin, invalid paths, invalid fields, and oversized streams", async ({ mock }) => {
  const upstream = mock.method(globalThis, "fetch");
  const env = makeEnv();
  assert.equal((await worker.fetch(post(feedback, { Origin: "https://other.example" }), env)).status, 403);
  for (const input of [
    { page: "docs/en/home.md" },
    { page: "docs/ko/../home.md" },
    { page: "docs/ko/home.md#title" },
    { page: "docs/ko/home.md\n" },
    { message: "" },
    { message: "a".repeat(2001) },
    { github: "project/team" },
    { email: "invalid email" },
  ]) {
    assert.equal((await worker.fetch(post({ ...feedback, ...input }), env)).status, 400);
  }
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(new Uint8Array(10_000).fill(97));
      controller.enqueue(new Uint8Array(7_000).fill(97));
      controller.close();
    },
  });
  const oversized = new Request(route, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: stream,
    duplex: "half",
  });
  assert.equal(oversized.headers.get("Content-Length"), null);
  assert.equal((await worker.fetch(oversized, env)).status, 413);
  assert.equal(upstream.mock.callCount(), 0);
});

test("the service fails closed when a rate limiter is missing or rejects the request", async ({ mock }) => {
  const upstream = mock.method(globalThis, "fetch");
  const client = mock.fn(async () => ({ success: true }));
  const site = mock.fn(async () => ({ success: false }));
  const response = await worker.fetch(
    post(feedback, { "CF-Connecting-IP": "192.0.2.1" }),
    makeEnv({ FEEDBACK_CLIENT_LIMITER: { limit: client }, FEEDBACK_SITE_LIMITER: { limit: site } }),
  );
  assert.equal(response.status, 429);
  assert.deepEqual(client.mock.calls[0].arguments, [{ key: "192.0.2.1" }]);
  assert.deepEqual(site.mock.calls[0].arguments, [{ key: "book-feedback" }]);
  assert.equal((await worker.fetch(post(feedback), makeEnv({ FEEDBACK_SITE_LIMITER: null }))).status, 503);
  assert.equal(upstream.mock.callCount(), 0);
});

test("a definite GitHub rejection deletes the unused contact and suppresses upstream details", async ({ mock }) => {
  mock.method(globalThis, "fetch", async () => Response.json({ message: "private" }, { status: 422 }));
  const put = mock.fn(async () => {});
  const deleteContact = mock.fn(async () => {});
  const response = await worker.fetch(
    post({ ...feedback, email: "reader@example.org" }),
    makeEnv({ FEEDBACK_CONTACTS: { put, delete: deleteContact } }),
  );
  assert.equal(response.status, 502);
  assert.deepEqual(await response.json(), { error: "issue_not_created" });
  assert.deepEqual(deleteContact.mock.calls[0].arguments, [put.mock.calls[0].arguments[0]]);
});

test("the success URL must be an issue in the feedback repository", async ({ mock }) => {
  mock.method(globalThis, "fetch", async () => Response.json({
    html_url: "https://github.com/other/repo/issues/123",
  }, { status: 201 }));
  const response = await worker.fetch(post(feedback), makeEnv());
  assert.equal(response.status, 502);
  assert.deepEqual(await response.json(), { error: "issue_not_created" });
});

test("static assets fall through and the feedback route only accepts POST", async () => {
  const asset = new Request(`${origin}/ko/`);
  const env = makeEnv({ ASSETS: { fetch: async (request) => {
    assert.equal(request, asset);
    return new Response("교재");
  } } });
  assert.equal(await (await worker.fetch(asset, env)).text(), "교재");
  const response = await worker.fetch(new Request(route), env);
  assert.equal(response.status, 405);
  assert.equal(response.headers.get("Allow"), "POST");
});
