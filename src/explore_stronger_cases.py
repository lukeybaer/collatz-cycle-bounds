"""Exact finite-case SIZE estimates only; these certify no new coefficient."""
from pathlib import Path
import json,time
X=2**71;S=10**6;DL=1584962;DU=1584963;BL=DL-S;BU=DU-S
def ceildiv(n,d):return -(-n//d)
rows=[];watch=time.monotonic()
for J in [31,33,35,38,41]:
    B=100;master=1<<(J+B);mask=master-1;inv3=pow(3,-1,master);p=1
    total=classes=maxclass=0;maxbits=0
    for k in range(1,300):
        p=p*inv3&mask;low=max(1,ceildiv(X+2,1<<k))
        for ell in range(1,J):
            q1=ceildiv((100*J-1)*10000+1000-ell*S,BL)
            for s in range(1,B+1):
                q2=ceildiv((100*J-1)*(DU+S)*10000-BL*DL*k+BU*S*s-(ell*S+998000)*S,BL*(DL+S))
                q=min(q1,q2)
                if q<=0 or low>=1<<q:continue
                modulus=1<<(ell+s+1);r=(((1<<(ell+s))+1-(1<<ell))*p)&(modulus-1)
                first=low+((r-low)&(modulus-1));high=(1<<q)-1
                if first>high:continue
                last=high-((high-r)&(modulus-1));count=(last-first)//modulus+1
                total+=count;classes+=1;maxclass=max(maxclass,count);maxbits=max(maxbits,((last<<k)-1).bit_length())
    row={'J':J,'B':B,'classes':classes,'seeds':str(total),'largest_class':str(maxclass),'maximum_seed_bits':maxbits,'status':'size_estimate_only_not_a_capacity_certificate'}
    rows.append(row);print(row,flush=True)
root=Path(__file__).resolve().parents[1]
(root/'results'/'stronger-capacity-size-estimates.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Seconds',time.monotonic()-watch)
