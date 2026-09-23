# Quant — système de trading quantitatif géostatistique

> **Phase actuelle :** P1 — Géométrie classique (OPEN — I01 cadrage)
> **Protocol :** QDP v0.1

Plateforme expérimentale de trading quantitatif fondée sur la géométrie, les statistiques
et la validation reproductible. Le Risk Engine est souverain ; **NO_TRADE** est un résultat
de première classe.

## État du projet

| Phase | Statut | Document |
|-------|--------|----------|
| P0 Fondation | CLOSED (HAT PASS) | [P0-closure-report.md](docs/foundation/P0-closure-report.md) |
| P1 Géométrie classique | OPEN | [P1-cadrage.md](docs/foundation/P1-cadrage.md) |
| I01 Voisinage géométrique | Protocol draft | [research/I01/](research/I01/) |

## Installation (développement)

```bash
pip install -e ".[dev]"
pytest
```

## Ce que P0 contient

- Gouvernance QDP v0.1 et chaîne de promotion scientifique / opérationnelle
- Contrats versionnés C01–C05 (Experiment, DatasetSnapshot, MarketState, StrategySignal, RiskDecision)
- Implémentation Python typée (Pydantic) et tests d'invariants
- Traçabilité `DecisionTrace` pour reconstruction de décisions

## Ce que P0 ne contient pas

- Stratégies de trading réelles
- Source de données figée
- Connexion broker ou paper trading
- Branches p-adique / dynamique (frontière architecturale seulement)

## Prochaine étape

1. Revue protocole I01 → [evaluation_protocol_review.md](research/I01/evaluation_protocol_review.md)
2. Dérivation besoins data → `DATA-REQ-I01.md`
3. ADR source de données (si applicable)
4. Implémentation pipeline I01 (interdit avant 1–3)
