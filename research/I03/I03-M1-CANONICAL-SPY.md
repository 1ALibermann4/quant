# I03 — M1 Canonical SPY input (materialized)

> **Verdict :** `M1_CANONICAL_SPY: PASS`  
> **Class :** transport materialization only (Amendment B)  
> **Prereg :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a` — **unchanged**  
> **E01 :** **NOT executed**

```text
NO I03-E01 EXECUTION
NO MARKET SCIENTIFIC RESULT
NO MARKET DATA DOWNLOAD
NO PREREG CHANGE
NO PARAMETER CHANGE
```

## Artifact

| Path | Role |
|------|------|
| `data/exploratory/canonical_i03_spy_v1/returns.npy` | float64 LE returns |
| `data/exploratory/canonical_i03_spy_v1/manifest.json` | provenance + dual hashes |

Schema: `I03-CANONICAL-INPUT-v1`  
Source stem: `UNQUALIFIED_SPY_20260924T120016Z`  
Sessions: 8470 (`1993-01-29` … `2026-09-23`)  
Classification: EXPLORATORY / UNQUALIFIED

## Hashes

| Kind | SHA-256 |
|------|---------|
| SOURCE CSV FILE | `sha256:ac7c6a7f081e3548d94c6c744a31b3398ccffae5129799015b3331568159b2c2` |
| SOURCE META FILE | `sha256:c37b7ae0ed24dd6510feef5c753f1dca8201b793e066628e1730b43ebf507caf` |
| PRICE FLOAT64 PAYLOAD | `sha256:bc0d68b080f1f42c56f01da43820c11425ca1fc3a80bfb0ca32647821c2488d1` |
| RETURNS FLOAT64 PAYLOAD | `sha256:bde9a3045659bcb6ffdde99c52d7b088662456ed5d42737662f7c8384091c02e` |
| RETURNS.NPY FILE | `sha256:4aee1aaea6886a727b5f322e51af9e2c05132b32aaaa47d0d5c0dc68c795943e` |
| MANIFEST GIT TRANSPORT FILE (canonical) | `sha256:9d285f24f031424aa016313195b25917e189f8aa6cb0e5960c18587cee0cbf8f` |
| MANIFEST PRODUCER WORKING-TREE CRLF (historical, **NON-CANONICAL**) | `sha256:4cf1e219a824f5a73739c8eaaa160a81e4caf92a5b0e6fba91a70c690f5c6901` |

## Gates

- SOURCE_IDENTITY: PASS  
- consumer validation (`require_authorized_spy=True`): PASS  
- BITWISE_IDENTITY (A–D direct vs loaded, including NaN bits): PASS  

Producer: CPython 3.12.10 / Windows AMD64 MSC v.1943 / NumPy 2.5.3 / pandas 3.0.6  

Contract: [I03-AMENDMENT-B-CANONICAL-INPUT.md](I03-AMENDMENT-B-CANONICAL-INPUT.md)

---

## Erratum — M2 manifest transport identity (M2R)

**Do not rewrite M1 history.** M1 materialization and numerical gates remain PASS.

During M2 Cloud validation, the consumer compared the **M1-reported**
manifest FILE hash against Git/Cloud bytes and stopped **fail-closed**
(correct behavior).

| Fact | Value |
|------|--------|
| Hash reported at M1 | `sha256:4cf1e219…c6901` |
| What it actually hashed | Windows **CRLF** working-tree bytes (`Path.write_text` / autocrlf) |
| Git blob / Cloud LF bytes | `sha256:9d285f24…bf8f` |
| Logical JSON | identical (LF↔CRLF only) |
| `returns.npy` FILE | **unchanged** `sha256:4aee1aae…5943e` |
| RETURNS FLOAT64 PAYLOAD | **unchanged** `sha256:bde9a304…1c02e` |
| Scientific / numerical impact | **NONE** |

Canonical transport identity for `manifest.json` is therefore the
**Git-committed LF** representation. The CRLF hash is retained only as
producer working-tree provenance and is **NON-CANONICAL FOR GIT TRANSPORT**.

Infrastructure correction: [I03-AMENDMENT-B-CANONICAL-INPUT.md](I03-AMENDMENT-B-CANONICAL-INPUT.md) §4 / M2R.
