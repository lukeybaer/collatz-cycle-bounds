# A subordinate cyclic height envelope

Status: new derivation in this notebook, proof under audit and novelty unconfirmed. This repairs a limitation of the preceding capacity method: actual logarithmic heights need not satisfy the stronger affine edge inequality, but a suitable sequence BELOW those heights does.

Use the notation and certified alternatives from `lifted-capacity.md`. In particular, y_i=log_2(n_i+1)>71, d>=log_2(3), and c,B satisfy

    d*71-B-c*(d+1)/(d-1)>0.

Each transition obeys either y_(i+1)<=d*y_i-c or k_(i+1)<=B. In the latter case, y_(i+2)<=d*y_i+(d-1)*B.

## Pointwise future-run theorem

For every t>=0,

    k_(i+t) <= d^t*y_i-c*G_t,
    G_t=(d^t-1)/(d-1).

For t=0 this is k_i<=y_i. Induct on t. Under the first alternative, apply induction at i+1 to obtain the assertion. Under the second alternative, t=1 follows from k_(i+1)<=B<d*y_i-c. For t>=2, induction at i+2 gives

    k_(i+t) <= d^(t-2)*(d*y_i+(d-1)*B)-c*G_(t-2).

The desired upper bound minus this one equals

    d^(t-2)*[(d-1)*(d*y_i-B)-c*(d+1)],

which is positive by the stated dominance condition. This proves the claim for all t, including repeated traversals of the cycle.

## Envelope construction

Suppose all minima also exceed N>=2^71. Let b be any certified lower bound for log_2(N+1), with b>c/(d-1). Put a=c/(d-1) and v_i=max(b,k_i). Define

    z_i = a + max_(t>=0) d^(-t)*(v_(i+t)-a).

The sequence v is periodic, and every v_i-a is positive. Hence the maximum occurs among 0<=t<m. In particular, this is a finite, well-defined cyclic sequence.

The future-run theorem and y_i>=b>a imply

    v_(i+t) <= d^t*y_i-c*G_t
             = a+d^t*(y_i-a).

Therefore z_i<=y_i. Taking t=0 gives z_i>=v_i>=b and z_i>=k_i, so sum z_i>=K. Finally, separating t=0 from the remaining terms in the infinite maximum gives

    z_i = max(v_i, a+(z_(i+1)-a)/d).

Thus z_(i+1)<=d*z_i-c. These are exactly the stronger affine growth constraints needed for the sharp majorization theorem, now on z rather than on the actual heights y.

## Reciprocal consequence

The function f(u)=1/(2^u-1) is decreasing and convex for u>0. Since z_i<=y_i,

    sum 1/n_i = sum f(y_i) <= sum f(z_i).

If K>=m*b, apply the floor-plus-geometric majorization theorem after shifting z by a. If sum z>K, interpolate z toward the constant vector b until its sum is K; this preserves the affine growth inequalities because b>a, and can only increase the decreasing objective. The resulting sharp relaxed upper bound is the shifted geometric profile with total K, floor b, growth d, and shift a=c/(d-1). If K<m*b, interpolation to total K would violate the floor; use the direct bound sum 1/n_i < m/N instead. The numerical certificate implementation includes this separate minimum-only case.

This application uses a proved subordinate envelope. It does NOT assert the false stronger edge inequality for every actual y_i. The finite modular certificate, global odd-step upper bound, logarithmic interval bounds, and majorization proof are all dependencies.
