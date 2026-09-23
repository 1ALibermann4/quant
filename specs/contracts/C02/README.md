# C02 — Data Provenance & Dataset Snapshot

| Version | Fichier | Statut | Notes |
|---------|---------|--------|-------|
| 1.0 | [C02_v1.0.yaml](C02_v1.0.yaml) | Remplacée par 1.1 (objets 1.0 toujours valides) | Publiée en P0. Texte de précondition `availability_cutoff` erroné : voir erratum E-01 |
| **1.1** | [C02_v1.1.yaml](C02_v1.1.yaml) | **Courante** | Rétrocompatible. Résout DATA-GAP-01 et DATA-GAP-02 |

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
