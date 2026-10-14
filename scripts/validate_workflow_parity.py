#!/usr/bin/env python3
"""Verify the 1.6.25 canonical six-target CI/release workflow."""
from pathlib import Path
import sys
r=Path(__file__).resolve().parents[1]
ci=(r/'.github/workflows/ci.yml').read_text()
rel=(r/'.github/workflows/build-distributions.yml').read_text()
checks={'ci lint':'scripts/lint_gpt_project.py' in ci,'ci deterministic integrity':'scripts/test_project_integrity_contract.py' in ci,'ci state regression':'scripts/validate_stateful_behavior_contract.py' in ci,'ci build':'scripts/build_distributions.py' in ci,'ci validation':'scripts/validate_distributions.py' in ci,'release trigger':'types: [published]' in rel,'release tag-derived version':'${TAG#v}' in rel,'release tag check':'Unsupported release tag' in rel or '[[ "$TAG" =~' in rel,'release integrity':'scripts/test_project_integrity_contract.py' in rel,'release state':'scripts/validate_stateful_behavior_contract.py' in rel,'release validation':'scripts/validate_distributions.py' in rel,'release upload after validation':rel.index('scripts/validate_distributions.py') < rel.index('gh release upload')}
for t in ('project','chat','plugin','claude_project','claude_skills','opencode'):
 checks['ci target '+t]=t in ci.split('--targets ')[-1]
 checks['release target '+t]=t in rel.split('--targets ')[-1]
failed=[k for k,v in checks.items() if not v]
print('WORKFLOW PARITY:', 'FAIL' if failed else 'PASS',f'({sum(checks.values())}/{len(checks)})')
for f in failed:print('-',f)
sys.exit(bool(failed))
