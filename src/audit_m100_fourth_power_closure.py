"""Join a completed grafted search to its checked profile contradiction."""
from pathlib import Path
import argparse,hashlib,json
from verify_fourth_power_grafted_capacity import verify,NAME
from audit_nonlinear_config import audit as audit_config
from audit_journal import audit as audit_journal
from audit_resume import audit as resume_audit,resolve_parent
from audit_fourth_power_grafted_profiles import main as audit_profiles
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main(m,label,config):
    result=read(label+'-result.json')
    assert result['status']=='complete' and result['excluded'] and result['survivors']==0
    audited_profiles=audit_profiles();assert audited_profiles['status']=='passed'
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
    proposals=read('fourth-power-grafted-profile-proposals.json')
    profiles=read('fourth-power-grafted-profile-certificates.json')
    assert profiles['capacity_map_proved'] and profiles['capacity_certificate']==NAME
    assert profiles['capacity_certificate_sha256']==sha(R/NAME)
    candidates=[r for r in profiles['rows'] if r['m']==m]
    originals=[r for r in proposals['rows'] if r['m']==m]
    assert len(candidates)==len(originals)==1
    row,original=candidates[0],originals[0]
    assert row['capacity_map_proved'] and row['capacity_certificate']==NAME
    assert row['capacity_certificate_sha256']==sha(R/NAME)
    for key,value in original.items():
        if key not in ('capacity_map_proved','warning'):assert row[key]==value
    assert int(row['minimum'])<=int(cfg['high']) and row['conditional_contradiction']
    assert cfg['capacity_method']=='nonlinear' and m==100
    assert int(row['final_K'])>int(row['upper_ceiling'])
    deps={NAME,config,config.removesuffix('.json')+'-audit.json',
          'fourth-power-grafted-profile-certificates.json','fourth-power-grafted-profile-proposals.json',
          'fourth-power-grafted-profile-proposals-audit.json',cfg['initial_K_certificate'],cfg['capacity_certificate']}
    deps.update(label+suffix for suffix in ('-result.json','-metadata.json','-journal.jsonl',
                                          '-audit.json','-generator-audit.json','-partition-audit.json'))
    if 'resumeSourceHash' in meta:
        assert meta['resumeSourceHash'].lower()==sha(ROOT/'src/ResumePrefixKernel.cs')
        resume_audit(label)
        provenance=read(label+'-resume-audit.json');assert provenance['status']=='passed'
        deps.add(label+'-resume-audit.json')
        for field in ('parentJournal','parentMetadata'):
            parent=resolve_parent(meta[field],meta[field+'Hash'])
            deps.add(parent.relative_to(R).as_posix())
    if result['big_fallbacks']:
        fallback=read(label+'-fallback-reference-audit.json')
        selected=read(label+'-fallback-jobs.json')
        assert fallback['status']=='passed'
        assert fallback['journalHash'].lower()==sha(R/(label+'-journal.jsonl'))
        assert fallback['referenceSourceHash'].lower()==sha(ROOT/'src/PrefixKernel.cs')
        assert fallback['driverSourceHash'].lower()==sha(ROOT/'src/audit_fallback_jobs.ps1')
        assert fallback['selectionHash'].lower()==sha(R/(label+'-fallback-jobs.json'))
        assert fallback['configHash'].lower()==sha(R/config)
        assert selected['journal_sha256']==sha(R/(label+'-journal.jsonl'))
        assert sum(r['receipt']['big_fallbacks'] for r in selected['jobs'])==result['big_fallbacks']
        assert [r['job'] for r in fallback['jobs']]==[r['job'] for r in selected['jobs']]
        for a,b in zip(fallback['jobs'],selected['jobs']):
            assert all(a['reference'][key]==b['receipt'][key] for key in
                       ('nodes','singletons','descent','capacity','empty','survivors','odd_tail','even_tail'))
        deps.update((label+'-fallback-jobs.json',label+'-fallback-reference-audit.json'))
    reference=R/(label+'-full-reference-audit.json')
    reference_status='not yet a complete original-arithmetic repeat'
    if reference.exists():
        ref=read(reference.name);assert ref['status']=='passed' and ref['wide']==label
        for dep,value in ref['dependencies'].items():assert sha(R/dep)==value
        ref_label=ref['reference']
        assert read(ref_label+'-partition-audit.json')['status']=='passed'
        ref_journal=audit_journal(R/(ref_label+'-journal.jsonl'))
        assert ref_journal==read(ref_label+'-audit.json') and ref_journal['status']=='passed'
        deps.update(ref['dependencies'])
        deps.update((ref_label+'-journal.jsonl',ref_label+'-partition-audit.json'))
        deps.add(reference.name);reference_status='complete counter-for-counter original-arithmetic repeat'
    sources=('audit_m100_fourth_power_closure.py','audit_nonlinear_config.py','verify_fourth_power_grafted_capacity.py',
             'audit_fourth_power_grafted_profiles.py','audit_journal.py','PrefixKernel.cs','PrefixKernel128.cs',
             'WideInteger.cs','PartitionAudit.cs','audit_fallback_jobs.ps1','audit_full_reference.py','audit_resume.py','ResumePrefixKernel.cs','verify_nonlinear_capacity.py')
    receipt={'status':'passed','m':m,'externally_reviewed':False,'novelty_confirmed':False,
             'search_capacity_map_id':cfg['capacity_map_id'],'profile_capacity_map_id':profiles['map_id'],
             'minimum_window':[cfg['low'],cfg['high']],'complementary_profile_minimum':str(row['minimum']),
             'initial_search_K':cfg['K'],'final_K':str(row['final_K']),'upper_ceiling':row['upper_ceiling'],
             'nodes':result['nodes'],'jobs':journal['jobs_expected'],'zero_survivors':True,
             'full_original_reference':reference_status,
             'dependencies':{name:sha(R/name) for name in sorted(deps)},
             'source_dependencies':{name:sha(ROOT/'src'/name) for name in sources},
             'warning':'Internally checked m100 exclusion. The nonlinear search covers minima through16X; the independent fourth-power profile rules out every minimum above15X, so the two necessary-condition arguments overlap. Written proofs and external inputs require independent review. Full Collatz remains open.'}
    name=f'cycle-exclusion-m{m}-fourth-power-closure-audit.json'
    (R/name).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('PASSED end-to-end grafted cycle exclusion',m,flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,required=True)
    p.add_argument('--label',required=True);p.add_argument('--config',required=True)
    a=p.parse_args();main(a.m,a.label,a.config)
