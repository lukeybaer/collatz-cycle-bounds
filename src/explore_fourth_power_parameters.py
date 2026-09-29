import math,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
delta=math.log2(3);beta=delta-1;J0=200;U=(12/7)*(1+1/J0)*.6932
rows=[]
for cap in list(range(76,161,2))+[192,224,256]:
    found=[]
    for d,E in ((2,3),(4,4),(8,5)):
      for x2 in range(8,31):
        x=x2/2
        for L in range(3,11):
          for r2 in range(2,31):
            r=r2/2;S=math.ceil(x*L/r)
            if S>40:continue
            gr=r/2+(L-1)/(2*J0)-x*L/(6*S)
            gs=S/2-x*L/(6*(r+(L-1)/J0))
            b=4.6*((r+(S-1)*cap/d)*J0+L-2+(S-1)*(d-1)/d)/(2*(x*J0-1))
            logb=math.ceil(math.log(b)*1000)/1000
            margin=x*(L-1)*E*.693-x*logb-.15-L*(gr*d*1.099+gs*U)
            if margin<=0:continue
            cost=E*x*L;threshold=(cost+(delta+1)/beta)/delta
            if d*r>threshold-2 or threshold>=cap:continue
            found.append({'d':d,'E':E,'x2':x2,'L':L,'r2':r2,'S':S,'cost':cost,
                          'margin_lower_heuristic':margin,'lnb_upper':logb,'C_heuristic':threshold})
    found.sort(key=lambda r:(r['cost'],-r['margin_lower_heuristic']))
    rows.append({'cap':cap,'best':found[:3]})
    if found:print(cap,found[0],flush=True)
(root/'results/fourth-power-parameter-exploration.json').write_text(json.dumps({'status':'floating_point_exploration_only','J_min':J0,'J_multiple':2,'rows':rows},indent=2)+'\n',encoding='utf-8')
