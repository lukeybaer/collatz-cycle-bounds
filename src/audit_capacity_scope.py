"""Exercise conditional-capacity rejection before and after valid caching."""
from pathlib import Path
import hashlib,json
import verify_certificates as v

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
NAME='conditional-capacity-J41-f16-certificate.json'

def rejects(action):
    try:action()
    except AssertionError:return
    raise AssertionError('Invalid conditional scope was accepted.')

def main():
    v.verified_caps.pop(NAME,None)
    rejects(lambda:v.verify_scoped_capacity(NAME,X))
    rejects(lambda:v.verify_capacity(NAME))
    assert v.verify_scoped_capacity(NAME,16*X)==(None,v.F(4099,100))
    assert NAME in v.verified_caps
    rejects(lambda:v.verify_scoped_capacity(NAME,X))
    rejects(lambda:v.verify_scoped_capacity(NAME,16*X-1))
    rejects(lambda:v.verify_capacity(NAME))
    assert v.verify_scoped_capacity(NAME,17*X)==(None,v.F(4099,100))
    result={'status':'passed','valid_hypotheses':[str(16*X),str(17*X)],
            'rejected':'Original-basin use, below-cut use, and unscoped use, including after cache population.',
            'certificate_sha256':hashlib.sha256((R/NAME).read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'verifier_sha256':hashlib.sha256((ROOT/'src'/'verify_certificates.py').read_bytes()).hexdigest()}
    (R/'conditional-capacity-scope-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
