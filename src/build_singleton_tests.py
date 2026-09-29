from pathlib import Path
from random import Random
import json

def passes(current,original,m,targets):
    for i in range(m+1):
        if current<original or current<targets[i]:return False
        if i==m:return True
        while current%2:current=(3*current+1)//2
        while current%2==0:current//=2

rng=Random(981126)
numbers=[1,3,5,2**63-1,2**64-1,2**65-1,2**75-1,2**80-1,2**100-1,2**127-1,2**128-1]
numbers+=[rng.getrandbits(128)|1 for _ in range(100)]
rows=[]
for n in numbers:
    for m in [1,3,8]:
        for mode in [0,1,2]:
            targets=[1]*(m+1) if mode==0 else [2**min(500,60+mode*i*40) for i in range(m+1)]
            rows.append({'original':'1','current':str(n),'m':m,'targets':list(map(str,targets)),
                         'expected':passes(n,1,m,targets)})
(Path(__file__).resolve().parents[1]/'results'/'singleton-test-cases.json').write_text(json.dumps(rows)+'\n')
print(len(rows),'direct shortcut singleton reference cases')
