#!/usr/bin/env python3
from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]
m=yaml.safe_load((ROOT/"tests/test-manifest.yaml").read_text(encoding="utf-8"))
s=m.get("suites",{})
for sid in ["distribution_contract","state_transition_contract","behavioral_state_contract","live_runtime_eval"]:
    if sid not in s: errors.append("missing suite: "+sid)
for sid in ["distribution_contract","state_transition_contract","behavioral_state_contract"]:
    if s.get(sid,{}).get("blocking") is not True: errors.append(sid+" must block")
if s.get("live_runtime_eval",{}).get("blocking") is not False: errors.append("live runtime eval must be non-blocking")
cases=json.loads((ROOT/"tests/stateful-regression-cases.json").read_text(encoding="utf-8")).get("cases",[])
if len(cases)!=12: errors.append("expected 12 stateful regression cases")
ids=[x.get("id") for x in cases]
if len(ids)!=len(set(ids)): errors.append("duplicate case ids")
wf=(ROOT/".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
for script in ["validate_gpt_builder_tests.py","test_project_integrity_contract.py","validate_stateful_behavior_contract.py"]:
    if script not in wf: errors.append("workflow missing "+script)
if errors:
    print("GPT BUILDER TEST CONTRACT: FAIL"); [print("-",e) for e in errors]; sys.exit(1)
print("GPT BUILDER TEST CONTRACT: PASS")
print("suites=4 stateful_cases=12 blocking=3 manual_runtime=1")
