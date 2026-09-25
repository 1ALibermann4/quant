# I02 HAT — operational report (derived)

> **NOT SCIENTIFIC EVIDENCE** — synthetic operational acceptance only.

## Provenance

- Schema: `I02-HAT-ARTIFACT-v1`
- Prereg: `I02-PREREG-v0.3`
- Implementation commit: `2ef8f55c06bbb71ac038d92e27225e7ce5c8159a`
- Fixture: `I02-HAT-FIXTURE-v1` / `sha256:196f9c82a878521edb5db02416a6874f526020b989904152157d202accdbd2b5`
- Execution UTC: `2026-09-25T09:12:42.007364+00:00`
- Semantic fingerprint: `sha256:24b33236ef72e1a4aaf3e548f4d09e430ada6f7111b8c0c71744f0b86215a10f`
- Compressed-time MBB: `ACCEPTED CONTRACT RISK`

## Query summary

- Total scheduled: **638**
- Evaluable: **579**
- Skipped: **59**
- Skip reasons: `{'INSUFFICIENT_ADMISSIBLE_POOL': 59}`

## Structural audits (H-criteria)

- `H10_scores`: **True**
- `H11_z_scales`: **True**
- `H12_spearman_grid`: **True**
- `H13_bootstrap`: **True**
- `H14_no_best_star`: **True**
- `H15_artifact`: **True**
- `H16_human_report`: **True**
- `H3_query_pipeline`: **True**
- `H4_common_pool`: **True**
- `H5_hard_availability`: **True**
- `H6_k_equals_50`: **True**
- `H7_representations`: **True**
- `H8_s3_governance`: **True**
- `H9_forecast_atoms`: **True**
- `n_evaluable_audited`: **579**

## Association (structural)

- Spearman cells: **12**
- Grid keys: `['S1|12', 'S1|21', 'S1|3', 'S2|12', 'S2|21', 'S2|3', 'S3_Q|12', 'S3_Q|21', 'S3_Q|3', 'S3_phi|12', 'S3_phi|21', 'S3_phi|3']`
- MBB cells: **36**
- Bootstrap config: B=9999, seed=42, b_values=[20, 40, 80]

## Constants (frozen)

```json
{
  "M": 252,
  "M_Z": [
    3,
    12,
    21
  ],
  "W_RV": 20,
  "W_X": 20,
  "alpha": 0.05,
  "b_sensitivity": [
    20,
    40,
    80
  ],
  "b_star": 40,
  "bootstrap_B": 9999,
  "bootstrap_seed": 42,
  "h": 10,
  "k": 50,
  "stride": 1
}
```

## Note

This Markdown is generated from the canonical JSON artifact. Do not interpret synthetic ρ / CI as scientific evidence.
