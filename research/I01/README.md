# I01 — Classical Geometric Neighborhood

> **Identifier :** I01
> **Status :** ACCEPTED — protocol v0.2 (post review)
> **Exploratory sequence :** COMPLETE @ `4a920c3` — hypothèse originale **non recommandée** à la confirmation ; phénomène conditionnel au régime *identifié*, non validé. Pas un SCI-FAIL. Synthèse : [I01-exploratory-synthesis.md](I01-exploratory-synthesis.md)
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
├── README.md
├── I01-exploratory-synthesis.md   clôture E01–E04 (pas un SCI)
├── hypothesis.md
├── protocol.md
├── configuration.yaml
├── experiments/E01/       I01-E01 exploratoire UNQUALIFIED (pas un SCI)
├── experiments/E02/       I01-E02 diagnostics exploratoires (paramètres figés)
├── experiments/E03/       I01-E03 mécanisme volatilité (contrôle ≠ B0)
├── experiments/E04/       I01-E04 anatomie conditionnelle de D_t (blocs préfixés)
```

Séquence exploratoire E01–E04 **CLOSE**. I01 confirmatoire **non recommandé**
tel quel (pas un SCI-FAIL). Pas d'ouverture DR-003 / DR-005 pour I01.
Pas d'E05. Toute poursuite = nouvelle investigation, pas encore ouverte.

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
