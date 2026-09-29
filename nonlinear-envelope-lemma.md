# Cyclic majorization for a general increasing growth map

Status: newly derived here; proof below is self-contained but not externally reviewed. Novelty is unknown. The concrete Collatz map was subsequently certified by two complete native algorithms, exact threshold audits and sampled independent Python checks; see results/nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json. The application section below preserves the reasoning at the proposal stage.

## Sharp growth-constrained majorization

Let b be real, let m>=1, and let Phi:[b,infinity)->[b,infinity) be continuous and strictly increasing, with Phi(x)>=x. Define its truncated inverse Psi by

    Psi(t)=b,                         b<=t<=Phi(b),
    Psi(t)=Phi^(-1)(t),              t>Phi(b).

Then Psi is continuous, nondecreasing, and Psi(t)<=t. For any S>=m*b there is a unique t>=b such that

    w_j=Psi^(m-j)(t),  j=1,...,m,    sum_j w_j=S.

Existence and uniqueness follow because this sum is continuous and strictly increasing in t (its last term is t), starts at m*b, and tends to infinity.

**Theorem.** The increasing vector w majorizes every cyclic vector x with x_i>=b, x_(i+1)<=Phi(x_i), and sum_i x_i=S. Consequently, for every convex f,

    sum_i f(x_i) <= sum_j f(w_j).

The bound is attained by w itself arranged in increasing cyclic order.

**Proof.** Sort x into u_1<=...<=u_m. For every j<m, an edge of the original cycle goes from the set of j smallest vertices to its complement. Its starting value is at most u_j and its ending value is at least u_(j+1). Monotonicity gives

    u_(j+1)<=Phi(u_j), equivalently u_j>=Psi(u_(j+1)).

Suppose an increasing prefix through j had sum smaller than the corresponding w-prefix. If w_j=b this is impossible because all u_i>=b. Otherwise u_j<w_j: indeed u_j>=w_j would imply

    u_i>=Psi^(j-i)(u_j)>=Psi^(j-i)(w_j)=w_i

for every i<=j, contradicting the smaller prefix sum. Since w_j>b, all subsequent inverse steps are untruncated, so w_(j+r)=Phi^r(w_j). Strict monotonicity now gives u_(j+r)<w_(j+r) for every r>=1. The smaller prefix and smaller remaining suffix contradict equality of total sums. Thus every increasing prefix of u is at least the corresponding prefix of w, which is exactly the majorization assertion. Finally w_(j+1)<=Phi(w_j), including at the floor transition; the wraparound inequality holds because w_1<=w_m<=Phi(w_m). This proves feasibility and sharpness. End of proof.

The linear geometric-ramp lemma is the special case Phi(x)=d*x after shifting the floor. The proof does not require Phi to be concave or differentiable.

## A nonlinear subordinate envelope

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

## General block restart criterion

The future-run condition follows if, at each admissible starting minimum, there is a finite r>=1 such that

    k_(i+j)<=Phi^j(y_i) for 0<=j<r,
    y_(i+r)<=Phi^r(y_i).

Strong induction uses only monotonicity and composition of iterates. A proven entry into the verified convergence basin may instead discharge that seed. All intermediate run inequalities must be checked unless convergence is established independently.

If Phi is piecewise differentiable with slope at least 1, then Phi^j also has slope at least 1 wherever differentiable. For an exact family n_j=(P*a+Q)/2^S with P>0 and Q+2^S>=0, the restart difference

    Phi^j(k_root+log2(a))-log2(n_j+1)

is nondecreasing in a. Where derivatives exist, multiply the derivative by a*ln(2): the result is at least 1-P*a/(P*a+Q+2^S)>=0. Continuity extends monotonicity across the finitely many breakpoints. Thus a passed least-endpoint restart test still certifies an entire arithmetic progression interval. This is a sufficient condition for adapting the grouped family proof.

## A concrete proposed Collatz map

Let delta=log2(3), c0=37.99, c1=40.99 and h=71. Consider

    Phi(y)=max(delta*y-c1,
               min(delta*y-c0, y+h*(delta-1)-c0)), y>=71.

It equals delta*y-c0 up to h, has slope 1 until h+(c1-c0)/(delta-1), and then equals delta*y-c1. It is continuous, strictly increasing, at least the identity on y>=71, and has slope at least 1. Its dependence on delta is increasing, so rational lower and upper delta bounds give directed enclosures without floating-point decisions.

Every already established local c1 one- or two-block sufficient condition is also sufficient for this Phi, because Phi(y)>=delta*y-c1 and Phi is increasing. Therefore the existing globally exhaustive J41 exception list can serve as a conservative input. Those exceptional classes still need a NEW complete nonlinear block-restart or basin proof; neither the uniform c38 certificate nor the conditional c41 certificate alone proves this map.

The key attraction is that the difficult low-height classes receive the c38 first-step allowance, while large virtual heights eventually receive c41. The existing linear certificates cannot simply be pasted together: their restart blocks may cross the transition, so every exceptional block must be rechecked with the nonlinear iterates. No nonlinear coefficient or improved exclusion is claimed at this stage.

## Finite challenges and a limitation of additive growth guesses

An exact Fraction implementation checks 96,249 feasible sorted integer vectors, dimensions 2 through 7, on four continuous piecewise-linear growth maps. These include convex, concave, and neither-convex-nor-concave maps. It also checks 2,400 periodic subordinate envelopes and their common-cap normalizations. Every majorization prefix and every growth constraint passes. The receipt is nonlinear-majorization-check.json. These tests challenge the derivation; the general claim rests on the proof, not on finite examples.

It would be tempting to extend the middle slope-1 segment indefinitely. An unconditional pointwise bound k_next<=log2(n+1)+C with a fixed C is false. For each k>=1, let M=2*3^(k-1) and a=(2^M-1)/3^k. The integer a is positive and odd. Starting from n=a*2^k-1, the exact next minimum is 2^(M-1)-1: the current odd-run length is k, the intervening even-run length is 1, and the next odd-run length is M-1. Thus

    k_next-log2(n+1)=(delta-1)*k-1-log2(1-2^(-M)),

which is unbounded. A version restricted to orbits avoiding the verified basin would have to exclude these explicit trajectories by proving convergence or some other valid argument. Their eventual behavior is not established here. This is one reason to retain a finite transition and a slope-delta tail in the proposed map.
