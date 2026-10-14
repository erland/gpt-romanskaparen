#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KNOWLEDGE=sorted((ROOT/"knowledge-upload").glob("*.md"))
TEMPLATE_FILES=sorted(p.relative_to(ROOT/"templates/romanprojekt").as_posix() for p in (ROOT/"templates/romanprojekt").rglob("*") if p.is_file())

def sha(b:bytes): return hashlib.sha256(b).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--version"); ap.add_argument("--dist",default=str(ROOT/"dist"))
    a=ap.parse_args(); version=(a.version or (ROOT/"VERSION").read_text(encoding="utf-8")).strip()
    path=Path(a.dist)/f"romanskaparen-opencode-v{version}.zip"
    if not path.is_file(): raise SystemExit("Missing OpenCode distribution: "+str(path))
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad: raise SystemExit("Corrupt OpenCode ZIP: "+bad)
        names=set(z.namelist())
        req={"AGENTS.md","opencode.json","README.md","VERSION","MANIFEST.json",".opencode/romanskaparen/instructions.md",".opencode/romanskaparen/project-template-bundle.md",".opencode/romanskaparen/runtime-contract.json",".opencode/romanskaparen/platform-contract.json"}
        req|={f".opencode/romanskaparen/knowledge/{p.name}" for p in KNOWLEDGE}
        req|={f".opencode/romanskaparen/templates/romanprojekt/{p}" for p in TEMPLATE_FILES}
        missing=sorted(req-names)
        if missing: raise SystemExit("OpenCode package missing: "+", ".join(missing))
        if z.read(".opencode/romanskaparen/instructions.md")!=(ROOT/"gpt-instructions.md").read_bytes(): raise SystemExit("OpenCode canonical instruction drift")
        tool=".opencode/romanskaparen/templates/romanprojekt/scripts/project_integrity.py"
        if z.read(tool)!=(ROOT/"templates/romanprojekt/scripts/project_integrity.py").read_bytes(): raise SystemExit("OpenCode integrity tool drift")
        agents=z.read("AGENTS.md").decode("utf-8")
        for marker in ["exactly one explicit input ZIP","project-manifest.json","--expected-revision","--allow","preserve SHA-256","do not deliver the ZIP"]:
            if marker not in agents: raise SystemExit("AGENTS missing marker: "+marker)
        platform=json.loads(z.read(".opencode/romanskaparen/platform-contract.json"))
        if platform.get("runtime_id")!="opencode": raise SystemExit("OpenCode platform contract runtime_id drift")
        if platform.get("workspace_state",{}).get("authority")!="project_manifest": raise SystemExit("OpenCode platform contract state authority drift")
        contract=json.loads(z.read(".opencode/romanskaparen/runtime-contract.json"))
        for key,val in {"runtime_id":"opencode","state_authority":"project-manifest.json","source_rule":"exactly_one_explicit_input_zip","revision_increment":"exactly_one"}.items():
            if contract.get(key)!=val: raise SystemExit("Runtime contract drift: "+key)
        for key in ["native_filesystem","native_shell","native_archive","explicit_allow_list_required"]:
            if contract.get(key) is not True: raise SystemExit("Runtime capability missing: "+key)
        manifest=json.loads(z.read("MANIFEST.json"))
        if manifest.get("runtime_id")!="opencode" or manifest.get("version")!=version: raise SystemExit("OpenCode manifest metadata drift")
        for rel,meta in manifest.get("files",{}).items():
            if sha(z.read(rel))!=meta.get("sha256"): raise SystemExit("Manifest hash mismatch: "+rel)
    print(f"OpenCode runtime validation OK for Romanskaparen v{version}")

if __name__=="__main__": main()
