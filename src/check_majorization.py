"""Exact finite sanity checks of the cyclic growth majorization theorem.

The proof is in ../majorization-lemma.md. Enumeration is a falsification test,
not a proof of the unbounded theorem. Uses only Python's standard library.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import time


def extremizer(m, b, d, total):
    """Exact profile, selecting the number of entries strictly above the floor."""
    if total == m*b:
        return [b]*m
    for r in range(1, m+1):
        geom = sum((d**i for i in range(r)), F(0))
        a = (total-(m-r)*b)/geom
        if a >= b and (r == m or a <= d*b):
            return [b]*(m-r)+[a*d**i for i in range(r)]
    raise AssertionError((m, b, d, total))


def main():
    start=time.perf_counter()
    tested=0
    settings=[]
    for d in [F(3,2), F(8,5), F(2)]:
        for m in range(2,7):
            count=0
            for xs in product(range(2,11), repeat=m):
                if any(F(xs[(i+1)%m]) > d*xs[i] for i in range(m)):
                    continue
                total=F(sum(xs))
                ys=extremizer(m,F(2),d,total)
                us=sorted(map(F,xs))
                assert sum(ys)==total
                assert all(ys[(i+1)%m]<=d*ys[i] for i in range(m))
                assert all(sum(us[:j])>=sum(ys[:j]) for j in range(1,m))
                assert sum(1/u for u in us)<=sum(1/y for y in ys)
                count+=1
            tested+=count
            settings.append({'d':str(d),'m':m,'feasible_vectors':count})
            print(settings[-1],flush=True)
    result={'status':'passed','feasible_vectors':tested,'settings':settings,
            'elapsed_seconds':time.perf_counter()-start,
            'scope':'Finite exact sanity check; the theorem rests on its proof.'}
    path=Path(__file__).resolve().parents[1]/'results'/'majorization-check.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
