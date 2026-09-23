# Cadrage P1 — Géométrie classique

> **Identifier :** P1-CADRAGE-v0.1
> **Status :** OPEN
> **Authority class :** FOUNDATION
> **Protocol :** QDP v0.1
> **Baseline commit :** `a4c55b9`

---

## 1. Ouverture officielle

**P1 — Géométrie classique** est ouvert à partir du commit `a4c55b9` (P0 clôturé, HAT PASS).

Première investigation : **[I01 — Classical Geometric Neighborhood](../../research/I01/README.md)**.

## 2. Objectif de phase

Démontrer — ou invalider — qu'une **notion de proximité géométrique** entre états de marché
contient de l'**information sur le futur**, avant toute construction de stratégie rentable.

P1 ne cherche **pas** à gagner de l'argent. P1 cherche à répondre à une question SCI :

> Les voisins géométriques d'un état présentent-ils des futurs statistiquement plus homogènes
> qu'un contrôle naïf (B0) ?

## 3. Non-objectifs P1 (phase)

- Implémenter trend following, mean reversion, pairs ou allocation.
- Optimiser un portefeuille ou un P&L.
- Choisir une API de marché **avant** que le protocole I01 ne fixe les besoins data.
- Brancher p-adique / dynamique (R1/R2).
- Paper trading ou connexion broker.

## 4. Chaîne de promotion applicable

I01 relève exclusivement de la gate **SCI-*** :

```text
I01 : Hypothèse H₀/H₁ → protocole figé → exécution → SCI-*
                              ↓
                    (si PASS) → I02+ / PRED (hors P1 initial)
                    (si FAIL) → clôture ou reformulation
                    (si INCONCLUSIVE) → données/protocole insuffisants
```

Une SCI PASS **n'autorise pas** de trading. Elle autorise seulement à poser la question PRED :
*« cette information se généralise-t-elle hors échantillon ? »*

## 5. Livrables P1 attendus (ordre)

| Étape | Livrable | Statut |
|-------|----------|--------|
| 1 | Cadrage P1 (ce document) | OPEN |
| 2 | I01 hypothesis + protocol + configuration | OPEN |
| 3 | Revue de cohérence I01 | À faire |
| 4 | Spécification des besoins data (dérivée du protocole) | À faire post-revue |
| 5 | ADR source de données (si choix figé) | À faire post-besoins |
| 6 | Implémentation pipeline I01 | **Interdit avant 3–5** |
| 7 | Exécution + gate SCI | **Interdit avant 6** |

## 6. Environnement de référence (dev/test)

WSL Ubuntu 24.04 + Python 3.12.3 + `.venv` local — validé par [P0-HAT.md](P0-HAT.md).

Enregistré comme **référence de développement et de test**, pas comme environnement
d'exploitation future. Voir [DR-002](../adr/DR-002-wsl-reference-dev-environment.md).

## 7. Investigation I01 — résumé

| Élément | Référence |
|---------|-----------|
| Question | [I01/hypothesis.md](../../research/I01/hypothesis.md) |
| Protocole complet | [I01/protocol.md](../../research/I01/protocol.md) |
| Paramètres figés | [I01/configuration.yaml](../../research/I01/configuration.yaml) |
| Baseline obligatoire | **B0** (voisinage aléatoire) |

## 8. Critère de sortie P1 (initial)

P1 phase initiale = **I01 clôturé** avec verdict SCI explicite (PASS / FAIL / INCONCLUSIVE)
et dossier de preuve C01-compatible.

Extensions ultérieures (features enrichies, multi-actifs, métriques alternatives) =
investigations I02, I03… — pas scope de cette ouverture.

---

**STOP implémentation** — prochaine action : revue du protocole I01, puis dérivation des besoins data.
