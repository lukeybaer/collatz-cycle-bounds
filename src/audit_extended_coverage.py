"""Independent coverage audit for the extended p-adic reduction."""
from pathlib import Path
from fractions import Fraction as F
import json,time,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
S=10**6;DL=1584962;DU=1584963;BL=DL-S;BU=DU-S
def sufficient(q,k,ell,s,J):
    one=ell*S+BL*q-1000-(100*J-1)*10000
    pair=BL*DL*k-BU*S*s+BL*(DL+S)*q+(ell*S+998000)*S-(100*J-1)*(DU+S)*10000
    return one>=0 or pair>=0
def run(J):
    assert 31<=J<=41
    watch=time.monotonic()
    glob=json.loads((R/f'extended-capacity-J{J}-global.json').read_text());data=json.loads((R/f'extended-capacity-J{J}-classes.json').read_text())
    assert glob['status']=='passed' and glob['k_lower']==1 and glob['k_upper_exclusive']==2**19
    assert data['B']==glob['B']==100 and data['small_k_cutoff']==200
    assert data['capacity_c']==str(F(100*J-1,100)) and int(data['verified_basin'])==X
    assert F(27660,81)*F(140,100)*F(11,10)/F(69,100)**3<1700
    assert 1700*F(153,10)**2+3<2**19
    assert sufficient(0,200,1,100,J)
    pairs=0
    for ell in range(1,J):
        modulus=1<<(ell+101);r=(1-(1<<ell))%modulus;least=modulus;where=None
        for k in range(1,2**19):
            t=0 if r%3==0 else (1 if (r+modulus)%3==0 else 2)
            r=(r+t*modulus)//3
            if r<least:least=r;where=k
            pairs+=1
        q0=(12*(J-ell)+6)//7
        assert q0<=69 and BL*q0>=(J-ell)*S and least>=1<<q0
        assert glob['rows'][ell-1]=={'ell':ell,'a_exponent_upper':q0,'bits':ell+101,'minimum_residue':least,'minimum_at_k':where}
        assert (pow(3,where,modulus)*least+(1<<ell)-1)%modulus==0
    assert pairs==glob['checked_pairs']
    expected=[];total=0
    for k in range(1,200):
        low=max(1,-(-(X+2)//(1<<k)))
        for ell in range(1,J):
            for s in range(1,101):
                left=0;right=(12*(J-ell)+6)//7
                assert sufficient(right,k,ell,s,J)
                while left<right:
                    mid=(left+right)//2
                    if sufficient(mid,k,ell,s,J):right=mid
                    else:left=mid+1
                q=left
                if q==0 or low>=1<<q:continue
                modulus=1<<(ell+s+1)
                r=((1<<(ell+s))+1-(1<<ell))*pow(pow(3,k,modulus),-1,modulus)%modulus
                first=r+-(-(low-r)//modulus)*modulus
                last=r+(((1<<q)-1-r)//modulus)*modulus
                if first>last:continue
                count=(last-first)//modulus+1;total+=count
                expected.append({'k':k,'ell':ell,'s':s,'q':q,'first_a':str(first),'last_a':str(last),'step_a':str(modulus),'count':str(count)})
                for a in {first,last}:
                    assert a&1 and (a<<k)-1>X
                    peak=a*3**k-1
                    assert (peak&-peak).bit_length()-1==ell
                    n=peak>>ell
                    assert ((n+1)&-(n+1)).bit_length()-1==s
    assert expected==data['classes'] and len(expected)==data['class_count'] and total==int(data['seed_count'])
    out={'status':'passed','J':J,'pairs':pairs,'classes':len(expected),'seeds':str(total),
         'input_sha256':hashlib.sha256((R/f'extended-capacity-J{J}-classes.json').read_bytes()).hexdigest(),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.monotonic()-watch,
         'warning':'Coverage only: every exceptional class still needs a basin or block-restart proof.'}
    (R/f'extended-capacity-J{J}-coverage-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=31);a=p.parse_args();run(a.J)
