"""Rational certificates for the sharp affine majorization relaxation.

All transcendental evaluations are enclosed using positive Taylor series.
No floating-point number is an input to a certificate.
"""
from fractions import Fraction as F
from exact_intervals import DHI,DLO,L2LO,L2HI,simplest_open
from pathlib import Path
import json

C=1-F(1,2**104)
SHIFT=C/(DHI-1)
HEIGHT_DEN=10**30
COST_DEN=10**120

def down(x,den):
    return F((x*den).__floor__(),den)

def up(x,den):
    return F((x*den).__ceil__(),den)

def log2_integer_lower(n):
    """Return a certified lower bound, reduced to a compact rational."""
    h=n.bit_length()-1
    z=F(n-2**h,n+2**h)
    # n/2^h is in [1,2), hence 0<=z<1/3.
    power=z
    lower=F(0)
    for j in range(80):
        lower+=2*power/(2*j+1)
        power*=z*z
    return down(h+lower/L2HI,HEIGHT_DEN)

def reciprocal_upper(height):
    """Upper bound for 1/(2^height-1), height>0.

    Clip DOWN, split into integer and fractional parts, and use the
    positive-term lower Taylor sum of exp(frac*lower(log(2))).
    """
    y=down(min(F(512),height),HEIGHT_DEN)
    whole=y.__floor__()
    z=(y-whole)*L2LO
    total=term=F(1)
    for j in range(1,33):
        term*=z/j
        total+=term
    return up(1/(2**whole*total-1),COST_DEN)

def profile_cost(m,k,minimum,capacity_c=C):
    shift=capacity_c/(DHI-1)
    floor=log2_integer_lower(minimum+1)
    b=floor-shift
    assert b>0
    total=F(k)-m*shift
    if total<=m*b:
        return F(m,minimum),{'mode':'minimum_only'}
    geom=F(0)
    for r in range(1,m+1):
        geom+=DHI**(r-1)
        base=(total-(m-r)*b)/geom
        if base>=b and (r==m or base<=DHI*b):
            heights=[floor]*(m-r)+[shift+base*DHI**j for j in range(r)]
            terms=[reciprocal_upper(y) for y in heights]
            return sum(terms,F(0)),{'mode':'affine_majorization','floor':str(floor),
                'ramp_length':r,'base_lower':str(down(base,HEIGHT_DEN)),
                'base_formula':'(K-m*shift-(m-r)*b)/G_r',
                'terms':[str(x) for x in terms]}
    raise AssertionError('no geometric profile')

def certificate(m,minimum,initial,capacity_c=C):
    k=initial
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    rows=[]
    for _ in range(50):
        cost,proof=profile_cost(m,k,minimum,capacity_c)
        width=cost/(k*L2LO)
        farey=simplest_open(DLO,DHI+width)
        rows.append({'input_K':k,'cost':str(cost),'width':str(width),
                     'profile':proof,'farey':farey})
        if farey['q']<=k:
            break
        k=farey['q']
        if k>upper:
            break
    else:
        raise AssertionError('no termination')
    return {'m':m,'minimum':str(minimum),'initial_K':initial,'final_K':k,'capacity_c':str(capacity_c),
            'upper_ceiling':str(upper),'conditional_contradiction':k>upper,'rows':rows}

if __name__=='__main__':
    records=[]
    for m,factor in [(92,F(73,10)),(93,15),(94,24),(95,24),(96,26),(97,32),(98,36),(99,40),(99,48),(100,64)]:
        initial=205632218873398596256 if m<=99 else 77692019770391972923
        # The m=100 initial value is read from its existing proved certificate.
        if m==100:
            previous=json.loads((Path(__file__).resolve().parents[1]/'results'/'K-lower-bounds-two-block.json').read_text())
            initial=next(row['K_proved'] for row in previous if row['m']==m)
        row=certificate(m,(factor*2**71).__floor__(),initial)
        row['minimum_factor']=str(factor)
        records.append(row)
        print(m,factor,row['conditional_contradiction'],row['final_K'],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'affine-profile-conditional-certificates.json'
    out.write_text(json.dumps(records,indent=2)+'\n')
