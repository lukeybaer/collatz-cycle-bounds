# Stronger cycle consequences of the two-regime block bound

Private research supplement, 29 September 2026. These deductions use the
candidate theorem in two-regime-interpolation-bound.md and the primary
source cited below. They do not alter that frozen proof or any active
search input. Independent review and priority verification remain pending.

Put delta=log_2(3), lambda=delta-1/160, A=(delta/lambda)^26, and
a_0=log_2(delta). Let m count local minima and K count odd shortcut
steps of a hypothetical nontrivial positive cycle.

## A sharper middle-range bound

Theorem3(d) of Simons-de Weger, version1.44, states, for
91<=m<=515619,

    K<1.4784m*delta^m,
    n_min<51825000*m^2*delta^m.

Consequently, with C=51825000,

    y_min=log_2(n_min+1)
       <Y(m):=1+log_2(C)+2log_2(m)+a_0*m.

Rotate the cycle to its least member and sum the already proved block
bound. This gives the more precise candidate corollary

    K < U(m):= A*Y(m)*(lambda^m-1)/(lambda-1),
                  91<=m<=515619.                      (1)

This is a purely analytic deduction; it does not depend on the new
finite capacity computations. The published theorem's numerical
cycle-size inputs are retained as stated.

For m>=1024, the function log_2(m)/m is decreasing. Since C<2^26
and a_0<2/3, we have

    Y(m)/m < 2/3+47/1024.

The exact directed-interval audit proves A/(lambda-1)<383/200=1.915.
Therefore

    [A/(lambda-1)]*[2/3+47/1024]
       <838387/614400 <137/100,

and hence

    K<1.37m*lambda^m,            1024<=m<=515619.       (2)

The monotonicity used here follows, for example, from differentiating
(ln x)/x: its derivative is (1-ln x)/x^2<0 for x>=1024.
The bound a_0<2/3 follows from delta<317/200 and (317/200)^3<4.

## Comparison throughout the published middle range

For the comparison it is enough to enlarge U(m) by replacing
lambda^m-1 with lambda^m. The ratio to 1.4784m*delta^m is then

    R(m)=[A/(1.4784*(lambda-1))]*[Y(m)/m]*(lambda/delta)^m.

Both nonconstant factors are positive and decreasing for m>=91.
For Y(m)/m this follows by differentiating
[1+log_2(C)+2log_2(m)]/m; its derivative numerator is
2/ln2-[1+log_2(C)+2log_2(m)]<0. An exact rational interval
calculation at m=91 gives R(91)<1. Thus (1) is strictly smaller than
the stated 1.4784m*delta^m bound throughout 91<=m<=515619.
This comparison is with Theorem3(d)'s uniform bound, not every
individual K_2(m) value or every later result in the literature.

## Large m and a wider valid range

The same published theorem gives K<16m*delta^m for every m>=91
by coarsening its three applicable ranges. Thus the earlier calculation
from Corollary13 actually proves y_min<10m for every m>=1024.
The two-regime argument therefore gives

    K<19.15m*lambda^m,           m>=1024.               (3)

Use (2) where its sharper hypothesis holds, and (3) above515619.
The original restriction m>=515620 in the frozen note is sufficient
but unnecessarily narrow. No claim in that note is invalidated.

For m>=515620, (3) is also smaller than both published coefficients
15.109m*delta^m and 15.108m*delta^m in their respective ranges.
One entirely rational comparison uses lambda/delta<999/1000 and
(19.15/15.108)*(999/1000)^1024<1, then monotonicity in m.

These upper bounds still grow exponentially. They do not rule out
cycles of arbitrary complexity or establish convergence.

## A separate consequence of the finite capacity certificate

Let F be the frozen, basin-avoiding growth map in
two-regime-analytic-tail-graft.md. Its future-run bound gives

    K < sum(F^t(Y(m)), t=0,...,m-1),    91<=m<=515619. (4)

An upward rational iteration of F supplies a computable upper bound
without assuming that actual cycle heights obey F in one step.
Preliminary values around m=96 through105 are about30 percent of
the uniform published upper bound. These exploratory numbers require
their own directed-interval audit before use as certificates.
The present cycle-exclusion searches retain their earlier inputs.

## Primary source

J. Simons and B. de Weger, Theoretical and computational bounds for
m-cycles of the 3n+1 problem, version1.44,31August2010, Theorem3(d)
onp.5 and Corollary13. The theorem's complete range table was read
and visually checked from the author-hosted PDF.
https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf
