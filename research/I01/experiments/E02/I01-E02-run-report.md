# I01-E02 — Diagnostics exploratoires

> **EXPLORATORY / UNQUALIFIED / NOT SCIENTIFICALLY PROMOTABLE**
>
> Objectif : expliquer d'où vient le Δ d'E01. Pas un meilleur résultat.
> Paramètres **figés** : `W=20`, `k=50`, `h=10`, L2, B0 `R=200` seed `42`.
> Aucun gate SCI. Aucun retuning. Aucune reprise DR-003 / DR-005.

| Champ | Valeur |
|-------|--------|
| Parent | I01-E01 |
| Cache | même téléchargement UNQUALIFIED (2026-09-24T12:00:16Z) |
| Séances / `T_eval` | 8470 / 8038 |
| Période évaluée | 1994-09-30 → 2026-09-09 |

Les moyennes `H_*` reproduisent E01 à la précision affichée. On diagnostique
**le même run**, pas une nouvelle expérience.

## 1. Décomposition temporelle

`Δ = H_B0 − H_geo` (positif ⇒ voisinage géométrique plus homogène que B0).

| | moyenne `Δ` | part des `t` avec `Δ>0` |
|--|-------------|-------------------------|
| raw | +0.00622 | 90.4 % |
| vol | +1.83e-4 | 88.5 % |
| shape | +0.00288 | 53.7 % |

Sur **33** années civiles de `t` :

- 32 / 33 ont une moyenne annuelle `Δ_raw > 0` (97 %) ;
- la plus grosse année (2012) porte **5,5 %** de la somme des `Δ_raw` ;
- 1994 est la seule année à moyenne `Δ_raw` **négative** (−0.0018 ; 7,8 % des
  dates 1994 positives). C'est cohérent avec l'observation E01 sur `t=422` :
  au début, `L_t` est court.

**Observation :** l'effet raw n'est pas un artefact de deux ou trois crises.
Il est diffus sur trois décennies, avec un démarrage faible/négatif quand la
bibliothèque est encore petite. Ce n'est pas une preuve de robustesse
confirmatoire.

## 2. Âge des voisins (`t − s`, rangs de séance)

| | sessions |
|--|----------|
| q10 / médiane / q90 (voisins poolés) | 167 / **1220** / 3968 |
| part `t−s > 252` (~1 an) | 85.5 % |
| part `t−s > 1260` (~5 ans) | 48.9 % |
| part `t−s > 2520` (~10 ans) | 24.7 % |

Médiane des médianes d'âge par tertile de `T_eval` :

| Tertile | médiane de `median(t−s)` |
|---------|--------------------------|
| early | 612 |
| middle | 1514 |
| late | 2546 |

**Observation :** la géométrie ne se limite pas aux situations récentes. Un
voisin sur quatre a plus de dix ans de rang. L'âge médian **augmente** avec
`t` (la bibliothèque s'allonge) — propriété mécanique du protocole, pas un
bug. `t=422` reste le cas extrême du tertile early.

## 3. Structure du voisinage (distances L2)

Moyennes sur `T_eval` :

| | L2 |
|--|----|
| rang 1 | 3.17 |
| rang 25 | 3.97 |
| rang 50 | 4.15 |
| médiane de `L_t` (tous les candidats admissibles) | 6.04 |
| rang 50 / médiane bibliothèque | **0.671** |
| rang 1 / médiane bibliothèque | 0.509 |

Les 50 distances croissent lentement (3.17 → 4.15). Le 50e voisin reste plus
près qu'un candidat typique de `L_t`, sans coller au rang 1.

**Observation :** `k=50` n'est pas un voisinage vide de sens (le 50e n'est pas
aussi loin qu'un état quelconque), ni une boule ultra-serrée. On **n'en déduit
pas** qu'il faille changer `k`.

## 4. Décomposition `H_raw` / `H_vol` / `H_shape`

Réduction relative vs B0 (mêmes chiffres qu'E01) :

| | `(H_B0 − H_geo) / H_B0` |
|--|-------------------------|
| raw | 13.7 % |
| vol | 54.0 % |
| shape | 0.21 % |

Association descriptive sur les 8038 dates (OLS `Δ_raw ~ Δ_vol + Δ_shape`,
**pas un modèle causal**, pas un gate) :

| | |
|--|--|
| corr(`Δ_raw`, `Δ_vol`) | **0.762** |
| corr(`Δ_raw`, `Δ_shape`) | **0.009** |
| corr(`Δ_vol`, `Δ_shape`) | −0.185 |
| R² | 0.604 |
| coef `Δ_vol` / `Δ_shape` | 25.4 / 0.065 |

**Observation conservée, non tranchée :** le gain brut exploratoire se
comporte surtout comme un gain d'homogénéité d'**amplitude / volatilité**
future. La forme des trajectoires (`H_shape`) bouge à peine et n'accompagne
presque pas `Δ_raw`.

Question scientifique **toujours ouverte** (E01) :

> La proximité géométrique des passés sélectionne-t-elle des futurs de forme
> similaire, ou surtout des états menant à un régime de volatilité similaire ?

E02 **n'y répond pas**. Elle la rend quantitative.

## Ce que E02 n'autorise pas

- inventer I02, changer `W`, `k`, `h`, L2, B0 ou la représentation ;
- un SCI-PASS ou un SCI-FAIL ;
- rouvrir DR-003 / DR-005 par automatisme ;
- du trading.

## Revue exploratoire (décision humaine, pas ce rapport)

```text
E02
 ├── piste sans intérêt              → STOP I01 exploratoire
 ├── problème méthodologique         → nouvelle investigation documentée
 └── phénomène suffisamment intéressant
         → alors seulement DR-003 + DR-005 → C02 → I01 confirmatoire
```

Ce rapport **ne choisit pas** la branche. Il fournit les observations.

Figures hors git : `data/exploratory/UNQUALIFIED_e02_delta_by_year.png`,
`UNQUALIFIED_e02_distance_by_rank.png`.
