"""Check the finite/analytic joining margins and their proof dependencies.

This audit supports the written graft lemma; it is not a formal proof of
the cited p-adic theorem or a new trajectory search.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from exact_intervals import DLO,DHI
from verify_nonlinear_capacity import verify as verify_old
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
MAP='plateau-c3799-c4099-h71-graft-eps1over5000-B262144'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def audit(write=True):
    old=verify_old();assert old['capacity_certified']
    analytic=read('normalized-height-exponential-bound-audit.json')
    assert analytic['status']=='passed'
    assert analytic['source_sha256']==sha(ROOT/'src'/'audit_normalized_exponential_bound.py')
    assert analytic['note_sha256']==sha(ROOT/'normalized-height-exponential-bound.md')
    formalpath=ROOT/'formal'/'core-verification-v1.json'
    assert analytic['formal_receipt_sha256']==sha(formalpath)
    formal=json.loads(formalpath.read_text());assert formal['status']=='passed'
    assert formal['verifier_sha256']==sha(ROOT/'formal'/'verify_formal.py')
    assert formal['toolchain_sha256']==sha(ROOT/'formal'/'lean-toolchain')
    assert formal['lakefile_sha256']==sha(ROOT/'formal'/'lakefile.toml')
    assert sum(len(row['theorems']) for row in formal['checks'])==10
    for row in formal['checks']:
        assert row['exit_code']==0 and row['axioms']==['propext','Classical.choice','Quot.sound']
        assert row['source_sha256']==sha(ROOT/'formal'/(row['module']+'.lean'))
        assert row['compiler_output_sha256']==sha(ROOT/'formal'/(row['module']+'-compiler-output.txt'))
    data=read('extended-capacity-J41-classes.json');glob=read('extended-capacity-J41-global.json')
    assert data['B']==glob['B']==100 and data['small_k_cutoff']==200
    assert glob['k_upper_exclusive']==2**19 and glob['k_lower']==1
    assert max(row['a_exponent_upper'] for row in glob['rows'])==69
    root=max(row['k']+int(row['last_a']).bit_length() for row in data['classes'])
    assert root==117
    depth={label:read(label+'-result.json')['max_depth'] for label in (old['producer'],old['progression'])}
    assert max(depth.values())==5
    B=2**18;eps=F(1,5000);c0=F(3799,100);c1=F(4099,100)
    lo,hi=DLO-eps,DHI-eps
    assert eps*B-c1==F(28597,2500)>0
    assert 71+(c1-c0)/(DLO-1)<77
    assert eps*(B-77)>c1-c0
    assert lo>1 and 71*(DLO-1)>c0
    assert root*DHI**max(depth.values())<B
    assert 300*DHI**2<B and 200+69<300
    assert lo*200-c1>100>71
    slope=lo**2-DHI;assert slope>0
    margin=slope*200-(hi+1)*c1-(DHI-1)*100
    assert margin>0
    dependencies=['nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json',
                  'normalized-height-exponential-bound-audit.json','extended-capacity-J41-classes.json',
                  'extended-capacity-J41-global.json','extended-capacity-J41-coverage-audit.json']
    result={'status':'passed','map_id':MAP,'kind':'analytic_tail_graft',
            'verified_basin':str(2**71),'domain_height_floor':71,
            'parameters':{'c0':'3799/100','c1':'4099/100','h':71,'epsilon':'1/5000','cutoff':B},
            'finite_root_height_upper':root,'finite_max_restart_depths':depth,
            'middle_case_margin_lower':str(margin),'tail_offset':str(eps*B-c1),
            'source_sha256':sha(Path(__file__)),
            'source_dependencies':{p:sha(ROOT/'src'/p) for p in ('verify_nonlinear_capacity.py','exact_intervals.py','audit_normalized_exponential_bound.py')},
            'dependencies':{p:sha(R/p) for p in dependencies},
            'proof_dependencies':{p:sha(ROOT/p) for p in ('analytic-tail-graft.md','normalized-height-exponential-bound.md','formal/core-verification-v1.json')},
            'scope':'Written graft proof plus checked analytic/finite dependencies and exact interval margins. External mathematical review and priority remain pending.'}
    if write:
        (R/'grafted-capacity-audit.json').write_text(json.dumps(result,indent=2)+'\n')
        print('PASSED analytic tail graft dependencies; middle-case margin>',float(margin),flush=True)
    return result
if __name__=='__main__':audit()
