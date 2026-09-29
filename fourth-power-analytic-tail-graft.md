# Joining the certified low-height map to the analytic smaller base

Private derivation, 29 September 2026. This proposed capacity map combines the completed finite certificate with the analytic argument in `fourth-power-interpolation-bound.md`. It requires its own dependency audit before use in a cycle exclusion. External review and priority remain pending.

Let delta=log2(3), epsilon=1/93, lambda=delta-epsilon, B=2^15, c0=37.99, c1=40.99, and

    Phi(y)=max(delta*y-c1, min(delta*y-c0, y+71*(delta-1)-c0)),
    d=epsilon*B-c1=2895593/9300.

Define F on y>=71 by

    F(y)=Phi(y),              y<=B,
    F(y)=lambda*y+d,          y>=B.

The definitions agree at B. Equivalently F is the minimum of Phi and the affine tail lambda*y+d. This equivalence follows directly above the old turning height; below that height the affine tail lies strictly above Phi, since epsilon*(B-77)>c1-c0. The map is continuous, strictly increasing, has slopes at least one, satisfies y<=F(y)<=delta*y, and obeys the global lower estimate

    F(y)>=lambda*y-c1.                            (1)

Taking the minimum of two valid restart maps does not in general preserve a restart rule. The case analysis below is the additional argument needed here.

## High starting heights

For y>=B, the analytic one- or two-block restart for lambda*y applies. Since d>0, F(y)>=lambda*y; also F(y)>=y>=B. Thus monotonicity transfers both the endpoint and intermediate run bounds to F, including the two-block endpoint F(F(y)).

## Starting heights below B

Restrict to positive orbit segments avoiding the published basin through 2^71, as required by the finite certificate. Write n=a*2^k-1, and let ell be its following even-run length and s the next odd-run length. The existing J41 reduction has the following exhaustive alternatives.

If ell>=41, or a>=2^q0 with q0=ceil(12*(41-ell)/7), the one-block loss is at least c1. Hence y1<=delta*y-c1<=Phi(y)=F(y).

Otherwise ell<=40 and a<2^q0 with q0<=69. Since k<=y<B<2^19, the completed global residue sweep proves s<=100. This is the original exhaustive J41 sweep, not an extrapolation to larger exponents.

If k>=200, then y>=200. Dropping positive losses in the elementary two-block identity gives

    y2<=delta*y+(delta-1)*100.

On the other hand, (1) gives

    F(F(y))>=lambda^2*y-(lambda+1)*c1.

The exact rational interval audit checks

    (lambda^2-delta)*200-(lambda+1)*c1-(delta-1)*100>0,
    lambda*200-c1>100,
    lambda^2-delta>0.

These inequalities imply y2<=F(F(y)) and s<=F(y) for every y>=200 in this case, even when the first virtual step crosses B.

It remains to treat k<200. The existing class-generation audit exhaustively lists every transition failing the original one- or two-block sufficient inequalities. A transition outside that list already has a Phi restart of length at most two. Its starting height is less than 200+69<300, and Phi^2(300)<=delta^2*300<B, so this restart is unchanged under F.

For a transition inside the finite class list, the two completed algorithms either prove convergence into the basin or provide a Phi restart, with all required intermediate run checks. The audited input has k+bit_length(last_a)<=117. Both completed precise proofs have maximum restart depth five. Therefore every target height they use is at most

    delta^5*117 < B.

Their successful restart witnesses also remain valid for F. Singleton branches that converge into the basin cannot occur on a basin-avoiding orbit, regardless of their intermediate height.

This covers every starting height and every transition. The bounded block-restart induction gives k_(i+t)<=F^t(y_i) on every orbit segment avoiding the verified basin. In particular it applies to every hypothetical nontrivial positive cycle. The general envelope and majorization argument then applies to F without an affine or concavity assumption.

## Proof dependencies and scope

The finite dependencies are the frozen certificate `nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json`, its two full proofs and independent checks, and the original exhaustive J41 coverage and residue-sweep receipts. The new analytic dependency is the smaller-base theorem derived from Bugeaud1999, Theorem1, rational clause(6). The fourth-power graft audit checks the source hashes, the actual maximum input height and restart depths, the interval margins above, and the associated analytic and formal receipts.

The new map does not itself exclude any additional cycle size. A complete minimum-window search and exact rational approximation contradiction are still necessary. Preliminary floating-point profile improvements remain proposals until reconstructed and independently checked with rational arithmetic.
