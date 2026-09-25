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
- **P1 / I01** : protocole SCI v0.2 toujours le texte pré-enregistré ; la séquence exploratoire E01–E04 est **CLOSE** (voir [I01-exploratory-synthesis.md](research/I01/I01-exploratory-synthesis.md)).
- **DR-007 ACCEPTED** — deux classes exclusives : `EXPLORATORY` (`UNQUALIFIED`, amont de C02 ; aucun DATA-PASS / SCI-PASS / SCI-FAIL / PRED / ECON / promotion) et `CONFIRMATORY` (C02 + DR-003 D-1 ACCEPTED + DR-005 ACCEPTED). `intended_use: technical` reste sur la voie qualifiée. Un résultat exploratoire, positif ou négatif, n'est pas un verdict SCI.
- **I01 exploratoire CLOSE** — verdict : *ORIGINAL HYPOTHESIS NOT RECOMMENDED FOR CONFIRMATION; REGIME-CONDITIONAL PHENOMENON IDENTIFIED*. Pas un SCI-FAIL (DR-007). **Ne pas** confirmer I01 tel quel. **Ne pas** ouvrir DR-003 / DR-005 pour I01. **Pas d'E05.**
- **I02 = OPEN** (décision humaine ; commit d'ouverture antérieur à toute implémentation). Design core **R2** figé ; contrat [I02-preregistration.md](research/I02/I02-preregistration.md) (**P2**). Historique de design : [I02-hypothesis-draft.md](research/I02/I02-hypothesis-draft.md). **Pas encore** : HAT PASS, run exploratoire, evidence SCI, qualification C02. Cycle : OPEN → implementation → HAT → exploratory execution. Confirmatoire bloqué séparément (C02 + DR-003 D-1 + DR-005 + holdout). Les observations I01 ne prouvent pas H1-I02. Source sandbox I01 E01–E04 : `SPY / yfinance 1.6.0 / daily` — UNQUALIFIED ([DR-008](docs/adr/DR-008-i01-e01-exploratory-source.md)). Pas d'acquisition payante ; yfinance n'est pas admissible au confirmatoire (DR-003 L-13 inchangé). Ne pas modifier le design core sans change control (prereg §8).
- **Ne pas choisir d'API confirmatoire** avant que les besoins data soient dérivés du protocole.

## Protocol

**Quant Development Protocol v0.1 (QDP v0.1)**
