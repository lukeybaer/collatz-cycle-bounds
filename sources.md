# Source register

Retrieved 2026-09-28/29 during this task. Primary sources preferred.

Additional primary-source comparison on 29 September: Halbeisen and Hungerbühler, *Optimal bounds for the length of rational Collatz cycles*, author-hosted [PDF](https://people.math.ethz.ch/~halorenz/publications/pdf/collatz.pdf). Their cycle-minimum extremization uses ordered parity words and a cyclic rotation argument; this is relevant precedent for optimization over cycles, rather than the same growth-constrained real-vector theorem developed here. Also inspected Zhang, Shi, Xi and Chen, [*Majorization involving the cyclic moving average*](https://link.springer.com/article/10.1186/s13660-018-1737-4) (2018): its moving-average comparison is a different constraint problem. These comparisons do not establish novelty of our majorization lemma.

1. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum of Mathematics Pi 10 (2022), e12. Current arXiv v7 dated 2026-07-16: https://arxiv.org/abs/1909.03562 . Almost-all statement uses logarithmic density; it does not prove convergence for every starting integer.
2. Christian Hercher, *There are no Collatz m-Cycles with m <= 91*, Journal of Integer Sequences 26 (2023), article 23.3.5: https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html . The journal page links a June 14, 2026 corrigendum. Read that before using the original argument. Preprint: https://arxiv.org/abs/2201.00406 .
3. David Barina, live convergence-verification project: https://pcbarina.fit.vutbr.cz/ . Observed bound: all n < 2075*2^60. This is a project-reported computational result, not independently certified here.
4. Exploratory repository: https://github.com/tuliomarchetto/collatz . Lead for finite-state obstruction comparisons, not an assumed mathematical authority.
5. Exploratory repository: https://github.com/macindoe/collatz . Lead for prior work on reduced cycles and staircase sharpness, not an assumed mathematical authority.
6. Search lead, unverified: *Non-existence of Collatz m-cycles for m <=95*, ResearchGate publication 408180567. Determine author, full text, assumptions and review status before use.
7. Search lead, unverified: *A Corrected Suffix-Balanced Global-Minimum Certificate for Excluding Collatz m-Cycles for m <=94*, ResearchGate publication 406466331. Same cautions.

No result from an informal repository or search snippet is adopted without inspection.

8. J. Simons and B. de Weger, updated version 1.44 (2010), *Theoretical and computational bounds for m-cycles of the 3n+1 problem*: https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf . Checked Theorem 3(d): K<1.4784*m*delta^m applies for 91<=m<=515619. The smaller-m bounds have different coefficients. Do not generalize the displayed coefficient outside its proven range.
9. Xinjun Wang, June 2026 preprint and associated data, https://doi.org/10.5281/zenodo.21017296 . The readable manuscript and run logs were inspected; claimed m<=95 exclusion is not adopted as an independently verified input. Our work seeks to reproduce the relevant finite check with independently written code. Its initial global K>7e11 statement is broader than the range verified in the cited 2010 theorem; that distinction does not affect m=91..99, and our own K iteration avoids that initial assumption entirely.

- Bugeaud (2002), Linear Forms in two m-adic Logarithms and Applications to Diophantine Problems, Theorem2. https://doi.org/10.1023/A:1015825809661. Original PDF and visual theorem inspection saved locally; used for the proposed large-exponent reduction, finite cases still pending.

- Barina2025 published verification source now pinned: https://doi.org/10.1007/s11227-025-07337-0 ; primary institutional record https://www.fit.vut.cz/research/result/c197809/.en . Uses all n<2^71; the endpoint2^71 trivially converges. Journal article81:810.
- Bugeaud finite-case status updated: J30 basin-only proof and J35 block-restart proof have completed all finite checks; J38 C# proof complete, full independent Python check running. Earlier pending wording above is historical.
- Additional2026 lead inspected: Fernández–Ibáñez, Christoffel Words as Extremal Structures in Collatz Dynamics, arXiv:2607.24844v1. It addresses parity-word extrema; no result from it is assumed here.
- A search result claiming cycle complexity1322 was traced to a project that explicitly assumes an unproved BakerSeparation strengthening and DerivedLargeKBound. It is not treated as an unconditional bound superseding the m<=95 comparison. The project itself lists the hypotheses at https://collatz-lab.org/faq/ .
# Literature update, 29 September 2026

The Zenodo API's latest-version route for Wang's record21017296 resolves to
record21670936, published29July2026, DOI
[10.5281/zenodo.21670936](https://doi.org/10.5281/zenodo.21670936).
Its title still states exclusion through95. The PDF has the same MD5 as the
June paper already read, fe6acda216edecef1bffe2a663c3da27. The update adds a
readable C++ source, verify_m92_m95_parallel_pruned_journal.cpp, whose downloaded
MD5 matches the record, e500736ac0cc68e462cc2e31b80015bc. It is saved only in
work/sources for inspection; it has not been executed. The earlier archive's
unreadable source is therefore not the only available version. Initial review
confirms exact affine/residue conditions, dynamically tightened exponent
ranges, and rationally certified suffix targets. These are prior methods;
our possible contribution centers on the stronger capacity theorem and new
completed numerical cases, not a claim to have invented parity-prefix search.

Rozier and Terracol, *Paradoxical behavior in Collatz sequences*,
[arXiv2502.00948v5](https://arxiv.org/html/2502.00948v5),17May2026, later
Discrete Mathematics349(10),115167, DOI10.1016/j.disc.2026.115167, uses an
unordered majorization relation on parity words to compare affine remainders.
Its Section2 orders binary words by moving ones and comparing unsorted prefix
sums. This is distinct from our sorted-height extremizer with a cyclic growth
constraint, but is relevant prior Collatz work involving majorization. It is
not an input to the present certificates. Its paradoxical-sequence criterion
does not supply a missing all-orbit convergence proof here.

- Kwok Chi Chim (2025), Lower bounds for linear forms in two p-adic logarithms, Journal of Number Theory266,295-349, DOI10.1016/j.jnt.2024.07.012. Read Theorem2.1 pp.298-299 directly; rendered formula check retained. Primary institutional PDF: https://tugraz.elsevierpure.com/ws/portalfiles/portal/92346766/1-s2.0-S0022314X24001793-main.pdf . Used in logarithmic-run-loss.md. Multiplicative independence is required; our dependent rational case is treated separately.

- Attribution clarification: Chim's introduction credits Kunrui Yu's older general p-adic logarithmic-form estimates with linear dependence on log B. Therefore the asymptotic argument here cannot claim that this qualitative input first appeared in2025. A priority assessment must address the Collatz specialization and global envelope, including the possibility of deriving the same qualitative result from older estimates.
- Brox, *Collatz cycles with few descents*, Acta Arithmetica92 (2000),181–188, [DOI10.4064/aa-92-2-181-188](https://doi.org/10.4064/aa-92-2-181-188). The publisher record and indexed first-page statement were located. Full PDF retrieval from both official endpoints was blocked with403 responses; no claim of reading the full paper is made. Simons–de Weger cite it for the finiteness theorem. This is a remaining literature-review item.


## Bugeaud2022: provenance of the normalized exponent

Yann Bugeaud, B-prime, arXiv:2209.00275v1,1September2022. Primary source https://arxiv.org/pdf/2209.00275;Section1 read directly29September2026. The survey explains the established B/height refinement, credits Feldman and Baker, and records corresponding p-adic refinements due to Yu and two-logarithm results. Our normalization is an application of this established mechanism. The specific uniform Collatz block-growth bound still needs priority investigation; this source supplies no originality claim for it. Theorem1.3 distinguishes an either/or p-adic conclusion from stronger unconditional forms; our explicit argument instead uses the independently checked hypotheses of Bugeaud2002Theorem2.


## Luca2005: ascent runs and exponential cycle bounds

Florian Luca, *On the non-trivial cycles in Collatz's problem*, SUT Journal
of Mathematics41(1)(2005),31-41. Primary publisher PDF:
https://www.rs.tus.ac.jp/sutjmath/_userdata/41-1/03-luca.pdf . All11pages
were read from the publisher PDF; Theorem2.1 onp.33 was visually checked.
It proves t >> log(n), with effective absolute constants, and hence
finiteness with bounded t. Here n is the total shortcut cycle length,
and t counts maximal runs of division exponent1 in the accelerated odd
map. In our notation t equals the number of blocks with k_i>=2, not
necessarily all m blocks: a block with k_i=1 has no exponent1 step in
the accelerated odd map. Thus t<=m, and comparisons must retain this
parameter difference.

Luca's Lemma3.2 propagates logarithmic heights with the sufficient
recurrence C(s+1)>=delta*(C(s)+1), subsequently enlarged to a geometric
bound with a nonexplicit base at least delta+1. The paper therefore
provides relevant prior exponential cycle-complexity bounds and an
archimedean logarithmic-form argument; it does not state our uniform
all-orbit block bound with an explicit base below delta. This inspection
does not establish originality of that latter bound. The printed text
has some indexing typography; our comparison uses the displayed
recurrence and Theorem2.1, without relying on those typographical details.


## Bugeaud1999: direct rational interpolation

Y. Bugeaud, Linear forms in p-adic logarithms and the Diophantine equation (x^n-1)/(x-1)=y^q, Mathematical Proceedings of the Cambridge Philosophical Society127(3)(1999),373-381, DOI10.1017/S0305004199003692. Author primary: https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps . Complete PostScript rendered with portable Ghostscript10.08.0 in SAFER mode. Theorem1 and hypotheses visually read on author pages3-4. Rational clause(6) explicitly uses logarithmic heights, and has no multiplicative-independence requirement once its cardinalities hold. Final journal fulltext was not successfully retrieved; version comparison remains pending. Source hashes and exact scope are in results/interpolation-primary-source-provenance.json. The two-regime argument uses this statement as printed. It does not assume corrections to the differently typeset general Theorem1 of Bugeaud2002.

Bugeaud-Laurent1996 Theorem1, DOI10.1006/jnth.1996.0152, author primary https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.ps , was visually inspected as background; it also uses logarithmic heights. It is not the theorem supplying the refined rational constants here.


## Further prior-art checks,29September2026

- Vigleik Angeltveit, *An improved algorithm for checking the Collatz
  Conjecture for all n<2^N*, arXiv:2602.10466v1,11February2026.
  https://arxiv.org/html/2602.10466v1 . Introduction and Sections2-3 read;
  later sections not fully reviewed. It develops recursive binary-prefix
  sieves and path-merging optimizations. Its proposed higher verification
  ranges are resource projections, not newly established basin bounds.
  Smaller-preimage pruning cannot be transferred automatically to a search
  for cycle minima: the smaller preimage can lie outside the cycle.
- David Rackl,2021 bachelor's thesis, author/academic-hosted complete29-page
  PDF: https://benjamin-hackl.at/downloads/theses/2021-bachelor-rackl.pdf .
  Sections3.3-3.4 were read in full after local download, complementing the
  earlier partial reading. These concern total odd-step cycle length and
  interval tests around multiples of log2(3); no below-delta block-growth
  estimate appears in those sections. Theorem12's displayed iff is stronger
  than the necessity argument provided, so no sufficiency claim is adopted.
  Its implementation appendix was not executed. This is a literature lead,
  not an input to the present proof.

Additional keyword searches found no credible primary source establishing
the present explicit below-delta block bound. A negative search is not proof
of priority. Unreviewed online Collatz claims are not treated as authority.
