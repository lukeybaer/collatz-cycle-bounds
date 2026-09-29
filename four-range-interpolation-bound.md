# Four interpolation ranges: a smaller explicit block-growth base

Private candidate mathematical result, 29 September 2026. Independent review
and priority verification remain pending. This strengthens the base of the
fourth-power argument while increasing its finite height threshold. It does
not prove the Collatz conjecture.

## Statement

Use the shortcut Collatz map and maximal odd/even blocks of
`fourth-power-interpolation-bound.md`. At an odd block start let
k=v_2(n+1), y=log_2(n+1), delta=log_2(3), beta=delta-1. Set

    epsilon=1/83, lambda=delta-epsilon,
    C=82, B=2^18, A=(delta/lambda)^33.

For every positive orbit, indexed from any odd block start,

    k_t<=A*y_0*lambda^t                         (t>=0),
    y_t<=delta*A*y_0*lambda^(t-1)               (t>=1).

Here lambda is approximately1.572914307950072 and A approximately1.28635145.
For a hypothetical nontrivial cycle with m local minima and K odd terms,

    K<1.60m*lambda^m,                    1024<=m<=515619,
    K<15.19m*lambda^m,                   m>=515620.

The finite numerical capacity maps previously proved are not altered by this
statement. Its larger B means a smaller asymptotic base does not automatically
improve every finite-cycle calculation.

## Reduction and published theorem

Write n=a*2^k-1, with a positive odd integer, and let ell be the following
even-run length. Put b_0=2^ell-1 and D=ell+beta*log_2(a)-1>=0. The exact
block identities give

    y'<=delta*y-D,
    y''<=delta*y-D+beta*k',
    k'=v_2(a*3^k+b_0)-ell.

Fix J divisible by20, J>=2000, and suppose D<J and y>=82J. Then
ell<=J, log_2(a)<(12/7)(J+1), and k>80J. Let r_0 in{0,1,2,3} make
k+r_0 divisible by4, and put H=(k+r_0)/4. Use

    alpha_1=81, alpha_2=-3^(r_0)*b_0/a,
    Lambda=81^H-alpha_2=3^(r_0)*(a*3^k+b_0)/a>0.

For valuations at most3 the required bound is immediate. Otherwise alpha_2
is1 modulo16, and Bugeaud (1999), Theorem1, rational clause(6), applies
with p=2,g=1,E=4,b_1=H,b_2=1,u=0,D_field=e=f=1,t=1. In particular
v_2(alpha_1-1)=4 and v_2(alpha_2-1)>=4. The exact source hypotheses,
including signed rational arguments, are transcribed and checked in the
preceding fourth-power note and its self-contained review manuscript.

The logarithmic heights obey

    h(alpha_1)=4ln3,
    h(alpha_2)<U*J,
    U=(12/7)*(2001/2000)*.6932.

The denominator bound follows from log_2(a). The numerator has binary
logarithm less than J+3delta<J+5<(12/7)(J+1). Reduction cannot increase
height. These estimates use J>=2000, not just a sample of such values.

## A sharper factorial estimate

Let P_M=product(i!,i=1,...,M-1). For every integer M>=6000,

    P_M^(-2/[M(M-1)]) < (449/100)/(M-1).

The integral calculation in `two-regime-interpolation-bound.md` gives

    -2ln(P_M)/(M(M-1)) <= -ln(M-1)+3/2+ln(M-1)/M.

For M=6000u, u>=1, use ln6000<8.7 and lnu<=u-1 to obtain
ln(M-1)<8.7+u-1<9u. Hence ln(M-1)/M<.0015. Finally
1.5015<ln(449/100). Both numerical logarithm bounds have directed rational
series checks in `src/audit_four_range_bound.py`.

## Four parameter choices and complete interval coverage

In the published criterion rename its integer K as M, and choose

    M=xJ, L=5, R_1=5, S_1=1, R_2=rJ, S_2=S,
    R=rJ+4, N=5xJ, gamma=1/2-N/(6RS).

The four rows are used in order:

| Range for k/J | x | r | S | Upper limit T | Upper bound for ln b | k'/J is less than |
|---|---:|---:|---:|---:|---:|---:|
| k/J<=83 | 31/5 | 69/20 | 9 | 83 | 4.117 | 124 |
| 83<k/J<=89 | 63/10 | 7/2 | 9 | 89 | 4.170 | 126 |
| 89<k/J<=110 | 67/10 | 67/20 | 10 | 110 | 4.432 | 134 |
| 110<k/J<=256 | 42/5 | 21/5 | 10 | 256 | 5.044 | 168 |

All parameters are integers because20 divides J. Every M is at least12400,
so the factorial estimate applies. Since k>80J, H>20J>R_2. The first
cardinality condition follows from the five distinct powers81^(2z),
0<=z<5. The second follows from the injectivity of z+Hw on
0<=z<R_2,0<=w<S. In every row rS>=5x, so R_2*S>=ML>(M-1)L. In
particular RS>N and1/3<gamma<1/2. Congruence conditions modulo g=1
are vacuous. No multiplicative-independence assumption is needed.

With H<=(TJ+3)/4, the normalized parameter satisfies

    b<(449/100)*[rJ+3+(S-1)(TJ+3)/4]/[2(xJ-1)].

The ratio decreases with J: its numerator has positive slope and constant,
and its denominator is xJ-1. Evaluation at2000 therefore supplies a uniform
upper bound. Exact rational logarithm enclosures prove the displayed bounds
for ln b. Further,

    gamma*R/J = r/2+2/J-5x/(6S)
                <=r/2+1/1000-5x/(6S),
    gamma*S = S/2-5x/[6(r+4/J)]
                <=S/2-5x/[6(r+1/500)].

Finally3lnN/J<.018. To see this, write J=2000v,v>=1. Then
N<=84000v, ln84000<12, and lnv<=v-1 give lnN<12v=.006J.

The interpolation margin, divided by J, is strictly greater than

    4x*2.772-x*L_b-.018
      -5*{[r/2+.001-5x/(6S)]*4.396
                   +[S/2-5x/(6(r+.002))]*U},

where L_b is the row's logarithm upper bound. Its four exact positive
values are

    2389158679/81553500000,
    1120388537/18385500000,
    47604587/251400000,
    25238517/183837500.

Here we used ln2>.693 and ln3<1.099. Replacing -(M-1)lnb by
-M*L_b is valid since L_b>0 and ln b<L_b. Thus all criterion hypotheses
hold uniformly, yielding v_2(Lambda)<4ML=20xJ. This proves the last
column of the table.

For k/J>256, the already proved unbounded dyadic argument gives
k'<(38/25)k. Its hypotheses J>=100,D<J hold here. The proof uses the
alpha_1=9 normalization with q>=9; it does not assume an upper bound on k.

## Local loss and restart induction

The exact rational lower bounds delta>1.58496 and beta>.58496 imply

    .58496*(1.58496*82-124)>16/5,
    .58496*(1.58496*83-126)>16/5,
    .58496*(1.58496*89-134)>16/5,
    .58496*(1.58496*110-168)>16/5.

For the first row use y>=82J; for each later row use y>=k and the
preceding row's strict lower limit. Each gap delta*y-k' also exceeds J.
In the dyadic tail, beta*(delta-38/25)*k>(16/5)J follows already from
delta>19/12,beta>7/12 and k>256J. Consequently D<J implies

    k'<=delta*y-J,
    y''<=delta^2*y-(16/5)J.

If D>=J, the elementary bound instead gives y'<=delta*y-J.

For every y>=B choose J=20*floor(y/(20C)). This is a multiple of20,
is at least2000, satisfies y>=CJ, and exceeds y/C-20. Because
B/C>2000, we have J>=(99/100)y/C. Since82/83<99/100,

    epsilon*y<J.

The one-block endpoint and intermediate odd-run length are at most lambda*y.
The two-block endpoint is at most lambda^2*y, since
(delta^2-lambda^2)y<2delta*epsilon*y<(16/5)J.

Define G(y)=delta*y below B and G(y)=max(lambda*y,y+beta*B) above B.
It is continuous, increasing, between(3/2)y and delta*y, and equals lambda*y
for y>=2B. The same bounded-restart induction as in the fourth-power proof
bounds k_t by G^t(y_0) and y_t by delta*G^(t-1)(y_0). This induction
covers intermediate indices of two-block restarts, not just endpoints.
Since3^33>2^52, every virtual orbit from y_0>=1 reaches2B by step33.
The stated bounds follow, including t<33, with A=(delta/lambda)^33.

## Cycle consequences

Use exactly the published Simons-de Weger range table and Corollary13 as in
`cycle-bound-corollaries.md` and the fourth-power review manuscript. They
give y_0<10m for m>=1024 and
y_0/m<2/3+47/1024 for1024<=m<=515619. Directed rational bounds give

    10A/(lambda-1)<22.46,
    [A/(lambda-1)]*(2/3+47/1024)<1.60.

The first establishes K<22.46m*lambda^m before the following bootstrap.
The global map has the affine envelope G(y)<=lambda*y+epsilon*B.
With c=epsilon*B/(lambda-1), this implies
G^t(y_0)<=(y_0+c)*lambda^t-c. Substituting the established bound into
Corollary13 gives

    y_0<Q+14.3log_2(m)+13.3m*log_2(lambda),
    Q=1+13.3*.46057/ln2+13.3log_2(22.46).

Thus K is less than m*lambda^m times

    [13.3log_2(lambda)+(Q+14.3log_2(m)+c)/m]/(lambda-1).

This coefficient decreases for m>=515620. At the endpoint its exact
directed upper bound is less than15.19 (approximately15.189193). This proves
the large-range statement without circularity. The middle-range statement
follows directly from the preceding1.60 estimate.

## Evidence and scope

The proof above and its explicitly named predecessor arguments cover every
parameter value. The audit checks all displayed rational constants and
supplements them with high-precision parameter, factorial, virtual-orbit,
and large-integer Collatz challenges. Such finite challenges are not the
universal proof. No new finite-cycle exclusion is asserted by this note.

Primary theorem: Y. Bugeaud (1999), Theorem1, rational clause(6),
https://doi.org/10.1017/S0305004199003692 . The author-hosted version was
inspected at https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps .
Cycle input: Simons-de Weger, version1.44(2010), Theorem3(d), Corollary13,
https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf .
The bibliography, source caveats, and outstanding priority review in the
preceding manuscript apply unchanged.
