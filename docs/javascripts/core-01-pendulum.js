(() => {
  const captions = {
    ko: {
      label: "좌우로 흔들리는 진자의 개념도",
      caption: "진자의 왕복 운동을 보여 주는 개념 애니메이션입니다.",
      play: "예제 재생",
      pause: "예제 일시정지",
    },
    en: {
      label: "Illustration of a pendulum swinging from side to side",
      caption: "Concept animation of a pendulum swinging back and forth.",
      play: "Play illustration",
      pause: "Pause illustration",
    },
  };

  function addIllustration(container) {
    const labels = captions[container.dataset.language] ?? captions.en;
    const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
    const figure = document.createElement("figure");
    figure.className = "pendulum-illustration";
    figure.innerHTML = `
      <div class="pendulum-illustration__scene" role="img">
        <div class="pendulum-illustration__pivot">
          <div class="pendulum-illustration__arm"></div>
        </div>
      </div>
      <figcaption class="pendulum-illustration__caption">
        <span></span>
        <button type="button"></button>
      </figcaption>
    `;

    figure.querySelector("[role=img]").setAttribute("aria-label", labels.label);
    figure.querySelector("figcaption span").textContent = labels.caption;
    const playback = figure.querySelector("button");
    let paused = motionPreference.matches;

    function setPaused(value) {
      paused = value;
      figure.dataset.paused = String(paused);
      playback.textContent = paused ? labels.play : labels.pause;
    }

    setPaused(paused);
    playback.addEventListener("click", () => setPaused(!paused));
    motionPreference.addEventListener("change", ({ matches }) => setPaused(matches));
    container.append(figure);
  }

  function showIllustrations() {
    document.querySelectorAll(".core-01-pendulum").forEach(addIllustration);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showIllustrations, { once: true });
  } else {
    showIllustrations();
  }
})();
