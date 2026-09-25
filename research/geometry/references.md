# Geometry program — references (v0.1)

Companion to [GEOMETRY-PROGRAM-REVIEW-v0.1.md](GEOMETRY-PROGRAM-REVIEW-v0.1.md).

**Scope.** Bibliographic support for the literature sections of the review.
External sources are **not** project evidence. Prefer peer-reviewed /
monograph / arXiv-identified primary sources.

**Counts (this file):** ~28 bibliographic entries · types: monograph / book
chapter, peer-reviewed article, arXiv preprint, handbook/review.

---

## Project-internal (authority for I01/I02 history)

| Artifact | Path / commit |
|----------|----------------|
| I01 exploratory synthesis | `research/I01/I01-exploratory-synthesis.md` |
| I01 hypothesis | `research/I01/hypothesis.md` |
| I02 preregistration v0.3 | `research/I02/I02-preregistration.md` |
| I02 L2 contract | `research/I02/I02-L2-CONTRACT-TEST.md` |
| I02 HAT | `research/I02/I02-HAT.md` |
| I02 E01 | `research/I02/e01/run1/` · evidence `33d063d` · pin `2b00657` |
| I02 postmortem | `research/I02/I02-E01-POSTMORTEM.md` · `f581416` |
| I02 closure | `research/I02/I02-CLOSURE.md` · `68f7f56` · pin `c4ac436` |

---

## A. Embedding / dynamical systems

1. Takens, F. (1981). Detecting strange attractors in turbulence. In *Dynamical
   Systems and Turbulence, Warwick 1980* (Lecture Notes in Mathematics 898).
   Springer. https://doi.org/10.1007/BFb0091924
2. Sauer, T., Yorke, J. A., & Casdagli, M. (1991). Embedology. *Journal of
   Statistical Physics*, 65, 579–616. https://doi.org/10.1007/BF01053745

## B. Recurrence analysis

3. Marwan, N., Carmen Romano, M., Thiel, M., & Kurths, J. (2007). Recurrence
   plots for the analysis of complex systems. *Physics Reports*, 438(5–6),
   237–329. https://doi.org/10.1016/j.physrep.2006.11.001
4. Webber, C. L., & Marwan, N. (Eds.). (2015). *Recurrence Quantification
   Analysis*. Springer. https://doi.org/10.1007/978-3-319-07155-8

## C. Diffusion geometry / manifold methods

5. Coifman, R. R., & Lafon, S. (2006). Diffusion maps. *Applied and
   Computational Harmonic Analysis*, 21(1), 5–30.
   https://doi.org/10.1016/j.acha.2006.04.006
6. Belkin, M., & Niyogi, P. (2003). Laplacian eigenmaps for dimensionality
   reduction and data representation. *Neural Computation*, 15(6), 1373–1396.
   https://doi.org/10.1162/089976603321780317

## D. SPD / Riemannian covariance geometry

7. Pennec, X., Fillard, P., & Ayache, N. (2006). A Riemannian framework for
   tensor computing. *International Journal of Computer Vision*, 66, 41–66.
   https://doi.org/10.1007/s11263-005-3222-z
8. Bhatia, R., Jain, T., & Lim, Y. (2019). On the Bures–Wasserstein distance
   between positive definite matrices. *Expositiones Mathematicae*, 37(2),
   165–191. https://doi.org/10.1016/j.exmath.2018.01.002
9. van Driel, R., & others related BW geometry surveys — see also arXiv
   treatments of Bures–Wasserstein on positive-definite matrices, e.g.
   https://arxiv.org/abs/2001.08056 (geometry extensions; arXiv).

## E. Optimal transport / Wasserstein in finance-adjacent work

10. Villani, C. (2009). *Optimal Transport: Old and New*. Springer.
    https://doi.org/10.1007/978-3-540-71050-9
11. Blanchet, J., Chen, L., & Zhou, X. Y. (related line): distributionally
    robust mean-variance with Wasserstein distances — e.g.
    https://arxiv.org/abs/1802.04885
12. Nguyen, V. A., Kuhn, D., Mohajerin Esfahani, P., et al. Mean-covariance
    robust risk / Gelbrich–Wasserstein connections — e.g.
    https://arxiv.org/abs/2112.09959
13. Classical Gaussian \(W_2\) / Bures link: Givens, C. R., & Shortt, R. M.
    (1984). A class of Wasserstein metrics for probability distributions.
    *Michigan Mathematical Journal*, 31(2), 231–240.
    https://doi.org/10.1307/mmj/1029003026

## F. Topological data analysis (finance)

14. Gidea, M., & Katz, Y. (2018). Topological data analysis of financial time
    series: Landscapes of crashes. *Physica A*, 491, 820–834.
    https://doi.org/10.1016/j.physa.2017.09.028  
    Preprint: https://arxiv.org/abs/1703.04385
15. Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An
    Introduction*. AMS. (methods monograph; not finance claims)

## G. Information geometry

16. Amari, S., & Nagaoka, H. (2000). *Methods of Information Geometry*. AMS /
    Oxford. ISBN 978-0-8218-4302-4
17. Amari, S. (2016). *Information Geometry and Its Applications*. Springer.
    https://doi.org/10.1007/978-4-431-55978-8

## H. Classical multivariate / Mahalanobis

18. Mahalanobis, P. C. (1936). On the generalized distance in statistics.
    *Proceedings of the National Institute of Sciences of India*, 2, 49–55.
19. Mardia, K. V., Kent, J. T., & Bibby, J. M. (1979). *Multivariate Analysis*.
    Academic Press. (standard reference for Mahalanobis applications)

## I. Hierarchical / ultrametric (descriptive finance-adjacent)

20. Tumminello, M., Lillo, F., & Mantegna, R. N. (2010). Correlation,
    hierarchies, and networks in financial markets. *Journal of Economic
    Behavior & Organization*, 75(1), 40–58.
    https://doi.org/10.1016/j.jebo.2010.01.004
21. Mantegna, R. N. (1999). Hierarchical structure in financial markets.
    *European Physical Journal B*, 11, 193–197.
    https://doi.org/10.1007/s100510050929

## J. Metric learning (cautionary / methodological)

22. Bellet, A., Habrard, A., & Sebban, M. (2013). A survey on metric learning
    for feature vectors and structured data.
    https://arxiv.org/abs/1306.6709
23. Kulis, B. (2013). Metric learning: A survey. *Foundations and Trends in
    Machine Learning*, 5(4), 287–364. https://doi.org/10.1561/2200000019

## K. Negative / caution notes retained by the review

24. Nonstationarity and multiple testing undermine many “early warning”
    geometric claims; treat crisis-timed TDA results as **historical
    descriptive**, not prospective validation (review interpretation of
    items 14–15).
25. p-adic market models: no entry elevated to “established finance
    geometry”; niche literature exists but is classified
    **CURRENTLY UNJUSTIFIED** for this program until stronger primary
    evidence appears (intentionally under-cited to avoid false authority).

## L. Project governance (context, not geometry math)

26. QDP v0.1 / DR-007 / DR-008 — `docs/governance/` and `docs/adr/` as cited
    in `AGENTS.md`.

---

## Source-type tally

| Type | Approx. count in §§A–J |
|------|-------------------------|
| Peer-reviewed journal articles | 12 |
| Books / monographs / edited volumes | 7 |
| arXiv preprints (clearly identified) | 5 |
| Classical / historical papers | 2 |
| Explicit caution / non-citation (p-adic) | 1 |

*Totals are approximate; some items are both journal + arXiv.*
