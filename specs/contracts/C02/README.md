# C02 — Data Provenance & Dataset Snapshot

| Version | Fichier | Statut | Notes |
|---------|---------|--------|-------|
| 1.0 | [C02_v1.0.yaml](C02_v1.0.yaml) | Remplacée par 1.1 (objets 1.0 toujours valides) | Publiée en P0. Texte de précondition `availability_cutoff` erroné : voir erratum E-01 |
| **1.1** | [C02_v1.1.yaml](C02_v1.1.yaml) | **Courante — CLOSED / ACCEPTED** | Rétrocompatible (voir `compatibility.behaviour_changes`). Résout DATA-GAP-01 et DATA-GAP-02. Baseline de sourcing ; n'autorise pas l'acquisition |

## Historique de validation de la v1.1

| Étape | Document | Verdict |
|-------|----------|---------|
| Validation automatisée | [C02-v1.1-validation-report.md](../../../docs/validation/C02-v1.1-validation-report.md) (`97cb50b`) | PASS |
| HAT #1 | [C02-v1.1-HAT.md](../../../docs/validation/C02-v1.1-HAT.md) (`3c684b7`) | FAIL |
| Action corrective CA-01 | [C02-v1.1-CA-01-report.md](../../../docs/validation/C02-v1.1-CA-01-report.md) | voir rapport |
| HAT #2 | [C02-v1.1-HAT-2.md](../../../docs/validation/C02-v1.1-HAT-2.md) | FAIL |
| Action corrective CA-02 | [C02-v1.1-CA-02-report.md](../../../docs/validation/C02-v1.1-CA-02-report.md) | PASS (ne clôture pas) |
| HAT #3 | [C02-v1.1-HAT-3.md](../../../docs/validation/C02-v1.1-HAT-3.md) | FAIL |
| Action corrective CA-03 | [C02-v1.1-CA-03-report.md](../../../docs/validation/C02-v1.1-CA-03-report.md) | PASS (ne clôture pas) |
| HAT #4 | [C02-v1.1-HAT-4.md](../../../docs/validation/C02-v1.1-HAT-4.md) | FAIL |
| Action corrective CA-04 | [C02-v1.1-CA-04-report.md](../../../docs/validation/C02-v1.1-CA-04-report.md) | PASS (ne clôture pas) |
| HAT #5 | [C02-v1.1-HAT-5.md](../../../docs/validation/C02-v1.1-HAT-5.md) | PASS |
| Acceptation humaine / clôture | [C02-v1.1-CLOSURE.md](../../../docs/validation/C02-v1.1-CLOSURE.md) | **CLOSED / ACCEPTED** |

## Profils de validation

| Profil | Fichier | Autorité |
|--------|---------|----------|
| C02-I01 v1.0 | [profiles/C02-I01_v1.0.yaml](profiles/C02-I01_v1.0.yaml) | `research/I01/DATA-REQ-I01.md` v0.1 |

## Errata

| ID | Version affectée | Correction |
|----|------------------|------------|
| E-01 | 1.0 — précondition « `availability_cutoff <= as_of` is invalid → reject » | La règle correcte est `availability_cutoff <= as_of` **requis** ; seul `availability_cutoff > as_of` est rejeté. Le code et les tests l'appliquent depuis P0 : ce n'est pas une nouvelle sémantique |

Les fichiers publiés ne sont pas réécrits ; les corrections passent par les errata de la
version suivante.

## Décision

[DR-004 — C02 Data Provenance architecture](../../../docs/adr/DR-004-c02-data-provenance-architecture.md)

Clôture v1.1 : [C02-v1.1-CLOSURE.md](../../../docs/validation/C02-v1.1-CLOSURE.md) — acceptation humaine PASS. Baseline autorisée pour ouvrir séparément DR-003 v1.1 et DR-005 ; l'acquisition reste interdite tant que ces deux décisions ne sont pas ACCEPTED.
