"""Exploratory Decimal arithmetic, NOT a rigorous interval certificate.

Compares cycle reciprocal-sum bounds and iterates a rational-denominator test.
"""
from decimal import Decimal as D, getcontext, ROUND_FLOOR
from fractions import Fraction as F
from pathlib import Path
import json

getcontext().prec=120
LN2=D(2).ln()
DELTA=D(3).ln()/LN2
X=D(2)**71


def geom(r):
    return (DELTA**r-1)/(DELTA-1)


def cost(x):
    if x>1000:
        return D('1e-290')  # conservative cap in this exploratory regime
    return 3/((x*LN2).exp()-1)


def profile(m,k,b):
    if k<=m*b:
        return [b]*m
    for r in range(1,m+1):
        a=(k-(m-r)*b)/geom(r)
        if a>=b and (r==m or a<=DELTA*b):
            return [b]*(m-r)+[a*DELTA**j for j in range(r)]
    raise AssertionError((m,k,b))


def hercher(m,k):
    best=D(97)*m/(54*X)
    choice=0
    for r in range(1,m+1):
        v=D(r)*k/(m*geom(r))
        if v<(D(162)*X/97).ln()/LN2:
            continue
        rem=m-r
        small=D(0) if rem==0 else (D(3)/X if rem==1 else D(97*rem+73)/(54*X))
        bound=small+sum(cost(v*DELTA**j) for j in range(r))
        if bound<best:
            best,choice=bound,r
    return best,choice


def upper_approximants():
    z=DELTA
    pp,p=0,1
    qq,q=1,0
    out=[]
    for i in range(100):
        a=int(z)
        if i%2==1:
            for t in range(1,a+1):
                np,nq=t*p+pp,t*q+qq
                err=D(np)/nq-DELTA
                if err>0:
                    out.append((np,nq,err))
        np,nq=a*p+pp,a*q+qq
        pp,p=p,np
        qq,q=q,nq
        if q>10**45:
            break
        z=1/(z-a)
    return out


APPROX=upper_approximants()


def denominator(eps):
    return next(q for p,q,e in APPROX if e<eps)


def iterate(m,method):
    k=D(7)*10**11
    upper=D('1.4784')*m*DELTA**m
    rows=[]
    for it in range(30):
        h,r=hercher(m,k)
        ys=profile(m,k,(X+1).ln()/LN2)
        own=sum(cost(y) for y in ys)
        bound=h if method=='hercher' else min(h,own)
        eps=bound/(k*3*LN2)
        q=denominator(eps)
        rows.append({'K':str(k),'hercher_r':r,'hercher_scaled':str(h*X),
                     'profile_scaled':str(own*X),'next_denominator':q})
        if q>upper:
            return {'m':m,'method':method,'excluded_exploratory':True,'upper':str(upper),'rows':rows}
        if q<=k:
            return {'m':m,'method':method,'excluded_exploratory':False,'upper':str(upper),'rows':rows}
        k=D(q)
    raise AssertionError('iteration did not settle')


if __name__=='__main__':
    results=[iterate(m,method) for m in range(90,101) for method in ['hercher','profile']]
    path=Path(__file__).resolve().parents[1]/'results'/'cycle-bounds-exploratory.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(results,indent=2)+'\n')
    for r in results:
        print(r['m'],r['method'],r['excluded_exploratory'],len(r['rows']),r['rows'][-1],flush=True)
