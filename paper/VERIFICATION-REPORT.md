# Verification report — review revision

This report separates a written proof claim, computer checks of finite evidence, and Lean's formal scope. A result marked passed applies only to the named check.

| Claim or component | Evidence | Boundary |
|---|---|---|
| Block construction, actual iteration and elementary heights | `Blocks.lean`, `Dynamics.lean`, `Construction.lean`: every positive odd integer has a block orbit whose starts are actual shortcut iterates | This proves the represented dynamics, not the missing analytic certificate. |
| Headline growth envelope from local loss | `Collatz.odd_start_growth` in `proof/Collatz/Connected.lean`; successful local Lean build | `LocalLossCertificate` is an explicit input, not a proved instance. |
| Local analytic certificate | Written manuscript, published Bugeaud criterion, exact rational margin auditor | Full specialization and external theorem are not formalized or independently reviewed. |
| Cycle constants | Written deductions using Simons–de Weger and exact analytic auditors | Imported cycle statements and their entire composition are outside the connected Lean theorem. |
| Finite cases 92–100 | Four end-to-end exclusion audits bind maps, profiles, windows, partitions and journals | Correctness of the mathematical reduction remains a review obligation; Barina's floor is external. |
| Full m=100 arithmetic repeat | Original BigInteger run `reference-m100-full-20261002` | **Running at the initial revision commit.** Completion is not assumed. |
| Priority | [Dated primary-source comparisons](NOVELTY-REVIEW.md) | No matching statement found is not proof that none exists. |

## Routine reproduction

From the repository root on Windows with Python 3.11+ and PowerShell 7:

```sh
python scripts/verify_revision.py --audits
python scripts/verify_revision.py --small-tests
```

The first verifies the 428-file frozen manifest and saved 103-lemma compilation records, then reruns seven certificate audits in minimal temporary copies and requires byte-identical receipts. It does not invoke Lean or rerun large searches. The temporary-copy wrapper avoids copying `.lake` and preserves every frozen receipt.

The small tests regenerate expected cases by Python direct shortcut iteration. They compare the BigInteger and UInt128 searches, exercise singleton overflow fallback, test wide arithmetic, and validate rational intervals and prefix coverage on small instances. Fresh receipts are saved separately in `evidence/revision-20261002/` when run with `--record-small-tests`.

## Lean reproduction

```sh
lake exe cache get
python scripts/build_lean.py
lake build
```

The root project pins Lean 4.34.1 and mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. The helper serializes the legacy targets to limit memory, then builds the root normally. All 21 historical modules and the new connected modules are imported. Guarded axiom outputs allow `propext`, `Classical.choice`, and `Quot.sound`. The checked top-level type still contains its analytic hypothesis; absence of extra axioms does not remove that hypothesis.

The local root build succeeded on 3 October 2026 UTC. GitHub CI supplies a separate-machine Linux build. This is compiler reproduction, not an independent mathematician's assessment.

## Full m=100 original-arithmetic repeat

The run uses the unchanged `src/PrefixKernel.cs`, release compilation, eight workers, and split depth 1, giving 956 dispatched jobs. The fixed-width run used 231,505 jobs. Different partitions are intentional: total nodes must be normalized by subtracting dispatched split roots.

```powershell
pwsh -NoProfile -File src/run_reference_release.ps1 `
  -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json `
  -Workers 8 -Split 1 -NodeLimit 100000000000 `
  -Label reference-m100-full-20261002
python src/audit_journal.py results/reference-m100-full-20261002-journal.jsonl
pwsh -NoProfile -File src/audit_generator.ps1 `
  -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json `
  -Split 1 -Label reference-m100-full-20261002
pwsh -NoProfile -File src/audit_reference_partition.ps1 `
  -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json `
  -Split 1 -Label reference-m100-full-20261002
python scripts/verify_revision.py --record-m100
```

Check the JSON statuses; a process exit alone is not sufficient. `--record-m100` requires passed coverage, generator and partition receipts, a complete zero-survivor result, agreement of all seven terminal counters and normalized nodes, and a fresh end-to-end m=100 audit incorporating the reference run. It writes new receipts under `evidence/revision-20261002/`, without replacing the archival audit.

After the revision receipts are recorded, replay them with:

```sh
python scripts/verify_revision.py --m100
```

The repeat tests arithmetic and partition/coverage consistency. Both implementations share the mathematical reduction and related search logic, so a common logical error can survive agreement. Independent scrutiny of the pruning invariants and external inputs remains necessary.

## Manuscript and preserved evidence

The current mathematical source is `paper/collatz-research-paper.tex`; the workflow compiles it and uploads the PDF and TeX log. Original root paper files and `formal/` remain byte-for-byte archival evidence. Current wrappers are outside the original manifest, and revision evidence is separately identified. No unfinished m=101 computation is used.
