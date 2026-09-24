# DR-008 — Source sandbox I01-E01 (yfinance)

> **Identifier :** DR-008
> **Status :** ACCEPTED
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1
> **Date :** 2026-09-24
> **Baseline :** DR-007 ACCEPTED `a4ce062`
> **Relève :** DEF-E-01
> **Parent :** [DR-007](DR-007-exploratory-vs-confirmatory-data.md)

Choix **léger**. Ce n'est pas une qualification. Ce n'est pas un amendement à DR-003.

## Context

I01-E01 a besoin d'une source gratuite, pratique et traçable pour faire tourner le
pipeline géométrique déjà spécifié. DR-007 interdit d'attendre DR-003 / DR-005
pour explorer, et interdit d'utiliser l'exploration comme preuve SCI.

DR-003 L-13 a déjà écarté Yahoo / `yfinance` du confirmatoire (PA-14 : interface
non officielle, non affiliée). Ce FAIL confirmatoire **reste**.

## Decision

Pour I01-E01 uniquement :

```text
SPY / yfinance / daily / EXPLORATORY ONLY / UNQUALIFIED
```

| Champ | Valeur |
|-------|--------|
| Instrument | SPY |
| Bibliothèque | `yfinance` **1.6.0** (pinnée) |
| Barre | `interval="1d"` |
| Classe | `EXPLORATORY` / `UNQUALIFIED` |
| Promotion | `NOT SCIENTIFICALLY PROMOTABLE` |

Paramètres de requête **tous explicites** (aucun default yfinance n'est une
autorité). En particulier :

- `auto_adjust=False` — la série I01 est `Adj Close`, pas le `Close` muté par défaut ;
- `repair=False` — pas de réparation silencieuse ;
- `actions=True` — corporate actions conservées à titre de trace, pas comme calendrier ;
- `prepost=False`, `back_adjust=False`, `keepna=False`, `rounding=False` ;
- `start="1993-01-22"` (création SPY, DR-003 D-2) ;
- `end` = date UTC du jour d'acquisition, exclusive selon le contrat yfinance, **enregistrée**.

Le calendrier des lignes retournées **n'est pas** un calendrier de marché (DR-005).

## Constraints

- N'amende pas DR-003 (L-13 FAIL inchangé ; D-1 INCONCLUSIVE).
- Ne constitue pas DATA-PASS. Aucun `DatasetSnapshot` C02 n'est produit.
- Ne rend pas yfinance admissible au confirmatoire.
- Aucun verdict SCI / PRED / ECON / promotion.
- Aucune tentative de « qualification » de yfinance.
- Aucune acquisition payante.
- Cache et extraits bruts : `data/exploratory/` (gitignoré), marqués `UNQUALIFIED`.
- Le cœur I01 n'importe pas `yfinance`.

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| Attendre un finaliste DR-003 | Rejeté — c'est le confirmatoire |
| CSV manuel sans provenance | Rejeté — moins traçable qu'un adaptateur versionné |
| `auto_adjust=True` (default 1.6.0) | Rejeté comme implicite ; la série doit nommer `Adj Close` |

## Consequences

- DEF-E-01 déchargé pour I01-E01.
- Un adaptateur `quant.exploratory` peut télécharger SPY.
- Un futur adaptateur C02 remplacera cet adaptateur **sans** réécrire la géométrie.

## Status

**ACCEPTED** — choix sandbox I01-E01 uniquement. Pas une source confirmatoire.
