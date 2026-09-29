"""A deterministic permutation gives broad samples without claiming coverage."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
base=R/'high-capacity-J42-classes.json';data=json.loads(base.read_text());cases=data['classes']
selected=set(range(0,len(cases),max(1,len(cases)//150)))
by_k={}
for i,row in enumerate(cases):by_k.setdefault(row['k'],[]).append(i)
for indices in by_k.values():
    selected.update((indices[0],indices[-1],max(indices,key=lambda i:int(cases[i]['count']))))
order=sorted(selected)+[i for i in range(len(cases)) if i not in selected]
assert sorted(order)==list(range(len(cases)))
for c in (3999,4050,4099):
    original=R/f'flexible-capacity-J42-c{c}-classes.json';data=json.loads(original.read_text())
    data['classes']=[cases[i] for i in order];data['class_permutation']=order
    data['sample_count']=len(selected);data['sample_only']=True
    data['unpermuted_file']=original.name;data['unpermuted_sha256']=hashlib.sha256(original.read_bytes()).hexdigest()
    path=R/f'flexible-capacity-J42-c{c}-balanced.json';assert not path.exists()
    path.write_text(json.dumps(data,indent=2)+'\n')
print('Balanced sample size:',len(selected),'of',len(cases),flush=True)
