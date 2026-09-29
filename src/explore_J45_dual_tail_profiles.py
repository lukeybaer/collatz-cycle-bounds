"""Explore an analytic tail graft; proposals are not capacity certificates."""
from pathlib import Path
import json,time,hashlib
import explore_nonlinear_profiles as base
from cycle_bounds_explore import D,DELTA

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
base.C1=D('44.99')
base.TURN=base.H+(base.C1-base.C0)/base.BETA
base.HIGH_IMAGE=base.TURN+base.OFFSET
original_inverse=base.inverse
epsilon=D(1)/93;cut=D(18400);slope=DELTA-epsilon
epsilon2=D(1)/83;cut2=D(164000);slope2=DELTA-epsilon2
offset2=epsilon2*cut2-base.C1;image2=DELTA*D(1372480)-D('14604.99')
offset=epsilon*cut-base.C1;image=DELTA*cut-base.C1
assert offset>0
def inverse(y):
    if y<=image:return original_inverse(y)
    return (y-offset)/slope if y<=image2 else (y-offset2)/slope2
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
        'map_id':'plateau-c3799-c4499-h71-dual-eps93-83',
        'rows':rows,'seconds':time.monotonic()-start,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'warning':'The graft requires its own proof and dependency audit; no exclusion follows from these approximate profiles.'}
(R/'J45-dual-tail-profile-exploration.json').write_text(json.dumps(result,indent=2)+'\n')
