# Stronger capacity program using Bugeaud's theorem

Status: the finite global residue sweep and all 1,929,307 exceptional convergence checks have completed. The UInt128, BigInteger and independent Python implementations agree on every class trajectory digest. The independent coverage audit also passed. The coefficient c=2999/100 is internally certified; external mathematical review and novelty review are pending. The later block-restart method extends the completed coefficient to c=3499/100. Candidate cycle exclusions and their current audit status are recorded in STATUS.md.

Source: Yann Bugeaud, *Linear Forms in two m-adic Logarithms and Applications to Diophantine Problems*, Compositio Mathematica132 (2002),137–158, Theorem2, DOI10.1023/A:1015825809661. Original PDF and a rendered theorem page are saved in work/sources. The theorem's parameter mu is distinct from its valuation base m; the PDF text extraction confuses these letters. We use valuation base8 and parameter mu=6, whose constant is46.1. Multiplicative independence is not required for this version. The hypotheses include the stated unit and congruence conditions and coprimality of the valuation base and the two exponents collectively; the second exponent here is1.

## Large-exponent lemma

Let a be positive odd with a<2^50, let1<=ell<=29, and put b=2^ell-1. For k>=2^18, define s=v_2(a*3^k+b)-ell whenever this is a positive next odd-run length. Then s<k.

If a=b, LTE gives v_2(a*3^k+b)=v_2(3^k+1)<=2, so the claim is immediate. Otherwise apply Bugeaud's Theorem2 to

    Lambda = 9^k-(b/a)^2,
    alpha1=9, alpha2=(b/a)^2, exponents k and1,
    valuation base m=8, g=1, parameter mu=6,
    A1=9, A2=2^100.

Both rational numbers are2-adic units. The first has v_2(9-1)=3, and an odd rational square different from1 differs from1 by2-adic valuation at least3. Hence H1 and H2 hold. The rational heights are bounded by the stated A1,A2. Lambda is nonzero for k>=2^18 because9^k>(b/a)^2. Also

    b'=k/log(A2)+1/log(A1)<=k.

Use log2 in(.69,.7), log3<1.1, and log log8<1. For k>=2^18, the maximum in the theorem is less than log k+2, since6log8<12.6<log k+2. Passing from v_8 to v_2 gives

    v_2(Lambda) < C*(log k+2)^2+3,
    C=3*46.1*log9*(100log2)/(log8)^4
     =(27660/81)*log3/(log2)^3 <1200.

The original expression a*3^k+b is one factor of a^2*Lambda, and the other factor is an integer, so its2-adic valuation is at most v_2(Lambda). At k0=2^18,

    1200*(log k0+2)^2+3
      <1200*(73/5)^2+3=255795<262144=k0.

The function(k-3)/(log k+2)^2 is increasing for k>=k0, as direct differentiation shows. Therefore v_2(a*3^k+b)<k for all k>=k0, proving the claim.

## Stronger two-step alternative

Let d be the certified rational upper bound for log_2(3), beta=d-1, y=log_2(n+1), k the current odd-run length, and s the next odd-run length. With a=(n+1)/2^k and ell the intervening even-run length, use the conservative logarithmic loss

    D=ell+beta_lower*log_2(a)-epsilon,

where beta_lower=584962/10^6 and epsilon=1/1000 is a deliberately loose upper bound for the logarithmic additive error when relevant minima exceed2^71. Indeed the exact error is log_2(1+(2^ell-1)/(a*3^k)), which is less than log_2(1+1/n_next)<1/1000. The next block also loses at least e=999/1000 from its compulsory even step. Thus

    y_next<=d*y-D,
    y_nextnext<=d*y-D+beta*s-e.

For a proposed coefficient c>1, it suffices that every transition satisfy either D>=c or

    beta*(d*y-s)+D+e-c*(d+1)>=0.                  (P)

The same induction as in subordinate-height-envelope.md then proves k_(i+t)<=d^t*y_i-c*G_t. Under D<c, condition(P) also implies s<=d*y-c because2c>D+e. The subordinate-envelope and majorization consequences follow unchanged.

For any c=J-1/100 with J<=30, ell>=J or a>=2^ceil(12*(J-ell)/7) makes D>=c. Thus problematic transitions have ell<=29 and a<2^50. For k>=2^18, the large-exponent lemma gives s<k; since y>=k, condition(P) then holds with enormous margin for c<=30. It remains to check k<2^18.

## Finite reduction without enumerating every small a

First propose a uniform B=90 for next odd-run lengths in the remaining range. For each1<=k<2^18 and1<=ell<J, compute

    r=(1-2^ell)*3^(-k) mod2^(ell+B+1).

The modulus exceeds the entire exceptional a-range. If r is at least its upper endpoint, no allowed a gives s>=B+1. This requires at most29*(2^18-1) modular checks. It must be executed, not assumed.

Given s<=B, condition(P) is automatic when k exceeds a modest explicit threshold, about140 for c near30. For the remaining k, ell and exact s, the odd part a lies in the class

    a ==(2^(ell+s)+1-2^ell)*3^(-k) mod2^(ell+s+1).

The condition n=a*2^k-1>2^71 provides a lower endpoint. For fixed k,ell,s, both the one-step loss D and the left side of(P) increase with log_2(a). Hence only an initial finite interval of this residue class can fail the sufficient inequalities.

Use rational bounds delta_lower=1584962/10^6, delta_upper=1584963/10^6 and beta_lower=584962/10^6. They enclose the100-digit constants independently checked elsewhere. A conservative sufficient test is

    ell+beta_lower*log_2(a)-epsilon>=c,

or

    beta_lower*delta_lower*k-beta_upper*s
      +beta_lower*(delta_lower+1)*log_2(a)
      +ell+e-epsilon-c*(delta_upper+1)>=0.

Here beta_upper=584963/10^6. The negative s term must use this UPPER bound; using beta_lower on the entire delta_lower*k-s expression would be unsafe if that expression is negative. This rounding issue was corrected before the final trajectory runs; it did not change the finite exception list. Rounding the smaller required logarithm upward to an integer q makes a>=2^q sufficient. Thus all remaining candidates are represented by finite residue intervals with a<2^q.

## Optional basin exclusion for exceptional seeds

If a proposed coefficient fails the sufficient inequalities at finitely many explicit seeds, proving every such seed reaches the already verified basin[1,2^71] removes them from every nontrivial cycle. A forward descent below its own starting value is NOT sufficient for this particular lemma: it must reach the verified basin or another separately proved convergent value. A step or bit limit is unresolved, never a pass.

For J=30, B=90, the executed global sweep checks 7,602,147 pairs and passes. The remaining initial range k<200 produces 3,889 classes containing 1,929,307 seeds. Both C# trajectory paths prove every seed reaches the verified basin, using 265,699,552 accelerated odd steps in total. The longest path takes 396 such steps; the largest intermediate value has 139 bits. The fixed-width path uses 731 BigInteger fallback steps. The separate full BigInteger run agrees on every per-class SHA256 digest, including every seed, exact step count, terminal value, and maximum bit length. Files are named strong-capacity-J30-* in results/.

## Induction and scope

For an actual nontrivial positive cycle, every minimum exceeds X by the external verification theorem. The finite exceptions cannot occur, since their orbits enter that basin. Consequently each transition has D>=c or satisfies (P). In the first case, y_next<=d*y-c. In the second case, y_nextnext<=d^2*y-c*(d+1). If D<c, then (P) also gives

    beta*(d*y-s-c) >= 2*c-D-e > c-e > 0,

so s<d*y-c. Induction on the number of future blocks now proves

    k_(i+t)<=d^t*y_i-c*G_t,  t>=0.

This uses one step in the first alternative and two steps in the second; the separate inequality for s supplies the t=1 case. Sum over t=0,...,r-1 to obtain the capacity bound G_r*y_i-c*H_r. The subordinate-envelope construction in subordinate-height-envelope.md then applies unchanged, since y_i>71>c/(d-1).

The bound does not require the Simons-de Weger upper bound on K and is uniform in the number of cycle minima. It remains a statement about hypothetical nontrivial cycles; it does not assert convergence for all positive integers or for divergent orbits. Its external inputs are Bugeaud's theorem and the verified basin through 2^71, in addition to the elementary logarithmic bounds.
