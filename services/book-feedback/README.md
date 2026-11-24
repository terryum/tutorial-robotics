# 교재 피드백 서버

Cloudflare Worker가 교재와 같은 주소에서 `POST /api/book-feedback` 요청을 받고, `terryum/tutorial-robotics`에 공개 이슈를 만듭니다. GitHub 계정 없이 제출할 수 있으며, 이슈 작성자는 서버에 연결한 계정으로 표시됩니다. 선택적으로 입력한 GitHub 아이디는 본인이 적은 값으로 표시합니다.

## 검증과 배포

저장소 루트에서 한국어 폼과 영문 페이지를 포함한 MkDocs 사이트를 빌드하고 Worker를 검사합니다.

```sh
.venv/bin/mkdocs build --strict
node --test services/book-feedback/worker.test.mjs
wrangler deploy --config services/book-feedback/wrangler.toml --dry-run
```

실제 접수에는 이 저장소에만 접근할 수 있고 **Issues: Read and write** 권한을 가진 GitHub fine-grained 토큰이 필요합니다. 토큰은 Cloudflare Worker의 `GITHUB_ISSUES_TOKEN` 비밀 값으로만 설정합니다. [GitHub 이슈 API의 권한 안내](https://docs.github.com/en/rest/issues/issues#create-an-issue)를 참고하세요.

이메일 답변을 받으려면 전용 Workers KV 네임스페이스를 생성하고 설정에 연결합니다. 발급받은 네임스페이스 ID를 아래 예의 값 대신 사용합니다.

```toml
[[kv_namespaces]]
binding = "FEEDBACK_CONTACTS"
id = "replace-with-namespace-id"
```

```sh
wrangler secret put GITHUB_ISSUES_TOKEN --config services/book-feedback/wrangler.toml
wrangler deploy --config services/book-feedback/wrangler.toml
```

이메일은 KV에 30일 동안 보관합니다. 이슈에 표시된 참조 ID로 접수 담당자가 해당 이메일을 조회할 수 있습니다. KV 연결 없이도 이메일을 비운 피드백은 접수됩니다. Worker는 Cloudflare 위치별 요청 제한을 적용합니다. [Workers 요청 제한 설명](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)을 참고하세요.

파일로 연 HTML 미리보기에서는 접수 서버에 연결할 수 없습니다. 배포 전에는 위의 테스트로 GitHub 호출을 모의 검증합니다.
