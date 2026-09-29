"""High precision exploration only; exact certificate follows separately."""
from cycle_bounds_explore import D, DELTA, X, LN2, profile, cost, denominator
from pathlib import Path
import json

A=1/(DELTA-1)
K0=D(205632218873398596256)
rows=[]
for m in range(92,106):
    for factor in [1,8,16,24,26,28,30,32,36,40,48,64,96,128]:
        minimum=X*factor
        b=(minimum+1).ln()/LN2
        ys=[z+A for z in profile(m,K0-m*A,b-A)]
        reciprocal=sum(cost(y)/3 for y in ys)
        q=denominator(reciprocal/(K0*LN2))
        upper=D('1.4784')*m*DELTA**m
        rows.append({'m':m,'factor':factor,'cost_times_X':str(reciprocal*X),
                     'next_K':q,'exceeds_upper':q>upper,'heights':[str(y) for y in ys[:10]]})
        if q>upper:
            print(m,'first tested sufficient factor',factor,'scaled cost',str(reciprocal*X),flush=True)
            break
    else:
        print(m,'no sufficient factor tested',flush=True)
(Path(__file__).resolve().parents[1]/'results'/'affine-profile-exploratory.json').write_text(json.dumps(rows,indent=2)+'\n')
