"""Audit modular receipts independently; brute-check small exponent cases."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
from exact_intervals import DLO,DHI
from lift_small_odd_parts import bound_next

ROOT=Path(__file__).resolve().parents[1]

def verify(path):
    cert=json.loads(path.read_text())
    m=cert['m']; J=cert['loss_integer']; U=int(cert['K_upper_inclusive'])
    assert 91<=m<=515619
    assert U>F(14784,10000)*m*DHI**m
    expected={(a,ell) for ell in range(1,J)
              for a in range(1,2**(F(12*(J-ell),7).__ceil__()),2)}
    seen=set()
    for row in cert['pairs']:
        a,ell,t=row['a'],row['ell'],row['t']
        assert (a,ell) in expected and (a,ell) not in seen
        seen.add((a,ell))
        target=((1-2**ell)*pow(a,-1,2**t))%(2**t)
        assert int(row['target'])==target
        if row['reason']=='not_in_3_power_group':
            assert t==3 and target not in (1,3)
        else:
            assert row['reason']=='least_positive_exponent_exceeds_upper'
            r,p=int(row['residue']),int(row['period'])
            assert t>=3 and p==2**(t-2) and 0<=r<p
            assert pow(3,r,2**t)==target
            assert (r if r else p)>U
        assert row['B']==max(0,t-ell-1)
    assert seen==expected
    B=max(row['B'] for row in cert['pairs'])
    c=F(J)-F(1,100)
    margin=71*DLO-B-c*(DLO+1)/(DLO-1)
    assert cert['B']==B and F(cert['capacity_c'])==c
    assert F(cert['dominance_margin_lower'])==margin
    assert cert['capacity_certified']==(margin>0)
    return len(seen)

count=0
files=sorted((ROOT/'results').glob('lifted-capacity-m*-loss*.json'))
for path in files:
    count+=verify(path)

cases=0
for a,ell,U in product(range(1,64,2),range(1,7),[1,2,3,7,31,100,300]):
    receipt=bound_next(a,ell,U)
    actual=0
    for k in range(1,U+1):
        numerator=a*3**k-1
        if numerator<=0 or (numerator&-numerator).bit_length()-1!=ell:
            continue
        next_n=numerator>>ell
        s=((next_n+1)&-(next_n+1)).bit_length()-1
        actual=max(actual,s)
    assert actual<=receipt['B'],(a,ell,U,actual,receipt)
    cases+=1

out={'status':'passed','files':len(files),'modular_receipts':count,
     'brute_force_configurations':cases,
     'note':'Checks modular coverage and small-case soundness. Mathematical induction is documented separately.'}
(ROOT/'results'/'lifted-capacity-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out),flush=True)
