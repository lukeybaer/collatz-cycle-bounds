# Smaller global cutoffs for the explicit block-growth bounds

Private candidate mathematical refinement, 29 September2026. This note changes
neither the published interpolation theorem nor its already checked local
parameter arguments. It removes slack from the rounding and virtual warmup.
The Collatz conjecture remains open; review and priority confirmation are pending.

## General rounding lemma

Suppose a proved local argument applies whenever J is a positive multiple of M,
J>=J_0, and y>=CJ. Here M divides J_0. Its alternative is

    y'<=delta*y-J,

or

    k'<=delta*y-J,  y''<=delta^2*y-(16/5)J.

Let epsilon>0, epsilon*C<1, delta<8/5, and choose

    B>=max(C*J_0, M*C/(1-epsilon*C)).

For y>=B set J=M*floor(y/(MC)). Then J>=J_0 and y>=CJ.
The strict floor estimate gives

    J>y/C-M>=epsilon*y.

The second inequality follows from (1-epsilon*C)y>=MC. This is a direct
rounding argument; an auxiliary99/100 factor is unnecessary. With
lambda=delta-epsilon the local alternatives are therefore bounded by
lambda*y and lambda^2*y, including the intermediate run length.

## A shorter virtual warmup

Define G(y)=delta*y for y<=B, and G(y)=max(lambda*y,y+(delta-1)B) for
y>=B. The same restart induction as in the predecessor proofs applies.
For all y>=1, G(y)>=lambda*y. Furthermore G(y)=lambda*y as soon as

    y>=(delta-1)B/(lambda-1).

For both parameter sets below, exact rational bounds prove

    lambda>157/100,
    (103/100)(lambda-1)>delta-1.

Thus if (157/100)^T>(103/100)B, every virtual orbit from y_0>=1 is in
the linear region by step T. The global estimates hold with

    A=(delta/lambda)^T,
    k_t<=A*y_0*lambda^t,
    y_t<=delta*A*y_0*lambda^(t-1).

These estimates cover every t, including t<T. The threshold concerns the
virtual upper envelope, not actual trajectory growth.

## Two checked specializations

| Local argument | epsilon | C | M | J_0 | B | T |
|---|---:|---:|---:|---:|---:|---:|
| Fourth-power two-range proof | 1/93 | 92 | 2 | 200 | 18400 | 22 |
| Four-range proof | 1/83 | 82 | 20 | 2000 | 164000 | 27 |

In the first row CJ_0=18400 and MC/(1-epsilon*C)=17112. In the second
they are164000 and136120. The warmup inequalities are exactly

    157^22>103*18400*100^21,
    157^27>103*164000*100^26.

The local proofs are respectively `fourth-power-interpolation-bound.md` and
`four-range-interpolation-bound.md`. Each proves the alternative for all
admissible J before choosing its earlier, more conservative B. Applying that
same local result above is legitimate and does not extend a sampled range.

The amplification constants are approximately1.16155634080 and1.22878547850,
respectively. The smaller bases remain1.57420981255 and1.57291430795.
The audit gives exact upward rational cycle coefficients using the same
published range table and affine bootstrap as the predecessor proofs.

## Consequence for finite/analytic capacity maps

The certified finite map Phi_0 has parameters c_0=37.99,c_1=40.99,h=71.
The new cutoffs suggest the two affine tails

    L_1(y)=(delta-1/93)y+18400/93-c_1,
    L_2(y)=(delta-1/83)y+164000/83-c_1.

Their pointwise minimum can be joined to Phi_0 only after a separate proof
checks the finite tree, the intermediate range, and the switch between local
arguments. This note alone does not certify that combined map or any new
cycle exclusion. The proposed combination is recorded here to make its exact
mathematical dependency explicit.

## Verification scope

`src/audit_optimized_cutoffs.py` checks both local-result receipts and their
source/note hashes, all rational inequalities, integer warmup powers, rounding
near the new cutoffs, and virtual envelope examples. The general argument
above supplies the universal proof. The cited Bugeaud theorem and published
cycle bounds remain external mathematical inputs; no convergence claim follows.
