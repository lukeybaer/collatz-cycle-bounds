"""Exact arithmetic for a four-range Bugeaud interpolation specialization.

The universal inequalities are proved in four-range-interpolation-bound.md.
Finite high-precision challenges supplement, rather than replace, that proof.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import hashlib,json,itertools
from exact_intervals import log_interval,L2LO,L2HI,DLO,DHI
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
EPS=F(1,83);B=2**18;C=82;J0=2000;MULT=20

def lograt(q):
    q=F(q);power=0
    while q>=2:q/=2;power+=1
    while q<1:q*=2;power-=1
    lo,hi=log_interval(q)
    if power>=0:return lo+power*L2LO,hi+power*L2HI
    return lo+power*L2HI,hi+power*L2LO

assert DLO>F(158496,100000) and DHI<F(8,5)
assert F(3003,2000)<lograt(F(449,100))[0]
assert lograt(6000)[1]<F(87,10)
assert lograt(84000)[1]<12
assert DLO-EPS>F(3,2) and DLO-1>2*EPS
assert B>2000*C and F(82,83)<F(99,100)
assert 3**33>2**52
U=F(12,7)*F(2001,2000)*F(1733,2500)
assert F(82)-F(12,7)*F(2001,2000)>80
assert F(12,7)*(J0+1)>J0+3*DHI
choices=[(F(31,5),F(69,20),9,83,F(4117,1000)),
         (F(63,10),F(7,2),9,89,F(417,100)),
         (F(67,10),F(67,20),10,110,F(554,125)),
         (F(42,5),F(21,5),10,256,F(1261,250))]
rows=[]
for index,(x,r,S,T,logb) in enumerate(choices):
    assert (x*MULT).denominator==(r*MULT).denominator==1
    assert x*J0>=6000 and r*S>=5*x and r<20
    b=F(449,100)*(r*J0+3+(S-1)*F(T*J0+3,4))/(2*(x*J0-1))
    assert lograt(b)[1]<logb
    gr=r/2+F(1,1000)-5*x/(6*S)
    gs=F(S,2)-5*x/(6*(r+F(1,500)))
    assert 0<gr and 0<gs
    margin=x*4*F(2772,1000)-x*logb-F(18,1000)-5*(gr*F(1099,250)+gs*U)
    assert margin>0
    lower_height=82 if index==0 else choices[index-1][3]
    gap=F(158496,100000)*lower_height-20*x
    loss=F(58496,100000)*gap
    assert gap>1 and loss>F(16,5)
    rows.append({'x':str(x),'r':str(r),'S':S,'T':T,'valuation_bound_over_J':str(20*x),
                 'b_at_J2000':str(b),'log_b_upper':str(logb),
                 'gamma_R_over_J_upper':str(gr),'gamma_S_upper':str(gs),
                 'interpolation_margin_over_J_lower':str(margin),
                 'local_gap_over_J_lower':str(gap),'two_block_loss_over_J_lower':str(loss)})

# Directed exact cycle coefficients, with the same published inputs as the
# preceding fourth-power argument. Upward rounding keeps receipts compact.
lamlo=DLO-EPS;lamhi=DHI-EPS
Ahi=(DHI/lamlo)**33
basic=10*Ahi/(lamlo-1);middle=Ahi/(lamlo-1)*(F(2,3)+F(47,1024))
assert basic<F(2246,100) and middle<F(160,100)
assert 1+F(133,10)*F(46057,100000)/L2LO+F(532,10)<64
assert F(133,10)*F(2,3)+F(143,10)/64+F(64,1024)<10
assert F(317,200)**3<4
c_hi=EPS*B/(lamlo-1)
Q_hi=1+F(133,10)*F(46057,100000)/L2LO+F(133,10)*lograt(F(2246,100))[1]/L2LO
cycle=(F(133,10)*lograt(lamhi)[1]/L2LO+(Q_hi+F(143,10)*lograt(515620)[1]/L2LO+c_hi)/515620)/(lamlo-1)
assert cycle<F(1519,100)
DEN=10**60
compact={name:str(F((v*DEN).__ceil__(),DEN)) for name,v in
         [('basic',basic),('middle',middle),('affine_large',cycle)]}

parameter_checks=factorial_checks=virtual_checks=orbit_checks=0
sample_margins=[]
def dec(q):q=F(q);return D(q.numerator)/D(q.denominator)
def height(integer):return D(integer).ln()/D(2).ln()
with localcontext() as context:
    context.prec=110
    delta=D(3).ln()/D(2).ln();beta=delta-1;lam=delta-dec(EPS);amp=(delta/lam)**33
    def G(y):return delta*y if y<=B else max(lam*y,y+beta*B)
    for J in (2000,2020,4000,1000000,10**20):
      for row,(x,r,S,T,logb) in zip(rows,choices):
        M=dec(x)*J;RR=dec(r)*J+4;N=5*M
        gamma=D('.5')-N/(6*RR*S)
        assert D(0)<gamma<D('.5')
        b=D('4.49')*(RR-1+(S-1)*(D(T)*J+3)/4)/(2*(M-1))
        h2=dec(F(12,7))*(J+1)*D(2).ln()
        margin=(M*4*4*D(2).ln()-3*N.ln()-(M-1)*b.ln()-gamma*5*(RR*4*D(3).ln()+S*h2))/J
        assert margin>dec(row['interpolation_margin_over_J_lower'])>0
        assert 3*N.ln()/J<D('.018')
        # At the endpoint these are exact equalities; compare them rationally
        # so a Decimal rounding unit cannot turn equality into a false failure.
        exact_gr=r/2+F(2,J)-5*x/(6*S)
        exact_gs=F(S,2)-5*x/(6*(r+F(4,J)))
        assert exact_gr<=F(row['gamma_R_over_J_upper'])
        assert exact_gs<=F(row['gamma_S_upper'])
        assert abs(gamma*RR/J-dec(exact_gr))<D('1e-100')
        assert abs(gamma*S-dec(exact_gs))<D('1e-100')
        parameter_checks+=1
        if J==2000:sample_margins.append(str(margin))
    for M in (6000,6200,12400,12600,13400,16800):
        logP=sum(D(M-i)*D(i).ln() for i in range(1,M))
        assert -2*logP/(D(M)*(M-1))<D('4.49').ln()-D(M-1).ln()
        factorial_checks+=1
    for y0 in (D(1),D(71),D(B)-1,D(B),D(B)+1,D(2*B),D(10)**30,D(10)**200):
        v=y0;c=dec(EPS)*B/(lam-1)
        for t in range(351):
            assert v<=amp*y0*lam**t*(1+D('1e-90'))
            assert v<=((y0+c)*lam**t-c)*(1+D('1e-90'))
            if t>=33:assert v>=2*B
            v=G(v);virtual_checks+=1
    cases=[(a,k) for a in (1,3,17,2**80+1) for k in (B,B+1,B+20)]
    branches={'one':0,'two':0}
    for a,k in cases:
        n=(a<<k)-1;peak=a*3**k-1;ell=(peak&-peak).bit_length()-1;n1=peak>>ell
        kk=((n1+1)&-(n1+1)).bit_length()-1;a1=(n1+1)>>kk
        peak1=a1*3**kk-1;ell1=(peak1&-peak1).bit_length()-1;n2=peak1>>ell1
        y,y1,y2=height(n+1),height(n1+1),height(n2+1)
        if y1<=lam*y:branches['one']+=1
        else:
            assert kk<=lam*y and y2<=lam**2*y;branches['two']+=1
        orbit_checks+=1
    numeric={'lambda':str(lam),'amplification_A':str(amp),'basic_cycle_coefficient':str(10*amp/(lam-1)),
             'middle_cycle_coefficient':str(amp/(lam-1)*(D(2)/3+D(47)/1024)),
             'affine_constant_c':str(dec(EPS)*B/(lam-1))}
out={'status':'passed','epsilon':'1/83','B':B,'C':C,'J_minimum':J0,'J_multiple':MULT,'warmup':33,
     'rows':rows,'cycle_coefficient_upper_rationals':compact,'parameter_challenges':parameter_checks,
     'factorial_product_challenges':factorial_checks,'virtual_iteration_challenges':virtual_checks,
     'large_integer_orbit_challenges':orbit_checks,'observed_branches':branches,
     'actual_J2000_sample_margins':sample_margins,'numeric':numeric,
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'note_sha256':hashlib.sha256((ROOT/'four-range-interpolation-bound.md').read_bytes()).hexdigest(),
     'proof_dependencies':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                           ('fourth-power-interpolation-bound.md','two-regime-interpolation-bound.md','cycle-bound-corollaries.md')},
     'scope':'Exact constants and supplementary finite challenges. Universal proof, Bugeaud1999, and published cycle bounds are written dependencies. No convergence proof or priority confirmation.'}
(R/'four-range-exponential-bound-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ('rows','proof_dependencies')}),flush=True)
