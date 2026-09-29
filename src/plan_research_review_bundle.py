"""Discover the transitive file closure of completed exclusion receipts.

Does not package running computations or third-party papers. A later fresh
extraction must run the end-to-end audits before the package is called usable.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
ROOTS=['cycle-exclusions-m92-m95-fourth-power-direct-audit.json',
       'cycle-exclusions-m96-m98-fourth-power-direct-audit.json',
       'cycle-exclusion-m99-two-regime-grafted-audit.json',
       'cycle-exclusion-m100-fourth-power-grafted-audit.json',
       'four-range-exponential-bound-audit.json',
       'optimized-global-cutoffs-audit.json','retained-loss-exponential-bound-audit.json']
included=set();queue=[];unresolved=set()

def add(path):
    path=path.resolve()
    if path in included:return
    assert path.is_relative_to(ROOT)
    included.add(path)
    if path.suffix=='.json':queue.append(path)

def candidate(name):
    if not isinstance(name,str) or len(name)>500:return
    if not name.endswith(('.json','.jsonl','.sha256','.md','.lean','.cs','.py','.ps1','.txt','.toml')):return
    # Saved machine-specific paths can be relocated only when an existing
    # repository file with the exact basename is available.
    portable=name.replace('\\','/')
    options=[ROOT/portable,R/portable,ROOT/'src'/portable,ROOT/'formal'/portable,
             R/portable.rsplit('/',1)[-1]]
    for p in options:
        p=p.resolve()
        if p.is_relative_to(ROOT) and p.is_file():add(p);return
    unresolved.add(name)

def scan(value):
    if isinstance(value,dict):
        for key,val in value.items():candidate(key);scan(val)
    elif isinstance(value,list):
        for val in value:scan(val)
    elif isinstance(value,str):candidate(value)

for name in ROOTS:add(R/name)
while queue:
    path=queue.pop()
    scan(json.loads(path.read_text(encoding='utf-8-sig')))
files={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,
       'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(included)}
out={'status':'dependency_inventory_only','roots':ROOTS,'files':files,
     'unresolved_file_like_references':sorted(unresolved),
     'total_bytes':sum(v['bytes'] for v in files.values()),
     'warning':'Not yet a distribution certificate. Frozen dependency checks and end-to-end fresh-extraction audits remain required.'}
(R/'research-review-bundle-plan.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(files),'bytes':out['total_bytes'],'unresolved':out['unresolved_file_like_references']}),flush=True)
