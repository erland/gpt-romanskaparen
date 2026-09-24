#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/"tests/stateful-regression-cases.json").read_text(encoding="utf-8"))["cases"]
canonical=(ROOT/"gpt-instructions.md").read_text(encoding="utf-8").lower()
manual=(ROOT/"knowledge-upload/05-projektstruktur-och-synk.md").read_text(encoding="utf-8").lower()
errors=[]
for case in cases:
    if case.get("kind")!="instruction_adherence": continue
    for marker in case.get("markers",[]):
        if marker.lower() not in canonical and marker.lower() not in manual:
            errors.append(f'{case["id"]}: missing marker {marker}')
if len(cases)!=12: errors.append(f"expected 12 cases, found {len(cases)}")
if errors:
    print("STATEFUL BEHAVIOR CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print("STATEFUL BEHAVIOR CONTRACT: PASS")
print("cases=12")
