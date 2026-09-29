# A finite block restart certificate for stronger cycle capacity

Status: complete finite certificates and independent parity-bisection verification now support J31, J35 and J38 (c=30.99, 34.99 and37.99). The uniform J41 trials hit node limits and are unresolved; they certify no coefficient. A separate conditional J41 experiment is documented in conditional-capacity.md. Analytic arguments are internally audited, with external review and novelty review pending. Keep these certificates separate from the J30 basin-only proof.

Fix d>log_2(3), c>0 and F_r(y)=d^r*y-c*G_r. Suppose every minimum belonging to a hypothetical nontrivial cycle satisfies the following: for some finite r>=1, all intermediate run lengths obey k_j<=F_j(y_0), 0<=j<r, and y_r<=F_r(y_0). Then strong induction proves k_t<=F_t(y_0) for every t. For t<r use the direct check; for t>=r apply induction at the later minimum and the identity F_(t-r)(F_r(y))=F_t(y). This generalizes the one-or-two-step alternative used previously. A verified basin entry instead rules out that starting seed entirely.

The analytic and modular reduction can be extended to c=J-.01, J<=41. All one-step exceptions have ell<=40 and a<2^69. Bugeaud's theorem with A2=2^140, valuation base8 and mu6 gives v2(a*3^k+2^ell-1)<1700*(ln k+2)^2+3<k for k>=2^19. At the cutoff the latter expression is less than1700*(153/10)^2+3=397956<524288, and the same monotonicity argument applies. All other hypotheses are as in padic-capacity-program.md. A residue sweep with B=100 covers k<2^19, and the two-step margin is positive for k>=200. The remaining finite classes have the same exact format as before, but may contain vastly more seeds.

For a class of original odd parts a, a later minimum has the affine form n_j=(P*a+Q)/2^S, where P>0 and Q+2^S>=0. The last property follows inductively from n_next+1=(3/2)^k*(n+1)/2^ell+1-2^(-ell). The difference

    F_j(k_root+log_2(a))-log_2(n_j+1)

is increasing in a for j>=1: its derivative has the sign of

    (d^j-1)*P*a+d^j*(Q+2^S),

which is positive. Therefore checking a sufficient restart inequality at the least a covers the entire residue interval. Intermediate k_j is constant on an exact odd-run branch and its upper envelope increases with a, so again the least a suffices.

For cheap exact comparisons, lower-bound y_0 by k_root+floor(log_2 a) and upper-bound y_j by bit_length(n_j). Compute lower envelope thresholds with rational d_lower=1584962/10^6. Since c<=40.99<71*(d_lower-1), all iterated lower heights stay above71, and these thresholds are below the envelope for d>=log_2(3). A passed test is rigorous; a failed rounded test only means subdivide or continue.

Exact affine parity classes partition the remaining seeds. A whole interval can be removed when its largest current minimum is at most2^71, or when its restart inequality passes. A singleton can always be checked by exact iteration to the verified basin. Every unfinished, over-limit, or inconsistent branch is unresolved. Coverage counts must add to the original class cardinality using arbitrary-precision integers, and the implementation requires independent validation before any stronger coefficient is used.

## Executed certificates

For J35, the global reduction covers17,825,758 pairs. Its17,993 exceptional classes contain5,793,235,244,454 starting values. The C# grouped proof uses6,560,119 nodes:5,793,219,309,204 seeds are discharged by a block restart;13,979,621 enter the basin as whole classes;1,955,629 are checked individually to that basin. Maximum restart depth is4. The run took13.37sec on this host with competing computations. An independent Python implementation, using repeated even/odd bisection of arithmetic progressions rather than modular inverses, verifies every class in102.92sec. It uses only coarse integer logarithmic heights, so its proof does not depend on the C# precision table. Both implementations require exact total coverage and treat all limits as unresolved.

The J31 grouped certificate covers36,235,683 seeds in337,398 nodes, with maximum depth3, and also passed full independent Python verification. Its Python receipt predates an optional-precision extension to the checker source and should be regenerated before freezing a source-hash-dependent final package.

The c=40.99 trial is not successful: both coarse and finer logarithmic tests leave many of the first100 classes unresolved at a one-million-node-per-class limit. Preserve those failure receipts; they are not capacity certificates.

For J38, all30,304 classes and32,432,309,338,453,812 seeds pass. The original C# producer uses302,707,049 nodes and6,759,487,086 singleton odd steps, with maximum restart depth5. The full Python parity-bisection verification passes in3287.76sec. A compiled translation of that independent checker matches every Python row, including292,351,266 nodes and8,823,070,580 singleton steps. Separately, a faster version of the original producer matches all its per-class counters exactly. These distinct step counts reflect the different partition methods, not a discrepancy in seed coverage. The coefficient3799/100 is frozen in family-capacity-J38-certificate.json.

The local restart induction does not require periodicity. The same future-run bound holds for any positive orbit that never enters the verified basin, expressed at its successive odd-run starts. An infinite positive orbit cannot have an infinite uninterrupted odd or even run: the former would require n+1 divisible by arbitrarily high powers of two, and the latter strictly decreases a positive integer. Hence it has infinitely many such blocks. The later subordinate-envelope and cyclic-majorization arguments do require a cycle. No part of this observation rules out divergent orbits.
