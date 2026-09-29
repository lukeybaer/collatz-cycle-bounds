"""Check the written dual-tail joining argument and its frozen inputs."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
from exact_intervals import DLO,DHI
from verify_nonlinear_capacity import verify as verify_old
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
MAP='plateau-c3799-c4099-h71-dual-eps93-83'
PARAMS={'c0':'3799/100','c1':'4099/100','h':71,'epsilon1':'1/93','cutoff1':18400,
        'epsilon2':'1/83','cutoff2':164000,'switch_height':1372480}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))

def audit(write=True):
    old=verify_old();assert old['capacity_certified']
    cut=read('optimized-global-cutoffs-audit.json');assert cut['status']=='passed'
    assert cut['source_sha256']==sha(ROOT/'src/audit_optimized_cutoffs.py')
    for n,h in cut['dependencies'].items():assert sha(R/n)==h
    for n,h in cut['source_dependencies'].items():assert sha(ROOT/'src'/n)==h
    for n,h in cut['proof_dependencies'].items():assert sha(ROOT/n)==h
    assert [(r['epsilon'],r['B']) for r in cut['rows']]==[('1/93',18400),('1/83',164000)]
    proof_files=['dual-tail-capacity.md','optimized-global-cutoffs.md','fourth-power-interpolation-bound.md',
                 'four-range-interpolation-bound.md','two-regime-interpolation-bound.md',
                 'cycle-bound-corollaries.md','results/interpolation-primary-source-provenance.json']
    for receipt_name,verifier_name,count in (
        ('fourth-power-verification.json','verify_fourth_power_formal.py',10),
        ('four-range-verification.json','verify_four_range_formal.py',8),
        ('two-regime-parameters-verification.json','verify_two_regime_formal.py',7)):
        rec=json.loads((ROOT/'formal'/receipt_name).read_text(encoding='utf-8'))
        assert rec['status']=='passed' and rec['verifier_sha256']==sha(ROOT/'formal'/verifier_name)
        assert rec['toolchain_sha256']==sha(ROOT/'formal/lean-toolchain')
        assert rec['lakefile_sha256']==sha(ROOT/'formal/lakefile.toml')
        assert sum(len(r['theorems']) for r in rec['checks'])==count
        proof_files.extend(('formal/'+receipt_name,'formal/'+verifier_name))
        for row in rec['checks']:
            assert row['exit_code']==0
            assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in row['axioms_by_theorem'].values())
            src='formal/'+row['module']+'.lean';log='formal/'+row['module']+'-compiler-output.txt'
            assert row['source_sha256']==sha(ROOT/src) and row['compiler_output_sha256']==sha(ROOT/log)
            proof_files.extend((src,log))
    data=read('extended-capacity-J41-classes.json');glob=read('extended-capacity-J41-global.json')
    assert data['B']==glob['B']==100 and data['small_k_cutoff']==200
    assert glob['k_upper_exclusive']==2**19 and glob['k_lower']==1
    assert max(r['a_exponent_upper'] for r in glob['rows'])==69
    root=max(r['k']+int(r['last_a']).bit_length() for r in data['classes']);assert root==117
    depth={n:read(n+'-result.json')['max_depth'] for n in (old['producer'],old['progression'])}
    assert max(depth.values())==5
    e1,e2=F(1,93),F(1,83);B1,B2=18400,164000;c0,c1=F(3799,100),F(4099,100)
    l1lo,l1hi=DLO-e1,DHI-e1;l2lo,l2hi=DLO-e2,DHI-e2
    d1,d2=e1*B1-c1,e2*B2-c1
    switch=(e2*B2-e1*B1)/(e2-e1);assert switch==1372480>B2>B1
    assert e1*(switch-B1)+c1==e2*(switch-B2)+c1==F(1460099,100)
    assert d1>0 and d2>0 and l2lo>1
    assert 71*(DLO-1)>c0 and 71+(c1-c0)/(DLO-1)<77
    assert e1*(B1-77)>c1-c0 and e2*(B2-77)>c1-c0
    buffer=d2-(e2-e1)*DHI*B2;assert buffer>0
    assert root*DHI**max(depth.values())<B1 and 300*DHI**2<B1 and 200+69<300
    assert B1<2**19 and l2lo*200-c1>100>71
    slope=l2lo**2-DHI;assert slope>0
    margin=slope*200-(l2hi+1)*c1-(DHI-1)*100;assert margin>0
    deps=['nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json',
          'optimized-global-cutoffs-audit.json','fourth-power-exponential-bound-audit.json',
          'four-range-exponential-bound-audit.json','extended-capacity-J41-classes.json',
          'extended-capacity-J41-global.json','extended-capacity-J41-coverage-audit.json']
    src=['verify_nonlinear_capacity.py','exact_intervals.py','audit_optimized_cutoffs.py',
         'audit_fourth_power_bound.py','audit_four_range_bound.py']
    out={'status':'passed','map_id':MAP,'kind':'dual_analytic_tail_graft','parameters':PARAMS,
         'verified_basin':str(2**71),'domain_height_floor':71,'finite_root_height_upper':root,
         'finite_max_restart_depths':depth,'tail_offsets':[str(d1),str(d2)],
         'transition_buffer_lower':str(buffer),'middle_case_margin_lower':str(margin),
         'source_sha256':sha(Path(__file__)),
         'dependencies':{n:sha(R/n) for n in deps},'source_dependencies':{n:sha(ROOT/'src'/n) for n in src},
         'proof_dependencies':{n:sha(ROOT/n) for n in proof_files},
         'scope':'Checked dependencies and exact margins for the written dual-tail capacity proof. Not a new finite-cycle exclusion or external review.'}
    if write:
        (R/'dual-tail-capacity-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
        print('PASSED dual tail: buffer>',float(buffer),'middle margin>',float(margin),flush=True)
    return out
if __name__=='__main__':audit()
