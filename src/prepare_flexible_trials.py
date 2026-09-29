"""Preserve unsuccessful trials and prepare separately labelled weaker maps."""
from pathlib import Path
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
base=R/'high-capacity-J42-classes.json'
rows=[]
for path in sorted(R.glob('flexible-J42-c4150-*-result.json')):
    data=json.loads(path.read_text(encoding='utf-8-sig'))
    errors=Counter(str(r.get('error')).splitlines()[0] for r in data['rows'] if r['status']!='complete')
    rows.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                 'status':data['status'],'classes':data['classes'],'nodes':data['nodes'],
                 'max_depth':data['max_depth'],'seconds':data['seconds'],
                 'unresolved':sum(errors.values()),'errors':dict(errors)})
out=R/'flexible-c4150-failed-trials-audit.json'
# The original trial receipts remain immutable; this compact index is derived.
out.write_text(json.dumps({'status':'experiment_unresolved','trials':rows,
  'interpretation':'Resource-limited proof failures, not counterexamples to the map or to Collatz.'},indent=2)+'\n')
for c in (3999,4050,4099):
    data=json.loads(base.read_text());data['low_c_numerator']=c
    data['map_id']=f'plateau-c{c}-c4199-h71'
    data['source_class_file']=base.name;data['source_class_sha256']=hashlib.sha256(base.read_bytes()).hexdigest()
    path=R/f'flexible-capacity-J42-c{c}-classes.json'
    content=json.dumps(data,indent=2)+'\n'
    if path.exists():assert path.read_text()==content
    else:path.write_text(content)
print(json.dumps(rows,indent=2),flush=True)
