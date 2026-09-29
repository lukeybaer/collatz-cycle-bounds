"""Explore maximal-sum contiguous envelope blocks plus Hercher's complement."""
from cycle_bounds_explore import D,DELTA,X,LN2,profile,cost,denominator
from pathlib import Path
import json

b=(X+1).ln()/LN2
out=[]
for m in range(96,106):
    c=D('6.99') if m<=99 else D('5.99')
    shift=c/(DELTA-1)
    k=D(7)*10**11
    rows=[]
    for _ in range(30):
        best=D(97)*m/(162*X); selected=0
        for s in range(1,m+1):
            total=D(s)*k/m
            heights=[z+shift for z in profile(s,total-s*shift,b-shift)]
            rem=m-s
            rest=min(D(rem)/X,D(97*rem+73)/(162*X)) if rem else D(0)
            candidate=rest+sum(cost(y)/3 for y in heights)
            if candidate<best:best=candidate;selected=s
        q=denominator(best/(k*LN2))
        rows.append({'K':str(k),'selected':selected,'cost_scaled':str(best*X),'next':q})
        if q<=k:break
        k=D(q)
    out.append({'m':m,'c':str(c),'K':str(k),'rows':rows})
    print(m,k,'selected',selected,'scaled cost',best*X,flush=True)
(Path(__file__).resolve().parents[1]/'results'/'partial-envelope-exploratory.json').write_text(json.dumps(out,indent=2)+'\n')
