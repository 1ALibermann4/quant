# I03-PRE — references

Companion to
[I03-INTRINSIC-RECURRENCE-DECISION-v0.1.md](I03-INTRINSIC-RECURRENCE-DECISION-v0.1.md).

External sources support **definitions** of recurrence exclusion, surrogates,
and distance concentration. They are not project evidence and do not select
D1–D8.

---

## Project-internal

| Artifact | Location |
|----------|----------|
| Geometry Program Review v0.1 | `research/geometry/GEOMETRY-PROGRAM-REVIEW-v0.1.md` @ `547fc57` |
| Geometry references | `research/geometry/references.md` |
| I01 exploratory synthesis | `research/I01/I01-exploratory-synthesis.md` |
| I02 closure | `research/I02/I02-CLOSURE.md` |
| I02 prereg (G0 contract inheritance) | `research/I02/I02-preregistration.md` |

---

## Temporal exclusion / Theiler window

1. Theiler, J. (1986). Spurious dimension from correlation algorithms applied
   to limited time-series data. *Physical Review A*, 34(3), 2427–2432.
   https://doi.org/10.1103/PhysRevA.34.2427
2. Provenzale, A., Smith, L. A., Vio, R., & Murante, G. (1992). Distinguishing
   between low-dimensional dynamics and randomness in measured time series.
   *Physica D*, 58(1–4), 31–49. https://doi.org/10.1016/0167-2789(92)90100-Z
   (space-time separation ideas used to choose exclusion in practice)
3. Marwan, N., Carmen Romano, M., Thiel, M., & Kurths, J. (2007). Recurrence
   plots for the analysis of complex systems. *Physics Reports*, 438(5–6),
   237–329. https://doi.org/10.1016/j.physrep.2006.11.001

---

## Surrogate / null models

4. Theiler, J., Eubank, S., Longtin, A., Galdrikian, B., & Farmer, J. D.
   (1992). Testing for nonlinearity in time series: The method of surrogate
   data. *Physica D*, 58(1–4), 77–94.
   https://doi.org/10.1016/0167-2789(92)90102-R
5. Schreiber, T., & Schmitz, A. (1996). Improved surrogate data for
   nonlinearity tests. *Physical Review Letters*, 77(4), 635–638.
   https://doi.org/10.1103/PhysRevLett.77.635 (IAAFT)
6. Schreiber, T., & Schmitz, A. (2000). Surrogate time series.
   *Physica D*, 142(3–4), 346–382.
   https://doi.org/10.1016/S0167-2789(00)00043-9
7. Kantz, H., & Schreiber, T. (2004). *Nonlinear Time Series Analysis*
   (2nd ed.). Cambridge University Press.
   https://doi.org/10.1017/CBO9780511755798

---

## Distance concentration / nearest neighbors

8. Beyer, K., Goldstein, J., Ramakrishnan, R., & Shaft, U. (1999). When is
   “nearest neighbor” meaningful? In *ICDT 1999* (LNCS 1540). Springer.
   https://doi.org/10.1007/3-540-49257-7_15
9. Aggarwal, C. C., Hinneburg, A., & Keim, D. A. (2001). On the surprising
   behavior of distance metrics in high dimensional space. In *ICDT 2001*
   (LNCS 1973). Springer. https://doi.org/10.1007/3-540-44503-X_27

---

## Recurrence concepts (methodology)

10. Eckmann, J.-P., Kamphorst, S. O., & Ruelle, D. (1987). Recurrence plots of
    dynamical systems. *Europhysics Letters*, 4(9), 973–977.
    https://doi.org/10.1209/0295-5075/4/9/004
11. Webber, C. L., & Marwan, N. (Eds.). (2015). *Recurrence Quantification
    Analysis*. Springer. https://doi.org/10.1007/978-3-319-07155-8

---

## Volatility / heteroskedastic context (null motivation, not a chosen model)

12. Conceptual pointer: GARCH residual–shuffle / wild-bootstrap style surrogates
    appear in econometrics as tools to preserve volatility while breaking other
    structure — any I03 use would require a **preregistered** recipe (D5), not
    an ad hoc fit. No single paper is endorsed as *the* N4 generator here.

---

## Source-type tally

| Type | Count |
|------|------:|
| Peer-reviewed articles | 9 |
| Books / monographs | 2 |
| Project-internal anchors | 5 |
| Explicit non-endorsement note (N4) | 1 |
