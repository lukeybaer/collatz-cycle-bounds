"""Challenge the normalized-height proof with exact constants and sample orbits.

The written all-parameter proof and Bugeaud's theorem remain dependencies.
Finite numerical samples are not a replacement for either.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from pathlib import Path
import hashlib, itertools, json
from exact_intervals import L2LO,L2HI,log_interval,DLO,DHI

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
EPS=F(1,5000);B=2**18;C=3603
L3LO,L3HI=log_interval(3)
assert F(69,100)<L2LO<L2HI<F(7,10)
assert 1<L3LO<L3HI<F(11,10)
coef=F(24)*F(668,10)/81*F(11,10)/F(69,100)**3*F(51,50)
assert coef<68
assert F(25,69)*3600+F(1,2)<F(3,8)*3600
assert F(3,8)*F(21,10)==F(63,80)
assert F(63,80)-1+F(64,100)==F(171,400)<F(43,100)
assert 3600<2**12
assert 12*F(7,10)+F(43,100)==F(883,100)
assert 68*F(883,100)**2+F(3,50)==F(13254863,2500)<5400
assert 3**12>2**19
assert 3600*F(1,24)==150>3
assert B>50*C
assert EPS*C<F(98,125)
assert DHI<F(5,3)
assert DLO-EPS>F(3,2)
assert DLO-1>2*EPS
assert 3**33>2**52

valuation_challenges=0;iteration_challenges=0;restart_challenges=0;orbit_challenges=0
with localcontext() as context:
    context.prec=100;context.Emax=999999999;context.Emin=-999999999
    ln2=D(2).ln();delta=D(3).ln()/ln2;epsilon=D(1)/5000;lam=delta-epsilon
    amp=(delta/lam)**33
    def G(y):return delta*y if y<=B else max(lam*y,y+(delta-1)*B)
    def height(n):
        # A 250-bit leading mantissa suffices for this numerical challenge.
        exponent=n.bit_length()-1;shift=max(0,exponent-249)
        if n & (n-1) == 0:return D(exponent)
        return D(n>>shift).ln()/ln2+shift
    for J in (50,51,73,100,1000,10**6,10**30):
        for t in (3600,3601,4096,10**4,10**6,10**12,10**100,10**1000):
            tj=D(t);jd=D(J)
            bp=tj*jd/((4*jd+4)*ln2)+1/(2*D(3).ln())
            assert bp<D(3)/8*tj
            H=max(bp.ln()+(3*ln2).ln()+D('.64'),12*ln2)
            coeff=D(24)*D('66.8')/81*D(3).ln()/ln2**3*(jd+1)
            theorem_upper=coeff*H**2+3
            conservative=D(68)*jd*max(tj.ln()+D('.43'),D('8.4'))**2+3
            assert theorem_upper<conservative<D('1.5')*tj*jd
            assert D('1.5')*(tj.ln()+D('.43')-2)+6/(jd*tj)>0
            valuation_challenges+=1
    starts=[D(1),D(71),D(B)-1,D(B),D(B)+1,D(2*B),D(10)**20,D(10)**200]
    for y0 in starts:
        v=y0
        for t in range(351):
            assert v<=amp*y0*lam**t*(1+D('1e-90'))
            if t>=33:assert v>=2*B
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
    # Exact integer Collatz transitions at very large starting heights.
    # These test both local alternatives, without using the published basin.
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
        if y1<=lam*y:
            branch_counts['one']+=1
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

result={'status':'passed','coefficient_rational_upper':str(coef),
        'cutoff_comparison_margin':str(F(5400)-68*F(883,100)**2-F(3,50)),
        'valuation_parameter_challenges':valuation_challenges,'virtual_iteration_challenges':iteration_challenges,
        'abstract_restart_checks':restart_challenges,'large_integer_orbit_challenges':orbit_challenges,
        'observed_local_branches':branch_counts,'numeric':numeric,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'note_sha256':hashlib.sha256((ROOT/'normalized-height-exponential-bound.md').read_bytes()).hexdigest(),
        'formal_receipt_sha256':hashlib.sha256((ROOT/'formal'/'formal-verification.json').read_bytes()).hexdigest(),
        'scope':'Exact constant checks and finite challenges. The all-parameter analytic result depends on the written proof and cited theorems; external review and priority are pending.'}
(R/'normalized-height-exponential-bound-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
