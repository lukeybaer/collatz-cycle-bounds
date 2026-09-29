# Verification report

Prepared 29 September 2026. This report separates completed verification from
future or unfinished checks. The mathematical claims are in `collatz-paper.md`
and `collatz-research-paper.pdf`; their significance and prior-work comparison
are in `RESEARCH-SUMMARY.md`.

## Claim-to-evidence map

| Claim | Principal evidence | What it establishes |
|---|---|---|
| All-orbit base δ−1/80 | `retained-loss-interpolation-bound.md`; `src/audit_retained_loss_bound.py`; `results/retained-loss-exponential-bound-audit.json` | Written universal argument and exact constants |
| Cycle coefficients 1.61 and 15.27 | Same audit; `cycle-bound-corollaries.md`; cited Simons-de Weger theorem | Exact specialization of the applicable published ranges |
| General cyclic majorization | `nonlinear-envelope-lemma.md`; `results/nonlinear-majorization-check.json` | Self-contained proof, challenged on exact finite examples |
| Finite nonlinear map | `results/nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json` | Two completed native proofs and exact dependency checks |
| m=92–95 | `results/cycle-exclusions-m92-m95-fourth-power-direct-audit.json` | Four exact profile contradictions with the proved finite map |
| m=96–98 | `results/cycle-exclusions-m96-m98-fourth-power-direct-audit.json` | Three exact profile contradictions with the proved finite map |
| m=99 | `results/cycle-exclusion-m99-two-regime-grafted-audit.json` | Complete minimum-window search, full original-arithmetic repeat and profile closure |
| m=100 | `results/cycle-exclusion-m100-fourth-power-grafted-audit.json` | Complete minimum-window search, partition/journal/fallback checks and profile closure |

## Analytic argument

The retained-loss proof fixes J≥10,000, divisible by 100, and y≥79.5J.
When D≥J the elementary one-block loss suffices. Otherwise it splits at
D=0.9J. Two interpolation rows cover the smaller-loss stratum and five cover
the larger-loss stratum through k/J=256. A separate polynomial argument
covers every larger k/J. Every row has a positive exact interpolation margin,
a sufficient intermediate-run bound, and a retained two-block loss greater
than 3.2J. The cutoff B=1,272,000 and 32-step virtual warmup then give the
stated global theorem.

The exact audit also runs 35 large-parameter challenges, 14 rounding-boundary
checks, 1,260 virtual-envelope checks and nine exact-integer block challenges.
The largest specified odd-run exponent in the latter is 2,600,000. These
are supplemental challenges, not an enumeration of all possible orbits.
The receipt binds the source, proof notes and earlier infinite-range argument
by SHA-256. It has no floating-point decision in the certificate inequalities.

The author-hosted 1999 Bugeaud theorem was rendered and visually inspected,
including its rational clause, logarithmic-height convention, signed rational
arguments and two cardinality conditions. The first uses powers with exponent
2r because p=2 and the source's t=1. A comparison against the final journal
typesetting remains pending. The complete external theorem is an assumed
published input, not re-proved or formally verified here.

## Finite map and search arithmetic

The J41 map has an exhaustive 20,971,480-pair modular reduction and 44,497
remaining classes, with exactly 144,429,913,922,369,056,364 seeds. The inverse-
residue proof uses 1,648,100,522 nodes; the parity-progression proof uses
1,253,664,985 nodes. Both finish every class. The largest successful restart
depth is five. Their partition counts need not agree, but each independently
covers the full input.

Directed integer and rational logarithmic bounds are checked independently.
Python reconstructs 2,032,128 threshold values and repeats 112 selected
progression cases. Separate, simpler J35 and J38 capacity certificates have
full Python verification. No claim is made that the J41 proof itself was
fully repeated in Python.

The m=99 compact search consists of 206,426 jobs and 2,758,731,446 nodes.
Its original-arithmetic repeat uses 945 initial jobs and 2,758,525,965 nodes.
After normalizing the partition-boundary work, the node count is 2,758,525,020
in both, and all seven substantive counters agree. There are zero survivors.

The m=100 compact search consists of 231,505 jobs and 14,528,184,145 nodes,
with zero survivors. Its single fallback job, ID 21366, is independently
repeated with original arbitrary-precision arithmetic and matches at
5,063,641 nodes. The entire original-arithmetic repeat remains unfinished at
this report's snapshot. It must not be described as completed validation.

Each end-to-end audit checks the capacity certificate, initial lower bound,
directed target generation, exact window endpoints, complete job coverage,
journal totals, overflow/fallback evidence and final rational contradiction.
The fixed-width implementation has explicit checked paths and arbitrary-
precision fallback. A resource limit is unresolved, never an exclusion.

## Formal verification

The preserved aggregate receipt covers 93 lemmas in 20 Lean modules.
`formal/retained-loss-verification.json` adds ten lemmas in
`CollatzRetainedLoss.lean`: seven exact interpolation margins, the numerical
loss inequalities, the retained-loss implication and the rounding/warmup
constants. Total: **103 lemmas in 21 modules**.

Pinned environment: Lean 4.34.1, mathlib commit
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The verifiers reject `sorry`,
`admit`, custom axiom declarations and unsafe proof shortcuts. Compiler reports
use only `propext`, `Classical.choice` and `Quot.sound`. Source hashes,
compiler output and the axiom reports are included. No external proof service
or AI tactic was used.

The formalized material supports the written proof. It does not include all
published transcendence theory, every analytic specialization, all source
imports, the entire native search or a proof of convergence.

## Reproducing the evidence

The completed finite snapshot is `collatz-finite-review-bundle.zip`. A fresh
extraction reproduced four end-to-end exclusion receipts and two analytic
receipts byte for byte. Its verification receipt is
`results/finite-review-bundle-verification.json`.

The final integrated snapshot is `collatz-research-review-bundle.zip`.
Its manifest lists every included file, size and SHA-256. The companion
`results/research-review-bundle-verification.json` records whether its fresh
extraction and seven rerun audits pass. Consult that receipt for the final
package status; its existence is not inferred from the earlier archive.

After extraction, run:

    python verify_bundle.py
    python verify_bundle.py --audits

The first checks hashes and saved formal receipts. The second reruns four
end-to-end audits and three analytic audits in a temporary copy and requires
byte-identical results. It does not access the network or invoke any model.
It may take several minutes. It does not recompute billions of native search
nodes; the archive's `REPRODUCE.ps1` gives the separate full m=100 command.

To recompile the Lean proofs with the pinned dependencies, run both
`formal/verify_all_formal.py` and `formal/verify_retained_loss_formal.py`,
supplying their `--mathlib` and `--lean-bin` arguments. Mathlib, compiler
binaries and third-party papers are not redistributed in the archive.

## Limits and next independent checks

The proofs, implementations and selected checks were developed in one research
session on one machine. Different algorithms reduce some risks; they do not
eliminate shared mathematical or implementation errors. SHA-256 binds evidence
to files but does not establish correctness. Finite tests cannot prove a
universal theorem, and compiler acceptance applies only to the statements
actually formalized.

The highest-value next checks are external review of Bugeaud's hypotheses and
the restart/majorization bridge, independent-machine reproduction of the
finite certificates, completion of the full m=100 original-arithmetic repeat,
and a complete literature/priority review. The active J45 and m=101 work is
excluded from the completed claims. The full Collatz conjecture is unresolved.

**TLDR:** Exact analytic audits, two exhaustive capacity algorithms, completed
window searches and 103 selected formal lemmas support the candidate results.
The package makes them reproducible and reviewable; it does not substitute for
external mathematical review or prove Collatz convergence.
