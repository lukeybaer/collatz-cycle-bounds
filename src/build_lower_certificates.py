from exact_intervals import cycle_lower_bound
from pathlib import Path
import json

out=[]
for m in range(96,101):
    k,rows=cycle_lower_bound(m,2**71,method='two_block')
    out.append(dict(m=m,minimum=str(2**71),K_proved=k,rows=rows))
    print(m,k,flush=True)
path=Path(__file__).resolve().parents[1]/'results'/'K-lower-bounds-two-block.json'
path.write_text(json.dumps(out,indent=2)+'\n')
