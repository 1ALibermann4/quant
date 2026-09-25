# I03 — Implementation Contract v0.1

> **STATUS :** EXECUTABLE IMPLEMENTATION CONTRACT  
> **Prereg authority :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a`  
> **Code package :** `src/quant/i03/`  
>
> ```text
> NO MARKET DATA
> NO EXPERIMENT
> NO PREREG RETUNING
> N4 PRESERVES sigma_hat PATH BY CONSTRUCTION
>   (NOT recalculated rolling vol on r*)
> ```

---

## 1. Traceability matrix

| Prereg clause | Mathematical contract | Component | Test obligation |
|---------------|----------------------|-----------|-----------------|
| G0 / \(W_X{=}20\) / \(M{=}252\) | Causal μ/σ, no ε, skip σ=0 | `g0.py` (reuse `quant.i02.states_x`) | A, future-suffix |
| Causal indexing | Window `[t-M+1,t]`; returns index `0` unused (I02 convention) | `g0.py` | A, off-by-one |
| \(\tau{=}20\) | \(\lvert t-s\rvert\ge 20\) | `emnd.py` / `pool.py` | B |
| \(P{=}3\) blocks + remainder→\(B_3\) | Contiguous equal + append | `blocks.py` | C |
| Intra-block pool | \(s\in B_p\) and τ | `pool.py` | C, block leak |
| \(\mathcal{K}{=}\{10,25,50\}\) | All scales reported | `params.py`, `emnd.py` | Q |
| E-MND \(\delta_k\), \(\Theta_k^{(p)}\) | \(k\)-th distance mean | `emnd.py` | D,E,F,G |
| Ties | \((\mathrm{dist}\uparrow,s\uparrow)\) | `emnd.py` | E |
| Insufficient pool | Exclude from \(\mathcal{T}_p\) if \(\lvert A\rvert<50\) | `emnd.py` | F |
| \(n_{\min}{=}250\) | \(E\) fails if any \(\lvert\mathcal{T}_p\rvert<250\) | `pipeline.py` / `verdict.py` | sample gate |
| N4 \(W_\sigma{=}20\) sample stdev /19 | Inclusive causal; ≠ RMS RV | `n4.py` | H,I |
| N4 \(z\), shuffle \(\mathcal{Z}\), \(r^*=\sigma z^*\) | Preserve \(\sigma\) path | `n4.py` | J,K,L + N4 note |
| N4 seeds `42+b` | `b=1..B` | `n4.py` | N |
| N4 validity \(\lvert Z\rvert/T\), var | Exact thresholds | `n4.py` | L |
| N3 IAAFT | Approx spectrum+marginal | `iaaft.py`, `n3.py` | M |
| N3 seeds `10000+b`, \(I_{\max}\), ε | Per-surrogate flags | `n3.py` | M,N |
| \(B{=}999\), \(\alpha{=}0.05\), left tail | Finite-surrogate p | `inference.py` | O,P |
| \(p\le\alpha\) survives | Closed equality | `inference.py` | P |
| Locality \(\Lambda,\Gamma\) | Validity only | `locality.py` | W |
| Coherence / ND / verdict | Truth table | `verdict.py` | Q–V,Y |
| Artifact | Schema fields | `artifact.py` | X semantic |
| Diagnostics whitelist | Non-promotional | `types.py` labels | Y |

---

## 2. Domain model

Canonical config: `I03Config` / `DEFAULT_CONFIG` in `params.py` — **single source** of scientific constants.

Types (immutable dataclasses / enums): `TemporalBlock`, `EMNDResult`, `LocalityDiagnostic`, `SurrogateBatteryMeta`, `NullCellResult`, `I03Evidence`, `I03Verdict`, `I03Artifact`.

---

## 3. G0 reuse decision

**Reuse** `quant.i02.states_x.causal_mu_sigma` and `state_vector_x` / `all_state_vectors_x`.

Compatibility check vs I03-PREREG §3:

| Requirement | I02 `states_x` | Match? |
|-------------|----------------|--------|
| \(M{=}252\), \(W_X{=}20\) | yes | yes |
| Sample stdev `ddof=1` | yes | yes |
| No \(\varepsilon\) | yes | yes |
| \(\sigma=0\) → undefined | yes | yes |
| Indexing `start>=1` (slot 0 unused) | yes | **adopted as I03 indexing convention** |

If a future change breaks this, classify **L1-I5** and STOP.

---

## 4. N4 preservation semantics (critical)

N4 **preserves by construction** the path \(\{\hat\sigma_t^{\mathrm{N4}}(r^{\mathrm{obs}})\}\) computed once on the **observed** returns, then used to rebuild \(r^*=\hat\sigma^{\mathrm{obs}}\odot z^*\).

N4 does **not** claim that recomputing sample stdev on \(r^*\) yields the same path. Documentation and tests must state this explicitly (L2 attack surface).

---

## 5. Production vs test batteries

`I03Config` freezes \(B_{\mathrm{N4}}=B_{\mathrm{N3}}=999\).

Low-level battery builders accept an optional `B` **only for synthetic unit tests**. The production entrypoint `run_structural_analysis` **must not** expose a public override; tests call builders directly.

---

## 6. Issue classification (active)

See L1 report for any I1–I6 findings.
