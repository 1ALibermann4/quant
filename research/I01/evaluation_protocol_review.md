# I01 — Revue de cohérence du protocole

> **Identifier :** I01-REVIEW-v0.1
> **Status :** PENDING
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1

Revue à effectuer **avant** toute implémentation ou choix de source de données.

---

## Checklist

| # | Point | Verdict | Notes |
|---|-------|---------|-------|
| 1 | $X_t$ causal ($\leq t$ only) | PENDING | |
| 2 | $Y_t^{(h)}$ strictement futur ($> t$) | PENDING | |
| 3 | Embargo $\tau \geq W$ | PENDING | $\tau=20, W=20$ |
| 4 | B0 indépendant de $d$ | PENDING | |
| 5 | SCI-001 sur split test seul | PENDING | |
| 6 | Paramètres figés avant test | PENDING | configuration.yaml |
| 7 | $N_\min = 100$ atteignable avec §9 data req | PENDING | |
| 8 | Pas de fuite split train→test | PENDING | |
| 9 | Métrique primaire alignée H₁ | PENDING | $\mathcal{H}_\text{mpd}$ |
| 10 | Gates INCONCLUSIVE bien définies | PENDING | |
| 11 | Aucune API figée | PENDING | |
| 12 | FAIL = résultat valide documenté | PENDING | |

## Verdict global

**PENDING** — revue non effectuée.

## Prochaine action post-PASS

Produire `DATA-REQ-I01.md` à partir de [protocol.md §9](protocol.md).

---

**STOP implémentation** tant que verdict ≠ PASS.
