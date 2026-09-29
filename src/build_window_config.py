"""Build a scoped finite global-minimum window with exact necessary targets.

The lower endpoint is a search hypothesis, not a convergence verification.
Conditional capacity coefficients are accepted only after checking that every
candidate in this window satisfies the coefficient's minimum hypothesis.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json
from exact_intervals import geom_upper,L2LO
from verify_certificates import verify_scoped_capacity

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71

def build(m,low_factor,high_factor,k,capname,depth):
    assert X*low_factor==(X*low_factor).__floor__(),'Use an integral lower endpoint.'
    low=int(X*low_factor);high=(X*high_factor).__floor__()
    assert X<=low<=high and low%2==0,'Lower endpoint must be even, so every odd candidate exceeds it.'
    mm,c=verify_scoped_capacity(capname,low);assert mm is None or mm==m
    bits=(high if high%2 else high-1).bit_length()
    gs=[F(0)]+[geom_upper(i) for i in range(1,m+1)]
    hs=[sum(gs[:i],F(0)) for i in range(m+1)]
    targets=[];floors=[];prefix=[];heights=[]
    for i in range(m+1):
        used=(bits*gs[i]-c*hs[i]).__ceil__();prefix.append(str(used))
        raw=F(0) if i==m else max(F(0),min(F(4096),(k-used+c*hs[m-i])/gs[m-i]))
        floors.append(raw.__floor__())
        y=F((raw*10**30).__floor__(),10**30);heights.append(str(y))
        whole=y.__floor__();z=(y-whole)*L2LO;term=total=F(1)
        for j in range(1,33):term*=z/j;total+=term
        targets.append(str(max(low,(2**whole*total).__ceil__()-1)))
    cfg={'m':m,'low':str(low),'high':str(high),'K':str(k),'depth':depth,
         'start_log2_upper':bits,'prefix_odd_upper':prefix,'height_floors':floors,'targets':targets,
         'affine_c':str(c),'capacity_method':'scoped','capacity_certificate':capname,
         'height_upper_method':'largest_odd','fractional_targets':True,'height_lower_rationals':heights,
         'window_scope':'A hypothetical cycle whose global least minimum is an odd integer in [low,high]. Every cycle member therefore exceeds the even lower endpoint.',
         'verified_basin':str(X),'lower_factor':str(low_factor),'upper_factor':str(high_factor),
         'target_proof':'All members exceed low. Sum of completed odd runs is at most ceil(B*G_i-c*H_i); the remaining capacity forces the listed lower targets.'}
    lo=str(low_factor).replace('/','_');hi=str(high_factor).replace('/','_')
    name=f'native-config-m{m}-lo{lo}-hi{hi}-scoped.json';path=R/name
    assert not path.exists(),'Refusing to overwrite an existing configuration.'
    path.write_text(json.dumps(cfg,indent=2)+'\n')
    print(path,flush=True);print('First targets:',targets[:10],flush=True)
    return cfg

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,required=True)
    p.add_argument('--low-factor',type=F,required=True);p.add_argument('--high-factor',type=F,required=True)
    p.add_argument('--k',type=int,default=205632218873398596256)
    p.add_argument('--capacity-certificate',required=True);p.add_argument('--depth',type=int,default=10)
    a=p.parse_args();build(a.m,a.low_factor,a.high_factor,a.k,a.capacity_certificate,a.depth)
