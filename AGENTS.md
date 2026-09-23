# Quant — instructions pour assistants

Lire ce fichier avant de modifier le dépôt.

## Ordre de lecture

1. [docs/governance/README.md](docs/governance/README.md) — gouvernance QDP v0.1
2. [docs/governance/qdp_v0_1.md](docs/governance/qdp_v0_1.md) — protocole
3. [docs/foundation/P0-specification.md](docs/foundation/P0-specification.md) — fondation
4. [docs/governance/promotion_chain.md](docs/governance/promotion_chain.md) — promotion scientifique vs opérationnelle
5. Contrats `specs/contracts/C01–C05`

## Règles rapides

- L'historique de chat **n'est pas** une autorité.
- Classifier → identifier l'autorité → définir les gates → exécuter jusqu'à **closure**.
- **Risk Engine souverain** — ne jamais contourner C05.
- **NO_TRADE** est un résultat de première classe.
- Validation scientifique ≠ promotion opérationnelle.
- Ne pas implémenter de stratégie réelle avant **P2**.
- Ne pas connecter de broker avant **P6**.
- Toute décision technique figée → **Decision Record** dans `docs/adr/`.
- P0 est **clos** (HAT PASS, commit `a4c55b9`).
- **P1 / I01** est ouvert — protocole SCI voisinage géométrique.
- **Ne pas implémenter** I01 avant revue protocole + DATA-REQ-I01 + ADR data.
- **Ne pas choisir d'API** avant que les besoins data soient dérivés du protocole.

## Protocol

**Quant Development Protocol v0.1 (QDP v0.1)**
