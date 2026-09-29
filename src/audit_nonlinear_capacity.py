"""Connect two full nonlinear block proofs to the exhaustive J41 input.

This checker is deliberately separate from frozen linear-capacity checkers.
It cannot issue a uniform linear coefficient certificate.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json
from audit_logtable import audit as audit_logs
from verify_nonlinear_progression import audit_targets

ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'results'; X=2**71
MAP='plateau-c3799-c4099-h71'

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))

def audit(producer='nonlinear-J41-full', progression='nonlinear-progression-full', write=True,
          progression_source='NonlinearProgressionCapacityVerifier.cs'):
    assert progression_source in ('NonlinearProgressionCapacityVerifier.cs','ClippedNonlinearProgressionVerifier.cs')
    clipped=progression_source=='ClippedNonlinearProgressionVerifier.cs'
    inp='extended-capacity-J41-classes.json'; data=read(inp)
    coverage=read('extended-capacity-J41-coverage-audit.json')
    sweep=read('extended-capacity-J41-global.json')
    assert data['J']==41 and int(data['verified_basin'])==X
    assert 'assumed_cycle_minimum' not in data
    assert coverage['status']==sweep['status']=='passed'
    assert coverage['input_sha256']==sha(R/inp)
    assert coverage['source_sha256']==sha(ROOT/'src'/'audit_extended_coverage.py')
    assert coverage['pairs']==sweep['checked_pairs']==40*(2**19-1)
    count=sum(int(c['count']) for c in data['classes'])
    assert count==int(data['seed_count'])==int(coverage['seeds'])
    assert coverage['classes']==len(data['classes'])==44497
    assert F(27660,81)*F(140,100)*F(11,10)/F(69,100)**3<1700
    assert 1700*F(153,10)**2+3<2**19
    # Phi is monotone in delta and has slopes at least one on its domain.
    d=F(1584962,10**6); offset=71*(d-1)-F(3799,100)
    assert offset>0 and d>1
    log_check=audit_logs(write=False); targets=audit_targets()
    deps=[inp,'extended-capacity-J41-coverage-audit.json','extended-capacity-J41-global.json',
          'log2-mantissa-table.json','nonlinear-progression-thresholds.json']
    sources=['audit_extended_coverage.py','audit_logtable.py','verify_nonlinear_progression.py',
             'verify_family_capacity.py','NonlinearFamilyCapacity.cs','NonlinearProgressionCapacityVerifier.cs',
             'FamilyCapacityClipped.cs','ProgressionCapacityVerifier.cs']
    for label,source,derivation,original,keys in (
        (producer,'NonlinearFamilyCapacity.cs','nonlinear-family-source-derivation.json','FamilyCapacityClipped.cs',
         ('expected','restart_seeds','basin_seeds','singleton_seeds')),
        (progression,progression_source,'clipped-nonlinear-progression-source-derivation.json' if clipped else 'nonlinear-progression-source-derivation.json',
         'PreciseNonlinearProgressionVerifier.cs' if clipped else 'ProgressionCapacityVerifier.cs',
         ('seeds','restart','threshold','singles'))):
        result=read(label+'-result.json'); meta=read(label+'-metadata.json'); origin=read(derivation)
        assert result['status']=='complete' and result['full_input'] and result['capacity_exceptions_discharged']
        assert result['capacity_kind']=='nonlinear_block_restart' and not result['linear_coefficient_certified']
        assert result['map_id']==MAP and result['J']==41 and not result.get('conditional_only',False)
        assert result['classes']==len(data['classes']) and int(result['seeds'])==count
        assert meta['inputHash'].lower()==sha(R/inp) and meta['sourceHash'].lower()==sha(ROOT/'src'/source)
        assert origin['generated_source_sha256']==sha(ROOT/'src'/source)
        assert origin['original_source_sha256']==sha(ROOT/'src'/original)
        assert origin['map_id']==MAP and meta['take']==0 and meta['depth']==16
        assert len(result['rows'])==len(data['classes'])
        for i,(row,case) in enumerate(zip(result['rows'],data['classes'])):
            assert row['id']==i and row['status']=='complete' and not row.get('error')
            assert int(row[keys[0]])==int(case['count'])
            assert all(int(row[key])>=0 for key in keys[1:])
            assert sum(int(row[key]) for key in keys[1:])==int(case['count'])
        for key in ('nodes','singleton_steps'):
            assert sum(row[key] for row in result['rows'])==result[key]
        for rowkey,summarykey in zip(keys[1:],('restart_seeds','basin_seeds' if label==producer else 'threshold_seeds','singleton_seeds')):
            assert sum(int(row[rowkey]) for row in result['rows'])==int(result[summarykey])
        deps += [label+'-result.json',label+'-metadata.json',derivation]
    sidecar=producer+'-logtable.sha256'
    assert (R/sidecar).read_text(encoding='utf-8-sig').strip().lower()==log_check['table_sha256']
    deps.append(sidecar)
    sample='nonlinear-progression-first100-python-comparison.json'; check=read(sample)
    assert check['status']=='passed' and check['classes']==100 and not check['full_input']
    assert check['map_id']==MAP and check['exact_thresholds_checked']==targets
    assert check['source_sha256']==sha(ROOT/'src'/'verify_nonlinear_progression.py')
    assert check['inherited_source_sha256']==sha(ROOT/'src'/'verify_family_capacity.py')
    assert check['native_source_sha256']==sha(ROOT/'src'/'NonlinearProgressionCapacityVerifier.cs')
    assert check['input_sha256']==sha(R/inp)
    sample_result='nonlinear-progression-first100-result.json'
    assert check['native_result_sha256']==sha(R/sample_result)
    deps += [sample,sample_result]
    if clipped:
        assert read(progression+'-result.json')['height_method']=='exact_rational_mantissa_grid_clipped'
        assert read(progression+'-metadata.json')['logTableHash'].lower()==log_check['table_sha256']
        precise_origin=read('precise-nonlinear-progression-source-derivation.json')
        assert precise_origin['original_source_sha256']==sha(ROOT/'src'/'NonlinearProgressionCapacityVerifier.cs')
        assert precise_origin['generated_source_sha256']==sha(ROOT/'src'/'PreciseNonlinearProgressionVerifier.cs')
        deps += ['precise-nonlinear-progression-source-derivation.json','nonlinear-clipped-progression-thresholds.json']
        assert sha(R/'nonlinear-clipped-progression-thresholds.json')==sha(R/'nonlinear-precise-progression-first100-thresholds.json')
        for sample_name,expected_classes,source_name,threshold_count in (
            ('nonlinear-precise-progression-first100-python-comparison.json',100,'verify_precise_nonlinear_progression.py',2032128),
            ('nonlinear-precise-progression-challenge12-python-comparison.json',12,'verify_precise_nonlinear_progression.py',0),
            ('nonlinear-clipped-progression-challenge12-python-comparison.json',12,'verify_clipped_nonlinear_progression.py',None)):
            comparison=read(sample_name)
            assert comparison['status']=='passed' and comparison['classes']==expected_classes
            assert not comparison['full_global_input'] and comparison['map_id']==MAP
            if threshold_count is not None:assert comparison['exact_thresholds_checked']==threshold_count
            assert comparison['source_sha256']==sha(ROOT/'src'/source_name)
            for name,expected in comparison['source_dependencies'].items():assert sha(ROOT/'src'/name)==expected
            for name,expected in comparison['dependencies'].items():assert sha(R/name)==expected
            deps += [sample_name]+list(comparison['dependencies'])
        sources += ['PreciseNonlinearProgressionVerifier.cs','ClippedNonlinearProgressionVerifier.cs',
                    'verify_precise_nonlinear_progression.py','verify_clipped_nonlinear_progression.py',
                    'derive_precise_nonlinear_progression.py','derive_clipped_nonlinear_progression.py']
    receipt={'status':'passed','kind':'nonlinear_block_restart_native_pair','map_id':MAP,
             'linear_coefficient_certified':False,'conditional_only':False,'verified_basin':str(X),
             'classes':len(data['classes']),'seeds':str(count),'producer':producer,'progression':progression,
             'progression_source':progression_source,
             'exact_thresholds_checked':2032128 if clipped else targets,'python_sample_classes':112 if clipped else 100,'full_python_proof':False,
             'source_sha256':sha(Path(__file__)),
             'source_dependencies':{name:sha(ROOT/'src'/name) for name in sources},
             'dependencies':{name:sha(R/name) for name in sorted(set(deps))}}
    if write:
        (R/'nonlinear-capacity-proof-pair-audit.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print('PASSED nonlinear proof pair:',len(data['classes']),'classes',count,'seeds',flush=True)
    return receipt

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--producer',default='nonlinear-J41-full')
    parser.add_argument('--progression',default='nonlinear-progression-full')
    parser.add_argument('--progression-source',default='NonlinearProgressionCapacityVerifier.cs')
    args=parser.parse_args();audit(args.producer,args.progression,progression_source=args.progression_source)
