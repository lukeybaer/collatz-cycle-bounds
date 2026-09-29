"""Exact 2-adic certificates bounding adjacent odd-run lengths.

This computes modular powers, never actual 3^K. Inputs and receipts are
integers. A residue certificate is independently checkable with one pow().
"""
from fractions import Fraction as F
from exact_intervals import DLO,DHI
from pathlib import Path
import argparse,json

def bound_next(a,ell,upper):
    t=3
    modulus=8
    target=((1-2**ell)*pow(a,-1,modulus))%modulus
    if target not in (1,3):
        return {'a':a,'ell':ell,'B':max(0,2-ell),'t':3,'reason':'not_in_3_power_group','target':target}
    residue=0 if target==1 else 1
    period=2
    while True:
        smallest=residue if residue else period
        if smallest>upper:
            return {'a':a,'ell':ell,'B':max(0,t-ell-1),'t':t,'reason':'least_positive_exponent_exceeds_upper',
                    'residue':str(residue),'period':str(period),'target':str(target)}
        t+=1
        modulus*=2
        target=((1-2**ell)*pow(a,-1,modulus))%modulus
        if pow(3,residue,modulus)!=target:
            residue+=period
        period*=2
        assert pow(3,residue,modulus)==target
        assert 0<=residue<period

def make_certificate(m,loss_integer):
    assert 91<=m<=515619
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    pairs=[]
    for ell in range(1,loss_integer):
        exponent=(F(loss_integer-ell)/F(7,12)).__ceil__()
        for a in range(1,2**exponent,2):
            pairs.append(bound_next(a,ell,upper))
    B=max(row['B'] for row in pairs)
    c=F(loss_integer)-F(1,100)
    # d*y-B-c*(d+1)/(d-1)>0: use d lower in positive first term,
    # and d lower in the decreasing rational negative factor.
    margin=71*DLO-B-c*(DLO+1)/(DLO-1)
    return {'m':m,'K_upper_inclusive':str(upper),'loss_integer':loss_integer,
            'capacity_c':str(c),'B':B,'pairs':pairs,'dominance_margin_lower':str(margin),
            'capacity_certified':margin>0,
            'proof':'See lifted-capacity.md; finite 2-adic lifts plus induction.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--m',type=int,required=True)
    p.add_argument('--loss',type=int,default=6)
    args=p.parse_args()
    result=make_certificate(args.m,args.loss)
    out=Path(__file__).resolve().parents[1]/'results'/f'lifted-capacity-m{args.m}-loss{args.loss}.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('m',args.m,'loss',args.loss,'pairs',len(result['pairs']),'B',result['B'],
          'certified',result['capacity_certified'],flush=True)
