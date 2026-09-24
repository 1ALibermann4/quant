# DR-007 — Politique de données exploratoires vs confirmatoires

> **Identifier :** DR-007
> **Status :** ACCEPTED
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1
> **Date :** 2026-09-24
> **Human acceptance :** PASS — 2026-09-24
> **Baseline :** C02 v1.1 CLOSED `1cda21f` · DR-003 D-1 INCONCLUSIVE · DR-005 OPEN
> **Relève :** QDP v0.1 ; [promotion_chain.md](../governance/promotion_chain.md) ;
> [DATA-REQ-I01.md](../../research/I01/DATA-REQ-I01.md) §4.3 / §12 ;
> C02 v1.1 (`intended_use`) ; C01 (`experiment` type `exploratory`)

Cette pièce **définit une politique**. Elle n'autorise aucune acquisition, ne choisit
aucune API, n'envoie aucun mail, n'implémente pas I01 et ne modifie ni DR-003 ni DR-005.

## Context

La gouvernance construite jusqu'ici (C02, DATA-REQ, DR-003, DR-005) est faite pour
**valider** un résultat admissible à la promotion. Elle a commencé à être utilisée
comme prérequis pour simplement **explorer** I01 (pipeline, calculs, voisinages,
performance). Ce sont deux besoins distincts.

Les bloquer l'un par l'autre produit deux échecs symétriques :

- sans séparation, on ne peut pas développer I01 tant que DR-003 et DR-005 ne sont
  pas ACCEPTED ;
- sans séparation, on serait tenté d'assouplir DR-003 / DR-005 « pour avancer » —
  ce que cette pièce refuse.

DATA-REQ §4.3 connaît déjà `intended_use ∈ {technical, confirmatory}`. Ce n'est
**pas** l'axe introduit ici. `technical` décrit la **profondeur** d'un snapshot
**qualifié** C02 (SCI plafonné à INCONCLUSIVE). DR-007 porte sur la **classe** du
dataset : qualifié ou non.

## Decision

Introduire deux classes de données, exclusives, pour toute expérimentation I01
(et, par défaut, pour les investigations SCI suivantes).

```text
                    I01
                     │
              ┌──────┴──────┐
              │             │
        EXPLORATORY     CONFIRMATORY
              │             │
      données pratiques    données qualifiées
      et traçables         C02 + DR-003 + DR-005
              │             │
      aucun SCI-PASS       résultat admissible
      aucun PRED/ECON      à la promotion
              │
              ▼
      « Cette piste mérite-t-elle
        qu'on continue ? »
```

### D-1 — Classe `EXPLORATORY`

Autorise uniquement : développement du pipeline, debug, visualisation, mesures de
faisabilité et de performance, analyses préliminaires.

Un dataset de cette classe **doit** porter un statut non qualifié, visible et
non ambigu (libellé normatif : `UNQUALIFIED` / `EXPLORATORY`). Il ne peut pas se
présenter comme un `DatasetSnapshot` C02 éligible à un gate DATA.

Interdit, sur cette classe :

| Interdiction | Détail |
|--------------|--------|
| `DATA-PASS` | Le gate DATA-I01-* ne s'évalue pas. Absence de PASS, pas un FAIL déguisé en verdict |
| `SCI-PASS` | Y compris SCI-001. Un chiffre exploratoire n'est pas un verdict |
| `SCI-FAIL` | Un résultat négatif exploratoire n'est **pas** un FAIL SCI d'I01 |
| `PRED-*` / `ECON-*` | Hors chaîne de promotion |
| Promotion scientifique ou opérationnelle | [promotion_chain.md](../governance/promotion_chain.md) |
| Citation comme validation d'I01 | Rapport, revue, paper, décision de clôture |

Question légitime d'un run exploratoire : *est-ce que cette piste mérite qu'on
continue ?* Réponse possible : oui / non / pas encore — jamais PASS/FAIL SCI.

Symétrie obligatoire (acceptation humaine 2026-09-24) : un FAIL exploratoire ne
devient pas automatiquement un FAIL SCI d'I01, exactement comme un résultat
positif exploratoire ne peut devenir un PASS SCI. L'exploration décide si
l'investigation **mérite une confirmation** ; elle ne rend pas le verdict
scientifique final.

### D-2 — Classe `CONFIRMATORY`

Reste soumise **intégralement** à :

- C02 v1.1 CLOSED / ACCEPTED (forme, empreintes, `MarketCalendarSnapshot`) ;
- DATA-REQ-I01 (y compris `intended_use` `technical` | `confirmatory` et les paliers) ;
- DR-003 D-1 **ACCEPTED** (source de prix) ;
- DR-005 **ACCEPTED** (source de calendrier) ;
- `DR-003 D-1 ACCEPTED ∧ DR-005 ACCEPTED` avant toute acquisition destinée à un
  run confirmatoire.

Aucun assouplissement de critère n'est autorisé par DR-007.

`intended_use: technical` sur un snapshot C02 reste une sous-catégorie de
**CONFIRMATORY** (chemin qualifié, profondeur réduite, SCI plafonné). Ce n'est
pas un dataset `EXPLORATORY`.

### D-3 — Non-mélange

Une conclusion confirmatoire ne peut pas combiner les deux classes.

Interdit notamment :

- un calendrier `EXPLORATORY` + des prix `CONFIRMATORY`, ou l'inverse ;
- un train exploratoire et un test présenté comme confirmatoire ;
- « on a vu le résultat exploratoire, donc le run C02 est un formalisme » ;
- requalifier après coup un artefact `EXPLORATORY` en `CONFIRMATORY`.

Si les deux classes existent dans le dépôt, elles portent des identifiants,
chemins et empreintes disjoints.

### D-4 — Anti-snooping : l'exploration ne réécrit pas l'hypothèse en silence

L'hypothèse confirmatoire I01 v0.2 est déjà figée (`W=20`, `k=50`, `h=10`,
`M=252`, $\tau=20$, endpoint $\mathcal{H}_\text{raw}$, gates SCI-001 / SCI-002 /
SCI-004, DATA-REQ).

Si un run `EXPLORATORY` conduit à vouloir changer $W$, $k$, $h$, la métrique,
les gates, le split, $L$, l'instrument ou la fenêtre :

1. **enregistrer** le motif (ce qui a été vu, sans en faire un verdict) ;
2. **figer** une nouvelle spécification versionnée (hypothèse / protocole /
   DATA-REQ selon le cas) ;
3. **seulement alors** ouvrir un run `CONFIRMATORY` contre cette nouvelle spec.

Choisir $W$, $k$, $h$, $L$ ou la fenêtre *parce que* l'exploration a mieux
marché, puis lancer la confirmation sur la même spécification « ajustée » sans
enregistrement, est du **data snooping**. DR-007 le nomme et l'interdit.

L'exploration peut **informer** une révision. Elle ne peut pas **tenir lieu**
de révision.

### D-5 — DR-003 et DR-005 inchangés

| Pièce | Statut après DR-007 | Effet |
|-------|---------------------|--------|
| DR-003 D-1 | **INCONCLUSIVE** (inchangé) | Questionnaires et scores v1.0 intacts |
| DR-003 v1.1 SEND | **HOLD** — ne pas envoyer | Les paquets restent valides ; l'envoi n'est plus le prochain pas |
| DR-005 | **OPEN**, sélection INCONCLUSIVE (inchangé) | Cadrage et comparaison vague 1 intacts |

DR-007 n'est pas un substitut à DR-003 ou DR-005. Il crée un **amont** sandbox.

### D-6 — Aucune acquisition payante

DR-007 **n'autorise** :

- aucun abonnement ;
- aucun achat de données ;
- aucun essai payant « pour explorer » ;
- aucun téléchargement présenté comme confirmatoire.

Une future source exploratoire, si elle est retenue après acceptation de cette
politique, devra être **gratuite pour l'usage déclaré**, clairement `UNQUALIFIED`,
et faire l'objet d'une décision **séparée**. Cette pièce n'en choisit aucune.

`yfinance` (DR-003 L-13, FAIL PA-14 / interface non officielle) est un *exemple*
de source qui ne pourra **jamais** être confirmatoire. Ce n'est **pas** une
sélection exploratoire. La choisir exigerait un ADR ultérieur, après acceptation
de DR-007, et n'effacerait pas L-13.

## Constraints

- P0 clos, C02 clos : aucun changement de contrat dans cette pièce.
- I01 n'est pas implémenté ici.
- Risk Engine (C05) et NO_TRADE inchangés.
- Ne pas connecter de broker (P6).
- Ne pas implémenter de stratégie réelle (P2).
- Les mails fournisseurs ne partent pas au titre de DR-007.

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| Attendre DR-003 ∧ DR-005 ACCEPTED avant tout code I01 | Rejeté — confond validation et exploration ; immobilise la R&D sans protéger davantage la confirmation |
| Assouplir DR-003 / DR-005 pour « avancer » | Rejeté — détruit la protection confirmatoire |
| Traiter DATA-REQ `technical` comme sandbox | Rejeté — `technical` est un snapshot C02 qualifiable ; ce n'est pas `UNQUALIFIED` |
| Choisir `yfinance` dans cette pièce | Rejeté — politique ≠ sélection de source ; L-13 reste un FAIL confirmatoire |
| Autoriser un SCI-PASS « provisoire » exploratoire | Rejeté — un PASS n'est pas provisoire ; on recrée la confusion |
| Annuler les questionnaires DR-003 | Rejeté — ils restent le chemin confirmatoire ; HOLD, pas CANCEL |

## Consequences

- La R&D I01 peut ouvrir un chantier `EXPLORATORY` sans attendre D-1 / DR-005.
- `AGENTS.md` distingue les deux classes (DEF-E-04, déchargé à l'acceptation).
- Le premier run exploratoire exige encore : source exploratoire nommée
  (DEF-E-01), marquage `UNQUALIFIED` (DEF-E-02), aucun mail, aucun achat.
- La confirmation I01 reste bloquée par `DR-003 D-1 ACCEPTED ∧ DR-005 ACCEPTED`
  et par un snapshot C02 DATA-PASS.
- Aucune source exploratoire n'est choisie ici. Ne pas ouvrir une qualification
  C02 du sandbox.

## Deferred items

| ID | Objet | Déclencheur |
|----|-------|-------------|
| DEF-E-01 | Sélection d'une source exploratoire (éventuellement une bibliothèque gratuite déjà FAIL en confirmatoire) | DR-007 ACCEPTED |
| DEF-E-02 | Marquage concret des artefacts `UNQUALIFIED` (chemin, en-tête, type C01) | DR-007 ACCEPTED + DEF-E-01 |
| DEF-E-03 | Première exécution exploratoire d'I01 | DEF-E-01 + DEF-E-02 |
| DEF-E-04 | Mise à jour d'une ligne `AGENTS.md` | **Déchargé** à l'acceptation (2026-09-24) |
| DEF-E-05 | Reprise de l'envoi DR-003 et du dossier notices DR-005 | Décision humaine distincte ; pas un effet de DR-007 |

## Status

**ACCEPTED** — acceptation humaine PASS, 2026-09-24.

Aucune source exploratoire retenue. Aucune acquisition. Aucun mail.
DR-003 reste INCONCLUSIVE. DR-005 reste OPEN. Prochain pas distinct :
DEF-E-01 (source sandbox `EXPLORATORY ONLY / UNQUALIFIED`), sans
requalification C02.
