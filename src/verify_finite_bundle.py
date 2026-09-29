"""Verify an extracted review archive without network or model access."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--audits',action='store_true',help='Rerun end-to-end receipt audits and the new analytic constant audit in a temporary copy; does not rerun the billion-node searches.')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
    for name,row in manifest['files'].items():
        p=ROOT/name
        assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],name
    formal=ROOT/'formal';aggregate=json.loads((formal/'aggregate-verification.json').read_text(encoding='utf-8'))
    assert aggregate['status']=='passed' and aggregate['theorem_count']==93 and aggregate['module_count']==20
    assert aggregate['source_sha256']==sha(formal/'verify_all_formal.py')
    for name,digest in aggregate['receipt_sha256'].items():
        assert sha(formal/name)==digest
        receipt=json.loads((formal/name).read_text(encoding='utf-8'))
        for row in receipt['checks']:
            assert sha(formal/(row['module']+'.lean'))==row['source_sha256']
            assert sha(formal/(row['module']+'-compiler-output.txt'))==row['compiler_output_sha256']
    print('PASSED',len(manifest['files']),'manifest entries and saved93-lemma formal receipts.',flush=True)
    if args.audits:
        commands=[
          ('audit_early_fourth_power_exclusions.py',[], 'cycle-exclusions-m92-m95-fourth-power-direct-audit.json'),
          ('audit_fourth_power_direct_exclusions.py',[], 'cycle-exclusions-m96-m98-fourth-power-direct-audit.json'),
          ('audit_two_regime_grafted_exclusion.py',['--m','99','--label','wide-m99-two-regime-grafted-release','--config','two-regime-grafted-config-m99-lo1-hi11.json'], 'cycle-exclusion-m99-two-regime-grafted-audit.json'),
          ('audit_fourth_power_grafted_exclusion.py',['--m','100','--label','wide-m100-fourth-power-J38-grafted-release','--config','fourth-power-J38-grafted-config-m100-lo1-hi15.json'], 'cycle-exclusion-m100-fourth-power-grafted-audit.json'),
          ('audit_four_range_bound.py',[], 'four-range-exponential-bound-audit.json'),
          ('audit_optimized_cutoffs.py',[], 'optimized-global-cutoffs-audit.json')]
        with tempfile.TemporaryDirectory(prefix='collatz-finite-review-') as tmp:
            copy=Path(tmp)/'review';shutil.copytree(ROOT,copy)
            for script,extra,result in commands:
                expected=sha(copy/'results'/result)
                run=subprocess.run([sys.executable,'-X','utf8',str(copy/'src'/script),*extra],cwd=copy,text=True,encoding='utf-8',capture_output=True)
                assert run.returncode==0,script+'\n'+run.stdout+run.stderr
                assert sha(copy/'results'/result)==expected,'Receipt mismatch: '+result
                print('REPRODUCED',result,'byte for byte',flush=True)
    print('No convergence proof, priority confirmation or external mathematical review is implied.',flush=True)
if __name__=='__main__':main()
