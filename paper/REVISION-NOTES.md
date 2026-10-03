# Review revision — 3 October 2026 UTC

This revision strengthens the presentation and verification of the existing claims. It does not claim a new mathematical result beyond the first public edition of 29 September 2026.

## Response to the substance of the feedback

The original collection of Lean lemmas did not constitute a connected proof of the headline theorem. The active root Lake project now imports every module, pins its dependencies and builds on GitHub. All 103 selected historical axiom reports are guarded. The new theorem `Collatz.odd_start_growth` begins with any positive odd integer, constructs its block orbit, proves that its block starts are actual shortcut iterates, and derives both growth inequalities under the explicit `LocalLossCertificate` hypothesis. The formalization still does not supply that certificate: the external interpolation theorem and its specialization remain a written proof obligation.

The paper is now a conventional LaTeX manuscript. It states the parameters, distinguishes block count from odd-step count and total shortcut steps, gives a short proof strategy before the details, and explains how the finite certificates join to the claimed exclusion. The standard project commands, claim-to-evidence table and public CI make the checked statements easier to locate and reproduce.

## Correction to the archived text

At the closed boundary of a retained-loss stratum, the justified even-run estimate is `ell <= d_+ J + 1`, not a strict inequality. In particular, equality is not ruled out merely by membership in the stratum ending at `D = 0.9 J`. The LaTeX revision uses the non-strict bound. The subsequent rational-height estimate is still strict because of its separate positive margin. No certificate parameter or search kernel changes are needed for this correction. The seven exact analytic/exclusion audits were replayed successfully.

The old root manuscript and historical source files still carry the original wording because the manifest freezes that evidence. Use the LaTeX paper for the corrected current statement.

## Priority and scope

The expanded primary-source review found important prior art in Hercher's 2026 corrigendum for the geometric extremal mechanism. That debt is now explicit. The general nonlinear profile lemma is not presented as an independently established novelty claim. The candidate contributions are the specific explicit growth specialization and the finite extension through 100 local minima; relative to Wang's located preprint, the additional cases are 96–100. Search coverage and access limitations are documented in `NOVELTY-REVIEW.md`.

## Computational confidence

Fresh small tests compare independently generated Python shortcut trajectories with both native kernels, exercise overflow fallback, and check wide arithmetic and exact interval/prefix tools. The full original-arithmetic m=100 repeat, its status and exact comparison requirements are documented in `VERIFICATION-REPORT.md`. New receipts are kept under `evidence/revision-20261002/`; all 428 historical manifest entries remain unchanged.

The arithmetic repeat and successful Lean build address specific risks. They do not replace specialist review of the written interpolation argument, imported cycle results and search soundness. The feedback that prompted this revision was not an endorsement of correctness or priority.
