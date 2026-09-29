"""Exact constant checks for the effective asymptotic run-loss derivation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
coefficient=F(11064,10*81)*F(11,10)/F(69,100)**3
assert coefficient<50
assert 75*F(5,4)**2==F(1875,16)<128
minimum_valuation_margin=(128-F(1875,16))*2*12**2-3
assert minimum_valuation_margin>0
assert F(126,10)<F(5,4)*12
assert F(23,60)*2+F(49,30)>0
assert F(1,4)*18432>3
samples=[]
for J in (2,3,4,7,8,31,41,100,1000,10**6,10**12):
    q=(2*J-1).bit_length();cut=128*J*(q+10)**2
    assert q>=2 and J<=2**(q-1) and cut>=18432*J
    assert 75*J*F(5*(q+10),4)**2+3<cut
    samples.append({'J':J,'q':q,'k_cutoff':cut,'height_cutoff':cut+2*J+2})
counterexample_checks=[]
for k in range(1,13):
    exponent=2*3**(k-1);a,rem=divmod(2**exponent-1,3**k)
    assert rem==0 and a%2==1
    n=(a<<k)-1;peak=a*3**k-1
    assert (n+1)&-(n+1)==2**k and peak%4==2
    nxt=peak//2;s=(nxt+1).bit_length()-1
    assert nxt==2**(exponent-1)-1 and s==exponent-1
    integer_gap=0
    while s-integer_gap-1>=0 and n+1<2**(s-integer_gap-1):integer_gap+=1
    counterexample_checks.append({'k':k,'next_run':s,'proved_gap_greater_than':integer_gap})
result={'status':'passed','coefficient_upper':str(coefficient),'minimum_valuation_margin':str(minimum_valuation_margin),
        'cutoff_examples':samples,'explicit_additive_bound_family':counterexample_checks,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'warning':'Constant and identity checks support the written proof; Bugeaud hypotheses and the general calculus argument remain written mathematical dependencies.'}
(ROOT/'results'/'asymptotic-run-loss-arithmetic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('cutoff_examples','explicit_additive_bound_family')}),flush=True)
