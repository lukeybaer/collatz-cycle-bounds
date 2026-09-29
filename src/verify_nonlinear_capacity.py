"""Verify the frozen nonlinear descriptor, with no linear-capacity fallback."""
from pathlib import Path
import hashlib,json
from audit_nonlinear_capacity import audit
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
NAME='nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(name=NAME):
    cert=json.loads((R/name).read_text())
    assert cert['kind']=='nonlinear_block_restart_native_pair' and cert['capacity_certified']
    assert not cert['conditional_only'] and not cert['linear_coefficient_certified']
    assert cert['map_id']=='plateau-c3799-c4099-h71' and int(cert['verified_basin'])==2**71
    assert cert['domain_height_floor']==71
    assert cert['parameters']=={'c0':'3799/100','c1':'4099/100','h':71,'delta':'log2(3)'}
    assert cert['definition']=='max(delta*y-c1,min(delta*y-c0,y+h*(delta-1)-c0))'
    assert cert['audit_source_sha256']==sha(ROOT/'src'/'audit_nonlinear_capacity.py')
    for name,expected in cert['source_dependencies'].items():assert sha(ROOT/'src'/name)==expected
    for name,expected in cert['dependencies'].items():assert sha(R/name)==expected
    pair=audit(producer=cert['producer'],progression=cert['progression'],write=False,
               progression_source=cert['progression_source'])
    assert pair['status']=='passed' and pair['map_id']==cert['map_id']
    return cert

if __name__=='__main__':
    print('PASSED nonlinear capacity:',verify()['map_id'],flush=True)
