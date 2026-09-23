# Gates de clôture

> **Identifier :** CLOSURE-GATES-v0.1
> **Status :** ACCEPTED
> **Authority class :** GOVERNANCE
> **Protocol :** QDP v0.1

## Modèle de cycle

```text
OPEN → EXECUTION → GATE REVIEW
                      ├─ PASS        → CLOSED (succès)
                      ├─ FAIL        → OPEN (travaux correctifs) ou CLOSED (échec documenté)
                      ├─ INCONCLUSIVE → OPEN (données/protocole insuffisants)
                      └─ AUTHORITY BLOCKER → ESCALATE
```

Chaque cycle déclare **avant exécution** : OBJECTIVE, SCOPE, NON-GOALS, AUTHORITIES, GATES, STOP CONDITIONS.

## Préfixes de gates

| Préfixe | Domaine |
|---------|---------|
| **P0-*** | Fondation P0 |
| **SCI-*** | Validation statistique |
| **PRED-*** | Validation prédictive |
| **ECON-*** | Validation économique |
| **PAPER-*** | Validation paper |
| **OPS-*** | Promotion opérationnelle |
| **RISK-*** | Risk Engine |
| **DATA-*** | Intégrité et provenance des données |

## Gates P0 (fondation)

| Gate | Critère | Verdict attendu P0 |
|------|---------|-------------------|
| P0-SPEC | Spécification P0 complète et revue | PASS |
| P0-CONTRACTS | C01–C05 définis et implémentés | PASS |
| P0-INVARIANTS | Tests d'invariants passent | PASS |
| P0-REPRO | Protocole de reproductibilité documenté | PASS |
| P0-NO-TRADE | NO_TRADE modélisé comme résultat de première classe | PASS |
| P0-RISK-SOV | Souveraineté Risk Engine formalisée | PASS |
| P0-NO-STRATEGY | Aucune stratégie réelle implémentée | PASS |
| P0-NO-BROKER | Aucune connexion broker / live | PASS |
| P0-CLEAN-TREE | Working tree propre à la clôture | PASS |

## Verdicts

| Verdict | Usage |
|---------|-------|
| **PASS** | Gate satisfaite ; preuve attachée |
| **FAIL** | Gate non satisfaite ; raison documentée |
| **INCONCLUSIVE** | Évaluation impossible faute de données, de spec ou de protocole |

INCONCLUSIVE est **normatif** dans QDP (contrairement à ADP Argus où il est absent).
Il force la distinction entre « échec » et « on ne sait pas encore ».

## Recommandation GO / NO-GO P1

Le rapport de clôture P0 émet une recommandation explicite :

- **GO P1** : fondation suffisante pour démarrer la géométrie classique.
- **NO-GO P1** : blockers documentés ; P1 ne démarre pas.
