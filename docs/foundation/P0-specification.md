# Spécification P0 — Fondation

> **Identifier :** P0-SPEC-v0.1
> **Status :** ACCEPTED
> **Authority class :** FOUNDATION
> **Protocol :** QDP v0.1
> **Verdict :** Foundation — no trading

Document fondateur opérationnel dérivé du rapport fondateur v0.1.
P0 établit contrats, invariants et protocole de reproductibilité **sans** implémenter
de stratégie réelle, de connexion broker ou de trading live.

---

## 1. Objectifs P0

| Objectif | Livrable |
|----------|----------|
| Formaliser objectifs, non-objectifs et invariants | §2, §3 |
| Fixer le vocabulaire canonique | [vocabulary.md](../governance/vocabulary.md) |
| Délimiter les frontières entre couches | §4 |
| Définir les contrats versionnés C01–C05 | [specs/contracts/](../../specs/contracts/) |
| Distinguer Contract / Implementation / Manifest | [versioning_axes.md](../governance/versioning_axes.md) |
| Protocole anti look-ahead et reproductibilité | §6, §7 |
| Baselines obligatoires | [mandatory_baselines.md](../../specs/baselines/mandatory_baselines.md) |
| Chaîne de promotion scientifique vs opérationnelle | [promotion_chain.md](../governance/promotion_chain.md) |
| NO_TRADE et souveraineté Risk Engine | §5, C05 |
| Reconstruction intégrale d'une décision | §8 |
| Frontière socle opérationnel / R&D | §9 |
| Squelette logiciel minimal | `src/quant/` |

## 2. Non-objectifs P0

- Implémenter trend following, mean reversion, pairs ou toute stratégie réelle.
- Choisir définitivement une source de données (API, broker, format de fichiers).
- Connecter un broker ou exécuter du trading live / paper.
- Implémenter la branche p-adique ou dynamique/chaos (frontière architecturale seulement).
- Optimiser des paramètres sur des données de marché.
- Produire des métriques de performance économique.

## 3. Invariants système

Ces invariants s'appliquent à toutes les phases futures. Leur violation est un **FAIL** de gate.

### I1 — Risk sovereignty

Le Risk Engine peut **REDUCE**, **DELAY**, **VETO** ou émettre **NO_TRADE** indépendamment
de la confiance, du grade ou du signal brut. Aucune couche amont ne peut contourner C05.

### I2 — NO_TRADE first-class

`NO_TRADE` est un verdict explicite de RiskDecision, traçable et mesurable.
L'abstention n'est pas modélisée comme absence de données ou signal nul implicite.

### I3 — Temporal integrity

Aucune feature, état ou signal à l'instant *t* ne consomme d'information dont la
disponibilité effective est postérieure à *t* (no look-ahead).

### I4 — Traceability

Toute décision future (P3+) doit être reconstructible à partir d'un enregistrement
structuré : DatasetSnapshot → MarketState → StrategySignal(s) → RiskDecision.

### I5 — Hypothesis before optimization

L'hypothèse et les métriques de succès sont documentées **avant** l'exécution de l'expérience.

### I6 — Baseline obligation

Toute innovation est comparée à au moins une baseline déclarée dans le protocole.

### I7 — Two-level promotion

Une validation scientifique (SCI/PRED) ne déclenche pas automatiquement une promotion opérationnelle (ECON/PAPER/OPS).

### I8 — Separation of concerns

Les couches §4 ne fusionnent pas leurs responsabilités ; pas de « god object » Strategy+Risk.

## 4. Frontières entre couches

```text
┌─────────────────────────────────────────────────────────────┐
│ DATA (C02)                                                  │
│  Observations brutes → qualité → horodatage → snapshot      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ REPRESENTATION / FEATURES (hors contrat P0 — P1)            │
│  Rendements, distances, volatilité, vecteurs d'état         │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ MARKET STATE (C03)                                          │
│  État x_t, régime, incertitude, stabilité                   │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ STRATEGY (C04) — proposition seulement                      │
│  StrategySignal : direction, force, confiance, abstention   │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ GRADING / PORTFOLIO (P4 — hors P0)                          │
│  Pertinence conditionnelle, combinaison d'expositions       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ RISK ENGINE (C05) — SOUVERAIN                               │
│  RiskDecision : AUTHORISE | REDUCE | DELAY | VETO | NO_TRADE│
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ EXECUTION (P6 — hors P0)                                    │
│  Ordres, fills, coûts — sans autorité stratégique           │
└─────────────────────────────────────────────────────────────┘

        EXPERIMENTATION (C01) — transversal, encadre toute investigation
        R&D branches (p-adic, dynamics) — interfaces expérimentales, hors socle P0
```

### Règles de frontière

| Frontière | Règle |
|-----------|-------|
| Data → Representation | Les snapshots C02 sont la seule source autoritaire pour une expérience |
| Representation → MarketState | C03 référence les features par nom/version, ne les recalcule pas silencieusement |
| MarketState → Strategy | C04 consomme C03 ; ne modifie pas l'état |
| Strategy → Risk | C05 ne lit pas directement les features brutes ; passe par signaux et contexte risque |
| Risk → Execution | L'exécution ne peut augmenter l'exposition au-delà de C05 |
| Experimentation | C01 référence C02–C05 versions ; ne court-circuite aucune couche |

## 5. Contrats versionnés (C01–C05)

| ID | Nom | Fichier spec | Rôle |
|----|-----|--------------|------|
| C01 | Experiment | `specs/contracts/C01/C01_v1.0.yaml` | Investigation reproductible |
| C02 | DatasetSnapshot | `specs/contracts/C02/C02_v1.0.yaml` | Provenance et empreinte des données |
| C03 | MarketState | `specs/contracts/C03/C03_v1.0.yaml` | État de marché à *t* |
| C04 | StrategySignal | `specs/contracts/C04/C04_v1.0.yaml` | Proposition de stratégie |
| C05 | RiskDecision | `specs/contracts/C05/C05_v1.0.yaml` | Verdict souverain |

Implémentation typée : `src/quant/contracts/`.

Objets de traçabilité minimaux (P0) :

| Objet | Rôle |
|-------|------|
| `DecisionTrace` | Chaîne C02→C03→C04→C05 pour reconstruction |
| `PromotionRecord` | Verdicts SCI/PRED/ECON par expérience |
| `GateResult` | PASS / FAIL / INCONCLUSIVE par gate |

## 6. Identité et provenance des données (C02)

C02 exige sans présumer de format de stockage :

- `snapshot_id` : identifiant unique
- `fingerprint` : empreinte cryptographique du contenu (ex. SHA-256)
- `as_of` : date/heure de figement
- `provenance` : source logique (nom, pas vendor figé), fenêtre temporelle, univers
- `adjustments` : liste documentée (splits, dividendes, etc.)
- `availability_cutoff` : dernière information incluse — **critique pour I3**

Les besoins auxquels une future source devra répondre :

1. Horodatage cohérent UTC.
2. Traçabilité des corporate actions appliquées.
3. Reproductibilité via fingerprint.
4. Séparation train/validation/test sans fuite.

Le choix concret (CSV, Parquet, API) est **différé** — voir DR-001 pour le langage d'implémentation seulement.

## 7. Protocole de reproductibilité

### 7.1 Avant exécution

1. Rédiger `hypothesis` et `success_criteria` dans C01.
2. Référencer `dataset_snapshot_id` + fingerprint C02.
3. Lister les baselines obligatoires.
4. Déclarer les gates et seuils (PASS/FAIL/INCONCLUSIVE).
5. Enregistrer les Contract Versions (C01–C05).

### 7.2 Exécution

1. Générer un `experiment_run_id` unique.
2. Persister les artefacts listés dans C01 (`artifacts` manifest).
3. Ne pas modifier le DatasetSnapshot en cours de run.

### 7.3 Après exécution

1. Évaluer chaque gate → `GateResult`.
2. Produire `PromotionRecord` (scientifique / opérationnelle séparés).
3. Archiver empreinte code (`implementation_version` + git commit).

### 7.4 Reconstruction

Un `DecisionTrace` (P0 : structure seulement) lie :

```text
experiment_run_id
  → dataset_snapshot (id, fingerprint)
  → market_state (id, as_of, feature_refs)
  → strategy_signals[] (id, strategy_id, raw_signal)
  → risk_decision (verdict, constraints_applied, final_exposure)
```

## 8. Anti look-ahead et fuite d'information

| Règle | Mécanisme |
|-------|-----------|
| Cutoff temporel | `MarketState.as_of` ≤ toute feature utilisée |
| Snapshot immuable | C02 fingerprint vérifié au chargement |
| Split explicite | C01 déclare `data_splits` (train/val/test dates) |
| Paramètres | Sélection hyperparamètres sur train/val uniquement |
| Survivorship | Documenté dans C02.provenance ; biais signalé si présent |

Tests : `tests/invariants/test_temporal.py`.

## 9. Socle opérationnel vs branches R&D

| Zone | Contenu P0 | Phases |
|------|------------|--------|
| **Socle opérationnel** | Contrats, invariants, pipeline reproductible, géométrie classique (future) | P0–P8 |
| **Branche p-adique** | Slot `experimental_engines.p_adic` dans architecture ; pas d'impl | R1 |
| **Branche dynamique** | Slot `experimental_engines.dynamics` ; pas d'impl | R2 |

Les moteurs expérimentaux consomment les mêmes C02/C03 et produisent des artefacts C01.
Leur promotion suit la chaîne § promotion_chain.md.

## 10. Baselines obligatoires

Voir [mandatory_baselines.md](../../specs/baselines/mandatory_baselines.md).

Minimum P0 (déclaratif) :

- **B0 — Naive neighbor** : voisinage aléatoire / uniforme (contrôle négatif).
- **B1 — Buy-and-hold** : référence passive (future validation économique).
- **B2 — Rolling mean / z-score** : référence statistique simple.

P0 ne les **exécute** pas ; il les **impose** comme contrat méthodologique.

## 11. Métriques et artefacts d'expérience

### Métriques (déclarées dans C01)

| Catégorie | Exemples | Phase |
|-----------|----------|-------|
| Voisinage | homogénéité distribution future, stabilité temporelle | P1 / SCI |
| Prédictive | calibration, log-loss, hit rate OOS | PRED |
| Économique | Sharpe net, turnover, slippage | ECON |
| Risque | drawdown, VaR diagnostic | P3+ |

### Artefacts obligatoires

- `metrics.json` (ou équivalent structuré)
- `gate_results.json`
- `config.yaml` (configuration figée du run)
- Référence au git commit et implementation_version

## 12. Gates PASS / FAIL / INCONCLUSIVE

Aligné sur [closure_gates.md](../governance/closure_gates.md) et [promotion_chain.md](../governance/promotion_chain.md).

Chaque expérience C01 contient une section `gates[]` :

```yaml
gates:
  - id: SCI-001
    description: "Voisinages plus homogènes que B0"
    verdict: PASS | FAIL | INCONCLUSIVE
    evidence_ref: "artifacts/metrics.json#neighbor_homogeneity"
```

## 13. Politique de versionnement des expériences

- Format ID expérience : `I{nn}` (investigation) ou `E-{uuid}` (run ponctuel).
- Un changement de protocole → **nouvelle** Experiment ID ou version C01.
- Les résultats sont immuables ; une réplication est un nouveau `experiment_run_id`.
- Promotion scientifique / opérationnelle enregistrée dans `PromotionRecord`.

## 14. Critères de clôture P0

| Gate | Statut attendu |
|------|----------------|
| P0-SPEC | PASS |
| P0-CONTRACTS | PASS |
| P0-INVARIANTS | PASS |
| P0-REPRO | PASS |
| P0-NO-TRADE | PASS |
| P0-RISK-SOV | PASS |
| P0-NO-STRATEGY | PASS |
| P0-NO-BROKER | PASS |

## 15. Références

- Rapport fondateur v0.1 (vision projet)
- [QDP v0.1](../governance/qdp_v0_1.md)
- Contrats C01–C05
- [DR-001](../adr/DR-001-python-implementation-language.md)

---

**STOP P0** — P1 (géométrie classique) ne démarre qu'après rapport de clôture et GO explicite.
