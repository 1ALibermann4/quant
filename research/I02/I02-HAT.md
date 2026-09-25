# I02 — Human Acceptance Test (HAT)

> **STATUS :** `PRE-RUN`
> **Authority class :** OPERATIONAL ACCEPTANCE (not scientific evidence)
> **Preregistration :** [I02-PREREG-v0.3](I02-preregistration.md) — **unchanged**
> **L2 baseline :** `16cfee2` (pin `653ffbd`) — L2-PASS
> **HAT_BASELINE :** *(this commit — filled at PRE-RUN commit)*
>
> ```text
> PREREG v0.3 UNCHANGED
> CORE DESIGN UNCHANGED
> NO MARKET DATA
> NO EXPLORATORY SCIENTIFIC RUN
> NO POST-HOC CHOICE
> SYNTHETIC HAT ≠ SCIENTIFIC EVIDENCE
> COMPRESSED_TIME_MBB = ACCEPTED CONTRACT RISK
> ```

---

## 0. Purpose

Validate that the **assembled I02 runtime** operates end-to-end through
its real operator boundary on a controlled synthetic fixture and emits
the expected structural artefacts.

This HAT is **not** scientific evidence, exploratory evidence, or
parameter validation.

---

## 1. Real entry point

```text
py -3.12 -m quant.i02 --input <fixture.npz> --output-dir <dir> --fixture-id I02-HAT-FIXTURE-v1
```

Console script (when installed): `i02-runtime`.

**Allowed operator arguments:** `--input`, `--output-dir`, `--fixture-id`
(label only).

**Forbidden:** any scientific knobs (`W_X`, `M`, `h`, `k`, `B`, `b`,
`alpha`, S3 primary, etc.).

Path exercised:

```text
operator command
  → fixture load
  → evaluate_series (query pipeline)
  → X / S1 / S2 / S3_Q / S3_phi
  → CRPS / D / R
  → Z^(3,12,21)
  → Spearman grid
  → MBB (B=9999, seed=42, b∈{20,40,80})
  → artifact.json (canonical)
  → report.md (derived from JSON only)
```

---

## 2. Fixture (PRE-RUN)

| Field | Value |
|-------|-------|
| ID | `I02-HAT-FIXTURE-v1` |
| Path | `research/I02/hat/fixture_v1.npz` |
| Length \(N\) | **900** |
| SHA-256 | `sha256:196f9c82a878521edb5db02416a6874f526020b989904152157d202accdbd2b5` |
| Generator | `quant.i02.fixture_hat.generate_hat_returns` |
| Construction | deterministic multi-frequency × amplitude modulation (no RNG) |
| Market data | **NONE** |

---

## 3. PRE-RUN structural expectations

Recorded **before** first execution. Scientific ρ / CI signs are
**not** expected.

| ID | Expectation |
|----|-------------|
| E1 | Input loads; fixture hash matches §2 |
| E2 | ≥1 evaluable query completes full forecast pipeline |
| E3 | Branches `X`, `S1`, `S2`, `S3_Q`, `S3_phi` all present on evaluable queries |
| E4 | `S3_Q` and `S3_phi` both retained; no primary/best S3 |
| E5 | \(k=50\) for every evaluable forecast |
| E6 | Common \(A_t\): every neighbor ∈ shared pool |
| E7 | Hard availability: every selected \(s\) has \(s+10\le t\) |
| E8 | Predictive measures contain exactly 50 atoms |
| E9 | \(Z\) emits \(m\in\{3,12,21\}\) |
| E10 | Spearman grid has 12 cells (`4` comparators × `3` scales) |
| E11 | MBB uses `B=9999`, `seed=42`, `b∈{20,40,80}` when \(n\) permits |
| E12 | Canonical `artifact.json` persisted |
| E13 | Human `report.md` derived from artifact |
| E14 | Second identical run: semantic fingerprint identical |

**Not expected / not used for verdict:** sign of ρ, magnitude of ρ,
CI excluding 0, “good performance”.

---

## 4. Acceptance criteria (H1–H18)

| ID | Criterion | PRE-RUN status |
|----|-----------|----------------|
| H1 | Runtime entry point exits successfully | PENDING |
| H2 | Fixture identity/hash recorded | PENDING |
| H3 | ≥1 complete evaluable query | PENDING |
| H4 | Common \(A_t\) | PENDING |
| H5 | Hard availability | PENDING |
| H6 | \(k=50\) | PENDING |
| H7 | Representations X/S1/S2/S3_Q/S3_phi | PENDING |
| H8 | S3 dual-branch governance | PENDING |
| H9 | 50 atoms / multiplicity | PENDING |
| H10 | CRPS / D / R emitted | PENDING |
| H11 | Z scales {3,12,21} | PENDING |
| H12 | Complete Spearman grid | PENDING |
| H13 | MBB B=9999 seed=42 b={20,40,80} | PENDING |
| H14 | No best-S / best-m / best-b / best-S3 | PENDING |
| H15 | Canonical artifact | PENDING |
| H16 | Human report from artifact | PENDING |
| H17 | Reproducibility (2 runs) | PENDING |
| H18 | Post-HAT regression green | PENDING |

---

## 5. Commands (to execute after HAT_BASELINE)

```text
# Run #1
py -3.12 -m quant.i02 --input research/I02/hat/fixture_v1.npz --output-dir research/I02/hat/run1 --fixture-id I02-HAT-FIXTURE-v1

# Run #2 (identical; no code changes)
py -3.12 -m quant.i02 --input research/I02/hat/fixture_v1.npz --output-dir research/I02/hat/run2 --fixture-id I02-HAT-FIXTURE-v1

# Regression
py -3.12 -m pytest tests/i02 -q
py -3.12 -m pytest -q
```

---

## 6. POST-RUN evidence

*(append after execution — do not fill before HAT_BASELINE)*

---

## 7. Verdict

**CURRENT:** `PRE-RUN` — not executed.
