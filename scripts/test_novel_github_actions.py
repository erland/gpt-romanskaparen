#!/usr/bin/env python3
"""Regression: each exported novel project includes self-contained optional Actions."""
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
import json

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/romanprojekt"
EXPECTED = [
    ".github/workflows/verify.yml",
    ".github/workflows/build-book.yml",
    "scripts/build_book.py",
    "scripts/validate_book.py",
]
for rel in EXPECTED:
    assert (TEMPLATE / rel).is_file(), f"Missing novel template asset: {rel}"
assert "project_integrity.py verify" in (TEMPLATE / EXPECTED[0]).read_text()
assert "project_integrity.py verify" in (TEMPLATE / EXPECTED[1]).read_text()
assert "upload-artifact" in (TEMPLATE / EXPECTED[1]).read_text()
with tempfile.TemporaryDirectory() as td:
    dst = Path(td) / "novel"
    shutil.copytree(TEMPLATE, dst)
    before = sorted((p.relative_to(dst), p.read_bytes()) for p in dst.rglob("*") if p.is_file())
    tool = dst / "scripts/project_integrity.py"
    p = subprocess.run([sys.executable, str(tool), "init", str(dst),
        "--slug", "actions-regression", "--project-id", "ACTIONS-TEST",
        "--revision", "0", "--zip-name", "actions-regression-r0000.zip"], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    p = subprocess.run([sys.executable, str(tool), "verify", str(dst)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    manifest = json.loads((dst / "project-manifest.json").read_text())
    for rel in EXPECTED:
        assert rel in manifest["tracked_files"], f"Untracked: {rel}"
        assert (dst / rel).read_bytes() == dict(before)[Path(rel)]
print("ROMAN GITHUB ACTIONS TEMPLATE: PASS")
