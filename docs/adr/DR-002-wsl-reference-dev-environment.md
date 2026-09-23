# DR-002 — WSL Ubuntu comme environnement de référence dev/test

> **Identifier :** DR-002
> **Status :** ACCEPTED
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1

## Context

P0-HAT a validé l'exécutabilité du squelette via WSL Ubuntu 24.04 (Python 3.12.3).
Python natif Windows n'est pas fiable sur la machine de développement actuelle.

## Decision

Adopter **WSL Ubuntu 24.04** comme environnement de **référence** pour le développement
et l'exécution des tests (`pytest`, pipelines research) jusqu'à décision contraire.

## Constraints

- Ce choix ne fige **pas** l'environnement d'exploitation future (paper/live, cloud, CI).
- Les artefacts doivent rester reproductibles hors WSL si un ADR ultérieur le exige.
- `.venv/` reste local et gitignored.

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| Réparer Python Windows natif | Possible ultérieurement ; non bloquant |
| Devcontainer Docker | Différé — complexité non justifiée en P1 |
| CI cloud | Différé — après premier pipeline I01 |

## Rejected alternatives

- Imposer WSL comme **runtime de production** — rejeté ; hors scope.

## Consequences

- Documentation et scripts d'exemple ciblent WSL bash.
- P1/I01 et tests s'exécutent via `source .venv/bin/activate` sous WSL.

## Status

ACCEPTED — référence dev/test uniquement.
