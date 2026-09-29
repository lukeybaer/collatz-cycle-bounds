"""Verify the extracted analytic review bundle; no network or model access."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parent
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--numeric',action='store_true',help='Rerun all three numerical audits in a temporary copy.')
    args=p.parse_args()
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
    for name,record in manifest['files'].items():
        path=ROOT/name
        assert path.is_file(),name
        assert path.stat().st_size==record['bytes'],name
        assert sha(path)==record['sha256'],name
    formal=ROOT/'formal'
    aggregate=json.loads((formal/'aggregate-verification.json').read_text(encoding='utf-8'))
    assert aggregate['status']=='passed' and aggregate['theorem_count']==71
    assert aggregate['module_count']==16
    assert aggregate['source_sha256']==sha(formal/'verify_all_formal.py')
    for name,digest in aggregate['receipt_sha256'].items():
        assert sha(formal/name)==digest,name
        receipt=json.loads((formal/name).read_text(encoding='utf-8'))
        for row in receipt['checks']:
            assert sha(formal/(row['module']+'.lean'))==row['source_sha256']
            assert sha(formal/(row['module']+'-compiler-output.txt'))==row['compiler_output_sha256']
    for row in aggregate['checks']:
        assert sha(formal/(row['module']+'.lean'))==row['source_sha256']
        assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in row['axioms_by_theorem'].values())
    print('PASSED bundle manifest and source-bound saved formal receipts:',len(manifest['files']),'files',flush=True)
    if args.numeric:
        with tempfile.TemporaryDirectory(prefix='collatz-review-check-') as tmp:
            copy=Path(tmp)/'review'
            shutil.copytree(ROOT,copy)
            for script,result in (
                ('audit_two_regime_bound.py','two-regime-exponential-bound-audit.json'),
                ('audit_cycle_bound_corollaries.py','cycle-bound-corollaries-audit.json'),
                ('audit_two_regime_review_constants.py','two-regime-review-constants-audit.json')):
                expected=sha(copy/'results'/result)
                run=subprocess.run([sys.executable,'-X','utf8',str(copy/'src'/script)],
                                   cwd=copy,text=True,encoding='utf-8',capture_output=True)
                assert run.returncode==0,run.stdout+run.stderr
                assert sha(copy/'results'/result)==expected,'Receipt mismatch: '+result
                print('REPRODUCED',result,'byte for byte',flush=True)
    print('These checks are supporting evidence, not a formalization of the p-adic theorem or full Collatz proof.',flush=True)

if __name__=='__main__':main()
