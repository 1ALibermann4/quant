# Gouvernance — Quant Development Protocol

> **Protocol :** QDP v0.1
> **Authority class :** GOVERNANCE

Ce dossier définit comment le projet quantitatif est conçu, validé et promu.

## Ordre de lecture

1. [qdp_v0_1.md](qdp_v0_1.md) — protocole de développement
2. [vocabulary.md](vocabulary.md) — vocabulaire canonique
3. [versioning_axes.md](versioning_axes.md) — axes de versionnement indépendants
4. [promotion_chain.md](promotion_chain.md) — chaîne scientifique vs opérationnelle
5. [closure_gates.md](closure_gates.md) — gates PASS / FAIL / INCONCLUSIVE
6. [../foundation/P0-specification.md](../foundation/P0-specification.md) — fondation P0

## Principes non négociables

- Le **Risk Engine** est souverain : il peut refuser toute proposition.
- **NO_TRADE** est un résultat de première classe, pas un échec implicite.
- Une validation **scientifique** ne confère pas automatiquement une promotion **opérationnelle**.
- Les tests prouvent ; ils ne définissent pas silencieusement le comportement normatif.
- Aucun choix technique externe (source de données, broker, format de persistance) n'est figé sans ADR.
