"""Floating-point scouting only: interval covers for local interpolation loss."""
from pathlib import Path
import math,json
J0=2000
delta=math.log2(3);beta=delta-1
U=(12/7)*(1+1/J0)*.6932
factor=4.49
rows=[]
for d,E in ((2,3),(4,4),(8,5),(16,6)):
  for L in range(3,10):
    for xn in range(60,281):
      x=xn/20
      M=x*J0
      if M<6000:continue
      for rn in range(20,241):
        r=rn/20
        S=math.ceil((x*L/r)-1e-12)
        if S>40 or S<3:continue
        gr=r/2+(L-1)/(2*J0)-x*L/(6*S)
        gs=S/2-x*L/(6*(r+(L-1)/J0))
        if gr<=0 or gs<=0:continue
        # 3lnN/J <= 3ln(x*L*J0)/J0, decreasing for J>=J0.
        overhead=3*math.log(x*L*J0)/J0
        allowed=(x*(L-1)*E*.693-overhead-L*(gr*d*1.099+gs*U))/x
        max_b=math.exp(allowed) if allowed<700 else float('inf')
        cap=(2*(x*J0-1)*max_b/factor-r*J0-(L-2)-(S-1)*(d-1)/d)*d/((S-1)*J0)
        cost=E*x*L
        need=(cost+2*delta/beta)/delta
        if cap<need or d*r+2>=need:continue
        rows.append({'d':d,'E':E,'x':x,'L':L,'r':r,'S':S,'cost':cost,
                     'lower':need,'upper':cap,'lnb_limit':allowed})
rows.sort(key=lambda v:(v['lower'],-v['upper']))
# Greedily identify the connected component reaching the proven tail at 256.
edge=256.;chosen=[]
while True:
    available=[r for r in rows if r['upper']>edge and r['lower']<edge]
    if not available:break
    r=min(available,key=lambda v:(v['lower'],-v['upper']))
    chosen.append(r);edge=r['lower']
out={'status':'floating_point_exploration_only','J_minimum':J0,'J_multiple':20,
     'factorial_factor':factor,'candidate_count':len(rows),'lowest_connected_threshold':edge,
     'backwards_cover':chosen,'best_low_threshold_candidates':rows[:20]}
dest=Path(__file__).resolve().parents[1]/'results/interpolation-cover-exploration.json'
dest.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out),flush=True)
