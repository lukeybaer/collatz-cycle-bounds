# Collatz cycle bounds: research and reproduction code

Research by Luke Baer and Amy, an AI research system operating through OpenAI Codex.

This repository contains the code and evidence accompanying *Explicit block-growth bounds and finite-cycle exclusions for the 3n+1 problem*. The manuscript presents candidate analytic bounds and finite-cycle exclusions. Independent mathematical review and confirmation of novelty are pending. The Collatz conjecture remains unsolved.

## Read the work

- [Paper, with authorship and AI-contribution disclosure](paper/collatz-research-paper.pdf)
- [Paper source](paper/collatz-paper.md)
- [Results, comparison with prior work and limitations](paper/RESEARCH-SUMMARY.md)
- [Claim-to-evidence verification report](paper/VERIFICATION-REPORT.md)
- [Python and C# research source](src/)
- [Lean source and compilation records](formal/)
- [Saved configurations, certificates and search journals](results/)

The analytic manuscript gives the block-growth base `lambda = log2(3) - 1/80`. Its displayed odd-step upper bound at 1,024 local minima is about 3,049 times smaller than the cited explicit bound. This is a ratio of mathematical upper bounds. The finite certificates cover local-minimum cases 92 through 100, using the external inputs described in the paper. These claims require specialist scrutiny of the deductions and their assumptions.

## Reproduce the saved evidence

Clone the repository, enter its directory, and use Python 3.11 or newer. The following checks use only the standard library; no AI service or API key is needed.

```sh
git clone https://github.com/lukeybaer/collatz-cycle-bounds.git
cd collatz-cycle-bounds
python verify_bundle.py
python verify_bundle.py --audits
```

The first command verifies the 428 manifest entries and the preserved receipts for 103 selected Lean lemmas in 21 modules. It checks the saved compilation records; it does not invoke Lean. The second reruns four end-to-end exclusion audits and three analytic audits in a temporary copy, requiring byte-identical output receipts. Allow several minutes.

These audits examine the supplied search evidence. They do not repeat the multi-billion-node searches. [START-HERE.md](START-HERE.md) describes how to rerun the full original-arithmetic search and recompile the Lean modules. The complete `m = 100` original-arithmetic repeat was still pending at the research snapshot. The entire paper, external p-adic theorem and finite search are not formally verified.

## Snapshot and provenance

The manifest-bound files at the repository root preserve the 29 September 2026 research snapshot byte for byte. Historical wording such as “private research manuscript” in those files describes the snapshot before this public release. The current author-disclosed paper is in `paper/`; the root PDF is retained as archival evidence. The mathematical content was unchanged by the authorship revision.

`MANIFEST.json` binds the original research files. README, GitHub workflow, citation metadata, and the `paper/` copies are publication wrappers outside that original manifest. The source folder contains exploratory utilities as well as the named reproduction paths; not every historical experiment is self-contained.

The Lean environment is pinned to Lean 4.34.1 and mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. See [formal/README.md](formal/README.md) and the aggregate verification scripts for compilation scope. Paper rendering uses ReportLab and configured Windows fonts, separately from the standard-library mathematical auditors.

## Review and corrections

Please open an issue with a precise claim, file or theorem reference, and a reproducible countercalculation where possible. Independent reproduction, scrutiny of the external inputs, and comparison with prior work are welcome. Public availability and passing code checks do not constitute peer review or acceptance.

The paper cites Simons and de Weger, Hercher, Wang, Bugeaud, and Barina. References and the comparison boundaries are in the manuscript and [sources.md](sources.md). No endorsement by those authors is claimed.
