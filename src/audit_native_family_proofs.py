"""Join two complete family proofs, their exhaustive inputs, and source hashes.

One implementation uses affine inverse residues; the other bisects progression
indices. Conditional inputs are independently reconstructed from global classes.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(J,producer,producer_source,progression,factor=None,write=True):
    assert 31<=J<=41
    allowed={'FamilyCapacityPrecise.cs','FamilyCapacityPreciseFast.cs','FamilyCapacityClipped.cs','ConditionalFamilyCapacity.cs'}
    assert producer_source in allowed
    conditional=factor is not None
    global_name=f'extended-capacity-J{J}-classes.json'
    input_name=f'conditional-capacity-J{J}-f{factor}-classes.json' if conditional else global_name
    data=read(input_name);glob=read(global_name)
    coverage_name=f'extended-capacity-J{J}-coverage-audit.json';coverage=read(coverage_name)
    sweep_name=f'extended-capacity-J{J}-global.json';sweep=read(sweep_name)
    assert glob['J']==data['J']==J and int(glob['verified_basin'])==int(data['verified_basin'])==X
    assert coverage['status']==sweep['status']=='passed'
    assert coverage['input_sha256']==sha(R/global_name)
    assert coverage['source_sha256']==sha(ROOT/'src'/'audit_extended_coverage.py')
    assert coverage['pairs']==sweep['checked_pairs']==(J-1)*(2**19-1)
    assert int(coverage['seeds'])==int(glob['seed_count']) and coverage['classes']==len(glob['classes'])
    cut=X
    if conditional:
        assert factor>=1 and producer_source=='ConditionalFamilyCapacity.cs'
        cut=factor*X;assert int(data['assumed_cycle_minimum'])==cut
        expected=[]
        for i,case in enumerate(glob['classes']):
            a=int(case['first_a']);step=int(case['step_a']);count=int(case['count']);k=case['k']
            assert int(case['last_a'])==a+(count-1)*step
            root=(a<<k)-1;spacing=step<<k
            gone=max(0,min(count,(cut-root)//spacing+1))
            if gone<count:
                row=dict(case);row.update(source_class=i,first_a=str(a+gone*step),count=str(count-gone));expected.append(row)
        assert data['classes']==expected
    else:
        assert producer_source!='ConditionalFamilyCapacity.cs' and 'assumed_cycle_minimum' not in data
    count=sum(int(row['count']) for row in data['classes']);assert count==int(data['seed_count'])
    c=F(100*J-1,100)
    assert F(cut.bit_length()-1)>c/(F(1584962,10**6)-1)
    from audit_logtable import audit as audit_logs
    log_check=audit_logs(write=False)
    dependencies=[input_name,global_name,coverage_name,sweep_name,'log2-mantissa-table.json']
    log_sidecar=R/(producer+'-logtable.sha256')
    if log_sidecar.exists():
        assert log_sidecar.read_text(encoding='utf-8-sig').strip().lower()==log_check['table_sha256']
        dependencies.append(log_sidecar.name)
    for label,source,keys in (
        (producer,producer_source,('expected','restart_seeds','threshold_seeds' if conditional else 'basin_seeds','singleton_seeds')),
        (progression,'ProgressionCapacityVerifier.cs',('seeds','restart','threshold','singles'))):
        result_name=label+'-result.json';meta_name=label+'-metadata.json'
        result=read(result_name);meta=read(meta_name)
        assert result['status']=='complete' and result['full_input'] and result['capacity_exceptions_discharged']
        assert result['J']==J and result['classes']==len(data['classes']) and int(result['seeds'])==count
        assert meta['inputHash'].lower()==sha(R/input_name) and meta['sourceHash'].lower()==sha(ROOT/'src'/source)
        if conditional:assert result['conditional_only'] and int(result['assumed_cycle_minimum'])==cut
        else:assert not result.get('conditional_only',False)
        assert len(result['rows'])==len(data['classes'])
        for i,(row,case) in enumerate(zip(result['rows'],data['classes'])):
            assert row['id']==i and row['status']=='complete' and not row.get('error')
            assert int(row[keys[0]])==int(case['count'])
            assert all(int(row[key])>=0 for key in keys[1:])
            assert sum(int(row[key]) for key in keys[1:])==int(case['count'])
        assert sum(row['nodes'] for row in result['rows'])==result['nodes']
        assert sum(row['singleton_steps'] for row in result['rows'])==result['singleton_steps']
        dependencies += [result_name,meta_name]
    # The compiled progression translation was checked against every Python
    # row on the full J35 corpus, including millions of overflow fallback steps.
    translation='family-J35-progression-full-python-comparison.json';check=read(translation)
    assert check['status']=='passed' and check['classes']==17993
    assert check['source_sha256']==sha(ROOT/'src'/'ProgressionCapacityVerifier.cs')
    for dep,expected_hash in check['dependencies'].items():assert sha(R/dep)==expected_hash
    dependencies += [translation]
    result={'status':'passed','J':J,'conditional_only':conditional,'assumed_cycle_minimum':str(cut) if conditional else None,
            'classes':len(data['classes']),'seeds':str(count),'producer':producer,'producer_source':producer_source,
            'progression':progression,'source_sha256':sha(Path(__file__)),
            'source_dependencies':{name:sha(ROOT/'src'/name) for name in (producer_source,'ProgressionCapacityVerifier.cs','audit_extended_coverage.py','audit_logtable.py')},
            'dependencies':{name:sha(R/name) for name in sorted(set(dependencies))}}
    if write:
        name=progression+'-proof-pair-audit.json';(R/name).write_text(json.dumps(result,indent=2)+'\n')
        print('PASSED complete proof pair',J,'conditional',conditional,len(data['classes']),'classes',flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,required=True);p.add_argument('--producer',required=True)
    p.add_argument('--producer-source',required=True);p.add_argument('--progression',required=True);p.add_argument('--factor',type=int)
    a=p.parse_args();audit(a.J,a.producer,a.producer_source,a.progression,a.factor)
