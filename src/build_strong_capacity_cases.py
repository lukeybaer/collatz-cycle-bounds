"""Finite residue checks for the proposed Bugeaud-based capacity bound.

Output remains CONDITIONAL until all listed exceptional seeds are proved to
reach the verified basin. The finite range reduction is documented separately.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,time,hashlib
from exact_intervals import DLO,DHI

ROOT=Path(__file__).resolve().parents[1]
DL=F(1584962,10**6);DU=F(1584963,10**6);BL=DL-1;BU=DU-1
EPS=F(1,1000);EVEN=1-EPS;X=2**71;K_CUTOFF=2**18
assert DL<DLO<DHI<DU
assert F(27660,81)*F(11,10)/F(69,100)**3<1200
assert 1200*F(73,5)**2+3<K_CUTOFF

def run(J,B):
    assert 2<=J<=30
    watch=time.monotonic();c=F(J)-F(1,100)
    master_bits=J+B;mask=(1<<master_bits)-1;inv3=pow(3,-1,1<<master_bits)
    specs=[{'ell':ell,'a_exponent_upper':F(12*(J-ell),7).__ceil__(),
            'bits':ell+B+1,'minimum_residue':None,'minimum_at_k':None} for ell in range(1,J)]
    p=1;count=0
    # Transpose the enumeration: bound k first, then solve for a in each
    # residue class. This checks whole intervals of small odd parts at once.
    for k in range(1,K_CUTOFF):
        p=(p*inv3)&mask
        for row in specs:
            ell=row['ell'];r=((1-(1<<ell))*p)&((1<<row['bits'])-1)
            if row['minimum_residue'] is None or r<row['minimum_residue']:
                row['minimum_residue']=r;row['minimum_at_k']=k
            count+=1
    global_pass=all(row['minimum_residue']>=1<<row['a_exponent_upper'] for row in specs)
    global_cert={'status':'passed' if global_pass else 'failed','J':J,'B':B,
                 'k_lower':1,'k_upper_exclusive':K_CUTOFF,'checked_pairs':count,'rows':specs,
                 'seconds':time.monotonic()-watch,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'results'/f'strong-capacity-J{J}-global.json').write_text(json.dumps(global_cert,indent=2)+'\n')
    print('Global next-run bound:',global_pass,'pairs',count,'seconds',round(time.monotonic()-watch,3),flush=True)
    if not global_pass:return
    small_k_cutoff=200
    margin=BL*DL*small_k_cutoff-BU*B+1+EVEN-EPS-c*(DU+1)
    assert margin>0
    large_margin=BL*(DL-1)*K_CUTOFF+1+EVEN-EPS-c*(DU+1)
    assert large_margin>0
    cases=[];total=0;p=1
    for k in range(1,small_k_cutoff):
        p=(p*inv3)&mask
        low=max(1,(X+2+(1<<k)-1)//(1<<k))
        for ell in range(1,J):
            q1=((c-ell+EPS)/BL).__ceil__()
            for s in range(1,B+1):
                # The negative s term uses the UPPER beta bound. Using BL
                # on the combined (DL*k-s) would be unsafe when it is negative.
                q2=((c*(DU+1)-BL*DL*k+BU*s-ell-EVEN+EPS)/(BL*(DL+1))).__ceil__()
                q=min(q1,q2)
                if q<=0:continue
                high=(1<<q)-1
                if low>high:continue
                modulus=1<<(ell+s+1)
                residue=(((1<<(ell+s))+1-(1<<ell))*p)&(modulus-1)
                first=low+((residue-low)&(modulus-1))
                if first>high:continue
                last=high-((high-residue)&(modulus-1))
                number=(last-first)//modulus+1;total+=number
                cases.append({'k':k,'ell':ell,'s':s,'q':q,'first_a':str(first),
                              'last_a':str(last),'step_a':str(modulus),'count':str(number)})
    out={'status':'convergence_checks_pending','J':J,'capacity_c':str(c),'B':B,
         'verified_basin':str(X),'small_k_cutoff':small_k_cutoff,
         'small_k_margin':str(margin),'large_k_margin':str(large_margin),
         'global_certificate':f'strong-capacity-J{J}-global.json',
         'class_count':len(cases),'seed_count':str(total),'classes':cases,
         'source_sha256':global_cert['source_sha256'],
         'warning':'No stronger capacity is certified until every exceptional seed converges and coverage is independently audited.'}
    (ROOT/'results'/f'strong-capacity-J{J}-classes.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Exceptional classes',len(cases),'seeds',total,'seconds',round(time.monotonic()-watch,3),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--J',type=int,default=30);parser.add_argument('--B',type=int,default=90)
    args=parser.parse_args();run(args.J,args.B)
