"""Independent finite validation for arithmetic and prefix coverage."""
from fractions import Fraction as F
from itertools import product
from exact_intervals import simplest_open,DLO,DHI,L2LO,L2HI
from prefix_search import Search
import json
from pathlib import Path


def direct_passes(n,m,k_bound,targets):
    initial=n
    used=0
    for completed in range(m+1):
        if n<initial or n<targets(completed,used):
            return False
        if completed==m:
            return True
        k=0
        while n%2:
            n=(3*n+1)//2
            k+=1
        while n%2==0:
            n//=2
        used+=k


def represented(n,branches):
    for b in branches:
        if 'n0' in b:
            if n==int(b['n0']):
                return True
        elif int(b['lo'])<=n<=int(b['hi']) and (n-int(b['r']))%(1<<(b['S']+1))==0:
            return True
    return False


def main():
    farey=0
    for lo_n,hi_n in product(range(0,20),repeat=2):
        if lo_n>=hi_n:
            continue
        lo,hi=F(lo_n,7),F(hi_n,7)
        result=simplest_open(lo,hi)
        q=result['q']
        assert lo<F(result['p'],q)<hi
        for qq in range(1,q):
            assert not any(lo<F(p,qq)<hi for p in range((hi*qq).__floor__()+1))
        farey+=1
    cases=0
    seeds=0
    for m,kbound,low,high in product(range(1,7),[1,3,10,30,100], [1,3,17], [63,255]):
        s=Search(m,low,high,kbound,m,1000000)
        result=s.run()
        assert result['status']=='complete'
        for n in range(low,high+1):
            if n%2==0:
                continue
            direct=direct_passes(n,m,kbound,s.target)
            indexed=represented(n,result['survivors'])
            assert direct==indexed,(m,kbound,low,high,n,direct,indexed)
            seeds+=1
        cases+=1
    out={'status':'passed','farey_intervals':farey,'prefix_cases':cases,'individual_seed_comparisons':seeds}
    path=Path(__file__).resolve().parents[1]/'results'/'exact-tools-check.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':
    main()
