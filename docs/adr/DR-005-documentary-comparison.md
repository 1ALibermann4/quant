# DR-005 — Comparaison documentaire des sources de calendrier (vague 1)

> **Identifier :** DR-005-DOC-1
> **Parent :** [DR-005](DR-005-i01-market-calendar-source.md) (cadrage pré-enregistré)
> **Status :** OPEN — comparaison commencée ; **aucun candidat PASS** ; sélection **INCONCLUSIVE**
> **Authority class :** DECISION RECORD (annexe de preuves)
> **Protocol :** QDP v0.1
> **Date de consultation :** 2026-09-24
> **Baseline :** C02 v1.1 CLOSED `1cda21f` · DR-003 D-1 INCONCLUSIVE
> **Décharge :** DEF-C-01 (notation) — partielle. DEF-C-02 / DEF-C-03 / DEF-C-04 restent ouverts.

Cette pièce **note** les classes C-01…C-06 contre la grille figée dans DR-005. Elle
n'autorise aucune acquisition, n'implémente pas `MarketCalendarSnapshot`, n'exécute
aucune bibliothèque pour émettre une liste de séances, et ne télécharge aucune série
de prix.

**Principe conservé :** `price data ≠ authoritative market calendar`.

## Méthode

| Autorisé | Interdit |
|----------|----------|
| Pages et notices publiques (NYSE, ICE IR, SIFMA, documentation de bibliothèques) | Téléchargement SPY, API de prix, loaders, backtests |
| Lecture du **code source publié** des bibliothèques (ce qu'elles *encodent*) | Exécuter une bibliothèque pour produire le calendrier I01 |
| Communiqués datés, PDF officiels encore hébergés, archives Wayback citées par URL | Traiter Wikipedia, un miroir tiers ou une page marketing comme autorité |
| Constat d'absence (404, page limitée à 2026–2028) | Compléter un trou par l'absence d'une barre de prix |

Une réponse « le calendrier récent a l'air correct » n'est pas un PASS. Les cas
difficiles (fermetures exceptionnelles 1993–présent) sont le test.

Notation par critère : **PASS** / **FAIL** / **UNKNOWN**. Un UNKNOWN sur un REQUIRED
empêche le PASS du candidat. Un FAIL sur un REQUIRED écarte le candidat comme source
**primaire**.

## Réponse intermédiaire à la question de DR-005

> Quelle source — ou quelle politique de sources — permet de matérialiser de façon
> reproductible la séquence des séances attendues par I01 ?

**Aucun candidat isolé de la longlist ne le permet.**

- Le produit officiel NYSE **courant** (C-01) est primaire pour les fériés **à venir**,
  mais il n'est pas un calendrier historique versionné 1993–présent.
- SIFMA (C-02) n'est pas le calendrier actions NYSE.
- Les notices ICE/NYSE (C-03) existent, mais fragmentées ; elles ne forment pas un
  produit unique.
- Les bibliothèques (C-04) encodent les cas difficiles, mais ce sont des
  **implémentations** dont la provenance est mixte (PDF NYSE disparu, miroirs
  tiers, Wikipedia). Elles échouent CAL-S-01 si on les nomme comme source.
- Un calendrier fournisseur de prix (C-05) est interdit comme définition (CAL-S-09).
- « Lun–ven moins fériés fédéraux » (C-06) omet structurellement CAL-02.

La seule voie encore ouverte — **non choisie ici** — est une **politique composite**
(autorité NYSE + notices datées + générateur piné après vérification). Elle reste
INCONCLUSIVE tant que le dossier de notices 1993–présent, la licence de conservation
et la procédure de reconstruction ne sont pas établis (DEF-C-02, DEF-C-03, CAL-S-07,
CAL-S-08).

## Sources consultées (vague 1)

| ID | Document | Rôle |
|----|----------|------|
| S-N1 | [NYSE Holidays & Trading Hours](https://www.nyse.com/markets/hours-calendars) (consulté 2026-09-24) | Produit officiel courant : fériés **2026–2028**, heures régulières, early closes planifiés de ces années |
| S-N2 | PDF annuels ICE/NYSE *Yearly Trading Calendar* : 2022–2026 encore hébergés sous `nyse.com/publicdocs/` | Calendriers officiels **récents** ; pas un archive 1993– |
| S-N3 | `ICE_NYSE_2021_Yearly_Trading_Calendar.pdf` (deux chemins testés) → **404** | Le produit annuel officiel n'est pas retrievable pour 2021 |
| S-N4 | `ICE_NYSE_2012_Yearly_Trading_Calendar.pdf` → **404** | Idem pour l'année Sandy |
| S-N5 | Ancien `http://www.nyse.com/pdfs/closings.pdf` — cité par `exchange_calendars` ; URL vive absente ; captures Wayback (ex. 2007-09-25) | Ancien recueil officiel NYSE *Special Closings, 1885–date* ; plus le produit courant |
| S-N6 | Miroirs tiers du même titre (`ltadvisors.net`, `bcm-news.de`) | **Non officiels** ; utiles seulement pour savoir que le texte a circulé |
| S-N7 | ICE IR — [fermeture 2025-01-09, deuil Jimmy Carter](https://ir.theice.com/press/news-details/2024/The-New-York-Stock-Exchange-Will-Close-Markets-on-January-9-to-Honor-the-Passing-of-Former-President-Jimmy-Carter-on-National-Day-of-Mourning/default.aspx) | Notice officielle datée d'une fermeture exceptionnelle récente |
| S-N8 | NYSE Regulation — [National Day of Mourning 2025-01-02](https://www.nyse.com/publicdocs/nyse/markets/american-options/rule-interpretations/2025/National_Day_of_Mourning_20250102.pdf) | Corroboration réglementaire Carter |
| S-N9 | NYSE Regulation — [Rule 36 / Sandy, 2012-11-06](https://www.nyse.com/publicdocs/nyse/markets/nyse/rule-interpretations/2012/2012-10.pdf) | Preuve *post hoc* de perturbation ; **pas** l'annonce de fermeture des 29–30 octobre |
| S-N10 | ICE IR — [calendrier fériés 2018–2020](https://ir.theice.com/press/news-details/2017/NYSE-Group-Announces-2018-2019-and-2020-Holiday-and-Early-Closings-Calendar/default.aspx) (2017-11-27) | Notices officielles **prospectives**, pas un historique des fermetures exceptionnelles |
| S-S1 | [SIFMA Holiday Schedule](https://www.sifma.org/resources/guides-playbooks/holiday-schedule) | Recommandations **fixed income**, pas NYSE cash equity |
| S-B1 | BBC — [Sandy, 2012-10-29](https://www.bbc.com/news/business-20120344) | Journalisme contemporain ; pas une autorité de calendrier |
| S-L1 | `exchange_calendars` `XNYSExchangeCalendar` + `us_holidays.py` (GitHub, consultés 2026-09-24) | Ce que la bibliothèque encode ; licence Apache-2.0 |
| S-L2 | `pandas_market_calendars` README / `calendars/nyse.py` | Fork / miroir ; licence MIT ; calendriers **shippés dans le code**, pas un flux live |
| S-Q1 | [Quant.SE 14479](https://quant.stackexchange.com/questions/14479/list-of-dates-at-which-the-nyse-was-closed-from-2005-to-2014) | Pointe vers `closings.pdf` et des URL NYSE **mortes** ; propose aussi de déduire les séances d'un fichier de prix — interdit ici |

Aucun fichier de prix n'a été ouvert. Aucune bibliothèque n'a été exécutée.

## Cas difficiles (test CAL-S-03)

Liste **a priori** du cadrage, plus les deuils et le distinguo SIFMA. « Encodé (C-04) »
= présent dans le code source lu, **pas** vérifié par génération ni par prix.

| Événement | Preuve officielle encore vivante ? | S-N1 (page 2026–28) | C-04 (code) | C-02 SIFMA | C-06 fédéraux |
|-----------|------------------------------------|---------------------|-------------|------------|---------------|
| 2001-09-11 … 2001-09-14 (rouvert 17) | Ancien PDF NYSE (S-N5, archive) ; plus le produit courant | Absent | Encodé (`September11Closings`) ; commentaire = Wikipedia | Hors sujet | Absent |
| 2012-10-29 / 2012-10-30 Sandy | Annonce de fermeture NYSE/ICE **non retrouvée vivante** ; S-N9 est postérieur (réouverture / Rule 36) ; S-B1 n'est pas officiel | Absent | Encodé (`HurricaneSandyClosings`) ; commentaire = Wikipedia | Hors sujet | Absent |
| 1994-04-27 Nixon | S-N5 / miroirs ; pas la page courante | Absent | Encodé (`USNationalDaysofMourning`) | Hors sujet | Absent |
| 2004-06-11 Reagan | Idem | Absent | Encodé | Hors sujet | Absent |
| 2007-01-02 Ford | Idem | Absent | Encodé | Hors sujet | Absent |
| 2018-12-05 G.H.W. Bush | À confirmer par notice ICE/NYSE datée (non archivée dans cette vague) | Absent | Encodé | Hors sujet | Absent |
| 2025-01-09 Carter | **Oui** : S-N7, S-N8 | Absent (événement passé, hors table 2026–28) | Encodé | Calendrier bonds distinct | Absent |
| Juneteenth (NYSE dès 2022) | S-N1, S-N2 | Présent pour 2026–28 | Encodé (`USJuneteenth`, `start_date=2022`) | Observé (bonds) | Présent seulement si la liste fédérale est à jour **et** post-2022 |
| Good Friday | S-N1 : NYSE **fermé** | Présent | Encodé | 2026 : **early close 12:00** recommandé, pas une fermeture actions | Absent (n'est pas un férié fédéral) |
| Columbus Day / Veterans Day | S-N1 : **non** listés comme fériés NYSE | Ouvert | Ouvert après 1953 (commentaire XNYS) | 2026 : **fermés** (bonds) | Fermés si on copie le calendrier fédéral |

Lecture : une source « holiday standard 2026 » peut paraître correcte et échouer
CAL-S-03 sur 2001 et 2012. C-02 diverge de NYSE sur Good Friday, Columbus Day et
Veterans Day — preuve directe que SIFMA ne peut pas définir les séances SPY.

## Notation par candidat

Légende du verdict candidat : **PASS** seulement si tous les REQUIRED sont PASS.
Sinon **FAIL** (au moins un REQUIRED FAIL) ou **INCONCLUSIVE** (aucun FAIL, au
moins un REQUIRED UNKNOWN).

### C-01 — Produit officiel NYSE / ICE (page + PDF annuels courants)

| ID | Verdict | Preuve |
|----|---------|--------|
| CAL-S-01 | **PASS** (comme *autorité* des fériés publiés) | S-N1, S-N2, S-N7 : organisme et URL nommables, distincts des barres de prix |
| CAL-S-02 | **FAIL** *comme produit unique* | S-N1 = 2026–2028 seulement. S-N3/S-N4 = 404 pour 2021 et 2012. Fenêtre I01 ≥ 1993-01-22 non couverte par le produit courant |
| CAL-S-03 | **FAIL** *comme produit unique* | La page courante omet structurellement 9/11, Sandy, les deuils antérieurs. Carter n'apparaît que via une notice séparée (S-N7), pas dans S-N1 |
| CAL-S-04 | **UNKNOWN** hors 2026–2028 | Early closes 1:00 ET documentés pour 2026–2028 (S-N1). Historique (2:00 avant 1993, ad hoc 1997-12-26, 1999-12-31, 2003-12-26, etc.) absent du produit courant |
| CAL-S-05 | **PASS** (présent) | S-N1 : core session 09:30–16:00 ET = `America/New_York` |
| CAL-S-06 | **UNKNOWN** | Pas d'identifiant de version unique pour « le calendrier NYSE 1993–as_of ». Les PDF annuels sont datés par année, pas un snapshot historique consolidé |
| CAL-S-07 | **UNKNOWN** | Les *Vendor Agreements* NYSE Data Products (PDP) restreignent la reproduction des produits de données. Ils ne tranchent pas clairement la conservation d'une liste de jours extraite de S-N1. Faits publics ≠ licence établie |
| CAL-S-08 | **UNKNOWN** | Procédure de reconstruction 1993–présent non écrite : le produit courant ne suffit pas |
| CAL-S-09 | **PASS** | S-N1 ne dérive pas les séances d'un fichier de prix |

**Verdict C-01 : FAIL** comme source unique de la fenêtre I01. Reste l'autorité
**primaire** pour les fériés et heures **qu'il publie encore**.

### C-02 — Recommandations SIFMA (US holiday)

| ID | Verdict | Preuve |
|----|---------|--------|
| CAL-S-01 | **FAIL** | S-S1 : « recommendations » pour titres à revenu fixe USD, pas le calendrier NYSE cash equity |
| CAL-S-03 | **FAIL** | Calendrier distinct (Good Friday, Columbus Day, Veterans Day). N'encode pas 9/11 / Sandy comme calendrier actions |
| CAL-S-09 | n/a | Hors rôle de définition |

**Verdict C-02 : FAIL** comme source primaire. Rôle conservé : **corroboration
négative** (détecter une confusion bonds / actions).

### C-03 — Notices ICE / NYSE historiques (communiqués, rule interpretations)

| ID | Verdict | Preuve |
|----|---------|--------|
| CAL-S-01 | **PASS** (par notice) | S-N7, S-N8, S-N10 : émetteur identifiable |
| CAL-S-02 | **UNKNOWN** | Pas d'index officiel unique 1993–présent. S-N10 couvre des fériés *futurs* en 2017, pas Sandy ni 9/11 |
| CAL-S-03 | **UNKNOWN** | Carter : PASS local (S-N7). Sandy : l'annonce de fermeture n'est pas retrouvée vivante (S-N9 insuffisant). 9/11 : dépend de S-N5 archivé, plus du flux notices actuel |
| CAL-S-04 | **UNKNOWN** | Notices early-close prospectives existent (S-N10) ; série historique incomplète dans cette vague |
| CAL-S-05 | **PASS** lorsqu'une notice donne l'heure ET | S-N1 / S-N10 |
| CAL-S-06 | **UNKNOWN** | Chaque notice est datée ; l'ensemble n'a pas d'identifiant de compilation |
| CAL-S-07 | **UNKNOWN** | Même réserve que C-01 |
| CAL-S-08 | **UNKNOWN** | Dossier à constituer ; URLs historiques souvent mortes (S-Q1) |
| CAL-S-09 | **PASS** | Notices d'échange, pas des barres |

**Verdict C-03 : INCONCLUSIVE** comme *complément* ; **FAIL** comme produit unique
(couverture et versionnement non établis). Indispensable pour CAL-02 si on refuse
C-04 comme autorité.

### C-04 — `exchange_calendars` / `pandas_market_calendars`

| ID | Verdict | Preuve |
|----|---------|--------|
| CAL-S-01 | **FAIL** *comme source* | DR-005 Constraints : implémentation, pas autorité, tant que le contenu n'est pas rattaché à une publication versionnée. S-L1 cite `nyse.com/pdfs/closings.pdf` (mort), `stevemorse.org`, et Wikipedia pour 9/11 et Sandy |
| CAL-S-02 | **UNKNOWN** (capacité, pas autorité) | Le code XNYS couvre largement avant 1993 ; non démontré ici par génération |
| CAL-S-03 | **UNKNOWN** (encodage ≠ preuve) | 9/11, Sandy, deuils jusqu'à Carter, Gloria 1985 sont dans `us_holidays.py`. La provenance de plusieurs listes ad hoc n'est pas NYSE vivant |
| CAL-S-04 | **UNKNOWN** (encodage) | Early close régulier 13:00 depuis 1993, 14:00 avant ; ad hoc 1997-12-26, 1999-12-31, 2003-12-26. Non recoupé notice par notice dans cette vague |
| CAL-S-05 | **PASS** (implémentation) | `tz = ZoneInfo("America/New_York")`, `close_times` 16:00 (S-L1) |
| CAL-S-06 | **PASS** *du générateur* | Paquet + commit Git pinables ; S-L2 : « shipped as package code », pas un serveur live. Ce n'est **pas** une version NYSE |
| CAL-S-07 | **PASS** *du code* | Apache-2.0 (S-L1) / MIT (S-L2) pour le logiciel. Cela n'autorise pas à relabeler la sortie « calendrier officiel NYSE » |
| CAL-S-08 | **UNKNOWN** | Reproductible *si* version pinée + procédure ; la procédure n'est pas écrite (DEF-C-03) |
| CAL-S-09 | **PASS** conditionnel | Les bibliothèques ne lisent pas un fichier SPY. Interdit : « corriger » une date parce qu'une barre manque |

**Verdict C-04 : FAIL** comme source primaire (CAL-S-01). **Rôle possible plus
tard** : générateur piné **après** rattachement à une autorité et vérification
indépendante — ce n'est pas un choix dans cette pièce.

### C-05 — Calendrier livré par un fournisseur de prix

| ID | Verdict | Preuve |
|----|---------|--------|
| CAL-S-01 / CAL-S-09 | **FAIL** | DR-003 F-05 : aucun finaliste prix ne livre un calendrier versionné indépendant. Définir les séances par les barres viole le cadrage |

**Verdict C-05 : FAIL** comme définition. Contrôle croisé Q-05 / Q-06 seulement,
après les deux DR ACCEPTED.

### C-06 — « Lun–ven moins fériés fédéraux » maison

| ID | Verdict | Preuve |
|----|---------|--------|
| CAL-S-03 | **FAIL** | Omet Good Friday, 9/11, Sandy, deuils ; ajoute Columbus Day / Veterans Day que NYSE n'observe plus |

**Verdict C-06 : FAIL.**

## Synthèse des verdicts

| Candidat | Verdict vague 1 | Peut-il définir les séances I01 ? |
|----------|-----------------|-----------------------------------|
| C-01 produit NYSE courant | **FAIL** (couverture + exceptionnels) | Non, seul. Oui, comme autorité des fériés *publiés* |
| C-02 SIFMA | **FAIL** | Non |
| C-03 notices ICE/NYSE | **INCONCLUSIVE** | Pas seul. Nécessaire au dossier CAL-02 |
| C-04 bibliothèques | **FAIL** comme source | Générateur seulement, plus tard |
| C-05 fournisseur prix | **FAIL** | Non |
| C-06 fériés fédéraux | **FAIL** | Non |
| Politique composite (non choisie) | **INCONCLUSIVE** | Seule voie restante ; DEF-C-02 ouvert |

Aucun REQUIRED n'a été assoupli.

## Politique composite (piste, non retenue)

Si DEF-C-02 devait un jour retenir une politique plutôt qu'un produit unique, la
seule combinaison **non déjà FAIL** serait :

1. **Autorité des fériés planifiés** : S-N1 / PDF annuels ICE-NYSE encore hébergés,
   plus notices prospectives ICE (type S-N10), pinées par URL + date de consultation.
2. **Autorité des fermetures exceptionnelles** : notices ICE/NYSE datées lorsqu'elles
   existent (modèle S-N7) ; pour le passé, **captures Wayback datées** de
   `closings.pdf` *uniquement si* on établit que la capture est bien l'édition
   officielle NYSE, puis notices postérieures pour tout événement après la dernière
   édition.
3. **Générateur** : bibliothèque pinée (C-04) pour *matérialiser* QCC-1, jamais pour
   * trancher* un désaccord. Un écart bibliothèque / notice officielle se résout
   **en faveur de la notice**.
4. **Interdits** : C-02 comme définition ; C-05 / fichier de prix comme définition ;
   C-06.

Cette piste **n'est pas ACCEPTED**. Bloquants restants :

| ID | Pourquoi ce n'est pas encore PASS |
|----|-----------------------------------|
| CAL-S-02 / CAL-S-03 | Dossier notice-par-notice 1993–présent incomplet (Sandy : pas d'annonce de fermeture vivante) |
| CAL-S-04 | Early closes historiques non recoupés officiellement au-delà de 2026–28 et de quelques communiqués |
| CAL-S-06 | Pas d'identifiant `(source, version)` pour la *compilation* |
| CAL-S-07 | Licence de conservation de la liste extraite des pages NYSE **UNKNOWN** |
| CAL-S-08 | Procédure écrite absente (DEF-C-03) |

## Ce que cette vague n'a pas fait

- Pas de génération d'une liste QCC-1.
- Pas d'implémentation `MarketCalendarSnapshot`.
- Pas d'appel d'API, pas d'abonnement, pas de SPY.
- Pas d'archivage binaire des PDF NYSE dans le dépôt (droit de reproduction non établi).
- Pas de verdict ACCEPTED.

## Prochaine étape de **cette** branche

Constituer un **dossier de notices** (URLs stables ou captures datées) pour chaque
fermeture exceptionnelle 1993–présent connue a priori, en commençant par Sandy
(annonce de fermeture, pas seulement S-N9) et les deuils 1994–2018. Ensuite seulement
on pourra rouvrir DEF-C-02.

L'attente DR-003 (réponses fournisseurs) ne bloque pas ce travail.

## Status

DR-005 reste **OPEN**. La sélection de source est **INCONCLUSIVE** : comparaison
faite, aucun PASS, plusieurs FAIL établis, aucune politique retenue.
L'acquisition reste interdite.
