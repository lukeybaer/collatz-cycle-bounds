"""Exact necessary targets from upward-rounded sums of nonlinear iterates."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib
from exact_intervals import DHI,L2LO
from verify_nonlinear_capacity import verify,NAME
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71;SCALE=10**30
DN,DD=DHI.numerator,DHI.denominator
C0=3799*SCALE//100;C1=4099*SCALE//100
OFFSET=(F(71)*(DHI-1)*SCALE-F(C0)).__ceil__()

def step(n):
    grown=(DN*n+DD-1)//DD
    return max(grown-C1,min(grown-C0,n+OFFSET))

def sum_upper(n,terms):
    total=0
    for _ in range(terms):total+=n;n=step(n)
    return total

def target(height,minimum):
    whole=height.__floor__();z=(height-whole)*L2LO;term=total=F(1)
    for j in range(1,33):term*=z/j;total+=term
    return max(minimum,(2**whole*total).__ceil__()-1)

def build(m,lo_factor,hi_factor,depth,proposal):
    assert 96<=m<=110 and lo_factor>=1 and hi_factor>=lo_factor
    low=(X*lo_factor).__floor__();high=(X*hi_factor).__floor__()
    assert F(low)==X*lo_factor and low%2==0
    if not proposal:verify()
    initial_name='family-J35-elementary-lower-bounds.json'
    candidates=[r for r in json.loads((R/initial_name).read_text()) if r['m']==m]
    assert len(candidates)==1
    initial=candidates[0];k=initial['K_proved']
    bits=(high if high%2 else high-1).bit_length()
    heights=[];targets=[];prefix=[];proofs=[]
    accumulated=0;current=bits*SCALE
    for i in range(m+1):
        used=(accumulated+SCALE-1)//SCALE;prefix.append(str(used))
        remaining=k-used;terms=m-i
        if not terms or sum_upper(71*SCALE,terms)>remaining*SCALE:
            raw=F(71);proof='minimum';threshold=low
        else:
            left=71*SCALE;right=4096*SCALE
            while left<right:
                middle=(left+right+1)//2
                if sum_upper(middle,terms)<=remaining*SCALE:left=middle
                else:right=middle-1
            raw=F(left,SCALE);proof='suffix_capacity';threshold=target(raw,low)
        heights.append(str(raw));targets.append(str(threshold));proofs.append(proof)
        accumulated+=current;current=step(current)
    cfg={'m':m,'low':str(low),'high':str(high),'K':str(k),'depth':depth,'start_log2_upper':bits,
         'prefix_odd_upper':prefix,'height_lower_rationals':heights,'height_floors':[F(h).__floor__() for h in heights],
         'targets':targets,'height_proof_kinds':proofs,'capacity_method':'nonlinear','capacity_map_id':'plateau-c3799-c4099-h71',
         'capacity_map_proved':not proposal,'capacity_certificate':NAME if not proposal else None,
         'capacity_certificate_sha256':hashlib.sha256((R/NAME).read_bytes()).hexdigest() if not proposal else None,
         'initial_K_certificate':initial_name,'verified_basin':str(X),'lower_factor':str(lo_factor),'upper_factor':str(hi_factor),
         'rounding_scale':str(SCALE),'fractional_targets':True,'height_upper_method':'largest_odd',
         'window_scope':'Global least minimum in the stated interval; all cycle members exceed its even lower endpoint.',
         'target_proof':'Completed odd runs are bounded by upward-rounded sums of Phi iterates. Each nontrivial listed height has its remaining upward sum no larger than K minus the completed upper bound.',
         'warning':'UNPROVED MAP: search results would remain conditional.' if proposal else 'Requires complete search and final profile closure for a cycle exclusion.'}
    suffix='-proposal' if proposal else ''
    name=f'nonlinear-config-m{m}-lo{str(lo_factor).replace("/","_")}-hi{str(hi_factor).replace("/","_")}{suffix}.json'
    path=R/name;assert not path.exists(),'Do not overwrite an existing search configuration'
    path.write_text(json.dumps(cfg,indent=2)+'\n')
    print(path,flush=True);print('First targets',targets[:8],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,required=True);p.add_argument('--low-factor',type=F,default=F(1))
    p.add_argument('--high-factor',type=F,required=True);p.add_argument('--depth',type=int,default=10)
    p.add_argument('--proposal',action='store_true');a=p.parse_args();build(a.m,a.low_factor,a.high_factor,a.depth,a.proposal)
