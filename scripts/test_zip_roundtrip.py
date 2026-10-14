#!/usr/bin/env python3
"""Verify real ZIP round-trip, revision persistence and tamper rejection."""
import json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "templates/romanprojekt/scripts/project_integrity.py"
TEMPLATE = ROOT / "templates/romanprojekt"

def run(*args, expect_ok=True):
    result = subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True)
    assert (result.returncode == 0) == expect_ok, f"{args}: {result.stdout} {result.stderr}"

def archive(source, target):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(source.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(source).as_posix())

def reopen(source, destination):
    with zipfile.ZipFile(source) as z:
        for name in z.namelist():
            p = Path(name)
            assert not p.is_absolute() and ".." not in p.parts
        z.extractall(destination)

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        a = root / "original"
        shutil.copytree(TEMPLATE, a)
        run("init", a, "--slug", "arkivroman", "--project-id", "ZIP-TEST", "--revision", "0", "--zip-name", "arkivroman-r0000.zip")
        run("verify", a)
        old_zip = root / "arkivroman-r0000.zip"
        archive(a, old_zip)
        b = root / "restored"
        reopen(old_zip, b)
        run("verify", b)
        (b / "kapitel/kapitel-01.md").write_text("# Kapitel 1\n\nEn berättelse.\n", encoding="utf-8")
        run("commit", b, "--expected-revision", "0", "--operation", "Kapitel 1", "--zip-name", "arkivroman-r0001.zip", "--source-zip-name", old_zip.name, "--allow", "kapitel/kapitel-01.md")
        run("verify", b)
        new_zip = root / "arkivroman-r0001.zip"
        archive(b, new_zip)
        c = root / "reopened"
        reopen(new_zip, c)
        run("verify", c)
        manifest = json.loads((c / "project-manifest.json").read_text(encoding="utf-8"))
        assert manifest["revision"] == 1 and manifest["parent_revision"] == 0
        assert "kapitel/kapitel-01.md" in manifest["tracked_files"]
        (c / "kapitel/kapitel-01.md").write_text("TAMPERED", encoding="utf-8")
        run("verify", c, expect_ok=False)
    print("ZIP ROUNDTRIP: PASS")

if __name__ == "__main__":
    main()
