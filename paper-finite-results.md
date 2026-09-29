## Certified finite-cycle application

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
theorem proved below to F and f(y)=1/(2^y-1). An established lower bound
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

## Verification, prior work and significance

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

## Reproducibility and remaining review

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
