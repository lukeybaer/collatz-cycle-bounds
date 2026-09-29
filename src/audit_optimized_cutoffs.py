"""Exact cutoff/warmup refinements of the already proved local arguments."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import hashlib,json
from exact_intervals import DLO,DHI,L2LO,L2HI,log_interval
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lograt(q):
    q=F(q);power=0
    while q>=2:q/=2;power+=1
    while q<1:q*=2;power-=1
    lo,hi=log_interval(q)
    if power>=0:return lo+power*L2LO,hi+power*L2HI
    return lo+power*L2HI,hi+power*L2LO
def compact(q):return str(F((q*10**60).__ceil__(),10**60))
deps=['fourth-power-exponential-bound-audit.json','four-range-exponential-bound-audit.json']
notes=['fourth-power-interpolation-bound.md','four-range-interpolation-bound.md']
sources=['audit_fourth_power_bound.py','audit_four_range_bound.py']
for name,note,source in zip(deps,notes,sources):
    data=json.loads((R/name).read_text(encoding='utf-8'))
    assert data['status']=='passed' and data['note_sha256']==sha(ROOT/note)
    assert data['source_sha256']==sha(ROOT/'src'/source)
    for p,h in data['proof_dependencies'].items():assert sha(ROOT/p)==h
rows=[]
for q,C,M,J0,B,T in ((93,92,2,200,18400,22),(83,82,20,2000,164000,27)):
    eps=F(1,q);lo,hi=DLO-eps,DHI-eps
    assert J0%M==0 and B>=C*J0 and B>=M*C/(1-eps*C)
    assert lo>F(157,100)
    assert F(103,100)*(lo-1)>DHI-1
    assert 157**T>103*B*100**(T-1)
    challenges=0
    for j in range(101):
        for extra in (F(-1,1000000),F(0),F(1,1000000)):
            y=F(B+j*M*C)+extra
            if y<B:continue
            J=M*(y/(M*C)).__floor__()
            assert J>=J0 and y>=C*J and J>eps*y
            challenges+=1
    Ahi=(DHI/lo)**T;basic=10*Ahi/(lo-1)
    basic_round=F((basic*100).__ceil__(),100)
    middle=Ahi/(lo-1)*(F(2,3)+F(47,1024))
    c=eps*B/(lo-1)
    Q=1+F(133,10)*F(46057,100000)/L2LO+F(133,10)*lograt(basic_round)[1]/L2LO
    large=(F(133,10)*lograt(hi)[1]/L2LO+(Q+F(143,10)*lograt(515620)[1]/L2LO+c)/515620)/(lo-1)
    with localcontext() as ctx:
        ctx.prec=100;delta=D(3).ln()/D(2).ln();lam=delta-D(1)/q;amp=(delta/lam)**T
        def G(y):return delta*y if y<=B else max(lam*y,y+(delta-1)*B)
        count=0
        for y0 in (D(1),D(71),D(B)-1,D(B),D(B)+1,D(10)**40):
            v=y0
            for t in range(201):
                assert v<=amp*y0*lam**t*(1+D('1e-90'))
                if t>=T:assert v>D(103)*B/100
                v=G(v);count+=1
    rows.append({'epsilon':str(eps),'C':C,'J_multiple':M,'J_minimum':J0,'B':B,'warmup':T,
                 'lambda':str(lam),'amplification_A':str(amp),'rounding_challenges':challenges,
                 'virtual_iteration_challenges':count,'cycle_coefficient_upper_rationals':
                 {'basic':compact(basic),'middle':compact(middle),'affine_large':compact(large)},
                 'rounded_cycle_coefficients':{'basic':str(basic_round),'middle':str(F((middle*100).__ceil__(),100)),
                                               'affine_large':str(F((large*100).__ceil__(),100))}})
out={'status':'passed','rows':rows,'source_sha256':sha(Path(__file__)),
     'dependencies':{n:sha(R/n) for n in deps},'proof_dependencies':{n:sha(ROOT/n) for n in notes+['optimized-global-cutoffs.md']},
     'source_dependencies':{n:sha(ROOT/'src'/n) for n in sources+['exact_intervals.py']},
     'scope':'Smaller global cutoffs from already checked local interpolation arguments. Combined finite/analytic capacity requires a separate proof.'}
(R/'optimized-global-cutoffs-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'rows':rows}),flush=True)
