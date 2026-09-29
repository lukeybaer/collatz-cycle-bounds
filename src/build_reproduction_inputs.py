"""Independent lower-bound inputs for reproduction of m=92,...,95."""
from exact_intervals import cycle_lower_bound,DHI
from fractions import Fraction as F
from pathlib import Path
import json

rows=[]
for m in range(92,96):
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    k,proof=cycle_lower_bound(m,2**71,method='elementary',stop_upper=upper)
    assert k>=205632218873398596256
    rows.append({'m':m,'minimum':str(2**71),'K_proved':k,'proof':proof})
    print(m,k,flush=True)
(Path(__file__).resolve().parents[1]/'results'/'K-lower-bounds-reproduction.json').write_text(json.dumps(rows,indent=2)+'\n')
