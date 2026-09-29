"""Exact inverse-ramp proposals for the analytic tail graft, not a capacity proof."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D
import json,hashlib,time
import explore_nonlinear_profiles as approximate
from exact_intervals import DHI,DLO,L2LO,simplest_open
from affine_profile_certificates import log2_integer_lower,reciprocal_upper,down,HEIGHT_DEN

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
C0=F(3799,100);C1=F(4099,100);B=F(2**18);EPS=F(1,5000)
OFFSET=71*(DHI-1)-C0;TURN=71+(C1-C0)/(DHI-1)
LOW_IMAGE=71+OFFSET;HIGH_IMAGE=TURN+OFFSET
LAM=DHI-EPS;TAIL_OFFSET=EPS*B-C1;TAIL_IMAGE=DHI*B-C1
MAP='plateau-c3799-c4099-h71-graft-eps1over5000-B262144'
def dec(v):return D(v.numerator)/D(v.denominator)
original_inverse=approximate.inverse
def inverse_approximate(y):
    return original_inverse(y) if y<=dec(TAIL_IMAGE) else (y-dec(TAIL_OFFSET))/dec(LAM)
approximate.inverse=inverse_approximate
def phi(y):return min(max(DHI*y-C1,min(DHI*y-C0,y+OFFSET)),LAM*y+TAIL_OFFSET)
def inverse_piece(y):
    if y<=LOW_IMAGE:return 1,(y+C0)/DHI
    if y<=HIGH_IMAGE:return 2,y-OFFSET
    if y<=TAIL_IMAGE:return 3,(y+C1)/DHI
    return 4,(y-TAIL_OFFSET)/LAM
def reconstruct(m,total,b,branches):
    pairs=[(F(1),F(0))]
    for branch in branches:
        a,c=pairs[-1]
        if branch==0:p=F(0),b
        elif branch==1:p=a/DHI,(c+C0)/DHI
        elif branch==2:p=a,c-OFFSET
        elif branch==3:p=a/DHI,(c+C1)/DHI
        elif branch==4:p=a/LAM,(c-TAIL_OFFSET)/LAM
        else:raise AssertionError('unknown branch')
        pairs.append(p)
    top=(total-sum(c for _,c in pairs))/sum(a for a,_ in pairs)
    backwards=[a*top+c for a,c in pairs]
    assert sum(backwards)==total and all(y>=b for y in backwards)
    assert all(backwards[i+1]==max(b,inverse_piece(backwards[i])[1]) for i in range(m-1))
    values=backwards[::-1]
    assert all(values[(i+1)%m]<=phi(values[i]) for i in range(m))
    return values
def cost(m,k,minimum):
    b=log2_integer_lower(minimum+1)
    if k<=m*b:return F(m,minimum),{'mode':'minimum_only'}
    proposals=approximate.profile(m,D(k),dec(b))[::-1];branches=[]
    for y in proposals[:-1]:
        if y<=dec(LOW_IMAGE):branch=1;v=(y+dec(C0))/dec(DHI)
        elif y<=dec(HIGH_IMAGE):branch=2;v=y-dec(OFFSET)
        elif y<=dec(TAIL_IMAGE):branch=3;v=(y+dec(C1))/dec(DHI)
        else:branch=4;v=(y-dec(TAIL_OFFSET))/dec(LAM)
        branches.append(0 if v<=dec(b) else branch)
    values=reconstruct(m,F(k),b,branches);terms=[reciprocal_upper(y) for y in values]
    return sum(terms,F(0)),{'mode':'grafted_majorization','floor':str(b),
        'inverse_pieces_from_largest':branches,'largest_height_lower':str(down(values[-1],HEIGHT_DEN)),
        'terms':[str(t) for t in terms]}
def main():
    start=time.monotonic();explored=json.loads((R/'grafted-profile-exploration.json').read_text())
    initial={r['m']:r['K_proved'] for r in json.loads((R/'K-lower-bounds-family-J38.json').read_text())}
    output=[]
    for proposal in explored['rows']:
        m=proposal['m'];factor=proposal['minimum_factor'];minimum=factor*X;k=initial[m];rows=[]
        upper=(F(14784,10000)*m*DHI**m).__ceil__()
        for _ in range(40):
            bound,profile=cost(m,k,minimum);width=bound/(k*L2LO);farey=simplest_open(DLO,DHI+width)
            rows.append({'input_K':k,'cost':str(bound),'width':str(width),'profile':profile,'farey':farey})
            if farey['q']<=k:break
            k=farey['q']
            if k>upper:break
        assert k>upper
        output.append({'m':m,'minimum_factor':factor,'minimum':str(minimum),'initial_K':initial[m],
            'final_K':k,'upper_ceiling':str(upper),'capacity_map_id':MAP,'capacity_map_proved':False,
            'conditional_contradiction':True,'rows':rows})
        result={'status':'unproved_map_proposals','capacity_map_proved':False,'map_id':MAP,
            'parameters':{'c0':'3799/100','c1':'4099/100','h':71,'epsilon':'1/5000','cutoff':2**18},
            'rows':output,'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'warning':'Exact profiles under a grafted capacity hypothesis pending its separate proof audit; no cycle exclusion.'}
        (R/'grafted-profile-proposals.json').write_text(json.dumps(result,indent=2)+'\n')
        print('Exact graft proposal',m,'factor',factor,flush=True)
if __name__=='__main__':main()
