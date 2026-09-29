"""Recompile every accepted module without rewriting frozen proof receipts.

No downloads, external search tactics, model calls, or remote proof services.
Uses the explicitly supplied pinned local Lean and mathlib installations.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, datetime, hashlib, json, os, re, subprocess

HERE = Path(__file__).resolve().parent
REV = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
RECEIPTS = (
    'core-verification-v1.json', 'sharper-constants-verification.json',
    'global-envelope-verification.json', 'convex-cost-verification.json',
    'independent-constants-verification.json', 'dependent-valuation-verification.json',
    'reciprocal-cost-verification.json', 'cyclic-envelope-verification.json',
    'parity-constants-verification.json', 'common-cap-verification.json',
    'signed-normalization-verification.json',
    'interpolation-parameters-verification.json', 'two-regime-parameters-verification.json',
    'third-range-verification.json','fourth-power-verification.json',
    'four-range-verification.json',
)
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mathlib', type=Path, required=True)
    parser.add_argument('--lean-bin', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=2, choices=(1, 2))
    args = parser.parse_args()
    env = dict(os.environ)
    env['PATH'] = str(args.lean_bin.resolve()) + os.pathsep + env['PATH']
    suffix = '.exe' if os.name == 'nt' else ''
    lean = args.lean_bin / ('lean' + suffix)
    lake = args.lean_bin / ('lake' + suffix)
    version = subprocess.check_output([str(lean), '--version'], text=True, encoding='utf-8', env=env).strip()
    assert 'version 4.34.1,' in version
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.mathlib, text=True).strip()
    assert revision == REV
    subprocess.run(['git', 'diff', '--exit-code', 'HEAD', '--', 'Mathlib'], cwd=args.mathlib, check=True)
    modules = {}
    hashes = {}
    for name in RECEIPTS:
        path = HERE/name
        record = json.loads(path.read_text(encoding='utf-8'))
        assert record['status'] == 'passed' and record['mathlib_commit'] == REV
        hashes[name] = sha(path)
        for row in record['checks']:
            module = row['module']
            assert module not in modules
            source = HERE/(module+'.lean')
            assert sha(source) == row['source_sha256']
            assert sha(HERE/(module+'-compiler-output.txt')) == row['compiler_output_sha256']
            assert not re.search(r'\b(sorry|admit|unsafe|axiom)\b', source.read_text(encoding='utf-8'))
            modules[module] = row

    def compile_one(item):
        module, saved = item
        source = HERE/(module+'.lean')
        run = subprocess.run([str(lake), 'env', 'lean', str(source)], cwd=args.mathlib,
                             env=env, text=True, encoding='utf-8', capture_output=True)
        output = run.stdout + run.stderr
        assert run.returncode == 0, output
        reports = {}
        for line in output.strip().splitlines():
            match = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line)
            assert match, line
            assert match[1] not in reports
            axioms = [x.strip() for x in match[2].split(',') if x.strip()]
            assert set(axioms) <= ALLOWED_AXIOMS
            reports[match[1]] = axioms
        assert set(reports) == {module+'.'+name for name in saved['theorems']}
        assert sha(source) == saved['source_sha256']
        return {'module': module, 'source_sha256': sha(source), 'axioms_by_theorem': reports,
                'compiler_output': output, 'exit_code': run.returncode}

    checked = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        jobs = [executor.submit(compile_one, item) for item in modules.items()]
        for future in as_completed(jobs):
            row = future.result()
            checked.append(row)
            print('RECHECKED', row['module'], len(row['axioms_by_theorem']), flush=True)
    assert hashes == {name: sha(HERE/name) for name in RECEIPTS}
    count = sum(len(row['axioms_by_theorem']) for row in checked)
    result = {'status': 'passed', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'theorem_count': count, 'module_count': len(checked), 'lean_version': version,
              'mathlib_commit': revision, 'receipt_sha256': hashes,
              'checks': sorted(checked, key=lambda x: x['module']),
              'source_sha256': sha(Path(__file__)),
              'scope': 'Accepted supporting lemmas only. Does not formalize the complete Collatz application, the external p-adic theorem, or finite-search programs.'}
    (HERE/'aggregate-verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('PASSED aggregate formal recheck:', count, 'theorems;', len(checked), 'modules', flush=True)

if __name__ == '__main__':
    main()
