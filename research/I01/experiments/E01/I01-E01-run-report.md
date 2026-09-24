# I01-E01 — Rapport du premier run exploratoire

> **EXPLORATORY / UNQUALIFIED / NOT SCIENTIFICALLY PROMOTABLE**
>
> Ce document **n'est pas** un verdict SCI. Il n'est pas un DATA-PASS.
> Il n'autorise aucune promotion. `mean_Δ > 0` n'est **pas** un SCI-PASS.
> `mean_Δ ≤ 0` n'aurait **pas** été un SCI-FAIL.

| Champ | Valeur |
|-------|--------|
| Investigation | I01-E01 |
| Baseline gouvernance | DR-007 `a4ce062` · DR-008 (cette vague) |
| Instrument | SPY |
| Source | yfinance **1.6.0** |
| Série I01 | `Adj Close` (`auto_adjust=False`, `repair=False`) |
| Acquisition UTC | 2026-09-24T12:00:16Z |
| Requête | `start=1993-01-22`, `end=2026-09-25` (exclusive), `interval=1d` |
| Paramètres I01 | `W=20`, `M=252`, `ε=1e-8`, `k=50`, `h=10`, `τ=20`, `L_min=150`, B0 `R=200` seed `42` |

Les barres brutes restent dans `data/exploratory/` (gitignoré). Elles ne sont
**pas** un calendrier NYSE.

## Couverture reçue

| Mesure | Valeur |
|--------|--------|
| Séances reçues | 8470 |
| Première / dernière ligne | 1993-01-29 → 2026-09-23 |
| États évaluables `T_eval` | 8038 |
| Première / dernière date évaluée | 1994-09-30 → 2026-09-09 |

**Observation (pas un défaut à corriger ici) :** la première ligne livrée est
le 1993-01-29, pas le 1993-01-22 demandé. Yahoo n'a pas renvoyé de barre pour
les premiers jours civils. On n'en déduit pas une fermeture de marché.

## Exemple — `t = 422` (1994-09-30)

`X_t` (20 composantes, standardisation causale) :

```text
-0.736  0.038  -0.183  0.813  -1.792
-0.520  0.486   0.150  2.087  -1.215
 0.150 -3.222  -0.017 -0.415  -0.587
 0.837 -0.131   1.285 -0.865  -0.244
```

50 voisins L2 (plus proche → plus loin) : 1994-06-20 (d=4.067) … 1994-05-10
(d=6.469). Médiane 5.946, moyenne 5.840.

**Observation :** à la première date évaluable, `L_t` ne contient que l'histoire
1993–1994. Les 50 voisins tombent donc tous en 1994. Ce n'est pas une raison
pour changer `W`, `k` ou `τ`.

| Métrique (cet exemple) | Géo | B0 |
|------------------------|-----|----|
| `H_raw` | 0.02801 | 0.02767 |
| `H_vol` | 5.18e-5 | 5.00e-5 |
| `H_shape` | 1.380 | 1.396 |

Sur **cet** exemple, `H_raw` géo n'est pas inférieur à B0. Le run global
ci-dessous moyenne 8038 dates.

## Moyennes sur `T_eval` (8038 dates)

| | Géo | B0 | Δ = B0 − géo |
|--|-----|----|----------------|
| `H_raw` | 0.03912 | 0.04534 | +0.00622 |
| `H_vol` | 1.55e-4 | 3.38e-4 | +1.83e-4 |
| `H_shape` | 1.3854 | 1.3883 | +0.00288 |

Lecture autorisée : *sur ce run non qualifié, la moyenne de `H_raw` géométrique
est inférieure à B0.* Lecture **interdite** : SCI-PASS, robustesse, alpha,
trading.

Aucun paramètre n'a été retuné après ces chiffres.

## Anti-fuite

Les tests synthétiques (`tests/i01/test_anti_leakage.py`) passent, y compris un
jeu où une standardisation qui lit `r_{t+1}` est détectée. Le run SPY n'ajoute
pas de p-value.

## Figures

Générées hors git, mêmes étiquettes UNQUALIFIED :

- `data/exploratory/UNQUALIFIED_example_distances.png`
- `data/exploratory/UNQUALIFIED_h_raw_series.png`

## Ce qui n'a pas été fait

- Pas de block bootstrap, pas de split test, pas de gate SCI-*.
- Pas de travail DR-003 / DR-005.
- Pas de qualification de yfinance.
- Pas de signal, portefeuille, broker, capital.

## Suite possible (hors cette clôture)

Choisir plus tard une autre date d'exemple (milieu de `T_eval`) pour l'illustration,
sans changer les paramètres. Reprendre DR-003 / DR-005 quand on voudra confirmer.
