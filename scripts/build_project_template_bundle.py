#!/usr/bin/env python3
"""Build project-template-bundle.md deterministically from templates/romanprojekt.

Run from the repository root:

    python scripts/build_project_template_bundle.py
    python scripts/build_project_template_bundle.py --check

The generator keeps the monolithic GPT Knowledge file synchronized with the
actual template directory. It does not alter template files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "templates" / "romanprojekt"
OUTPUT = REPO_ROOT / "project-template-bundle.md"

LANGUAGES = {
    ".json": "json",
    ".py": "python",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".css": "css",
    ".tex": "latex",
    ".md": "markdown",
}

PREFERRED_ORDER = [
    "README.md",
    "project-manifest.json",
    "revision-log.md",
    "project-index.md",
    "arbetslogg.md",
    "kapitelplan.md",
    "projektstatus.md",
    "roman-bibel.md",
    "synopsis.md",
    "stilguide.md",
    "tidslinje.md",
    "kontinuitetsanteckningar.md",
    "revisionsonskemal.md",
    "kapitelnoteringar.md",
    "karaktarer/huvudperson.md",
    "karaktarer/antagonist.md",
    "karaktarer/bifigurer.md",
    "kapitel/kapitelmall.md",
    "scripts/project_integrity.py",
    "publishing/metadata.yaml",
    "publishing/epub.css",
    "publishing/pdf-template.tex",
    "publishing/build-notes.md",
    "publishing/fix-epub-after-pandoc.py",
    "exports/README.md",
    "exports/exportlogg.md",
]

HEADER = """# Romanprojektmall – revisionslåst ZIP/GitHub-version

Detta är den samlade projektmallen för Romanskaparen. Den genereras deterministiskt från `templates/romanprojekt/` och innehåller schema 2, ZIP/GitHub-lagringsmetadata och det filsystembaserade integritetsverktyget.

Nya projekt initieras i valt kanoniskt lagringsläge. ZIP- och GitHub-projekt använder samma interna revisioner, manifest, SHA-256-hashar och kapitelskydd. GitHub-API, branchlås, commits och pull requests hanteras av GPT-arbetsflödet, inte av integritetsverktyget.

Mallen `kapitel/kapitelmall.md` finns från början, men numeriska kapitelfiler skapas först när kapiteltext finns.
"""

FOOTER = """
## Obligatoriskt lagringsbeteende

- Välj och lås exakt en kanonisk projektkälla per operation.
- Kör `verify` före ändring.
- Använd förväntad revision och strikt `--allow`-lista vid intern commit.
- Vid nytt kapitel får inga befintliga kapitelfiler ändras.
- Vid revision av ett kapitel får inga andra kapitelfiler ändras.
- ZIP-läge: paketera, återöppna och verifiera leverans-ZIP:en.
- GitHub-läge: kontrollera branch-head igen före publicering, använd aldrig force push och skapa eller återanvänd PR mot default branch.
- Leverera en lagringsanpassad revisionskvittens.
"""


def template_paths() -> list[Path]:
    discovered = {
        path.relative_to(TEMPLATE_ROOT).as_posix(): path
        for path in TEMPLATE_ROOT.rglob("*")
        if path.is_file() and ".DS_Store" not in path.parts
    }
    missing = [name for name in PREFERRED_ORDER if name not in discovered]
    if missing:
        raise ValueError("Mallen saknar förväntade filer: " + ", ".join(missing))
    extras = sorted(name for name in discovered if name not in PREFERRED_ORDER)
    return [discovered[name] for name in PREFERRED_ORDER + extras]


def fence_for(content: str) -> str:
    longest = 3
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("`"):
            count = len(stripped) - len(stripped.lstrip("`"))
            longest = max(longest, count + 1)
    return "`" * longest


def render_file(path: Path) -> str:
    relative = path.relative_to(TEMPLATE_ROOT).as_posix()
    content = path.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content += "\n"
    fence = fence_for(content)
    language = LANGUAGES.get(path.suffix.lower(), "text")
    return f"\n## `{relative}`\n\n{fence}{language}\n{content}{fence}\n"


def build() -> str:
    parts = [HEADER.rstrip() + "\n"]
    parts.extend(render_file(path) for path in template_paths())
    parts.append(FOOTER.lstrip())
    return "".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in bundle is stale")
    args = parser.parse_args()

    generated = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != generated:
            print("FEL: project-template-bundle.md är inte synkad med templates/romanprojekt/", file=sys.stderr)
            return 1
        print("OK: project-template-bundle.md är synkad.")
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"Skapade {OUTPUT.relative_to(REPO_ROOT)} ({len(generated.encode('utf-8'))} byte).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
