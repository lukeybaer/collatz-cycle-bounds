from pathlib import Path
import json

def passes(n,m,targets):
    initial=n
    for i in range(m+1):
        if n<initial or n<targets[i]:
            return False
        if i==m:
            return True
        while n%2:
            n=(3*n+1)//2
        while n%2==0:
            n//=2

cases=[]
for m in range(1,8):
    for low in [1,3,17]:
        for high in [63,255]:
            for mode in range(4):
                targets=[max(low,(i+1)**mode) for i in range(m+1)]
                cases.append({'m':m,'low':str(low),'high':str(high),
                              'targets':list(map(str,targets)),
                              'expected':[str(n) for n in range(low,high+1,2) if passes(n,m,targets)]})
path=Path(__file__).resolve().parents[1]/'results'/'native-test-cases.json'
path.write_text(json.dumps(cases)+'\n')
print(len(cases),'independent direct-iteration cases')
