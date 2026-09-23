# I01 — Classical Geometric Neighborhood

> **Identifier :** I01
> **Status :** OPEN — protocol draft
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Phase :** P1
> **Baseline commit :** `a4c55b9`

---

## Question centrale

> **H-I01 :** une proximité géométrique entre états de marché observable contient-elle
> de l'information sur la distribution des futurs — au-delà d'un contrôle naïf (B0) ?

Formulation formelle : [hypothesis.md](hypothesis.md)

## Contexte

Première expérience SCI du projet. Aucune stratégie, aucun P&L, aucune API de marché
tant que le protocole n'est pas revu et que les besoins data ne sont pas dérivés.

```text
P0 (contrats, invariants) ──► I01 (SCI voisinage) ──► I02+ / PRED (si SCI PASS)
```

## Périmètre

| Inclus | Exclu |
|--------|-------|
| Définition mathématique de X_t, Y_t, d, N_k | Implémentation pipeline |
| Protocole statistique et gates SCI | Choix API / broker |
| Baseline B0 obligatoire | Baselines B1–B3 (ECON) |
| Besoins data minimaux (spec) | Téléchargement de données |
| Contrôles anti-fuite | Features p-adiques / chaos |

## Structure

```text
I01/
├── README.md              ← ce document
├── hypothesis.md          H₀, H₁, définitions mathématiques
├── protocol.md            Protocole expérimental complet
├── configuration.yaml     Paramètres figés (sans source data)
├── evaluation_closure.md  (à créer post-exécution)
└── experiments/           (vide — interdit avant revue protocole)
```

## Documents normatifs I01

1. [hypothesis.md](hypothesis.md) — hypothèses et objets mathématiques
2. [protocol.md](protocol.md) — voisinage, métriques, tests, gates, anti-fuite, besoins data
3. [configuration.yaml](configuration.yaml) — paramètres numériques

## Gates (aperçu)

| Gate | Description |
|------|-------------|
| SCI-000 | Baseline B0 exécutée |
| SCI-001 | Homogénéité future : géométrique > B0 (primaire) |
| SCI-002 | Effet non concentré sur une sous-période |
| SCI-003 | Robustesse sensibilité (W, k, h) |
| SCI-004 | Contrôles anti-fuite satisfaits |

Détail : [protocol.md §8](protocol.md)

## Ordre de travail obligatoire

```text
1. Revue protocole I01 (cohérence, ambiguïtés)
2. Dérivation besoins data → document DATA-REQ-I01
3. ADR source de données (si applicable)
4. Implémentation pipeline (experiments/)
5. Exécution + evaluation_closure.md
```

## Références

- [P1-cadrage.md](../../docs/foundation/P1-cadrage.md)
- [mandatory_baselines.md](../../specs/baselines/mandatory_baselines.md) — B0
- [promotion_chain.md](../../docs/governance/promotion_chain.md)
