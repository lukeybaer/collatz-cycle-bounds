"""Connect completed finite searches to their exact cycle contradictions.

This is an end-to-end dependency audit, not a rerun of billions of search
nodes or a formal verification of the written mathematical arguments.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
import verify_certificates as arithmetic
from audit_journal import audit as audit_journal

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
CASES={
 96:('native-config-m96-f10-strong-fractional.json','wide-m96-J35-fractional-release','family-J35-conditional-certificates.json'),
 97:('native-config-m97-f15-strong.json','wide-m97-J35-release','family-J35-conditional-certificates.json'),
 98:('native-config-m98-f16-strong-tight-fractional.json','wide-m98-J38-fractional-release','family-J38-conditional-certificates.json'),
 99:('native-config-m99-f21-strong-fractional.json','wide-m99-J38-fractional-release','family-J38-conditional-certificates.json'),
}
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def row(name,m):
    rows=[r for r in read(name) if r['m']==m];assert len(rows)==1
    return rows[0]

def one(m):
    config_name,label,profile_name=CASES[m]
    cfg=read(config_name);result=read(label+'-result.json');meta=read(label+'-metadata.json')
    assert cfg['m']==m and int(cfg['low'])==X and int(cfg['high'])>X
    assert meta['configHash'].lower()==sha(R/config_name) and meta['config']==cfg
    assert meta['sourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel128.cs')
    assert meta['arithmeticHash'].lower()==sha(ROOT/'src'/'WideInteger.cs')
    journal_path=R/(label+'-journal.jsonl');journal=audit_journal(journal_path)
    assert journal['status']=='passed' and journal['survivors']==0
    saved=read(label+'-audit.json');assert saved==journal
    with journal_path.open(encoding='utf-8-sig') as stream:
        start=json.loads(next(stream));last=None
        for line in stream:last=line
    finish=json.loads(last)
    assert start['m']==m and int(start['low'])==X and int(start['high'])==int(cfg['high'])
    assert finish['event']=='finish' and finish['receipt']==result
    assert result['status']=='complete' and result['excluded'] and result['survivors']==0
    generator=read(label+'-generator-audit.json');partition=read(label+'-partition-audit.json')
    assert generator['status']==partition['status']=='passed'
    assert generator['jobs']==partition['jobs']==journal['jobs_expected']
    assert generator['configHash'].lower()==sha(R/config_name)
    assert generator['sourceHash'].lower()==sha(ROOT/'src'/'PrefixKernel.cs')
    for key,value in journal['generator_counters'].items():assert generator['generator'][key]==value
    initial_name='family-J35-elementary-lower-bounds.json';initial=row(initial_name,m)
    assert int(initial['minimum'])==X
    mm,c=arithmetic.verify_capacity(initial['capacity_certificate']);assert mm is None
    proved=arithmetic.verify_suffix(initial['rows'],m,X,capacity_c=c)
    assert proved==initial['K_proved'] and int(cfg['K'])<=proved
    profile=row(profile_name,m)
    arithmetic.verify_profile(profile,{m:proved})
    assert profile['conditional_contradiction'] and int(profile['minimum'])==int(cfg['high'])
    dependencies=[config_name,initial_name,profile_name,initial['capacity_certificate'],profile['capacity_certificate']]
    dependencies += [label+s for s in ('-result.json','-metadata.json','-journal.jsonl','-audit.json','-generator-audit.json','-partition-audit.json')]
    reference=R/(label+'-full-reference-audit.json')
    reference_status='not yet a complete full rerun'
    if reference.exists():
        ref=read(reference.name);assert ref['status']=='passed' and ref['wide']==label
        for dep,expected in ref['dependencies'].items():assert sha(R/dep)==expected
        dependencies.append(reference.name);reference_status='complete counter-for-counter agreement'
    return {'m':m,'status':'passed','minimum_window':[str(X),cfg['high']],
            'initial_K':str(proved),'final_K':str(profile['final_K']),'upper_ceiling':profile['upper_ceiling'],
            'nodes':result['nodes'],'jobs':journal['jobs_expected'],'zero_survivors':True,
            'full_original_reference':reference_status,
            'dependencies':{name:sha(R/name) for name in sorted(set(dependencies))}}

def main(maximum):
    assert 96<=maximum<=99
    arithmetic.main()
    rows=[]
    for m in range(96,maximum+1):
        rows.append(one(m));print('Connected complete exclusion:',m,flush=True)
    result={'status':'passed','scope':'Candidate exclusions for the explicitly listed numbers of local minima.',
            'maximum_m':maximum,'externally_reviewed':False,'novelty_confirmed':False,
            'external_inputs':['Published convergence below 2^71; endpoint is trivial.',
                               'Bugeaud 2002 Theorem 2, with the stated hypotheses.',
                               'Simons-de Weger v1.44 Theorem 3(d), within its stated m range.'],
            'analytic_dependencies':['block-restart-capacity.md','padic-capacity-program.md','majorization-lemma.md','subordinate-height-envelope.md'],
            'warning':'This joins exact certificates and completed computation receipts. Written proofs, source code and external theorems still require mathematical review; this is not a proof of full Collatz.',
            'source_dependencies':{name:sha(ROOT/'src'/name) for name in ('audit_exclusions.py','verify_certificates.py','audit_journal.py','PrefixKernel.cs','PrefixKernel128.cs','WideInteger.cs')},
            'rows':rows}
    path=R/f'cycle-exclusions-through-m{maximum}-audit.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(path,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--maximum',type=int,default=98);a=p.parse_args();main(a.maximum)
