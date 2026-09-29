"""Certified suffix bounds using finite lifted capacity certificates."""
from exact_intervals import cycle_lower_bound,DHI
from lift_small_odd_parts import make_certificate
from pathlib import Path
from fractions import Fraction as F
import json

ROOT=Path(__file__).resolve().parents[1]
rows=[]
for m in range(96,106):
    for J in [7,6,5,4]:
        cert=make_certificate(m,J)
        if cert['capacity_certified']:
            break
    else:
        raise AssertionError('no usable capacity')
    path=ROOT/'results'/f'lifted-capacity-m{m}-loss{J}.json'
    path.write_text(json.dumps(cert,indent=2)+'\n')
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    k,proof=cycle_lower_bound(m,2**71,method='three_block',stop_upper=upper,capacity_c=F(cert['capacity_c']))
    rows.append({'m':m,'minimum':str(2**71),'capacity_certificate':path.name,'K_proved':k,'proof':proof})
    print(m,'c',cert['capacity_c'],'B',cert['B'],'K>=',k,flush=True)
(ROOT/'results'/'K-lower-bounds-lifted.json').write_text(json.dumps(rows,indent=2)+'\n')
