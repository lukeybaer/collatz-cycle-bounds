# Collatz cycle bounds: research and reproduction code

Research by Luke Baer and Amy, an AI research system operating through OpenAI Codex.

This repository accompanies *Explicit block-growth bounds and finite-cycle exclusions for the 3n+1 problem*. It contains a written argument, exact certificates and a **partial, conditional formalization**. Independent mathematical review and confirmation of novelty are pending. Collatz remains unsolved.

## Read the work

- [LaTeX manuscript](paper/collatz-research-paper.tex) and [PDF](paper/collatz-research-paper.pdf).
- [Results and limits](paper/RESEARCH-SUMMARY.md).
- [Claim-to-evidence and reproduction guide](paper/VERIFICATION-REPORT.md).
- [Expanded priority review, sources and search limitations](paper/NOVELTY-REVIEW.md).
- [Revision notes and correction to the archived text](paper/REVISION-NOTES.md).
- [Active Lean project and its exact formal boundary](proof/README.md).
- [Research implementations](src/) and [saved certificates and journals](results/).

The written analytic claim uses `lambda = log2(3) - 1/80`. At 1,024 local minima its displayed odd-step upper bound is about 3,049 times smaller than the applicable explicit bound in Simons–de Weger, version 1.44. This compares two upper bounds; it is not a runtime speedup. The finite claim covers 92–100 local minima using separate, earlier frozen analytic specializations. Relative to Wang's located preprint through 95, the additional candidate cases are 96–100.

## What the Lean build establishes

`Collatz.odd_start_growth` starts from any positive odd integer, constructs its block orbit, identifies its block starts with actual shortcut Collatz iterates, and connects elementary height bounds, rounding, restart induction and the finite warmup to the two headline growth inequalities. Its `LocalLossCertificate` is an **explicit hypothesis**. The written specialization of Bugeaud's external theorem is not fully formalized. A passing axiom guard does not discharge a theorem's hypotheses.

```sh
lake exe cache get
python scripts/build_lean.py
lake build
```

Lean 4.34.1 and mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612` are pinned. The helper builds legacy modules sequentially to bound memory, then invokes the normal root `lake build`. CI builds this project on Linux. All 21 legacy modules and the connected theorem have guarded axiom reports. See [proof/README.md](proof/README.md) before interpreting a successful build as mathematical evidence.

## Reproduce arithmetic evidence

Python 3.11+ is sufficient for the certificate auditors. Windows is required for byte-identical historical receipts; the small native tests also use PowerShell 7. No AI service or API key is needed.

```sh
python scripts/verify_revision.py --audits
python scripts/verify_revision.py --small-tests
```

The first checks all 428 frozen manifest entries and replays seven saved audits in a minimal temporary copy. It does not copy the Lean dependency cache or modify the archived receipts. The second regenerates Python direct-iteration cases and compares both native kernels, exercises overflow fallback, and checks exact interval/prefix tools.

The full `m=100` BigInteger reference rerun is being completed as part of this revision. Its final status and reproduction commands are recorded in the [verification report](paper/VERIFICATION-REPORT.md). The routine audits do not repeat the billion-node searches or Barina's external convergence computation.

## Preservation and review

`MANIFEST.json` binds the unchanged 29 September research snapshot, including historical wording and compiler records. Current publication files are in `paper/`, the active Lean project is in `proof/`, and new receipts go in `evidence/revision-20261002/`. The old root manuscript and `formal/` are archival. Code in `src/` includes exploratory utilities as well as the named reproduction paths.

Please open an issue with a precise statement, source reference or reproducible countercalculation. Public availability, passing CI and agreement between programs do not constitute peer review. The work builds on Simons–de Weger, Hercher (including his corrigendum), Wang, Bugeaud, Luca, Brox and Barina; no endorsement is claimed.
