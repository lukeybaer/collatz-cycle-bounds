"""Explore an analytic tail graft; proposals are not capacity certificates."""
from pathlib import Path
import json,time,hashlib
import explore_nonlinear_profiles as base
from cycle_bounds_explore import D,DELTA

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
original_inverse=base.inverse
epsilon=D(1)/5000;cut=D(2**18);slope=DELTA-epsilon
offset=epsilon*cut-base.C1;image=DELTA*cut-base.C1
assert offset>0
def inverse(y):
    return original_inverse(y) if y<=image else (y-offset)/slope
base.inverse=inverse
initial={row['m']:row['K_proved'] for row in json.loads((R/'K-lower-bounds-family-J38.json').read_text())}
rows=[];start=time.monotonic()
for m in range(96,106):
    lo=1;hi=128
    assert base.iterate(m,hi,initial[m])[0]
    while lo<hi:
        middle=(lo+hi)//2
        if base.iterate(m,middle,initial[m])[0]:hi=middle
        else:lo=middle+1
    passed,chain=base.iterate(m,lo,initial[m]);assert passed
    rows.append({'m':m,'minimum_factor':lo,'chain':chain})
    print('UNPROVED graft, approximate profile:',m,lo,flush=True)
result={'status':'exploratory_only','capacity_proved':False,'exact_profiles':False,
        'map_id':'plateau-c3799-c4099-h71-graft-eps1over5000-B262144',
        'rows':rows,'seconds':time.monotonic()-start,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'warning':'The graft requires its own proof and dependency audit; no exclusion follows from these approximate profiles.'}
(R/'grafted-profile-exploration.json').write_text(json.dumps(result,indent=2)+'\n')
