#!/usr/bin/env python3
"""Check Chat ZIP keeps canonical project templates without duplicate Skill assets."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "templates" / "romanprojekt"
files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
assert files, "Roman project template is empty"
archives = sorted((ROOT / "dist").glob("romanskaparen-chat-*.zip"))
assert len(archives) == 1, f"Expected one Chat ZIP, got {len(archives)}"
with zipfile.ZipFile(archives[0]) as archive:
    names = set(archive.namelist())
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        assert relative in names, f"Missing canonical template {relative}"
        assert archive.read(relative) == path.read_bytes(), f"Template changed: {relative}"
        for skill in ("romanplanering", "revisionssakerhet"):
            duplicated = f"assistant/skills/{skill}/assets/romanprojekt/{path.relative_to(SOURCE).as_posix()}"
            assert duplicated not in names, f"Duplicate Chat ZIP asset {duplicated}"
    for skill in ("romanplanering", "revisionssakerhet"):
        assert f"assistant/skills/{skill}/SKILL.md" in names
print(f"CHAT TEMPLATE DEDUPLICATION: PASS ({len(files)} canonical files, no duplicated Skill assets)")
