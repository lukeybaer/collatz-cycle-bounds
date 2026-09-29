"""Exact directed bounds for the rounded coefficient in the review paper."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
from exact_intervals import DLO,DHI,L2LO

ROOT=Path(__file__).resolve().parents[1]
lamlo=DLO-F(1,93)
Ahi=(DHI/lamlo)**28
coefficient_hi=10*Ahi/(lamlo-1)
assert coefficient_hi<F(2108,100)
assert 1+F(133,10)*F(46057,100000)/L2LO+F(532,10)<64
assert F(133,10)*F(2,3)+F(143,10)/64+F(64,1024)<10
assert F(317,200)**3<4
assert Ahi/(lamlo-1)*(F(2,3)+F(47,1024))<F(151,100)
out={'status':'passed','cycle_coefficient_upper_rational':str(coefficient_hi),
     'rounded_coefficient_upper':'21.08',
     'cycle_height_constant_check':'10m for m>=1024, using log2(m)<=m/64 for m>=1024',
     'scope':'Exact rational final coefficient and cycle-height constants; monotonic logarithm argument remains in the written proof.',
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'review_manuscript_sha256':hashlib.sha256((ROOT/'fourth-power-review-manuscript.md').read_bytes()).hexdigest()}
(ROOT/'results'/'fourth-power-review-constants-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('PASSED exact fourth-power coefficients and cycle-height constants.',flush=True)
