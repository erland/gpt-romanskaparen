#!/usr/bin/env python3
"""Require complete canonical romanprojekt assets in portable skill runtimes."""
from pathlib import Path
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONF = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
SOURCE = ROOT / "templates" / "romanprojekt"
FILES = {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_file()}
assert FILES and {"project-manifest.json", "scripts/project_integrity.py", "revision-log.md"} <= FILES

targets = {
    "plugin": ["skills/romanplanering/assets/romanprojekt/", "skills/revisionssakerhet/assets/romanprojekt/"],
    "claude-skills": ["skills/romanplanering/assets/romanprojekt/", "skills/revisionssakerhet/assets/romanprojekt/"],
    "opencode": [".opencode/skills/romanplanering/assets/romanprojekt/", ".opencode/skills/revisionssakerhet/assets/romanprojekt/"],
}
for name, prefixes in targets.items():
    candidates = sorted((ROOT / "dist").glob("romanskaparen-" + name + "-*.zip"))
    assert candidates, f"Missing {name} distribution"
    archive = candidates[-1]
    with zipfile.ZipFile(archive) as z:
        names = set(z.namelist())
        for prefix in prefixes:
            missing = {prefix + rel for rel in FILES} - names
            assert not missing, f"{name}: missing {len(missing)} assets under {prefix}: {sorted(missing)[:5]}"
            for rel in FILES:
                assert z.read(prefix + rel) == (SOURCE / rel).read_bytes(), f"{name}: changed template {rel}"
    print(f"{name}: {len(FILES)} templates verified")
print("PORTABLE ROMANPROJEKT ASSETS: PASS")
