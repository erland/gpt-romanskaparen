#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates" / "romanprojekt"
KNOWLEDGE_ROOT = ROOT / "knowledge-upload"
BUNDLE_PATH = ROOT / "project-template-bundle.md"
VERSION_PATH = ROOT / "VERSION"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$")

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


def resolve_version(explicit_version: str | None) -> str:
    version = explicit_version if explicit_version is not None else VERSION_PATH.read_text(encoding="utf-8").strip()
    if not version:
        raise RuntimeError("Version är tom.")
    if version.startswith("v"):
        raise RuntimeError("Ange versionsnumret utan inledande v, exempelvis 1.1.0.")
    if not SEMVER_RE.fullmatch(version):
        raise RuntimeError(f"Ogiltig SemVer-version: {version}")
    return version


def write_version(path: Path, version: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(version + "\n", encoding="utf-8")


def build(output_dir: Path, explicit_version: str | None = None) -> list[Path]:
    version = resolve_version(explicit_version)

    write_bundle(check=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        custom = tmp / "romanskaparen-custom-gpt"
        custom.mkdir()
        for name in ["README.md", "SETUP.md", "gpt-instructions.md", "conversation-starters.md", "project-template-bundle.md"]:
            copy_file(ROOT / name, custom / name)
        copy_file(ROOT / "runtime-contracts" / "chatgpt-custom.json", custom / "runtime-contract.json")
        write_version(custom / "VERSION", version)
        for name in KNOWLEDGE_FILES:
            copy_file(KNOWLEDGE_ROOT / name, custom / "knowledge-upload" / name)
        custom_zip = output_dir / f"romanskaparen-custom-gpt-v{version}.zip"
        zip_dir(custom, custom_zip)

        portable = tmp / "romanskaparen-chat"
        portable.mkdir()
        copy_file(ROOT / "portable" / "START-HERE.md", portable / "START-HERE.md")
        write_version(portable / "VERSION", version)
        copy_file(ROOT / "gpt-instructions.md", portable / "assistant" / "instructions.md")
        copy_file(ROOT / "runtime-contracts" / "chatgpt-chat.json", portable / "assistant" / "runtime-contract.json")
        for name in KNOWLEDGE_FILES:
            copy_file(KNOWLEDGE_ROOT / name, portable / "knowledge" / name)
        copy_file(BUNDLE_PATH, portable / "knowledge" / "project-template-bundle.md")
        copy_tree(TEMPLATE_ROOT, portable / "templates" / "romanprojekt")
        write_portable_manifest(portable, version)
        portable_zip = output_dir / f"romanskaparen-chat-v{version}.zip"
        zip_dir(portable, portable_zip)

        plugin = tmp / "romanskaparen-openai-plugin"
        plugin.mkdir()
        skill = plugin / "skills" / "romanskaparen"
        refs = skill / "references" / "knowledge"
        assets = skill / "assets" / "romanprojekt"
        scripts_dir = skill / "scripts"
        refs.mkdir(parents=True)
        assets.mkdir(parents=True)
        scripts_dir.mkdir(parents=True)

        canonical = (ROOT / "gpt-instructions.md").read_text(encoding="utf-8").strip()
        skill_text = (
            "---\n"
            "name: romanskaparen\n"
            "description: Stateful skrivassistent för planering, skrivande, revision, versionshantering och export av revisionslåsta romanprojekt.\n"
            "---\n\n"
            "# Romanskaparen\n\n"
            "## Plugin-runtime\n\n"
            "- Full filbaserad projektfunktion kräver host workspace, filesystem read/write, archive read/write, code execution och persistent state.\n"
            "- Välj exakt en explicit indata-ZIP. Blockera om rätt ZIP saknas eller flera kandidater är oklara.\n"
            "- project-manifest.json är auktoritativ state. Rekonstruera aldrig projektstate från chatt, EPUB eller PDF.\n"
            "- Kör project_integrity.py verify före filändring och efter återöppnad leverans-ZIP.\n"
            "- Varje commit ska använda explicit allow-list och öka revision exakt med 1.\n"
            "- Utan code execution får ingen filbaserad ändring beskrivas som integritetsverifierad.\n"
            "- Utan archive read/write får ingen revisionslåst ZIP-transaktion genomföras.\n"
            "- Planering, synopsis, karaktärsarbete och textutkast kan fortsätta med begränsad host, men får inte framställas som verifierad projektstate.\n"
            "- Ingen MCP-wrapper genereras.\n\n"
            "## Kanoniskt beteendekontrakt\n\n"
            + canonical
            + "\n\n## References\n\n"
            + "\n".join(f"- references/knowledge/{name}" for name in KNOWLEDGE_FILES)
            + "\n\n## Assets\n\n- assets/romanprojekt/\n"
            + "\n## Script resources\n\n"
            + "- scripts/project_integrity.py (required)\n"
            + "- scripts/publishing/fix-epub-after-pandoc.py (recommended)\n"
        )
        (skill / "SKILL.md").write_text(skill_text, encoding="utf-8")

        for name in KNOWLEDGE_FILES:
            copy_file(KNOWLEDGE_ROOT / name, refs / name)

        script_map = {
            "scripts/project_integrity.py": "project_integrity.py",
            "publishing/fix-epub-after-pandoc.py": "publishing/fix-epub-after-pandoc.py",
        }
        for path in sorted(p for p in TEMPLATE_ROOT.rglob("*") if p.is_file()):
            rel = path.relative_to(TEMPLATE_ROOT).as_posix()
            if rel in script_map:
                target = scripts_dir / script_map[rel]
            else:
                target = assets / rel
            copy_file(path, target)

        plugin_manifest = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "romanskaparen",
            "version": version,
            "description": "Stateful skrivassistent för revisionslåsta romanprojekt.",
        }
        (plugin / "plugin.json").write_text(json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        runtime_tools = {
            **json.loads((ROOT / "runtime-contracts" / "opencode.json").read_text(encoding="utf-8")).get("tools", {}),
        }
        if isinstance(runtime_tools.get("tools"), list):
            runtime_tools["tools"] = [t for t in runtime_tools["tools"] if t.get("id") == "project-integrity"]

        runtime_contract = {
            "schema_version": 1,
            "runtime_id": "openai_plugin",
            "version": version,
            "capabilities": {
                "workspace": "required_host_runtime",
                "filesystem_read": "required_host_runtime",
                "filesystem_write": "required_host_runtime",
                "archive_read": "required_host_runtime",
                "archive_write": "required_host_runtime",
                "code_execution": "required_host_runtime",
                "persistent_state": "required_host_runtime",
            },
            "workspace_state": {
                "authority": "project_manifest",
                "source_rule": "exactly_one_explicit_input_zip",
                "revision_increment": "exactly_one",
                "conversation_fallback": False,
                "reconstruct_from_chat": False,
                "reconstruct_from_export": False,
            },
            "tools": runtime_tools,
            "adapter": {
                "mode": "skills_first",
                "compatibility": "ready_runtime_dependent",
                "mcp_generated": False,
                "script_resources": [
                    {
                        "path": "skills/romanskaparen/scripts/project_integrity.py",
                        "requirement": "required",
                        "materialize_to": "scripts/project_integrity.py",
                    },
                    {
                        "path": "skills/romanskaparen/scripts/publishing/fix-epub-after-pandoc.py",
                        "requirement": "recommended",
                        "materialize_to": "publishing/fix-epub-after-pandoc.py",
                    },
                ],
                "fallback_policy": {
                    "without_workspace_or_archive": "block_file_based_project_transaction",
                    "without_code_execution": "do_not_claim_integrity_verified_change",
                    "without_persistent_state": "do_not_claim_stateful_project_management",
                },
            },
        }
        (plugin / "runtime-contract.json").write_text(json.dumps(runtime_contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (plugin / "README.md").write_text(
            "# Romanskaparen – OpenAI Plugin\n\n"
            "Skills-first peer-runtime enligt GPT Byggaren 1.5.1. Full filbaserad funktion kräver hoststöd för workspace, archive, filesystem, code execution och persistent state. Ingen MCP-wrapper ingår.\n",
            encoding="utf-8",
        )
        write_version(plugin / "VERSION", version)

        files = []
        for path in sorted(p for p in plugin.rglob("*") if p.is_file() and p.name != "MANIFEST.json"):
            files.append({
                "path": path.relative_to(plugin).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            })
        (plugin / "MANIFEST.json").write_text(
            json.dumps({
                "schema_version": 1,
                "runtime_id": "openai_plugin",
                "version": version,
                "entrypoint": "plugin.json",
                "files": files,
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        plugin_zip = output_dir / f"romanskaparen-openai-plugin-v{version}.zip"
        zip_dir(plugin, plugin_zip)

    for path in (custom_zip, portable_zip, plugin_zip):
        verify_zip(path)
    return [custom_zip, portable_zip, plugin_zip]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bygg Romanskaparens Custom GPT- och portabla chat-distributioner.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--version", help="Explicit SemVer-version utan inledande v. Överstyr VERSION, avsett för releasebyggen.")
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

    built = build(args.output_dir, args.version)
    for path in built:
        print(f"OK: {path} ({path.stat().st_size} bytes, sha256={sha256(path)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
