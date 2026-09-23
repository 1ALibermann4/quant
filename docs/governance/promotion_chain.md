# Chaîne de promotion — scientifique vs opérationnelle

> **Identifier :** PROMO-CHAIN-v0.1
> **Status :** ACCEPTED
> **Authority class :** GOVERNANCE
> **Protocol :** QDP v0.1

## Problème adressé

Éviter le piège : *« ça marche mathématiquement, donc tradons-le »*.

Une métrique, une représentation ou une stratégie peut améliorer une mesure statistique
sans produire d'avantage économique après coûts. Les deux dimensions doivent être tracées séparément.

## Chaîne complète

```text
Hypothèse
    ↓
Investigation (Ixx)
    ↓
Validation statistique      ← gate SCI-*
    ↓
Validation prédictive       ← gate PRED-*
    ↓
Validation économique       ← gate ECON-*
    ↓
Validation paper            ← gate PAPER-*
    ↓
Promotion opérationnelle    ← gate OPS-*
```

## Verdicts possibles par gate

| Verdict | Signification | Effet |
|---------|---------------|-------|
| **PASS** | Critères satisfaits pour cette étape | Passage à l'étape suivante autorisé |
| **FAIL** | Hypothèse invalidée ou critères non atteints | Clôture ou retour à l'investigation |
| **INCONCLUSIVE** | Données ou protocole insuffisants | Pas de promotion ; préciser ce qui manque |

## Matrice de promotion (exemples)

| Résultat | SCI | PRED | ECON | Décision |
|----------|-----|------|------|----------|
| Meilleurs voisinages, pas d'edge | PASS | PASS | FAIL | **Promotion scientifique**, NO-GO opérationnel |
| Edge in-sample seulement | PASS | FAIL | — | Retour investigation / reformulation |
| Edge OOS mais coûts destructeurs | PASS | PASS | FAIL | Archive R&D, pas de paper |
| Edge OOS + coûts OK | PASS | PASS | PASS | Éligible paper (P6) |

## Gates minimales par étape (P0 — définition)

### SCI-* (validation statistique)

- Hypothèse et mécanisme documentés **avant** optimisation.
- Baseline obligatoire exécutée sur les mêmes données.
- Métriques primaires et secondaires déclarées à l'avance.
- Pas de look-ahead bias (voir C02 invariants).

### PRED-* (validation prédictive)

- Split train / validation / test ou walk-forward documenté.
- Performance évaluée hors échantillon de sélection des paramètres.
- Sensibilité paramétrique minimale documentée.

### ECON-* (validation économique)

- Frais, spread, slippage et contraintes de liquidité modélisés.
- Avantage net vs baseline après coûts.
- Résultats non concentrés sur une poignée de trades ou une seule période.

### PAPER-* (validation paper)

- Flux temps réel ou simulation d'ordres réaliste.
- Écart backtest/paper expliqué ou borné.

### OPS-* (promotion opérationnelle)

- Tous les gates précédents PASS.
- Plan de désactivation défini.
- Risk Engine validé indépendamment (P3).

## Séparation des registres

| Registre | Contenu |
|----------|---------|
| `research/` | Investigations Ixx, prototypes jetables |
| `specs/contracts/` | Contrats normatifs versionnés |
| `specs/baselines/` | Baselines obligatoires |
| Artefacts d'expérience | Métriques, empreintes, logs — référencés par C01 |

Une promotion scientifique **n'écrit pas** automatiquement dans le socle opérationnel.
