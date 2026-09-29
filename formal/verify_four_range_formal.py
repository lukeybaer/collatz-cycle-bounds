"""Compile the formal core and preserve a checked, source-bound receipt.

Requires the pinned Lean runtime and an initialized mathlib checkout.
This does not download dependencies or invoke any external proof service.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess

HERE = Path(__file__).resolve().parent
REV = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
MODULES = {'CollatzFourRange': ['first_margin','second_margin','third_margin','fourth_margin','numeric_gaps','local_loss','ratio_decreases','restart_constants']}


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
                             env=env, text=True, encoding="utf-8", capture_output=True)
        output = run.stdout + run.stderr
        log = HERE / (module + '-compiler-output.txt')
        log.write_text(output, encoding='utf-8')
        assert run.returncode == 0, output
        assert 'warning:' not in output and 'error:' not in output, output
        reports = {}
        for line in output.strip().splitlines():
            match = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line)
            assert match, line
            axioms = [x.strip() for x in match[2].split(',') if x.strip()]
            assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}, axioms
            reports[match[1]] = axioms
        assert set(reports) == {f'{module}.{name}' for name in names}
        checks.append({'module': module, 'theorems': names, 'exit_code': run.returncode,
                       'source_sha256': sha(source), 'compiler_output_sha256': sha(log),
                       'axioms_by_theorem': reports})
        print('PASSED', module, flush=True)
    receipt = {'status': 'passed', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'lean_version': version, 'mathlib_commit': revision, 'checks': checks,
               'scope': 'Eight supporting four-range parameter, local-loss, monotonic-ratio and restart lemmas. Not a formalization of Collatz convergence, the p-adic theorem, or the numerical exclusions.',
               'verifier_sha256': sha(Path(__file__)),
               'toolchain_sha256': sha(HERE / 'lean-toolchain'),
               'lakefile_sha256': sha(HERE / 'lakefile.toml')}
    (HERE / 'four-range-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('All eight four-range lemmas checked without proof placeholders.', flush=True)

if __name__ == '__main__':
    main()
