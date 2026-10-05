#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")

REQUIRED_KNOWLEDGE = {
    "01-arbetsflode-och-nyborjarstod.md",
    "02-berattelsehantverk.md",
    "03-karaktarer-varld-och-kontinuitet.md",
    "04-genreguider.md",
    "05-projektstruktur-och-synk.md",
}


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()



def filename_version(path: Path, prefix: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}-v(.+)\.zip$")
    match = pattern.match(path.name)
    if not match:
        raise RuntimeError(f"Felaktigt distributionsfilnamn: {path.name}")
    version = match.group(1)
    if not SEMVER_RE.fullmatch(version):
        raise RuntimeError(f"Ogiltig SemVer i filnamnet: {version}")
    return version


def zip_version(zf: zipfile.ZipFile) -> str:
    version = zf.read("VERSION").decode("utf-8").strip()
    if not SEMVER_RE.fullmatch(version):
        raise RuntimeError(f"Ogiltig VERSION i ZIP: {version}")
    return version

def validate_portable(path: Path) -> None:
    expected_version = filename_version(path, "romanskaparen-chat")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Skadad ZIP-post: {bad}")
        names = set(zf.namelist())
        required = {"START-HERE.md", "VERSION", "MANIFEST.json", "assistant/instructions.md", "assistant/runtime-contract.json", "knowledge/project-template-bundle.md"}
        required |= {f"knowledge/{name}" for name in REQUIRED_KNOWLEDGE}
        missing = sorted(required - names)
        if missing:
            raise RuntimeError(f"Saknade filer i portable package: {missing}")
        internal_version = zip_version(zf)
        if internal_version != expected_version:
            raise RuntimeError(f"VERSION {internal_version} matchar inte filnamnets version {expected_version}")
        manifest = json.loads(zf.read("MANIFEST.json").decode("utf-8"))
        if manifest.get("version") != expected_version:
            raise RuntimeError(f"Manifestversion {manifest.get('version')} matchar inte {expected_version}")
        if manifest.get("format") != "portable-chat-assistant":
            raise RuntimeError("Fel format i MANIFEST.json")
        if manifest.get("entrypoint") != "START-HERE.md":
            raise RuntimeError("Fel entrypoint i MANIFEST.json")
        for item in manifest.get("files", []):
            name = item["path"]
            if name not in names:
                raise RuntimeError(f"Manifestfil saknas i ZIP: {name}")
            actual = hash_bytes(zf.read(name))
            if actual != item["sha256"]:
                raise RuntimeError(f"SHA-256 stämmer inte för {name}")
        template_names = [n for n in names if n.startswith("templates/romanprojekt/") and not n.endswith("/")]
        if not template_names:
            raise RuntimeError("Portable package saknar romanprojektmallen")
        contract = json.loads(zf.read("assistant/runtime-contract.json").decode("utf-8"))
        if contract.get("runtime_id") != "chatgpt_chat":
            raise RuntimeError("Fel runtime_id i Chat runtime contract")
        if contract.get("workspace_state", {}).get("authority") != "project_manifest":
            raise RuntimeError("Chat runtime contract saknar project_manifest authority")


def validate_custom(path: Path) -> None:
    expected_version = filename_version(path, "romanskaparen-custom-gpt")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Skadad ZIP-post: {bad}")
        names = set(zf.namelist())
        required = {"gpt-instructions.md", "conversation-starters.md", "project-template-bundle.md", "runtime-contract.json", "SETUP.md", "README.md", "VERSION"}
        required |= {f"knowledge-upload/{name}" for name in REQUIRED_KNOWLEDGE}
        missing = sorted(required - names)
        if missing:
            raise RuntimeError(f"Saknade filer i Custom GPT package: {missing}")
        internal_version = zip_version(zf)
        if internal_version != expected_version:
            raise RuntimeError(f"VERSION {internal_version} matchar inte filnamnets version {expected_version}")
        contract = json.loads(zf.read("runtime-contract.json").decode("utf-8"))
        if contract.get("runtime_id") != "chatgpt_custom":
            raise RuntimeError("Fel runtime_id i Custom GPT runtime contract")
        if contract.get("workspace_state", {}).get("authority") != "project_manifest":
            raise RuntimeError("Custom GPT runtime contract saknar project_manifest authority")



def validate_plugin(path: Path) -> None:
    expected_version = filename_version(path, "romanskaparen-openai-plugin")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Skadad ZIP-post: {bad}")
        names = set(zf.namelist())
        required = {
            "plugin.json", "README.md", "VERSION", "MANIFEST.json", "runtime-contract.json",
            "skills/romanskaparen/SKILL.md",
            "skills/romanskaparen/scripts/project_integrity.py",
            "skills/romanskaparen/scripts/publishing/fix-epub-after-pandoc.py",
        }
        required |= {f"skills/romanskaparen/references/knowledge/{name}" for name in REQUIRED_KNOWLEDGE}
        missing = sorted(required - names)
        if missing:
            raise RuntimeError(f"Saknade filer i OpenAI Plugin package: {missing}")
        if any(name.startswith("romanskaparen/") for name in names):
            raise RuntimeError("Plugin ZIP får inte ha wrapper-/toppkatalog")
        internal_version = zip_version(zf)
        if internal_version != expected_version:
            raise RuntimeError(f"VERSION {internal_version} matchar inte filnamnets version {expected_version}")
        plugin = json.loads(zf.read("plugin.json").decode("utf-8"))
        if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            raise RuntimeError("Plugin schema mismatch")
        if plugin.get("name") != "romanskaparen" or plugin.get("version") != expected_version:
            raise RuntimeError("Plugin metadata mismatch")
        skill = zf.read("skills/romanskaparen/SKILL.md").decode("utf-8")
        canonical = (Path(__file__).resolve().parents[1] / "gpt-instructions.md").read_text(encoding="utf-8").strip()
        if canonical not in skill:
            raise RuntimeError("Plugin skill saknar canonical instruktion")
        for marker in (
            "exakt en explicit indata-ZIP",
            "project-manifest.json är auktoritativ state",
            "Utan code execution får ingen filbaserad ändring",
            "Ingen MCP-wrapper genereras",
        ):
            if marker not in skill:
                raise RuntimeError(f"Plugin skill saknar runtime marker: {marker}")
        contract = json.loads(zf.read("runtime-contract.json").decode("utf-8"))
        if contract.get("runtime_id") != "openai_plugin":
            raise RuntimeError("Plugin runtime_id mismatch")
        caps = contract.get("capabilities", {})
        for key in ("workspace","filesystem_read","filesystem_write","archive_read","archive_write","code_execution","persistent_state"):
            if caps.get(key) != "required_host_runtime":
                raise RuntimeError(f"Plugin capability mismatch: {key}")
        state = contract.get("workspace_state", {})
        if state.get("authority") != "project_manifest":
            raise RuntimeError("Plugin state authority mismatch")
        if state.get("source_rule") != "exactly_one_explicit_input_zip":
            raise RuntimeError("Plugin source ZIP rule mismatch")
        if state.get("revision_increment") != "exactly_one":
            raise RuntimeError("Plugin revision rule mismatch")
        if state.get("conversation_fallback") is not False or state.get("reconstruct_from_chat") is not False or state.get("reconstruct_from_export") is not False:
            raise RuntimeError("Plugin state fallback mismatch")
        if contract.get("tools") != {"project_integrity":"required"}:
            raise RuntimeError("Plugin runtime tools mismatch")
        adapter = contract.get("adapter", {})
        if adapter.get("mode") != "skills_first" or adapter.get("compatibility") != "ready_runtime_dependent":
            raise RuntimeError("Plugin adapter mismatch")
        if adapter.get("mcp_generated") is not False:
            raise RuntimeError("Plugin får inte generera MCP-wrapper")
        declared = {x.get("path") for x in adapter.get("script_resources", [])}
        if declared != {
            "skills/romanskaparen/scripts/project_integrity.py",
            "skills/romanskaparen/scripts/publishing/fix-epub-after-pandoc.py",
        }:
            raise RuntimeError("Plugin script_resources mismatch")
        unexpected_python = [n for n in names if n.endswith(".py") and n not in declared]
        if unexpected_python:
            raise RuntimeError("Plugin innehåller odeklarerad Python: " + ", ".join(sorted(unexpected_python)))
        manifest = json.loads(zf.read("MANIFEST.json").decode("utf-8"))
        if manifest.get("runtime_id") != "openai_plugin" or manifest.get("version") != expected_version:
            raise RuntimeError("Plugin MANIFEST metadata mismatch")
        for item in manifest.get("files", []):
            name = item["path"]
            if name not in names or hash_bytes(zf.read(name)) != item["sha256"]:
                raise RuntimeError(f"Plugin MANIFEST SHA mismatch: {name}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.paths:
        if "romanskaparen-chat-" in path.name:
            validate_portable(path)
        elif "romanskaparen-custom-gpt-" in path.name:
            validate_custom(path)
        elif "romanskaparen-openai-plugin-" in path.name:
            validate_plugin(path)
        else:
            raise RuntimeError(f"Okänd distributionstyp: {path.name}")
        print(f"OK: verifierad {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
