# An explicit Collatz block-growth bound below log_2(3)

A specialization of Bugeaud's p-adic interpolation theorem gives the
candidate all-orbit block-growth bound below, with base
lambda=log_2(3)-1/93, approximately 1.574210. The argument combines a
fourth-power normalization, two explicit interpolation ranges, a dyadic
tail, and a bounded restart construction. Published cycle-size estimates
then give K<15.17m*lambda^m for hypothetical cycles with m>=515620
local minima. The complete derivation is presented here. Independent
mathematical review and priority verification remain pending. The
Collatz conjecture remains open.

## Statement and conventions

Use T(n)=(3n+1)/2 for odd positive n and T(n)=n/2 for even n. A block
is a maximal odd run followed by a maximal even run. At the odd start
n_t define k_t=v_2(n_t+1) and y_t=log_2(n_t+1). Put
delta=log_2(3), beta=delta-1, and

    epsilon=1/93, lambda=delta-epsilon,
    C=92, B=2^15, A=(delta/lambda)^28.

The candidate theorem, for every positive orbit, is

    k_t<=A*y_0*lambda^t                         (t>=0),
    y_t<=delta*A*y_0*lambda^(t-1)               (t>=1).

The index counts blocks and lambda>1, so these bounds allow unbounded
trajectories. For a hypothetical nontrivial cycle, m counts local minima
and K is the sum of the m odd-run lengths. The cycle consequences are

    K<1.51m*lambda^m,                    1024<=m<=515619,
    K<15.17m*lambda^m,                   m>=515620.

The proposed contribution is the explicit specialization and its global
application. P-adic interpolation and normalized-exponent refinements
are established methods; novelty of this application is unconfirmed.

## Exact block identities

Write n=a*2^k-1, with a positive odd integer. Let ell>=1 be the
following maximal even-run length, b_0=2^ell-1, and n' the next odd
block start. Then

    n'=(a*3^k-1)/2^ell,
    k'=v_2(a*3^k+b_0)-ell,
    y=k+log_2(a).

With D=ell+beta*log_2(a)-1>=0, elementary logarithmic estimates give

    y' <= delta*y-D,
    y'' <= delta*y-D+beta*k'.                         (1)

For example, n'+1<(a*3^k)/2^ell+1<2*a*3^k/2^ell
gives the first bound. The second also uses y''<=y'+beta*k',
which follows by applying the first bound to the next block and
discarding ell'-1>=0. Always k<=y and y'<=delta*y.

## The published interpolation criterion

We use Bugeaud (1999), Theorem 1, rational clause (6) [1]. In the
rational, 2-adic setting used below, the theorem has the following form.
For two rational 2-adic units alpha_1, alpha_2 and positive integers
b_1=H, b_2=1, let Lambda=alpha_1^H-alpha_2 be nonzero. Our choices
have g=1, u=0, field parameters D_field=e=f=1 and t=1, with
v_2(alpha_1-1)>=E>1 and v_2(alpha_2-1)>=2.

Rename the theorem's integer K as M. For integers M>=3,L>=2 and
positive integers R_1,S_1,R_2,S_2, set

    R=R_1+R_2-1, S=S_1+S_2-1, N=ML,
    gamma=1/2-N/(6RS), P_M=product(i!,i=1,...,M-1),
    b=[R-1+(S-1)H]*P_M^(-2/[M(M-1)])/2.

The two cardinality requirements will be checked explicitly in each
range. If they hold and

    M(L-1)*E*ln2-3lnN-(M-1)lnb
      -gamma*L*R*h(alpha_1)-gamma*L*S*h(alpha_2)>0,

then v_2(Lambda)<=E(ML-1/2)<EML. For a reduced rational p/q, its
logarithmic height is h(p/q)=ln(max(|p|,|q|)). Negative rational arguments are allowed by the
theorem. Once the stated cardinalities hold, this criterion requires
no multiplicative-independence assumption.

## Factorial normalization and numerical logarithms

For every integer M>=800,

    P_M^(-2/[M(M-1)]) < (23/5)/(M-1).                (2)

Indeed ln(i!)>=i ln(i)-i+1 by integrating ln x. Since x ln x is
increasing for x>=1, a second integral comparison gives

    ln P_M >= ((M-1)^2/2)ln(M-1) - (M-1)^2/4 +1/4
                  - M(M-1)/2 + M-1.

Multiplying by -2/[M(M-1)] gives a quantity at most
-ln(M-1)+3/2+ln(M-1)/M. For M=800u, u>=1,
ln(M-1)<ln800+lnu<6.7+u-1<7.2u, using lnu<=u-1.
Consequently ln(M-1)/M<.009. Finally 1.509<ln(23/5), proving (2).
We may also use the weaker factor5/(M-1).

The numerical bounds used throughout are

    .693<ln2<.6932, ln3<1.099, ln264<5.576,
    ln(7/4)<.56, ln800<6.7, ln11<2.4.

The additional bounds ln90<4.5 and ln150<5.011 follow from
ln90=ln2+2ln3+ln5 and ln150=ln2+ln3+2ln5 using exact series
enclosures. Every numerical logarithm bound used here has a directed
rational check in the accompanying audit.

## Normalization and interpolation hypotheses

Use n=a*2^k-1, b_0=2^ell-1 and D=ell+beta*log_2(a)-1 with the preceding notation. Fix an even integer J>=200, and assume D<J and y>=92J. Then
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
    h(alpha_2)<(12/7)(J+1)ln2<=U_4*J,
    U_4=(12/7)*(201/200)*.6932.

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

The factorial proof above applies, giving a normalization factor below
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

Use the interpolation criterion with E=4 and h(alpha_1)=4ln3. Using
ln2>.693, ln3<1.099, ln90<4.5 and ln150<5.011 gives the strict margins
after division by J:

    7*4*2.772-7*4.5-.15
      -5*[(353/300)*4.396+(3343/1000)*U_4]
      =73710029/525000000>0,

    9*4*2.772-9*5.011-.15
      -5*[(151/100)*4.396+(3343/1000)*U_4]
      =243378343/175000000>0.

The logarithm bounds have exact rational series checks. The theorem yields
v_2(Lambda)<4ML. Consequently

    k'<140J             if k/J<=120,
    k'<180J             if 120<k/J<=256.

For k/J>256 we switch to the following dyadic argument. Both
normalizations concern the same integer a*3^k+b_0.

## The unbounded dyadic range

Assume D<J and k/J>256. Put r=k mod2, H=(k+r)/2,
alpha_1=9 and alpha_2=-3^r*b_0/a. Then
Lambda=3^r*(a*3^k+b_0)/a>0. If its valuation is at most2 the desired
bound is immediate. Otherwise alpha_2 is congruent to1 modulo8.
Thus the rational criterion applies with E=3 and the same field and
exponent parameters as before. Here h(alpha_1)=2ln3 and
h(alpha_2)<U_0*J, where U_0=525099/437500 follows from
(12/7)*(101/100)*.6932 and J>=100. Below, gamma>0.

Let q be the least integer with k/J<=2^q. Then q>=9 and
k/J>2^(q-1). Choose

    M=(q+1)J, L=q+2, R_1=L, S_1=1,
    R_2=(q-1)J, S_2=q+5.

Thus R=(q-1)J+q+1,S=q+5,N=(q+1)(q+2)J. Here M>=1000.
The inequality q-1<2^(q-2) gives R_2<H. Also
R_2*S_2=(q^2+4q-5)J>=ML>(M-1)L, because q>=9.
Again RS>N and 1/3<gamma<1/2.

The weaker factorial factor5, and H<=(2^q J+1)/2, give

    b < 5*{[2(q-1)+(q+4)2^q]J+3q+4}/[4((q+1)J-1)]
      <=(7/4)*2^q.

For the last step it suffices that
J[(2q-13)2^q-10q+10]>=7*2^q+15q+20. At J>=100 this
follows from (200q-1307)2^q>=1015q-980. The latter holds
for q>=9 already on replacing 2^q by512. Hence lnb<.6932q+.56.

The exact gamma formulas imply

    gamma*R/J=q/3-1/6-2/(q+5)+(q+1)/(2J)
               <=(203/600)q-97/600,
    gamma*S<=[1/2-350/2127]q+5/2-1400/2127.

For the second bound use (q+1)/[(q-1)J]<=9/700 and
(q+1)(q+2)/(q-1)=q+4+6/(q-1).
Finally 3lnN/J<q/25: lnJ<J/20, ln(q+2)<q/3, and
ln(q+1)<q/3 imply 3lnN/J<.15+.02q<.04q at q>=9.
The logarithm inequalities follow by writing J=100u or q+2=11u
and using lnu<=u-1, ln100<4.7 and ln11<2.4.

The interpolation margin, divided by J, is therefore greater than

    P(q)=(q+1)[(q+1)*2.079-.6932q-.56]-q/25
      -(q+2){[(203/600)q-97/600]*2.198
                +[(1/2-350/2127)q+5/2-1400/2127]*U_0}.

Its exact coefficients, from quadratic to constant, are

    1783170953/7444500000,
    -454813329/354500000,
    -1631430293/744450000.

The leading coefficient is positive,
P(9)=3011630363/531750000>5.66, and
P'(9)=1503066483/496300000>3.02. Expansion at 9 proves P(q)>0
for every real q>=9. The theorem yields k'<3J(q+1)(q+2).
At q=9, 3(q+1)(q+2)=330<(38/25)*256. The ratio of consecutive
left sides is (q+3)/(q+1)<=2, so induction proves

    3(q+1)(q+2)<(38/25)*2^(q-1)<(38/25)*(k/J).

The first cardinality is L because 9^(2z),0<=z<L, are distinct.
The second follows from R_2<=H, which makes z+Hw injective on the
stated rectangle. Thus all hypotheses are checked, and this proves
k'<(38/25)k throughout k/J>256.

## Retaining enough loss for the full fractional improvement

Use the elementary inequalities

    y'<=delta*y-D,
    y''<=delta*y-D+beta*k'.

If D>=J, the first gives y'<=delta*y-J. If D<J, the three ranges above
give both k'<=delta*y-J and the stronger two-block endpoint

    y''<=delta^2*y-(16/5)J.                         (3)

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
are therefore at most lambda*y. Since delta<8/5, (3) gives

    y''<=delta^2*y-(16/5)J<lambda^2*y.

Indeed (delta^2-lambda^2)y<2delta*epsilon*y<(16/5)J.
Keeping the actual two-block loss, rather than weakening it to
(delta+1)J, is what permits this larger epsilon.

Define the global extension by G(y)=delta*y for y<=B and
G(y)=max(lambda*y,y+beta*B) for y>=B. It is continuous and increasing,
satisfies (3/2)y<=G(y)<=delta*y, and equals lambda*y above2B.
Below B, apply the elementary one-block estimate. Above B, use the
proved one- or two-block alternative, G(y)>=lambda*y, and monotonicity.
Induction along the selected restart times bounds each endpoint by the
corresponding virtual iterate G^t(y_0). At the single intermediate block
of a two-block restart, the bound on k' gives k_t<=G^t(y_0), while
y'<=delta*y gives y_t<=delta*G^(t-1)(y_0). At endpoints the latter also
follows from G<=delta*y. This covers every block index.

Since 3^28>2^44, (3/2)^28>2B. Every virtual orbit from y_0>=1 reaches
2B by step28. Before that point use G<=delta*y, and afterwards use
G=lambda*y, to get G^t(y_0)<=A*y_0*lambda^t, including t<28.
This proves the stated all-orbit bounds.

## An affine envelope and sharper cycle consequences

The same extension also satisfies, for every y>=1,

    G(y)<=lambda*y+epsilon*B.

For y<=B this is epsilon*y<=epsilon*B. For y>=B the linear term is
immediate; for the other term subtracting the right side leaves
(lambda-1)(B-y)<=0. Set c=epsilon*B/(lambda-1). Induction gives

    G^t(y_0)<=(y_0+c)*lambda^t-c.                   (4)

For a hypothetical nontrivial cycle, rotate to its minimum. Simons-de Weger [2], Theorem3(d), gives K<16m*delta^m for m>=91
after coarsening its three applicable coefficients. Corollary13 gives
n_min<m*exp(13.3*(.46057+lnK)). Consequently, with a_0=log_2(delta),

    y_0<1+13.3*.46057/ln2+53.2+14.3log_2(m)+13.3a_0*m.

For m>=1024 use ln2>.69, a_0<2/3, and log_2(m)<=m/64. The
constant term is below64, and
13.3*(2/3)+14.3/64+64/1024<10. The logarithm inequality holds at1024
and its difference increases thereafter. The bound a_0<2/3 follows
from delta<317/200 and (317/200)^3<4. Thus y_0<10m.
Exact rational coefficient bounds now imply

    K<21.08m*lambda^m,                             m>=1024,
    K<1.51m*lambda^m,                              1024<=m<=515619.

For the second bound, Theorem3(d) gives n_min<51825000*m^2*delta^m
when91<=m<=515619. Hence

    y_0<Y(m)=1+log_2(51825000)+2log_2(m)+a_0*m.

Since 51825000<2^26 and log_2(m)/m decreases for m>=1024,
Y(m)/m<2/3+47/1024. The exact audit checks
[A/(lambda-1)]*[2/3+47/1024]<1.51. Summing the block estimates
therefore gives the stated middle-range coefficient.

There is a stronger large-range coefficient. Substitute the first bound
into Simons-de Weger, Corollary13. With

    Q=1+13.3*.46057/ln2+13.3log_2(21.08),

we obtain y_0<Q+14.3log_2(m)+13.3m*log_2(lambda). Summing (4) around
the cycle consequently gives

    K<[(y_0+c)/(lambda-1)]*lambda^m,
    K<15.17m*lambda^m,                             m>=515620. (5)

For (5), the coefficient upper bound

    [13.3log_2(lambda)+(Q+14.3log_2(m)+c)/m]/(lambda-1)

decreases for m>=515620, since both 1/m and log(m)/m decrease there.
At m=515620 an exact upward rational calculation puts it below15.17.
This uses an already established bound as input to Corollary13, so the
argument is not circular. The affine estimate improves the coefficient;
the fourth-power normalization and retained loss improve the base.

## Verification and prior work

The written proof covers all parameter values; finite numerical challenges
only supplement it. Exact rational audits check the constants, and Lean
checks selected algebra, congruence, local-loss, envelope and restart
lemmas. The published p-adic theorem, the full specialization, and the
cycle-size inputs are not formally verified here. A domain expert should
review the source hypotheses and both universal parameter arguments.

The normalized-exponent method is established transcendence theory [3].
Luca [4] proves a related effective relation between cycle complexity and
height, using a run parameter that counts blocks with k_i>=2 and can be
smaller than m. The explicit smaller base in this manuscript still needs
a complete priority review. None of these estimates excludes arbitrary
cycles or proves the Collatz conjecture.

## Primary references

[1] Y. Bugeaud, Linear forms in p-adic logarithms and the Diophantine
equation (x^n-1)/(x-1)=y^q, Mathematical Proceedings of the Cambridge
Philosophical Society 127(3)(1999),373-381, Theorem 1, clause (6).
https://doi.org/10.1017/S0305004199003692
Author's complete PostScript, pages 3-4 visually inspected after local
rendering: https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps
The author version explicitly uses logarithmic heights. A comparison
with the final journal text remains desirable; no unread text is assumed.

[2] J. Simons and B. de Weger, Theoretical and computational bounds
for m-cycles of the 3n+1 problem, version 1.44, 31 August 2010,
Theorem 3(d) and Corollary 13.
https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf

[3] Y. Bugeaud, B-prime, arXiv:2209.00275(2022), Section 1, for the
history of normalized-exponent refinements: https://arxiv.org/abs/2209.00275

[4] F. Luca, On the non-trivial cycles in Collatz's problem,
SUT Journal of Mathematics 41(1)(2005),31-41. Theorem 2.1 is relevant
prior work on exponential cycle-complexity bounds. Its run parameter
counts the blocks with k_i>=2, and can be smaller than m. Its displayed
height recurrence uses a geometric factor at least delta, rather than
the explicit smaller base established in the present derivation.
https://www.rs.tus.ac.jp/sutjmath/_userdata/41-1/03-luca.pdf
