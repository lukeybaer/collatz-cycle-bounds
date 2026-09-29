"""Freeze a fully audited block-restart coefficient and conditional inputs."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse
from exact_intervals import cycle_lower_bound,DHI
from affine_profile_certificates import certificate
from cycle_bounds_explore import D,DELTA,LN2,profile,cost,denominator
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def save(name,obj):(R/name).write_text(json.dumps(obj,indent=2)+'\n')
def exploratory(m,factor,initial,c):
    shift=c/(DELTA-1);floor=(D(factor)*X+1).ln()/LN2;k=D(initial)
    upper=D('1.4784')*m*DELTA**m
    for _ in range(40):
        ys=[v+shift for v in profile(m,k-m*shift,floor-shift)]
        bound=sum(cost(y)/3 for y in ys)
        q=denominator(bound/(k*LN2))
        if q<=k:return False
        k=D(q)
        if k>upper:return True
    raise AssertionError('exploratory iteration')
def run(J,resume=False):
    pyname=f'family-J{J}-python-full.json';cppname=f'family-J{J}-precise-full-result.json'
    coverage=f'extended-capacity-J{J}-coverage-audit.json'
    py=read(pyname);cpp=read(cppname);cov=read(coverage)
    assert py['status']=='passed' and py['full_input'] and cpp['capacity_exceptions_discharged'] and cov['status']=='passed'
    assert py['source_sha256']==hashlib.sha256((ROOT/'src'/'verify_family_capacity.py').read_bytes()).hexdigest()
    assert py['seeds']==cpp['seeds']==cov['seeds'] and py['classes']==cpp['classes']==cov['classes']
    C=F(100*J-1,100);capname=f'family-capacity-J{J}-certificate.json'
    deps=[f'extended-capacity-J{J}-global.json',f'extended-capacity-J{J}-classes.json',coverage,pyname,cppname,f'family-J{J}-precise-full-metadata.json','log2-mantissa-table.json']
    save(capname,{'kind':'uniform_block_restart','J':J,'capacity_certified':True,'capacity_c':str(C),'verified_basin':str(X),
      'proof':'../block-restart-capacity.md','analytic_status':'internally derived and audited; external review and novelty review pending',
      'scope':'all hypothetical nontrivial positive cycles, uniformly in m',
      'independent_proof':'Python parity-bisection checker uses coarse integer heights and does not depend on the C# logarithm table.',
      'dependencies':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in deps}})
    lower=read(f'K-lower-bounds-family-J{J}.json') if resume and (R/f'K-lower-bounds-family-J{J}.json').exists() else []
    profiles=read(f'family-J{J}-conditional-certificates.json') if resume and (R/f'family-J{J}-conditional-certificates.json').exists() else []
    unavailable=[]
    for m in range(96,111):
        upper=(F(14784,10000)*m*DHI**m).__ceil__()
        previous=next((row for row in lower if row['m']==m),None)
        if previous:k=previous['K_proved']
        else:
            k,rows=cycle_lower_bound(m,X,method='three_block',capacity_c=C,stop_upper=upper)
            lower.append({'m':m,'minimum':str(X),'K_proved':k,'rows':rows,'capacity_certificate':capname})
            save(f'K-lower-bounds-family-J{J}.json',lower)
        if m<=105:
            if any(row['m']==m for row in profiles):continue
            lo=1;hi=128
            if not exploratory(m,hi,k,D(C.numerator)/D(C.denominator)):
                unavailable.append({'m':m,'maximum_factor_tried':hi,'status':'no_exploratory_contradiction_in_range'})
                save(f'family-J{J}-factor-limits.json',unavailable)
                print('No conditional contradiction up to factor128:',m,flush=True)
                continue
            while lo<hi:
                mid=(lo+hi)//2
                if exploratory(m,mid,k,D(C.numerator)/D(C.denominator)):hi=mid
                else:lo=mid+1
            factor=lo
            cert=certificate(m,factor*X,k,C)
            assert cert['conditional_contradiction']
            cert.update(capacity_certificate=capname,minimum_factor=factor,warning='Conditional until the finite minimum window is excluded.')
            profiles.append(cert);save(f'family-J{J}-conditional-certificates.json',profiles)
            print('J',J,'m',m,'K',k,'factor',factor,'finalK',cert['final_K'],flush=True)
        else:print('J',J,'m',m,'K',k,flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=35);p.add_argument('--resume',action='store_true');a=p.parse_args();run(a.J,a.resume)
