# DR-006 — Parsabilité des fichiers YAML normatifs (contrôle dev/CI)

> **Identifier :** DR-006
> **Status :** ACCEPTED
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1
> **Date :** 2026-09-23
> **Numérotation :** DR-005 est réservé à la charte d'investigation calendrier (non ouverte).

## Context

Le HAT #1 de C02 v1.1 (`docs/validation/C02-v1.1-HAT.md`, commit `3c684b7`) et CA-01
(constat CA-F2, `docs/validation/C02-v1.1-CA-01-report.md`) ont montré qu'un contrat
YAML normatif pouvait être invalide ou mal interprété (listes contenant « : », valeurs
tronquées par ` #`) sans qu'aucun contrôle automatisé ne le détecte : PyYAML n'était
pas une dépendance du dépôt.

## Decision

1. **Règle.** Tout fichier `.yaml` / `.yml` normatif versionné sous `specs/`, `research/`
   ou `docs/` doit être syntaxiquement parsable par le validateur retenu.
2. **Validateur retenu.** PyYAML (`yaml.SafeLoader`) augmenté d'un refus des clés
   dupliquées. Le document de premier niveau doit être un mapping.
3. **Portée.** Contrôle de **développement / CI** uniquement :
   `tests/specs/test_yaml_parsable.py`. PyYAML figure dans le groupe optionnel `dev`
   de `pyproject.toml` et **n'entre pas** dans les dépendances runtime de `quant`.
4. **Aucun chargement dynamique.** Aucun modèle C01–C05 n'est construit depuis le YAML ;
   les contrats YAML restent des spécifications, les modèles Python restent
   l'implémentation. Le test vérifie que `src/` n'importe pas `yaml`.

## Constraints

- La parsabilité ne vaut pas validation sémantique : la cohérence contrat ↔ code reste
  établie par les tests de contrat et les HAT.
- Ajouter un validateur de schéma YAML (JSON Schema, etc.) exigerait un DR distinct.

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| PyYAML en dépendance runtime | Rejeté — aucun besoin runtime ; élargit la surface |
| `ruamel.yaml` | Non retenu — plus lourd, aucun besoin YAML 1.2 identifié |
| Test ignoré (`importorskip`) si PyYAML absent | Rejeté — masquerait silencieusement le contrôle |

## Consequences

- `pip install -e '.[dev]'` installe PyYAML ; l'absence de PyYAML fait échouer la collecte
  du test (visible), sans affecter le runtime.
- Toute future spécification YAML invalide fait échouer la suite.

## Status

ACCEPTED — contrôle dev/CI, sans dépendance runtime.
