"""Join two completed minimum windows to the scoped final contradiction.

Refuses incomplete searches. This is a dependency audit, not a full rerun of
the search nodes or a formal verification of the written mathematics.
"""
from pathlib import Path
import hashlib,json
import verify_certificates as v
from audit_journal import audit as journal_audit
from audit_nonlinear_config import audit as nonlinear_config_audit
from audit_resume import audit as resume_audit,resolve_parent
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
CASES=(('nonlinear-config-m100-lo1-hi16.json','wide-m100-lower-nonlinear-J41-resumed-release'),
       ('native-config-m100-lo16-hi21-scoped.json','wide-m100-upper-conditional-J41-resumed-release'))
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def main():
    for _,label in CASES:
        path=R/(label+'-result.json')
        if not path.exists() or read(path.name)['status']!='complete':
            raise RuntimeError('No exclusion certificate: incomplete window '+label)
    v.main()
    lower_check=nonlinear_config_audit(CASES[0][0]);assert lower_check['status']=='passed'
    initial_name='family-J35-elementary-lower-bounds.json'
    initial=[row for row in read(initial_name) if row['m']==100];assert len(initial)==1
    initial=initial[0];assert int(initial['minimum'])==X
    _,capacity=v.verify_capacity(initial['capacity_certificate'])
    bound=v.verify_suffix(initial['rows'],100,X,capacity_c=capacity)
    assert bound==initial['K_proved']
    windows=[];dependencies={initial_name,initial['capacity_certificate']}
    for index,(config_name,label) in enumerate(CASES):
        cfg=read(config_name);meta=read(label+'-metadata.json');result=read(label+'-result.json')
        assert cfg['m']==100 and int(cfg['K'])<=bound and cfg==meta['config']
        assert meta['configHash'].lower()==sha(R/config_name)
        assert meta['sourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel128.cs')
        assert meta['arithmeticHash'].lower()==sha(ROOT/'src'/'WideInteger.cs')
        assert result['excluded'] and result['survivors']==0
        journal=journal_audit(R/(label+'-journal.jsonl'))
        assert journal==read(label+'-audit.json') and journal['status']=='passed'
        generator=read(label+'-generator-audit.json');partition=read(label+'-partition-audit.json')
        assert generator['status']==partition['status']=='passed'
        assert generator['jobs']==partition['jobs']==journal['jobs_expected']
        assert generator['sourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel.cs')
        assert generator['configHash'].lower()==sha(R/config_name)
        for key,value in journal['generator_counters'].items():assert generator['generator'][key]==value
        with (R/(label+'-journal.jsonl')).open(encoding='utf-8-sig') as stream:
            start=json.loads(next(stream));last=None
            for line in stream:last=line
        finish=json.loads(last)
        assert start['m']==100 and int(start['low'])==int(cfg['low']) and int(start['high'])==int(cfg['high'])
        assert finish['event']=='finish' and finish['receipt']==result
        if index==0:
            assert int(cfg['low'])==X and int(cfg['high'])==16*X and cfg['capacity_map_proved']
            dependencies.update((cfg['capacity_certificate'],config_name.removesuffix('.json')+'-audit.json'))
        else:
            assert int(cfg['low'])==16*X and int(cfg['high'])==21*X
            assert cfg['capacity_certificate']=='conditional-capacity-J41-f16-certificate.json'
            v.verify_scoped_capacity(cfg['capacity_certificate'],int(cfg['low']))
        if 'resumeSourceHash' in meta:
            assert meta['resumeSourceHash'].lower()==sha(ROOT/'src'/'ResumePrefixKernel.cs')
            resume_audit(label)
            provenance=read(label+'-resume-audit.json');assert provenance['status']=='passed'
            dependencies.update((cfg['capacity_certificate'],label+'-resume-audit.json'))
            for field in ('parentJournal','parentMetadata'):
                parent=resolve_parent(meta[field],meta[field+'Hash'])
                dependencies.add(parent.relative_to(R).as_posix())
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
            dependencies.update((label+'-fallback-jobs.json',label+'-fallback-reference-audit.json'))
        dependencies.add(config_name)
        dependencies.update(label+suffix for suffix in ('-result.json','-metadata.json','-journal.jsonl','-audit.json','-generator-audit.json','-partition-audit.json'))
        windows.append({'label':label,'low':cfg['low'],'high':cfg['high'],'nodes':result['nodes'],
                        'jobs':journal['jobs_expected'],'zero_survivors':True,
                        'ordered_partition_sha256':partition['ordered_partition_sha256']})
    assert windows[0]['high']==windows[1]['low']
    # The endpoints are even. The windows cover every possible odd minimum
    # above X and at most21X, with no missing boundary candidate.
    profile_name='conditional-J41-f16-profile-certificates.json'
    profile=[row for row in read(profile_name) if row['m']==100];assert len(profile)==1
    profile=profile[0];assert int(profile['minimum'])==21*X
    v.verify_profile(profile,{100:bound})
    assert profile['conditional_contradiction']
    dependencies.add(profile_name)
    sources=('audit_m100_windows.py','verify_certificates.py','audit_nonlinear_config.py','verify_nonlinear_capacity.py',
             'audit_journal.py','audit_resume.py','PrefixKernel.cs','PrefixKernel128.cs','WideInteger.cs','ResumePrefixKernel.cs','PartitionAudit.cs','audit_fallback_jobs.ps1')
    receipt={'status':'passed','m':100,'externally_reviewed':False,'novelty_confirmed':False,
             'initial_K':str(bound),'final_K':str(profile['final_K']),'upper_ceiling':profile['upper_ceiling'],
             'windows':windows,'dependencies':{name:sha(R/name) for name in sorted(dependencies)},
             'source_dependencies':{name:sha(ROOT/'src'/name) for name in sources},
             'warning':'Candidate cycle exclusion for exactly100 local minima. Includes a nonlinear lower window and a separately scoped upper window; not a proof of full Collatz.'}
    (R/'cycle-exclusion-m100-two-windows-audit.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('PASSED joined m100 minimum windows and final contradiction',flush=True)
if __name__=='__main__':main()
