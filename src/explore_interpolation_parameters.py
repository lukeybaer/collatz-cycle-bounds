"""Floating-point parameter scouting only; never a certificate."""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
delta=math.log2(3);beta=delta-1
rows=[]
for cap in (128,160,192,224,256,384,512):
    found=[]
    for x in range(8,31):
        for L in range(3,15):
            for r in range(1,31):
                S=math.ceil(x*L/r)
                if S>40:continue
                margins=[]
                for J in (100,101,200,1000,10**6,10**12):
                    M=x*J;R=r*J+L-1;N=M*L
                    gamma=.5-N/(6*R*S)
                    b=4.6*(R-1+(S-1)*(cap*J+1)/2)/(2*(M-1))
                    h2=(12/7)*(J+1)*math.log(2)
                    margin=(M*(L-1)*3*math.log(2)-3*math.log(N)-(M-1)*math.log(b)
                            -gamma*L*(R*2*math.log(3)+S*h2))/J
                    margins.append(margin)
                if min(margins)<=0:continue
                cost=3*x*L
                # For an additive J loss at the endpoint of a two-block restart.
                threshold=(cost+(delta+1)/beta)/delta
                if 2*r>threshold or threshold>=cap:continue
                found.append({'x':x,'L':L,'r':r,'S':S,'valuation_over_J':cost,
                              'sampled_margin_min':min(margins),
                              'k_over_J_threshold_heuristic':threshold})
    found.sort(key=lambda r:(r['valuation_over_J'],-r['sampled_margin_min']))
    rows.append({'cap_k_over_J':cap,'best':found[:8]})
out={'status':'exploration_only','parameters_sampled':True,'rows':rows,
     'warning':'Floating point sampled inequalities do not prove any universal estimate.'}
(ROOT/'results/interpolation-parameter-exploration.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
for row in rows:print(row['cap_k_over_J'],row['best'][:2],flush=True)
