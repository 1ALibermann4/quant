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
- **DR-007 ACCEPTED** — deux classes exclusives : `EXPLORATORY` (`UNQUALIFIED`, amont de C02 ; aucun DATA-PASS / SCI-PASS / SCI-FAIL / PRED / ECON / promotion) et `CONFIRMATORY` (C02 + DR-003 D-1 ACCEPTED + DR-005 ACCEPTED). `intended_use: technical` reste sur la voie qualifiée. Un résultat exploratoire, positif ou négatif, n'est pas un verdict SCI.
- **Ne pas implémenter** I01 confirmatoire avant DATA-REQ-I01 + `DR-003 D-1 ACCEPTED ∧ DR-005 ACCEPTED`. I01 exploratoire (I01-E01) : source sandbox `SPY / yfinance 1.6.0 / daily` — **EXPLORATORY ONLY / UNQUALIFIED** ([DR-008](docs/adr/DR-008-i01-e01-exploratory-source.md)). Pas d'acquisition payante ; pas de qualification C02 ; yfinance n'est pas admissible au confirmatoire (DR-003 L-13 inchangé).
- **Ne pas choisir d'API confirmatoire** avant que les besoins data soient dérivés du protocole.

## Protocol

**Quant Development Protocol v0.1 (QDP v0.1)**
