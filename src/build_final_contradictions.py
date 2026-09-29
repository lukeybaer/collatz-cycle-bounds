"""Conditional final arithmetic, independent of the finite prefix search.

An output here alone is NOT a cycle exclusion: the stated minimum threshold
must first be proved by a complete finite prefix certificate.
"""
from exact_intervals import cycle_lower_bound,DHI
from fractions import Fraction as F
from pathlib import Path
import json

out=[]
for m,factor in [(92,F(73,10)),(93,15),(94,24),(95,24),(96,32),(97,40),(98,40)]:
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    minimum=(factor*2**71).__floor__()
    k,rows=cycle_lower_bound(m,minimum,initial=205632218873398596256,stop_upper=upper)
    result={'m':m,'assumed_minimum_greater_than':str(minimum),
            'upper_bound_integer_ceiling':str(upper),'new_K_lower_bound':str(k),
            'conditional_contradiction':k>upper,'rows':rows,
            'warning':'Conditional only until the minimum-window exclusion is fully certified.'}
    out.append(result)
    print(m,'conditional contradiction:',k>upper,'K>=',k,'K<',upper,flush=True)
path=Path(__file__).resolve().parents[1]/'results'/'conditional-final-contradictions.json'
path.write_text(json.dumps(out,indent=2)+'\n')
