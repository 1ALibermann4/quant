# I01 — Revue de cohérence contradictoire du protocole (v0.2)

> **Identifier :** I01-REVIEW-v0.2
> **Status :** CLOSED
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Reviewer stance :** indépendant — réévaluation post-décisions
> **Documents examinés :** `hypothesis.md` v0.2, `protocol.md` v0.2, `configuration.yaml` v0.2, `review_decisions.md`
> **Précédent :** I01-REVIEW-v0.1 @ `d9481b5` → **INCONCLUSIVE**
> **Verdict revue :** **PASS**

---

## 0. Synthèse exécutive

Les décisions DEC-01…DEC-16 ont été appliquées au protocole v0.2. Les **2 BLOCKER**
(REV-07, REV-08) et la majorité des **MAJOR** sont **résolus ou mitigés** avec
documentation explicite.

Le protocole I01 v0.2 est **suffisamment spécifié** pour dériver `DATA-REQ-I01.md`.

**Limitations résiduelles** (non bloquantes) : chevauchement $Y$ inter-voisins (diagnostic),
crédibilité inférentielle modeste (~15 blocs bootstrap à 10 ans), adjusted_close non PIT
(report DATA-REQ).

**Aucun faux PASS forcé** : les chemins INCONCLUSIVE (profondeur $< 10$ ans, instabilité $L$,
effect size borderline) restent explicites.

---

## 1. Traçabilité décisions → protocole

| Décision | Appliqué dans | Vérifié |
|----------|---------------|---------|
| DEC-01 Bootstrap blocs | protocol §7.2, config `statistics.block_bootstrap` | ✓ |
| DEC-02 $s+h\leq t$ | hypothesis §4.5, protocol §3, config `hard_constraint` | ✓ |
| DEC-03 $H_\text{raw}$ + diagnostics | hypothesis §5, protocol §7.1 | ✓ |
| DEC-04 Clôture + $r_t$ inclus | hypothesis §3, config `temporal_convention` | ✓ |
| DEC-05 10 ans cible | protocol §7.3, §9.2, config `confirmatory_target_days` | ✓ |
| DEC-06…DEC-16 | protocol §3, §6, §8, §9, §11, §12 | ✓ |

---

## 2. Réexamen des 15 axes

### Axe 1 — $X_t$ et causalité

| Champ | v0.1 | v0.2 |
|-------|------|------|
| REV-01 | MAJOR | **RÉSOLU** — formule explicite $\hat{\mu}_t,\hat{\sigma}_t$ sur $[t-M+1,t]$ inclusif |
| REV-02 | MINOR | **RÉSOLU** — convention after_close_of_t |

**Constat résiduel (NOTE REV-01b)** : double usage de $r_t$ (dans stats et dans $X_t$) crée
couplage mécanique — **accepté** par décision humaine DEC-04.

---

### Axe 2 — $Y_t^{(h)}$

| Verdict | **RÉSOLU** |
|---------|------------|
| $Y$ commence $t+1$ | Explicite §3 DEC-04 |
| Fenêtres complètes | $\mathcal{T}_\text{eval}$ formalisé |
| $Y$ hors sélection | AF-08 |

---

### Axe 3 — $\mathcal{L}_t$ et embargo

| Constats | Sévérité v0.2 |
|----------|---------------|
| REV-07 $s+h\leq t$ | **RÉSOLU** — hard constraint + invariant impl |
| REV-05 texte overlap $X$ | **RÉSOLU** — $t-s\geq 21$ ⇒ zéro rendement commun |
| REV-06 overlap $Y$ inter-voisins | **MITIGÉ** — SCI-DIAG-1 obligatoire ; contrainte $|i-j|\geq h$ reportée |

**ID REV-06r** | NOTE | Chevauchement $Y_i,Y_j$ dans $\mathcal{H}_\text{raw}$ persiste | Interprétation geo peut être partiellement driven par overlap calendaire | Accepté v0.1 ; diagnostic suffit | **ACCEPTÉ**

---

### Axe 4 — Dépendance temporelle / inférence

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-08 t-test iid | Interdit ; block bootstrap confirmatoire |
| REV-09 permutation vague | Remplacé par bootstrap spécifié (§7.2) |

**Constat résiduel (MAJOR atténué → NOTE REV-08b)** :

| Champ | Contenu |
|-------|---------|
| Problème | ~15 blocs effectifs à 10 ans / $L=30$ — puissance limitée |
| Conséquence | PASS difficile ; INCONCLUSIVE fréquent — **conservateur** |
| Décision | **ACCEPTÉ** — DEC-05 pousse vers 15–20 ans ; INCONCLUSIVE si profondeur insuffisante |

Sensibilité $L$ avec verdict INCONCLUSIVE si instable — **empêche cherry-picking** ✓

---

### Axe 5 — Baseline B0

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-10 | $L_\min=150$ ; SCI-DIAG-1 compare dispersion temporelle geo vs B0 |

B0 stratifié vol : reporté I01-bis — **NOTE**.

---

### Axe 6 — $\mathcal{H}_\text{mpd}$ / vol / forme

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-11 | $H_\text{raw}$ endpoint ; $H_\text{vol}$, $H_\text{shape}$ diagnostics obligatoires ; tableau lecture croisée |

Cherry-picking interdit normativement (DEC-03, DEC-13).

---

### Axe 7 — $\Delta_t$

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-12 | Signe $\Delta = \bar{\mathcal{H}}_\text{B0} - \mathcal{H}_\text{geo}$ ; terme « paired t-test » supprimé |

---

### Axe 8 — Splits

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-13 | Train descriptif only ; SCI-001 test seul ; SCI-003 validation |

---

### Axe 9 — Multiplicité

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-14 | `gate_roles` : primary / confirmatory / diagnostic |

SCI-002 sur même split test que SCI-001 — corrélation confirmatoire acceptée (NOTE).

---

### Axe 10 — Taille effective

| Profondeur | Test brut (~20%) | Blocs ~ ($L=30$) | Crédibilité |
|------------|------------------|------------------|-------------|
| 1 500 j | ~244 | ~8 | **Insuffisant** → INCONCLUSIVE auto si $< 10$ ans |
| 2 520 j | ~448 | ~15 | **Minimum cible** |
| 3 780 j | ~670 | ~22 | Préféré |

DEC-05 aligné avec gate SCI-001 (10 ans requis pour PASS confirmatoire).

---

### Axe 11 — Non-stationnarité

| Verdict | **DOCUMENTÉ** (DEC-16) |
|---------|------------------------|
| REV-16 | Portée SCI PASS limitée ; pas preuve stationnarité |

---

### Axe 12 — adjusted_close

| Verdict | **MITIGÉ** |
|---------|------------|
| REV-17 | C02 metadata requis §9.3 ; PIT → DATA-REQ |

Suffisant pour **spécifier** exigences fournisseur ; pas pour exécuter.

---

### Axe 13 — Falsifiabilité

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-18 | §12 protocol ; protocole versionné avant snapshot |

---

### Axe 14 — Reproductibilité

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-19 | §11 protocol ; seeds, tri, tolérance |

Test reproductibilité impl : report P1 pipeline.

---

### Axe 15 — Portée SCI PASS

| Verdict | **RÉSOLU** |
|---------|------------|
| REV-20 | hypothesis §8 ; protocol §8 — texte strict |

---

## 3. Registre v0.2 — constats résiduels

| ID | Sévérité | Problème | Décision |
|----|----------|----------|----------|
| REV-01b | NOTE | Couplage $r_t$ dans $\mu,\sigma$ et $X_t$ | ACCEPTÉ (DEC-04) |
| REV-06r | NOTE | Overlap $Y$ intra-voisinage | Diagnostic SCI-DIAG-1 |
| REV-08b | NOTE | ~15 blocs à 10 ans — puissance modeste | INCONCLUSIVE path ; 15–20 ans préféré |
| REV-17r | NOTE | Pas de PIT prices | DATA-REQ-I01 |
| REV-14b | NOTE | SCI-002 non indépendant de SCI-001 | Accepté confirmatoire |

**Aucun BLOCKER ouvert.**

---

## 4. Comparaison verdicts v0.1 → v0.2

| Métrique | v0.1 | v0.2 |
|----------|------|------|
| BLOCKER ouverts | 2 | **0** |
| MAJOR ouverts | 9 | **0** (5 résolus, 4 mitigés/documentés) |
| Prêt DATA-REQ | Non | **Oui** |
| Prêt impl | Non | **Non** — DATA-REQ puis ADR data d'abord |

---

## 5. Verdict de la revue v0.2

### **PASS**

| Critère | Évaluation |
|---------|------------|
| BLOCKERs résolus | Oui |
| Inférence défendable | Block bootstrap + sensibilité $L$ |
| Anti-fuite | $s+h\leq t$ invariant |
| Endpoint / diagnostics | Séparés, non substituables |
| Falsifiabilité | Oui |
| Profondeur data | Spécifiée (10 ans cible) |
| Prêt pour `DATA-REQ-I01.md` | **Oui** |

**PASS** signifie uniquement : *le protocole est suffisamment bien spécifié pour dériver
les exigences de données et, ensuite, l'implémentation.*

**PASS ne signifie pas** : que I01 réussira scientifiquement, ni qu'une API est choisie.

---

## 6. Prochaine étape autorisée

```text
1. DATA-REQ-I01.md  ← autorisé
2. ADR source de données (si applicable)
3. Implémentation pipeline I01
4. Exécution + evaluation_closure.md
```

---

## 7. Checklist finale (v0.2)

| # | Point | Verdict |
|---|-------|---------|
| 1 | $X_t$ causal, $r_t$ inclus explicite | PASS |
| 2 | $Y_t$ strictement futur | PASS |
| 3 | $\mathcal{L}_t$ + $s+h\leq t$ + embargo | PASS |
| 4 | Inférence temporelle | PASS |
| 5 | B0 équitable + $L_\min$ | PASS |
| 6 | $H_\text{raw}$ / vol / shape | PASS |
| 7 | $\Delta_t$ signe cohérent | PASS |
| 8 | Splits verrouillés | PASS |
| 9 | Multiplicité / rôles gates | PASS |
| 10 | Taille effective + 10 ans | PASS |
| 11 | Non-stationnarité documentée | PASS |
| 12 | adjusted_close C02 | PASS (mitigé) |
| 13 | Falsifiabilité | PASS |
| 14 | Reproductibilité spec | PASS |
| 15 | Portée SCI PASS | PASS |

---

**STOP re-review I01** — pas de DATA-REQ dans cette intervention (instruction respectée).
