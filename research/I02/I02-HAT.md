# I02 — Human Acceptance Test (HAT)

> **STATUS :** `HAT-PASS`
> **Authority class :** OPERATIONAL ACCEPTANCE (not scientific evidence)
> **Preregistration :** [I02-PREREG-v0.3](I02-preregistration.md) — **unchanged**
> **L2 baseline :** `16cfee2` (pin `653ffbd`) — L2-PASS
> **HAT_BASELINE :** `cd6dfb0` (`test(I02): prepare preregistered HAT`)
> **Runtime fix (HAT-I1) :** `2ef8f55` (ASCII success message — Windows cp1252)
> **Evidence commit :** `dedf3ff` (`test(I02): record successful HAT`)
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
$env:PYTHONPATH = "src"
py -3.12 -m quant.i02 --input research/I02/hat/fixture_v1.npz --output-dir <dir> --fixture-id I02-HAT-FIXTURE-v1
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

Recorded **before** first execution (`cd6dfb0`). Scientific ρ / CI signs
are **not** expected.

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

| ID | Criterion | Result |
|----|-----------|--------|
| H1 | Runtime entry point exits successfully | **PASS** |
| H2 | Fixture identity/hash recorded | **PASS** |
| H3 | ≥1 complete evaluable query | **PASS** (579) |
| H4 | Common \(A_t\) | **PASS** |
| H5 | Hard availability | **PASS** |
| H6 | \(k=50\) | **PASS** |
| H7 | Representations X/S1/S2/S3_Q/S3_phi | **PASS** |
| H8 | S3 dual-branch governance | **PASS** |
| H9 | 50 atoms / multiplicity | **PASS** |
| H10 | CRPS / D / R emitted | **PASS** |
| H11 | Z scales {3,12,21} | **PASS** |
| H12 | Complete Spearman grid | **PASS** (12 cells) |
| H13 | MBB B=9999 seed=42 b={20,40,80} | **PASS** (36 cells) |
| H14 | No best-S / best-m / best-b / best-S3 | **PASS** |
| H15 | Canonical artifact | **PASS** |
| H16 | Human report from artifact | **PASS** |
| H17 | Reproducibility (2 runs) | **PASS** (`SEMANTIC_IDENTICAL`) |
| H18 | Post-HAT regression green | **PASS** (97/97 I02; 697/697 repo) |

---

## 5. Commands executed

```text
# HAT_BASELINE
cd6dfb0  test(I02): prepare preregistered HAT

# HAT-I1 fix (Unicode print on Windows cp1252)
2ef8f55  fix(I02): use ASCII success message in HAT runtime

# Run #1
$env:PYTHONPATH = "src"
py -3.12 -m quant.i02 --input research/I02/hat/fixture_v1.npz --output-dir research/I02/hat/run1 --fixture-id I02-HAT-FIXTURE-v1

# Run #2 (identical; no code changes between runs)
py -3.12 -m quant.i02 --input research/I02/hat/fixture_v1.npz --output-dir research/I02/hat/run2 --fixture-id I02-HAT-FIXTURE-v1

# Reproducibility
py -3.12 -m quant.i02.compare_hat research/I02/hat/run1/artifact.json research/I02/hat/run2/artifact.json
# → SEMANTIC_IDENTICAL

# Regression
py -3.12 -m pytest tests/i02 -q   # 97 passed
py -3.12 -m pytest -q             # 697 passed
```

---

## 6. POST-RUN evidence

### 6.1 Query counts

| Metric | Value |
|--------|-------|
| Scheduled | **638** |
| Evaluable | **579** |
| Skipped | **59** |
| Skip reasons | `INSUFFICIENT_ADMISSIBLE_POOL`: 59 |

### 6.2 Branches observed

`X`, `S1`, `S2`, `S3_Q`, `S3_phi` — no singular `S3` winner.

### 6.3 Association / MBB

| Item | Value |
|------|-------|
| Spearman grid | **12** cells (4×3) |
| MBB cells | **36** (12×3 b) |
| B | **9999** |
| seed | **42** |
| b executed | **{20, 40, 80}** |
| n_valid (all cells) | **579** |
| n_finite_replicates | **9999** (no cell inconclusive on this fixture) |

### 6.4 Reproducibility

| Run | Path | Wall-clock (s) |
|-----|------|----------------|
| #1 | `research/I02/hat/run1/` | ≈ 684 |
| #2 | `research/I02/hat/run2/` | ≈ 730 |

Semantic compare: **SEMANTIC_IDENTICAL**
(`sha256:fd2ac01e1dba59178063a5c857add206fe7958a4a63ded1f0c21bb7b049ec2ea`
on payloads with non-scientific metadata excluded).

Stored artifact semantic_fingerprint field (run1/run2 identical):
`sha256:24b33236ef72e1a4aaf3e548f4d09e430ada6f7111b8c0c71744f0b86215a10f`

### 6.5 Issues

| ID | Class | Description | Resolution |
|----|-------|-------------|------------|
| HAT-I1 | runtime | Success `print` used Unicode arrow → Windows cp1252 crash **after** artifact write | Fixed `2ef8f55`; both acceptance runs re-executed with clean exit |
| HAT-I2 | tests | L2 static audits false-positive on denial string `best_s3` and operational `argparse` | Narrowed L2 patterns (post-HAT regression) |

No HAT-I3…I5. No I4/I5 contract blockers.

### 6.6 Artifact paths

- `research/I02/hat/run1/artifact.json` + `report.md`
- `research/I02/hat/run2/artifact.json` + `report.md`
- Fixture: `research/I02/hat/fixture_v1.npz`

### 6.7 Runtime diagnostic

- Fixture size: N=900
- Evaluable queries: 579
- Wall-clock ≈ 11–12 minutes / run (dominated by B=9999 × 36 MBB cells)
- No performance gate applied

---

## 7. Verdict

\[
\boxed{\texttt{HAT-PASS}}
\]

H1–H18 satisfied. Synthetic operational acceptance only.
**HAT-PASS ≠ scientific evidence. HAT-PASS ≠ exploratory run. HAT-PASS ≠ SCI-PASS.**

Next authorized boundary (human decision): exploratory E01-style run on
declared data class under DR-007 **UNQUALIFIED** — separate from this HAT.
