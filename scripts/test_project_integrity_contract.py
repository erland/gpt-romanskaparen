#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/"templates/romanprojekt/scripts/project_integrity.py"
TEMPLATE=ROOT/"templates/romanprojekt"

def run(*args,cwd=None):
    return subprocess.run([sys.executable,str(TOOL),*map(str,args)],cwd=cwd,text=True,capture_output=True)

def copy_template(dst:Path):
    shutil.copytree(TEMPLATE,dst)

def main():
    errors=[]
    with tempfile.TemporaryDirectory() as td:
        base=Path(td)

        # Happy path: init -> allowed change -> commit increments exactly one and records parent/source.
        p=base/"project"; copy_template(p)
        r=run("init",p,"--slug","testroman","--project-id","TEST-PROJECT","--revision","0","--zip-name","testroman-r0000.zip")
        if r.returncode!=0: errors.append("init failed: "+r.stderr)
        else:
            chapter=p/"kapitel"/"kapitel-01.md"
            chapter.write_text("# 1. Start\n\nText.\n",encoding="utf-8")
            r=run("commit",p,"--expected-revision","0","--operation","Skapade kapitel 1","--zip-name","testroman-r0001-kapitel-01.zip","--source-zip-name","testroman-r0000.zip","--allow","kapitel/kapitel-01.md")
            if r.returncode!=0: errors.append("allowed commit failed: "+r.stderr)
            else:
                m=json.loads((p/"project-manifest.json").read_text(encoding="utf-8"))
                if m.get("revision")!=1: errors.append("revision did not increment exactly one")
                if m.get("parent_revision")!=0: errors.append("parent_revision mismatch")
                if m.get("last_operation",{}).get("source_revision")!=0: errors.append("source_revision mismatch")
                vr=run("verify",p)
                if vr.returncode!=0: errors.append("post-commit verify failed: "+vr.stderr)

        # Disallowed change must block and leave revision unchanged.
        p2=base/"disallowed"; copy_template(p2)
        r=run("init",p2,"--slug","testroman2","--project-id","TEST-PROJECT-2","--revision","0","--zip-name","testroman2-r0000.zip")
        if r.returncode==0:
            (p2/"roman-bibel.md").write_text((p2/"roman-bibel.md").read_text(encoding="utf-8")+"\nÄndring\n",encoding="utf-8")
            r=run("commit",p2,"--expected-revision","0","--operation","Otillåtet test","--zip-name","testroman2-r0001.zip","--allow","projektstatus.md")
            if r.returncode==0: errors.append("disallowed change was accepted")
            m=json.loads((p2/"project-manifest.json").read_text(encoding="utf-8"))
            if m.get("revision")!=0: errors.append("blocked commit changed revision")

        # Wrong expected revision must block.
        p3=base/"wrongrev"; copy_template(p3)
        r=run("init",p3,"--slug","testroman3","--project-id","TEST-PROJECT-3","--revision","0","--zip-name","testroman3-r0000.zip")
        if r.returncode==0:
            (p3/"projektstatus.md").write_text((p3/"projektstatus.md").read_text(encoding="utf-8")+"\nÄndring\n",encoding="utf-8")
            r=run("commit",p3,"--expected-revision","9","--operation","Fel revision","--zip-name","testroman3-r0001.zip","--allow","projektstatus.md")
            if r.returncode==0: errors.append("wrong expected revision was accepted")

        # Existing modern manifest must make audit-legacy fail.
        legacy_zip=base/"modern.zip"
        with zipfile.ZipFile(legacy_zip,"w",zipfile.ZIP_DEFLATED) as z:
            z.writestr("project-manifest.json",'{"schema_version":1}')
            z.writestr("kapitel/kapitel-01.md","# 1. Start\n")
        r=run("audit-legacy",legacy_zip)
        if r.returncode==0: errors.append("audit-legacy accepted zip with manifest")

        # Broken modern manifest must not be overwritten by init.
        p4=base/"broken"; p4.mkdir()
        (p4/"project-manifest.json").write_text("{broken",encoding="utf-8")
        r=run("init",p4,"--slug","broken")
        if r.returncode==0: errors.append("init overwrote broken modern manifest")

    if errors:
        print("PROJECT INTEGRITY CONTRACT: FAIL")
        for e in errors: print("-",e)
        return 1
    print("PROJECT INTEGRITY CONTRACT: PASS")
    print("verified=revision+1,parent_revision,allow-list,expected-revision,legacy-gate,broken-manifest-gate")
    return 0

if __name__=="__main__": raise SystemExit(main())
