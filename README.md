# Quant — système de trading quantitatif géostatistique

> **Phase actuelle :** P0 — Fondation (CLOSED)
> **Protocol :** QDP v0.1

Plateforme expérimentale de trading quantitatif fondée sur la géométrie, les statistiques
et la validation reproductible. Le Risk Engine est souverain ; **NO_TRADE** est un résultat
de première classe.

## État P0

- Spécification : [docs/foundation/P0-specification.md](docs/foundation/P0-specification.md)
- Contrats : [specs/contracts/](specs/contracts/)
- Rapport de clôture : [docs/foundation/P0-closure-report.md](docs/foundation/P0-closure-report.md)

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

## Prochaine phase

**P1 — Géométrie classique** — uniquement après GO explicite (voir rapport P0).
