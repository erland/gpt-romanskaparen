#!/usr/bin/env python3
"""Build the shared project-template bundle from the canonical core template."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "core" / "templates" / "romanprojekt"
TARGETS = (
    ROOT / "distributions" / "gpt" / "project-template-bundle.md",
    ROOT / "distributions" / "project" / "project-template-bundle.md",
)

LANG_BY_SUFFIX = {
    ".css": "css",
    ".json": "json",
    ".md": "markdown",
    ".py": "python",
    ".tex": "latex",
    ".yaml": "yaml",
    ".yml": "yaml",
}


def build_bundle() -> str:
    files = sorted(path for path in SOURCE.rglob("*") if path.is_file())
    lines = [
        "# Romanprojektmall – genererad från Romanskaparen Core",
        "",
        "Denna fil är genererad från `core/templates/romanprojekt/`.",
        "Ändra inte distributionens bundle manuellt; ändra kärnmallen och kör byggskriptet.",
        "",
    ]
    for path in files:
        relative = path.relative_to(SOURCE).as_posix()
        language = LANG_BY_SUFFIX.get(path.suffix.lower(), "text")
        content = path.read_text(encoding="utf-8")
        lines.extend(
            [
                f"## `{relative}`",
                "",
                f"`````{language}",
                content.rstrip("\n"),
                "`````",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated targets are stale")
    args = parser.parse_args()

    expected = build_bundle()
    stale: list[Path] = []
    for target in TARGETS:
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != expected:
                stale.append(target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected, encoding="utf-8")
            print(f"Wrote {target.relative_to(ROOT)}")

    if stale:
        for target in stale:
            print(f"STALE: {target.relative_to(ROOT)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
