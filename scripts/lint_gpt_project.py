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
manual=(ROOT/"knowledge-upload/05-projektstruktur-och-synk.md").read_text(encoding="utf-8")
for marker in ["Absolut källregel","exakt **en** indata-zip","återskapa aldrig","verifierad projekt-zip"]:
    check(marker.lower() in canonical.lower(),f"canonical instruction missing marker: {marker}")
for marker in ["project-manifest.json","revision-log.md","--allow","audit-legacy","verify","commit"]:
    check(marker.lower() in manual.lower(),f"file-work manual missing marker: {marker}")

runtime=cfg.get("runtime",{})
opencode=runtime.get("opencode",{})
claude=runtime.get("claude",{})
check(opencode.get("enabled") is True,"OpenCode peer runtime must be enabled")
check(opencode.get("mode")=="opencode_workspace","OpenCode runtime mode drift")
check(opencode.get("runtime_root")==".opencode/romanskaparen","OpenCode runtime root drift")
check(opencode.get("state_authority")=="project-manifest.json","OpenCode state authority drift")
check(opencode.get("integrity_tool")==".opencode/romanskaparen/templates/romanprojekt/scripts/project_integrity.py","OpenCode integrity tool drift")
check(claude.get("enabled") is False,"Claude must remain inactive")
check(claude.get("role")=="assessed_reduced","Claude assessment must remain reduced")
check(runtime.get("openai_plugin",{}).get("enabled") is False,"OpenAI Plugin must remain inactive")
check(runtime.get("openai_plugin",{}).get("role")=="assessed_reduced","OpenAI Plugin assessment must remain reduced")

parity=cfg.get("runtime_parity",{})
check(parity.get("model")=="runtime-parity.yaml","runtime parity model not registered")
check(set(parity.get("registered_runtimes",[]))==expected,"runtime parity must register all five runtimes")
check(set(parity.get("compared_categories",[]))=={"behavior","capability","artifact","workspace_state","tool"},"runtime parity categories differ")

testing=cfg.get("testing",{})
check(testing.get("manifest")=="tests/test-manifest.yaml","GPT Builder test manifest not registered")
check(testing.get("manifest_schema")=="schemas/test-manifest.schema.json","test manifest schema not registered")
check(testing.get("stateful_cases")=="tests/stateful-regression-cases.json","stateful regression catalog not registered")
check(testing.get("contract_validator")=="scripts/validate_gpt_builder_tests.py","test contract validator not registered")
check(testing.get("deterministic_state_tests")=="scripts/test_project_integrity_contract.py","state transition tests not registered")
check(testing.get("behavioral_contract_validator")=="scripts/validate_stateful_behavior_contract.py","behavioral state validator not registered")
check(testing.get("deterministic_suites_block_release") is True,"deterministic state suites must block release")
check(testing.get("live_runtime_evals_are_separate") is True,"live runtime evals must remain separate")

for rel in [
  "schemas/test-manifest.schema.json","tests/test-manifest.yaml","tests/stateful-regression-cases.json",
  "scripts/validate_gpt_builder_tests.py","scripts/test_project_integrity_contract.py","scripts/validate_stateful_behavior_contract.py",
  "scripts/build_opencode_runtime.py","scripts/validate_opencode_runtime.py",
  "runtime-parity.yaml","runtime-contracts/chatgpt-chat.json","runtime-contracts/chatgpt-custom.json","runtime-contracts/opencode.json",
  "scripts/build_project_package.py","scripts/build_delivery_metadata.py","scripts/validate_runtime_parity.py","scripts/validate_release_readiness.py",
  "scripts/final_project_hygiene.py","scripts/validate_workflow_parity.py","scripts/verify_reproducible_build.py",
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
