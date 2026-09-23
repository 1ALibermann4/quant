# Baselines obligatoires

> **Identifier :** BASELINES-v0.1
> **Status :** ACCEPTED
> **Authority class :** SPECIFICATION
> **Protocol :** QDP v0.1

Toute expérience C01 doit déclarer au moins une baseline pertinente.
L'absence de baseline est un **FAIL** de gate SCI-000.

## Catalogue P0 (déclaratif)

| ID | Nom | Mécanisme | Usage |
|----|-----|-----------|-------|
| **B0** | Naive neighbor | Voisinage aléatoire ou uniforme sur l'espace d'état | Contrôle négatif pour études de voisinage (P1) |
| **B1** | Buy-and-hold | Détention passive de l'univers | Référence économique minimale |
| **B2** | Rolling z-score | Écart à une moyenne mobile normalisée | Référence statistique simple (mean reversion naïf) |
| **B3** | Simple momentum | Rendement cumulé sur fenêtre fixe | Référence trend/momentum naïf |

## Règles

1. La baseline doit utiliser le **même** DatasetSnapshot (C02) que l'hypothèse testée.
2. Les métriques comparées doivent être identiques (même protocole, mêmes splits).
3. B0 est obligatoire pour toute expérience portant sur la qualité de voisinage.
4. B1 est obligatoire dès qu'une métrique économique est déclarée (gate ECON-*).
5. Les baselines ne sont **pas exécutées** en P0 ; leur catalogue est normatif.

## Extension

De nouvelles baselines (B4+) requièrent une mise à jour de ce document et une reference dans C01.
