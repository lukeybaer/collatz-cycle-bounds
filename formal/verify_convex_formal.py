"""Compile the formal core and preserve a checked, source-bound receipt.

Requires the pinned Lean runtime and an initialized mathlib checkout.
This does not download dependencies or invoke any external proof service.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess

HERE = Path(__file__).resolve().parent
REV = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
MODULES = {'CollatzConvexCost': ['weighted_prefix_bound', 'convex_sum_from_tangents', 'supporting_tangent', 'differentiable_convex_majorization']}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mathlib', type=Path, required=True)
    p.add_argument('--lean-bin', type=Path, required=True)
    args = p.parse_args()
    env = dict(os.environ)
    env['PATH'] = str(args.lean_bin.resolve()) + os.pathsep + env['PATH']
    suffix = '.exe' if os.name == 'nt' else ''
    lean = args.lean_bin / ('lean' + suffix)
    lake = args.lean_bin / ('lake' + suffix)
    version = subprocess.check_output([str(lean), '--version'], text=True, env=env).strip()
    assert 'version 4.34.1,' in version, version
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.mathlib, text=True).strip()
    assert revision == REV, revision
    checks = []
    for module, names in MODULES.items():
        source = HERE / (module + '.lean')
        code = source.read_text(encoding='utf-8-sig')
        assert not re.search(r'\b(sorry|admit|unsafe|axiom)\b', code)
        run = subprocess.run([str(lake), 'env', 'lean', str(source)], cwd=args.mathlib,
                             env=env, text=True, capture_output=True)
        output = run.stdout + run.stderr
        log = HERE / (module + '-compiler-output.txt')
        log.write_text(output, encoding='utf-8')
        assert run.returncode == 0, output
        assert 'warning:' not in output and 'error:' not in output, output
        expected = [f"'{module}.{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
                    for name in names]
        assert sorted(output.strip().splitlines()) == sorted(expected), output
        checks.append({'module': module, 'theorems': names, 'exit_code': run.returncode,
                       'source_sha256': sha(source), 'compiler_output_sha256': sha(log),
                       'axioms': ['propext', 'Classical.choice', 'Quot.sound']})
        print('PASSED', module, flush=True)
    receipt = {'status': 'passed', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'lean_version': version, 'mathlib_commit': revision, 'checks': checks,
               'scope': 'Four weighted-prefix and differentiable convex majorization lemmas. Not a formalization of Collatz convergence, the p-adic theorem, or the numerical exclusions.',
               'verifier_sha256': sha(Path(__file__)),
               'toolchain_sha256': sha(HERE / 'lean-toolchain'),
               'lakefile_sha256': sha(HERE / 'lakefile.toml')}
    (HERE / 'convex-cost-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('All four convex-cost lemmas checked without proof placeholders.', flush=True)

if __name__ == '__main__':
    main()
