# I01 — Protocole expérimental

> **Identifier :** I01-PROTO-v0.1
> **Status :** OPEN
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1

Protocole opérationnel dérivé de [hypothesis.md](hypothesis.md).
**Aucune implémentation** tant que ce document n'a pas passé la revue de cohérence.

---

## 1. Population expérimentale

### 1.1 Instrument (v0.1)

| Attribut | Spécification |
|----------|---------------|
| Classe | ETF large-cap US, très liquide |
| Exemple indicatif | SPY (non figé comme ticker — **classe d'instrument**) |
| Justification | Liquidité, historique long, corporate actions documentées |
| Nombre d'actifs | **1** (univarié strict) |

Multi-actif, cross-section, secteurs : **I02+**.

### 1.2 Granularité

| Attribut | Valeur |
|----------|--------|
| Barre | **Daily** (clôture ajustée) |
| Fuseau | Heure de clôture marché US, documenté dans C02 |
| Minimum historique | Voir §9 |

### 1.3 Points d'évaluation $\mathcal{T}_\text{eval}$

Dates $t$ éligibles telles que :

- $X_t$ calculable (historique suffisant pour $W$ et $M$)
- $Y_t^{(h)}$ observable (h jours futurs dans l'échantillon)
- $|\mathcal{L}_t| \geq k + \text{marge}$

---

## 2. Construction de $X_t$ (rappel opérationnel)

Voir [hypothesis.md §3.2](hypothesis.md).

**Checklist causalité :**

- [ ] $P_\tau$ = prix ajusté corporate actions, connu à $t$ pour $\tau \leq t$
- [ ] $\hat{\mu}_t, \hat{\sigma}_t$ utilisent uniquement $r_{\max(t_0,t-M+1)}, \ldots, r_t$
- [ ] Aucun paramètre de $\phi$ estimé sur données $> t$

---

## 3. Bibliothèque historique $\mathcal{L}_t$

$$
\mathcal{L}_t = \{ s \in \mathcal{T} : s < t,\ s \notin \mathcal{E}_t,\ X_s \text{ valide} \}
$$

### Embargo temporel $\mathcal{E}_t$

Exclure du voisinage les dates trop proches de $t$ (autocorrélation / chevauchement de fenêtres) :

$$
\mathcal{E}_t = \{ s : |s - t| \leq \tau \}
$$

| Paramètre | Symbole | Valeur |
|-----------|---------|--------|
| Embargo | $\tau$ | $W$ (= 20 jours) |

**Règle :** $\tau \geq W$ garantit qu'aucune fenêtre $X_s$ et $X_t$ ne partagent
plus d'un rendement commun.

---

## 4. Voisinage géométrique $N_k^{\text{geo}}(X_t)$

1. Calculer $d(X_t, X_s)$ pour tout $s \in \mathcal{L}_t$
2. Sélectionner les $k$ plus petites distances (ties : date la plus ancienne gagne)
3. Enregistrer distances, dates voisins, empreinte tri

**Sortie structurée (C01 artefact) :**

```yaml
neighbor_set:
  method: geometric_l2
  k: 50
  dates: [...]
  distances: [...]
```

---

## 5. Baseline B0 — $N_k^{\text{B0}}(X_t)$

Pour chaque $t \in \mathcal{T}_\text{eval}$ :

1. Tirer uniformément $k$ dates dans $\mathcal{L}_t$ (sans remplacement)
2. Répéter $R$ fois (seed documentée)
3. Calculer $\bar{\mathcal{H}}_\text{B0}(t) = \frac{1}{R}\sum_{r=1}^R \mathcal{H}_\text{mpd}(N_{k,r}^{\text{B0}}(X_t))$

| Paramètre | Valeur |
|-----------|--------|
| Répétitions MC | $R = 200$ |
| Seed | Figée dans configuration.yaml |

B0 **ne regarde pas** $d$ — contrôle négatif strict.

---

## 6. Contrôles anti-fuite

| ID | Risque | Contrôle |
|----|--------|----------|
| AF-01 | Look-ahead dans $X_t$ | $X_t = \phi(\mathcal{O}_{\leq t})$ uniquement |
| AF-02 | Look-ahead dans voisinage | $s < t$ strict ; embargo $\tau$ |
| AF-03 | Look-ahead dans $Y$ | $Y_t^{(h)}$ utilise $t+1 \ldots t+h$ seulement |
| AF-04 | Fuite train→test | Splits temporels stricts (§7) |
| AF-05 | Optimisation implicite | $(W,k,h,M)$ **figés** avant exécution ; sensibilité = diagnostic, pas sélection |
| AF-06 | Survitance | Documenter dans C02.provenance |
| AF-07 | Réutilisation voisins futurs | $\mathcal{L}_t$ tronquée au split courant |

**Split temporel obligatoire :**

| Split | Usage | Fraction indicative |
|-------|-------|---------------------|
| **Train** | Diagnostic, calibration empirique des seuils INCONCLUSIVE | 60 % |
| **Validation** | Sensibilité $(W, k, h)$ — **sans** modifier paramètres figés | 20 % |
| **Test** | **Gate SCI primaire** — une seule passe | 20 % |

Les dates exactes seront figées dans `configuration.yaml` une fois le DatasetSnapshot connu.
Les paramètres $(W, k, h)$ ne sont **jamais** choisis en fonction du test.

---

## 7. Tests statistiques

### 7.1 Statistique par date

$$
\Delta_t = \bar{\mathcal{H}}_\text{B0}(t) - \mathcal{H}_\text{mpd}(N_k^{\text{geo}}(X_t))
$$

### 7.2 Agrégation

Sur $\mathcal{T}_\text{eval}$ du split concerné :

| Statistique | Formule |
|-------------|---------|
| Moyenne | $\bar{\Delta} = \frac{1}{|\mathcal{T}_\text{eval}|}\sum_t \Delta_t$ |
| Fraction positive | $f_+ = \frac{|\{t : \Delta_t > 0\}|}{|\mathcal{T}_\text{eval}|}$ |
| Médiane | $\text{med}(\Delta_t)$ |

### 7.3 Test primaire (SCI-001)

**Test t apparié sur $\Delta_t$** (sur split **test** uniquement) :

$$
H_0': \mathbb{E}[\Delta_t] = 0 \quad \text{vs} \quad H_1': \mathbb{E}[\Delta_t] > 0
$$

- Niveau : $\alpha = 0.05$
- Alternative unilatérale (homogénéité géométrique > B0)

**Test de permutation** (robustesse, split test) :

- Ré-alléer aléatoirement labels geo/B0 au niveau des paires de voisinages
- $N_\text{perm} = 1000$ permutations, seed figée
- p-value empirique ; doit concorder directionnellement avec t-test

### 7.4 Tests auxiliaires

| ID | Objet | Méthode |
|----|-------|---------|
| SCI-AUX-1 | $\mathcal{H}_\text{var}$ (rendement cumulé) | Même structure $\Delta_t$ |
| SCI-AUX-2 | $\mathcal{H}_\text{iqr}$ | Même structure |
| SCI-AUX-3 | Corrélation distance-futur | Spearman entre $d(X_t,X_s)$ et $D(Y_t,Y_s)$ sur paires — **exploratoire** |

---

## 8. Gates SCI — PASS / FAIL / INCONCLUSIVE

Évaluées sur le split **test** sauf mention.

### SCI-000 — Baseline présente

| Verdict | Condition |
|---------|-----------|
| PASS | B0 exécutée avec $R$ répétitions, seed documentée |
| FAIL | B0 absente |

### SCI-001 — Homogénéité primaire (gate bloquante)

| Verdict | Condition |
|---------|-----------|
| **PASS** | $\bar{\Delta}_\text{test} > 0$ **ET** p-value t-test $< 0.05$ **ET** p-value permutation $< 0.05$ |
| **FAIL** | $\bar{\Delta}_\text{test} \leq 0$ **OU** les deux p-values $\geq 0.05$ |
| **INCONCLUSIVE** | Effet positif mais un seul test significatif ; ou $|\mathcal{T}_\text{eval,test}| < N_\min$ |

$N_\min = 100$ points d'évaluation test — en dessous → INCONCLUSIVE automatique.

### SCI-002 — Non-concentration temporelle

Partitionner $\mathcal{T}_\text{eval,test}$ en 3 tertiles temporels.

| Verdict | Condition |
|---------|-----------|
| PASS | $\bar{\Delta} > 0$ dans **≥ 2/3** tertiles |
| FAIL | $\bar{\Delta} \leq 0$ dans ≥ 2/3 tertiles |
| INCONCLUSIVE | Mixte |

### SCI-003 — Sensibilité paramétrique (validation split)

Varier **un paramètre à la fois** autour de la valeur figée :

| Paramètre | Grille |
|-----------|--------|
| $W$ | {10, 20, 40} |
| $k$ | {25, 50, 100} |
| $h$ | {5, 10, 20} |

| Verdict | Condition |
|---------|-----------|
| PASS | Signe de $\bar{\Delta}$ **cohérent** (≥ 5/9 configurations) |
| FAIL | Signe inversé dans ≥ 7/9 configurations |
| INCONCLUSIVE | Mixte |

**Important :** la grille de sensibilité **ne modifie pas** le verdict SCI-001 (paramètres figés sur test).

### SCI-004 — Anti-fuite

| Verdict | Condition |
|---------|-----------|
| PASS | Tous contrôles AF-01…AF-07 vérifiés et logués |
| FAIL | Toute violation détectée |
| INCONCLUSIVE | Audit incomplet |

### Verdict global I01

| SCI-001 | SCI-002 | SCI-004 | Global |
|---------|---------|---------|--------|
| PASS | PASS | PASS | **PASS** → H₀ rejetée, promotion scientifique I01 |
| FAIL | * | PASS | **FAIL** → proximité L2 non informative |
| INCONCLUSIVE | * | PASS | **INCONCLUSIVE** |
| * | * | FAIL | **FAIL** (invalidation protocole) |

**Promotion opérationnelle :** **NOT_APPLICABLE** — gate ECON non concernée.

---

## 9. Besoins data minimaux (API-agnostique)

Spécification dérivée **du protocole**, pas d'une API.

### 9.1 Champs requis par observation

| Champ | Requis | Notes |
|-------|--------|-------|
| `timestamp` | Oui | Date de clôture, UTC ou TZ documenté |
| `adjusted_close` | Oui | Prix ajusté splits/dividendes |
| `volume` | Non (I01) | Futur contrôle liquidité |
| `open/high/low` | Non (I01) | |

### 9.2 Profondeur historique

$$
T_\min \geq M + W + \tau + h + T_\text{eval,train} + T_\text{eval,val} + T_\text{eval,test} + k
$$

Avec valeurs figées :

| Composant | Jours |
|-----------|-------|
| $M$ | 252 |
| $W + \tau$ | 40 |
| $h$ | 10 |
| Évaluations (estim.) | 500+ |
| Marge | 252 |
| **Total indicatif** | **≥ 1 500 jours de bourse (~6 ans)** |

Recommandé : **≥ 10 ans** pour robustesse SCI-002 et sensibilité.

### 9.3 Qualité

- Corporate actions appliquées (adjusted close)
- Pas de trous non documentés > 3 sessions consécutives
- Survivorship : N/A (un seul ETF)
- `availability_cutoff` C02 = date de figement du snapshot

### 9.4 Livrable suivant (post-revue)

Document **`research/I01/DATA-REQ-I01.md`** à produire après revue de ce protocole,
traduisant §9 en checklist d'acceptation pour toute source candidate.

**Aucune API ne sera choisie avant DATA-REQ-I01.**

---

## 10. Artefacts C01 attendus

| Artefact | Contenu |
|----------|---------|
| `metrics.json` | $\bar{\Delta}$, p-values, $f_+$, par split |
| `gate_results.json` | SCI-000…004 |
| `config.yaml` | Copie configuration.yaml + snapshot ref |
| `neighbor_samples.jsonl` | Échantillon de voisinages (10 dates test) |
| `sensitivity.json` | Grille SCI-003 |

---

## 11. Revue de cohérence (à faire)

Checklist avant implémentation :

- [ ] $X_t$ et $Y_t^{(h)}$ disjoints temporellement
- [ ] Embargo $\tau \geq W$
- [ ] B0 indépendant de $d$
- [ ] SCI-001 évalué sur test seul
- [ ] Paramètres figés avant accès au test
- [ ] Besoins data §9 suffisants pour $N_\min$
- [ ] Pas de décision API prématurée

Documenter dans `research/I01/evaluation_protocol_review.md` (à créer).

---

## Références

- [hypothesis.md](hypothesis.md)
- [configuration.yaml](configuration.yaml)
- [C01 Experiment](../../specs/contracts/C01/C01_v1.0.yaml)
- [C02 DatasetSnapshot](../../specs/contracts/C02/C02_v1.0.yaml)
