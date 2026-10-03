"""Replay frozen and revision evidence in manifest-only temporary copies.

No Lean compiler and no billion-node search is run by this script. Windows
is needed for byte-identical historical receipts. It never copies .lake or
rewrites the frozen evidence in the working tree.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = 'reference-m100-full-20261002'
WIDE = 'wide-m100-fourth-power-J38-grafted-release'
CONFIG = 'fourth-power-J38-grafted-config-m100-lo1-hi15.json'
EVIDENCE = ROOT / 'evidence/revision-20261002'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def run(root, script, *args):
    result = subprocess.run([sys.executable, '-X', 'utf8', str(root / script), *args],
                            cwd=root, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(script + '\n' + result.stdout + result.stderr)
    print(result.stdout.strip(), flush=True)


def archive_copy(destination):
    manifest = read(ROOT / 'MANIFEST.json')
    for name in ['MANIFEST.json', *manifest['files']]:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audits', action='store_true', help='Replay all seven frozen audits.')
    parser.add_argument('--record-m100', action='store_true', help='Write new m=100 revision receipts after successful checks.')
    parser.add_argument('--m100', action='store_true', help='Reproduce and compare the saved revision receipts.')
    parser.add_argument('--small-tests', action='store_true', help='Regenerate direct-iteration cases and run both kernels, arithmetic and interval tests.')
    parser.add_argument('--record-small-tests', action='store_true', help='Run and save the small test receipts in revision evidence.')
    args = parser.parse_args()
    run(ROOT, 'verify_bundle.py')
    with tempfile.TemporaryDirectory(prefix='collatz-revision-') as directory:
        copy = Path(directory) / 'review'
        archive_copy(copy)
        if args.audits:
            run(copy, 'verify_bundle.py', '--audits')
        if args.small_tests or args.record_small_tests:
            run(copy, 'src/build_native_tests.py')
            run(copy, 'src/build_singleton_tests.py')
            run(copy, 'src/test_exact_tools.py')
            for script in ('test_native.ps1', 'test_kernel128.ps1', 'test_singletons.ps1', 'test_wide.ps1'):
                result = subprocess.run(['pwsh', '-NoProfile', '-File', str(copy / 'src' / script)],
                                        cwd=copy, capture_output=True, text=True, encoding='utf-8')
                if result.returncode:
                    raise RuntimeError(script + '\n' + result.stdout + result.stderr)
                print(script, result.stdout.strip(), flush=True)
            for name in ('native-test-receipt.json', 'kernel128-test-receipt.json',
                         'singleton-test-receipt.json', 'wide-arithmetic-test.json', 'exact-tools-check.json'):
                source = copy / 'results' / name
                if read(source)['status'] != 'passed':
                    raise AssertionError('Small test not passed: ' + name)
                if args.record_small_tests:
                    EVIDENCE.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, EVIDENCE / name)
        if args.record_m100 or args.m100:
            suffixes = ('-result.json', '-metadata.json', '-audit.json', '-generator-audit.json',
                        '-partition-audit.json', '-journal.jsonl')
            for suffix in suffixes:
                source = ROOT / 'results' / (REFERENCE + suffix)
                shutil.copyfile(source, copy / 'results' / source.name)
            r = copy / 'results'
            for suffix in ('-audit.json', '-generator-audit.json', '-partition-audit.json'):
                if read(r / (REFERENCE + suffix))['status'] != 'passed':
                    raise AssertionError('Unpassed reference audit: ' + suffix)
            metadata = read(r / (REFERENCE + '-metadata.json'))
            if metadata['sourceHash'].lower() != sha(copy / 'src/PrefixKernel.cs'):
                raise AssertionError('Reference kernel hash mismatch')
            if metadata['configHash'].lower() != sha(r / CONFIG):
                raise AssertionError('Configuration hash mismatch')
            sys.path.insert(0, str(copy / 'src'))
            spec = importlib.util.spec_from_file_location('fresh_full_reference', copy / 'src/audit_full_reference.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.compare(WIDE, REFERENCE)
            run(copy, 'src/audit_fourth_power_grafted_exclusion.py', '--m', '100', '--label', WIDE, '--config', CONFIG)
            names = [WIDE + '-full-reference-audit.json', 'cycle-exclusion-m100-fourth-power-grafted-audit.json']
            for name in names:
                receipt = read(r / name)
                if receipt['status'] != 'passed':
                    raise AssertionError(name)
                if name.startswith('cycle-') and receipt['full_original_reference'] != 'complete counter-for-counter original-arithmetic repeat':
                    raise AssertionError('Full repeat was not included')
                if args.record_m100:
                    EVIDENCE.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(r / name, EVIDENCE / name)
                else:
                    if sha(r / name) != sha(EVIDENCE / name):
                        raise AssertionError('Revision receipt mismatch: ' + name)
                print('REVISION VERIFIED', name, flush=True)
    print('Complete: frozen archive preserved; no mathematical endorsement implied.', flush=True)


if __name__ == '__main__':
    main()
