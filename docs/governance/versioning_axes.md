# Axes de versionnement indépendants

> **Identifier :** VERSION-AXES-v0.1
> **Status :** ACCEPTED
> **Authority class :** GOVERNANCE
> **Protocol :** QDP v0.1

Inspiré de la séparation ADP/Argus : éviter qu'un bump de package implique
silencieusement un changement de garantie contractuelle.

## Axes

| Axe | Ce qu'il versionne | Exemple | Immuable après publish ? |
|-----|-------------------|---------|--------------------------|
| **Contract Version** | Garanties d'un contrat Cxx | C01 v1.0 | Oui — nouveau minor/major pour changement de garantie |
| **Implementation Version** | État du code implémentant les contrats | quant 0.1.0 | Tag git ; évolution continue |
| **Capability Manifest** | Combinaison promue de contrats + impl pour un usage | manifest_v1.0.yaml | Oui après promotion — nouveau manifest si changement |
| **Experiment ID** | Investigation reproductible | I01, E-2025-001 | Immuable — nouvelle expérience si protocole change |
| **DatasetSnapshot fingerprint** | Empreinte des données figées | sha256:… | Immuable |
| **QDP Protocol** | Processus de gouvernance | QDP v0.1 | Prospective |

## Relations

```text
QDP v0.1
  └── Contract C01 v1.0 ──┐
  └── Contract C02 v1.0 ──┼── Capability Manifest v1.0 (post-promotion)
  └── …                   │
                          └── Implementation quant 0.x.y
```

## Règles

1. Changer une **garantie** d'un contrat → nouvelle **Contract Version** + mise à jour des tests d'invariants.
2. Changer l'implémentation sans changer les garanties → **Implementation Version** uniquement.
3. Promouvoir une combinaison contrats+impl → nouveau **Capability Manifest** figé.
4. Chaque **Experiment** référence explicitement les Contract Versions et DatasetSnapshot utilisés.

## Champs normatifs dans les contrats

Tout objet contractuel porte au minimum :

- `contract_id` (ex. C01)
- `contract_version` (semver du contrat)
- `implementation_version` (optionnel, pour traçabilité runtime)
- `created_at` / horodatage ISO 8601 UTC

Le **Capability Manifest** (futur, post-P0) listera les paires `(contract_id, contract_version, implementation_id)`.
