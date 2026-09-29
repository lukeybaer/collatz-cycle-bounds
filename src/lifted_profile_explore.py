"""Explore the newly derived subordinate-height envelope (not certificates)."""
from cycle_bounds_explore import D,DELTA,X,LN2,profile,cost,denominator
from pathlib import Path
import json

rows=[]
for m in range(92,106):
    c=D('6.99') if m<=99 else D('5.99')
    shift=c/(DELTA-1)
    start=D(205632218873398596256 if m<=101 else 77692117359936589403)
    upper=D('1.4784')*m*DELTA**m
    for factor in range(1,101):
        k=start
        b=(factor*X+1).ln()/LN2
        for _ in range(30):
            heights=[z+shift for z in profile(m,k-m*shift,b-shift)]
            reciprocal=sum(cost(y)/3 for y in heights)
            q=denominator(reciprocal/(k*LN2))
            if q<=k:break
            k=D(q)
            if k>upper:break
        if k>upper:
            rows.append({'m':m,'factor':factor,'c':str(c),'K':str(k),'cost_scaled':str(reciprocal*X)})
            print(m,'first sufficient factor',factor,'K',k,flush=True)
            break
    else: print(m,'none',flush=True)
(Path(__file__).resolve().parents[1]/'results'/'lifted-profile-exploratory.json').write_text(json.dumps(rows,indent=2)+'\n')
