# Revue de cohérence P0

> **Identifier :** P0-REVIEW-v0.1
> **Status :** ACCEPTED
> **Authority class :** FOUNDATION
> **Protocol :** QDP v0.1
> **Verdict :** PASS — proceed to skeleton

Revue effectuée après rédaction de la spécification P0 et des contrats C01–C05,
**avant** implémentation du squelette.

---

## 1. Dépendances circulaires

| Chaîne | Verdict |
|--------|---------|
| C02 → C03 → C04 → C05 | **Acyclique** — flux unidirectionnel |
| C01 → C02–C05 (refs) | **Acyclique** — C01 référence sans être référencé |
| DecisionTrace | **Acyclique** — agrégation en fin de chaîne |

**Action :** aucune.

## 2. Responsabilités ambiguës

| Zone | Risque identifié | Résolution |
|------|------------------|------------|
| Features vs MarketState | C03 pourrait recalculer des features | C03 utilise `feature_refs` par référence, pas recalcul |
| Confidence vs Risk | Confusion autorisation | C04 documente ; C05 invariant explicite |
| Abstain (strategy) vs NO_TRADE (risk) | Double sémantique | C04 ABSTAIN = stratégie ; C05 NO_TRADE = risque souverain |
| Grading vs Orchestrator | Hors P0 | Non implémenté ; frontière documentée §4 P0-spec |

**Action :** commentaires dans modèles Python ; tests d'invariants.

## 3. Contrats trop spécialisés

| Contrat | Risque | Verdict |
|---------|--------|---------|
| C03 experimental_branch | Prématuré ? | **Justifié** — frontière R&D sans impl |
| C02 storage_hint | Décision technique | **Non normatif** — hint optionnel seulement |
| C05 authorized_exposure | Structure libre | **Acceptable P0** — typage `dict` générique ; spécialisation P3 |

**Action :** `storage_hint` reste optionnel ; pas de loader en P0.

## 4. Décisions prématurées évitées

| Candidat | Statut P0 |
|----------|-----------|
| yfinance / Polygon | **Non choisi** — C02.provenance.source_label abstrait |
| Parquet / CSV | **Non choisi** — storage_hint informatif |
| Makefile / justfile | **Non choisi** — pyproject + pytest suffisent |
| Broker / paper engine | **Exclu** explicitement |
| Stratégies réelles | **Exclu** explicitement |
| Python | **ADR DR-001** — seul choix figé (langage impl) |

## 5. Chaîne de promotion

| Check | Verdict |
|-------|---------|
| Distinction scientifique / opérationnelle | **Claire** — PromotionRecord dual |
| INCONCLUSIVE normatif | **Présent** — GateSpec.verdict |
| Piège « math ⇒ trade » | **Adressé** — promotion_chain.md + ECON gate |

## 6. Invariants testables

| Invariant | Test prévu |
|-----------|------------|
| I1 Risk sovereignty | test_risk.py |
| I2 NO_TRADE first-class | test_risk.py |
| I3 Temporal integrity | test_temporal.py |
| I4 Traceability | test_decision_trace.py |
| C01 baselines non-empty | test_experiment.py |
| C04 abstain_reason | test_strategy_signal.py |

## 7. Blockers identifiés

**Aucun blocker** pour le squelette P0.

## 8. Dette acceptée (documentée)

| Item | Report |
|------|--------|
| Capability Manifest YAML | Post-P0, quand première promotion |
| Loader de données concret | P1 |
| Schéma JSON Schema export | Optionnel ; pydantic suffit P0 |
| Registre experiments persistant | P1 |

---

**Conclusion :** PASS — implémentation du squelette autorisée.
