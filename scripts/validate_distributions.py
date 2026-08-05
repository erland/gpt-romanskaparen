#!/usr/bin/env python3
"""Validate Romanskaparen distributions and their canonical-source alignment."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_KNOWLEDGE = ROOT / "core" / "knowledge"
EXPECTED_KNOWLEDGE = sorted(path.name for path in CORE_KNOWLEDGE.glob("*.md"))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_distribution(name: str, instruction_name: str, errors: list[str]) -> None:
    root = ROOT / "distributions" / name
    manifest_path = root / "distribution-manifest.json"
    if not manifest_path.exists():
        fail(f"{name}: missing distribution-manifest.json", errors)
        return

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{name}: invalid manifest JSON: {exc}", errors)
        return

    knowledge_dir = root / "knowledge"
    actual_knowledge = sorted(path.name for path in knowledge_dir.glob("*.md"))
    if actual_knowledge != EXPECTED_KNOWLEDGE:
        fail(f"{name}: knowledge file set differs from core", errors)

    for filename in EXPECTED_KNOWLEDGE:
        source = CORE_KNOWLEDGE / filename
        target = knowledge_dir / filename
        if not target.exists() or source.read_bytes() != target.read_bytes():
            fail(f"{name}: stale knowledge/{filename}", errors)

    bundle = root / "project-template-bundle.md"
    if not bundle.exists() or bundle.stat().st_size == 0:
        fail(f"{name}: missing or empty project-template-bundle.md", errors)

    instruction = root / instruction_name
    if not instruction.exists():
        fail(f"{name}: missing {instruction_name}", errors)
    elif name == "gpt":
        characters = len(instruction.read_text(encoding="utf-8"))
        maximum = int(manifest.get("limits", {}).get("instructions_max_characters", 8000))
        if characters > maximum:
            fail(f"gpt: instructions are {characters} characters, limit is {maximum}", errors)

    knowledge_count = len(actual_knowledge) + (1 if bundle.exists() else 0)
    maximum_files = int(manifest.get("limits", {}).get("knowledge_max_files", 20))
    declared = int(manifest.get("limits", {}).get("knowledge_files_used", knowledge_count))
    if knowledge_count != declared:
        fail(f"{name}: manifest declares {declared} knowledge files, found {knowledge_count}", errors)
    if knowledge_count > maximum_files:
        fail(f"{name}: {knowledge_count} knowledge files exceed limit {maximum_files}", errors)

    if manifest.get("generated") is not True:
        fail(f"{name}: manifest is not marked generated", errors)


def main() -> int:
    errors: list[str] = []

    build_check = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_distributions.py"), "--check"],
        check=False,
    )
    if build_check.returncode != 0:
        fail("Generated distribution files are stale", errors)

    validate_distribution("gpt", "instructions.md", errors)
    validate_distribution("project", "PROJECT-INSTRUCTIONS.md", errors)

    gpt_bundle = ROOT / "distributions" / "gpt" / "project-template-bundle.md"
    project_bundle = ROOT / "distributions" / "project" / "project-template-bundle.md"
    if gpt_bundle.exists() and project_bundle.exists() and gpt_bundle.read_bytes() != project_bundle.read_bytes():
        fail("GPT and Project bundles differ", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("OK: Romanskaparen distributions are synchronized and valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
