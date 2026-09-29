"""Copy external checkpoint parents into a portable, content-addressed folder."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';folder=R/'resume-parents'
rows=[]
for meta_path in R.glob('*-metadata.json'):
    meta=json.loads(meta_path.read_text(encoding='utf-8-sig'))
    if 'parentJournal' not in meta:continue
    for field in ('parentJournal','parentMetadata'):
        original=Path(meta[field]);expected=meta[field+'Hash'].lower()
        assert hashlib.sha256(original.read_bytes()).hexdigest()==expected
        if original.parent.resolve()==R.resolve():
            relative=original.relative_to(R).as_posix()
        else:
            folder.mkdir(exist_ok=True);target=folder/(expected+original.suffix)
            if not target.exists():shutil.copyfile(original,target)
            assert hashlib.sha256(target.read_bytes()).hexdigest()==expected
            relative=target.relative_to(R).as_posix()
        rows.append({'metadata':meta_path.name,'field':field,'sha256':expected,'portable_path':relative})
(R/'resume-parent-locations.json').write_text(json.dumps({'status':'preserved','parents':rows},indent=2)+'\n')
print('Preserved',len(rows),'checkpoint parent references',flush=True)
