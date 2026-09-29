"""Exact constant height targets for a compiled independent search."""
from exact_intervals import geom_upper,L2LO
from fractions import Fraction as F
from pathlib import Path
import argparse,json

p=argparse.ArgumentParser()
p.add_argument('--m',type=int,required=True)
p.add_argument('--factor',type=F,required=True)
p.add_argument('--depth',type=int,default=10)
p.add_argument('--k',type=int,default=205632218873398596256)
p.add_argument('--affine',action='store_true')
p.add_argument('--two-step',action='store_true')
p.add_argument('--lifted',type=Path)
p.add_argument('--strong',type=Path)
p.add_argument('--tight-height',action='store_true')
p.add_argument('--fractional-targets',action='store_true')
args=p.parse_args()
low=2**71
high=(low*args.factor).__floor__()
# A universal upper bound on the starting logarithmic height.
bits=(high+1).bit_length()
if args.tight_height:
    # A local minimum is odd. For integer n>0, ceil(log2(n+1))=bit_length(n).
    bits=(high if high%2 else high-1).bit_length()
targets=[]
heights=[]
prefix_bounds=[]
height_lower_rationals=[]
gs=[F(0)]+[geom_upper(i) for i in range(1,args.m+1)]
hs=[sum(gs[:i],F(0)) for i in range(args.m+1)]
assert sum([args.affine,args.two_step,args.lifted is not None,args.strong is not None])<=1
c=F(7,3) if args.two_step else (F(2**104-1,2**104) if args.affine else F(0))
if args.lifted:
    lifted=json.loads(args.lifted.read_text())
    assert lifted['m']==args.m and lifted['capacity_certified']
    c=F(lifted['capacity_c'])
if args.strong:
    cap=json.loads(args.strong.read_text())
    assert cap['kind'] in ('uniform_padic_and_basin','uniform_block_restart','uniform_block_restart_native_pair') and cap['capacity_certified']
    c=F(cap['capacity_c'])
for i in range(args.m+1):
    used_upper=(bits*gs[i]-c*hs[i]).__ceil__()
    prefix_bounds.append(str(used_upper))
    h=0 if i==args.m else max(0,((args.k-used_upper+c*hs[args.m-i])/gs[args.m-i]).__floor__())
    h=min(4096,h)
    heights.append(h)
    if args.fractional_targets and i<args.m:
        y=max(F(0),min(F(4096),(args.k-used_upper+c*hs[args.m-i])/gs[args.m-i]))
        y=F((y*10**30).__floor__(),10**30)
        whole=y.__floor__();z=(y-whole)*L2LO;total=term=F(1)
        for j in range(1,33):term*=z/j;total+=term
        target=max(low,(2**whole*total).__ceil__()-1)
        height_lower_rationals.append(str(y))
    else:
        target=max(low,2**h-1);height_lower_rationals.append(str(h))
    targets.append(str(target))
out={'m':args.m,'low':str(low),'high':str(high),'K':str(args.k),'depth':args.depth,
     'start_log2_upper':bits,'prefix_odd_upper':prefix_bounds,'height_floors':heights,'targets':targets,
     'affine_c':str(c),'capacity_method':'strong' if args.strong else ('lifted' if args.lifted else ('two_step' if args.two_step else 'pointwise')),
     'lifted_certificate':str(args.lifted) if args.lifted else None,
     'strong_certificate':str(args.strong) if args.strong else None,
     'height_upper_method':'largest_odd' if args.tight_height else 'legacy_bit_length_plus_one',
     'fractional_targets':args.fractional_targets,'height_lower_rationals':height_lower_rationals,
     'target_proof':'K_used <= ceil(bit_length(high+1)*G_completed-c*H_completed); G,H use a rational upper delta.'}
suffix='-strong' if args.strong else ('-lifted' if args.lifted else ('-two-step' if args.two_step else ('-affine' if args.affine else '')))
if args.tight_height:suffix+='-tight'
if args.fractional_targets:suffix+='-fractional'
path=Path(__file__).resolve().parents[1]/'results'/f'native-config-m{args.m}-f{str(args.factor).replace("/","_")}{suffix}.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(path)
print('Initial height floors:',heights[:12])
