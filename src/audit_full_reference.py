"""Compare complete reference and fixed-width runs, allowing different splits."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results'
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(name):return hashlib.sha256((R/name).read_bytes()).hexdigest()

def compare(wide,reference):
    w=read(wide+'-result.json');r=read(reference+'-result.json')
    wm=read(wide+'-metadata.json');rm=read(reference+'-metadata.json')
    wa=read(wide+'-audit.json');ra=read(reference+'-audit.json')
    assert wm['configHash']==rm['configHash']
    assert w['status']==r['status']=='complete' and w['excluded'] and r['excluded']
    assert wa['status']==ra['status']=='passed'
    for label in (wide,reference):
        assert read(label+'-generator-audit.json')['status']=='passed'
    keys=('singletons','descent','capacity','empty','survivors','odd_tail','even_tail')
    for key in keys:assert w[key]==r[key],key
    assert w['survivors']==0
    # The generator counts each split root once; the dispatched job counts it again.
    wn=w['nodes']-wa['jobs_expected'];rn=r['nodes']-ra['jobs_expected']
    assert wn==rn
    dependencies={label+suffix:sha(label+suffix) for label in (wide,reference)
                  for suffix in ('-result.json','-metadata.json','-audit.json','-generator-audit.json')}
    receipt={'status':'passed','wide':wide,'reference':reference,'config_sha256':wm['configHash'],
             'normalized_nodes':wn,'normalization':'nodes minus number of dispatched split roots',
             'matching_counters':{key:w[key] for key in keys},'dependencies':dependencies}
    (R/(wide+'-full-reference-audit.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(wide, 'PASSED',wn,'normalized nodes',flush=True)

if __name__=='__main__':
    compare('wide-m96-J35-fractional-release','reference-m96-J35-fractional-release')
    compare('wide-m97-J35-release','reference-m97-J35-release')
    compare('wide-m98-J38-fractional-release','reference-m98-J38-fractional-release')
