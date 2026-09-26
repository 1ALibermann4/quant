# I03-E01 — exploratory / unqualified report (derived)

> **EXPLORATORY / UNQUALIFIED** — not confirmatory; not promotable.
>
> ```text
> EXPLORATORY / UNQUALIFIED
> NO SCI CLAIM
> NO PRED
> NO ECON
> NO PARAMETER TUNING
> ```

## Provenance

- Schema: `I03-ARTIFACT-v1`
- Prereg: `I03-PREREG-v0.1`
- Input hash: `sha256:bde9a3045659bcb6ffdde99c52d7b088662456ed5d42737662f7c8384091c02e`
- Implementation: `1dfdae6775925c0f76a2761344f8aa245f29ff6a`
- Mode: `E01_EXPLORATORY_UNQUALIFIED`
- Dataset: `SPY` / `canonical_input_amendment_B` `1.6.0`
- Sessions: `1993-01-29` → `2026-09-23` (n=`8470`)
- Price SHA-256: `sha256:bc0d68b080f1f42c56f01da43820c11425ca1fc3a80bfb0ca32647821c2488d1`
- Returns SHA-256: `sha256:bde9a3045659bcb6ffdde99c52d7b088662456ed5d42737662f7c8384091c02e`

## Frozen config (from artifact)

- `W_X` = `20`
- `M` = `252`
- `W_sigma` = `20`
- `tau` = `20`
- `K` = `[10, 25, 50]`
- `P` = `3`
- `B_N4` = `999`
- `B_N3` = `999`
- `alpha` = `0.05`
- `n_min` = `250`
- `iaaft_I_max` = `100`
- `iaaft_eps` = `1e-08`

## Blocks

- period 1: [0, 2822] n=2823
- period 2: [2823, 5645] n=2823
- period 3: [5646, 8469] n=2824

## E-MND

- period 1: n_queries=2571 skip_x=252 skip_pool=0 theta={10: 3.859335495339422, 25: 4.095941103288431, 50: 4.29290062392035}
- period 2: n_queries=2823 skip_x=0 skip_pool=0 theta={10: 3.685117805772465, 25: 3.8978688458478246, 50: 4.074203240654269}
- period 3: n_queries=2824 skip_x=0 skip_pool=0 theta={10: 3.5321969175125383, 25: 3.731692535088638, 50: 3.8991966311715283}

## Locality (DIAGNOSTIC — NON-PROMOTIONAL)

- period 1: Lambda=0.5136658157041173 Gamma=0.3008102094612582 hard=False
- period 2: Lambda=0.4968686821484349 Gamma=0.29215259164476165 hard=False
- period 3: Lambda=0.4758921405460369 Gamma=0.29144092914181696 hard=False

## Null batteries

- N4 valid=True reason=None B=999 Z_frac=0.9976387249114522
- N3 valid=False reason=N3_IAAFT_NONCONV_FRAC B_req=999 converged=0 nonconv=999

## Predicates / coherence

- V=True E=False
- C4=False C3=False F4=False

## Structural verdict (internal)

- structural label: **INCONCLUSIVE**
- nd_code: `None`
- reason: `NEG_E`

## Exploratory verdict (E01 reporting)

- exploratory label: **EXPL-INCONCLUSIVE**
- mapping: `PASS→EXPL-SUPPORT; FAIL→EXPL-ABSENT; INCONCLUSIVE→EXPL-INCONCLUSIVE`
- EXPL-SUPPORT ≠ SCI-PASS
- EXPL-ABSENT ≠ SCI-FAIL
- EXPL-INCONCLUSIVE ≠ evidence of absence

## Timing (engineering only)

- total_seconds: 7218.321
- workers_requested: 4
- workers_used: 4
- checkpoint_dir: research\I03\e01\run2_ckpt
- resume: False
- note: engineering observation only; no scientific performance gate

## Note

This Markdown is generated from the canonical JSON artifact. E01 is exploratory/unqualified under DR-007/DR-008. No SCI/PRED/ECON claim.
