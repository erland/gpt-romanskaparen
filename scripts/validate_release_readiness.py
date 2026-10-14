#!/usr/bin/env python3
"""Six-artifact release gate with checksum and CRC validation."""
from pathlib import Path
import argparse,hashlib,json,zipfile,sys
r=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--version');a.add_argument('--dist');ns=a.parse_args()
v=ns.version or (r/'VERSION').read_text().strip();dist=Path(ns.dist) if ns.dist else r/'dist'
expected={f'romanskaparen-{name}-{v}.zip' for name in ['project','chat','plugin','claude-project','claude-skills','opencode']}
errors=[]
manifest=dist/'DELIVERY-MANIFEST.json';checksums=dist/'SHA256SUMS.txt'
if not manifest.exists():errors.append('missing manifest')
else:
 data=json.loads(manifest.read_text());actual={x['file'] for x in data.get('artifacts',[]) if x.get('type','').endswith('_zip')};errors.extend('not in manifest: '+n for n in sorted(expected-actual))
if not checksums.exists():errors.append('missing checksums')
else:
 sums={l.split(None,1)[1].strip():l.split(None,1)[0] for l in checksums.read_text().splitlines() if l.strip()}
 for n in sorted(expected):
  p=dist/n
  if not p.exists():errors.append('missing '+n);continue
  if hashlib.sha256(p.read_bytes()).hexdigest()!=sums.get(n):errors.append('SHA256 mismatch '+n)
  try:
   with zipfile.ZipFile(p) as z:
    if z.testzip():errors.append('CRC mismatch '+n)
  except zipfile.BadZipFile:errors.append('invalid archive '+n)
print('RELEASE READINESS:', 'FAIL' if errors else 'PASS')
for e in errors:print('-',e)
sys.exit(bool(errors))
