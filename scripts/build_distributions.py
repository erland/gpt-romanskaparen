#!/usr/bin/env python3
"""Synchronize generated distribution files from Romanskaparen Core."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_KNOWLEDGE = ROOT / "core" / "knowledge"
CORE_STARTERS = ROOT / "core" / "prompts" / "default-starters.md"
DISTRIBUTIONS = ("gpt", "project")


def sync_file(source: Path, target: Path, check: bool, stale: list[Path]) -> None:
    expected = source.read_bytes()
    if check:
        if not target.exists() or target.read_bytes() != expected:
            stale.append(target)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(expected)
    print(f"Synced {target.relative_to(ROOT)}")


def sync_knowledge(check: bool, stale: list[Path]) -> None:
    expected_names = {path.name for path in CORE_KNOWLEDGE.glob("*.md")}
    for distribution in DISTRIBUTIONS:
        target_dir = ROOT / "distributions" / distribution / "knowledge"
        if not check:
            target_dir.mkdir(parents=True, exist_ok=True)
        actual_names = {path.name for path in target_dir.glob("*.md")} if target_dir.exists() else set()
        for extra in sorted(actual_names - expected_names):
            target = target_dir / extra
            if check:
                stale.append(target)
            else:
                target.unlink()
                print(f"Removed {target.relative_to(ROOT)}")
        for source in sorted(CORE_KNOWLEDGE.glob("*.md")):
            sync_file(source, target_dir / source.name, check, stale)


def update_manifest(path: Path, check: bool, stale: list[Path]) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["generated"] = True
    manifest["generation_note"] = "Generated from canonical files under core/ by scripts/build_distributions.py."
    expected = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if check:
        if path.read_text(encoding="utf-8") != expected:
            stale.append(path)
    else:
        path.write_text(expected, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    stale: list[Path] = []
    sync_knowledge(args.check, stale)
    sync_file(
        CORE_STARTERS,
        ROOT / "distributions" / "gpt" / "conversation-starters.md",
        args.check,
        stale,
    )

    for distribution in DISTRIBUTIONS:
        update_manifest(ROOT / "distributions" / distribution / "distribution-manifest.json", args.check, stale)

    command = [sys.executable, str(ROOT / "scripts" / "build_project_template_bundle.py")]
    if args.check:
        command.append("--check")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        return result.returncode

    if stale:
        for path in sorted(set(stale)):
            print(f"STALE: {path.relative_to(ROOT)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
