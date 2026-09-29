"""Independent forward reconstruction of experimental nonlinear profiles.

The proposal's inverse-piece counts only suggest the shape. The verifier
solves the forward total anew and checks every exact edge and cost bound.
No inverse-map producer routine is imported.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
import verify_certificates as v
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def audit(name):
    path=R/name;data=json.loads(path.read_text());assert data['status']=='unproved_map_proposals'
    assert not data['capacity_map_proved'] and data['parameters']['h']==71
    c0=F(data['parameters']['c0']);c1=F(data['parameters']['c1']);d=v.DHI
    assert F(3799,100)<=c0<c1<=F(4799,100)
    assert 71*(v.DLO-1)>c0
    offset=71*(d-1)-c0;shift=c1/(d-1)
    def phi(y):return max(d*y-c1,min(d*y-c0,y+offset))
    initial=v.read('K-lower-bounds-family-J38.json');proved={}
    for row in initial:
        if row['m'] not in {c['m'] for c in data['rows']}:continue
        _,capacity=v.verify_capacity(row['capacity_certificate'])
        bound=v.verify_suffix(row['rows'],row['m'],int(row['minimum']),capacity_c=capacity)
        assert bound==row['K_proved'];proved[row['m']]=bound
    receipts=[]
    for cert in data['rows']:
        m=cert['m'];k=cert['initial_K'];minimum=int(cert['minimum'])
        assert not cert['capacity_map_proved'] and cert['capacity_map_id']==data['map_id']
        assert k<=proved[m] and minimum==cert['minimum_factor']*2**71
        shapes=[]
        for row in cert['rows']:
            assert row['input_K']==k;profile=row['profile']
            if profile['mode']=='minimum_only':
                assert F(row['cost'])==F(m,minimum);shapes.append('minimum_only')
            else:
                assert profile['mode']=='nonlinear_majorization'
                b=F(profile['floor']);assert 71<=b<=v.log2_lower(minimum+1) and k>=m*b
                hints=profile['inverse_pieces_from_largest'];assert len(hints)==m-1
                assert all(h in (0,1,2,3) for h in hints)
                floors=hints.count(0);q=hints.count(2);r=m-floors
                assert 0<=q<r
                geom=v.geom(r-q)
                base=(k-floors*b-offset*q*(q-1)/2-(r-q)*shift-geom*(q*offset-shift))/(q+geom)
                tail=[base+j*offset for j in range(q)]
                tail += [shift+d**j*(base+q*offset-shift) for j in range(r-q)]
                values=[b]*floors+tail
                assert base>=b and (not floors or base<=phi(b))
                assert len(values)==m and sum(values)==k
                assert all(tail[i+1]==phi(tail[i]) for i in range(r-1))
                assert all(values[i]<=values[i+1] for i in range(m-1))
                assert all(values[(i+1)%m]<=phi(values[i]) for i in range(m))
                terms=list(map(F,profile['terms']));assert len(terms)==m
                assert all(term>=v.reciprocal_bound(y) for term,y in zip(terms,values))
                assert F(row['cost'])==sum(terms)
                shapes.append({'floor_entries':floors,'initial_slope_one_edges':q})
            k=v.verify_farey(row)
        upper=(F(14784,10000)*m*d**m).__ceil__()
        assert int(cert['upper_ceiling'])==upper and cert['final_K']==k
        assert cert['conditional_contradiction']==(k>upper)
        receipts.append({'m':m,'minimum_factor':cert['minimum_factor'],'arithmetic_passed':True,'shapes':shapes})
    result={'status':'passed','capacity_map_proved':False,'map_id':data['map_id'],'rows':receipts,
            'input_sha256':sha(path),'source_sha256':sha(Path(__file__)),
            'verification_source_sha256':sha(ROOT/'src'/'verify_certificates.py'),
            'warning':'Arithmetic under an unproved capacity map. Not a cycle exclusion.'}
    (R/(path.stem+'-audit.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('PASSED independent forward profiles:',data['map_id'],len(receipts),flush=True)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args();audit(a.input)
