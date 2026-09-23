# I01 — Protocole expérimental

> **Identifier :** I01-PROTO-v0.2
> **Status :** ACCEPTED
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Decisions :** [review_decisions.md](review_decisions.md)

Protocole v0.2 — post revue contradictoire v0.1 (`d9481b5`).

---

## 1. Population expérimentale

### 1.1 Instrument

| Attribut | Spécification |
|----------|---------------|
| Classe | ETF large-cap US, très liquide |
| Exemple indicatif | SPY (non contractuel) |
| Nombre d'actifs | 1 (univarié) |

### 1.2 Granularité et convention temporelle (DEC-04)

| Attribut | Valeur |
|----------|--------|
| Barre | Daily, clôture ajustée |
| Observation | **Après clôture** de $t$ ; $r_t$ connu |
| Futur $Y_t$ | Commence à $t+1$ strictement |

### 1.3 Points d'évaluation $\mathcal{T}_\text{eval}$

$$
\mathcal{T}_\text{eval} = \{ t : X_t \text{ valide},\ Y_t^{(h)} \text{ complet},\ |\mathcal{L}_t| \geq L_\min \}
$$

$L_\min = 3k = 150$ (DEC-07).

---

## 2. Construction de $X_t$

Voir [hypothesis.md §4.2](hypothesis.md).

$$
\hat{\mu}_t, \hat{\sigma}_t \text{ sur } [t-M+1, t] \text{ inclusif — } r_t \text{ inclus}
$$

Checklist causalité :

- [ ] $P_\tau$ adjusted close connu à $t$ pour $\tau \leq t$
- [ ] Aucune donnée $> t$ dans $X_t$

---

## 3. Bibliothèque $\mathcal{L}_t$ (DEC-02)

$$
\mathcal{L}_t = \{ s \in \mathcal{T} :
  s < t,\ s \notin \mathcal{E}_t,\ \mathbf{s + h \leq t},\ X_s \text{ valide},\ Y_s^{(h)} \text{ valide} \}
$$

$$
\mathcal{E}_t = \{ s : |s - t| \leq \tau \}, \quad \tau = 20
$$

### Invariant anti-look-ahead (hard)

```text
∀ s ∈ L_t :  s + h ≤ t
```

Implémentation future — invariant testable :

```text
candidate.future_end <= query.information_cutoff
```

### Chevauchement fenêtres $X$

Pour $s \in \mathcal{L}_t$ : $t - s \geq \tau + 1 = 21 > W - 1$ ⇒ **zéro** rendement
commun entre fenêtres $X_t$ et $X_s$ (DEC-10).

### Chevauchement $Y$ inter-voisins (DEC-06)

Non contraint en v0.1. **Diagnostic obligatoire** SCI-DIAG-1 :
distribution de $|i-j|$ pour $i,j \in N^\text{geo}$ vs $N^\text{B0}$ (moyenne pairwise distance temporelle).

---

## 4. Voisinage géométrique

1. Calculer $d(X_t, X_s)$ pour $s \in \mathcal{L}_t$
2. Sélectionner $k=50$ plus petites distances (ties : date la plus ancienne)
3. **AF-08** : sélection fonction de $X$ uniquement — $Y$ n'intervient pas

---

## 5. Baseline B0

Pour chaque $t$ :

1. Tirer $k$ dates uniformément dans $\mathcal{L}_t$ (sans remplacement)
2. Répéter $R=200$ (seed 42)
3. $\bar{\mathcal{H}}_\text{B0,raw}(t) = \frac{1}{R}\sum_r \mathcal{H}_\text{raw}(N_{k,r}^{B0})$

B0 ne regarde pas $d$. Même $\mathcal{L}_t$, même $k$, mêmes contraintes causales.

---

## 6. Contrôles anti-fuite

| ID | Risque | Contrôle |
|----|--------|----------|
| AF-01 | Look-ahead $X_t$ | $\mathcal{O}_{\leq t}$ seulement |
| AF-02 | Look-ahead voisinage | $s < t$ ; embargo $\tau$ ; **$s+h \leq t$** |
| AF-03 | Look-ahead $Y$ | $Y_t$ utilise $t+1 \ldots t+h$ |
| AF-04 | Fuite train→test | Splits chronologiques ; test **une passe** |
| AF-05 | Optimisation implicite | $(W,k,h,M,L)$ figés ; sensibilité = diagnostic |
| AF-06 | Survivorship | N/A (1 ETF) ; documenter C02 |
| AF-07 | $\mathcal{L}_t$ causale | $s < t$ ; pas de dates futures |
| AF-08 | $Y$ dans sélection | Voisinage = $f(X)$ uniquement |

### Splits temporels (DEC-08)

| Split | Fraction | Usage |
|-------|----------|-------|
| Train | 60 % | **Descriptif uniquement** — interdit modifier gates/métriques/seuils |
| Validation | 20 % | Sensibilité $(W,k,h,L)$ — diagnostic |
| Test | 20 % | **Gate SCI-001** confirmatoire — une passe |

Dates figées dans `configuration.yaml` lors du DatasetSnapshot (C02).

---

## 7. Métriques et statistiques

### 7.1 Par date $t$

| Métrique | Formule | Rôle |
|----------|---------|------|
| $\Delta_t^\text{raw}$ | $\bar{\mathcal{H}}_\text{B0,raw}(t) - \mathcal{H}_\text{raw}(N^\text{geo})$ | **Endpoint SCI-001** |
| $\Delta_t^\text{vol}$ | idem avec $\mathcal{H}_\text{vol}$ | Diagnostic obligatoire |
| $\Delta_t^\text{shape}$ | idem avec $\mathcal{H}_\text{shape}$ | Diagnostic obligatoire |

**Signe** : $\Delta > 0$ ⇔ geo **plus homogène** que B0.

### 7.2 Inférence SCI-001 — block bootstrap (DEC-01)

**Interdit** : t-test iid, test apparié mal spécifié, choix de $L$ selon p-value.

**Méthode confirmatoire** : moving block bootstrap sur $\{\Delta_t^\text{raw}\}_{t \in \mathcal{T}_\text{eval,test}}$.

Paramètres :

| Param | Valeur |
|-------|--------|
| $L_\min$ | $\max(W,h) = 20$ |
| $L_\text{default}$ | 30 (première passe — **non optimisé**) |
| Grille sensibilité $L$ | $\{20, 30, 40, 60\}$ |
| $N_\text{boot}$ | 5000 |
| Seed | 456 |

Procédure :

1. Partitionner $\mathcal{T}_\text{eval,test}$ en blocs contigus de longueur $L$
2. Rééchantillonner blocs avec remplacement jusqu'à longueur originale
3. Calculer $\bar{\Delta}_\text{raw}^*$ sur échantillon bootstrap
4. Répéter $N_\text{boot}$ ; p-value unilatérale : fraction $\bar{\Delta}_\text{raw}^* \leq 0$

**Sensibilité $L$ (validation split)** :

- Répéter bootstrap pour chaque $L \in \{20,30,40,60\}$
- Si signe de p-value $<0.05$ **change** entre $L$ raisonnables → SCI-001 **INCONCLUSIVE**
- **Jamais** sélectionner $L$ minimisant p-value

### 7.3 Taille effective (DEC-05)

| Profondeur | Rôle |
|------------|------|
| ~1 500 séances | Minimum **technique** (pipeline exécutable) |
| **≥ 2 520 (~10 ans)** | Exigence **cible** inférence confirmatoire |
| 3 780–5 040 (15–20 ans) | Préféré si disponible sans changement méthodologique |

Estimation blocs test ($\approx \text{test}/L$) : ~8 blocs à 6 ans / $L=30$ — **insuffisant**
pour inférence confirmatoire ; 10 ans → ~15 blocs — **minimum crédible**.

Si confirmatoire sur $< 10$ ans : SCI-001 → **INCONCLUSIVE** automatique (profondeur).

### 7.4 Diagnostics obligatoires (non gates)

| ID | Contenu |
|----|---------|
| SCI-DIAG-1 | Distribution $|i-j|$ voisins geo vs B0 |
| SCI-DIAG-2 | $\bar{\Delta}^\text{vol}$, $\bar{\Delta}^\text{shape}$ sur test (signe + magnitude) |
| SCI-DIAG-3 | Tableau lecture croisée raw/vol/shape |

Cherry-picking interdit (DEC-03, DEC-13).

---

## 8. Gates SCI

### Rôles (DEC-09)

| Type | Gates |
|------|-------|
| **Primaire** | SCI-001 |
| **Confirmatoire** | SCI-002, SCI-004 |
| **Diagnostique** | SCI-003, SCI-DIAG-*, SCI-AUX-* |

Un FAIL SCI-001 **ne peut pas** être contourné par un diagnostic positif.

### SCI-000 — Baseline

| Verdict | Condition |
|---------|-----------|
| PASS | B0 exécutée, $R=200$, seed documentée |
| FAIL | B0 absente |

### SCI-001 — Homogénéité L2 brute (bloquante)

Sur split **test**, $\Delta^\text{raw}$ :

| Verdict | Condition |
|---------|-----------|
| **PASS** | $\bar{\Delta}_\text{raw,test} > 0$ **ET** p-value block bootstrap ($L=30$) $< 0.05$ **ET** sensibilité $L$ stable (§7.2) **ET** profondeur $\geq 10$ ans |
| **FAIL** | $\bar{\Delta}_\text{raw,test} \leq 0$ **OU** p-value $\geq 0.05$ |
| **INCONCLUSIVE** | Effet positif mais sensibilité $L$ instable ; ou profondeur $< 10$ ans ; ou $|\mathcal{T}_\text{eval,test}| < 60$ |

### SCI-002 — Non-concentration temporelle

Tertiles temporels du test ; $\bar{\Delta}^\text{raw} > 0$ dans ≥ 2/3.

| Verdict | Condition |
|---------|-----------|
| PASS | ≥ 2/3 tertiles positifs |
| FAIL | ≤ 1/3 positifs |
| INCONCLUSIVE | Mixte |

### SCI-003 — Sensibilité $(W,k,h)$ (validation, diagnostique)

Grille 9 configs ; ≥ 5/9 signe cohérent avec $\bar{\Delta}^\text{raw}$ — **n'affecte pas** verdict global.

### SCI-004 — Anti-fuite

| Verdict | Condition |
|---------|-----------|
| PASS | AF-01…AF-08 vérifiés ; invariant $s+h\leq t$ testé |
| FAIL | Violation |

### Verdict global I01

| SCI-001 | SCI-002 | SCI-004 | Global |
|---------|---------|---------|--------|
| PASS | PASS | PASS | **PASS** |
| FAIL | * | PASS | **FAIL** |
| INCONCLUSIVE | * | PASS | **INCONCLUSIVE** |
| * | * | FAIL | **FAIL** |

**Promotion opérationnelle** : NOT_APPLICABLE.

### Portée SCI PASS (DEC-12)

Voir [hypothesis.md §8](hypothesis.md). Aucune inférence PRED/ECON/trading.

---

## 9. Besoins data (API-agnostique, DEC-05)

### 9.1 Champs

| Champ | Requis |
|-------|--------|
| `timestamp` | Oui — clôture, TZ documenté |
| `adjusted_close` | Oui |

### 9.2 Profondeur

| Niveau | Jours | Usage |
|--------|-------|-------|
| Minimum technique | 1 500 | Pipeline exécutable |
| **Cible confirmatoire** | **≥ 2 520** | Gate SCI-001 |
| Préféré | 3 780–5 040 | Robustesse |

### 9.3 C02 / adjusted_close (DEC-15)

DatasetSnapshot **doit** documenter :

- `adjustment_policy` (vendor, splits/dividendes)
- `vendor_revision` ou `as_of_download`
- `fingerprint` immuable
- Risque révision rétroactive explicité

Point-in-time : reporté à DATA-REQ-I01.

### 9.4 DATA-REQ-I01

Produit **après** revue protocole PASS. **Non produit** dans l'intervention courante.

---

## 10. Artefacts C01

| Artefact | Contenu |
|----------|---------|
| `metrics.json` | $\bar{\Delta}^\text{raw/vol/shape}$, p-values bootstrap, par split |
| `gate_results.json` | SCI-* + SCI-DIAG-* |
| `bootstrap_sensitivity_L.json` | Grille $L$ |
| `neighbor_temporal_diag.json` | SCI-DIAG-1 |
| `config.yaml` | configuration + snapshot ref + git commit |

---

## 11. Reproductibilité (DEC-14)

- Tri dates : lexicographique / ordre calendrier croissant stable
- Seeds : B0=42, bootstrap=456
- Tolérance float : $10^{-10}$ sur distances
- `implementation_version` + deps dans artefacts

---

## 12. Falsifiabilité (DEC-13)

- Protocole v0.2 + configuration figés **avant** accès aux résultats test
- Interdit : changer métrique endpoint, $(W,k,h,L)$, subset dates post-hoc
- FAIL est résultat valide

---

## Références

- [hypothesis.md](hypothesis.md)
- [configuration.yaml](configuration.yaml)
- [review_decisions.md](review_decisions.md)
