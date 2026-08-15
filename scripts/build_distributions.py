#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates" / "romanprojekt"
KNOWLEDGE_ROOT = ROOT / "knowledge-upload"
BUNDLE_PATH = ROOT / "project-template-bundle.md"
VERSION_PATH = ROOT / "VERSION"

KNOWLEDGE_FILES = [
    "01-arbetsflode-och-nyborjarstod.md",
    "02-berattelsehantverk.md",
    "03-karaktarer-varld-och-kontinuitet.md",
    "04-genreguider.md",
    "05-projektstruktur-och-synk.md",
]

BUNDLE_INTRO = """# Romanprojektmall – revisionslåst version

Detta är den samlade projektmallen för Romanskaparen. Den innehåller manifest, revisionslogg och ett deterministiskt integritetsverktyg som skyddar befintliga kapitel mot oavsiktlig ändring eller återställning. Verktyget har även ett särskilt `audit-legacy`-läge för projektzippar skapade före manifeststandarden.

När ett nytt projekt skapas ska `scripts/project_integrity.py init` köras innan den första zipen levereras. Ett äldre manifestlöst projekt ska först granskas direkt som zip med `audit-legacy`; därefter skapas en separat revisionslåst migrationsbaslinje där befintliga kapitel måste vara byte-identiska med källzipen. Därefter ska varje filbaserad ändring verifieras, committas med en explicit ändringslista och kontrolleras igen efter att zipen skapats.

Mallen `kapitel/kapitelmall.md` finns från början, men inga numeriska kapitelfiler skapas förrän kapiteltexten faktiskt finns. Det förhindrar att tomma mallkapitel räknas som färdiga kapitel.

"""

BUNDLE_FILE_ORDER = [
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

BUNDLE_FOOTER = """## Obligatoriskt chatt- och zip-beteende\n\n- Välj exakt en uttryckligen angiven indata-zip.\n- Avbryt om rätt zip inte är åtkomlig eller om flera kandidater är oklara.\n- Packa alltid upp i en ny tom katalog.\n- Kör `verify` före ändringar.\n- Använd strikt `--allow`-lista vid `commit`.\n- Vid nytt kapitel får inga befintliga kapitelfiler ändras.\n- Vid revision av ett kapitel får inga andra kapitelfiler ändras.\n- Skapa en ny revision, paketera hela projektet, packa upp leveranszipen och kör `verify` igen.\n- Leverera revisionskvittens tillsammans med zipen.\n"""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def language_for(path: Path) -> str:
    return {
        ".md": "markdown",
        ".json": "json",
        ".py": "python",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".css": "css",
        ".tex": "latex",
    }.get(path.suffix.lower(), "text")


def fence_for(text: str) -> str:
    # Minst fem backticks bevarar originalbundle-formatet; väx om innehållet kräver mer.
    longest = 4
    run = 0
    for ch in text:
        if ch == "`":
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return "`" * (longest + 1)


def render_bundle() -> str:
    parts = [BUNDLE_INTRO]
    actual = {
        p.relative_to(TEMPLATE_ROOT).as_posix(): p
        for p in TEMPLATE_ROOT.rglob("*")
        if p.is_file()
    }
    expected = set(BUNDLE_FILE_ORDER)
    missing = [name for name in BUNDLE_FILE_ORDER if name not in actual]
    extra = sorted(set(actual) - expected)
    if missing or extra:
        details = []
        if missing:
            details.append(f"saknade: {', '.join(missing)}")
        if extra:
            details.append(f"nya ej ordnade filer: {', '.join(extra)}")
        raise RuntimeError(
            "Mallens filuppsättning avviker från den revisionslåsta bundle-ordningen ("
            + "; ".join(details)
            + "). Uppdatera BUNDLE_FILE_ORDER medvetet innan distribution byggs."
        )

    for rel in BUNDLE_FILE_ORDER:
        path = actual[rel]
        text = path.read_text(encoding="utf-8")
        fence = fence_for(text)
        parts.append(f"## `{rel}`\n\n{fence}{language_for(path)}\n{text.rstrip()}\n{fence}\n\n")
    parts.append(BUNDLE_FOOTER)
    return "".join(parts)


def write_bundle(check: bool = False) -> None:
    rendered = render_bundle()
    if check:
        current = BUNDLE_PATH.read_text(encoding="utf-8") if BUNDLE_PATH.exists() else ""
        if current != rendered:
            raise SystemExit(
                "project-template-bundle.md är inte synkad med templates/romanprojekt/. "
                "Kör scripts/build_distributions.py --sync-bundle."
            )
        return
    BUNDLE_PATH.write_text(rendered, encoding="utf-8")


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def write_portable_manifest(package_root: Path, version: str) -> None:
    files = []
    for path in sorted(p for p in package_root.rglob("*") if p.is_file() and p.name != "MANIFEST.json"):
        files.append({
            "path": path.relative_to(package_root).as_posix(),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    manifest = {
        "package": "romanskaparen",
        "format": "portable-chat-assistant",
        "format_version": 1,
        "version": version,
        "entrypoint": "START-HERE.md",
        "instructions": "assistant/instructions.md",
        "knowledge": [f"knowledge/{name}" for name in KNOWLEDGE_FILES] + [
            "knowledge/project-template-bundle.md"
        ],
        "template_root": "templates/romanprojekt",
        "files": files,
    }
    (package_root / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def zip_dir(src: Path, dst: Path) -> None:
    # Deterministisk ZIP: samma filinnehåll ger samma arkivhash oavsett byggmaskin och mtime.
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in src.rglob("*") if p.is_file()):
            rel = path.relative_to(src).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100644 << 16)
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"ZIP-integritetsfel i {path.name}: {bad}")
        if not zf.namelist():
            raise RuntimeError(f"Tom ZIP: {path.name}")


def build(output_dir: Path) -> list[Path]:
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    if not version:
        raise RuntimeError("VERSION är tom.")

    write_bundle(check=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        custom = tmp / "romanskaparen-custom-gpt"
        custom.mkdir()
        for name in ["README.md", "SETUP.md", "gpt-instructions.md", "conversation-starters.md", "project-template-bundle.md", "VERSION"]:
            copy_file(ROOT / name, custom / name)
        for name in KNOWLEDGE_FILES:
            copy_file(KNOWLEDGE_ROOT / name, custom / "knowledge-upload" / name)
        custom_zip = output_dir / f"romanskaparen-custom-gpt-v{version}.zip"
        zip_dir(custom, custom_zip)

        portable = tmp / "romanskaparen-chat"
        portable.mkdir()
        copy_file(ROOT / "portable" / "START-HERE.md", portable / "START-HERE.md")
        copy_file(VERSION_PATH, portable / "VERSION")
        copy_file(ROOT / "gpt-instructions.md", portable / "assistant" / "instructions.md")
        for name in KNOWLEDGE_FILES:
            copy_file(KNOWLEDGE_ROOT / name, portable / "knowledge" / name)
        copy_file(BUNDLE_PATH, portable / "knowledge" / "project-template-bundle.md")
        copy_tree(TEMPLATE_ROOT, portable / "templates" / "romanprojekt")
        write_portable_manifest(portable, version)
        portable_zip = output_dir / f"romanskaparen-chat-v{version}.zip"
        zip_dir(portable, portable_zip)

    for path in (custom_zip, portable_zip):
        verify_zip(path)
    return [custom_zip, portable_zip]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bygg Romanskaparens Custom GPT- och portabla chat-distributioner.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--sync-bundle", action="store_true", help="Generera project-template-bundle.md från templates/romanprojekt/ och avsluta.")
    parser.add_argument("--check-bundle", action="store_true", help="Kontrollera att project-template-bundle.md är synkad och avsluta.")
    args = parser.parse_args()

    if args.sync_bundle:
        write_bundle(check=False)
        print(f"Synkade {BUNDLE_PATH.relative_to(ROOT)}")
        return 0
    if args.check_bundle:
        write_bundle(check=True)
        print("OK: project-template-bundle.md är synkad med templates/romanprojekt/.")
        return 0

    built = build(args.output_dir)
    for path in built:
        print(f"OK: {path} ({path.stat().st_size} bytes, sha256={sha256(path)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
