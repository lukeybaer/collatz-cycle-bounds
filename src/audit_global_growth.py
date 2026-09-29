"""Exact constants and high-precision challenges for the global analytic note.

Finite checks supplement the written proof; no computation here proves an
all-parameter asymptotic statement or the external p-adic theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import itertools,json,hashlib
from exact_intervals import DLO,DHI
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
eps=F(3,10**6)
assert F(1584962,10**6)<DLO<DHI<F(317,200)
assert F(1584962,10**6)-eps>F(3,2)
assert 3**64>2**99
assert F(317,200)**3<4
assert eps>F(2,10**6)*F(317,200)*F(2,3)
assert 1+F(133,10)*F(46057,100000)/F(69,100)+F(266,5)<64
assert F(133,10)*F(2,3)+F(143,10*64)+F(64,1024)<10
assert F(1,1024)*F(100,69)<F(1,64)
samples=[];iteration_checks=0;restart_checks=0
with localcontext() as ctx:
    ctx.prec=100;ctx.Emax=999999999;ctx.Emin=-999999999
    ln2=D(2).ln();delta=D(3).ln()/ln2;beta=delta-1;a0=delta.ln()/ln2
    epsilon=D(3)/D(10**6);B=D(2**34);eta=epsilon/(delta*a0)
    def loss(y):return epsilon*y/(y.ln()/ln2+802)
    def phi(y):return delta*y-loss(y)
    def growth(y):return delta*y if y<=B else max(phi(y),y+beta*B)
    starts=[D(1),D(71),B-D(1),B,B+D(1),B+D(2),B+D(3),2*B,D(2)**100,D(2)**1000]
    for start in starts:
        z=start.ln()/ln2+802+64*a0;y=start
        for t in range(1,351):
            previous=y;y=growth(y)
            assert D('1.5')*previous<=y<=delta*previous
            if t>=64:
                assert y>=2*B
                upper=start*delta**t*(z/(z+a0*(t-64)))**eta
                assert y<=upper*(1+D('1e-95'))
                iteration_checks+=1
        samples.append({'initial_log2_height':str(start.ln()/ln2),
                        'iterations':350,'ratio_to_delta_power':str(y/(start*delta**350))})
    # Exhaust all one/two-block restart schedules of eight blocks.
    # Intermediate points take their maximal elementary bound; endpoints
    # take the smaller restart bound. This directly challenges the lemma.
    for start in (D(1),B-D(1),B+D(1),2*B):
        iterates=[start]
        for t in range(16):iterates.append(growth(iterates[-1]))
        for schedule in itertools.product((1,2),repeat=8):
            time=0;y=start
            for length in schedule:
                if length==2:
                    intermediate=delta*y
                    assert intermediate<=delta*iterates[time]*(1+D('1e-95'))
                    restart_checks+=1
                for _ in range(length):y=growth(y)
                time+=length
                assert y<=delta*iterates[time-1]*(1+D('1e-95'))
                restart_checks+=1
    ratios=[]
    for exponent in (6,1000,100000,500000,1000000,10000000):
        logm=D(exponent)*D(10).ln()
        z=(D(10).ln()+logm)/ln2+802+64*a0
        # Normalized second term in (7). The first is positive and omitted
        # here only to illustrate the asymptotic scale, not as an upper bound.
        ratio=D(10)/beta*(eta*((4*z/a0).ln()-logm)).exp()
        ratios.append({'log10_m':exponent,'second_term_divided_by_m_delta_power':str(ratio)})
    exponent_value=str(eta)
result={'status':'passed','scope':'Exact constants and finite numerical challenges; the all-parameter claim rests on the written proof.',
        'iteration_checks':iteration_checks,'bounded_restart_checks':restart_checks,
        'saving_exponent_approximate':exponent_value,'iteration_samples':samples,
        'asymptotic_second_term_examples':ratios,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_dependencies':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
          ('global-growth-and-cycle-bound.md','logarithmic-run-loss.md','sharpened-logarithmic-run-loss.md','actual-height-growth-corollary.md')},
        'prior_arithmetic_audit_sha256':hashlib.sha256((R/'sharpened-logarithmic-run-loss-audit.json').read_bytes()).hexdigest()}
(R/'global-growth-and-cycle-bound-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('iteration_samples','asymptotic_second_term_examples')}),flush=True)
