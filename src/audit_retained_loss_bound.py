"""Exact constants for the retained-loss two-stratum interpolation proof."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import hashlib,json
from exact_intervals import DLO,DHI,L2LO,L2HI,log_interval
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
C=F(159,2);EPS=F(1,80);J0=10000;MULT=100;B=1272000;WARMUP=32

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lograt(q):
    q=F(q);power=0
    while q>=2:q/=2;power+=1
    while q<1:q*=2;power-=1
    lo,hi=log_interval(q)
    return (lo+power*(L2LO if power>=0 else L2HI),hi+power*(L2HI if power>=0 else L2LO))
def dec(q):q=F(q);return D(q.numerator)/D(q.denominator)
def ceilrat(q,den=10**50):return F((q*den).__ceil__(),den)

def audit(write=True):
    dl=F(126797,80000);bl=dl-1;ln2lo=F(34657359,50000000);ln2hi=F(69314719,100000000)
    ln3hi=F(109861229,100000000);fact=F(4483,1000)
    assert dl<DLO and ln2lo<L2LO<L2HI<ln2hi and lograt(3)[1]<ln3hi
    assert lograt(60000)[1]<12 and F(7501,5000)<lograt(fact)[0]
    assert lograt(423500)[1]<13
    assert C-F(12,7)*F(J0+1,J0)>77
    assert F(12,7)*(F(9,10)*J0+1)>F(9,10)*J0+1+3*DHI
    # (D/J lower, D/J upper, x, r, S, k/J upper).
    specifications=[
      ('0','9/10','6.02','3.01',10,'102.41'),
      ('0','9/10','7.84','3.92',10,'256'),
      ('9/10','1','6.10','3.39',9,'79.95'),
      ('9/10','1','6.13','3.41',9,'80.92'),
      ('9/10','1','6.21','3.45',9,'86.03'),
      ('9/10','1','6.62','3.68',9,'109.43'),
      ('9/10','1','8.47','4.24',10,'256')]
    rows=[];lower_by_stratum={F(0):C,F(9,10):C}
    for amin,amax,x,r,S,T in specifications:
        amin,amax,x,r,T=map(F,(amin,amax,x,r,T));lower=lower_by_stratum[amin]
        assert (x*MULT).denominator==(r*MULT).denominator==1 and x*J0>=60000
        assert r*S>=5*x and r<F(77,4) and T>lower
        assert 5*x*J0<=423500
        U=F(12,7)*(amax+F(1,J0))*ln2hi
        bound=fact*(r*J0+3+(S-1)*(T*J0+3)/4)/(2*(x*J0-1))
        logb=ceilrat(lograt(bound)[1],100000)
        gr=r/2+F(2,J0)-5*x/(6*S);gs=F(S,2)-5*x/(6*(r+F(4,J0)))
        margin=16*x*ln2lo-x*logb-F(39,10000)-5*(gr*4*ln3hi+gs*U)
        gap=dl*lower-20*x;loss=amin+bl*gap
        assert margin>0 and gap>1 and loss>F(16,5),(amin,T,float(margin),float(loss))
        rows.append(dict(D_lower=str(amin),D_upper=str(amax),lower_height=str(lower),T=str(T),
          x=str(x),r=str(r),S=S,height_coefficient=str(U),log_b_upper=str(logb),
          interpolation_margin_lower=str(margin),gap_lower=str(gap),retained_loss_lower=str(loss)))
        lower_by_stratum[amin]=T
    assert all(t==256 for t in lower_by_stratum.values())
    assert (F(19,12)-1)*(F(19,12)-F(38,25))*256>F(16,5)
    assert EPS*C<1 and B>=C*J0 and B>=MULT*C/(1-EPS*C)
    lamlo,lamhi=DLO-EPS,DHI-EPS
    assert lamlo>F(157,100) and F(103,100)*(lamlo-1)>DHI-1
    assert 157**WARMUP>103*B*100**(WARMUP-1)
    assert DHI<F(8,5) and 2*DHI*EPS-EPS**2<F(16,5)*EPS
    Ahi=(DHI/lamlo)**WARMUP
    basic=10*Ahi/(lamlo-1);middle=Ahi/(lamlo-1)*(F(2,3)+F(47,1024))
    basic_round=ceilrat(basic,100);middle_round=ceilrat(middle,100)
    Q=1+F(133,10)*F(46057,100000)/L2LO+F(133,10)*lograt(basic_round)[1]/L2LO
    c=EPS*B/(lamlo-1)
    large=(F(133,10)*lograt(lamhi)[1]/L2LO+(Q+F(143,10)*lograt(515620)[1]/L2LO+c)/515620)/(lamlo-1)
    parameters=virtual=rounding=orbits=0
    with localcontext() as ctx:
        ctx.prec=100;delta=D(3).ln()/D(2).ln();beta=delta-1;lam=delta-dec(EPS);amp=(delta/lam)**WARMUP
        for row in rows:
            x,r,T=map(F,(row['x'],row['r'],row['T']));S=row['S'];amax=F(row['D_upper'])
            for j in (J0,J0+MULT,2*J0,10**8,10**20):
                M=dec(x)*j;RR=dec(r)*j+4;N=5*M;g=D('.5')-N/(6*RR*S)
                h2=dec(F(12,7))*(dec(amax)*j+1)*D(2).ln()
                b=dec(fact)*(RR-1+(S-1)*(dec(T)*j+3)/4)/(2*(M-1))
                v=(16*M*D(2).ln()-3*N.ln()-(M-1)*b.ln()-5*g*(RR*4*D(3).ln()+S*h2))/j
                assert v>dec(F(row['interpolation_margin_lower']));parameters+=1
        def G(y):return delta*y if y<=B else max(lam*y,y+beta*B)
        for start in (D(1),D(71),D(1000),D(B)-D('.1'),D(B),D(B)+D('.1'),D(10**9)):
            y=start
            for t in range(180):
                assert y<=amp*start*lam**t*(1+D('1e-90'))
                y=G(y);virtual+=1
        for q in (0,1,10,100,10000):
            for offset in (F(-1,1000000),F(0),F(1,1000000)):
                y=F(B)+q*MULT*C+offset
                if y<B:continue
                j=MULT*(y/(MULT*C)).__floor__()
                assert j>=J0 and C*j<=y and j>EPS*y;rounding+=1
        # Long exact integer blocks from both strata; no stochastic sampling.
        for k in (800000,1100000,2600000):
          for q in (0,8000,16000):
            a=1 if q==0 else (1<<q)+1;n=(a<<k)-1
            y=D(n+1).ln()/D(2).ln();peak=a*3**k-1
            ell=(peak&-peak).bit_length()-1;n1=peak>>ell
            kp=((n1+1)&-(n1+1)).bit_length()-1
            a1=(n1+1)>>kp;peak1=a1*3**kp-1;ell1=(peak1&-peak1).bit_length()-1;n2=peak1>>ell1
            yp=D(n1+1).ln()/D(2).ln();ypp=D(n2+1).ln()/D(2).ln()
            loss=D(ell)+beta*(D(a).ln()/D(2).ln())-1
            j=MULT*int(y/dec(MULT*C))
            assert yp<=delta*y-loss+D('1e-85')
            assert ypp<=delta*y-loss+beta*kp+D('1e-85')
            if loss>=j:assert yp<=delta*y-j+D('1e-85')
            else:assert kp<=delta*y-j and ypp<=delta**2*y-D('3.2')*j+D('1e-85')
            orbits+=1
        numeric={'lambda':str(lam),'amplification':str(amp)}
    notes=['retained-loss-interpolation-bound.md','four-range-interpolation-bound.md',
           'fourth-power-interpolation-bound.md','two-regime-interpolation-bound.md',
           'optimized-global-cutoffs.md','cycle-bound-corollaries.md']
    dependencies=['four-range-exponential-bound-audit.json','two-regime-exponential-bound-audit.json',
                  'interpolation-primary-source-provenance.json']
    out={'status':'passed','epsilon':str(EPS),'C':str(C),'J0':J0,'multiple':MULT,'B':B,'warmup':WARMUP,
         'rows':rows,'cycle_coefficients_upper':{'basic':str(basic_round),'middle':str(middle_round),'large':str(ceilrat(large,100))},
         'parameter_challenges':parameters,'rounding_challenges':rounding,'virtual_challenges':virtual,'exact_integer_orbit_challenges':orbits,
         'numeric':numeric,'source_sha256':sha(Path(__file__)),
         'source_dependencies':{'exact_intervals.py':sha(ROOT/'src/exact_intervals.py')},
         'proof_dependencies':{p:sha(ROOT/p) for p in notes},'dependencies':{p:sha(R/p) for p in dependencies},
         'scope':'Exact constants plus finite challenges for the written universal retained-loss proof; not a proof of convergence or a priority claim.'}
    if write:
        (R/'retained-loss-exponential-bound-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
        print('PASSED retained-loss epsilon 1/80:',numeric,out['cycle_coefficients_upper'],flush=True)
    return out
if __name__=='__main__':audit()
