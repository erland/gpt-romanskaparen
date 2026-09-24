#!/usr/bin/env python3
from pathlib import Path
import json, sys, yaml

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def check(cond,msg):
    if not cond: errors.append(msg)

cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
check(cfg.get("schema_version")==1,"schema_version must be 1")
check(cfg.get("project",{}).get("id")=="romanskaparen","wrong project id")

rob=cfg.get("model_robustness",{})
check(rob.get("level")=="stateful","model robustness must be stateful")
for key in ["operational_core","explicit_workflow","deterministic_gates","authoritative_structured_state","resume_recovery","instruction_adherence_evals"]:
    check(rob.get(key) is True,f"stateful robustness flag must be true: {key}")

expected={"chatgpt_chat","chatgpt_custom","claude_project","opencode","openai_plugin"}
candidates={x.get("runtime_id"):x for x in cfg.get("analysis",{}).get("runtime",{}).get("candidates",[]) if isinstance(x,dict)}
check(set(candidates)==expected,"all five peer runtimes must be assessed")
check(candidates.get("chatgpt_chat",{}).get("suitability")=="ready","Chat must be ready")
check(candidates.get("chatgpt_custom",{}).get("suitability")=="ready","Custom GPT must be ready")
check(candidates.get("opencode",{}).get("suitability")=="ready","OpenCode must be ready")
check(candidates.get("claude_project",{}).get("suitability")=="reduced","Claude must currently be reduced")
check(candidates.get("openai_plugin",{}).get("suitability")=="reduced","OpenAI Plugin must be reduced")

ws=cfg.get("workspace_state",{})
check(ws.get("state",{}).get("authority")=="project_manifest","project manifest must be authoritative state")
check(ws.get("state",{}).get("model")=="templates/romanprojekt/project-manifest.json","manifest model path drift")
check(ws.get("state",{}).get("integrity_tool")=="templates/romanprojekt/scripts/project_integrity.py","integrity tool path drift")
check(ws.get("workspace",{}).get("source_rule")=="exactly_one_explicit_input_zip","source ZIP rule drift")
tx=ws.get("transaction",{})
check(tx.get("precondition")=="verify_selected_input","transaction precondition must verify selected input")
check(tx.get("mutation",{}).get("explicit_allow_list_required") is True,"explicit allow list must be required")
check(tx.get("mutation",{}).get("revision_increment")=="exactly_one","revision increment must be exactly one")
check(tx.get("postcondition",{}).get("reopen_delivery_zip") is True,"delivery ZIP must be reopened")
check(tx.get("postcondition",{}).get("verify_delivery") is True,"delivery must be verified")
check(tx.get("postcondition",{}).get("unchanged_chapters_must_preserve_hash") is True,"unchanged chapters must preserve hashes")
check(ws.get("resume",{}).get("reconstruct_from_chat") is False,"project may not be reconstructed from chat")
check(ws.get("resume",{}).get("reconstruct_from_export") is False,"project may not be reconstructed from export")

manifest=json.loads((ROOT/"templates/romanprojekt/project-manifest.json").read_text(encoding="utf-8"))
for key in ["schema_version","project_id","project_slug","revision","parent_revision","canonical_zip_name","tracked_files","chapters","last_operation"]:
    check(key in manifest,f"project manifest missing state field: {key}")

canonical=(ROOT/"gpt-instructions.md").read_text(encoding="utf-8")
for marker in ["Absolut källregel","exakt **en** indata-zip","project-manifest.json","revision-log.md","--allow","återskapa aldrig","verifierad projekt-zip"]:
    check(marker.lower() in canonical.lower(),f"canonical instruction missing marker: {marker}")

for rel in [
  "schemas/capability-contract.schema.json","schemas/artifact-contract.schema.json",
  "schemas/workspace-state-contract.schema.json","schemas/tool-contract.schema.json",
  "docs/gpt-builder-1.5-migration-plan.md","PROJECT.md","STATUS.md","project-status.yaml"
]:
    check((ROOT/rel).exists(),f"missing GPT Builder file: {rel}")

if errors:
    print("GPT BUILDER PROJECT LINT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print("GPT BUILDER PROJECT LINT: PASS")
print("robustness=stateful authority=project_manifest source=explicit_zip revision=+1")
