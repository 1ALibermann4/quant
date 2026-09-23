# Quant Development Protocol v0.1 (QDP v0.1)

> **Identifier :** QDP-v0.1
> **Status :** ACCEPTED
> **Authority class :** GOVERNANCE
> **Protocol :** QDP v0.1

## Principe fondateur

Codifier la rigueur R&D et de gouvernance du projet quantitatif. Ne pas remplacer
la doctrine scientifique du rapport fondateur v0.1 par une méthodologie agile générique.

Le marché est un objet à **mesurer** avant d'être un objet à **trader**.

## Cycle de vie d'une investigation

```text
HYPOTHÈSE
  → INVESTIGATION (Ixx)
  → VALIDATION STATISTIQUE
  → VALIDATION PRÉDICTIVE
  → VALIDATION ÉCONOMIQUE
  → VALIDATION PAPER
  → PROMOTION OPÉRATIONNELLE
```

Chaque étape produit un **verdict de gate** explicite : PASS, FAIL ou INCONCLUSIVE.
Une étape INCONCLUSIVE ne promeut pas ; elle peut exiger des données ou une reformulation.

## Deux niveaux de promotion

| Niveau | Question | Conséquence |
|--------|----------|-------------|
| **Scientifique** | La représentation ou la métrique apporte-t-elle une information robuste et reproductible ? | Autorise la poursuite R&D et l'intégration dans le socle expérimental |
| **Opérationnelle** | L'avantage survit-il aux coûts, au risque, à la liquidité et à l'exécution ? | Autorise la promotion dans le moteur de trading (paper puis réel) |

Un résultat peut être **scientifiquement positif** et **opérationnellement NO-GO**.
Exemple : une métrique p-adique produit de meilleurs voisinages d'états sans edge économique.

## Séparation des responsabilités

| Couche | Responsabilité | Ne décide pas |
|--------|----------------|---------------|
| Data | Observation propre, horodatée, qualifiée | Quoi trader |
| Representation / Features | Forme mathématique de l'état | Taille de position |
| Market State | Régime et incertitude contextuelle | Exécution |
| Strategy | Proposition structurée | Budget de risque final |
| Grading / Orchestration | Pertinence conditionnelle | Contourner le risque |
| Portfolio | Combinaison cohérente | Veto final |
| Risk Engine | Autorisation, réduction, veto | Générer des signaux |
| Execution | Réalisation sans dégrader l'idée | Stratégie |
| Experimentation | Hypothèse, protocole, artefacts | Trading live |

## Règles pour les agents et contributeurs

1. L'historique de chat n'est **pas** une autorité.
2. Classifier la tâche → identifier l'autorité → définir les gates → exécuter jusqu'à **closure**.
3. STOP uniquement aux frontières d'autorité (ambiguïté contractuelle, conflit spec/test).
4. Ne pas implémenter de stratégie réelle avant P2.
5. Ne pas connecter de broker avant P6.
6. Toute décision technique figée requiert un **Decision Record** (ADR/DR).

## Phases roadmap (rappel)

| Phase | But | Gate de sortie |
|-------|-----|----------------|
| **P0** | Contrats, reproductibilité, invariants | Pipeline reproductible sans trading |
| P1 | Géométrie classique, features, état | Mesures testées et visualisables |
| P2 | Stratégies minimales | Backtests corrects avec baselines |
| P3 | Risk Engine | Veto et limites testés |
| P4 | Orchestrateur | Grading conditionnel |
| P5 | Validation robuste | Résultats OOS documentés |
| P6 | Paper trading | Écart backtest/paper compris |
| R1/R2 | Branches p-adique / dynamique | Promotion uniquement si gain robuste |

P0 **s'arrête** après son rapport de clôture. P1 ne démarre pas sans GO explicite.
