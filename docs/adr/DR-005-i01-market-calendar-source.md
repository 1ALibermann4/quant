# DR-005 — I01 : source du calendrier de marché (cadrage)

> **Identifier :** DR-005
> **Status :** OPEN — cadrage figé ; comparaison documentaire vague 1 : aucun candidat PASS
> **Comparaison :** [DR-005-documentary-comparison.md](DR-005-documentary-comparison.md)
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1
> **Date :** 2026-09-24
> **Baseline :** C02 v1.1 CLOSED `1cda21f` · [DR-003](DR-003-i01-market-data-source-selection.md) D-1 INCONCLUSIVE
> **Dérivé de :** `research/I01/DATA-REQ-I01.md` v0.1 §2 (GRA-*, CAL-*, TS-*) ;
> `specs/contracts/C02/C02_v1.1.yaml` (`MarketCalendarSnapshot`, QCC-1)
> **Relève :** DR-003 DEF-04 (non réécrit dans DR-003 v1.0)

Cette pièce **cadre** l'investigation (critères figés). La notation vague 1 est dans
[DR-005-documentary-comparison.md](DR-005-documentary-comparison.md). Aucun candidat
n'est retenu. Aucune acquisition n'est autorisée.

## Context

I01 indexe le temps en **rangs de séance** (CAL-04, DEC-02). Une séance attendue absente
des prix est une **séance manquante** (CAL-03), jamais une preuve que le marché était
fermé. DR-003 F-05 : aucun finaliste prix ne livre un calendrier versionné.

C02 v1.1 fournit le type `MarketCalendarSnapshot` (liste matérialisée, empreintes QCC-1,
`early_closes`, fuseau IANA). Il ne choisit aucune source réelle
(`MarketCalendarSnapshot.non_goals`).

**Principe obligatoire :**

```text
price data ≠ authoritative market calendar
```

Le fournisseur de prix peut servir au **contrôle croisé** (Q-05, Q-06). Il ne définit
pas les séances attendues.

DR-005 est **indépendant** de DR-003 : un INCONCLUSIVE ou un FAIL de l'un ne se
compense pas par l'autre. L'acquisition n'est autorisée que si

```text
DR-003 D-1 ACCEPTED  ∧  DR-005 ACCEPTED
```

## Decision (cadrage seulement)

Ouvrir l'investigation de sourcing du calendrier **avant** toute comparaison notée.
Les critères ci-dessous sont figés **avant** d'examiner les candidats. Aucune source
n'est choisie dans cette révision.

## Constraints

- Aucun téléchargement SPY, aucune série de prix, aucune API, aucun loader, aucun backtest.
- C02 n'est pas modifié. I01 n'est pas exécuté.
- Preuves futures : documentation officielle ou publication versionnée de la source
  de calendrier — pas les barres d'un fournisseur de prix.
- Les bibliothèques (`pandas_market_calendars`, `exchange_calendars`, …) sont des
  **implémentations**, pas des sources primaires, tant que leur contenu n'est pas
  rattaché à une autorité versionnée.

## Authorities consulted

| Document | Rôle |
|----------|------|
| DATA-REQ-I01 v0.1 §2, §6, Q-05/Q-06/Q-10 | GRA-01…04, CAL-01…04, TS-01…04 |
| C02 v1.1 `MarketCalendarSnapshot` | Forme à matérialiser (QCC-1) |
| DR-003 F-05, DEF-04, D-2 (SPY / NYSE Arca) | Constat et instrument ; pas la source de séances |
| DR-004 | C02 ne choisit pas la source de calendrier |
| QDP v0.1 | INCONCLUSIVE normatif ; pas d'API avant besoins dérivés |

## Périmètre pré-enregistré

| Élément | Enregistrement |
|---------|----------------|
| Marché | Séances régulières du marché actions US dont la clôture officielle est celle que I01 attribue à **SPY** (GRA-02, GRA-04). Convention de place : **NYSE** au sens « journée de négociation régulière US cash equity », pas « toute séance Arca étendue ». |
| Instrument | SPY (DR-003 D-2) — le calendrier n'est pas dérivé de la présence de SPY dans un fichier de prix. |
| Granularité | Daily, une date ISO par séance (GRA-01, TS-01). |
| Fenêtre minimale | Au moins la fenêtre CONFIRMATORY I01 : ≥ 10 ans calendaires **et** ≥ 2 520 séances (DATA-REQ PA-03 / §4). |
| Fenêtre préférée | 15–20 ans (PA-04, REV-D / profondeur). |
| Borne inférieure de couverture | Au plus tard le **1993-01-22** (création SPY, DR-003 D-2), afin de ne pas tronquer l'instrument par le calendrier. |
| Borne supérieure | `as_of` / `last_session` déclarés à la matérialisation du snapshot ; pas une date opportuniste après avoir vu des prix. |
| Fuseau | `America/New_York` (TS-01). Clôture régulière locale : **16:00** (convention I01 `after_close_of_t`). |
| Pré / post-marché | Hors séance (GRA-02). |

## Définition d'une session

Une **séance** est une date `YYYY-MM-DD` (fuseau de la place) durant laquelle le marché
de référence a une **journée de négociation régulière**, y compris si la clôture est
anticipée (GRA-03).

Ce n'est pas :

- un jour civil de semaine ;
- un jour où un fichier de prix contient une ligne ;
- une séance étendue (pre/post) ;
- un jour férié observé, un deuil national, une fermeture météo ou un arrêt d'urgence.

## Fermetures exceptionnelles

CAL-02 : le calendrier doit inclure les **jours fériés planifiés** et les **fermetures
non planifiées** (événements, deuils, intempéries, arrêts d'urgence) sur la fenêtre
couverte.

Des cas historiques **connus a priori** (liste non exhaustive, à vérifier contre la
source retenue, sans série de prix) : 2001-09-11 et jours suivants ; 2012-10-29/30
(Sandy) ; deuils nationaux ; autres fermetures NYSE documentées sur 1993–présent.

Une source qui ne couvre que le calendrier « holiday standard » sans fermetures
exceptionnelles **ne peut pas** obtenir CAL-02 = PASS.

## Corrections historiques

Toute révision de la liste des séances (ajout/retrait d'une fermeture, correction d'une
date) doit être **observable** : identifiant de version différent, ou publication datée.
Un calendrier mutable sans version n'est pas CAL-01.

Les corrections ne s'appliquent à un snapshot C02 déjà figé qu'en produisant un **nouveau**
`MarketCalendarSnapshot` (nouvelle empreinte). On ne réécrit pas silencieusement l'ancien.

## Early closes

GRA-03 : une clôture anticipée **reste une séance**. C02 : champ optionnel `early_closes`
`[{session, close_local}]` ; `close_instant` utilise cette heure.

Le cadrage exige que la source permette, ou qu'une règle officielle permette, de
renseigner les early closes sur la fenêtre. Une source qui ignore les early closes
peut encore lister les dates de séance, mais I01 ne pourra pas dater `after_close_of_t`
correctement ces jours-là → au minimum WARN / INCONCLUSIVE sur Q-10 tant que les heures
ne sont pas établies.

## Timezone

- Canonique : `America/New_York`.
- `regular_close_local` : `16:00` (heure naïve locale), sauf early close.
- Interdit : déduire la séance d'un instant UTC à minuit (TS-02 / TS-04, DR-003 F-03).

## Provenance

Un `MarketCalendarSnapshot` C02 exige `source` et `source_version` (`Knowable`).
La source doit être **nommable** (organisme, produit, URL stable) et distincte du
fournisseur de prix retenu par DR-003, sauf preuve que ce fournisseur publie un
calendrier **indépendant** de ses barres — ce qui n'est pas établi en v1.0 (F-05).

## Licence

La copie du calendrier matérialisé (liste QCC-1 + métadonnées) doit être **conservable**
localement pour la durée de reproductibilité du snapshot (analogue PA-08 / PA-09 / REP-05).
Une licence qui interdit de retenir la liste des séances interdit CAL-01 opérationnel.

## Versionnement

CAL-01 : identité `(source, version)` enregistrée. Deux builds avec la même version
doivent produire la même liste QCC-1 (C02-INV-06 / INV-14).

## Reproductibilité

| Exigence | Mesure |
|----------|--------|
| Liste complète | `sessions` matérialisée, pas une règle « lun–ven moins fériés » non développée |
| Empreinte | QCC-1 → `sessions_fingerprint` ; `content_fingerprint` C02 |
| Rang | `rank(session)` défini (CAL-04) |
| Reconstruction | à partir de la source versionnée + procédure écrite, sans appel réseau pendant un run I01 (REP-01) |

## Politique de corroboration

| Rôle | Autorisé | Interdit |
|------|----------|----------|
| Source de calendrier | définit les séances attendues | — |
| Fournisseur de prix (DR-003) | Q-05 / Q-06 : taux de manquants, dates hors calendrier | définir ou « corriger » le calendrier parce qu'une barre manque ou existe |
| Bibliothèque | reproductibilité d'un algorithme **si** son entrée est une source versionnée | servir de source innommée |

`absence de ligne de prix ⇏ marché fermé`.

## Critères PASS / FAIL / INCONCLUSIVE

Notés **par candidat** dans [DR-005-documentary-comparison.md](DR-005-documentary-comparison.md)
(vague 1, 2026-09-24). Les critères ci-dessous n'ont pas été assouplis.

| Verdict | Condition |
|---------|-----------|
| **PASS** | Tous les critères REQUIRED ci-dessous sont établis par une preuve officielle ou une publication versionnée ; un `MarketCalendarSnapshot` C02 est constructible sans inventer de séance ; licence de conservation OK ; indépendance au fournisseur de prix établie. |
| **FAIL** | La source définit les séances par les barres de prix ; ou nie / omet structurellement les fermetures exceptionnelles ; ou interdit la conservation de la liste ; ou n'est pas versionnable. |
| **INCONCLUSIVE** | Aucun FAIL, mais au moins un REQUIRED non tranché (documentation absente, early closes non établis, couverture historique non prouvée). |

### Grille (à noter plus tard — non notée ici)

| ID | Critère | Niveau |
|----|---------|--------|
| CAL-S-01 | Source primaire identifiable, distincte des barres de prix | REQUIRED |
| CAL-S-02 | Couverture ≥ 1993-01-22 jusqu'à une borne `as_of` déclarée | REQUIRED |
| CAL-S-03 | Jours fériés **et** fermetures exceptionnelles (CAL-02) | REQUIRED |
| CAL-S-04 | Early closes représentables ou explicitement hors capacité (alors I01 Q-10) | REQUIRED pour un PASS I01 confirmatory ; sinon INCONCLUSIVE |
| CAL-S-05 | Fuseau + clôture régulière déterminables (TS-*) | REQUIRED |
| CAL-S-06 | Versionnement + liste matérialisable QCC-1 | REQUIRED |
| CAL-S-07 | Licence de conservation de la copie calendrier | REQUIRED |
| CAL-S-08 | Procédure de reconstruction sans réseau au run | REQUIRED |
| CAL-S-09 | Indépendance : aucune séance n'est ajoutée/retirée pour coller à un fichier de prix | REQUIRED |

Un candidat qui échoue un REQUIRED est écarté. Un UNKNOWN sur un REQUIRED empêche
l'ACCEPTED de DR-005.

## Alternatives à examiner

Longlist du cadrage. **Notée** en vague 1 (aucun PASS). Y figurer n'est ni un PASS
ni une présélection. Détail : [comparaison](DR-005-documentary-comparison.md).

| # | Classe | Rôle possible | Risque déjà visible (non noté) |
|---|--------|---------------|--------------------------------|
| C-01 | Calendrier officiel NYSE / notices d'échange (jours fériés + fermetures) | Source primaire plausible | Couverture historique et forme versionnée à établir |
| C-02 | Recommandations SIFMA (US holiday) | Corroboration | N'est pas le calendrier NYSE |
| C-03 | Publications ICE / notices historiques de fermeture | Complément CAL-02 | Fragmentation des documents |
| C-04 | Bibliothèques `exchange_calendars` / `pandas_market_calendars` | Implémentation | Pas une autorité ; dépendre d'elles sans source = FAIL CAL-S-01 |
| C-05 | Calendrier livré par un fournisseur de prix | Contrôle croisé seulement | DR-003 F-05 ; interdit comme définition (CAL-S-09) |
| C-06 | « Lun–ven moins une liste de fériés fédéraux » maison | — | Omet fermetures exceptionnelles → FAIL CAL-S-03 |

Aucun de ces items n'est choisi. Vague 1 : C-02 / C-05 / C-06 FAIL ; C-01 FAIL comme
produit unique ; C-03 et toute politique composite restent INCONCLUSIVE.

## Consequences

- DR-005 est **OPEN**. Aucune source de calendrier n'est ACCEPTED.
- Aucune acquisition de prix ni de calendrier n'est autorisée par cette pièce.
- C02 et I01 inchangés.
- Vague 1 documentaire : [DR-005-documentary-comparison.md](DR-005-documentary-comparison.md).
  Aucun candidat isolé ne passe la grille. La prochaine étape de **cette** branche :
  dossier de notices pour les fermetures exceptionnelles 1993–présent (Sandy en
  priorité), sans API de prix et sans implémenter `MarketCalendarSnapshot`.
- L'acquisition I01 attend `DR-003 D-1 ACCEPTED ∧ DR-005 ACCEPTED`.

## Deferred items

| ID | Objet | Déclencheur |
|----|-------|-------------|
| DEF-C-01 | Notation des classes C-01… | **Partiel (2026-09-24)** : [comparaison](DR-005-documentary-comparison.md). C-02, C-05, C-06 FAIL ; C-01 FAIL comme produit unique ; C-03 / politique composite INCONCLUSIVE |
| DEF-C-02 | Décision de source + version | Un candidat PASS sur tous les REQUIRED |
| DEF-C-03 | Procédure de build du `MarketCalendarSnapshot` | Après DEF-C-02 |
| DEF-C-04 | Articulation early closes ↔ Q-10 | Si CAL-S-04 INCONCLUSIVE |

## Status

**OPEN.** Cadrage inchangé. Comparaison vague 1 faite : **sélection INCONCLUSIVE**
(aucun PASS, plusieurs FAIL). Aucun candidat retenu. Pas ACCEPTED.

[DR-007](DR-007-exploratory-vs-confirmatory-data.md) (ACCEPTED) n'assouplit pas
cette grille. Un calendrier exploratoire futur, s'il existe, ne pourra pas servir
de source confirmatoire.
