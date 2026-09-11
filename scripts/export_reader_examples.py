"""Copy public measured figures only; keep raw runs and learner records local."""
import json
import shutil
from pathlib import Path

from pai_lab.catalog import ROOT, resolve_lesson
from pai_lab.lessons.evidence import validate_run


def main() -> None:
    state=json.loads((ROOT/'.local/reader-redesign/course/progress.json').read_text())
    for identifier, entry in state['completed'].items():
        resolve_lesson(identifier)
        source=Path(entry['run_dir']);source=source if source.is_absolute() else ROOT/source
        errors=validate_run(identifier,source)
        if errors:raise ValueError(f'{identifier}: {errors}')
        for kind in ('plot','frame'):
            image=source/f'{kind}.png'
            if image.exists():shutil.copyfile(image,ROOT/f'docs/assets/examples/{identifier}-{kind}.png')
    print(f"Exported measured figures for {len(state['completed'])} public lessons")


if __name__=='__main__':main()
