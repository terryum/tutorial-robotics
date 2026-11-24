"""Keep GitHub-relative source links valid when the same Markdown becomes a site."""

from __future__ import annotations

import json
import posixpath
import re
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?P<opening>!?\[[^\]]*\]\()(?P<href>[^)\s]+)(?P<closing>\))")


def render_source_links(markdown: str, source: Path, root: Path = ROOT) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match["href"]
        if href.startswith(("#", "http:", "https:", "mailto:")):
            return match[0]
        path, separator, anchor = href.partition("#")
        target = (source.parent / unquote(path)).resolve()
        if not target.is_file() or not target.is_relative_to(root):
            return match[0]
        if target.is_relative_to(root / "docs"):
            return match[0]
        url = "https://github.com/terryum/tutorial-robotics/blob/main/" + quote(
            target.relative_to(root).as_posix(), safe="/"
        )
        return match["opening"] + url + (separator + anchor if separator else "") + match["closing"]

    return LINK.sub(replace, markdown)


def on_page_markdown(markdown, page, **kwargs):
    source = Path(page.file.abs_src_path)
    uri = page.file.src_uri
    if uri == "ko/index.md":
        # Keep the generated catalog available in the GitHub Markdown.
        markdown = re.sub(
            r"<!-- pal:catalog:start -->.*?<!-- pal:catalog:end -->",
            "",
            markdown,
            flags=re.DOTALL,
        )
        markdown = markdown.replace("## 전체 수업 목록\n", "")
    elif uri.startswith("ko/lessons/") and source.stem != "core-00":
        # The Korean site supplies the stage-based previous/next links.
        markdown = re.sub(
            r"<!-- pal:navigation:start -->.*?<!-- pal:navigation:end -->",
            "",
            markdown,
            flags=re.DOTALL,
        )
    return render_language_links(
        render_source_links(markdown, source),
        source,
        use_directory_urls=kwargs["config"].use_directory_urls,
    )


def render_language_links(
    markdown: str, source: Path, root: Path = ROOT, *, use_directory_urls: bool = True
) -> str:
    """Raw HTML anchors bypass MkDocs' Markdown-link conversion."""

    def url(path: Path) -> str:
        relative = path.relative_to(root / "docs")
        if not use_directory_urls:
            return relative.with_suffix(".html").as_posix()
        return (
            relative.parent if relative.name == "index.md" else relative.with_suffix("")
        ).as_posix()

    def replace(match: re.Match[str]) -> str:
        target = (source.parent / match["href"]).resolve()
        if not target.is_file() or not target.is_relative_to(root / "docs"):
            return match[0]
        if use_directory_urls:
            href = posixpath.relpath(url(target), url(source)).rstrip("/") + "/"
        else:
            href = posixpath.relpath(url(target), posixpath.dirname(url(source)) or ".")
        return match["opening"] + href + match["closing"]

    return re.sub(
        r'(?P<opening><a\s+href=")(?P<href>[^"]+)(?P<closing>"\s+lang="(?:en|ko)">)',
        replace,
        markdown,
    )


# Reading stages group the catalog by the learner's equipment progression.
STAGES = {
    "foundations": (
        "공통 기초",
        "진자 실험부터 모델과 렌더링까지 배웁니다. 지원되는 Apple Silicon Mac 또는 Linux x86-64에서 Core 환경을 사용합니다.",
    ),
    "local": (
        "로봇 시뮬레이션 실습",
        "MuJoCo에서 로봇 모델·제어·학습을 실습합니다. 지원되는 Apple Silicon Mac 또는 Linux x86-64를 사용합니다.",
    ),
    "workstation": (
        "워크스테이션 실습",
        "수업에 따라 Ubuntu 24.04에서 ROS 2만 사용하거나 NVIDIA GPU로 Isaac·학습을 실행합니다. 기록 분석과 오프라인 배포 검사는 지원되는 Mac에서도 할 수 있습니다.",
    ),
    "hardware": (
        "로봇 하드웨어 실습",
        "선택형 XR·시연 수집과 실물 로봇 준비를 다룹니다. 수업별로 합성 입력, 오프라인 재생, 실제 장비 점검에 필요한 환경을 확인하세요.",
    ),
}
FOUNDATIONS = ("core-01", "core-02", "core-03", "core-04")
COLLECTION = {"sim-teleop-01", "sim-teleop-02", "sim-enlight-06"}
TOPICS = {
    "simulation": "시뮬레이션과 재현성",
    "kinematics": "좌표계와 기구학",
    "control-contact": "제어와 접촉",
    "reinforcement-learning": "강화학습",
    "data-imitation": "데이터와 모방학습",
    "robot-hands": "로봇 손",
    "mobile-motion": "이동형 로봇과 모션",
    "ros": "ROS 통신",
    "physx": "PhysX와 엔진 비교",
    "vla": "비전·언어·행동",
    "deployment-hardware": "배포와 실물 검증",
}
PLATFORMS = {
    "macos-arm64": "Apple Silicon Mac",
    "linux-x86_64": "Linux x86-64",
    "ubuntu-24.04-x86_64": "Ubuntu 24.04 x86-64",
}
CAPABILITIES = {
    "python-3.12": "Python 3.12",
    "numpy": "NumPy",
    "mujoco": "MuJoCo",
    "ros2-jazzy": "ROS 2 Jazzy",
    "isaac-sim": "NVIDIA GPU + Isaac Sim",
    "nvidia-cuda": "NVIDIA GPU + CUDA",
    "robot-runtime": "로봇 런타임",
    "isolated-network": "격리 네트워크",
    "fr3-hardware": "FR3 실물",
    "wuji-hardware": "Wuji Hand 2 Beta 2 실물",
    "enlight-hardware": "Enlight 실물",
    "read-only-preflight-fr3": "FR3 읽기 전용 사전 점검",
    "read-only-preflight-wuji": "Wuji 읽기 전용 사전 점검",
    "read-only-preflight-enlight": "Enlight 읽기 전용 사전 점검",
}
LESSON_REQUIREMENTS = {
    "core-teleop-01": "합성 입력을 사용하며 XR 장비 없이 실습합니다.",
    "sim-fr3-04": "별도로 검증된 MuJoCo와 PhysX 실행 기록이 필요합니다. Mac에서는 기록을 분석합니다.",
    "sim-deploy-01": "검증할 후보 실행 기록이 필요합니다. 오프라인에서 검사합니다.",
    "sim-teleop-01": "실제 입력 검증에는 Ubuntu와 호환되는 Quest 3·MANUS 장갑·VIVE 트래커, SDK 및 보정이 필요합니다.",
    "sim-teleop-02": "합성 입력으로 정합과 명령 차단을 확인합니다. 실제 장비 입력 검증은 별도입니다.",
    "sim-enlight-06": "합성 손목 입력으로 시뮬레이션 시연을 수집합니다. XR 장비와 실물 팔은 필요하지 않습니다.",
    "hw-common-01": "검증된 후보로 오프라인 재생과 명령 차단을 확인합니다. 실물 연결은 필요하지 않습니다.",
    "hw-common-02": "실물 연결 전 읽기 전용 준비 절차를 확인합니다.",
    "hw-enlight-05": "별도로 검토한 프로브·하중과 힘 제어기가 필요합니다.",
    "hw-enlight-06": "별도로 검토한 그리퍼·하중과 제어기가 필요합니다.",
}


def reading_stage(lesson):
    if lesson["id"] in FOUNDATIONS:
        return "foundations"
    if lesson["id"] in COLLECTION:
        return "hardware"
    return {"core": "local", "sim": "workstation", "hardware": "hardware"}[lesson["stage"]]


def on_files(files, config):
    def load(name):
        return json.loads((ROOT / "curriculum" / f"{name}.json").read_text(encoding="utf-8"))

    def link(src, title):
        return {"url": files.get_file_from_path(src).url, "title": title}

    home = link("ko/home.md", "홈")
    learning_map = link("ko/index.md", "커리큘럼")
    safety = link("07_SAFETY.md", "안전 지침")
    stages = {
        key: {"id": key, "title": title, "description": description, "lessons": [], "topics": {}}
        for key, (title, description) in STAGES.items()
    }
    entries = {}
    topics = load("book-topics")
    # Keep optional collection lessons before physical robot preparation in the merged stage.
    catalog = sorted(
        load("catalog")["lessons"],
        key=lambda lesson: (lesson["stage"] == "hardware", lesson["order"]),
    )
    for lesson in catalog:
        lesson_id = lesson["id"]
        entry = link(f"ko/lessons/{lesson_id}.md", lesson["title_ko"])
        entry.update(id=lesson_id, requirement=LESSON_REQUIREMENTS.get(lesson_id))
        if not lesson.get("diagnostic"):
            stage = stages[reading_stage(lesson)]
            topic = topics[lesson_id][0]
            capabilities = [
                CAPABILITIES.get(capability, capability) for capability in lesson["capabilities"]
            ]
            if {"isaac-sim", "nvidia-cuda"}.issubset(lesson["capabilities"]):
                capabilities[capabilities.index("NVIDIA GPU + Isaac Sim")] = (
                    "NVIDIA GPU + Isaac Sim + CUDA"
                )
                capabilities.remove("NVIDIA GPU + CUDA")
            entry.update(
                stage=stage["id"],
                topic=topic,
                platforms=", ".join(PLATFORMS.get(p, p) for p in lesson["platforms"]),
                capabilities=", ".join(capabilities),
            )
            stage["lessons"].append(entry)
            stage["topics"].setdefault(topic, {"title": TOPICS[topic], "lessons": []})[
                "lessons"
            ].append(entry)
        entries[lesson_id] = entry

    sequence = [
        home,
        learning_map,
        *(lesson for stage in stages.values() for lesson in stage["lessons"]),
    ]
    pagination = {
        current["url"]: (previous, following)
        for previous, current, following in zip([None, *sequence], sequence, [*sequence[1:], None])
    }

    config.extra["korean_book"] = {
        "home": home,
        "map": learning_map,
        "safety": safety,
        "sources": link("SOURCES.md", "외부 소스 목록"),
        "diagnostic": entries["core-00"],
        "entries": entries,
        "stages": stages,
        "pagination": pagination,
    }


def on_page_context(context, page, config, **kwargs):
    if page.file.src_uri.startswith("ko/"):
        book = config.extra["korean_book"]
        context["book"] = book
        context["book_current"] = (
            book["entries"].get(Path(page.file.src_uri).stem)
            if page.file.src_uri.startswith("ko/lessons/")
            else None
        )
        context["book_pagination"] = book["pagination"].get(page.url)
    return context
