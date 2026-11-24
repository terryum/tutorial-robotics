(() => {
  const form = document.querySelector(".book-feedback-form");
  const button = form.querySelector("button[type=submit]");
  const status = form.querySelector("[role=status]");
  const issue = /^https:\/\/github\.com\/terryum\/tutorial-robotics\/issues\/[1-9]\d*$/;
  button.disabled = false;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (location.protocol === "file:") {
      status.textContent = "파일 미리보기에서는 접수 서버에 연결할 수 없습니다. GitHub에서 직접 작성하거나 에이전트에게 요청해 주세요.";
      return;
    }

    const fields = new FormData(form);
    const feedback = {
      page: form.dataset.page,
      message: fields.get("message").trim(),
      github: fields.get("github").trim(),
      email: fields.get("email").trim(),
    };
    if (!feedback.message) {
      status.textContent = "피드백 내용을 입력해 주세요.";
      form.elements.message.focus();
      return;
    }

    button.disabled = true;
    status.textContent = "피드백을 보내는 중입니다.";
    try {
      const response = await fetch("/api/book-feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(feedback),
      });
      const result = await response.json();
      if (response.status === 201 && issue.test(result.url)) {
        const link = document.createElement("a");
        link.href = result.url;
        link.textContent = "등록된 GitHub 이슈 보기";
        status.replaceChildren("피드백을 접수했습니다. ", link);
        form.reset();
      } else if (result.error === "contact_unavailable") {
        status.textContent = "지금은 이메일을 보관할 수 없습니다. 이메일을 비운 뒤 다시 보내 주세요.";
      } else if (response.status === 429) {
        status.textContent = "잠시 후 다시 보내 주세요.";
      } else if (response.status === 400 || response.status === 413) {
        status.textContent = "피드백 길이와 선택 항목을 확인해 주세요.";
      } else {
        status.textContent = "접수를 확인하지 못했습니다. GitHub 이슈 목록을 확인하거나 직접 작성해 주세요.";
      }
    } catch {
      status.textContent = "접수를 확인하지 못했습니다. GitHub 이슈 목록을 확인하거나 직접 작성해 주세요.";
    } finally {
      button.disabled = false;
    }
  });
})();
