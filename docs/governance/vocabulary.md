# Vocabulaire canonique

> **Identifier :** VOCAB-v0.1
> **Status :** ACCEPTED
> **Authority class :** GOVERNANCE
> **Protocol :** QDP v0.1

Termes normatifs du domaine. Les contrats P0 (C01–C05) s'appuient sur ce vocabulaire.

## Entités principales

| Terme | Définition |
|-------|------------|
| **Observation** | Mesure brute ou dérivée à un instant ou sur une fenêtre, avant interprétation stratégique. |
| **DatasetSnapshot** | Empreinte versionnée d'un ensemble de données figé pour une expérience, avec provenance. |
| **Feature** | Variable dérivée d'observations, comparable entre actifs et périodes. |
| **Representation** | Choix de features, métriques et espace d'état pour décrire le marché. |
| **MarketState** | Vecteur d'état contextualisé à l'instant *t*, avec incertitude et métadonnées de régime. |
| **StrategySignal** | Proposition normalisée d'une stratégie : direction, force, confiance, preuves, abstention. |
| **Grade** | Score décomposable d'adéquation stratégie ↔ contexte ; ne vaut pas autorisation de risque. |
| **RiskDecision** | Verdict souverain : AUTHORISE, REDUCE, DELAY, VETO ou NO_TRADE. |
| **Experiment** | Unité reproductible d'investigation : hypothèse, protocole, données, métriques, verdict. |
| **Baseline** | Référence simple obligatoire contre laquelle toute innovation est comparée. |
| **NO_TRADE** | Décision explicite de ne pas exposer de capital ; résultat de première classe. |
| **Gate** | Critère PASS/FAIL/INCONCLUSIVE évalué avant promotion ou clôture. |
| **Artefact** | Sortie persistante d'une expérience (métriques, figures, logs, snapshots). |

## Verbes normatifs

| Verbe | Signification |
|-------|---------------|
| **Propose** | Une stratégie émet un StrategySignal ; elle ne fixe pas la taille finale. |
| **Grade** | L'orchestrateur estime la pertinence conditionnelle ; sans autorité sur le risque. |
| **Authorise / Veto** | Le Risk Engine tranche ; ses invariants ne sont pas contournables. |
| **Promote (scientifique)** | Une brique R&D rejoint le socle expérimental documenté. |
| **Promote (opérationnelle)** | Une brique rejoint le pipeline paper/live après gates économiques. |
| **Abstain** | Refus explicite de proposer une opération, avec `abstain_reason`. |

## Branches R&D (hors socle opérationnel initial)

| Branche | Objet | Statut P0 |
|---------|-------|-----------|
| **Classique** | Géométrie euclidienne, statistiques, voisinages standards | Socle cible P1 |
| **p-adique / ultramétrique** | Encodages et distances alternatives | Frontière architecturale uniquement |
| **Dynamique / chaos** | Divergence, horizon de prévisibilité, régimes | Frontière architecturale uniquement |

## Anti-patterns terminologiques

- Ne pas confondre **confidence** (score modèle) et **autorisation de risque**.
- Ne pas appeler « prédiction » une simple **description** de l'état passé/présent.
- Ne pas traiter un backtest in-sample comme **validation hors échantillon**.
- Ne pas qualifier « robuste » un résultat sans baseline et sans protocole documenté.
