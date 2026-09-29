"""Verify the frozen analytic graft without altering any receipt."""
from pathlib import Path
import json,hashlib
from audit_dual_tail_capacity import audit,MAP,PARAMS
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
NAME='dual-tail-capacity-certificate.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(name=NAME):
    cert=json.loads((R/name).read_text())
    assert cert['kind']=='dual_analytic_tail_graft' and cert['capacity_certified']
    assert cert['map_id']==MAP and not cert['conditional_only'] and not cert['linear_coefficient_certified']
    assert int(cert['verified_basin'])==2**71 and cert['domain_height_floor']==71
    assert cert['parameters']==PARAMS
    for name,value in cert['dependencies'].items():assert sha(R/name)==value
    for name,value in cert['proof_dependencies'].items():assert sha(ROOT/name)==value
    for name,value in cert['source_dependencies'].items():assert sha(ROOT/'src'/name)==value
    checked=audit(write=False)
    assert checked==json.loads((R/'dual-tail-capacity-audit.json').read_text())
    return cert
if __name__=='__main__':print('PASSED frozen analytic graft:',verify()['map_id'],flush=True)
