"""Join a completed nonlinear search to its checked profile contradiction."""
from pathlib import Path
import argparse,hashlib,json
from verify_nonlinear_capacity import verify,NAME
from audit_nonlinear_config import audit as audit_config
from audit_journal import audit as audit_journal
from audit_nonlinear_profiles import main as audit_profiles
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main(m,label,config):
    result=read(label+'-result.json')
    assert result['status']=='complete' and result['excluded'] and result['survivors']==0
    audit_profiles();assert read('nonlinear-profile-proposals-audit.json')['status']=='passed'
    verify()
    target_check=audit_config(config);assert target_check['status']=='passed'
    cfg=read(config);meta=read(label+'-metadata.json')
    assert cfg['m']==m and int(cfg['low'])==X and meta['config']==cfg
    assert meta['configHash'].lower()==sha(R/config)
    assert meta['sourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel128.cs')
    assert meta['arithmeticHash'].lower()==sha(ROOT/'src'/'WideInteger.cs')
    journal=audit_journal(R/(label+'-journal.jsonl'))
    assert journal==read(label+'-audit.json') and journal['status']=='passed'
    generator=read(label+'-generator-audit.json');partition=read(label+'-partition-audit.json')
    assert generator['status']==partition['status']=='passed'
    assert generator['jobs']==partition['jobs']==journal['jobs_expected']
    assert generator['configHash'].lower()==sha(R/config)
    assert generator['sourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel.cs')
    assert all(generator['generator'][key]==value for key,value in journal['generator_counters'].items())
    with (R/(label+'-journal.jsonl')).open(encoding='utf-8-sig') as stream:
        start=json.loads(next(stream));last=None
        for line in stream:last=line
    finish=json.loads(last)
    assert start['m']==m and int(start['low'])==X and int(start['high'])==int(cfg['high'])
    assert finish['event']=='finish' and finish['receipt']==result
    proposals=read('nonlinear-profile-proposals.json')
    profiles=read('nonlinear-profile-certificates.json')
    candidates=[r for r in profiles if r['m']==m]
    originals=[r for r in proposals if r['m']==m]
    assert len(candidates)==len(originals)==1
    row,original=candidates[0],originals[0]
    assert row['capacity_map_proved'] and row['capacity_certificate']==NAME
    assert row['capacity_certificate_sha256']==sha(R/NAME)
    for key,value in original.items():
        if key not in ('capacity_map_proved','warning'):assert row[key]==value
    assert int(row['minimum'])==int(cfg['high']) and row['conditional_contradiction']
    assert int(row['final_K'])>int(row['upper_ceiling'])
    deps={NAME,config,config.removesuffix('.json')+'-audit.json',
          'nonlinear-profile-certificates.json','nonlinear-profile-proposals.json',
          'nonlinear-profile-proposals-audit.json',cfg['initial_K_certificate']}
    deps.update(label+suffix for suffix in ('-result.json','-metadata.json','-journal.jsonl',
                                          '-audit.json','-generator-audit.json','-partition-audit.json'))
    reference=R/(label+'-full-reference-audit.json')
    reference_status='not yet a complete original-arithmetic repeat'
    if reference.exists():
        ref=read(reference.name);assert ref['status']=='passed' and ref['wide']==label
        for dep,value in ref['dependencies'].items():assert sha(R/dep)==value
        deps.add(reference.name);reference_status='complete counter-for-counter original-arithmetic repeat'
    if result['big_fallbacks']:
        fallback=read(label+'-fallback-reference-audit.json')
        assert fallback['status']=='passed'
        assert fallback['journalHash'].lower()==sha(R/(label+'-journal.jsonl'))
        assert fallback['referenceSourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel.cs')
        assert fallback['driverSourceHash'].lower()==sha(ROOT/'src'/'audit_fallback_jobs.ps1')
        selected=read(label+'-fallback-jobs.json')
        assert fallback['selectionHash'].lower()==sha(R/(label+'-fallback-jobs.json'))
        assert sum(r['receipt']['big_fallbacks'] for r in selected['jobs'])==result['big_fallbacks']
        assert [r['job'] for r in fallback['jobs']]==[r['job'] for r in selected['jobs']]
        for a,b in zip(fallback['jobs'],selected['jobs']):
            assert all(a['reference'][key]==b['receipt'][key] for key in ('nodes','singletons','descent','capacity','empty','survivors','odd_tail','even_tail'))
        deps.update((label+'-fallback-jobs.json',label+'-fallback-reference-audit.json'))
    sources=('audit_nonlinear_exclusion.py','audit_nonlinear_config.py','verify_nonlinear_capacity.py',
             'audit_nonlinear_profiles.py','audit_journal.py','PrefixKernel.cs','PrefixKernel128.cs',
             'WideInteger.cs','PartitionAudit.cs')
    receipt={'status':'passed','m':m,'externally_reviewed':False,'novelty_confirmed':False,
             'capacity_map_id':cfg['capacity_map_id'],'minimum_window':[cfg['low'],cfg['high']],
             'initial_search_K':cfg['K'],'final_K':str(row['final_K']),'upper_ceiling':row['upper_ceiling'],
             'nodes':result['nodes'],'jobs':journal['jobs_expected'],'zero_survivors':True,
             'full_original_reference':reference_status,
             'dependencies':{name:sha(R/name) for name in sorted(deps)},
             'source_dependencies':{name:sha(ROOT/'src'/name) for name in sources},
             'warning':'Internally checked cycle exclusion for the stated m, using the certified nonlinear map. Written proofs and external inputs require independent review. Full Collatz remains open.'}
    name=f'cycle-exclusion-m{m}-nonlinear-audit.json'
    (R/name).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('PASSED end-to-end nonlinear cycle exclusion',m,flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,required=True)
    p.add_argument('--label',required=True);p.add_argument('--config',required=True)
    a=p.parse_args();main(a.m,a.label,a.config)
