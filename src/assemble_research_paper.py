"""Assemble the complete review manuscript from its preserved proof sources."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sections(name):
    text=(ROOT/name).read_text(encoding='utf-8')
    return {m[1]:m[2].strip() for m in re.finditer(r'^## (.*?)\n(.*?)(?=^## |\Z)',text,re.M|re.S)}
old=sections('fourth-power-review-manuscript.md');new=sections('retained-loss-interpolation-bound.md')
env=sections('nonlinear-envelope-lemma.md')
parts=[r'''# Explicit block-growth bounds and finite-cycle exclusions for the 3n+1 problem

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
''']
def add(title,body):parts.append('## '+title+'\n\n'+body.strip()+'\n')
add('2. Exact block identities',old['Exact block identities'])
add('3. The published interpolation criterion',old['The published interpolation criterion'])
add('4. A factorial estimate used in both ranges',old['Factorial normalization and numerical logarithms'])
add('5. Retaining the elementary loss',new['The loss that was previously discarded'])
add('6. Fourth-power normalization and hypotheses',new['Fourth-power normalization and hypotheses'].replace('exactly as in the\nfourth-power note,','with the following choices,'))
add('7. Exact parameters for the two loss strata',new['Factorial bound and exact parameter table'].replace('The complete rational margins\nare saved in results/retained-loss-exponential-bound-audit.json.','The companion exact audit records every rational margin.'))
add('8. Local loss in every range',new['Local loss in all ranges'].replace('previously proved\nunbounded dyadic argument','following\nunbounded dyadic argument'))
add('9. The unbounded dyadic argument',old['The unbounded dyadic range'])
add('10. Global restart induction',r'''
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
''')
cycle=old['An affine envelope and sharper cycle consequences']
cycle=cycle.replace('21.08','22.51').replace('1.51','1.61').replace('15.17','15.27')
cycle=cycle.replace('(4)','(3)').replace('(5)','(4)')
cycle=cycle.replace('The affine estimate improves the coefficient;\nthe fourth-power normalization and retained loss improve the base.','This proves Theorem 2. The affine estimate improves the coefficient;\nthe fourth-power normalization and retained loss improve the base.')
add('11. Cycle consequences and comparison',cycle)
major=env['Sharp growth-constrained majorization'].replace('**Theorem.**','Theorem 4.').replace('**Proof.**','Proof.')
add('12. Sharp majorization for cyclic growth constraints',major)
add('13. A subordinate envelope for periodic run lengths',env['A nonlinear subordinate envelope'])
finite=(ROOT/'paper-finite-results.md').read_text(encoding='utf-8')
finite=finite.replace('## Certified finite-cycle application','## 14. Certified finite-cycle application')
finite=finite.replace('## Verification, prior work and significance','## 15. Verification, prior work and significance')
finite=finite.replace('## Reproducibility and remaining review','## 16. Reproducibility and remaining review')
finite=finite.replace('theorem proved below','theorem proved above')
parts.append(finite)
add('Primary references',r'''
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
''')
target=ROOT/'collatz-paper.md'
target.write_text('\n\n'.join(parts).strip()+'\n',encoding='utf-8')
print(target,flush=True)
