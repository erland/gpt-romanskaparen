#!/usr/bin/env python3
"""Assert lossless canonical modular assembly against the preserved legacy instruction."""
import hashlib
import json
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.canonical_skill_sources import projected_instruction

def main():
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert config["instructions"]["mode"] == "modular_skills"
    definitions = config["skills"]["definitions"]
    assert len(definitions) == 4
    assembly = json.loads((ROOT / config["instructions"]["assembly"]).read_text(encoding="utf-8"))
    owners = {"core"} | {item["id"] for item in definitions}
    assert set(assembly["sources"]) == owners
    assert {row["owner"] for row in assembly["sections"]} == owners
    original = (ROOT / "gpt-instructions.md").read_text(encoding="utf-8")
    assembled = projected_instruction(ROOT, config, definitions)
    assert assembled == original, "Canonical instructions drifted: byte-exact parity lost"
    print("MODULAR PARITY PASS", len(assembly["sections"]), "sections", hashlib.sha256(assembled.encode()).hexdigest())

if __name__ == "__main__":
    main()
