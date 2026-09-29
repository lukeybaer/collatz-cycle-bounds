"""Package completed evidence, the main paper and strongest analytic result."""
from pathlib import Path
import datetime,hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT.parents[1]/'work/research-review-bundle-stage';STAGE.mkdir(parents=True,exist_ok=True)
plan=json.loads((ROOT/'results/research-review-bundle-plan.json').read_text(encoding='utf-8'))
assert not plan['unresolved_file_like_references']
files=set(plan['files'])
for folder in ('src','formal'):
    files.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).iterdir() if p.is_file())
files.update(['collatz-paper.md','collatz-research-paper.pdf','paper-finite-results.md',
 'RESEARCH-SUMMARY.md','VERIFICATION-REPORT.md','sources.md','nonlinear-envelope-lemma.md',
 'majorization-lemma.md','subordinate-height-envelope.md','block-restart-capacity.md',
 'fourth-power-review-manuscript.md','collatz-fourth-power-growth-review.pdf',
 'four-range-interpolation-bound.md','optimized-global-cutoffs.md','retained-loss-interpolation-bound.md'])
for name in sorted(files):
    p=ROOT/name;dest=STAGE/name;dest.parent.mkdir(parents=True,exist_ok=True)
    if name in plan['files']:assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['files'][name]['sha256'],name
    shutil.copyfile(p,dest)
shutil.copyfile(ROOT/'src/verify_research_bundle.py',STAGE/'verify_bundle.py')
readme='''# Collatz research review package

Prepared for Luke Baer with OpenAI Codex, 29 September 2026.
Private research manuscript. Independent mathematical review and priority
confirmation are pending. The Collatz conjecture remains open.

## Start here

Read `RESEARCH-SUMMARY.md`, the 13-page `collatz-research-paper.pdf`, and
`VERIFICATION-REPORT.md`. The complete manuscript source is `collatz-paper.md`.

The two candidate contributions are an explicit all-orbit block-growth base
lambda=log2(3)-1/80 and internally checked exclusions through 100 local minima.
The finite proof uses earlier frozen analytic specializations, not an
unfinished stronger-map or m=101 experiment. The case m=100 has a complete
14,528,184,145-node search and all partition/journal/fallback audits; its full
original-arithmetic repeat remains additional ongoing work at this snapshot.
The m=99 original-arithmetic repeat is complete.

## Reproduce the saved evidence

Use Python 3.11 or newer and its standard library:

    python verify_bundle.py
    python verify_bundle.py --audits

The first verifies every manifest hash and the saved receipts for 103 selected
Lean lemmas in 21 modules. The second runs four end-to-end exclusion audits
and three analytic audits in a temporary copy, requiring byte-identical
receipts. It can take several minutes. Neither command accesses a network or
invokes an AI model. Neither silently claims to repeat billions of search nodes.

To repeat the entire m=100 search with original arbitrary-precision arithmetic
on PowerShell 7/.NET 10, from the extracted directory run:

    pwsh -File src/run_reference_release.ps1 -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json -Workers 8 -Split 1 -NodeLimit 100000000000 -Label fresh-m100

`REPRODUCE.ps1` contains that command. Use a fresh label to preserve evidence.
The computation can take hours. The complete finite-capacity class inputs,
both native implementations, independent checks and saved counters are also
included for inspection and more expensive regeneration.

The formal environment is pinned to Lean 4.34.1 and mathlib commit
`d13f23b723b8a846827a245b89c10fc7d3f11612`. With those dependencies installed,
run `formal/verify_all_formal.py` and `formal/verify_retained_loss_formal.py`,
each with `--mathlib` and `--lean-bin`. The first compiles the preserved
93-lemma baseline; the second compiles the ten retained-loss lemmas. The
external p-adic theorem and the entire search are not formally verified.

The paper builder requires ReportLab and the configured fonts. It is separate
from the standard-library mathematical auditors. No compiler binaries,
mathlib checkout, cache or third-party paper is redistributed.

## Scope

The SHA-256 manifest binds files; it does not establish their correctness.
Exact arithmetic, independent algorithms, written proofs and external inputs
must still be reviewed. Barina's published basin below 2^71 is an external
computational assumption, not a computation repeated in this package.

The source folder retains historical and exploratory utilities. Only the
named reproduction paths and manifest-rooted completed receipts are asserted
self-contained. Other experiments may require data outside this archive.
No active search journal is included. The paper explicitly compares with
Simons-de Weger, Hercher and Wang and does not claim a completed priority review.
'''
(STAGE/'START-HERE.md').write_text(readme,encoding='utf-8')
(STAGE/'REPRODUCE.ps1').write_text("$ErrorActionPreference='Stop'\nPush-Location $PSScriptRoot\ntry {\n    ./src/run_reference_release.ps1 -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json -Workers 8 -Split 1 -NodeLimit 100000000000 -Label fresh-m100\n} finally { Pop-Location }\n",encoding='utf-8')
files.update(('START-HERE.md','REPRODUCE.ps1','verify_bundle.py'))
manifest={'format_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'roots':plan['roots'],'scope':'Candidate exclusions92..100 and epsilon1/80 analytic bound; external review and priority unconfirmed.',
 'files':{n:{'bytes':(STAGE/n).stat().st_size,'sha256':hashlib.sha256((STAGE/n).read_bytes()).hexdigest()} for n in sorted(files)}}
(STAGE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
archive=ROOT/'collatz-research-review-bundle.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in sorted(files|{'MANIFEST.json'}):
        info=zipfile.ZipInfo(name,date_time=(2026,9,29,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,(STAGE/name).read_bytes())
out={'archive':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
 'bytes':archive.stat().st_size,'files':len(files)+1,'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'manifest_sha256':hashlib.sha256((STAGE/'MANIFEST.json').read_bytes()).hexdigest(),'scope':manifest['scope']}
(ROOT/'results/research-review-bundle-build.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out),flush=True)
