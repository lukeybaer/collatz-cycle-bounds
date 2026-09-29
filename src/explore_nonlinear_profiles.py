"""Exploratory profiles under a proposed, UNPROVED nonlinear capacity map."""
from pathlib import Path
from cycle_bounds_explore import D,DELTA,LN2,X,cost,denominator
import json,time

ROOT=Path(__file__).resolve().parents[1]
C0=D('37.99');C1=D('40.99');H=D(71);BETA=DELTA-1
TURN=H+(C1-C0)/BETA
OFFSET=H*BETA-C0
LOW_IMAGE=H+OFFSET;HIGH_IMAGE=TURN+OFFSET

def phi(y):return max(DELTA*y-C1,min(DELTA*y-C0,y+OFFSET))
def inverse(y):
    if y<=LOW_IMAGE:return (y+C0)/DELTA
    if y<=HIGH_IMAGE:return y-OFFSET
    return (y+C1)/DELTA

def profile(m,total,b):
    if total<=m*b:return [b]*m
    def vector(t):
        out=[t]
        for _ in range(m-1):out.append(max(b,inverse(out[-1])))
        return out[::-1]
    low=b;high=total-(m-1)*b
    for _ in range(180):
        middle=(low+high)/2
        if sum(vector(middle))<total:low=middle
        else:high=middle
    values=vector((low+high)/2)
    assert abs(sum(values)/total-1)<D('1e-45')
    return values

def iterate(m,factor,initial):
    b=(D(factor)*X+1).ln()/LN2;k=D(initial);upper=D('1.4784')*m*DELTA**m
    rows=[]
    for _ in range(30):
        ys=profile(m,k,b);bound=sum(cost(y)/3 for y in ys)
        q=denominator(bound/(k*LN2))
        rows.append({'input_K':str(k),'scaled_cost':str(bound*X),'next_K':str(q)})
        if q<=k:return False,rows
        if q>upper:return True,rows
        k=D(q)
    raise AssertionError('iteration limit')

def main():
    start=time.monotonic();rows=[]
    proved=json.loads((ROOT/'results'/'K-lower-bounds-family-J38.json').read_text())
    initial={row['m']:row['K_proved'] for row in proved}
    for m in range(96,106):
        lo=1;hi=128
        assert iterate(m,hi,initial[m])[0]
        while lo<hi:
            middle=(lo+hi)//2
            if iterate(m,middle,initial[m])[0]:hi=middle
            else:lo=middle+1
        passed,chain=iterate(m,lo,initial[m]);assert passed
        rows.append({'m':m,'minimum_factor':lo,'chain':chain})
        print('UNPROVED nonlinear map, exploratory only:',m,'factor',lo,flush=True)
    result={'status':'exploratory_only','capacity_proved':False,'map':{'c0':str(C0),'c1':str(C1),'h':str(H)},
            'rows':rows,'seconds':time.monotonic()-start,
            'warning':'Neither a nonlinear capacity certificate nor an exact profile certificate nor a finite minimum-window exclusion.'}
    (ROOT/'results'/'nonlinear-profile-exploration.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
