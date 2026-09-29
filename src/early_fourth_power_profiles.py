"""Exact factor-one profile proposals for the previously reproduced92..95 cases."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
from fourth_power_grafted_profile_proposals import cost,MAP,X,DHI,DLO,L2LO,simplest_open
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'

def main():
    initial={r['m']:r['K_proved'] for r in json.loads((R/'K-lower-bounds-reproduction.json').read_text())}
    output=[]
    for m in range(92,96):
        k=initial[m];rows=[];upper=(F(14784,10000)*m*DHI**m).__ceil__()
        for _ in range(40):
            bound,profile=cost(m,k,X);width=bound/(k*L2LO);farey=simplest_open(DLO,DHI+width)
            rows.append({'input_K':k,'cost':str(bound),'width':str(width),'profile':profile,'farey':farey})
            if farey['q']<=k:break
            k=farey['q']
            if k>upper:break
        assert k>upper,(m,k,upper)
        output.append({'m':m,'minimum_factor':1,'minimum':str(X),'initial_K':initial[m],
            'final_K':k,'upper_ceiling':str(upper),'capacity_map_id':MAP,'capacity_map_proved':False,
            'conditional_contradiction':True,'rows':rows})
        print('Exact factor-one proposal',m,k,flush=True)
    out={'status':'unproved_map_proposals','capacity_map_proved':False,'map_id':MAP,
         'parameters':{'c0':'3799/100','c1':'4099/100','h':71,'epsilon':'1/93','cutoff':2**15},
         'rows':output,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'warning':'Exact proposals awaiting their independent forward audit and frozen-map dependency check.'}
    (R/'early-fourth-power-profile-proposals.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
