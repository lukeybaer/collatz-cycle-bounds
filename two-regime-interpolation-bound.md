# An explicit block-growth bound below log_2(3)

Private research manuscript, 29 September 2026. Candidate mathematical
result: independent review and priority verification are pending. The
proof uses a published p-adic theorem, together with the elementary
estimates below. It neither proves Collatz convergence nor excludes all
nontrivial cycles. No frozen numerical certificate depends on this file.

## Statement and block conventions

Use T(n)=(3n+1)/2 for odd positive n and T(n)=n/2 for even n.
A block is a maximal odd run followed by a maximal even run. At its
odd starting value n_t set k_t=v_2(n_t+1) and y_t=log_2(n_t+1).
Write delta=log_2(3), beta=delta-1, and put

    epsilon=1/160, lambda=delta-epsilon,
    B=2^14, C=127, A=(delta/lambda)^26.

The claimed all-orbit estimates are

    k_t <= A*y_0*lambda^t                         (t>=0),
    y_t <= delta*A*y_0*lambda^(t-1)               (t>=1).

The index counts blocks. In particular lambda>1, so these estimates
allow unbounded trajectories. For a hypothetical nontrivial positive
cycle with m local minima and K odd shortcut steps, the published
cycle-size bounds cited below further imply

    K < [10A/(lambda-1)]*m*lambda^m,              m>=515620.

The proposed contribution is the explicit specialization and global
restart argument. The transcendence method and its normalized exponent
are established prior work. Novelty of this application is unconfirmed.

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

Fix an integer J>=100. If D<J, then ell<=J and
log_2(a)<(12/7)(J+1), since beta>7/12. We will prove

    k >=125J and D<J  ==>  k'<(38/25)k.                (2)

## The published p-adic input, with hypotheses checked

Use Bugeaud1999, Theorem1, rational clause(6) [1]. Put r=k mod2,
H=(k+r)/2, alpha_1=9, and alpha_2=-3^r*b_0/a. Then

    Lambda=alpha_1^H-alpha_2=3^r*(a*3^k+b_0)/a>0.

If the valuation of a*3^k+b_0 is at most2, (2) is immediate.
Otherwise alpha_2 is congruent to1 modulo8, because 9^H is.
Both rational arguments are 2-adic units. In the theorem use
p=2, g=1, E=3, b_1=H, b_2=1, and u=0. Its auxiliary field
parameters are D_field=e=f=1, t=1. In particular
v_2(alpha_1-1)=3>1 and v_2(alpha_2-1)>=3>=2.
Both exponents are positive, b_2 is odd, and Lambda is nonzero.
Logarithmic rational heights obey

    h(alpha_1)=2ln3,
    h(alpha_2)<(12/7)(J+1)ln2.                        (3)

For the second bound, log_2(a) has already been bounded, while
log_2(3^r*b_0)<J+delta<(12/7)(J+1). Fraction reduction only lowers
height. Negative rational arguments are permitted in the statement.

Rename the theorem's integer parameter K as M. Given positive integer
parameters M>=3, L>=2, R_1,S_1,R_2,S_2, define

    R=R_1+R_2-1, S=S_1+S_2-1, N=ML,
    gamma=1/2-N/(6RS),
    P_M=product(i!, i=1,...,M-1),
    b=[R-1+(S-1)H]*P_M^(-2/[M(M-1)])/2.

We choose S_1=1,R_1=L. Thus the first required cardinality is L:
the powers alpha_1^(p^t x)=9^(2x) are distinct for 0<=x<L.
We also ensure R_2<=H. Then x+Hy, with 0<=x<R_2 and
0<=y<S_2, are distinct. Their count R_2*S_2 will exceed (M-1)L,
as checked in each range. Restrictions modulo g=1 are vacuous.
No multiplicative-independence assumption is needed once these
cardinality conditions hold.

The theorem applies if

    M(L-1)*3ln2 - 3lnN - (M-1)lnb
       - gamma*L*R*h(alpha_1) - gamma*L*S*h(alpha_2)>0. (4)

It then gives v_2(Lambda)<=3(ML-1/2)<3ML. This is also the valuation
of a*3^k+b_0; in particular k'<3ML.

## Factorial normalization and numerical logarithms

For every integer M>=800,

    P_M^(-2/[M(M-1)]) < (23/5)/(M-1).                (5)

Indeed ln(i!)>=i ln(i)-i+1 by integrating ln x. Since x ln x is
increasing for x>=1, a second integral comparison gives

    ln P_M >= ((M-1)^2/2)ln(M-1) - (M-1)^2/4 +1/4
                  - M(M-1)/2 + M-1.

Multiplying by -2/[M(M-1)] gives a quantity at most
-ln(M-1)+3/2+ln(M-1)/M. For M=800u, u>=1,
ln(M-1)<ln800+lnu<6.7+u-1<7.2u, using lnu<=u-1.
Consequently ln(M-1)/M<.009. Finally 1.509<ln(23/5), proving(5).
We may also use the weaker factor5/(M-1).

The numerical bounds used throughout are

    .693<ln2<.6932, ln3<1.099, ln264<5.576,
    ln(7/4)<.56, ln800<6.7, ln11<2.4.

Each is checked with an exact rational logarithm-series enclosure in
the accompanying audit. Define

    U=(12/7)*(101/100)*.6932=525099/437500.

Then h(alpha_2)<UJ for every J>=100.

## Range I: 125<=k/J<=256

Choose M=9J,L=7,R_1=7,S_1=1,R_2=7J,S_2=9. Thus
R=7J+6,S=9,N=63J. Here M>=900, R_2<=H, and
R_2*S_2=63J>(9J-1)*7. Also RS>N, so 1/3<gamma<1/2.

Since H<=128J+1/2, (5) gives

    b < (23/5)*(1031J+9)/(18J-2) <264.

The last ratio decreases with J, and its value at100 is less than264.
The exact identities for gamma give

    gamma*R/J =7/3+3/J <=709/300,
    gamma*S =9/2-(21/2)*J/(7J+6)
            <=2127/706 <3013/1000.

Furthermore 3lnN/J<3/10. To see this, N<=100J and ln(100J)<J/10
for J>=100: put J=100u, use ln10000<10 and lnu<=u-1.

Substitution in (4) gives the following strict lower bound after
division by J:

    9*6*2.079 -9*5.576 -.3
        -7*[(709/300)*2.198+(3013/1000)*U]
      =19833889/187500000 >0.

It follows that k'<3ML=189J<190J<=(38/25)k, proving(2)
in this range. Bounds on -(M-1)lnb use the positive upper bound
lnb<ln264, and remain valid even if lnb were negative.

## Range II: k/J>256

Let q be the least integer with k/J<=2^q. Then q>=9 and
k/J>2^(q-1). Choose

    M=(q+1)J, L=q+2, R_1=L, S_1=1,
    R_2=(q-1)J, S_2=q+5.

Thus R=(q-1)J+q+1,S=q+5,N=(q+1)(q+2)J. Here M>=1000.
The inequality q-1<2^(q-2) gives R_2<H. Also
R_2*S_2=(q^2+4q-5)J>=ML>(M-1)L, because q>=9.
Again RS>N and 1/3<gamma<1/2.

The weaker factor5 in (5), and H<=(2^q J+1)/2, give

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

The left side of(4), divided by J, is therefore greater than

    P(q)=(q+1)[(q+1)*2.079-.6932q-.56]-q/25
      -(q+2){[(203/600)q-97/600]*2.198
                +[(1/2-350/2127)q+5/2-1400/2127]*U}.

Its exact coefficients, from quadratic to constant, are

    1783170953/7444500000,
    -454813329/354500000,
    -1631430293/744450000.

The leading coefficient is positive,
P(9)=3011630363/531750000>5.66, and
P'(9)=1503066483/496300000>3.02. Expansion at9 proves P(q)>0
for every real q>=9. The theorem yields k'<3J(q+1)(q+2).
At q=9, 3(q+1)(q+2)=330<(38/25)*256. The ratio of consecutive
left sides is (q+3)/(q+1)<=2, so induction proves

    3(q+1)(q+2)<(38/25)*2^(q-1)<(38/25)*(k/J).

This finishes(2) for all k>=125J.

## From the valuation bound to all-orbit growth

Suppose y>=Y_J=125J+(12/7)(J+1). If D>=J, (1) gives
y'<=delta*y-J. If D<J, then k>=125J and(2) applies. Since
delta>19/12, beta>7/12, and delta<5/3,

    delta*y-k' > (19/300)k >J,
    beta*(delta*y-k')+D > (7/12)*(19/300)*125J
                       =(665/144)J >(delta+1)J.

Using(1), we have therefore proved the following bounded restart:
either y'<=delta*y-J, or both

    k'<=delta*y-J, y''<=delta^2*y-(delta+1)J.            (6)

For y>=B, let J=floor(y/C). Then J>=100,
J>=(99/100)y/C, and Y_J<=CJ<=y. Since
epsilon*C=127/160 <(81/100)*(99/100), epsilon*y<(81/100)J.
The one-block bound and intermediate k' in(6) are below lambda*y.
The two-block endpoint is below lambda^2*y, because

    (delta^2-lambda^2)y<2delta*epsilon*y
       <(162/100)delta*J<(delta+1)J.

The last inequality uses delta<8/5. This is a one- or two-block
restart statement, not a bound y'<=lambda*y at every block.

Define the continuous increasing extension for y>=1 by

    G(y)=delta*y                         (y<=B),
    G(y)=max(lambda*y,y+beta*B)           (y>=B).

It satisfies (3/2)y<=G(y)<=delta*y, and G(y)=lambda*y for y>=2B.
Below B apply the elementary one-block estimate. Above B use(6),
G>=lambda*y, and monotonicity. Induction along the selected restarts
gives k_t<=G^t(y_0), and y_t<=delta*G^(t-1)(y_0) for t>=1.
At the single intermediate block of a two-block restart, the k' bound
in(6) supplies the former inequality and y'<=delta*y supplies the latter.

The exact integer inequality 3^26>2^41 implies (3/2)^26>2B.
Every virtual orbit thus reaches y>=2B by step26. Use G<=delta*y
before that point and G=lambda*y afterwards to obtain
G^t(y_0)<=(delta/lambda)^26*y_0*lambda^t, including t<26.
This proves the stated all-orbit bounds.

## Consequence for hypothetical cycles and scope of verification

For m>=515620, Simons-de Weger [2], Theorem3(d), gives the coarsened
bound K<16m*delta^m, while Corollary13 gives
n_min<m*exp(13.3*(.46057+lnK)). Combining them gives
log_2(n_min+1)<10m; the elementary calculation is recorded in
Section5 of sharper-exponential-bound.md. This input is independent
of the improved lambda. Rotate a cycle to its smallest member. Then

    K <= A*log_2(n_min+1)*(lambda^m-1)/(lambda-1)
      < [10A/(lambda-1)]*m*lambda^m.

Exact rational constant checks and finite large-integer challenges
accompany this manuscript. Some supporting algebra and restart lemmas
are checked in Lean. These checks do not formalize the published
p-adic theorem or the whole application. A domain expert should review
the source specialization, universal parameter bounds, and restart
induction. Finite tests alone cannot establish these statements.

## Primary references

[1] Y. Bugeaud, Linear forms in p-adic logarithms and the Diophantine
equation (x^n-1)/(x-1)=y^q, Mathematical Proceedings of the Cambridge
Philosophical Society127(3)(1999),373-381, Theorem1, clause(6).
https://doi.org/10.1017/S0305004199003692
Author's complete PostScript, pages3-4 visually inspected after local
rendering: https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps
The author version explicitly uses logarithmic heights. A comparison
with the final journal text remains desirable; no unread text is assumed.

[2] J. Simons and B. de Weger, Theoretical and computational bounds
for m-cycles of the 3n+1 problem, version1.44,31August2010,
Theorem3(d) and Corollary13.
https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf

[3] Y. Bugeaud, B-prime, arXiv:2209.00275(2022), Section1, for the
history of normalized-exponent refinements: https://arxiv.org/abs/2209.00275

[4] F. Luca, On the non-trivial cycles in Collatz's problem,
SUT Journal of Mathematics41(1)(2005),31-41. Theorem2.1 is relevant
prior work on exponential cycle-complexity bounds. Its run parameter
differs from m; see sources.md for the checked comparison.
https://www.rs.tus.ac.jp/sutjmath/_userdata/41-1/03-luca.pdf
