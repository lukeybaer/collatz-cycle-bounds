"""Directed rational checks for the additional cycle-bound corollaries."""
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
import hashlib,json
from exact_intervals import DLO,DHI,L2LO,L2HI

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
EPS=F(1,160);LAMLO=DLO-EPS;LAMHI=DHI-EPS
C=51825000

def log2_interval(x,terms=180):
    """Range-reduced atanh series, with exact positive-tail enclosure."""
    x=F(x);assert x>0
    power=x.numerator.bit_length()-x.denominator.bit_length()
    scale=F(2)**power;u=x/scale
    if u<1:power-=1;u*=2
    elif u>=2:power+=1;u/=2
    assert 1<=u<2
    z=(u-1)/(u+1);z2=z*z;v=z;lower=F(0)
    for j in range(terms):lower+=2*v/(2*j+1);v*=z2
    upper=lower+2*v/((2*terms+1)*(1-z2))
    den=10**80
    lo=F(((power+lower/L2HI)*den).__floor__(),den)
    hi=F(((power+upper/L2LO)*den).__ceil__(),den)
    return lo,hi

ALO=(DLO/LAMHI)**26;AHI=(DHI/LAMLO)**26
COEFHI=AHI/(LAMLO-1)
assert COEFHI<F(383,200)
assert C<2**26 and DHI<F(317,200) and F(317,200)**3<4
middle_coefficient=F(383,200)*(F(2,3)+F(47,1024))
assert middle_coefficient==F(838387,614400)<F(137,100)
clo,chi=log2_interval(C);alo,ahi=log2_interval(DHI)
assert ahi<F(2,3)

def Yhi(m):return 1+chi+2*log2_interval(m)[1]+m*ahi

ratio_base_hi=1-EPS/DHI
R91=COEFHI*Yhi(91)/(F(14784,10000)*91)*ratio_base_hi**91
assert R91<1
R91compact=F((R91*10**80).__ceil__(),10**80)
assert R91<=R91compact<1
assert 2/L2LO <1+clo+2*log2_interval(91)[0]
assert ratio_base_hi<F(999,1000)
assert F(1915,100)/F(15108,1000)*F(999,1000)**1024<1
assert 1+F(133,10)*F(46057,100000)/L2LO+F(532,10)<64
assert F(133,10)*F(2,3)+F(143,10)/64+F(64,1024)<10

rows=[]
with localcontext() as ctx:
    ctx.prec=90;ctx.Emin=-999999999
    delta=D(3).ln()/D(2).ln();lam=delta-D(1)/160;A=(delta/lam)**26
    for m in (91,96,99,100,1024,10000,515619,515620):
        y=1+D(C).ln()/D(2).ln()+2*D(m).ln()/D(2).ln()+m*delta.ln()/D(2).ln()
        if m<=515619:
            coefficient=A*y/(lam-1)/m;old_coefficient=D('1.4784')
            rounded=D('1.37') if m>=1024 else None
        else:
            coefficient=10*A/(lam-1);old_coefficient=D('15.109');rounded=D('19.15')
        ratio=coefficient/old_coefficient*(lam/delta)**m
        rows.append({'m':m,'coefficient_for_lambda_power_times_m':str(coefficient),
                     'comparison_coefficient':str(old_coefficient),
                     'ratio_to_published_uniform_upper':str(ratio),
                     'simplified_coefficient':str(rounded) if rounded else None})
result={'status':'passed','middle_range':[1024,515619],'middle_coefficient':'1.37',
        'general_range_minimum':1024,'general_coefficient':'19.15',
        'precise_middle_range':[91,515619],'rational_middle_coefficient_bound':str(middle_coefficient),
        'R91_upper_decimal':str(float(R91compact)),'R91_upper_rational':str(R91compact),
        'numerical_comparisons':rows,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'note_sha256':hashlib.sha256((ROOT/'cycle-bound-corollaries.md').read_bytes()).hexdigest(),
        'scope':'Exact coefficient and endpoint inequalities. Monotonicity, the published cycle-size theorem, and the two-regime proof remain written mathematical inputs. No new numerical exclusion is claimed.'}
(R/'cycle-bound-corollaries-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='R91_upper_rational'}),flush=True)
