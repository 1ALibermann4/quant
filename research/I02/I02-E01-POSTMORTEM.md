# I02 — Post-E01 scientific review (read-only)

> **STATUS :** INVESTIGATION CLOSURE REVIEW  
> **Authority class :** RESEARCH (diagnostic; not SCI)  
> **Preregistration :** [I02-PREREG-v0.3](I02-preregistration.md) — **unchanged**  
> **E01 evidence :** `33d063d` (pin `2b00657`) · baseline `cd0d720` · ops `8d70e97`  
> **Source of truth :** `research/I02/e01/run1/artifact.json` (+ `dataset.json`, `I02-E01.md`)  
>
> ```text
> NO NEW DATA
> NO NEW RUN
> NO NEW METRIC
> NO RETUNING
> NO POST-HOC TEST
> PREREG v0.3 UNCHANGED
> E01 ARTIFACT UNCHANGED
> ```

Labels used below: **FACT** / **INTERPRETATION** / **NOT IDENTIFIABLE**.

---

## 1. Scope and evidence boundary

This review interprets the negative E01 result (`EXPL-ABSENT`) using
**only** persisted E01 material. It does not recompute I02, fetch data,
bin \(Z\), add nonlinear tests, or design I03.

**Persisted and used**

- full 12-cell Spearman + MBB grid (`association`)
- query counts / skip reasons / structural audits
- secondary aggregates: `mean_D_by_S`, `mean_abs_R_by_S`,
  `crps_s_zero_count_by_S`, `r_abs_gt_10_count_by_S`
- compact sample: first and last evaluable query only
- dataset metadata / QC
- documented I01 exploratory synthesis (external to E01 artifact,
  already in-repo)

**Not persisted (hence limited)**

- full per-query \(D_t\), \(R_t\), \(\mathrm{CRPS}\) series
- signed `mean_R`, fraction \(D>0\), concentration of \(D\)/\(R\)
- distribution / quantiles of \(\mathrm{CRPS}_S\)
- joint \((Z,R)\) scatter or residual plots

Compact mode was an operational choice (`store_full_queries=False`);
it bounds what H-C can resolve.

---

## 2. E01 factual recap

Independent read of the canonical artifact (no I02 recomputation).

| S | m | \(n\) | \(\hat\rho\) | CI20 | det20 | CI40 | det40 | CI80 | det80 |
|---|---|------|-------------|------|-------|------|-------|------|-------|
| S1 | 3 | 8149 | −0.0009 | [−0.030,+0.028] | no | [−0.029,+0.028] | no | [−0.029,+0.028] | no |
| S1 | 12 | 8149 | −0.0152 | [−0.064,+0.032] | no | [−0.063,+0.033] | no | [−0.064,+0.036] | no |
| S1 | 21 | 8149 | +0.0162 | [−0.046,+0.074] | no | [−0.050,+0.079] | no | [−0.052,+0.080] | no |
| S2 | 3 | 8149 | +0.0005 | [−0.027,+0.027] | no | [−0.026,+0.026] | no | [−0.026,+0.026] | no |
| S2 | 12 | 8149 | +0.0378 | [−0.010,+0.084] | no | [−0.011,+0.083] | no | [−0.012,+0.085] | no |
| S2 | 21 | 8149 | +0.0458 | [−0.013,+0.101] | no | [−0.017,+0.105] | no | [−0.021,+0.105] | no |
| S3_Q | 3 | 8149 | −0.0004 | [−0.030,+0.028] | no | [−0.029,+0.028] | no | [−0.028,+0.028] | no |
| S3_Q | 12 | 8149 | −0.0085 | [−0.057,+0.040] | no | [−0.057,+0.040] | no | [−0.059,+0.044] | no |
| S3_Q | 21 | 8149 | +0.0227 | [−0.040,+0.081] | no | [−0.045,+0.086] | no | [−0.046,+0.086] | no |
| S3_phi | 3 | 8149 | −0.0003 | [−0.030,+0.028] | no | [−0.028,+0.028] | no | [−0.028,+0.028] | no |
| S3_phi | 12 | 8149 | −0.0065 | [−0.055,+0.042] | no | [−0.055,+0.042] | no | [−0.057,+0.046] | no |
| S3_phi | 21 | 8149 | +0.0262 | [−0.036,+0.085] | no | [−0.041,+0.090] | no | [−0.043,+0.090] | no |

**FACT**

- Detectability: **0/12** at \(b^\star=40\); also 0/12 at \(b\in\{20,80\}\).
- \(n_{\mathrm{valid}}=8149\) every cell; \(B=9999\); no inconclusive MBB cell.
- Scheduled / evaluable / skipped: 8208 / 8149 / 59
  (`INSUFFICIENT_ADMISSIBLE_POOL` only).
- Structural audits H3–H16: all true in artifact.
- S3_Q vs S3_phi: same qualitative null (agreement).
- MS reading in E01 report: **MS-1** (coherent null across \(m\) for each \(S\)).
- K1–K8: none triggered (per E01 report; nothing in the artifact
  contradicts that under the frozen kill definitions as applied there).

**Discrepancy vs `I02-E01.md`:** none material on the grid / detectability /
MS / K status. Rounding in the markdown table matches the artifact.

---

## 3. H-A — \(Z\) information failure

**Claim H-A:** \(Z\) does not meaningfully organize relative predictive
advantage \(R\).

**FACT**

- \(\hat\rho\) is near zero for all \(m\in\{3,12,21\}\) and all \(S\).
- Signs flip across \(m\) within \(S\) (e.g. S1: −/−/+; S2: +/+/+;
  S3: −/−/+) at magnitudes \(\ll\) CI half-widths — consistent with
  numerical noise around a null, not a stable signed effect.
- No \(m\) is detectable; none reverses the null under \(b\)-robustness.
- MS-1 (null) is supported by the complete grid, not by discarding scales.

**INTERPRETATION (precise)**

E01 supports:

> *no detectable **monotone** organization of \(R\) by \(Z^{(m)}\)*
> under the frozen evidence unit.

E01 does **not** support the stronger claim:

> *“\(Z\) contains no information (about anything).”*

Some CIs (e.g. S2, \(m=21\), \(b^\star\): about \([-0.017,+0.105]\)) remain
compatible with modest monotone effects that the run did not detect;
that is uncertainty, not evidence of an effect.

| Classification | |
|----------------|--|
| **H-A (weak form: no detectable monotone \(Z\leftrightarrow R\))** | **SUPPORTED INTERPRETATION** |
| **H-A (strong form: \(Z\) is informationless)** | **NOT IDENTIFIABLE** (and not claimed) |

---

## 4. H-B — monotonicity failure

Spearman only probes **monotone** association.

**FACT**

- No persisted diagnostic in E01 exposes non-monotone \((Z,R)\) structure
  (no scatters, no residual series, no alternative dependence stats).

**INTERPRETATION**

```text
NON-MONOTONE DEPENDENCE NOT TESTED BY I02-E01
```

H-B remains a logical open possibility. It must **not** be used as a
rescue of H1-I02: E01 answered the preregistered monotone question
negatively; it did not affirm a nonlinear alternative.

| Classification | |
|----------------|--|
| **H-B** | **NOT IDENTIFIABLE** as an explanation of E01; **open possibility only** (not a supported interpretation) |

---

## 5. H-C — residual-\(X\) failure

**Claim H-C:** \(X\) may have little or no useful incremental predictive
advantage over \(S_1/S_2/S_3\), leaving little structure for \(Z\) to
organize.

Recall: \(D=\mathrm{CRPS}_S-\mathrm{CRPS}_X\); **\(D>0\) ⇒ \(X\) better**.

### Persisted aggregates (FACT)

| Comparator | mean \(D\) | mean \|R\| | # \|R\|>10 | # CRPS_S=0 |
|------------|------------|------------|------------|------------|
| S1 | **−6.59e−4** | 0.833 | 4 | 0 |
| S2 | **−7.23e−4** | 0.836 | 6 | 0 |
| S3_Q | **−6.47e−4** | 0.831 | 5 | 0 |
| S3_phi | **−6.41e−4** | 0.831 | 5 | 0 |

**FACT**

- mean \(D<0\) for **every** comparator → on average, each \(S\) has
  **lower CRPS than \(X\)** (comparators better unconditionally).
- Pattern is **common across** S1 / S2 / S3 charts (not S1-only).
- Extreme \|R\| counts are tiny (4–6 / 8149).
- Compact samples: first evaluable query has \(D\approx 0\); last has
  \(D>0\) for all \(S\) (local \(X\) better) — so **heterogeneity exists**,
  but its prevalence is **NOT IDENTIFIABLE** (no fraction \(D>0\), no
  concentration stats persisted).

**INTERPRETATION**

- Unconditional residual advantage for \(X\) is **not** evidenced; the
  opposite sign of mean \(D\) is evidenced.
- Whether mean \(D\) is “tiny relative to score scale” is only partially
  addressable: sample query CRPS values are \(\sim 7\times 10^{-4}\) to
  \(1\times 10^{-3}\), so \(|\mathrm{mean}\,D|\sim 6\text{–}7\times 10^{-4}\)
  is **order-comparable** to those sample CRPS levels
  (**INTERPRETATION**, not a formal scale audit — mean CRPS not persisted).
- Large mean \|R\| with negative mean \(D\) is compatible with frequent
  sign changes / heavy tails of \(R\) without average \(X\) advantage
  (**INTERPRETATION**). Signed mean \(R\): **NOT IDENTIFIABLE**.

**Implication for the null \(Z\leftrightarrow R\)**

H1-I02 was about association of \(R\) with \(Z\), **not** \(\mathbb{E}[R]>0\)
(prereg §1.4). E01’s null association still stands on its own.

But H-C changes the *scientific reading* of that null:

- If \(X\) is on average **not** better than the frozen controls, then
  asking whether volatility-regime instability organizes “\(X\)’s
  residual advantage” is asking \(Z\) to organize a residual that is,
  on average, an **\(S\)-advantage**.
- That makes “why doesn’t \(Z\) modulate \(R\)?” a **secondary** question
  relative to “does a broad residual \(X\) advantage exist at all under
  I02’s CRPS/\(R\) design?”

| Classification | |
|----------------|--|
| **H-C (average / broad residual \(X\) advantage absent)** | **SUPPORTED INTERPRETATION** |
| **H-C (“\(X\) never helps on any date”)** | **CONTRADICTED** by the last-query sample (\(D>0\)); prevalence **NOT IDENTIFIABLE** |

---

## 6. \(R\) denominator diagnostic

**FACT**

- \(\mathrm{CRPS}_S=0\) count = 0 for all \(S\) (no structural zero-denominator
  mass in the skip sense).
- Extreme \|R\|>10: 4–6 queries only.
- Distribution / range / quantiles of \(\mathrm{CRPS}_S\): **not persisted**.
- Explicit small-denominator concentration diagnostics: **not persisted**.

**INTERPRETATION**

No evidence in the artifact that denominator pathology *drove* the
grid-wide Spearman null. Large mean \|R\| could still reflect variable
\(\mathrm{CRPS}_S\), but that is not demonstrated.

| Classification | |
|----------------|--|
| Denominator | **NO EVIDENT DENOMINATOR ISSUE** (with residual uncertainty: full \(\mathrm{CRPS}_S\) law **NOT IDENTIFIABLE**) |

---

## 7. Adversarial-control interpretation

**FACT**

- Null \(Z\leftrightarrow R\) is already present **vs S1** (level), not only
  vs richer \(S_2/S_3\).
- Richer controls (S2, S3_Q, S3_phi) do not reveal a hidden association
  that S1 missed.
- Unconditional mean \(D\) is similarly negative vs all four branches.

**INTERPRETATION**

The negative association result does **not** “strengthen as controls
become richer” in the sense of a gradient from S1→S3; the null is
**already complete against the simplest volatility-level adversary**.
That weakens any story that I02’s geometry retained residual predictive
content *systematically linked to \(Z\)* beyond simple volatility summaries.
It does **not**, by itself, settle whether geometry ever beats those
summaries on selected dates (see H-C / I01).

---

## 8. Relation to I01

From [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
(documented exploratory record only):

- L2 reduced \(H_{\mathrm{raw}}\) vs B0; effect heavily volatility-driven;
  shape nearly absent.
- `rv_W` control explained part but not all of the L2 vs-naive story.
- Remaining advantage vs `rv_W` was **highly concentrated** in stress/tail
  periods; median \(D_{\mathrm{vol}}\) negative; original broad I01 hypothesis
  **not recommended for confirmation**.

| Question | Reading |
|----------|---------|
| **A.** Does I02 reproduce a **broad residual geometric advantage**? | **No evidence** of broad average CRPS advantage for \(X\) vs frozen \(S\) (mean \(D<0\)). Compatible with I01’s finding that typical days do not favor geometry vs a volatility control. |
| **B.** Does I02 support residual I01 structure as **monotone in \(Z\)**? | **No** — EXPL-ABSENT on the \(Z\leftrightarrow R\) grid. |
| **C.** Compatibility if I01 residual was **episodic / tail-concentrated**? | **Compatible**: I01 stressed concentration and non-uniform regimes; I02’s Spearman/\(Z\) design would miss episodic non-monotone structure (H-B open; not tested). |

**Do not claim I02 “disproves I01”.** Different estimands, targets, and
controls. Tension: I01 left a regime-conditional *candidate*; I02’s
first frozen test of “organized by \(Z\) via \(R\)” found nothing monotone.

---

## 9. What E01 weakens

Claims **weakened by frozen E01** (UNQUALIFIED SPY path only):

1. Broad **monotone** association between \(Z^{(m)}\) and \(R^{(S)}\) under
   I02-PREREG-v0.3.
2. Robustness of such an association across \(m\in\{3,12,21\}\) and
   \(b\in\{20,40,80\}\) (vacuously: nothing to be robust *for*).
3. A **metric-specific** S3_Q or S3_phi hidden signal (charts agree on null).
4. The hope that a simple “state-dependent incremental value of \(X\)”
   would appear as Spearman(\(Z,R\)) on this design/data class.

---

## 10. What E01 leaves open

Logically open; **not** invitations to retune I02:

- nonlinear / non-monotone \(Z\)–\(R\) dependence (not tested);
- event-localized / episodic dependence (not tested under E01 primary);
- other state variables than this \(Z\);
- other representation / scoring families;
- other assets / universes;
- UNQUALIFIED-data artifacts vs a future C02 path;
- the **existence and episodic structure of residual \(X\) advantage**
  under I02’s own CRPS/\(D\) objects (only averages + 2 samples persisted).

---

## 11. Investigation disposition

**Recommendation: A — CLOSE I02 / NEGATIVE EXPLORATORY RESULT**

H1-I02 received **no** exploratory support on the preregistered evidence
unit. E01 is interpretable (not execution-invalid). Continuing I02 only
to “rescue” a negative result would violate the negative-result policy.

- **B** rejected: no unanswered *preregistered* H1 cell remains; H-B/H-C
  deepen interpretation but are not unfinished H1 tests.
- **C** rejected: E01 is not inconclusive due to data/execution failure;
  compact persistence limits H-C detail but does not invalidate the
  primary EXPL-ABSENT grid.

Preserve I02 as a **completed negative exploratory investigation**.
Any materially different scientific question becomes **I03+**, decided
separately.

---

## 12. Candidate I03 question (not designed)

If a distinct follow-on is ever considered, the highest-value question
suggested by this review is **not** “retry Spearman(\(Z,R\)) with new
knobs,” but:

> **CANDIDATE I03 QUESTION:** Under I02’s CRPS forecast objects, does a
> *residual* predictive advantage of the geometric representation \(X\)
> over the frozen volatility summaries exist in any scientifically
> specified (non-monotone / episodic) sense — and if so, is it organized
> by a state distinct from the failed \(Z\leftrightarrow R\) monotone link?

No metrics, parameters, or runs are defined here.
