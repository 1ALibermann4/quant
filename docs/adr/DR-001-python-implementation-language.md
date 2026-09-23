# DR-001 — Python comme langage d'implémentation P0

> **Identifier :** DR-001
> **Status :** ACCEPTED
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1

## Context

P0 requiert des contrats typés, des tests d'invariants et une ossature extensible.
Aucun langage n'était figé dans le rapport fondateur. Python est un candidat naturel
pour la R&D quantitative, mais reste une décision technique distincte des contrats.

## Decision

Utiliser **Python ≥ 3.11** avec **Pydantic v2** pour matérialiser les contrats C01–C05
en P0.

## Constraints

- Les contrats normatifs restent définis dans `specs/contracts/*.yaml` ; le code Python
  est une implémentation référence, pas l'autorité silencieuse.
- Aucune dépendance liée à une source de données, un broker ou un format de persistance.
- `implementation_version` (0.1.0) est indépendant des `contract_version`.

## Authorities consulted

- P0-specification.md
- versioning_axes.md
- Revue de cohérence P0

## Evidence

- Écosystème mature pour prototypage quantitatif et validation statistique future.
- Pydantic permet validation stricte alignée sur les invariants I1–I4.
- Alignement partiel avec la stack Argus (cpu-python) sans importer ADP tel quel.

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| Rust | Performance future possible ; coût R&D P0 plus élevé |
| TypeScript | Moins naturel pour pipeline numérique / stats |
| Contrats YAML seuls sans code | Insuffisant pour tests d'invariants exécutables |

## Rejected alternatives

- **Figer yfinance / Polygon / Parquet** — rejeté ; besoins data définis dans C02, choix différé.
- **Monorepo multi-langage P0** — rejeté ; complexité sans justification P0.

## Consequences

- `pyproject.toml` + `src/quant/` comme layout minimal.
- Tests via pytest.
- Une future implémentation alternative (ex. Rust) devra prouver conformité aux contrats YAML.

## Deferred items

- Outil de génération code ↔ YAML (non requis P0).
- Lockfile production / CI matrix.

## Status

ACCEPTED — P0 foundation only.
