"""Conditional profile/Farey contradictions giving smaller global K uppers.

The initial K>=T is a temporary assumption, not a proved lower bound.
A contradiction with the published upper bound proves K<T.
"""
from pathlib import Path
from fractions import Fraction as F
import json
from exact_intervals import DHI
from affine_profile_certificates import certificate
from cycle_bounds_explore import D,DELTA,LN2,profile,cost,denominator
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71;C=F(3499,100);CC=D('34.99')
def can_contradict(m,initial):
    shift=CC/(DELTA-1);floor=D(X+1).ln()/LN2;k=D(initial);upper=D('1.4784')*m*DELTA**m
    for _ in range(50):
        ys=[v+shift for v in profile(m,k-m*shift,floor-shift)]
        bound=sum(cost(y)/3 for y in ys)
        try:q=denominator(bound/(k*LN2))
        except StopIteration:return True # exploratory only; exact certificate follows
        if q<=k:return False
        k=D(q)
        if k>upper:return True
    raise AssertionError('exploratory upper iteration')
rows=[]
for m in range(96,111):
    external=(F(14784,10000)*m*DHI**m).__ceil__()
    lo=1;hi=external
    while hi-lo>max(1,external//10**6):
        mid=(lo+hi)//2
        if can_contradict(m,mid):hi=mid
        else:lo=mid
    proof=certificate(m,X,hi,C)
    assert proof['conditional_contradiction'] and hi<external
    proof['purpose']='temporary_lower_assumption_to_prove_upper'
    proof['capacity_certificate']='family-capacity-J35-certificate.json'
    proof['conclusion_K_less_than']=str(hi)
    proof['warning']='The initial K in these rows is ASSUMED for contradiction. It is not a proved lower bound.'
    rows.append(proof)
    (R/'improved-K-upper-bounds-J35.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('m',m,'K <',hi,'old',external,'ratio',round(hi/external,4),flush=True)
