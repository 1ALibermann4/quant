# I02 — Formal closure

> **STATUS :** **CLOSED — EXPL-ABSENT**  
> **Disposition :** A — NEGATIVE EXPLORATORY RESULT  
> **Authority class :** RESEARCH  
> **Protocol :** QDP v0.1 · DR-007  
> **Preregistration :** [I02-PREREG-v0.3](I02-preregistration.md) (historical contract)  
> **Postmortem :** [I02-E01-POSTMORTEM.md](I02-E01-POSTMORTEM.md) @ `f581416`  
>
> ```text
> I02 = CLOSED
> FINAL STATUS = EXPL-ABSENT
> NOT SCI-FAIL
> NOT SCI-PASS
> NO SCI CLAIM
> NO NEW DATA / RUN / RETUNING
> I03 NOT OPENED
> ```

---

## 1. Investigation identity

| Field | Value |
|-------|-------|
| ID | **I02** |
| Title | Conditional geometric incremental predictive value vs volatility-regime instability |
| Parent | I01 exploratory CLOSE (regime-conditional lead; not proof of H1-I02) |
| Data class (E01) | EXPLORATORY / UNQUALIFIED (DR-007 / DR-008) |
| Software | not failed — HAT-PASS; L2-PASS |

---

## 2. Original question

**H1-I02 (preregistered):** under the frozen design, the comparator-relative
CRPS incremental value \(R_t^{(S)}\) of representation \(X\) vs
\(S\in\{S_1,S_2,S_3\}\) (S3 expanded to co-equal `S3_Q` / `S3_phi`)
exhibits a systematic **monotone** Spearman association with
volatility-regime instability \(Z_t^{(m)}\), \(m\in\{3,12,21\}\).

---

## 3. Frozen design (unchanged at closure)

Core **R2** + **I02-PREREG-v0.3**: \(W_X=W_{RV}=20\), \(M=252\), \(h=10\),
\(k=50\), \(\mathcal{M}_Z=\{3,12,21\}\), stride 1, CRPS / \(R=D/\mathrm{CRPS}_S\),
S3-A L2 product metrics (no primary), MBB \(B=9999\), seed 42,
\(b^\star=40\), robustness \(\{20,40,80\}\).

---

## 4. Execution history (lifecycle)

```text
DESIGN CLOSED (R2)
    →
IMPLEMENTATION C2
    →
L2-PASS
    →
HAT-PASS
    →
E01 EXPLORATORY / UNQUALIFIED
    →
EXPL-ABSENT
    →
POSTMORTEM (read-only)
    →
CLOSED
```

Documented interruptions / operational notes are preserved where already
recorded (e.g. HAT Unicode exit I1; first E01 run aborted then restarted
after operational speedups `8d70e97` — **before** scientific observation of
the successful E01). History is not rewritten to appear smoother.

---

## 5. E01 result

| Item | Outcome |
|------|---------|
| Verdict | **EXPL-ABSENT** |
| Detectability | **0/12** cells at \(b^\star=40\) (also 0/12 at \(b\in\{20,80\}\)) |
| MS | **MS-1** (coherent null across \(m\)) |
| S3 | `S3_Q` / `S3_phi` **agree** (null) |
| K1–K8 | **not triggered** |
| Queries | 8208 scheduled / 8149 evaluable / 59 skip |

No exploratory support for the preregistered broad monotone
\(Z\leftrightarrow R\) association on the DR-008 SPY path.

---

## 6. Postmortem conclusion

Read-only review (`f581416`):

- **H-A (weak):** no detectable monotone organization of \(R\) by \(Z\) —
  supported; “\(Z\) contains no information” **not** concluded.
- **H-B:** non-monotone dependence **not tested** — open possibility only.
- **H-C:** mean \(D<0\) vs **all four** comparator branches — supports
  absence of an **average** residual advantage of \(X\) in E01;
  “\(X\) never helps” **not** concluded.
- Disposition recommendation: **A** (close).

---

## 7. Final disposition

**I02 = CLOSED** because:

1. the preregistered exploratory question was successfully executed;
2. E01 produced **EXPL-ABSENT**;
3. no execution/design defect invalidated that interpretation;
4. postmortem found no pre-existing reason requiring continuation;
5. changing the question now would be a **new** investigation.

I02 is **not** closed due to a kill criterion, HAT failure, or broken
software.

**Final scientific status:** `EXPL-ABSENT` · **not** `SCI-FAIL` · **not** `SCI-PASS`.

---

## 8. What is NOT concluded

- “\(Z\) contains no information”
- “\(X\) never helps”
- “I02 is scientifically disproven”
- any SCI / PRED / ECON / promotional claim
- confirmatory status of any kind

---

## 9. Open questions (not I02 continuation)

Unresolved, **outside** I02:

- nonlinear dependence;
- episodic / event-localized structure;
- alternative causal state variables;
- detailed existence/structure of residual \(X\) advantage.

**CANDIDATE I03 QUESTION — UNDESIGNED**

> Does \(X\) exhibit residual predictive advantage over the adversarial
> controls in specific episodes/conditions even though no broad average
> advantage or monotone \(Z\) organization was observed in I02-E01?

I03 is **not opened**. No conditions, metrics, or runs are defined here.

---

## 10. Artifact / commit chain

| Milestone | Artifact / note | Commit (short) |
|-----------|-----------------|----------------|
| OPEN | formal open | `4f6be2a` |
| Design freeze | draft R2 | `260988b` |
| Prereg v0.2 gaps | X / MBB; S3 human | `4778842` |
| Prereg v0.3 + L1 patch | S3-A | `b5465b0` |
| L2 | [I02-L2-CONTRACT-TEST.md](I02-L2-CONTRACT-TEST.md) | `16cfee2` |
| HAT | [I02-HAT.md](I02-HAT.md) | `dedf3ff` |
| E01 PRE-RUN | [I02-E01.md](I02-E01.md) | `cd0d720` |
| Ops (pre-obs.) | speedups | `8d70e97` |
| E01 evidence | `e01/run1/` | `33d063d` |
| Postmortem | [I02-E01-POSTMORTEM.md](I02-E01-POSTMORTEM.md) | `f581416` |
| **Closure** | **this document** | *(this commit)* |

Immutability: scientific I02 artifacts are historical evidence. Material
scientific change ⇒ new investigation ID, not “I02-E02 tuning.”
