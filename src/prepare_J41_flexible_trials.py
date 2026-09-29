"""Specialize separate, journaled copies to a stronger low-height J41 map."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proofs=[]
for kind,oldns in [('FamilyCapacity','CollatzFlexibleNonlinearFamilies'),
                   ('ProgressionVerifier','CollatzFlexibleNonlinearProgressionAudit')]:
    old=S/('FlexibleNonlinear'+kind+'.cs');new=S/('J41Flexible'+kind+'.cs')
    assert not new.exists()
    s=old.read_text(encoding='utf-8')
    s=s.replace(oldns,oldns+'J41')
    s=s.replace('(input.J<42 || input.J>48)','(input.J!=41)')
    s=s.replace('if(bits>83)','if(bits>69)')
    s=s.replace('int take=0) {','int take=0,string journalPath=null) {')
    insertion='''  using var journal=journalPath==null?null:new System.IO.StreamWriter(journalPath,false,new System.Text.UTF8Encoding(false));
'''
    marker='  var rows=new Receipt[length];'
    assert s.count(marker)==1
    s=s.replace(marker,insertion+marker)
    marker='   Interlocked.Add(ref nodes,'
    pos=s.index(marker)
    s=s[:pos]+'''   if(journal!=null)lock(journal){journal.WriteLine(JsonSerializer.Serialize(receipt));journal.Flush();}
'''+s[pos:]
    new.write_text(s,encoding='utf-8')
    runner='run_flexible_nonlinear_'+('family' if kind=='FamilyCapacity' else 'progression')+'.ps1'
    newrunner='run_J41_flexible_'+('family' if kind=='FamilyCapacity' else 'progression')+'.ps1'
    script=(S/runner).read_text(encoding='utf-8').replace(old.name,new.name).replace(oldns,oldns+'J41')
    script=script.replace('$Workers,$Depth,$NodeLimit,$Take)','$Workers,$Depth,$NodeLimit,$Take,(Join-Path $resultDir ($Label+\'-classes.jsonl\')))')
    (S/newrunner).write_text(script,encoding='utf-8')
    proofs.append({'original':old.name,'original_sha256':sha(old),'generated':new.name,
                   'generated_sha256':sha(new),'changes':['namespace only','restrict J exactly41','odd-part limit69','per-class journal after each completed or unresolved proof attempt']})
base=R/'extended-capacity-J41-classes.json';data=json.loads(base.read_text());cases=data['classes']
data.update(low_c_numerator=3999,map_id='plateau-c3999-c4099-h71',
            source_class_file=base.name,source_class_sha256=sha(base))
full=R/'flexible-capacity-J41-c3999-classes.json';assert not full.exists()
full.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
selected=set(range(0,len(cases),max(1,len(cases)//150)));by_k={}
for i,row in enumerate(cases):by_k.setdefault(row['k'],[]).append(i)
for ids in by_k.values():selected.update((ids[0],ids[-1],max(ids,key=lambda i:int(cases[i]['count']))))
order=sorted(selected)+[i for i in range(len(cases)) if i not in selected]
assert sorted(order)==list(range(len(cases)))
data.update(classes=[cases[i] for i in order],class_permutation=order,sample_count=len(selected),
            sample_only=True,unpermuted_file=full.name,unpermuted_sha256=sha(full))
sample=R/'flexible-capacity-J41-c3999-balanced.json'
sample.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
(R/'J41-flexible-source-derivations.json').write_text(json.dumps(proofs,indent=2)+'\n',encoding='utf-8')
print('Prepared',len(selected),'balanced classes out of',len(cases),flush=True)
