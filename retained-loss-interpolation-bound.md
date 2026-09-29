# Retaining the elementary loss in the interpolation argument

Private candidate result, 29 September 2026. This is a mathematical refinement
of the preceding block-growth bounds, subject to independent review and priority
verification. It does not prove the Collatz conjecture.

## Statement

Use the shortcut Collatz map and maximal odd/even blocks of the preceding
fourth-power proof. At an odd block start n, put k=v_2(n+1), y=log_2(n+1),
delta=log_2(3), and beta=delta-1. The following explicit constants give

    epsilon=1/80, lambda=delta-epsilon,
    B=1272000, A=(delta/lambda)^32,
    k_t<=A*y_0*lambda^t                       (t>=0),
    y_t<=delta*A*y_0*lambda^(t-1)             (t>=1).

This improves the exponential base from delta-1/83 to delta-1/80. The larger
height cutoff has a cost in the leading constants. Neither estimate dominates
the other in every finite calculation.

## The loss that was previously discarded

Write n=a*2^k-1 with a odd, and let ell be the following even-run length. Set

    D=ell+beta*log_2(a)-1>=0.

The exact elementary block inequalities used before are

    y'<=delta*y-D,
    y''<=delta*y-D+beta*k'
        =delta^2*y-D-beta*(delta*y-k').

The previous local proof bounded the last loss using only the beta term. Here
we keep D when it is large; when D is small the logarithmic height in the
interpolation theorem becomes smaller. These are two exhaustive alternatives,
not assumptions about typical trajectories.

Fix J divisible by 100, J>=10000, and y>=79.5J. If D>=J, the one-block
alternative y'<=delta*y-J already suffices. Otherwise split into

    I: 0<=D<=.9J,       II: .9J<D<J.

In either stratum write a_-=0,a_+=.9 for I and a_-=.9,a_+=1 for II.
Then ell<a_+J+1 and log_2(a)<(12/7)(a_+J+1), using beta>7/12.
The resulting strict upper bound is safe also at the closed boundary D=.9J:
ell<=D+1 and beta*log_2(a)=D-ell+1<=D.
In particular k>77J.

## Fourth-power normalization and hypotheses

Choose r_0 in {0,1,2,3} so that k+r_0 is divisible by 4, and H=(k+r_0)/4.
Apply Bugeaud (1999), Theorem 1, rational clause (6), exactly as in the
fourth-power note, with

    alpha_1=81, alpha_2=-3^r_0*(2^ell-1)/a,
    Lambda=81^H-alpha_2,
    p=2, g=1, E=4, b_1=H, b_2=1, u=0,
    D_field=e=f=t=1.

If v_2(Lambda)<=3, all bounds below are immediate. Otherwise alpha_2 is
1 modulo 16 and both required valuations are at least 4. Signed rational
arguments are permitted by the cited theorem. The result is nonzero because
alpha_1^H>0>alpha_2. Reduction of the rational alpha_2 cannot increase its height.

The logarithmic heights satisfy

    h(alpha_1)=4ln3,
    h(alpha_2)<U*J,
    U=(12/7)(a_++1/10000)*.69314719.

For the numerator, its binary logarithm is less than ell+3delta, which is
less than a_+J+1+3delta<(12/7)(a_+J+1); the last inequality is uniform for
J>=10000 and a_+>=.9. The denominator follows from the preceding bound for a.

## Factorial bound and exact parameter table

For M>=60000, the already proved integral estimate gives

    -2ln(product(i!,1<=i<M))/(M(M-1))
      <=-ln(M-1)+3/2+ln(M-1)/M.

Write M=60000u, u>=1. Since ln60000<12 and lnu<=u-1,
ln(M-1)<12u, so the last quotient is less than .0002. Exact rational
logarithm enclosures prove 1.5002<ln4.483. Therefore the factorial factor
in the interpolation criterion is strictly less than 4.483/(M-1).

Set M=xJ,L=5,R_1=5,S_1=1,R_2=rJ,S_2=S. Thus R=rJ+4,N=5xJ and
gamma=1/2-N/(6RS). Use these rows in order within each stratum:

| Stratum | Lower height/J for the loss | Upper k/J | x | r | S | Valuation bound/J |
|---|---:|---:|---:|---:|---:|---:|
| I | 79.5 | 102.41 | 6.02 | 3.01 | 10 | 120.4 |
| I | 102.41 | 256 | 7.84 | 3.92 | 10 | 156.8 |
| II | 79.5 | 79.95 | 6.10 | 3.39 | 9 | 122.0 |
| II | 79.95 | 80.92 | 6.13 | 3.41 | 9 | 122.6 |
| II | 80.92 | 86.03 | 6.21 | 3.45 | 9 | 124.2 |
| II | 86.03 | 109.43 | 6.62 | 3.68 | 9 | 132.4 |
| II | 109.43 | 256 | 8.47 | 4.24 | 10 | 169.4 |

The first row of each stratum uses the assumed y>=79.5J. Subsequent rows
apply after k exceeds the preceding endpoint, and use y>=k. All parameters
are integers because 100 divides J; M>=60200. Also R_2<H because k>77J
and r<=4.24. Distinct powers of 81 prove the first cardinality condition;
injectivity of z+Hw on 0<=z<R_2,0<=w<S proves the second, because
rS>=5x and hence R_2*S>=ML>(M-1)L. No multiplicative independence is needed.

For upper endpoint T, the normalized interpolation parameter obeys

    b<4.483*[rJ+3+(S-1)(TJ+3)/4]/[2(xJ-1)].

The right side decreases with J. Moreover

    gamma*R/J<=r/2+.0002-5x/(6S),
    gamma*S<=S/2-5x/[6(r+.0004)],
    3lnN/J<.0039.

For the last inequality use J=10000v, N<=423500v, ln423500<13 and
lnv<=v-1. The exact rational auditor encloses ln b at J=10000 upward
to five decimal places. With that upper bound L_b, it checks the positive
margin

    16x*.69314718-x*L_b-.0039
      -5*{[r/2+.0002-5x/(6S)]*4*1.09861229
                 +[S/2-5x/(6(r+.0004))]*U}>0.

The logarithmic constants are all checked by directed rational series.
This is precisely a sufficient lower bound for the published interpolation
criterion divided by J, uniformly for every admissible J. It follows that
v_2(Lambda)<4ML=20xJ, and therefore k'<20xJ. The complete rational margins
are saved in results/retained-loss-exponential-bound-audit.json.

## Local loss in all ranges

For each row let h be its lower height/J. The auditor checks exactly

    g=1.5849625*h-20x>1,
    a_-+.5849625*g>16/5.

Consequently k'<=delta*y-J and

    y''<=delta^2*y-D-beta*(delta*y-k')
        <=delta^2*y-(16/5)J.

The term a_- is retained in stratum II. For k/J>256, the previously proved
unbounded dyadic argument gives k'<(38/25)k. Its hypotheses J>=100 and D<J
hold here. The weaker exact bounds delta>19/12,beta>7/12 already imply
beta*(delta-38/25)*256>16/5 and delta-38/25>1/256. Thus the same local
alternative holds beyond the finite table. This covers every k and D.

## Global induction and cycle bounds

Take C=79.5 and, for y>=B, choose J=100*floor(y/(100C)). The general
rounding lemma applies because

    C*10000=795000,
    100C/(1-C/80)=1272000=B.

Thus J>=10000, y>=CJ, and J>y/80. The one-block endpoint and the
intermediate run length are at most lambda*y. The two-block endpoint is
at most lambda^2*y, since 2delta*epsilon-epsilon^2<(16/5)epsilon.

Use the same continuous increasing envelope

    G(y)=delta*y                     for y<=B,
    G(y)=max(lambda*y,y+beta*B)       for y>=B.

The already established restart induction bounds k_t by G^t(y_0) and y_t
by delta*G^(t-1)(y_0), including indices inside two-block restarts. Exact
inequalities lambda>1.57, 1.03(lambda-1)>beta, and

    157^32>103*1272000*100^31

put every virtual orbit from y_0>=1 in the linear region by step 32. This
proves the statement with A=(delta/lambda)^32.

The same published Simons-de Weger cycle inputs and affine bootstrap from
cycle-bound-corollaries.md give explicit upper coefficients for K/(m*lambda^m).
The receipt records upward rational constants for the basic m>=1024 bound,
the sharper 1024<=m<=515619 bound, and the affine m>=515620 bound. The
bootstrap first proves the basic bound, then substitutes it in Corollary 13;
it has no circular dependency.

## Scope and references

The universal proof is the inequalities above and the cited predecessor
lemmas. The auditor checks their exact constants and supplements them with
large-parameter, rounding-boundary, virtual-orbit and exact-integer challenges.
Those finite challenges are not the universal argument. Existing finite
capacity certificates remain frozen; this result is not automatically grafted
onto any of them.

Primary theorem: Y. Bugeaud (1999), Theorem 1, rational clause (6),
https://doi.org/10.1017/S0305004199003692 ; inspected author source:
https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps . The source-version
caveat in results/interpolation-primary-source-provenance.json remains in force.
Cycle input: Simons-de Weger, version 1.44 (2010), Theorem 3(d), Corollary 13,
https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf .
