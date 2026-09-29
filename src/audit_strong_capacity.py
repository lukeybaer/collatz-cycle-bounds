"""Independent finite coverage and trajectory audit for the strong capacity.

No producer imports. Integer inequalities use a common denominator; modular
inverses in the global sweep use division with a chosen multiple of 2^t.
Optional full Python trajectories provide a third, separate implementation.
"""
from pathlib import Path
import argparse,json,hashlib,time

ROOT=Path(__file__).resolve().parents[1];RESULTS=ROOT/'results'
S=10**6;DL=1584962;DU=1584963;BL=DL-S;BU=DU-S;X=2**71
def read(name):return json.loads((RESULTS/name).read_text(encoding='utf-8-sig'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def sufficient(q,k,ell,s,J):
    one=ell*S+BL*q-1000-(100*J-1)*10000
    pair=BL*DL*k-BU*S*s+BL*(DL+S)*q+(ell*S+998000)*S-(100*J-1)*(DU+S)*10000
    return one>=0 or pair>=0
def main(J,trajectories):
    start=time.monotonic();glob=read(f'strong-capacity-J{J}-global.json');data=read(f'strong-capacity-J{J}-classes.json')
    B=data['B'];assert B==glob['B']==90 and data['small_k_cutoff']==200
    assert 2<=J<=30 and data['capacity_c']==str(__import__('fractions').Fraction(100*J-1,100))
    assert int(data['verified_basin'])==X and glob['k_lower']==1 and glob['k_upper_exclusive']==2**18
    pairs=0;rows=[]
    for ell in range(1,J):
        modulus=1<<(ell+B+1);residue=(1-(1<<ell))%modulus
        least=modulus;where=None
        for k in range(1,2**18):
            # Solve 3*r_new=r_old+t*modulus with t in {0,1,2}.
            t=0 if residue%3==0 else (1 if (residue+modulus)%3==0 else 2)
            residue=(residue+t*modulus)//3
            assert 0<=residue<modulus
            if residue<least:least=residue;where=k
            pairs+=1
        q0=(12*(J-ell)+6)//7
        assert q0<=50 and least>=1<<q0 and ell+B+1>q0
        assert BL*q0>=(J-ell)*S
        row=glob['rows'][ell-1]
        assert row=={'ell':ell,'a_exponent_upper':q0,'bits':ell+B+1,'minimum_residue':least,'minimum_at_k':where}
        assert (pow(3,where,modulus)*least+(1<<ell)-1)%modulus==0
        rows.append(row)
    assert pairs==glob['checked_pairs'] and glob['status']=='passed'
    print('Independent global coverage:',pairs,'pairs;',round(time.monotonic()-start,2),'seconds',flush=True)
    # Check the uniform middle and large k margins, using integer bounds.
    assert sufficient(0,200,1,B,J)
    assert BL*BL*2**18+(S+998000)*S-(100*J-1)*(DU+S)*10000>0
    expected=[];total=0
    for k in range(1,200):
        lower=max(1,-(-(X+2)//(1<<k)))
        for ell in range(1,J):
            q0=(12*(J-ell)+6)//7
            for s in range(1,B+1):
                lo=0;hi=q0
                assert sufficient(hi,k,ell,s,J)
                while lo<hi:
                    mid=(lo+hi)//2
                    if sufficient(mid,k,ell,s,J):hi=mid
                    else:lo=mid+1
                q=lo
                if q==0 or lower>=1<<q:continue
                modulus=1<<(ell+s+1)
                inverse=pow(pow(3,k,modulus),-1,modulus)
                residue=((1<<(ell+s))+1-(1<<ell))*inverse%modulus
                first=residue+-(-(lower-residue)//modulus)*modulus
                last=residue+(((1<<q)-1-residue)//modulus)*modulus
                if first>last:continue
                count=(last-first)//modulus+1;total+=count
                row={'k':k,'ell':ell,'s':s,'q':q,'first_a':str(first),'last_a':str(last),'step_a':str(modulus),'count':str(count)}
                expected.append(row)
                for a in {first,last}:
                    assert a&1 and X<(a<<k)-1 and a<1<<q
                    peak=a*3**k-1
                    assert (peak&-peak).bit_length()-1==ell
                    next_min=peak>>ell
                    assert ((next_min+1)&-(next_min+1)).bit_length()-1==s
    assert expected==data['classes'] and total==int(data['seed_count']) and len(expected)==data['class_count']
    print('Independent exceptional coverage:',len(expected),'classes;',total,'seeds',flush=True)
    # Verify complete C# receipts, launch hashes and equality of every digest.
    labels=[f'strong-capacity-J{J}-basin-wide',f'strong-capacity-J{J}-basin-reference']
    receipts=[]
    for label in labels:
        meta=read(label+'-metadata.json');got=read(label+'-result.json')
        assert meta['inputHash'].lower()==digest(RESULTS/f'strong-capacity-J{J}-classes.json')
        assert meta['sourceHash'].lower()==digest(ROOT/'src'/'BasinVerifier.cs')
        assert got['status']=='complete' and got['all_enter_verified_basin'] and got['seeds']==total
        assert int(got['verified_basin'])==X and len(got['rows'])==len(expected)
        for i,(row,case) in enumerate(zip(got['rows'],expected)):
            assert row['id']==i and row['status']=='complete' and not row['error']
            assert row['seeds']==int(case['count']) and row['odd_steps']>0
        receipts.append(got)
    for left,right in zip(receipts[0]['rows'],receipts[1]['rows']):
        for key in ('id','status','seeds','odd_steps','max_steps','max_bits','trajectory_digest'):
            assert left[key]==right[key]
    assert receipts[0]['reference_path'] is False and receipts[1]['reference_path'] is True
    assert receipts[1]['bigint_steps']==receipts[1]['odd_steps']
    if trajectories:
        for i,case in enumerate(expected):
            h=hashlib.sha256();count=steps_total=max_steps=max_bits=0
            for a in range(int(case['first_a']),int(case['last_a'])+1,int(case['step_a'])):
                n=seed=(a<<case['k'])-1;steps=0;bits=n.bit_length()
                while n>X:
                    n=3*n+1;bits=max(bits,n.bit_length());steps+=1
                    assert steps<1000000 and bits<=4096
                    n>>=(n&-n).bit_length()-1
                h.update(f'{seed}:{steps}:{n}:{bits}\n'.encode('ascii'))
                count+=1;steps_total+=steps;max_steps=max(max_steps,steps);max_bits=max(max_bits,bits)
            receipt=receipts[0]['rows'][i]
            assert (count,steps_total,max_steps,max_bits,h.hexdigest())==(receipt['seeds'],receipt['odd_steps'],receipt['max_steps'],receipt['max_bits'],receipt['trajectory_digest'])
            if i%200==0:print('Python trajectories',i+1,'/',len(expected),'elapsed',round(time.monotonic()-start,1),flush=True)
    out={'status':'passed','J':J,'capacity_c':data['capacity_c'],'global_pairs':pairs,'classes':len(expected),'seeds':total,
         'two_csharp_paths_agree':True,'all_python_trajectories_verified':trajectories,
         'class_file_sha256':digest(RESULTS/f'strong-capacity-J{J}-classes.json'),
         'source_sha256':digest(Path(__file__)),'seconds':time.monotonic()-start,
         'warning':'Finite coverage and convergence only. The analytic reduction and external verified basin remain explicit proof dependencies.'}
    suffix='-python' if trajectories else ''
    (RESULTS/f'strong-capacity-J{J}-audit{suffix}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=30);p.add_argument('--trajectories',action='store_true');a=p.parse_args();main(a.J,a.trajectories)
