"""Build a compact self-contained review package, excluding third-party papers."""
from pathlib import Path
import datetime,hashlib,json,shutil,zipfile

ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT.parents[1]/'work'/'analytic-review-bundle-stage'
STAGE.mkdir(parents=True,exist_ok=True)
files=['two-regime-review-manuscript.md','collatz-two-regime-growth-review.pdf',
       'two-regime-interpolation-bound.md','cycle-bound-corollaries.md',
       'block-restart-capacity.md','majorization-lemma.md','global-growth-and-cycle-bound.md',
       'src/exact_intervals.py','src/audit_two_regime_bound.py',
       'src/audit_cycle_bound_corollaries.py','src/audit_two_regime_review_constants.py',
       'results/two-regime-exponential-bound-audit.json',
       'results/cycle-bound-corollaries-audit.json','results/two-regime-review-constants-audit.json',
       'results/two-regime-review-pdf-qa.json','results/interpolation-primary-source-provenance.json']
files += [p.relative_to(ROOT).as_posix() for p in (ROOT/'formal').iterdir() if p.is_file()]
for name in files:
    dst=STAGE/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dst)
shutil.copyfile(ROOT/'src/verify_analytic_bundle.py',STAGE/'verify_bundle.py')
readme='''# Collatz block-growth research: review package

Prepared for Luke Baer with Codex, 29 September 2026.

Start with `collatz-two-regime-growth-review.pdf` (six pages). The matching
Markdown manuscript is included. This is a private mathematical draft seeking
independent review; novelty has not been confirmed and the Collatz conjecture
remains open.

The principal candidate theorem bounds maximal odd-run lengths along every
positive orbit by A*y0*lambda^t, where t counts odd/even blocks,
lambda=log2(3)-1/160 and A=(log2(3)/lambda)^26. It specializes Bugeaud's 1999
p-adic interpolation theorem and combines local losses through bounded
restarts. Since lambda>1, it does not establish convergence.

Using the cited published cycle-size bounds, the manuscript derives
K<1.37*m*lambda^m for 1024<=m<=515619 and K<19.15*m*lambda^m for m>=1024.
A precise version improves the cited 2010 uniform bound for 91<=m<=515619.
These comparisons do not establish priority against all later literature.

## What to review

1. Match every specialized hypothesis to Bugeaud (1999), Theorem 1, rational
   clause (6). The author-hosted version is linked in the manuscript.
2. Check the factorial normalization and the inequalities covering both
   parameter ranges for every integer J>=100, not just the sampled values.
3. Check the one- or two-block restart induction, including its intermediate
   run-length bound. Actual heights need not contract at every block.
4. Check the cycle conventions and imported Simons-de Weger range table.

The standalone frozen proof `two-regime-interpolation-bound.md` states a
narrower valid cycle range. `cycle-bound-corollaries.md` supplies the later
extension included in the PDF. Three background notes describe the abstract
restart, majorization, and earlier global-envelope work; their older constants
are historical and do not replace the principal theorem's constants.

## Reproduce the checks

Python 3.11 or newer is sufficient for the standard-library scripts:

    python verify_bundle.py
    python verify_bundle.py --numeric

The first command verifies all file hashes and the saved Lean receipts against
their sources and compiler logs. The second reruns three numerical audits in a
temporary copy and requires byte-for-byte agreement with the saved receipts.
It leaves this package unchanged and does not access the network.

To recompile all 71 supporting lemmas in 16 modules, obtain Lean 4.34.1 and a
mathlib checkout at commit d13f23b723b8a846827a245b89c10fc7d3f11612, initialize
its declared dependencies/cache, and run:

    python formal/verify_all_formal.py --mathlib PATH_TO_MATHLIB --lean-bin PATH_TO_LEAN_BIN

The original Lake project builds only four core modules; use the aggregate
verifier for all sixteen. It writes a fresh aggregate receipt. The separate
original receipts are preserved. No external proof service or AI model is used.
Only Lean's standard propext, Classical.choice, and Quot.sound axioms occur.

The formal files prove supporting statements, including some generic growth,
majorization, convexity, normalization, and parameter lemmas. They do not
formalize the published p-adic theorem, its complete Collatz specialization,
or convergence. Finite numerical challenges supplement the written universal
arguments and cannot replace them.

## Scope of this archive

This compact archive contains analytic proofs, exact checks, formal sources,
receipts, and review material. Large finite-search certificates for the separate
candidate exclusions of cycles with 96 through 99 local minima are maintained
in the research repository and are not part of this archive. Their validity is
not needed for the all-orbit theorem. Exploratory finite-capacity values in the
supplement are explicitly unproved as numerical certificates and are unused here.

Third-party papers, Lean binaries, mathlib, and caches are not redistributed.
The source-provenance record gives hashes of privately inspected papers; those
source files are intentionally absent. Follow the manuscript's primary links.
The SHA256 manifest detects accidental changes; it is not a digital signature
or independent mathematical endorsement.
'''
(STAGE/'START-HERE.md').write_text(readme,encoding='utf-8')
included=files+['verify_bundle.py','START-HERE.md']
manifest={'format_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope':'Analytic review bundle only; no finite-search certificate or proof of convergence.',
          'files':{name:{'bytes':(STAGE/name).stat().st_size,
                         'sha256':hashlib.sha256((STAGE/name).read_bytes()).hexdigest()}
                   for name in sorted(included)}}
(STAGE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
archive=ROOT/'collatz-analytic-review-bundle.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in sorted(included+['MANIFEST.json']):
        info=zipfile.ZipInfo(name,date_time=(2026,9,29,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,(STAGE/name).read_bytes())
receipt={'archive':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
         'bytes':archive.stat().st_size,'files':len(included)+1,
         'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'manifest_sha256':hashlib.sha256((STAGE/'MANIFEST.json').read_bytes()).hexdigest(),
         'scope':manifest['scope']}
(ROOT/'results/analytic-review-bundle-build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt),flush=True)
