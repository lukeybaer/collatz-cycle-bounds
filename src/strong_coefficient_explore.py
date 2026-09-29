"""UNPROVED coefficient experiment: no resulting exclusion may be claimed."""
from cycle_bounds_explore import D,DELTA,X,LN2,profile,cost,denominator
from pathlib import Path
import json

rows=[]
for m in [96,97,98,99,100]:
    for cc in [10,15,20,25,30]:
        c=D(cc);a=c/(DELTA-1);upper=D('1.4784')*m*DELTA**m
        for factor in range(1,65):
            k=D(205632218873398596256);b=(X*factor+1).ln()/LN2
            for _ in range(30):
                ys=[z+a for z in profile(m,k-m*a,b-a)]
                total=sum(cost(y)/3 for y in ys)
                q=denominator(total/(k*LN2))
                if q<=k:break
                k=D(q)
                if k>upper:break
            if k>upper:break
        found=k>upper
        rows.append({'m':m,'unproved_c':cc,'factor':factor if found else None})
        print(m,cc,factor if found else None,flush=True)
(Path(__file__).resolve().parents[1]/'results'/'strong-coefficient-UNPROVED-exploratory.json').write_text(json.dumps(rows,indent=2)+'\n')
