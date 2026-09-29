"""Rebuild the proposed extremizers in the forward direction, independently."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import verify_certificates as v
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    path=R/'fourth-power-grafted-profile-proposals.json';data=json.loads(path.read_text())
    assert data['status']=='unproved_map_proposals' and not data['capacity_map_proved']
    assert data['parameters']=={'c0':'3799/100','c1':'4099/100','h':71,'epsilon':'1/93','cutoff':2**15}
    d=v.DHI;c0=F(3799,100);c1=F(4099,100);eps=F(1,93);B=2**15
    lam=d-eps;offset=71*(d-1)-c0;tail=eps*B-c1
    def phi(y):return min(max(d*y-c1,min(d*y-c0,y+offset)),lam*y+tail)
    pieces={1:(d,-c0),2:(F(1),offset),3:(d,-c1),4:(lam,tail)}
    initial={}
    for row in v.read('K-lower-bounds-family-J38.json'):
        if row['m'] not in {r['m'] for r in data['rows']}:continue
        _,capacity=v.verify_capacity(row['capacity_certificate'])
        bound=v.verify_suffix(row['rows'],row['m'],int(row['minimum']),capacity_c=capacity)
        assert bound==row['K_proved'];initial[row['m']]=bound
    rows=[]
    for cert in data['rows']:
        m=cert['m'];minimum=int(cert['minimum']);k=cert['initial_K']
        assert minimum==cert['minimum_factor']*2**71 and k<=initial[m]
        assert cert['capacity_map_id']==data['map_id'] and not cert['capacity_map_proved']
        checks=0
        for row in cert['rows']:
            assert row['input_K']==k;profile=row['profile']
            if profile['mode']=='minimum_only':
                assert F(row['cost'])==F(m,minimum)
            else:
                assert profile['mode']=='grafted_majorization'
                b=F(profile['floor']);assert 71<=b<=v.log2_lower(minimum+1)
                hints=profile['inverse_pieces_from_largest'];assert len(hints)==m-1
                assert all(h in (0,1,2,3,4) for h in hints)
                floors=hints.count(0);active=[h for h in hints if h!=0][::-1]
                pairs=[(F(1),F(0))]
                for h in active:
                    a,c=pairs[-1];slope,shift=pieces[h]
                    pairs.append((slope*a,slope*c+shift))
                base=(k-floors*b-sum(c for _,c in pairs))/sum(a for a,_ in pairs)
                ramp=[a*base+c for a,c in pairs];values=[b]*floors+ramp
                assert base>=b and (not floors or base<=phi(b))
                assert len(values)==m and sum(values)==k
                assert all(ramp[i+1]==phi(ramp[i]) for i in range(len(ramp)-1))
                assert all(values[i]<=values[i+1] for i in range(m-1))
                assert all(values[(i+1)%m]<=phi(values[i]) for i in range(m))
                terms=list(map(F,profile['terms']));assert len(terms)==m
                assert all(a>=v.reciprocal_bound(y) for a,y in zip(terms,values))
                assert F(row['cost'])==sum(terms);checks+=m
            k=v.verify_farey(row)
        upper=(F(14784,10000)*m*d**m).__ceil__()
        assert cert['final_K']==k and int(cert['upper_ceiling'])==upper and k>upper
        rows.append({'m':m,'minimum_factor':cert['minimum_factor'],'profile_entries_checked':checks,
                     'arithmetic_passed':True})
    result={'status':'passed','capacity_map_proved':False,'map_id':data['map_id'],'rows':rows,
            'input_sha256':sha(path),'source_sha256':sha(Path(__file__)),
            'verification_source_sha256':sha(ROOT/'src'/'verify_certificates.py'),
            'warning':'Exact arithmetic passed; the new graft capacity requires a separate proof audit.'}
    (R/'fourth-power-grafted-profile-proposals-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASSED independent forward graft profiles:',[(x['m'],x['minimum_factor']) for x in rows],flush=True)
    return result
if __name__=='__main__':main()
