"""Finite conservative candidates for c<=48.99. No coefficient is certified by this file.

The separate large-k proof uses A2=2^168, valuation base8, mu6,
C<2000 and cutoff2^19. Exceptions require basin OR block-restart proofs.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,argparse,hashlib
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
X=2**71;S=10**6;DL=1584962;DU=1584963;BL=DL-S;BU=DU-S
def ceildiv(n,d):return -(-n//d)
def run(J):
    assert 42<=J<=49
    assert F(27660,81)*F(168,100)*F(11,10)/F(69,100)**3<2000
    assert 2000*F(153,10)**2+3<2**19
    watch=time.monotonic();B=100;master=1<<(J+B);mask=master-1;inv3=pow(3,-1,master);p=1
    rows=[{'ell':ell,'a_exponent_upper':ceildiv(12*(J-ell),7),'bits':ell+B+1,'minimum_residue':master,'minimum_at_k':None} for ell in range(1,J)]
    for k in range(1,2**19):
        p=p*inv3&mask
        for row in rows:
            r=((1-(1<<row['ell']))*p)&((1<<row['bits'])-1)
            if r<row['minimum_residue']:row['minimum_residue']=r;row['minimum_at_k']=k
    passed=all(r['minimum_residue']>=1<<r['a_exponent_upper'] for r in rows)
    glob={'status':'passed' if passed else 'failed','J':J,'B':B,'k_lower':1,'k_upper_exclusive':2**19,
          'checked_pairs':(J-1)*(2**19-1),'rows':rows,'seconds':time.monotonic()-watch,
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (R/f'high-capacity-J{J}-global.json').write_text(json.dumps(glob,indent=2)+'\n')
    print('Global',J,passed,glob['checked_pairs'],flush=True)
    if not passed:return
    p=1;cases=[];total=0
    for k in range(1,200):
        p=p*inv3&mask;low=max(1,ceildiv(X+2,1<<k))
        for ell in range(1,J):
            q1=ceildiv((100*J-1)*10000+1000-ell*S,BL)
            for s in range(1,B+1):
                q2=ceildiv((100*J-1)*(DU+S)*10000-BL*DL*k+BU*S*s-(ell*S+998000)*S,BL*(DL+S))
                q=min(q1,q2)
                if q<=0 or low>=1<<q:continue
                modulus=1<<(ell+s+1);r=(((1<<(ell+s))+1-(1<<ell))*p)&(modulus-1)
                first=low+((r-low)&(modulus-1));high=(1<<q)-1
                if first>high:continue
                last=high-((high-r)&(modulus-1));count=(last-first)//modulus+1;total+=count
                cases.append({'k':k,'ell':ell,'s':s,'q':q,'first_a':str(first),'last_a':str(last),'step_a':str(modulus),'count':str(count)})
    margin=BL*DL*200-BU*S*B+(S+998000)*S-(100*J-1)*(DU+S)*10000
    assert margin>0 and BL*BL*2**19+(S+998000)*S-(100*J-1)*(DU+S)*10000>0
    data={'status':'exceptions_pending','J':J,'capacity_c':str(F(100*J-1,100)),'B':B,'verified_basin':str(X),
          'small_k_cutoff':200,'small_k_margin_times_1e12':str(margin),'class_count':len(cases),'seed_count':str(total),
          'classes':cases,'global_certificate':f'high-capacity-J{J}-global.json',
          'warning':'Not a capacity certificate. Every class needs a proved basin entry or valid finite block restart.'}
    (R/f'high-capacity-J{J}-classes.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Classes',len(cases),'seeds',total,'seconds',time.monotonic()-watch,flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=49);a=p.parse_args();run(a.J)
