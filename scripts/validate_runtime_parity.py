#!/usr/bin/env python3
from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]
cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
parity=yaml.safe_load((ROOT/"runtime-parity.yaml").read_text(encoding="utf-8"))
expected={"chatgpt_chat","chatgpt_custom","claude_project","opencode","openai_plugin"}
if set(parity.get("registered_runtimes",[]))!=expected: errors.append("all five runtimes must be registered")
if set(parity.get("compared_categories",[]))!={"behavior","capability","artifact","workspace_state","tool"}: errors.append("parity categories differ")
candidates={x["runtime_id"]:x for x in cfg["analysis"]["runtime"]["candidates"]}
for rid in {"chatgpt_chat","chatgpt_custom","opencode"}:
    if candidates[rid].get("suitability")!="ready" or candidates[rid].get("activate_by_default") is not True: errors.append(rid+" not ready/active")
for rid in {"claude_project","openai_plugin"}:
    if candidates[rid].get("suitability")!="reduced" or candidates[rid].get("activate_by_default") is not False: errors.append(rid+" not reduced/inactive")
contracts={"chatgpt_chat":"runtime-contracts/chatgpt-chat.json","chatgpt_custom":"runtime-contracts/chatgpt-custom.json","opencode":"runtime-contracts/opencode.json"}
for rid,path in contracts.items():
    d=json.loads((ROOT/path).read_text(encoding="utf-8"))
    if d.get("runtime_id")!=rid: errors.append(rid+" runtime_id mismatch")
    if d.get("workspace_state",{}).get("authority")!="project_manifest": errors.append(rid+" state authority drift")
    if d.get("workspace_state",{}).get("source_rule")!="exactly_one_explicit_input_zip": errors.append(rid+" source rule drift")
    if d.get("workspace_state",{}).get("revision_increment")!="exactly_one": errors.append(rid+" revision rule drift")
if errors:
    print("RUNTIME PARITY: FAIL"); [print("-",e) for e in errors]; sys.exit(1)
print("RUNTIME PARITY: PASS")
