const repository = "terryum/tutorial-robotics";
const route = "/api/book-feedback";
const maxBodyBytes = 16_384;
const pagePattern = /^docs\/ko\/(?:[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*\/)*[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*\.md$/;
const issueUrlPattern = /^https:\/\/github\.com\/terryum\/tutorial-robotics\/issues\/[1-9][0-9]*$/;
const responseHeaders = { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" };

function error(status, code) {
  return Response.json({ error: code }, { status, headers: responseHeaders });
}

async function readBody(request) {
  if (Number(request.headers.get("Content-Length")) > maxBodyBytes) {
    return { tooLarge: true };
  }
  if (!request.body) return {};

  const reader = request.body.getReader();
  const decoder = new TextDecoder("utf-8", { fatal: true });
  let text = "";
  let size = 0;
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) return { value: JSON.parse(text + decoder.decode()) };
      size += value.byteLength;
      if (size > maxBodyBytes) {
        await reader.cancel().catch(() => {});
        return { tooLarge: true };
      }
      text += decoder.decode(value, { stream: true });
    }
  } catch {
    return {};
  } finally {
    reader.releaseLock();
  }
}

function feedbackFields(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const { page, message, github = "", email = "" } = value;
  if ([page, message, github, email].some((field) => typeof field !== "string")) return null;
  const fields = {
    page,
    message: message.trim().replace(/\r\n?/g, "\n"),
    github: github.trim().replace(/^@/, ""),
    email: email.trim(),
  };
  if (page.length > 180 || !pagePattern.test(page) || !fields.message) return null;
  if (fields.message.length > 2000 || /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(fields.message)) {
    return null;
  }
  if (fields.github && !/^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$/.test(fields.github)) {
    return null;
  }
  if (fields.email && (fields.email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email))) {
    return null;
  }
  return fields;
}

function issueContent(fields, receipt) {
  const pageUrl = `https://github.com/${repository}/blob/main/${fields.page}`;
  let message = fields.message;
  if (fields.email) {
    const literalEmail = fields.email.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    message = message.replace(new RegExp(literalEmail, "gi"), "[이메일 비공개]");
  }
  // A code block preserves the submitted text without interpreting it as GitHub Markdown.
  const indented = message.replaceAll("@", "@\u200b").split("\n").map((line) => `    ${line}`);
  const body = [
    `교재 페이지: [${fields.page}](${pageUrl})`,
    fields.github ? `GitHub 아이디(본인 기재): \`${fields.github}\`` : "제출자: 익명",
    ...(receipt ? [`비공개 이메일 연락처 있음 (참조 ID: \`${receipt}\`)`] : []),
    "",
    "### 피드백",
    "",
    ...indented,
  ].join("\n");
  return { title: `[교재 피드백] ${fields.page.slice("docs/ko/".length)}`, body };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== route) {
      return env.ASSETS ? env.ASSETS.fetch(request) : error(404, "not_found");
    }
    if (request.method !== "POST") {
      return Response.json({ error: "method_not_allowed" }, {
        status: 405,
        headers: { ...responseHeaders, Allow: "POST" },
      });
    }
    const origin = request.headers.get("Origin");
    if (origin !== null && origin !== url.origin) return error(403, "origin_not_allowed");
    const contentType = request.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase();
    if (contentType !== "application/json") return error(400, "invalid_feedback");

    const body = await readBody(request);
    if (body.tooLarge) return error(413, "feedback_too_large");
    const fields = feedbackFields(body.value);
    if (!fields) return error(400, "invalid_feedback");

    const token = env.GITHUB_ISSUES_TOKEN;
    if (!token || !env.FEEDBACK_CLIENT_LIMITER || !env.FEEDBACK_SITE_LIMITER) {
      return error(503, "service_unavailable");
    }
    try {
      const key = request.headers.get("CF-Connecting-IP") || "unknown";
      if (!(await env.FEEDBACK_CLIENT_LIMITER.limit({ key })).success ||
          !(await env.FEEDBACK_SITE_LIMITER.limit({ key: "book-feedback" })).success) {
        return error(429, "rate_limited");
      }
    } catch {
      return error(503, "service_unavailable");
    }

    let receipt;
    if (fields.email) {
      receipt = crypto.randomUUID();
      try {
        await env.FEEDBACK_CONTACTS.put(receipt, fields.email, { expirationTtl: 2_592_000 });
      } catch {
        return error(503, "contact_unavailable");
      }
    }

    try {
      const result = await fetch(`https://api.github.com/repos/${repository}/issues`, {
        method: "POST",
        headers: {
          Accept: "application/vnd.github+json",
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
          "User-Agent": "tutorial-robotics-feedback",
          "X-GitHub-Api-Version": "2022-11-28",
        },
        body: JSON.stringify(issueContent(fields, receipt)),
        redirect: "error",
        signal: AbortSignal.timeout(10_000),
      });
      if (result.status >= 400 && result.status < 500 && receipt) {
        // A rejected issue has no corresponding contact. Expiration covers cleanup failures.
        await env.FEEDBACK_CONTACTS.delete(receipt).catch(() => {});
      }
      if (result.status !== 201) return error(502, "issue_not_created");
      const { html_url: issueUrl } = await result.json();
      if (typeof issueUrl !== "string" || !issueUrlPattern.test(issueUrl)) {
        return error(502, "issue_not_created");
      }
      return Response.json({ url: issueUrl }, { status: 201, headers: responseHeaders });
    } catch {
      return error(502, "issue_not_created");
    }
  },
};
