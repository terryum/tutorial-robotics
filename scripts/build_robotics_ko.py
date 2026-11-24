"""Build the Korean robotics textbook as one offline HTML file."""

from __future__ import annotations

import argparse
import base64
import json
import re
from html import escape, unescape
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book/robotics-ko"
CHAPTERS = {
    "foundations": "공통 기초",
    "manipulation": "로봇 시뮬레이션 · 매니퓰레이션",
    "mobile": "로봇 시뮬레이션 · 이동 로봇",
    "workstation": "워크스테이션 실습",
    "hardware": "로봇 하드웨어 실습",
}
LESSONS = {
    "foundations": ("core-01", "core-data-01", "core-il-01", "core-rl-01", "sim-ros-01"),
    "manipulation": (
        "core-enlight-02",
        "core-enlight-03",
        "core-enlight-04",
        "core-enlight-05",
        "core-fr3-04",
        "core-fr3-09",
        "core-fr3-10",
    ),
    "workstation": ("sim-enlight-03", "sim-enlight-04", "sim-enlight-05"),
    "hardware": ("core-teleop-01",),
}
FIGURES = {
    "foundations": (
        ("pendulum.png", "진자 에너지 기록. 64개 표본의 기준값과 관측값을 겹쳐 표시합니다."),
        ("arm.svg", "2링크 팔의 구성공간 경로와 작업공간 장애물."),
    ),
    "manipulation": (
        ("pick-rgb.png", "Enlight 작업 장면의 색 영상."),
        ("pick-mask.png", "색 영상에서 분할한 물체 마스크."),
        ("pick-lift.png", "알려진 자세와 RGB-D 경로의 물체 높이 기록."),
    ),
    "mobile": (
        ("slam-scan.png", "2D LiDAR 스캔과 벽의 거리 관측."),
        ("slam-map.png", "오도메트리와 SLAM 궤적, 점유 격자 비교."),
    ),
    "workstation": (("enlight-home.png", "Mac MuJoCo의 Enlight 초기 자세와 고정 카메라 시야."),),
    "hardware": (("xr.png", "합성 입력을 재생했을 때 차단과 복구 구간."),),
}
WS_STATUS = {"passed": "통과", "blocked": "차단", "failed": "실패", "pending": "현장 확인 대기"}


def data_file(name: str) -> dict:
    value = json.loads((BOOK / name).read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"unsupported evidence schema: {name}")
    return value


def chapter_html(chapter: str, body: str) -> str:
    # Prefix subsection IDs so repeated lesson headings cannot collide.
    def slug(value: str, separator: str) -> str:
        return chapter + "--" + slugify_unicode(value, separator)

    fragment = markdown.markdown(
        body,
        extensions=["tables", "fenced_code", "toc", "md_in_html"],
        extension_configs={"toc": {"slugify": slug, "baselevel": 2}},
        output_format="html5",
    )
    fragment = re.sub(
        r'<p><img alt="([^"]+)" src="figures/([a-z0-9.-]+)"></p>',
        lambda match: figure(match[2], unescape(match[1])),
        fragment,
    )
    for slug in CHAPTERS:
        fragment = fragment.replace(f'href="{slug}.md#', f'href="#{slug}--')
    return fragment.replace("<table>", '<div class="table-scroll"><table>').replace(
        "</table>", "</table></div>"
    )


def figure(filename: str, caption: str) -> str:
    path = BOOK / "figures" / filename
    mime = {".png": "image/png", ".svg": "image/svg+xml"}[path.suffix]
    image = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        f'<figure><img src="data:{mime};base64,{image}" alt="{escape(caption)}">'
        f"<figcaption>{escape(caption)}</figcaption></figure>"
    )


def mac_rows(chapter: str, evidence: dict) -> str:
    rows = []
    for identifier in LESSONS.get(chapter, ()):
        entry = evidence["lessons"].get(identifier, {})
        if entry.get("status") == "passed":
            metrics = entry["metrics"]
            value = f"{metrics['metric']} = {metrics['value']:.5g} {metrics['unit']}"
            evaluation = metrics.get("evaluation")
            if evaluation:
                value = (
                    f"학습 실행 통과 · 독립 목표 {evaluation['successes']}/"
                    f"{evaluation['attempts']} · 기준 {evaluation['required_successes']}회 · "
                    + ("성능 통과" if evaluation["passed"] else "성능 기준 미달")
                )
            elif "heldout_mse" in metrics:
                value += f" · 보류 시연 MSE {metrics['heldout_mse']:.5g}"
            badge = "Mac 직접 실행"
        else:
            badge = "현장 확인 대기"
            value = "지원 환경에서 실행해야 합니다."
        rows.append((identifier, badge, value))
    return result_table(rows) if rows else ""


def result_table(rows: list[tuple[str, str, str]]) -> str:
    cells = "".join(
        "<tr>" + "".join(f"<td>{escape(value)}</td>" for value in row) + "</tr>" for row in rows
    )
    return (
        '<div class="table-scroll"><table><thead><tr><th scope="col">실습</th>'
        '<th scope="col">검증 상태</th><th scope="col">근거</th></tr></thead>'
        f"<tbody>{cells}</tbody></table></div>"
    )


def ws2_table(data: dict) -> str:
    rows = [
        (entry["title"], WS_STATUS[entry["status"]], entry["evidence"]) for entry in data["checks"]
    ]
    provenance = ""
    if data["source_commit"]:
        if not re.fullmatch(r"[0-9a-f]{40}", data["source_commit"]):
            raise ValueError("WS2 report requires a full Git SHA")
        provenance = (
            f"<p>검증한 커밋 <code>{data['source_commit']}</code><br>"
            f"실행 환경 {escape(data['environment'])}</p>"
        )
    return '<h3 id="ws2-results">WS2 검증 결과</h3>' + provenance + result_table(rows)


def build() -> str:
    css = (BOOK / "book.css").read_text(encoding="utf-8")
    evidence = data_file("mac-results.json")
    ws2 = data_file("ws2-results.json")
    nav = "".join(f'<li><a href="#{slug}">{title}</a></li>' for slug, title in CHAPTERS.items())
    sections = []
    for slug in CHAPTERS:
        chapter = (BOOK / f"{slug}.md").read_text(encoding="utf-8")
        results = mac_rows(slug, evidence)
        if slug == "workstation":
            results += ws2_table(ws2)
        appendix = (
            f'<aside class="evidence" aria-label="검증 근거">{results}</aside>' if results else ""
        )
        figures = "".join(figure(*item) for item in FIGURES.get(slug, ()))
        sections.append(
            f'<section id="{slug}">{chapter_html(slug, chapter)}{appendix}{figures}'
            '<a class="back" href="#contents">목차로 돌아가기 ↑</a></section>'
        )
    intro = chapter_html("intro", (BOOK / "index.md").read_text(encoding="utf-8"))
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy"
      content="default-src 'none'; style-src 'unsafe-inline'; img-src data:;">
<title>로보틱스 실습 교재</title>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">본문으로 건너뛰기</a>
<header><div class="inner"><h1>로보틱스 실습 교재</h1>
<p>진자의 상태에서 로봇의 계획, 제어, 학습까지</p></div></header>
<div class="layout">
<nav id="contents" aria-label="교재 목차"><strong>목차</strong><ol>{nav}</ol></nav>
<main id="main">
<section aria-label="교재 사용법">
<h2>실습을 시작하기 전에</h2>
{intro}
</section>
{"".join(sections)}
</main>
</div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/robotics-ko/index.html")
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
