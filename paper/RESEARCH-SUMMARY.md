# Collatz research: results and significance

The work produced two substantial candidate contributions: a smaller explicit
growth bound for every positive Collatz orbit, and a computer-assisted exclusion
of cycles with up to 100 local minima. Both have written arguments and
reproducible internal checks. Correctness and priority still need independent
specialist review. The full Collatz conjecture remains open.

## What improved

**An explicit smaller exponential base.** Write δ=log₂3. The new argument gives
λ=δ−1/80≈1.572462500721156. If kₜ is the length of the t-th maximal odd run and
y₀=log₂(n₀+1), it gives

    kₜ ≤ A y₀ λᵗ,  A=(δ/λ)³²≈1.288362904142.

For a hypothetical cycle with m local minima and K odd steps, it gives

    K < 1.61 m λᵐ       for 1,024 ≤ m ≤ 515,619,
    K < 15.27 m λᵐ      for m ≥ 515,620.

The comparison is with the explicit δᵐ estimates in
[Simons and de Weger, version 1.44, Theorem 3(d)](https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf).
At m=1,024, our displayed upper bound is about 3.28×10²⁰⁴, compared with
9.99×10²⁰⁷: over 3,000 times smaller. The improvement grows exponentially
with m, although the absolute bounds remain enormous.

The proof specializes [Bugeaud's 1999 p-adic interpolation theorem](https://doi.org/10.1017/S0305004199003692).
The useful new step in our derivation retains an elementary loss that earlier
versions discarded, then treats small and large losses separately. Explicit
parameter inequalities cover both cases and an unbounded tail. A restart
argument converts those local estimates into the global result.

**Candidate exclusion through 100 local minima.** Our completed certificates
cover m=92 through 100 independently of the claimed 2026 exclusion through 95.
Together with [Hercher's journal result through 91 and its corrigendum](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html),
this would exclude all nontrivial positive cycles with at most 100 local minima.
The located comparison is [Wang's 2026 preprint through 95](https://doi.org/10.5281/zenodo.21670936).
Thus 96–100 are the candidate new cases; 92–95 are independently checked prior cases.

A local minimum here starts a maximal odd/even block. This is not merely an
exclusion of cycles containing 100 integers. The finite argument uses
[Barina's published convergence verification below 2⁷¹](https://doi.org/10.1007/s11227-025-07337-0),
stronger block-growth maps, exact majorization, rational approximation and
complete searches over the remaining possible least cycle members.

## How it was checked

- Exact rational audits verify the analytic constants, all seven interpolation
  rows, the infinite-range reduction and the rounding and warmup inequalities.
  Large-parameter and exact-integer examples challenge the argument; they do
  not replace its universal proof.
- Two complete algorithms verify the central finite-capacity certificate over
  44,497 arithmetic-progression classes representing more than 1.44×10²⁰ seeds.
  Python checks every one of 2,032,128 rational thresholds and 112 selected cases.
  The full Python check is **not** claimed for those 44,497 classes.
- The compact m=99 search visits 2,758,731,446 nodes. A full repeat using the
  original arbitrary-precision arithmetic agrees on every substantive counter.
  The m=100 search visits 14,528,184,145 nodes; its partition, journal and
  fallback checks pass. Its whole-search original-arithmetic repeat is still
  running and is not part of the completed claim.
- **103 selected lemmas** have passed Lean 4.34.1 with pinned mathlib, without
  proof placeholders. This is partial formal verification, not a formal proof
  of the entire manuscript or of Collatz convergence.
- A fresh extraction of the final research archive passed all 428 manifest
  checks and the saved 103-lemma receipts. Four finite end-to-end audits and
  three analytic audits, including the strongest retained-loss estimate,
  reproduced their saved results byte for byte. This did not repeat the
  billion-node native searches.

## What this means for the field

If independent review confirms correctness and priority, this is a quantitative
advance in Collatz cycle bounds, with reusable exact certificates and a general
growth-constrained majorization argument. It is a plausible specialist research
contribution, not an established breakthrough on the full conjecture.

The new base is still greater than one, so the analytic theorem permits
unbounded growth. Excluding every cycle up to any fixed number of minima leaves
infinitely many possible cycle sizes. The next decisive step is external
mathematical scrutiny and independent-machine reproduction, particularly of
the p-adic specialization and finite-capacity reduction. A negative literature
search does not establish that a result is new.

The 13-page paper, its mathematical source, this summary, the verification
report, and the reproducible review archive are saved together. Research notes,
failed approaches and unfinished experiments are preserved separately. No
Claude or external AI research reviewer was consulted, and no reset credit was used.

**TLDR:** Two internally checked candidate advances: a smaller explicit
exponential growth base and cycle exclusions through 100 local minima.
The evidence is substantial and reviewable; novelty and external validation
remain open, and Collatz itself is not solved.
