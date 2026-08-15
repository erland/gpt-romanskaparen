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
        required = {"START-HERE.md", "VERSION", "MANIFEST.json", "assistant/instructions.md", "knowledge/project-template-bundle.md"}
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


def validate_custom(path: Path) -> None:
    expected_version = filename_version(path, "romanskaparen-custom-gpt")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Skadad ZIP-post: {bad}")
        names = set(zf.namelist())
        required = {"gpt-instructions.md", "conversation-starters.md", "project-template-bundle.md", "SETUP.md", "README.md", "VERSION"}
        required |= {f"knowledge-upload/{name}" for name in REQUIRED_KNOWLEDGE}
        missing = sorted(required - names)
        if missing:
            raise RuntimeError(f"Saknade filer i Custom GPT package: {missing}")
        internal_version = zip_version(zf)
        if internal_version != expected_version:
            raise RuntimeError(f"VERSION {internal_version} matchar inte filnamnets version {expected_version}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.paths:
        if "romanskaparen-chat-" in path.name:
            validate_portable(path)
        elif "romanskaparen-custom-gpt-" in path.name:
            validate_custom(path)
        else:
            raise RuntimeError(f"Okänd distributionstyp: {path.name}")
        print(f"OK: verifierad {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
