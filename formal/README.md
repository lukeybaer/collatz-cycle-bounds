# Mechanically checked proof core

These files formalize ten abstract lemmas used in the research notes. They were checked with Lean 4.34.1 and mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. The compiler reports only the standard axioms `propext`, `Classical.choice`, and `Quot.sound`; there are no proof placeholders or additional declared axioms.

`CollatzGrowthEnvelope.lean` proves:

1. A gap between consecutive sorted values inherits a monotone growth bound from a cyclic ordering.
2. A deficit below an extremal ramp persists at every subsequent index.
3. Equal total sums then force the required comparison of every prefix sum.

`CollatzRestart.lean` proves:

1. A local one- or two-block restart rule covers every index by an endpoint or a single intermediate point.
2. All run lengths are bounded by the virtual orbit of the growth map.
3. Actual heights are bounded using one extra elementary multiplicative step.

`CollatzLocalLoss.lean` proves the two-block loss from a p-adic run bound and the conversion of an additive loss into a fractional loss.

`CollatzNormalizedLog.lean` verifies the quadratic logarithm bound and the all-parameter valuation cutoff, using mathlib's proved numerical bound for log(2). It uses an elementary square-root comparison instead of differentiation.

The hypotheses are explicit in the source. The formalization does not construct the inverse-iterate ramp, specialize the p-adic theorem, or verify the finite search. It does not establish the Collatz conjecture. Those parts remain ordinary mathematical and computational arguments requiring review.

## Reproduction

With Lean 4.34.1 available, this directory is a Lake project:

```text
lake update
lake exe cache get Mathlib/Basic/Real/Basic.lean Mathlib/Algebra/Order/BigOperators/Group/Finset.lean Mathlib/Tactic.lean Mathlib/Analysis/SpecialFunctions/Log/Basic.lean Mathlib/Analysis/SpecialFunctions/Sqrt.lean Mathlib/Analysis/Complex/ExponentialBounds.lean
lake build
```

Alternatively, use a mathlib checkout at the pinned commit with its dependencies initialized and cached:

```text
python verify_formal.py --mathlib PATH_TO_MATHLIB --lean-bin PATH_TO_LEAN_BIN
```

The latter command compiles all four files, checks the complete axiom reports, and writes `formal-verification.json` with source and output hashes. It runs no external proof assistant service or language model. The portable Lean runtime used during this session was obtained from the official Lean release; the large runtime and dependency cache are kept outside the deliverable.


## Later, separately checked extensions

The original ten-lemma receipt is frozen in core-verification-v1.json as a finite-search dependency. Two later modules add thirteen lemmas without changing that core.

CollatzSharperConstants.lean proves the tighter all-parameter cutoff and local loss for epsilon1/3200 (three lemmas). Reproduce with verify_sharper_formal.py using the same --mathlib and --lean-bin options. Its receipt is sharper-constants-verification.json.

CollatzGlobalEnvelope.lean proves monotonicity, upper and lower estimates, and the linear tail of the global extension; virtual-orbit bounds; the finite warmup amplification; the numerical bounds on log(3)/log(2); and the explicit33-step virtual bound (ten lemmas). Reproduce with verify_global_formal.py; receipt global-envelope-verification.json. These compile directly against the pinned mathlib checkout and do not change the frozen Lake project.

All23lemmas have passed with only propext,Classical.choice,Quot.sound. The p-adic theorem and its Collatz specialization, cycle-size input, and finite search remain outside this formalization.

Further separately checked modules bring the total to34 lemmas:

- CollatzConvexCost.lean: four weighted-prefix and differentiable convex majorization lemmas; reproduce with verify_convex_formal.py.
- CollatzIndependentConstants.lean: four all-parameter cutoff/local-loss lemmas supporting epsilon1/2500; reproduce with verify_independent_formal.py.
- CollatzDependentValuation.lean: three elementary lemmas proving v2(u*(3^p+3^q))<=2 for every odd positive u and nonnegative p,q; reproduce with verify_dependent_formal.py. The rational unique-factorization reduction is a written input.

Each separate verifier preserves its source-bound receipt and compiler report. Only standard Lean axioms appear; none of these modules invokes a model or proof-search service. The older paragraph's23 count describes the earlier checkpoint, not the current total.

The current total is48 supporting lemmas. CollatzReciprocalCost.lean adds seven derivative, monotonicity and convexity lemmas, including the exact binary cost1/(2^y-1). CollatzCyclicEnvelope.lean adds seven order-theoretic lemmas: iteration of the inverse/forward adjunction, construction of the cyclic envelope between run lengths and actual heights, its growth constraint, and preservation of that constraint under a common cap. Reproduce separately with verify_reciprocal_formal.py and verify_cyclic_formal.py.

For a single reproducibility entry point, run verify_all_formal.py with the same --mathlib and --lean-bin arguments. It checks the saved source hashes, recompiles all accepted modules, checks every printed axiom report, and writes a new aggregate-verification.json. It does not rewrite frozen original receipts. The original Lake project still builds only its four original core modules.


There are now60 accepted supporting lemmas. CollatzParityConstants adds five
constant/cutoff lemmas for the signed-rational epsilon1/1250 argument;
CollatzSignedNormalization adds four exact parity/algebra/congruence lemmas;
CollatzCommonCap adds three continuity, cap-existence, and growth-preservation
lemmas. Each module has a separate verifier and receipt. No complete Collatz
application or external transcendence theorem is claimed to be formalized.


The current accepted total is71 supporting lemmas. CollatzInterpolationParameters
adds four all-parameter inequalities for the epsilon1/440 precursor.
CollatzTwoRegimeParameters adds seven exact margin, dyadic, cardinality,
normalization, local-loss and restart-constant results for epsilon1/160.
Their separate verifiers are verify_interpolation_formal.py and
verify_two_regime_formal.py. The full application still contains ordinary
mathematical proof inputs; this count is not a measure of a complete proof.


The accepted total is now85 lemmas in19modules. CollatzThirdRange adds four
lemmas for the epsilon1/131 intermediate range. CollatzFourthPower adds eight
signed normalization, congruence, margin and local-loss lemmas for epsilon1/93;
CollatzAffineEnvelope adds the global affine envelope and its exact iterative
bound. Reproduce with verify_third_range_formal.py and
verify_fourth_power_formal.py, or the aggregate verifier. All85passed the
aggregate recheck at2026-09-29T13:12:14.651730+00:00. The compact earlier
epsilon1/160 review archive retains its own consistent71-lemma snapshot.
