# A sharp majorization bound for cyclic growth constraints

Status: candidate proved below, pending independent computational checks and novelty assessment. This is an auxiliary theorem, not a proof of Collatz.

## Statement

Let d>1, b>0, m>=1, and S>=m*b. Let x_1,...,x_m be a cyclic sequence satisfying x_i>=b, x_(i+1)<=d*x_i, and sum x_i=S (indices modulo m).

Choose t>=b uniquely such that

    sum_(r=0)^(m-1) max(b,t*d^(-r)) = S,

and let y_j=max(b,t*d^(j-m)), j=1,...,m.

Then y majorizes x: after sorting x increasingly as u_1<=...<=u_m,

    sum_(i=1)^j u_i >= sum_(i=1)^j y_i,   1<=j<m.

Consequently every convex function f on [b,infinity) satisfies

    sum f(x_i) <= sum f(y_i).

The bound is attained: y in increasing cyclic order is feasible. Thus this solves the symmetric convex maximization exactly, not merely with an upper bound.

## Proof

First, the increasing rearrangement u satisfies u_(j+1)<=d*u_j. Otherwise partition the cyclic indices into values <=u_j and values >=u_(j+1). Both parts are nonempty, and some directed cycle edge exits the first part. That edge contradicts x_(i+1)<=d*x_i. Conversely, an increasing sequence satisfying these adjacent inequalities is cyclically feasible because its final-to-first edge decreases.

Fix j<m. If y_j=b, the required prefix inequality follows from u_i>=b. Suppose y_j>b and, for contradiction, the u-prefix sum is smaller than the y-prefix sum.

Backward application of the growth constraint gives

    u_i >= max(b,u_j*d^(i-j))   for i<=j.

The sum H_j(z)=sum_(i=1)^j max(b,z*d^(i-j)) is nondecreasing and strictly increasing for z>=b. The y-prefix sum equals H_j(y_j). Hence the presumed smaller prefix implies u_j<y_j.

Forward growth now gives u_i<=u_j*d^(i-j)<y_j*d^(i-j)=y_i for all i>j; the last equality holds because y_j>b makes the entire y-suffix geometric. Both the prefix sum and the suffix sum of u are smaller than those of y, contradicting their equal total S. This proves all prefix inequalities. The convex-function conclusion is the standard majorization inequality and can also be proved by successive averaging transfers.

## Application to a relaxed Collatz cycle problem

For x_i=log_2(n_i+1), take d=log_2(3), b=log_2(X+1). The standard local-minimum estimates imply x_(i+1)<d*x_i and K<=sum x_i. If K>=m*b, interpolate any x with sum x>K toward the constant vector b to obtain a feasible z with sum K and z_i<=x_i. For any decreasing convex f, sum f(x_i)<=sum f(z_i)<=sum f(y_i(K)).

The function f(x)=3/(2^x-1) is positive, decreasing, and convex for x>0. It gives

    sum_i T(n_i) < sum_j 3/(2^y_j(K)-1).

This is a valid relaxation only. It discards arithmetic restrictions and the stronger average bounds on T from published cycle work. It might be weaker numerically than those bounds. A proof of the auxiliary lemma is not evidence of a new Collatz exclusion until that comparison is made.

## Further possibility

The mandatory even step gives a stronger nearly affine relation for logarithmic heights. Investigate shifting the heights to retain that relation. Also investigate a potential-function bound that incorporates the published improvement from 3/X per minimum to a smaller amortized cost.
