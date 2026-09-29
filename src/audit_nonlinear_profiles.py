"""Independent forward-ramp audit of the nonlinear profile proposals.

The producer solves by inverse-map branch coefficients. This checker instead
enumerates floor length and zero, one, or two initial slope-one edges, then
solves the forward ramp's total directly. No producer routines are imported.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import verify_certificates as v

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
D=v.DHI;C0=F(3799,100);C1=F(4099,100);OFFSET=71*(D-1)-C0;SHIFT=C1/(D-1)
def phi(x):return max(D*x-C1,min(D*x-C0,x+OFFSET))

def forward_profile(m,total,b):
    # Below the high-slope tail, the positive offset permits at most two
    # slope-one edges before crossing the upper breakpoint.
    turn=71+(C1-C0)/(D-1)
    assert OFFSET>0 and turn-71<2*OFFSET
    for floors in range(m):
        r=m-floors
        for flat_edges in range(min(2,r-1)+1):
            q=flat_edges;g=v.geom(r-q)
            base=(total-floors*b-OFFSET*q*(q-1)/2-(r-q)*SHIFT-g*(q*OFFSET-SHIFT))/(q+g)
            if base<b or (floors and base>phi(b)):continue
            tail=[base+j*OFFSET for j in range(q)]
            tail += [SHIFT+D**j*(base+q*OFFSET-SHIFT) for j in range(r-q)]
            if any(tail[i+1]!=phi(tail[i]) for i in range(r-1)):continue
            values=[b]*floors+tail
            assert len(values)==m and sum(values)==total
            assert all(values[i]<=values[i+1] for i in range(m-1))
            assert all(values[(i+1)%m]<=phi(values[i]) for i in range(m))
            return values,{'floors':floors,'initial_slope_one_edges':q}
    raise AssertionError('No forward extremizer found.')

def main():
    path=R/'nonlinear-profile-proposals.json';certs=json.loads(path.read_text());rows=[]
    lower=v.read('K-lower-bounds-family-J38.json');proved={}
    for record in lower:
        if record['m'] not in {c['m'] for c in certs}:continue
        _,c=v.verify_capacity(record['capacity_certificate'])
        k=v.verify_suffix(record['rows'],record['m'],int(record['minimum']),capacity_c=c)
        assert k==record['K_proved'];proved[record['m']]=k
    for cert in certs:
        m=cert['m'];minimum=int(cert['minimum']);k=cert['initial_K']
        assert not cert['capacity_map_proved'] and cert['capacity_map_id']=='plateau-c3799-c4099-h71'
        assert k<=proved[m] and minimum>=v.X
        profiles=[]
        for row in cert['rows']:
            assert row['input_K']==k;profile=row['profile']
            if profile['mode']=='minimum_only':
                assert F(row['cost'])==F(m,minimum)
                profiles.append({'mode':'minimum_only'})
            else:
                assert profile['mode']=='nonlinear_majorization'
                b=F(profile['floor']);assert 71<=b<=v.log2_lower(minimum+1) and k>=m*b
                values,shape=forward_profile(m,F(k),b)
                terms=list(map(F,profile['terms']));assert len(terms)==m
                for height,term in zip(values,terms):assert term>=v.reciprocal_bound(height)
                assert F(row['cost'])==sum(terms)
                profiles.append(shape)
            k=v.verify_farey(row)
        upper=(F(14784,10000)*m*D**m).__ceil__()
        assert cert['final_K']==k and int(cert['upper_ceiling'])==upper
        assert cert['conditional_contradiction']==(k>upper)
        rows.append({'m':m,'minimum_factor':cert['minimum_factor'],'profiles':profiles,'arithmetic_passed':True})
        print('Independent forward nonlinear profile passed:',m,profiles,flush=True)
    result={'status':'passed','capacity_map_proved':False,'cycle_exclusion_claimed':False,
            'method':'Forward floor/linear/geometric ramp, independently of inverse-piece proposal.',
            'rows':rows,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'warning':'These exact contradictions remain conditional on the currently unproved nonlinear growth map.'}
    (R/'nonlinear-profile-proposals-audit.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
