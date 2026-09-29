# Explicit block-growth bounds and finite-cycle exclusions for the 3n+1 problem

The arguments and computational claims below have internal checks;
independent mathematical review and priority confirmation are pending.

We give an explicit bound for every positive Collatz orbit, indexed by maximal
odd/even blocks, with exponential base lambda=log_2(3)-1/80. A retained
elementary loss, two height strata, explicit fourth-power interpolation
parameters, an unbounded dyadic argument and a restart envelope yield the
bound. Published cycle estimates then give K<1.61m*lambda^m for
1024<=m<=515619 and K<15.27m*lambda^m for m>=515620. Separately,
exact finite certificates support a candidate exclusion through 100 local
minima, extending the journal result through 91 and the located preprint
claim through 95. We give the mathematical reduction, source-bound evidence,
and reproduction instructions. Neither result proves the Collatz conjecture.

## 1. Statements and conventions

Use T(n)=(3n+1)/2 for odd positive n and T(n)=n/2 for even n. A block
consists of a maximal odd run followed by a maximal even run. At its odd
start n_t define k_t=v_2(n_t+1) and y_t=log_2(n_t+1). Let

    delta=log_2(3), beta=delta-1, epsilon=1/80,
    lambda=delta-epsilon, B=1272000, A=(delta/lambda)^32.

Theorem 1 (analytic bound). For every positive orbit, from every odd block
start, the following estimates hold:

    k_t<=A*y_0*lambda^t                         (t>=0),
    y_t<=delta*A*y_0*lambda^(t-1)               (t>=1).

Numerically lambda is approximately 1.572462500721156 and A approximately
1.288362904142. Theorem 2 (cycle bound). For a hypothetical nontrivial
positive cycle with m local minima and K odd shortcut steps,

    K<1.61m*lambda^m,                    1024<=m<=515619,
    K<15.27m*lambda^m,                   m>=515620.

The index m counts blocks, not total cycle length. Theorem 3
(computer-assisted candidate). The completed certificates exclude
92<=m<=100. Together with Hercher [4] this gives exclusion through 100,
subject to the stated external inputs and independent review. The proof
chain through 100 does not depend on any unfinished m=101 computation.

The comparison for Theorem 2 is the explicit delta^m upper bound in
Simons-de Weger [2]. At m=1024 the displayed new bound is over 3,000 times
smaller: approximately 3.28*10^204 instead of 9.99*10^207. Both are still
very large. A smaller exponential base is an asymptotic improvement, not
a convergence theorem; lambda remains greater than one.


## 2. Exact block identities

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


## 3. The published interpolation criterion

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


## 4. A factorial estimate used in both ranges

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


## 5. Retaining the elementary loss

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


## 6. Fourth-power normalization and hypotheses

Choose r_0 in {0,1,2,3} so that k+r_0 is divisible by 4, and H=(k+r_0)/4.
Apply Bugeaud (1999), Theorem 1, rational clause (6), with the following choices, with

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


## 7. Exact parameters for the two loss strata

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
v_2(Lambda)<4ML=20xJ, and therefore k'<20xJ. The companion exact audit records every rational margin.


## 8. Local loss in every range

For each row let h be its lower height/J. The auditor checks exactly

    g=1.5849625*h-20x>1,
    a_-+.5849625*g>16/5.

Consequently k'<=delta*y-J and

    y''<=delta^2*y-D-beta*(delta*y-k')
        <=delta^2*y-(16/5)J.

The term a_- is retained in stratum II. For k/J>256, the following
unbounded dyadic argument gives k'<(38/25)k. Its hypotheses J>=100 and D<J
hold here. The weaker exact bounds delta>19/12,beta>7/12 already imply
beta*(delta-38/25)*256>16/5 and delta-38/25>1/256. Thus the same local
alternative holds beyond the finite table. This covers every k and D.


## 9. The unbounded dyadic argument

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


## 10. Global restart induction

Set C=79.5. For y>=B choose J=100*floor(y/(100C)). Then J is a multiple
of 100, and the exact conditions

    C*10000=795000<=B,
    100C/(1-C/80)=1272000=B

give J>=10000, y>=CJ and

    J>y/C-100>=epsilon*y.

The preceding alternatives therefore bound either the next height by
lambda*y, or both the intermediate odd-run length by lambda*y and the
two-block height by lambda^2*y. The latter follows from
2delta*epsilon-epsilon^2<(16/5)epsilon.

Define G(y)=delta*y for y<=B, and G(y)=max(lambda*y,y+beta*B) for y>=B.
It is continuous and increasing, and lambda*y<=G(y)<=delta*y. Below B
use the elementary one-block inequality. Above B use the proved alternative
and monotonicity. Induction along the selected restart times bounds every
restart endpoint by the corresponding virtual iterate G^t(y_0). At the
single intermediate index of a two-block restart, the checked run bound
gives k_t<=G^t(y_0), while y'<=delta*y gives
y_t<=delta*G^(t-1)(y_0). At restart endpoints the latter follows from
G(y)<=delta*y. Thus every block index is covered, not just restart times.

For y>=beta*B/(lambda-1), G(y)=lambda*y. Directed rational checks give
lambda>1.57 and 1.03(lambda-1)>beta. The integer inequality

    157^32>103*1272000*100^31

therefore puts every virtual orbit from y_0>=1 in the linear region by
step 32. Before that time use G<=delta*y, and afterwards G=lambda*y.
Consequently G^t(y_0)<=A*y_0*lambda^t, including t<32. This proves
Theorem 1. The virtual envelope reaching its linear regime does not assert
that an actual orbit grows or reaches any particular height.


## 11. Cycle consequences and comparison

The same extension also satisfies, for every y>=1,

    G(y)<=lambda*y+epsilon*B.

For y<=B this is epsilon*y<=epsilon*B. For y>=B the linear term is
immediate; for the other term subtracting the right side leaves
(lambda-1)(B-y)<=0. Set c=epsilon*B/(lambda-1). Induction gives

    G^t(y_0)<=(y_0+c)*lambda^t-c.                   (3)

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

    K<22.51m*lambda^m,                             m>=1024,
    K<1.61m*lambda^m,                              1024<=m<=515619.

For the second bound, Theorem3(d) gives n_min<51825000*m^2*delta^m
when91<=m<=515619. Hence

    y_0<Y(m)=1+log_2(51825000)+2log_2(m)+a_0*m.

Since 51825000<2^26 and log_2(m)/m decreases for m>=1024,
Y(m)/m<2/3+47/1024. The exact audit checks
[A/(lambda-1)]*[2/3+47/1024]<1.61. Summing the block estimates
therefore gives the stated middle-range coefficient.

There is a stronger large-range coefficient. Substitute the first bound
into Simons-de Weger, Corollary13. With

    Q=1+13.3*.46057/ln2+13.3log_2(22.51),

we obtain y_0<Q+14.3log_2(m)+13.3m*log_2(lambda). Summing (3) around
the cycle consequently gives

    K<[(y_0+c)/(lambda-1)]*lambda^m,
    K<15.27m*lambda^m,                             m>=515620. (4)

For (4), the coefficient upper bound

    [13.3log_2(lambda)+(Q+14.3log_2(m)+c)/m]/(lambda-1)

decreases for m>=515620, since both 1/m and log(m)/m decrease there.
At m=515620 an exact upward rational calculation puts it below15.27.
This uses an already established bound as input to Corollary13, so the
argument is not circular. This proves Theorem 2. The affine estimate improves the coefficient;
the fourth-power normalization and retained loss improve the base.


## 12. Sharp majorization for cyclic growth constraints

Let b be real, let m>=1, and let Phi:[b,infinity)->[b,infinity) be continuous and strictly increasing, with Phi(x)>=x. Define its truncated inverse Psi by

    Psi(t)=b,                         b<=t<=Phi(b),
    Psi(t)=Phi^(-1)(t),              t>Phi(b).

Then Psi is continuous, nondecreasing, and Psi(t)<=t. For any S>=m*b there is a unique t>=b such that

    w_j=Psi^(m-j)(t),  j=1,...,m,    sum_j w_j=S.

Existence and uniqueness follow because this sum is continuous and strictly increasing in t (its last term is t), starts at m*b, and tends to infinity.

Theorem 4. The increasing vector w majorizes every cyclic vector x with x_i>=b, x_(i+1)<=Phi(x_i), and sum_i x_i=S. Consequently, for every convex f,

    sum_i f(x_i) <= sum_j f(w_j).

The bound is attained by w itself arranged in increasing cyclic order.

Proof. Sort x into u_1<=...<=u_m. For every j<m, an edge of the original cycle goes from the set of j smallest vertices to its complement. Its starting value is at most u_j and its ending value is at least u_(j+1). Monotonicity gives

    u_(j+1)<=Phi(u_j), equivalently u_j>=Psi(u_(j+1)).

Suppose an increasing prefix through j had sum smaller than the corresponding w-prefix. If w_j=b this is impossible because all u_i>=b. Otherwise u_j<w_j: indeed u_j>=w_j would imply

    u_i>=Psi^(j-i)(u_j)>=Psi^(j-i)(w_j)=w_i

for every i<=j, contradicting the smaller prefix sum. Since w_j>b, all subsequent inverse steps are untruncated, so w_(j+r)=Phi^r(w_j). Strict monotonicity now gives u_(j+r)<w_(j+r) for every r>=1. The smaller prefix and smaller remaining suffix contradict equality of total sums. Thus every increasing prefix of u is at least the corresponding prefix of w, which is exactly the majorization assertion. Finally w_(j+1)<=Phi(w_j), including at the floor transition; the wraparound inequality holds because w_1<=w_m<=Phi(w_m). This proves feasibility and sharpness. End of proof.

The linear geometric-ramp lemma is the special case Phi(x)=d*x after shifting the floor. The proof does not require Phi to be concave or differentiable.


## 13. A subordinate envelope for periodic run lengths

Suppose a periodic sequence of actual heights y_i>=b and positive odd-run lengths k_i satisfies

    k_(i+t)<=Phi^t(y_i) for every t>=0.

Write v_i=max(b,k_i), and set

    z_i=max_(t>=0) Psi^t(v_(i+t)).

It is enough to take 0<=t<m: periodicity and Psi^m(x)<=x make every later term no larger than its predecessor m places earlier. The future-run bounds and y_i>=b give z_i<=y_i. Also z_i>=v_i and

    z_i=max(v_i,Psi(z_(i+1))),

so z_(i+1)<=Phi(z_i). Thus sum_i z_i>=sum_i k_i=K.

If K>=m*b and sum_i z_i>K, cap every z_i at a common T>=b until the sum is K. This preserves the growth constraint for any Phi as above: if z_i<=T the previous edge inequality remains sufficient; if z_i>T, the capped successor is at most T<=Phi(T). A suitable T exists by continuity of sum_i min(z_i,T). This avoids a concavity assumption that a straight-line interpolation would require.

For any decreasing convex f, capping only increases the objective. Applying the sharp theorem gives an upper bound for sum_i f(y_i) from the extremal vector of total K. A proved lower bound K0<=K can be used in exactly the same way by capping to total K0, provided K0>=m*b. If K0<m*b, the direct bound m*f(b) applies.

For Collatz, use f(y)=1/(2^y-1). This converts a certified nonlinear future-run bound into an exact profile bound for the cycle logarithmic identity.


## 14. Certified finite-cycle application

We also give a computer-assisted candidate exclusion of nontrivial positive
cycles with 92 through 100 local minima. Together with Hercher's exclusion
through 91 [4], including its published corrigendum, this would exclude all
nontrivial positive cycles with at most 100 local minima. Here m is the number
of maximal odd/even blocks, not the number of integers in a cycle. The
strongest analytic theorem above is a separate result: the completed finite
certificates use earlier, already frozen specializations with epsilon=1/160
or 1/93. No unfinished stronger-map experiment is an input to these claims.

The external computational input is Barina's published verification below
X=2^71 [3]; X itself is a power of two and converges. Consequently a
hypothetical nontrivial cycle has every member greater than X. We have not
repeated that full convergence verification. Wang's 2026 preprint [5] states
an exclusion through 95 and supplies parity-prefix code. We inspected the
manuscript and the latest downloadable source, but do not use its claimed
exclusion as an input: our exact profiles independently cover 92 through 95.

### The finite restart map

Define, on y>=71,

    Phi(y)=max(delta*y-40.99,
                min(delta*y-37.99,y+71*(delta-1)-37.99)).

This continuous increasing map has slopes at least one and Phi(y)>=y.
A sufficient restart witness at a block start is a finite r>=1 with

    k_j<=Phi^j(y_0) for 0<=j<r,   y_r<=Phi^r(y_0).

Monotonicity and strong induction then give k_t<=Phi^t(y_0) for every t.
Every intermediate run must be checked. Alternatively, verified entry into
the convergence basin eliminates the starting value from any nontrivial cycle.

The finite reduction uses the elementary one- and two-block inequalities,
Bugeaud (2002), Theorem 2 [8], and an exhaustive modular sweep. It confines
exceptions to k<200, ell<=40, and odd parts below 2^69. The large-exponent
estimate is v_2(a*3^k+2^ell-1)<1700*(ln k+2)^2+3<k for k>=2^19;
the last comparison extends from its cutoff by monotonicity. For the remaining
range, the modular sweep verifies 40*(2^19-1)=20,971,480 pairs and the bound
on the next odd-run length s<=100. Exact sufficient inequalities remove
the range k>=200. The surviving input consists of 44,497 residue classes
containing exactly 144,429,913,922,369,056,364 seeds.

Two complete algorithms discharge that same input. The first branches using
inverse residues and exact affine formulas; the second bisects arithmetic
progressions by parity. They use 1,648,100,522 and 1,253,664,985 nodes,
respectively. Every class finishes, coverage totals agree, and the maximum
restart depth is five. Their different partition rules give different node
counts. Neither count is presented as an independent mathematical theorem.

For a progression of odd parts a, a later minimum has the form
n_j=(P*a+Q)/2^S with P>0 and Q+2^S>=0. The restart difference
Phi^j(k_root+log_2(a))-log_2(n_j+1) is nondecreasing: after multiplying
its derivative by a*ln2, it is at least

    1-P*a/(P*a+Q+2^S)>=0.

Continuity covers the breakpoints of Phi. Thus a successful least-endpoint
test certifies the entire progression. Whole-family basin tests instead use
the greatest endpoint. Integer logarithm bounds and a rational mantissa grid
give directed comparisons. Python independently checks all 2,032,128 grid
thresholds and 112 selected progression cases, including difficult cases.
It does not repeat all 44,497 classes. The full two-algorithm proof is native
integer code, with its sources, inputs, counters and hashes retained.

### Joining the analytic tail

For each of (epsilon,B)=(1/160,16384) and (1/93,32768), define

    F(y)=min(Phi(y),(delta-epsilon)*y+epsilon*B-40.99).

The earlier analytic specializations establish a one- or two-block restart
above B. Their proofs are included in the accompanying sources. The two
formulas meet at B, and F is continuous, increasing, at least the identity,
with slopes at least one. Merely taking a minimum of restart maps would
not prove a restart property; the following extra check is essential.

Above B, the analytic restart transfers because epsilon*B-40.99>0 and
F(y)>=y. Below B, all finite witnesses stay below the joining point:
the maximum initial upper height is 117 and delta^5*117<B. Nonexceptional
small-k witnesses satisfy delta^2*300<B. In the middle range k>=200,
the old sweep gives s<=100, and the global lower bound
F(y)>=(delta-epsilon)*y-40.99 gives a two-block witness from the exact
positive margin

    ((delta-epsilon)^2-delta)*200
      -(delta-epsilon+1)*40.99-(delta-1)*100>0.

The companion intermediate-run check is
(delta-epsilon)*200-40.99>100. These checks handle a virtual step crossing B.
The source-bound graft audits verify these inequalities and the actual finite
root heights and depths. Thus each F is valid for every basin-avoiding orbit,
in particular every hypothetical nontrivial cycle.

### Rational approximation and the finite window

Let H be the total number of binary divisions in a hypothetical shortcut
cycle and K its number of odd steps. The cycle product identity and the
geometric bound for reciprocals along each odd run give

    0<H/K-delta<(1/(K*ln2))*sum_i 1/n_i,

where n_i are the m local minima. Apply the growth-constrained majorization
theorem proved above to F and f(y)=1/(2^y-1). An established lower bound
K_0<=K gives an explicit upper bound for the reciprocal sum. Directed rational
intervals for delta and ln2 then give an open interval containing H/K.
Exact Stern-Brocot bracketing finds its minimum possible denominator and
therefore a new lower bound on K. The saved determinant-one neighbors
certify that step independently. Iterate until the lower bound exceeds
the applicable published upper bound 1.4784*m*delta^m [2].

For m=96,97,98 the completed profiles close directly at X. The cases 99
and 100 first require excluding least minima in [X,11X] and [X,15X],
respectively. Necessary prefix targets come from the remaining run capacity:
with A_r(y)=sum_(j=0)^(r-1) F^j(y), a prefix of i blocks obeys

    A_(m-i)(y_i)>=K_0-ceil(A_i(B_0)),

where B_0 is a proved upper bound on the starting height in that window.
Upward rational evaluation of A and a positive-series lower bound for 2^h
certify necessary integer targets for each later minimum.

The exact prefix search represents n_i=(P*n_0+Q)/2^S. Specifying an odd
run and its following even run adds congruences modulo powers of two;
intersecting them with the original interval produces disjoint residue
classes. A branch closes only by an empty class, descent below the assumed
global minimum, or violation of a necessary target. Singleton branches are
iterated exactly. A resource or depth limit is unresolved, never a successful
exclusion. Independent partition audits reconstruct coverage from the source
configuration and verify that the complete job list covers the window.

| m | Minimum factor after search | Prefix nodes | Completed verification |
|---|---:|---:|---|
| 96 | 1 | No additional window | Exact forward and inverse profiles |
| 97 | 1 | No additional window | Exact forward and inverse profiles |
| 98 | 1 | No additional window | Exact forward and inverse profiles |
| 99 | 11 | 2,758,731,446 | Full original-integer repeat and all audits |
| 100 | 15 | 14,528,184,145 | Complete partition, journal and fallback audits |

The m=99 repeat uses a different initial partition; after accounting for
the partition boundaries its seven substantive counters agree exactly. For
m=100, the single job that invokes arbitrary-precision fallback was also
repeated with the original arithmetic, using 5,063,641 nodes. A whole-search
original-arithmetic repeat remains in progress and is not counted as completed
evidence. Separately completed, larger m=100 searches provide another route
to the same exclusion; the compact package uses the 15X route in the table.

For m=99, the final exact profile lower bound is

    K>=7797285910967231555816016771572875912,

whereas the rounded published upper ceiling is 9274858856993487264329.
For m=100 the corresponding quantities are

    K>=3876482907693838530030634129025455,
    K<14848791401834506924263.

Each is a contradiction. The end-to-end checks bind the map certificates,
profile reconstruction, target derivation, complete searches, partition
audits and fallback validation. These are internally checked computational
proof claims, not external peer review.

## 15. Verification, prior work and significance

There are two proposed advances. The analytic result supplies an explicit
all-orbit block-growth base below delta and an asymptotically smaller cycle
upper bound than the delta^m bounds in Simons-de Weger [2]. The finite result
extends the completed candidate exclusions beyond Hercher's journal result
through 91 [4] and Wang's preprint claim through 95 [5]. The methods explicitly
build on their work, Bugeaud's p-adic estimates [1,8], and Barina's computation
[3]. Standard affine parity coding and prefix pruning are not inventions of
this manuscript.

Luca [6] proves effective exponential bounds relating cycle complexity and
height. His run parameter counts blocks with k_i>=2 and can be smaller than
our m; we do not identify the parameters. His displayed height recurrence
uses a factor at least delta, and does not state the uniform all-orbit bound
with the explicit smaller base given here. Normalized-exponent refinements
are established transcendence-theory tools, reviewed by Bugeaud [7]. The
specific specialization and finite cases still need a complete priority check.

The analytic proof consists of universal inequalities, not extrapolation
from computation. Exact rational auditors check its constants. Selected
algebraic, congruence, restart and majorization lemmas have also been accepted
by a pinned Lean/mathlib environment without proof placeholders. This is
partial formal verification: the published transcendence theorem, complete
specialization, imported cycle results and exhaustive native programs are not
all formalized in Lean. Independently written checks still share mathematical
assumptions and the same machine, so correlated mistakes remain possible.

The finite review archive was extracted into a fresh directory. Four
end-to-end exclusion audits and two analytic audits reproduced their saved
receipts byte for byte. The archive contains sources, exact inputs, journals,
proof notes, hashes and rerun commands; its default audit does not silently
claim to rerun every billion-node search. Longer reruns are documented.
The strongest new analytic specialization has a separate exact audit and
is included in the final companion package.

If independent review confirms both correctness and priority, these results
would be a quantitative contribution to the study of Collatz cycles and
block growth. They would not be a proof of convergence or a structural
classification of every possible cycle. The new base remains greater than
one, so the theorem still permits unbounded growth. Excluding any fixed
number of local minima still leaves infinitely many possible cycle sizes.
The work narrows rigorous bounds and supplies reusable certificates; it does
not establish that the main conjecture is close to resolution.

## 16. Reproducibility and remaining review

The companion package includes the complete mathematical source, standalone
exact auditors, native search and reference implementations, machine-readable
certificates, selected Lean proofs and a pinned toolchain description. Saved
hashes bind completed evidence to the source that produced it. Failed and
unfinished experiments remain in the research notebook with their status;
they are excluded from the claims above. No external AI model was consulted.

An external reviewer should first check the rational clause of Bugeaud's
1999 theorem, the height conventions, the cardinality conditions, the
unbounded dyadic range, the restart induction, and the analytic-to-finite
joining argument. The author-hosted 1999 version was inspected directly;
a comparison with the final journal text remains desirable. For the finite
argument the priority items are exhaustive residue coverage, directed height
rounding, overflow/fallback handling and global-minimum window scope. A full
original-arithmetic m=100 rerun and independent-machine reproduction would
add confidence. None of those future checks is reported as already done.


## Authorship and AI disclosure

Luke Baer and Amy (AI research system), 29 September 2026.

Luke Baer originated and directed this research project, supplied its resources,
and set the requirements for substantive results, saved evidence and reproducible
verification. Amy, operating through OpenAI Codex, developed the mathematical
arguments, wrote the implementations and manuscript, and performed the internal
checks described here. Amy is not a human researcher. The joint research credit
in this review edition is not a representation that an AI system is eligible
for journal authorship. Any submission must comply with the destination's
human-authorship and AI-disclosure rules and receive accountable human review.
No independent mathematical review has yet been obtained.

## Primary references

[1] Y. Bugeaud, Linear forms in p-adic logarithms and the Diophantine
equation (x^n-1)/(x-1)=y^q, Mathematical Proceedings of the Cambridge
Philosophical Society 127(3) (1999), 373-381, Theorem 1, rational clause (6).
https://doi.org/10.1017/S0305004199003692
The author-hosted complete source, whose pages 3-4 were visually inspected,
is https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps .

[2] J. Simons and B. de Weger, Theoretical and computational bounds for
m-cycles of the 3n+1 problem, version 1.44, 31 August 2010, Theorem 3(d)
and Corollary 13.
https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf

[3] D. Barina, Improved verification limit for the convergence of the
Collatz conjecture, The Journal of Supercomputing 81 (2025), article 810.
https://doi.org/10.1007/s11227-025-07337-0
We use the published bound below 2^71, rather than a changing live-project
counter or projected future verification range.

[4] C. Hercher, There are no Collatz m-Cycles with m<=91, Journal of Integer
Sequences 26 (2023), article 23.3.5, with the corrigendum linked by the journal
and dated 14 June 2026.
https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html

[5] X. Wang, Non-existence of Collatz m-cycles for m<=95, 2026 preprint
and computational files. Latest located Zenodo record, 29 July 2026:
https://doi.org/10.5281/zenodo.21670936
Its manuscript and downloadable C++ source were inspected, not executed.
Its claimed exclusion is a comparison, not an input to our certificates.

[6] F. Luca, On the non-trivial cycles in Collatz's problem, SUT Journal
of Mathematics 41(1) (2005), 31-41, Theorem 2.1 and Lemma 3.2.
https://www.rs.tus.ac.jp/sutjmath/_userdata/41-1/03-luca.pdf

[7] Y. Bugeaud, B-prime, arXiv:2209.00275 (2022), Section 1, for the
history of normalized-exponent refinements.
https://arxiv.org/abs/2209.00275

[8] Y. Bugeaud, Linear Forms in two m-adic Logarithms and Applications
to Diophantine Problems, Compositio Mathematica 132 (2002), 137-158,
Theorem 2. https://doi.org/10.1023/A:1015825809661
Only Theorem 2 supplies the finite reduction. We do not silently change
the height conventions in the differently printed general Theorem 1.
