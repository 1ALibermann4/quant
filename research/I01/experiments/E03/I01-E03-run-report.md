# I01-E03 — Diagnostic mécanistique (volatilité)

> **EXPLORATORY / UNQUALIFIED / NOT SCIENTIFICALLY PROMOTABLE**
>
> Objectif : la géométrie L2 apporte-t-elle une structure de volatilité future
> **au-delà** de la persistance de volatilité passée ?
> Paramètres **figés** : `W=20`, `k=50`, `h=10`, L2, B0 `R=200` seed `42`.
> Le voisinage `rv_W` est un **contrôle diagnostique**, pas un B0, pas un gate.

| Champ | Valeur |
|-------|--------|
| Parent | I01-E02 (revue : poursuivre, pas confirmer) |
| Cache | même téléchargement UNQUALIFIED (2026-09-24T12:00:16Z) |
| Séances / `T_eval` | 8470 / 8038 |
| Contrôle | `k` plus proches dans `\|rv_W(s) − rv_W(t)\|` sur le même `L_t` |

Les moyennes L2 / B0 reproduisent E01–E02 à la précision affichée.

## 1. Le contrôle fait bien ce qu'il doit

| | `H_vol` | réduction vs B0 | `H_raw` | réduction vs B0 |
|--|---------|-----------------|---------|-----------------|
| L2 | 1.55e-4 | **54,0 %** | 0.03912 | **13,7 %** |
| contrôle `rv_W` | 1.96e-4 | **41,9 %** | 0.04435 | **2,2 %** |
| B0 | 3.38e-4 | — | 0.04534 | — |

`H_shape` : L2 1.385 ; contrôle 1.388 ; B0 1.388. Le contrôle de vol ne
rapproche pas les formes.

Association descriptive (pas un modèle causal) :

| | corr. |
|--|--|
| `rv_W` ~ `‖Y‖` | **0,671** |
| `σ̂_M` ~ `‖Y‖` | 0,400 |
| `‖X‖` ~ `‖Y‖` | 0,448 |
| `rv_W` ~ `σ̂_M` | 0,534 |
| `‖X‖` ~ `rv_W` | 0,705 |

La persistance de volatilité existe sur ce sandbox : matcher `rv_W` homogénéise
les `‖Y‖` futurs (contrôle vs B0 : `H_vol` −42 %). Ce n'est pas une surprise.

## 2. L2 ne voyage pas par ce canal

Écart moyen de volatilité passée `|rv_W(s) − rv_W(t)|` :

| voisinage | `|Δ rv_W|` | vs bibliothèque |
|-----------|------------|-----------------|
| L2 | 0.00467 | **0,957** |
| contrôle `rv_W` | 0.000375 | 0,077 |
| médiane de `L_t` | 0.00488 | 1 |

Les voisins L2 sont **presque aussi éloignés en `rv_W`** qu'un candidat
quelconque de `L_t`. L2 n'est pas un sélecteur de niveau de volatilité
absolue de la fenêtre `W`.

Donc le diagramme demandé se lit ainsi :

```text
géométrie X  ─/─✗─/─►  proximité de rv_W   (quasi nulle)
      │
      ▼
voisins L2  ──────►  homogénéité de vol future   (présente)
```

## 3. Lecture exploratoire des trois situations

Sur la **moyenne** `H_vol` : L2 < contrôle < B0 (L2 environ 21 % plus bas que
le contrôle). Ce n'est **pas** « L2 ≈ contrôle » ni « L2 < contrôle ».

Nuance obligatoire : L2 a un `H_vol` plus bas que le contrôle sur **seulement
42,8 %** des dates. L'avantage moyen n'est pas un gain date par date. Les deux
battent B0 souvent (L2 88,5 % ; contrôle 83,6 %).

Sur `H_raw`, l'écart est net : le contrôle récupère **2,2 %** vs B0, L2
**13,7 %**. Le Δ brut d'E01 n'est pas une reformulation du matching `rv_W`.

Observation conservée, **pas un verdict** :

> Le clustering de volatilité (contrôle `rv_W`) existe et explique une partie
> de `H_vol`. Il n'explique pas le `H_raw` géométrique, et L2 n'opère pas en
> recopiant le niveau de `rv_W`. Il reste une structure — au moins
> descriptive — que ce contrôle ne capture pas.

`>>` / `≈` / `<` restent des observations, pas des gates.

## Ce que E03 n'autorise pas

- remplacer B0 par le contrôle `rv_W` ;
- inventer I02, changer `W`, `k`, `h`, L2, B0 ou la représentation ;
- un SCI-PASS ou un SCI-FAIL ;
- rouvrir DR-003 / DR-005 par automatisme ;
- du trading.

## Revue exploratoire (décision humaine, pas ce rapport)

```text
E03
 ├── piste sans intérêt              → STOP I01 exploratoire
 ├── problème méthodologique         → nouvelle investigation documentée
 ├── phénomène à reformuler          → nouvelle hypothèse (pas un retuning silencieux)
 └── I01 pré-enregistré encore pertinent
         → alors seulement DR-003 + DR-005 → C02 → I01 confirmatoire
```

Ce rapport **ne choisit pas** la branche.

Figures hors git : `data/exploratory/UNQUALIFIED_e03_h_vol_by_year.png`,
`UNQUALIFIED_e03_past_vol_proximity.png`.
