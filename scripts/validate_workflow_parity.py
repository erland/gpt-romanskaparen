#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
wf=(ROOT/".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
errors=[]
required=["scripts/lint_gpt_project.py","scripts/build_distributions.py --check-bundle","scripts/validate_gpt_builder_tests.py","scripts/test_project_integrity_contract.py","scripts/validate_stateful_behavior_contract.py","scripts/build_distributions.py --output-dir dist","scripts/validate_distributions.py","scripts/build_opencode_runtime.py","scripts/validate_opencode_runtime.py","scripts/build_project_package.py","scripts/validate_runtime_parity.py","scripts/build_delivery_metadata.py","scripts/validate_release_readiness.py","scripts/final_project_hygiene.py","scripts/validate_workflow_parity.py","scripts/verify_reproducible_build.py"]
for token in required:
    if token not in wf: errors.append("workflow missing "+token)
upload=wf.find("gh release upload")
for token in ["scripts/validate_release_readiness.py","scripts/final_project_hygiene.py","scripts/validate_workflow_parity.py","scripts/verify_reproducible_build.py"]:
    pos=wf.find(token)
    if pos<0 or upload<0 or pos>upload: errors.append(token+" must run before release upload")
if "github.event_name == 'release'" not in wf: errors.append("release upload must remain release-event gated")
if "github.event.release.tag_name" not in wf or 'version="${RELEASE_TAG#v}"' not in wf: errors.append("release tag must remain authoritative version source")
if errors:
    print("WORKFLOW PARITY: FAIL"); [print("-",e) for e in errors]; sys.exit(1)
print("WORKFLOW PARITY: PASS")
