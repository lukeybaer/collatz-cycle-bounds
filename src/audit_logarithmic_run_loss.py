"""Exact constants plus numerical challenges for the Chim specialization.

The written all-parameter proof, not the sampled numerical checks, establishes
the general statement. This artifact distinguishes those two roles explicitly.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
coefficient=8500*F(25,4)*F(11,10)*F(7,5)/F(69,100)**3
assert coefficient<250000
assert 250000*F(3,2)==375000
assert 180*F(25,4)*F(7,10)<800
assert 1000*F(7,10)<800 and 750000<2**20
assert F(2**12,835)>4
assert F(1,2**23)<F(1,2)
assert F(69,100)>F(1,2)
# The generic logarithm estimate used in the note has a positive margin:
# 2(q+800)-(.7q+14.3+(q+800))=.3q+785.7.
assert F(3,10)*2+F(7857,10)>0
cutoffs=[]
for j in (2,3,41,10**3,10**6,10**12,10**100):
    q=(2*j-1).bit_length(); k=2**20*j*(q+800)
    assert j<=2**(q-1) and 2*j+2<=k and k>12*j
    assert 750000*j*(q+800)<k
    cutoffs.append({'J':str(j),'q':q,'k_cutoff':str(k),'height_cutoff':str(k+2*j+2)})
# The dependent case is checked directly over mixed signs of the exponent t.
dependent=0
for k in range(1,301):
    for t in range(-20,21):
        a=3**max(0,-t);b=3**max(0,t);value=a*3**k+b
        valuation=(value&-value).bit_length()-1
        assert valuation in (1,2)
        dependent+=1
samples=[]
with localcontext() as ctx:
    ctx.prec=100;ln2=D(2).ln();delta=D(3).ln()/ln2
    eps=D(1)/D(2**23);a0=delta.ln()/ln2;eta=eps/(delta*a0)
    def loss(y):return eps*y/(y.ln()/ln2+802)
    def phi(y):return delta*y-loss(y)
    for power in (33,40,100,1000):
        start=D(2)**power;z0=D(power+802);height=start
        for t in range(1,301):
            height=phi(height)
            upper=start*delta**t*(z0/(z0+a0*t))**eta
            assert height<=upper
        x=start/(D(2**21)*(power+802));j=int(x)
        q=(2*j-1).bit_length();cut=2**20*j*(q+800)+2*j+2
        assert D(cut)<=start and D(j)>=2*loss(start)
        assert delta*loss(start)+loss(phi(start))<=D(j)*(delta+1)
        samples.append({'height_power_of_two':power,'iterations':300,
                        'ratio_to_pure_geometric':str(height/(start*delta**300))})
    exponent=str(eta)
result={'status':'passed','coefficient_upper':str(coefficient),'cutoff_examples':cutoffs,
        'dependent_valuation_checks':dependent,'decimal_challenges':samples,
        'saving_exponent_approximate':exponent,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_note_sha256':hashlib.sha256((ROOT/'logarithmic-run-loss.md').read_bytes()).hexdigest(),
        'scope':'Exact constant checks and finite high-precision challenges; not a formal proof of the general analytic argument or of Chim theorem hypotheses.'}
(ROOT/'results'/'logarithmic-run-loss-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('cutoff_examples','decimal_challenges')}),flush=True)
