# A fourth-power normalization and a stronger block-growth bound

Private research draft, 29 September 2026. This is a separate extension of
two-regime-interpolation-bound.md. Independent mathematical review and priority
verification remain pending. No existing finite-search input is changed.

For delta=log_2(3), beta=delta-1, set

    epsilon=1/93, lambda=delta-epsilon,
    C=92, B=2^15, A=(delta/lambda)^28.

For every positive Collatz orbit, at its odd block starts,

    k_t<=A*y_0*lambda^t                       (t>=0),
    y_t<=delta*A*y_0*lambda^(t-1)             (t>=1).

Here y_t=log_2(n_t+1), k_t=v_2(n_t+1), and one block consists of a maximal
odd run followed by a maximal even run for the shortcut map. In particular,
lambda is about1.574210 and remains greater than1. This is not convergence.

## Normalization and interpolation hypotheses

Use n=a*2^k-1, b_0=2^ell-1 and D=ell+beta*log_2(a)-1 as in the earlier
note. Fix an even integer J>=200, and assume D<J and y>=92J. Then
ell<=J, log_2(a)<(12/7)(J+1), and k>90J.

Let r be the unique member of {0,1,2,3} with k+r divisible by4. Put

    H=(k+r)/4, alpha_1=81, alpha_2=-3^r*b_0/a,
    Lambda=81^H-alpha_2=3^r*(a*3^k+b_0)/a>0.

If v_2(a*3^k+b_0)<=3, the bounds below are immediate. Otherwise
alpha_2 is congruent to1 modulo16, since 81^H is. In Bugeaud (1999),
Theorem1, rational clause(6), use p=2, g=1, E=4, b_1=H, b_2=1, u=0,
and field parameters D_field=e=f=1, t=1. Indeed v_2(81-1)=4>1 and
v_2(alpha_2-1)>=4>=2. Both rational arguments are 2-adic units and the
linear form is nonzero. Its valuation is exactly that of a*3^k+b_0.

The logarithmic heights satisfy

    h(alpha_1)=4ln3,
    h(alpha_2)<(12/7)(J+1)ln2<=U*J,
    U=(12/7)*(201/200)*.6932.

For the latter, the denominator height is already bounded. The numerator
has binary logarithm less than J+3delta<J+5<(12/7)(J+1) for J>=200.
Reduction of the fraction cannot increase height. Negative rational
arguments are allowed by the cited theorem.

## Two explicit parameter choices

Let x and the upper limit T take the two pairs (7,120) and (9,256).
For k/J<=T choose

    M=xJ, L=5, R_1=5, S_1=1, R_2=xJ/2, S_2=10,
    R=xJ/2+4, S=10, N=5xJ.

All parameters are integers because J is even, and M>=1400. Also
R_2<=H because k>90J, while x<=9. The first cardinality condition
holds because the five powers 81^(2z), 0<=z<5, are distinct. The second
holds because the R_2*S_2 values z+Hw are distinct when R_2<=H, and
R_2*S_2=ML>(M-1)L. Congruence restrictions modulo g=1 are vacuous.
No multiplicative-independence assumption is required here.

The earlier factorial proof applies, giving a normalization factor below
(23/5)/(M-1). Since H<=(TJ+3)/4, the theorem's b obeys

    b<(23/5)*[(2x+9T)J+39]/[8(xJ-1)].

This ratio decreases with J. At J=200 it is below90 for (x,T)=(7,120),
and below150 for (9,256). Write gamma=1/2-N/(6RS), as both gamma
parameters of the theorem coincide when g=1. Exact identities imply

    gamma*R/J=x/6+2/J<=x/6+1/100,
    gamma*S=5-5xJ/(3xJ+24)<=1765/528<3343/1000.

The second expression decreases with xJ, whose minimum is1400.
Also 3lnN/J<.15: with J=200v, v>=1, use
N<=9000v, ln9000<10 and lnv<=v-1 to get lnN<10v=J/20.

The theorem's sufficient inequality is the same as (4) in the earlier
note, with E=4 and h(alpha_1)=4ln3. Using
ln2>.693, ln3<1.099, ln90<4.5 and ln150<5.011 gives the strict margins
after division by J:

    7*4*2.772-7*4.5-.15
      -5*[(353/300)*4.396+(3343/1000)*U]
      =73710029/525000000>0,

    9*4*2.772-9*5.011-.15
      -5*[(151/100)*4.396+(3343/1000)*U]
      =243378343/175000000>0.

The logarithm bounds have exact rational series checks. The theorem yields
v_2(Lambda)<4ML. Consequently

    k'<140J             if k/J<=120,
    k'<180J             if 120<k/J<=256.

For k/J>256, retain the earlier dyadic argument with alpha_1=9, which
gives k'<(38/25)k. Its assumptions hold for the present even J>=200.

## Retaining enough loss for the full fractional improvement

Recall the elementary inequalities

    y'<=delta*y-D,
    y''<=delta*y-D+beta*k'.

If D>=J, the first gives y'<=delta*y-J. If D<J, the three ranges above
give both k'<=delta*y-J and the stronger two-block endpoint

    y''<=delta^2*y-(16/5)J.                         (1)

For the first range use y>=92J, delta>19/12 and beta>7/12:

    delta*y-k'>(92*(19/12)-140)J=(17/3)J,
    beta*(delta*y-k')+D>(119/36)J>(16/5)J.

In the second range k>120J gives delta*y-k'>10J and hence a loss
greater than(35/6)J. In the last range the bound k'<(38/25)k gives
a gap greater than(19/300)k; at k>256J its product with7/12 exceeds
16J/5. Each gap exceeds J, proving the intermediate run bound as well.

For y>=B choose J=2*floor(y/(2C)), which is even and at least200.
Writing z=y/C, we have J<=z and J>z-2. Since z>=B/C>200,
J>=(99/100)y/C. The exact inequality

    epsilon*C=92/93<99/100

implies epsilon*y<J. The one-block endpoint and intermediate run
are therefore at most lambda*y. Since delta<8/5, (1) gives

    y''<=delta^2*y-(16/5)J<lambda^2*y.

Indeed (delta^2-lambda^2)y<2delta*epsilon*y<(16/5)J.
Keeping the actual two-block loss, rather than weakening it to
(delta+1)J, is what permits this larger epsilon.

Use the same global extension: G(y)=delta*y for y<=B and
G(y)=max(lambda*y,y+beta*B) for y>=B. It is continuous and increasing,
satisfies (3/2)y<=G(y)<=delta*y, and equals lambda*y above2B.
The one- or two-block restart induction proves k_t<=G^t(y_0) and
y_t<=delta*G^(t-1)(y_0). Since 3^28>2^44, every virtual orbit from
y_0>=1 reaches2B by step28. This proves the stated all-orbit bounds.

## An affine envelope and sharper cycle consequences

The same extension also satisfies, for every y>=1,

    G(y)<=lambda*y+epsilon*B.

For y<=B this is epsilon*y<=epsilon*B. For y>=B the linear term is
immediate; for the other term subtracting the right side leaves
(lambda-1)(B-y)<=0. Set c=epsilon*B/(lambda-1). Induction gives

    G^t(y_0)<=(y_0+c)*lambda^t-c.                   (2)

For a hypothetical nontrivial cycle, rotate to its minimum. The earlier
cycle-size calculation gives y_0<10m for m>=1024. Exact rational
coefficient bounds therefore imply

    K<21.08m*lambda^m,                             m>=1024,
    K<1.51m*lambda^m,                              1024<=m<=515619.

The second uses the sharper middle-range Y(m) from the published theorem,
exactly as in cycle-bound-corollaries.md.

There is a stronger large-range coefficient. Substitute the first bound
into Simons-de Weger, Corollary13. With

    Q=1+13.3*.46057/ln2+13.3log_2(21.08),

we obtain y_0<Q+14.3log_2(m)+13.3m*log_2(lambda). Summing (2) around
the cycle consequently gives

    K<[(y_0+c)/(lambda-1)]*lambda^m,
    K<15.17m*lambda^m,                             m>=515620. (3)

For (3), the coefficient upper bound

    [13.3log_2(lambda)+(Q+14.3log_2(m)+c)/m]/(lambda-1)

decreases for m>=515620, since both 1/m and log(m)/m decrease there.
At m=515620 an exact upward rational calculation puts it below15.17.
This uses an already established bound as input to Corollary13, so the
argument is not circular. The affine estimate improves the coefficient;
the fourth-power normalization and retained loss improve the base.

## Review scope

The supporting checks do not formalize the external p-adic theorem or
establish priority. This argument depends on the theorem statement and
factorial/dyadic/restart proofs documented in two-regime-interpolation-bound.md,
and the cycle-size inputs documented in cycle-bound-corollaries.md. It does
not depend on a newly computed finite basin or a new finite cycle exclusion.
