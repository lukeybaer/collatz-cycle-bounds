"""Exact cutoff constants and finite high-precision composition challenges."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import json,hashlib
from exact_intervals import DLO,DHI
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
assert F(8500)*F(25,4)*F(11,10)*F(7,5)/F(69,100)**3<250000
assert F(250000)*F(51,50)==255000<260000<2**18
assert F(561,800)<1 and F(199,10)<800
assert 2**34>50*260001*836
assert F(3,10**6)*260001<F(4,5)*F(49,50)
assert DHI<F(5,3) and F(8,5)*DHI<DHI+1
assert DHI<F(317,200) and F(317,200)**3<4
assert F(3,10**6)>F(2,10**6)*F(317,300)
assert 3**64>2**99
thresholds=[]
for j in (50,51,100,10**3,10**6,10**100):
    q=(2*j-1).bit_length();k=260000*j*(q+800)
    assert j<=2**(q-1) and k>12*j and 2*j+2<=j*(q+800)
    assert 255000*j*(q+800)<k
    thresholds.append({'J':str(j),'q':q,'K_J':str(k),'Y_J':str(k+2*j+2)})
samples=[]
with localcontext() as ctx:
    ctx.prec=100;ln2=D(2).ln();delta=D(3).ln()/ln2;eps=D(3)/10**6
    def loss(y):return eps*y/(y.ln()/ln2+802)
    for exponent in (34,35,40,60,100,1000):
        y=D(2)**exponent;x=y/(D(260001)*(exponent+802));j=int(x)
        q=(2*j-1).bit_length();threshold=260000*j*(q+800)+2*j+2
        assert j>=50 and D(j)>=D(49)*x/50
        assert D(threshold)<=y and loss(y)<=D(4)*j/5
        phiy=delta*y-loss(y)
        assert delta*loss(y)+loss(phiy)<=D(j)*(delta+1)
        samples.append({'log2_height':exponent,'J':str(j),'cutoff_below_height':True})
    eta=str(eps/(delta*(delta.ln()/ln2)))
result={'status':'passed','scope':'Exact constants plus finite challenges; general proof is written separately.',
        'eta_approximate':eta,'eta_strictly_greater_than':'2/1000000','cutoffs':thresholds,'samples':samples,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_note_sha256':hashlib.sha256((ROOT/'sharpened-logarithmic-run-loss.md').read_bytes()).hexdigest(),
        'prior_proof_note_sha256':hashlib.sha256((ROOT/'logarithmic-run-loss.md').read_bytes()).hexdigest()}
(R/'sharpened-logarithmic-run-loss-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASSED sharpened logarithmic loss; eta approximately',eta,flush=True)
