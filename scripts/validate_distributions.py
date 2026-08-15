#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

REQUIRED_KNOWLEDGE = {
    "01-arbetsflode-och-nyborjarstod.md",
    "02-berattelsehantverk.md",
    "03-karaktarer-varld-och-kontinuitet.md",
    "04-genreguider.md",
    "05-projektstruktur-och-synk.md",
}


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_portable(path: Path) -> None:
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
        manifest = json.loads(zf.read("MANIFEST.json").decode("utf-8"))
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
