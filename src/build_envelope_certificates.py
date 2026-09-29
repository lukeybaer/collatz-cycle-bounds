from affine_profile_certificates import certificate
from lift_small_odd_parts import make_certificate
from pathlib import Path
from fractions import Fraction as F
import json

root=Path(__file__).resolve().parents[1]
initials=json.loads((root/'results'/'K-lower-bounds-lifted.json').read_text())
rows=[]
for m,factor in [(96,24),(97,29),(98,34),(99,39),(100,43),(101,48),(102,53)]:
    start=next(row for row in initials if row['m']==m)
    cap=json.loads((root/'results'/start['capacity_certificate']).read_text())
    assert cap['capacity_certified']
    row=certificate(m,factor*2**71,start['K_proved'],F(cap['capacity_c']))
    row['capacity_certificate']=start['capacity_certificate']
    row['minimum_factor']=factor
    row['warning']='Conditional until the full minimum window has been excluded. Depends on the subordinate height envelope proof.'
    rows.append(row)
    print(m,factor,row['conditional_contradiction'],row['final_K'],flush=True)
(root/'results'/'envelope-conditional-certificates.json').write_text(json.dumps(rows,indent=2)+'\n')
