# I03 HAT — operational report (derived)

> **NOT SCIENTIFIC EVIDENCE** — synthetic operational acceptance only.
>
> ```text
> SYNTHETIC HAT
> NOT MARKET EVIDENCE
> NOT SCIENTIFIC EVIDENCE
> ```

## Provenance

- Schema: `I03-ARTIFACT-v1`
- Prereg: `I03-PREREG-v0.1`
- Input hash: `sha256:0ed3625a7ed4a19e2fb75e04c8b906a92cc01be54446f61eb53c6cde1cf142dc`
- Implementation: `f6684edeb8cbeda040e5ad3b611b63f11af4cd31`
- Mode: `SYNTHETIC_HAT`

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

- period 1: [0, 799] n=800
- period 2: [800, 1599] n=800
- period 3: [1600, 2399] n=800

## E-MND

- period 1: n_queries=548 skip_x=252 skip_pool=0 theta={'10': 4.454472207833898, '25': 4.789826591665865, '50': 5.091833752373569}
- period 2: n_queries=800 skip_x=0 skip_pool=0 theta={'10': 4.235810954484789, '25': 4.541733749770569, '50': 4.80704591299855}
- period 3: n_queries=800 skip_x=0 skip_pool=0 theta={'10': 4.24559516682604, '25': 4.551048703702043, '50': 4.809975519030576}

## Locality (DIAGNOSTIC — NON-PROMOTIONAL)

- period 1: Lambda=0.5957087790477299 Gamma=0.3628073418036484 hard=False
- period 2: Lambda=0.5879055887418743 Gamma=0.33553976968052074 hard=False
- period 3: Lambda=0.5755344509631465 Gamma=0.3417829897757426 hard=False

## Null batteries

- N4 valid=True reason=None B=999 Z_frac=0.9916666666666667
- N3 valid=False reason=N3_IAAFT_NONCONV_FRAC B_req=999 converged=0 nonconv=999

## Predicates / coherence

- V=False E=False
- C4=False C3=False F4=True

## Verdict (synthetic — not market evidence)

- label: **INCONCLUSIVE**
- nd_code: `None`
- reason: `NEG_V`

## Timing (engineering only)

- total_seconds: 1372.031
- note: engineering observation only; no scientific performance gate

## Note

This Markdown is generated from the canonical JSON artifact. Do not interpret the synthetic verdict as market evidence.
