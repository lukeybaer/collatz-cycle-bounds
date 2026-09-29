"""Independent exact constants for the two-regime interpolation argument.

All-parameter reasoning is in the manuscript. Finite numerical challenges
are supplementary, not proofs of a universal theorem.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from pathlib import Path
import hashlib, itertools, json
from exact_intervals import L2LO,L2HI,log_interval,DLO,DHI

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
EPS=F(1,160);B=2**14;C=127
L3LO,L3HI=log_interval(3);L5LO,L5HI=log_interval(5)
L11LO,L11HI=log_interval(11)
L23LO,L23HI=log_interval(23,terms=600)
L7LO,L7HI=log_interval(7)
assert F(693,1000)<L2LO<L2HI<F(1733,2500)
assert L3HI<F(1099,1000)
assert 3*L2HI+L3HI+L11HI<F(697,125) # ln264
assert L7HI-2*L2LO<F(14,25) # ln(7/4)
assert F(1509,1000)<L23LO-L5HI # ln(23/5)
assert 5*L2HI+2*L5HI<F(67,10) # ln800
assert L11HI<F(12,5)
assert 2*L2HI+2*L5HI<F(47,10) # ln100
assert 4*L2HI+4*L5HI<10 # ln10000
U=F(12,7)*F(101,100)*F(1733,2500)
assert U==F(525099,437500)
small_margin=9*6*F(2079,1000)-9*F(697,125)-F(3,10)-7*(F(709,300)*F(1099,500)+F(3013,1000)*U)
assert small_margin==F(19833889,187500000)>0
assert F(23,5)*F(1031*100+9,18*100-2)<264
assert F(2127,706)<F(3013,1000)
def P(q):
    return (q+1)*((q+1)*F(2079,1000)-F(1733,2500)*q-F(14,25))-F(q,25)-(q+2)*((F(203,600)*q-F(97,600))*F(1099,500)+((F(1,2)-F(350,2127))*q+F(5,2)-F(1400,2127))*U)
Acoef=F(1783170953,7444500000)
Bcoef=-F(454813329,354500000)
Ccoef=-F(1631430293,744450000)
for q in (0,1,2):assert P(q)==Acoef*q*q+Bcoef*q+Ccoef
assert Acoef>0 and P(9)==F(3011630363,531750000)>F(566,100)
assert 18*Acoef+Bcoef==F(1503066483,496300000)>F(302,100)
assert F(3,20)+F(2*9,100)<F(9,25)
assert 189<F(38,25)*125
assert 3*10*11<F(38,25)*256
assert F(19,12)-F(38,25)==F(19,300)
assert F(7,12)*F(19,300)*125==F(665,144)>F(8,3)
assert F(12,7)*F(101,100)<2
assert B>100*C and EPS*C<F(81,100)*F(99,100)
assert DHI<F(8,5) and DLO-EPS>F(3,2) and DLO-1>2*EPS
assert F(81,50)*DHI<DLO+1 and 3**26>2**41

parameter_checks=0;factorial_checks=0;iteration_challenges=0;restart_challenges=0;orbit_challenges=0
margins=[]
with localcontext() as context:
    context.prec=100;context.Emax=999999999;context.Emin=-999999999
    ln2=D(2).ln();ln3=D(3).ln();delta=ln3/ln2
    epsilon=D(1)/160;lam=delta-epsilon;amp=(delta/lam)**26
    def G(y):return delta*y if y<=B else max(lam*y,y+(delta-1)*B)
    def height(n):
        exponent=n.bit_length()-1;shift=max(0,exponent-249)
        if n & (n-1) == 0:return D(exponent)
        return D(n>>shift).ln()/ln2+shift
    for J in (100,101,1000,10**6,10**12,10**50):
        jd=D(J)
        M=9*jd;L=D(7);R0=7*jd+6;S=D(9);N=M*L
        gamma=D('.5')-N/(6*R0*S)
        hp=128*jd+D('.5')
        bupper=D(23)/5*(R0-1+(S-1)*hp)/(2*(M-1))
        assert bupper<264
        assert D(1)/3<gamma<D('.5')
        assert 7*jd<=D(125)/2*jd and 7*jd*9>(M-1)*7
        assert gamma*R0/jd<=D(709)/300
        assert gamma*S<D(3013)/1000
        assert 3*N.ln()/jd<D('.3')
        h2=D(12)/7*(jd+1)*ln2
        margin=(M*(L-1)*3*ln2-3*N.ln()-(M-1)*bupper.ln()-gamma*L*(R0*2*ln3+S*h2))/jd
        assert margin>D(small_margin.numerator)/D(small_margin.denominator)
        margins.append({'range':'small','J':J,'theorem_margin_divided_by_J':str(margin)})
        parameter_checks+=1
        for q in (9,10,11,20,50,100,1000,10**6):
            qd=D(q);M=(qd+1)*jd;L=qd+2
            R2=(qd-1)*jd;R0=R2+qd+1;S=qd+5;N=M*L
            gamma=D('.5')-N/(6*R0*S)
            assert D(1)/3<gamma<D('.5')
            hp=D(2)**q*jd/2+D('.5')
            bupper=5*(R0-1+(S-1)*hp)/(2*(M-1))
            assert bupper<D(7)/4*D(2)**q
            assert gamma*R0/jd<=D(203)/600*qd-D(97)/600
            assert gamma*S<=(D('.5')-D(350)/2127)*qd+D('2.5')-D(1400)/2127
            assert 3*N.ln()/jd<qd/25
            margin=(M*(L-1)*3*ln2-3*N.ln()-(M-1)*bupper.ln()-gamma*L*(R0*2*ln3+S*h2))/jd
            lower=D(P(q).numerator)/D(P(q).denominator)
            assert margin>lower>0
            tlow=D(2)**(q-1)
            assert R2<tlow*jd/2 and R2*S>(M-1)*L
            assert 3*M*L<D(38)/25*tlow*jd
            parameter_checks+=1
            if q<21:margins.append({'range':'large','J':J,'q':q,'theorem_margin_divided_by_J':str(margin),'polynomial_lower':str(lower)})
    for M in (800,801,900,1000,1001,1100,2000,5000):
        logP=sum(D(M-i)*D(i).ln() for i in range(1,M))
        logfactor=-2*logP/(D(M)*(M-1))
        assert logfactor<(D(23)/5).ln()-D(M-1).ln()
        factorial_checks+=1
    starts=[D(1),D(71),D(B)-1,D(B),D(B)+1,D(2*B),D(10)**20,D(10)**200]
    for y0 in starts:
        v=y0
        for t in range(351):
            assert v<=amp*y0*lam**t*(1+D('1e-90'))
            if t>=26:assert v>=2*B
            previous=v;v=G(v)
            assert D('1.5')*previous<=v<=delta*previous
            iteration_challenges+=1
    for y0 in (D(1),D(B)-1,D(B)+1,D(2*B)):
        virtual=[y0]
        for t in range(16):virtual.append(G(virtual[-1]))
        for schedule in itertools.product((1,2),repeat=8):
            t=0;y=y0
            for length in schedule:
                if length==2:
                    assert delta*y<=delta*virtual[t]*(1+D('1e-90'))
                    restart_challenges+=1
                for _ in range(length):y=G(y)
                t+=length
                assert y<=delta*virtual[t-1]*(1+D('1e-90'))
                restart_challenges+=1
    cases=[]
    for a in (1,3,5,17,2**60-1,2**100+1):
        for k in (B,B+1,B+16,2*B+3):cases.append((a,k))
    for bits in (B//2,B,B+1):
        for extra in (1,7,101):cases.append((2**bits+1,max(0,B-bits)+extra))
    branch_counts={'one':0,'two':0}
    for a,k in cases:
        n=(a<<k)-1;peak=a*3**k-1
        ell=(peak&-peak).bit_length()-1;n1=peak>>ell
        s=((n1+1)&-(n1+1)).bit_length()-1
        a1=(n1+1)>>s;peak1=a1*3**s-1
        ell1=(peak1&-peak1).bit_length()-1;n2=peak1>>ell1
        y,y1,y2=height(n+1),height(n1+1),height(n2+1)
        assert y>=B
        if y1<=lam*y:branch_counts['one']+=1
        else:
            assert s<=lam*y and y2<=lam**2*y
            branch_counts['two']+=1
        orbit_challenges+=1
    ratios=[]
    for m in (515620,10**6,10**7):
        relative=(D(10)*amp/(lam-1)/16)*((lam/delta).ln()*m).exp()
        ratios.append({'m':m,'new_upper_divided_by_16_m_delta_power':str(relative)})
    numeric={'lambda':str(lam),'amplification_A':str(amp),'cycle_coefficient':str(D(10)*amp/(lam-1)),
             'comparison_with_coarsened_published_bound':ratios}

result={'status':'passed','theorem':'Bugeaud1999 Theorem1 rational clause(6)',
        'epsilon':'1/160','cutoff_k_over_J':125,'J_minimum':100,'B':B,'C':C,'warmup':26,
        'small_range_margin':str(small_margin),
        'large_range_polynomial_coefficients':[str(Acoef),str(Bcoef),str(Ccoef)],
        'polynomial_at_9':str(P(9)),'polynomial_derivative_at_9':str(18*Acoef+Bcoef),
        'parameter_challenges':parameter_checks,'factorial_product_challenges':factorial_checks,
        'sample_margins':margins,'virtual_iteration_challenges':iteration_challenges,
        'abstract_restart_checks':restart_challenges,'large_integer_orbit_challenges':orbit_challenges,
        'observed_local_branches':branch_counts,'numeric':numeric,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'note_sha256':hashlib.sha256((ROOT/'two-regime-interpolation-bound.md').read_bytes()).hexdigest(),
        'scope':'Exact rational constants plus finite numeric challenges. The all-parameter proof and external transcendence theorem remain written mathematical dependencies.'}
(R/'two-regime-exponential-bound-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='sample_margins'}),flush=True)
