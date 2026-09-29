"""Small exact rational tools. No floating point is used in certificates."""
from fractions import Fraction as F


def log_interval(integer, terms=220):
    """atanh series with an explicit positive-tail geometric bound."""
    z=F(integer-1,integer+1)
    z2=z*z
    power=z
    lower=F(0)
    for j in range(terms):
        lower+=2*power/(2*j+1)
        power*=z2
    tail=2*power/((2*terms+1)*(1-z2))
    return lower,lower+tail


L2LO,L2HI=log_interval(2)
L3LO,L3HI=log_interval(3)
DLO,DHI=L3LO/L2HI,L3HI/L2LO
# Compact enclosing rational bounds, validated against the exact series.
DEN=10**100
DLO=F((DLO*DEN).__floor__(),DEN)
DHI=F((DHI*DEN).__ceil__(),DEN)
L2LO=F((L2LO*DEN).__floor__(),DEN)
L2HI=F((L2HI*DEN).__ceil__(),DEN)


def geom_upper(m):
    return sum((DHI**j for j in range(m)),F(0))


def simplest_open(lo,hi):
    """Minimum-denominator rational in an open rational interval.

    Stern-Brocot bracketing with exact accelerated jumps. The returned Farey
    neighbors enclose the entire interval; determinant 1 certifies minimality.
    """
    assert 0<=lo<hi
    a,b,c,d=0,1,1,0
    iterations=0
    while True:
        iterations+=1
        p,q=a+c,b+d
        med=F(p,q)
        if med<=lo:
            step=((lo*b-a)/(c-lo*d)).__floor__()
            assert step>=1
            a,b=a+step*c,b+step*d
        elif med>=hi:
            step=((c-hi*d)/(hi*b-a)).__floor__()
            assert step>=1
            c,d=c+step*a,d+step*b
        else:
            assert c*b-a*d==1
            assert F(a,b)<=lo and (d==0 or F(c,d)>=hi)
            return {'p':p,'q':q,'left':[a,b],'right':[c,d],'iterations':iterations}


def cycle_lower_bound(m,minimum,initial=1,method='elementary',stop_upper=None,capacity_c=F(0)):
    """Suffix-balanced elementary cycle bound with integer height floors.

    For each t, n >= 2^floor(t*K/(m*G_t))-1. Every term also n>minimum.
    Sum 1/n bounds the logarithmic cycle error. Heights >=512 are clipped
    down to512, preserving an upper bound and keeping the certificate small.
    """
    gs=[None]+[geom_upper(t) for t in range(1,m+1)]
    hgs=[None]+[(gs[t]-t)/(DHI-1) for t in range(1,m+1)]
    k=initial
    rows=[]
    for _ in range(50):
        hs=[min(512,((F(t*k,m)+capacity_c*hgs[t])/gs[t]).__floor__()) for t in range(1,m+1)]
        terms=[F(1,max(minimum,2**h-1)) for h in hs]
        cost=sum(terms,F(0))
        if method in ('two_block','three_block'):
            # Hercher's two-block bound, with a direct proof in
            # ../two-block-bound.md. Cost here is one third of sum T.
            cost=min(cost,F(35*m,54*minimum))
            for s in range(1,m+1):
                rem=m-s
                rest=F(0) if rem==0 else (F(1,minimum) if rem==1 else F(35*rem+19,54*minimum))
                cost=min(cost,rest+sum(terms[:s],F(0)))
            if method=='three_block':
                # Hercher (2023), Theorem 14 and Corollary 17; the
                # verified-basin threshold, not merely a cycle minimum.
                cost=min(cost,F(97*m,162*minimum))
                for s in range(1,m+1):
                    rem=m-s
                    rest=F(0) if rem==0 else (F(1,minimum) if rem==1 else F(97*rem+73,162*minimum))
                    cost=min(cost,rest+sum(terms[:s],F(0)))
        elif method!='elementary':
            raise ValueError(method)
        width=cost/(k*L2LO)
        result=simplest_open(DLO,DHI+width)
        rows.append({'input_K':k,'method':method,'capacity_c':str(capacity_c),'height_floors':hs,'cost':str(cost),
                     'width':str(width),'farey':result})
        if result['q']<=k:
            return k,rows
        k=result['q']
        if stop_upper is not None and k>stop_upper:
            return k,rows
    raise AssertionError('failed to stabilize')


def ceildiv(a,b):
    return -(-a//b)
