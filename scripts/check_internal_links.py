from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def target_exists(source: Path, target: str) -> bool:
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return True
    target = unquote(target.split("#", 1)[0]).strip()
    if not target:
        return True
    if target.startswith("/"):
        candidate = DOCS / target.strip("/")
    else:
        candidate = source.parent / target
    if candidate.suffix:
        return candidate.exists()
    return candidate.exists() or (candidate / "index.md").exists() or candidate.with_suffix(".md").exists()


def main() -> int:
    broken: list[tuple[str, str]] = []
    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).strip()
            if not target_exists(path, target):
                broken.append((path.relative_to(ROOT).as_posix(), target))
    if broken:
        print("Broken internal links:")
        for source, target in broken:
            print(f"- {source} -> {target}")
        return 1
    print("No broken internal links detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
