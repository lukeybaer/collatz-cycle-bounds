"""Build a source-bound archive of completed finite and analytic evidence."""
from pathlib import Path
import datetime,hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT.parents[1]/'work/finite-review-bundle-stage';STAGE.mkdir(parents=True,exist_ok=True)
plan=json.loads((ROOT/'results/finite-review-bundle-plan.json').read_text(encoding='utf-8'))
assert not plan['unresolved_file_like_references']
files=set(plan['files'])
for folder in ('src','formal'):
    files.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).iterdir() if p.is_file())
files.update(['manuscript-draft.md','sources.md','nonlinear-envelope-lemma.md',
              'majorization-lemma.md','subordinate-height-envelope.md','block-restart-capacity.md',
              'fourth-power-review-manuscript.md','collatz-fourth-power-growth-review.pdf',
              'four-range-interpolation-bound.md','optimized-global-cutoffs.md'])
for name in sorted(files):
    p=ROOT/name;dest=STAGE/name;dest.parent.mkdir(parents=True,exist_ok=True)
    if name in plan['files']:assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['files'][name]['sha256'],name
    shutil.copyfile(p,dest)
shutil.copyfile(ROOT/'src/verify_finite_bundle.py',STAGE/'verify_bundle.py')
readme='''# Collatz research: completed computational evidence

Prepared for Luke Baer with Codex, 29 September 2026. Private research draft.

This archive contains internally checked candidate exclusions for exactly
92 through100 local minima, and the analytic four-range block-growth bound
with lambda=log2(3)-1/83, approximately1.572914307950072. The92--95 cases
were previously known; the96--100 cases are candidate extensions pending
independent mathematical review and a complete priority check. Collatz remains
open. A local minimum is a maximal odd/even block start, not an odd iterate.

## Read first

`manuscript-draft.md` explains the cycle method and historical searches.
`collatz-fourth-power-growth-review.pdf` is the self-contained seven-page
analytic argument with epsilon1/93, used by the finite certificate. The newer
`four-range-interpolation-bound.md` improves the asymptotic base to epsilon1/83;
it is not needed by the finite exclusions in this archive. Named proof notes
and the source register retain all mathematical dependencies and caveats.

The compact proof chain in this archive is:

*92--95: four exact factor-one profile contradictions, checked forward.
*96--98: three exact factor-one profile contradictions, checked forward.
*99: the epsilon1/160 graft with a complete2,758,731,446-node window search.
  Its full original BigInteger repeat agrees on every substantive counter.
*100: the epsilon1/93 graft with a complete14,528,184,145-node window search.
  Its single fallback job is fully repeated with the original arithmetic.
  A full original-arithmetic repeat is separate ongoing work and is not claimed
  by this snapshot unless its completed receipt appears in the manifest.

The first two lines still depend on completed finite-capacity proofs; they
avoid additional searches over the possible least cycle member. All cases
depend on the published convergence basin below2^71, the cited p-adic theorem,
and the precisely scoped Simons--de Weger cycle-size bounds. Combining these
cases with Hercher's published exclusion through91 gives the candidate result
through100. No claim of convergence for every positive orbit follows.

## Recheck the archive

Use Python3.11 or newer, with its standard library:

    python verify_bundle.py
    python verify_bundle.py --audits

The first checks file hashes and saved source-bound formal receipts. The
second reruns four complete dependency/profile/journal audits plus two new
analytic constant audits in a temporary copy, requiring byte-identical receipts.
Neither command accesses the network or invokes an AI model. They do not
recompute billions of search nodes. They check complete stored certificates
and their exact logical connections; source and mathematical review remain
necessary. The SHA256 manifest detects changes, not correctness by itself.

To repeat the m100 search itself on PowerShell7/.NET10, use a fresh label:

    pwsh -File src/run_reference_release.ps1 -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json -Workers8 -Split1 -NodeLimit100000000000 -Label fresh-m100

Insert spaces between each switch and its numeric value, for example
`-Workers 8 -Split 1 -NodeLimit 100000000000`. The compact line above is a
readable template, not a claim of cross-platform testing. Prefer the exact
command in `REPRODUCE.ps1`. It writes new result files and preserves the saved
certificates. This can take hours. The two independent capacity proof programs
and their full class receipts are included; their regeneration is also costly.

All93 supporting Lean lemmas in20 modules have passed Lean4.34.1 with mathlib
commit d13f23b723b8a846827a245b89c10fc7d3f11612. To recompile them, install
those pinned dependencies and use `formal/verify_all_formal.py`, with its
`--mathlib` and `--lean-bin` arguments. The complete external p-adic theorem,
Collatz specialization and search programs are not formalized.

The included source folder also contains historical and exploratory utilities.
Only the named reproduction paths and manifest-rooted completed receipts are
asserted self-contained. Running experiments elsewhere in that folder may need
data outside this archive. No running journal, third-party paper, Lean binary,
mathlib checkout or cache is distributed here.
'''
readme=readme.replace('*92','* 92').replace('*96','* 96').replace('*99','* 99').replace('*100','* 100')
# Keep the runnable command exact; do not ship a deliberately compact shell example.
start=readme.index('    pwsh -File');end=readme.index('This can take hours.',start)
readme=readme[:start]+'''    pwsh -File src/run_reference_release.ps1 -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json -Workers 8 -Split 1 -NodeLimit 100000000000 -Label fresh-m100

The same command is saved in `REPRODUCE.ps1`. It writes new result files and
preserves the saved certificates. '''+readme[end:]
(STAGE/'START-HERE.md').write_text(readme,encoding='utf-8')
(STAGE/'REPRODUCE.ps1').write_text("$ErrorActionPreference='Stop'\nPush-Location $PSScriptRoot\ntry {\n    ./src/run_reference_release.ps1 -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json -Workers 8 -Split 1 -NodeLimit 100000000000 -Label fresh-m100\n} finally { Pop-Location }\n",encoding='utf-8')
files.update(('START-HERE.md','REPRODUCE.ps1','verify_bundle.py'))
manifest={'format_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'roots':plan['roots'],'scope':'Completed candidate exclusions92..100 and analytic checks. External review and priority unconfirmed.',
          'files':{n:{'bytes':(STAGE/n).stat().st_size,'sha256':hashlib.sha256((STAGE/n).read_bytes()).hexdigest()} for n in sorted(files)}}
(STAGE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
archive=ROOT/'collatz-finite-review-bundle.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in sorted(files|{'MANIFEST.json'}):
        info=zipfile.ZipInfo(name,date_time=(2026,9,29,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,(STAGE/name).read_bytes())
out={'archive':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
     'bytes':archive.stat().st_size,'files':len(files)+1,
     'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'manifest_sha256':hashlib.sha256((STAGE/'MANIFEST.json').read_bytes()).hexdigest(),
     'scope':manifest['scope']}
(ROOT/'results/finite-review-bundle-build.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out),flush=True)
