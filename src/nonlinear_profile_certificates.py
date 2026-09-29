"""Exact nonlinear profile proposals, conditional on the UNPROVED map.

Decimal arithmetic proposes a sequence of inverse-map pieces. All accepted
profile heights, their total, each inverse relation, costs and Farey witnesses
are checked with exact rational arithmetic before writing a proposal.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D
import json
from exact_intervals import DHI,DLO,L2LO,simplest_open
from affine_profile_certificates import log2_integer_lower,reciprocal_upper,down,HEIGHT_DEN
from explore_nonlinear_profiles import profile as approximate_profile

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
C0=F(3799,100);C1=F(4099,100);H=F(71);OFFSET=H*(DHI-1)-C0
TURN=H+(C1-C0)/(DHI-1);LOW_IMAGE=H+OFFSET;HIGH_IMAGE=TURN+OFFSET
MAP='plateau-c3799-c4099-h71'

def dec(x):return D(x.numerator)/D(x.denominator)
def phi(x):return max(DHI*x-C1,min(DHI*x-C0,x+OFFSET))
def psi(x,b):
    if x<=LOW_IMAGE:y=(x+C0)/DHI
    elif x<=HIGH_IMAGE:y=x-OFFSET
    else:y=(x+C1)/DHI
    return max(b,y)

def reconstruct(m,total,b,branches):
    assert len(branches)==m-1 and b>=71 and phi(b)>=b
    coefficients=[(F(1),F(0))]
    for branch in branches:
        a,offset=coefficients[-1]
        if branch==0:pair=F(0),b
        elif branch==1:pair=a/DHI,(offset+C0)/DHI
        elif branch==2:pair=a,offset-OFFSET
        elif branch==3:pair=a/DHI,(offset+C1)/DHI
        else:raise AssertionError('unknown inverse piece')
        coefficients.append(pair)
    scale=sum(a for a,_ in coefficients);offset=sum(v for _,v in coefficients)
    top=(total-offset)/scale
    values=[a*top+v for a,v in coefficients]
    assert sum(values)==total and all(v>=b for v in values)
    assert all(values[i+1]==psi(values[i],b) for i in range(m-1))
    result=values[::-1]
    assert all(result[(i+1)%m]<=phi(result[i]) for i in range(m))
    return result

def profile_cost(m,k,minimum):
    b=log2_integer_lower(minimum+1)
    if k<=m*b:return F(m,minimum),{'mode':'minimum_only'}
    proposed=approximate_profile(m,D(k),dec(b))[::-1]
    branches=[]
    for value in proposed[:-1]:
        if value<=dec(LOW_IMAGE):branch=1;next_value=(value+dec(C0))/dec(DHI)
        elif value<=dec(HIGH_IMAGE):branch=2;next_value=value-dec(OFFSET)
        else:branch=3;next_value=(value+dec(C1))/dec(DHI)
        branches.append(0 if next_value<=dec(b) else branch)
    values=reconstruct(m,F(k),b,branches)
    terms=[reciprocal_upper(value) for value in values]
    return sum(terms,F(0)),{'mode':'nonlinear_majorization','floor':str(b),
                          'inverse_pieces_from_largest':branches,
                          'largest_height_lower':str(down(values[-1],HEIGHT_DEN)),
                          'terms':[str(term) for term in terms]}

def certificate(m,minimum,initial):
    k=initial;upper=(F(14784,10000)*m*DHI**m).__ceil__();rows=[]
    for _ in range(40):
        cost,proof=profile_cost(m,k,minimum);width=cost/(k*L2LO)
        farey=simplest_open(DLO,DHI+width)
        rows.append({'input_K':k,'cost':str(cost),'width':str(width),'profile':proof,'farey':farey})
        if farey['q']<=k:break
        k=farey['q']
        if k>upper:break
    else:raise AssertionError('iteration did not settle')
    return {'m':m,'minimum':str(minimum),'initial_K':initial,'final_K':k,'upper_ceiling':str(upper),
            'capacity_map_id':MAP,'capacity_map_proved':False,'conditional_contradiction':k>upper,
            'warning':'Exact arithmetic under an additional nonlinear capacity hypothesis that has not yet been proved. This is not a cycle exclusion.',
            'rows':rows}

def main():
    explored=json.loads((R/'nonlinear-profile-exploration.json').read_text())
    initial={r['m']:r['K_proved'] for r in json.loads((R/'K-lower-bounds-family-J38.json').read_text())}
    rows=[]
    for candidate in explored['rows']:
        m=candidate['m'];factor=candidate['minimum_factor']
        row=certificate(m,factor*X,initial[m]);assert row['conditional_contradiction']
        row['minimum_factor']=factor;rows.append(row)
        (R/'nonlinear-profile-proposals.json').write_text(json.dumps(rows,indent=2)+'\n')
        print('Exact profile, still conditional on unproved nonlinear map:',m,factor,row['final_K'],flush=True)

if __name__=='__main__':main()
