#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXED=(1980,1,1,0,0,0)
KNOWLEDGE=sorted((ROOT/"knowledge-upload").glob("*.md"))
TEMPLATE=ROOT/"templates/romanprojekt"

def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(src:Path,dst:Path): dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
def zipdir(src:Path,out:Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob("*") if x.is_file()):
            info=zipfile.ZipInfo(p.relative_to(src).as_posix(),FIXED)
            info.compress_type=zipfile.ZIP_DEFLATED; info.create_system=3; info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--version"); ap.add_argument("--output-dir",default=str(ROOT/"dist"))
    a=ap.parse_args(); version=(a.version or (ROOT/"VERSION").read_text(encoding="utf-8")).strip()
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        base=Path(td)/"opencode"; base.mkdir()
        runtime=base/".opencode"/"romanskaparen"; runtime.mkdir(parents=True)
        copy(ROOT/"gpt-instructions.md",runtime/"instructions.md")
        copy(ROOT/"project-template-bundle.md",runtime/"project-template-bundle.md")
        copy(ROOT/"runtime-contracts/opencode.json",runtime/"platform-contract.json")
        for src in KNOWLEDGE: copy(src,runtime/"knowledge"/src.name)
        shutil.copytree(TEMPLATE,runtime/"templates"/"romanprojekt")
        contract={
          "schema_version":1,"runtime_id":"opencode","version":version,
          "mode":"opencode_workspace","state_authority":"project-manifest.json",
          "integrity_tool":".opencode/romanskaparen/templates/romanprojekt/scripts/project_integrity.py",
          "native_filesystem":True,"native_shell":True,"native_archive":True,
          "source_rule":"exactly_one_explicit_input_zip","revision_increment":"exactly_one",
          "explicit_allow_list_required":True,"reconstruct_from_chat":False,"reconstruct_from_export":False
        }
        (runtime/"runtime-contract.json").write_text(json.dumps(contract,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        agents="# Romanskaparen – OpenCode\n\nUse .opencode/romanskaparen/instructions.md as the canonical assistant instructions.\n\nFor file-based novel work:\n- Select exactly one explicit input ZIP. Never merge project state from multiple ZIPs, chat history, EPUB or PDF.\n- Unpack only that ZIP into a new empty transaction directory.\n- Run the bundled project_integrity.py verify command before mutation.\n- Treat project-manifest.json as authoritative persistent state.\n- Use commit with --expected-revision and an explicit --allow list.\n- Revision must advance by exactly one.\n- Existing chapters outside the requested target must preserve SHA-256.\n- Package the complete project, reopen the delivery ZIP in a fresh directory and run verify again before delivery.\n- If verification fails, do not deliver the ZIP.\n- Workspace files outside the selected project transaction are context, never an alternate state source.\n"
        (base/"AGENTS.md").write_text(agents,encoding="utf-8")
        (base/"opencode.json").write_text(json.dumps({"$schema":"https://opencode.ai/config.json","instructions":["AGENTS.md"],"permission":{"edit":"ask","bash":"ask"}},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (base/"README.md").write_text("# Romanskaparen – OpenCode\n\nExtract at workspace root. The assistant runtime lives under .opencode/romanskaparen. Novel project ZIPs remain external user state and are never reconstructed from assistant memory.\n",encoding="utf-8")
        (base/"VERSION").write_text(version+"\n",encoding="utf-8")
        files={}
        for p in sorted(x for x in base.rglob("*") if x.is_file() and x.name!="MANIFEST.json"):
            files[p.relative_to(base).as_posix()]={"sha256":sha(p),"bytes":p.stat().st_size}
        (base/"MANIFEST.json").write_text(json.dumps({"schema_version":1,"runtime_id":"opencode","version":version,"entrypoint":"AGENTS.md","files":files},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        target=out/f"romanskaparen-opencode-v{version}.zip"; zipdir(base,target); print(target)

if __name__=="__main__": main()
