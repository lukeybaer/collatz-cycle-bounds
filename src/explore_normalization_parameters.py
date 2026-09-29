import math,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
delta=math.log2(3);beta=delta-1;rows=[]
for d,E in ((1,2),(2,3),(4,4),(8,5),(16,6)):
  for cap in (96,128,160,256):
    found=[]
    for x in range(1,31):
      for L in range(3,22):
        for r in range(1,31):
          S=math.ceil(x*L/r)
          if S>50:continue
          margins=[]
          for J in (1000,1001,10000,10**10):
            M=x*J;R=r*J+L-1;N=M*L;gamma=.5-N/(6*R*S)
            b=4.6*(R-1+(S-1)*(cap*J+d-1)/d)/(2*(M-1))
            h2=(12/7)*(J+1)*math.log(2)
            margin=(M*(L-1)*E*math.log(2)-3*math.log(N)-(M-1)*math.log(b)-gamma*L*(R*d*math.log(3)+S*h2))/J
            margins.append(margin)
          if min(margins)<=0:continue
          cost=E*x*L;threshold=(cost+(delta+1)/beta)/delta
          if d*r>threshold-2 or threshold>=cap:continue
          found.append({'x':x,'L':L,'r':r,'S':S,'cost':cost,'margin':min(margins),'C_heuristic':threshold})
    found.sort(key=lambda r:(r['cost'],-r['margin']))
    rows.append({'normalization_d':d,'E':E,'cap':cap,'J_min_sampled':1000,'best':found[:4]})
    print(d,E,cap,found[:1],flush=True)
(root/'results/normalization-parameter-exploration.json').write_text(json.dumps({'status':'floating_point_exploration_only','rows':rows},indent=2)+'\n',encoding='utf-8')
