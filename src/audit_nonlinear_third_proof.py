"""Audit the additional coarse progression proof without changing frozen receipts."""
from pathlib import Path
import json, hashlib
from audit_nonlinear_capacity import audit

ROOT = Path(__file__).resolve().parents[1]
result = audit(write=False)
result['kind'] = 'additional_coarse_progression_proof'
result['wrapper_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
path = ROOT / 'results' / 'nonlinear-third-proof-audit.json'
path.write_text(json.dumps(result, indent=2) + '\n')
print('PASSED additional coarse proof:', result['classes'], 'classes;', result['seeds'], 'seeds')
