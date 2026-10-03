# Results and scope of the review revision

The research has two candidate contributions: a particular explicit bound on Collatz block growth and finite certificates extending the located local-minimum exclusion from 95 to 100. Neither establishes the Collatz conjecture. The work remains unrefereed.

## Analytic result

With `delta = log2(3)`, `lambda = delta - 1/80`, `B = 1,272,000` and `A = (delta/lambda)^32`, the manuscript argues that every positive block orbit satisfies

```
k_t <= A y_0 lambda^t
y_(t+1) <= delta A y_0 lambda^t
```

Here a block is a maximal odd run followed by a maximal even run, `k` is its odd-run length, and `y = log2(n+1)` at its start. The resulting cycle upper bounds are `1.61 m lambda^m` for 1024–515619 local minima and `15.27 m lambda^m` above that range.

At m=1024 the first displayed bound is about 3,049 times smaller than the applicable `1.4784 m delta^m` bound in Simons–de Weger version 1.44, Theorem 3(d). Both bounds remain enormous. This is an asymptotic quantitative comparison, not a speedup or a proof of convergence; lambda is still greater than one.

## Finite result

Separate certificates use earlier frozen analytic parameters to exclude candidate cycles with 92–100 local minima. Hercher's journal result, including its corrigendum, covers through 91. Wang's located 2026 preprint claims through 95. Thus the additional cases relative to the latter are 96–100. `m` is not the number of individual steps in a cycle.

The reduction uses Barina's published verification below 2^71, nonlinear extremal profiles, exact rational-approximation certificates, and complete least-minimum window searches. The full m=100 original-arithmetic reproduction status is maintained in [VERIFICATION-REPORT.md](VERIFICATION-REPORT.md).

## What changed after feedback

- A conventional LaTeX paper replaces the prose-oriented PDF source, with a proof strategy, explicit notation, theorem/proof structure and a search soundness explanation.
- A standard pinned Lake project imports all active modules. Guarded axiom reports fail the build if the checked dependencies change.
- A connected top-level theorem now proves the growth inequalities from natural-number block identities **and an explicit local analytic hypothesis**. The external p-adic theorem and full specialization remain outside Lean.
- The literature review now distinguishes inherited methods from the specific candidate improvement. In particular, Hercher's corrigendum already uses the geometric extremal mechanism underlying our profile argument.
- The even-run inequality at a closed stratum boundary is corrected from strict to non-strict. The later bounds allow this and the exact analytic audits remain applicable.

Feedback has not independently established correctness or novelty. The most valuable next check is a specialist review of the p-adic specialization and its connection to the finite reduction. See the [dated priority search](NOVELTY-REVIEW.md) for inspected sources and limitations.
