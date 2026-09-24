# DR-003 — I01 : sélection de la source de données de marché et de l'instrument

> **Identifier :** DR-003
> **Status :** INCONCLUSIVE
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1
> **Dérivé de :** `research/I01/DATA-REQ-I01.md` v0.1 (commit `4e117e5`)
> **Date de consultation des sources :** 2026-09-23
> **Révision :** v1.1 OPEN — demandes écrites ; les résultats v1.0 ci-dessous ne sont ni
> supprimés ni réécrits. Questionnaires : [DR-003-v1.1-vendor-inquiries.md](DR-003-v1.1-vendor-inquiries.md).
> **Baseline C02 :** `1cda21f` CLOSED / ACCEPTED. L'acquisition reste interdite.

Ce DR contient **deux décisions distinctes** :

| ID | Objet | Résultat |
|----|-------|----------|
| **D-1** | Fournisseur de données (checklist DATA-REQ §10) | **INCONCLUSIVE** — aucun candidat ne satisfait tous les critères REQUIRED |
| **D-2** | Instrument I01 (DATA-REQ §1) | **SPY** pré-enregistré (critères INS-* et départage §1.2) |

Le statut global est INCONCLUSIVE parce que D-1 l'est. D-2 est enregistré dès maintenant, car
DATA-REQ §1.2 exige que le départage de l'instrument soit fixé avant toute exécution. Il ne
dépend d'aucun fournisseur particulier (voir §D-2).

---

## Context

DATA-REQ-I01 v0.1 fixe les propriétés que les données doivent garantir pour qu'I01 puisse
produire un verdict SCI. Il renvoie la comparaison des sources à un ADR, contre la checklist
PA-01…PA-14. Ce DR fait cette comparaison sur les fournisseurs disponibles en septembre 2026.

Principe directeur : le dataset fait partie de l'instrument scientifique. La provenance, la
méthode d'ajustement et le droit de conserver la copie brute l'emportent sur la gratuité, la
popularité et la facilité d'intégration.

## Authorities consulted

| Document | Rôle |
|----------|------|
| `research/I01/DATA-REQ-I01.md` v0.1 | Autorité normative : INS-*, §5, §7.1, §8, §10, §11 |
| `research/I01/protocol.md` v0.2 | Profondeur, convention `after_close_of_t` |
| `specs/contracts/C02/C02_v1.0.yaml` | Contrat DatasetSnapshot (non modifié ici) |
| `AGENTS.md`, `docs/governance/qdp_v0_1.md` | Pas de broker avant P6, statut INCONCLUSIVE normatif |
| Documentation officielle des fournisseurs | Preuves (liste §Sources) |

Aucun résultat I01 n'existe : l'expérience n'a pas commencé.

## Constraints

- Aucune donnée expérimentale téléchargée, aucun appel à un endpoint de données, aucun loader.
- I01 et C02 ne sont pas modifiés.
- Preuves normatives uniquement issues de la **documentation officielle** du fournisseur
  (référence d'API, conditions d'utilisation, tarifs, FAQ ou articles publiés sur son domaine).
  Les comparatifs tiers ne servent au mieux que de corroboration, jamais de preuve.
- La documentation Tiingo est rendue côté client. Son texte a été lu dans le module JavaScript
  statique du site officiel (`apimedia.tiingo.com/dist/src_app_api_documentation_documentation_module_ts-es2015.376f7741ca847feea8f8.js`),
  qui est la source du contenu affiché sur `tiingo.com/documentation`.

### Règles de notation

| Score | Sens |
|-------|------|
| **PASS** | La documentation officielle établit explicitement la propriété |
| **FAIL** | La documentation officielle établit explicitement que la propriété est absente ou violée |
| **UNKNOWN** | Aucune documentation officielle ne tranche ; une inférence plausible n'est **pas** un PASS |
| **NOT_APPLICABLE** | Le critère ne s'applique pas à ce candidat, ou n'a pas de seuil normatif (PA-13) |

- La licence dépend du palier : chaque **offre** (fournisseur × palier) est notée séparément.
- PA-01 et PA-03 sont notés sur la couverture et la profondeur **documentées au niveau du jeu de
  données**. La première date disponible pour l'instrument est un contrôle obligatoire
  d'acquisition (Q-09), pas une preuve de ce DR.
- Un candidat qui a au moins un FAIL sur un critère REQUIRED est écarté (DATA-REQ §10).
- Un candidat qui a un UNKNOWN sur un critère REQUIRED ne peut pas être accepté.

---

## Evidence

### E.1 Longlist

| # | Offre | Type | Motif d'inclusion |
|---|-------|------|-------------------|
| L-01 | Tiingo — Starter (gratuit) | API EOD | Piste fournie ; `adjClose`, CRSP |
| L-02 | Tiingo — Power (individuel, payant) | API EOD | Idem, licence différente |
| L-03 | Alpha Vantage — gratuit | API | Piste fournie |
| L-04 | Alpha Vantage — Premium | API | `TIME_SERIES_DAILY_ADJUSTED` |
| L-05 | Sharadar — gratuit | API / bulk | Offre d'entrée |
| L-06 | Sharadar — Prices, Full History (Personal Use) | API / bulk CSV | Table `funds` : `closeadj`, `closeunadj` |
| L-07 | EODHD — gratuit | API EOD | Offre d'entrée |
| L-08 | EODHD — EOD Historical Data All World (personnel) | API EOD | `adjusted_close` + `close` brut |
| L-09 | Massive (ex-Polygon.io) | API | Fournisseur US courant |
| L-10 | Databento — US Equities | API | Données de marché primaires |
| L-11 | Alpaca Market Data | API | Fournisseur US courant |
| L-12 | Norgate Data — US Stocks | Base locale | Données ajustées total return |
| L-13 | Yahoo Finance via `yfinance` | Bibliothèque non officielle | Usage répandu |
| L-14 | CRSP via WRDS | Base académique | Référence méthodologique d'ajustement |

Non examinés dans cette itération : Financial Modeling Prep, Twelve Data, Intrinio, Barchart,
Nasdaq Data Link USEDH. Ils peuvent être ajoutés par amendement ; ne pas les avoir examinés ne
préjuge pas de leur admissibilité.

### E.2 Élimination — FAIL certain sur une exigence bloquante

| Offre | Critère en échec | Preuve officielle | Source |
|-------|------------------|-------------------|--------|
| L-01 Tiingo Starter | **PA-08, PA-09** | CGU §1.6(a) : sur le plan Starter, « you may not write, save, archive, back up, or otherwise retain Tiingo Data in any persistent or durable storage » | S-T6 |
| L-03 Alpha Vantage gratuit | **PA-02, PA-03** | `TIME_SERIES_DAILY_ADJUSTED` est « a premium API function » ; `outputsize=full` est réservé aux clés premium, `compact` = 100 derniers points | S-A1 |
| L-05 Sharadar gratuit | **PA-01** | « Our entry level dataset is completely FREE and includes company fundamentals and market data for all 30 Dow Jones Industrial Average companies » — aucune table `funds` | S-S7 |
| L-07 EODHD gratuit | **PA-03** | « The free plan gives you the same endpoint for any ticker, but only the past year of history and 20 API calls a day » | S-E1 |
| L-09 Massive | **PA-02, PA-05** | Paramètre `adjusted` limité aux splits ; FAQ : « Aggregate bars are split-adjusted by default, and you get raw prices with adjusted=false. Nothing is dividend-adjusted » ⇒ ajustement splits seuls (§5.1 : non admissible) | S-M1, S-M2 |
| L-10 Databento | **PA-03** (+ GRA-02) | US Equities « Since 2018-05-01 », « 8+ years » (< 10 ans) ; `ohlcv-1d` « is based on UTC dates », pas sur la séance | S-D1, S-D2 |
| L-11 Alpaca | **DATA-REQ §11** (+ PA-06) | Données livrées par une plateforme de courtage ; §11 : « API broker — Interdit avant P6 ». Base d'événements sur titre accessible seulement depuis avril 2020 | S-L1, S-L2 |
| L-12 Norgate | **PA-08** (+ PA-06) | « The data is held on a user's Windows machine […] in a proprietary database format […] Access to the database is no longer possible if a subscription lapses. » Seul un export ASCII des prix (déjà transformés) est possible, pas les données telles que reçues. FAQ : pas de détail des événements sur titre | S-N1, S-N3 |
| L-13 Yahoo / `yfinance` | **PA-14** (+ PA-09) | « yfinance is not affiliated, endorsed, or vetted by Yahoo […] the Yahoo! finance API is intended for personal use only » ⇒ aucune interface officielle identifiable ni versionnée | S-Y1 |

L-14 **CRSP / WRDS** n'est pas écarté sur un FAIL : aucune offre individuelle n'est publiée
(WRDS : « Please contact wrds@wharton.upenn.edu for pricing information »). PA-09 et PA-13 sont
**UNKNOWN** ; le candidat n'est pas poursuivi, mais reste la **référence méthodologique** revendiquée
par Tiingo et EODHD (S-C1).

### E.3 Évaluation détaillée des offres restantes

Colonnes : **Élément** (liste de la demande) → **PA** (critère DATA-REQ) → **Score** → **Preuve** → **Source**.

#### E.3.1 Tiingo — Power (L-02)

| Élément | PA | Score | Preuve | Source |
|---------|----|-------|--------|--------|
| Couverture ETF US | PA-01 | PASS | Endpoints EOD couvrant « stocks, ETFs, and mutual funds » | S-T2 |
| Profondeur daily | PA-03 | PASS | « end-of-day history back to 1962 », « 30+ years of price history » ; endpoint meta : `startDate` = « earliest date we have price data available for the asset » | S-T5, S-T1 |
| Profondeur 15–20 ans homogène | PA-04 | UNKNOWN | Profondeur documentée, homogénéité de source non documentée (voir PA-11) | — |
| `adjusted_close` | PA-02 | PASS | `adjClose` : « The adjusted closing price for the asset on the given date » | S-T1 |
| Splits | — | PASS | `splitFactor = splitTo/splitFrom` ; ex-date « also the date used for split adjustments » | S-T2 |
| Distributions | — | PASS | `divCash` : « note that "date" will be the "exDate" for the dividend » ; ex-date « also the date used for dividend price adjustments » | S-T1, S-T3 |
| Close brut | PA-06 | PASS | « Both raw prices and adjusted prices are available » ; champ `close` | S-T1 |
| Événements sur titre | PA-06 | PASS | `divCash` et `splitFactor` par ligne ; endpoints Splits (bêta) et Distributions | S-T2, S-T3 |
| Méthodologie documentée | PA-05 | PASS | « The adjustment methodology follows the standard method set forth by "The Center for Research in Security Prices" (CRSP) […] incorporates both split and dividend adjustments » — méthode proportionnelle, référence ex-date explicite | S-T1 |
| Dates / ex-dates | PA-05 | PASS | Ex-date explicitement utilisée pour les deux ajustements | S-T2, S-T3 |
| Correction / révision | PA-10 | PASS | « exchanges may send corrections until 8 PM EST. As we obtain corrections, we update prices throughout the evening » ; KB : re-télécharger tout l'historique si `splitFactor != 1` ou `divCash > 0` | S-T1, S-T4 |
| Identifiants stables | INS-05 | PASS | `permaTicker` (« query EOD price history by permaTicker ») ; CUSIP/ISIN pris chez l'émetteur | S-T1, S-I1 |
| Fuseau / calendrier | PA-07 | PASS | `date` typé *date* (« The date this data pertains to »), sérialisé `YYYY-MM-DDT00:00:00.000Z` ⇒ règle TS-02 : lire la date littérale, **ne jamais convertir** en America/New_York. Aucun calendrier fourni (CAL-01 à traiter à part) | S-T1 |
| Formats d'export | PA-08 | PASS | JSON par défaut, `format=csv` | S-T1 |
| Conservation locale | PA-08 | PASS | CGU §1.6(b) : sur un plan payant, « you may persist Tiingo Data in storage solely to the extent permitted by that Paid Plan » | S-T6 |
| Limites d'API | PA-12 | PASS | Power : 10 000 requêtes/h, 100 000/jour, 40 Go/mois ; un seul appel historique suffit. CGU §7.3 : limites approximatives, modifiables | S-T7, S-T6 |
| Coût | PA-13 | NOT_APPLICABLE | 30 $/mois ou 300 $/an (individuel, non commercial) ; 50 $/mois ou 499 $/an (commercial interne) | S-T7 |
| Licence R&D personnelle | PA-09 | PASS | §7.3 : « All data via the API is for internal consumption only. If you are an individual, you may sign up for an Individual plan ». **Conservation limitée à l'abonnement** : §1.6(b) impose la suppression de toutes les copies à expiration, résiliation ou rétrogradation | S-T6 |
| Pas de raboutage non documenté | PA-11 | **UNKNOWN** | Sources amont EOD non documentées ; seul un « proprietary error checking framework » est mentionné | S-T1 |
| Identité + version d'interface | PA-14 | **UNKNOWN** | Endpoint `/tiingo/daily/<ticker>/prices` sans numéro de version ; aucune politique de versionnement publiée | S-T1 |

**Bloquants non résolus : PA-11, PA-14.**

#### E.3.2 Sharadar — Prices, Full History, Personal Use (L-06)

| Élément | PA | Score | Preuve | Source |
|---------|----|-------|--------|--------|
| Couverture ETF US | PA-01 | PASS | Table `funds` : ETF, CEF, ETN ; « Funds active or delisted from Nasdaq, NYSE, NYSEARCA, BATS and NYSEMKT » ; exemple `ticker=SPY,QQQ,IWM` | S-S1 |
| Profondeur daily | PA-03 | PASS | « History: December 1997 ». Le palier **Full History** est requis : « 10 Years » donnerait au plus ≈ 2 520 séances, donc aucune marge sur CONFIRMATORY (REV-D-04 retire 5 séances) | S-S1, S-S4 |
| Profondeur 15–20 ans homogène | PA-04 | UNKNOWN | ≈ 28 ans documentés ; homogénéité de source non documentée | — |
| `adjusted_close` | PA-02 | PASS | `closeadj` : « Close Price - Adjusted for Splits Dividends and Spinoffs » | S-S1 |
| Splits | — | PASS | « Adjustment Ratio = (New Float) / (Old Float) » | S-S3 |
| Distributions | — | PASS | « Adjustment Ratio = (Close Price + Dividend Amount) / (Close Price) » ; spinoffs couverts | S-S3 |
| Close brut | PA-06 | PASS | `closeunadj` : « Close Price - Unadjusted ». **Attention : `close` est ajusté des splits**, ce n'est pas le brut | S-S1, S-S5 |
| Événements sur titre | PA-06 | PASS | Table `actions` : splits, dividendes en numéraire, spinoffs, changements de ticker, depuis janvier 1998 | S-S2 |
| Méthodologie documentée | PA-05 | **UNKNOWN** | Formules publiées, ajustement « on a backwards basis », proportionnel, événements couverts ⇒ PASS sur ces points. Mais **la date de référence n'est jamais nommée** : la formule utilise la clôture « on that day » de l'événement. L'exemple AAPL du 2014-08-07 tombe sur l'ex-date, mais c'est une inférence, pas un énoncé | S-S3 |
| Dates / ex-dates | PA-05 | UNKNOWN | Idem | S-S3 |
| Correction / révision | PA-10 | UNKNOWN | Champ `lastupdated` par ligne, filtre `lastupdated.gte`, livraisons à 17 h 30 et 23 h 30 ET : un mécanisme qui rend les révisions observables (REV-D-03), mais aucune politique écrite | S-S1 |
| Identifiants stables | INS-05 | PASS | « we provide a permaticker in the tickers table that is Sharadar's own unchanging and unique identifier » | S-S5 |
| Fuseau / calendrier | PA-07 | PASS | `date` au format `YYYY-MM-DD` (« Price Date ») ; horaires de livraison en ET. Aucun calendrier fourni | S-S1 |
| Formats d'export | PA-08 | PASS | CSV (défaut), JSON, bulk CSV zippé ; schémas PostgreSQL/SQLite/MySQL publiés | S-S1 |
| Conservation locale | PA-08 | PASS | Téléchargements et bulk files explicitement prévus par la licence Personal Use | S-S1, S-S6 |
| Limites d'API | PA-12 | PASS | `limit` = 10 000 lignes par requête ; SPY depuis 1997 ≈ 7 200 lignes ⇒ une requête. Bulk download disponible | S-S1 |
| Coût | PA-13 | NOT_APPLICABLE | Prices Full History : 39 $/mois ou 299 $/an | S-S4 |
| Licence R&D personnelle | PA-09 | PASS | « Personal Use covers individuals using the data for their own purposes: research, backtesting ». **Conservation limitée à l'abonnement** : « Within thirty (30) days of termination, delete […] all copies of the Services Data ». Les résultats dérivés non reconstructibles peuvent être conservés | S-S5, S-S6 |
| Pas de raboutage non documenté | PA-11 | **UNKNOWN** | Sources amont des prix non documentées | — |
| Identité + version d'interface | PA-14 | PASS | API versionnée `/v1.0/` ; schéma par table ; `modified` du bulk file ; `lastupdated` par ligne | S-S1 |

**Bloquants non résolus : PA-05 (référence ex-date), PA-11.**

#### E.3.3 EODHD — EOD Historical Data All World, usage personnel (L-08)

| Élément | PA | Score | Preuve | Source |
|---------|----|-------|--------|--------|
| Couverture ETF US | PA-01 | PASS | Stocks, ETF, fonds ; VTI.US mesuré | S-E1 |
| Profondeur daily | PA-03 | PASS | Mesures fournisseur du 2026-09-17 : VTI.US depuis 2001-05-31, actions US depuis 1962 ; dividendes « over 30 years » pour les plans payants | S-E1, S-E2 |
| Profondeur 15–20 ans homogène | PA-04 | UNKNOWN | Voir PA-11 | — |
| `adjusted_close` | PA-02 | PASS | « Closing price adjusted for both splits and dividends » | S-E1 |
| Splits | — | PASS | Idem ; Splits API | S-E1, S-E2 |
| Distributions | — | PASS | Ex-dates et montants ; déclaration, record et paiement pour les grands tickers US | S-E2 |
| Close brut | PA-06 | PASS | `close` : « as traded — not adjusted » | S-E1 |
| Événements sur titre | PA-06 | PASS | Splits and Dividends API | S-E2 |
| Méthodologie documentée | PA-05 | PASS | « we use the Chicago Booth adjustment algorithm » ; facteur = (clôture de la veille de l'ex-date − dividende) / clôture de la veille ; « we keep 4 decimal places » | S-E3 |
| Dates / ex-dates | PA-05 | PASS | Ex-date explicite | S-E3 |
| Correction / révision | PA-10 | UNKNOWN | Seul énoncé : « Adjusted closes are recomputed, not stored » ; aucune politique de correction des prix bruts | S-E1 |
| Identifiants stables | INS-05 | UNKNOWN | Clé `SYMBOL.EXCHANGE` ; un ticker renommé perd son historique sous l'ancien symbole ; aucun identifiant permanent documenté dans l'API EOD. CUSIP/ISIN pris chez l'émetteur | S-E1 |
| Fuseau / calendrier | PA-07 | PASS | `date` : « Trading date, YYYY-MM-DD » ; NYSE/NASDAQ mis à jour « within 15 minutes after the market closes » | S-E1 |
| Formats d'export | PA-08 | PASS | CSV (défaut), JSON | S-E1 |
| Conservation locale | PA-08 | PASS | « Non-Professional Users are permitted to store, manipulate, and analyze the data for private, non-commercial purposes » ; aucune clause de suppression à la résiliation dans la section TERMINATION | S-E4 |
| Limites d'API | PA-12 | PASS | « One API key allows querying 100 000 API requests per day » ; « 1 call per request (any length of price history) » | S-E4, S-E1 |
| Coût | PA-13 | NOT_APPLICABLE | 19,99 $/mois ou 199 $/an | S-E5 |
| Licence R&D personnelle | PA-09 | PASS | Usage non professionnel, « solely in a personal capacity for their own personal investment activities » | S-E4 |
| Pas de raboutage non documenté | PA-11 | **UNKNOWN (indice défavorable)** | « We get USA data from Nasdaq Cloud API ». Le produit d'historique EOD que Nasdaq publie (U.S. Equity Daily History) ne remonte qu'à « January 2014 ». Le lien exact entre ce produit et la « Nasdaq Cloud API » n'est pas documenté, et l'origine de l'historique antérieur à 2014 non plus : jonction de sources possible vers 2014 | S-E6, S-E7 |
| Identité + version d'interface | PA-14 | **UNKNOWN** | Endpoint `/api/eod/{SYMBOL}` sans version ; pas de politique publiée | S-E1 |

**Bloquants non résolus : PA-11, PA-14.**

#### E.3.4 Alpha Vantage — Premium (L-04)

| Élément | PA | Score | Preuve | Source |
|---------|----|-------|--------|--------|
| Couverture ETF US | PA-01 | PASS | « global stock, ETF, or mutual fund symbols » | S-A1 |
| Profondeur daily | PA-03 | PASS | « covering 25+ years of historical data » | S-A1 |
| Profondeur 15–20 ans homogène | PA-04 | UNKNOWN | — | — |
| `adjusted_close` | PA-02 | PASS | `TIME_SERIES_DAILY_ADJUSTED` : « adjusted close values » | S-A1 |
| Splits / distributions | — | PASS | « historical split/dividend events » dans la réponse | S-A1 |
| Close brut | PA-06 | PASS | « raw (as-traded) daily open/high/low/close/volume » | S-A1 |
| Méthodologie documentée | PA-05 | **UNKNOWN** | « We adjust […] by both splits and cash dividend events, which is considered an industry standard methodology » — ni proportionnel/additif, ni date de référence | S-A2 |
| Correction / révision | PA-10 | UNKNOWN | — | — |
| Identifiants stables | INS-05 | UNKNOWN | Symbole uniquement | S-A1 |
| Fuseau / calendrier | PA-07 | **UNKNOWN** | Non documenté dans la référence consultée | S-A1 |
| Formats d'export | PA-08 | PASS | `datatype=json` ou `csv` | S-A1 |
| Conservation locale | PA-08 | **UNKNOWN** | La licence porte sur l'usage de la plateforme ; aucune clause explicite de conservation ; « Upon termination, User's access […] shall be deactivated » | S-A3 |
| Limites d'API | PA-12 | PASS | Premium à partir de 75 requêtes/min, « No daily limits » | S-A4 |
| Coût | PA-13 | NOT_APPLICABLE | À partir de 49,99 $/mois | S-A4 |
| Licence R&D personnelle | PA-09 | **UNKNOWN** | « personal, non-commercial use » ; droit de conservation non établi | S-A3 |
| Pas de raboutage non documenté | PA-11 | **UNKNOWN** | — | — |
| Identité + version d'interface | PA-14 | **UNKNOWN** | `/query?function=…` sans version | S-A1 |

**Bloquants non résolus : PA-05, PA-07, PA-08, PA-09, PA-11, PA-14.**

### E.4 Synthèse PA-01…PA-14

| PA | Niveau | Tiingo Power | Sharadar Full | EODHD All World | Alpha Vantage Premium |
|----|--------|--------------|---------------|-----------------|-----------------------|
| PA-01 | REQUIRED | PASS | PASS | PASS | PASS |
| PA-02 | REQUIRED | PASS | PASS | PASS | PASS |
| PA-03 | REQUIRED | PASS | PASS | PASS | PASS |
| PA-04 | RECOMMENDED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| PA-05 | REQUIRED | PASS | **UNKNOWN** | PASS | **UNKNOWN** |
| PA-06 | RECOMMENDED | PASS | PASS | PASS | PASS |
| PA-07 | REQUIRED | PASS | PASS | PASS | **UNKNOWN** |
| PA-08 | REQUIRED | PASS | PASS | PASS | **UNKNOWN** |
| PA-09 | REQUIRED | PASS | PASS | PASS | **UNKNOWN** |
| PA-10 | RECOMMENDED | PASS | UNKNOWN | UNKNOWN | UNKNOWN |
| PA-11 | REQUIRED | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |
| PA-12 | REQUIRED | PASS | PASS | PASS | PASS |
| PA-13 | à évaluer | 300 $/an | 299 $/an | 199 $/an | ≥ 49,99 $/mois |
| PA-14 | REQUIRED | **UNKNOWN** | PASS | **UNKNOWN** | **UNKNOWN** |
| **REQUIRED non résolus** | | 2 | 2 | 2 | 6 |

Différence non notée par la checklist, mais pertinente pour REP-05 : la **durée de conservation**
de la copie brute. Chez Tiingo et Sharadar, elle est bornée par l'abonnement (suppression à la
fin, dans les 30 jours pour Sharadar). EODHD autorise le stockage sans clause de suppression
publiée.

### E.5 Constats transverses

| ID | Constat | Conséquence |
|----|---------|-------------|
| F-01 | PA-11 est UNKNOWN pour **tous** les finalistes : aucun ne documente ses sources amont de prix EOD sur la fenêtre historique | Cause principale de l'INCONCLUSIVE ; le contrôle Q-11 ne suffira pas seul |
| F-02 | Sharadar et le standard CRSP ne calculent pas le facteur de dividende de la même façon. Sharadar : $(P_\tau + D)/P_\tau$ ⇒ $r_\tau = \ln\big((P_\tau + D)/P_{\tau-1}\big)$. CRSP (Tiingo, EODHD) : $(P_{\tau-1} - D)/P_{\tau-1}$ ⇒ $r_\tau = \ln\big(P_\tau/(P_{\tau-1} - D)\big)$ | Les deux formules sont causales (information connue à la clôture de $\tau$), donc admissibles (§9.2), mais elles donnent des $r_\tau$ différents : les snapshots ne sont pas interchangeables (§5.3). La formule doit être enregistrée dans le snapshot |
| F-03 | Tiingo sérialise la date en `T00:00:00.000Z` | Une conversion vers America/New_York décale d'un jour (TS-02/TS-04). Règle obligatoire : prendre le littéral `YYYY-MM-DD` |
| F-04 | Chez Sharadar, `close` est ajusté des splits | Le brut est `closeunadj` ; confondre les deux fausse ADJ-02 |
| F-05 | Aucun fournisseur ne livre un calendrier de marché versionné | CAL-01 exige une source de calendrier distincte, à choisir avant le loader |
| F-06 | Chez Tiingo et Sharadar, la conservation de la copie brute s'arrête avec l'abonnement | L'horizon de reproductibilité REP-05 = durée d'abonnement ; à accepter explicitement ou à éviter |
| F-07 | Sharadar : pas de palier « 10 Years » suffisant pour CONFIRMATORY avec marge | Seul Full History convient |

---

## Decision

### D-1 — Fournisseur : INCONCLUSIVE

Aucune offre ne satisfait l'ensemble des critères REQUIRED de DATA-REQ §10. **Aucun fournisseur
n'est sélectionné.** Aucune acquisition n'est autorisée par ce DR.

Trois finalistes restent en lice. Aucun n'a de FAIL, et chacun a exactement deux critères
REQUIRED non résolus :

| Finaliste | Critères à lever | Moyen de levée |
|-----------|------------------|----------------|
| Tiingo — Power | PA-11, PA-14 | Déclaration écrite du fournisseur sur les sources amont de l'historique SPY et sur le versionnement de l'interface EOD |
| Sharadar — Prices Full History | PA-05 (ex-date), PA-11 | Déclaration écrite que la date d'événement de `closeadj` est l'ex-date ; déclaration sur les sources amont |
| EODHD — EOD All World | PA-11, PA-14 | Déclaration écrite sur l'origine de l'historique SPY avant 2014 et l'existence éventuelle d'une jonction ; versionnement de l'interface |

Alpha Vantage Premium n'est pas éliminé (aucun FAIL), mais il a six critères REQUIRED non
résolus. Il n'est pas poursuivi en priorité.

Ce DR n'établit **aucune préférence** entre les trois finalistes. Une préférence ne peut
venir que des critères de DATA-REQ, et les critères bloquants qui les départageraient ne sont
pas résolus. Ni le prix, ni la popularité, ni la facilité d'intégration ne départagent.

### D-2 — Instrument : SPY

**Instrument I01 : SPY — State Street® SPDR® S&P 500® ETF Trust.** Coté sur NYSE Arca,
CUSIP `78462F103`, ISIN `US78462F1030`, devise USD.

Évaluation INS-* (sources émetteur) :

| ID | Niveau | Score | Preuve | Source |
|----|--------|-------|--------|--------|
| INS-01 | REQUIRED | PASS | Un seul instrument | — |
| INS-02 | REQUIRED | PASS | Coté NYSE Arca ; suit le S&P 500, « a diversified large cap U.S. index » | S-I1 |
| INS-03 | REQUIRED | PASS | « The Trust does not hold or trade futures or swaps » ; objectif : correspondre au prix et au rendement de l'indice avant frais (pas de levier, pas d'inverse) | S-I2, S-I1 |
| INS-04 | REQUIRED | PASS | Même trust coté depuis le 1993-01-22 ; seul le nom a changé (« formerly, SPDR® S&P 500® ETF Trust »). La continuité effective des cotations sera vérifiée par Q-05 | S-I1, S-I2 |
| INS-05 | REQUIRED | PASS | Ticker SPY + NYSE Arca + CUSIP 78462F103 + ISIN US78462F1030 | S-I1 |
| INS-06 | REQUIRED | PASS | « Trading Currency: USD », « Base Currency: USD » | S-I1 |
| INS-07 | REQUIRED / RECOMMENDED | PASS | Plus de 33 ans depuis la création ; ≥ 28 ans même avec la fenêtre la plus courte des finalistes (Sharadar, depuis décembre 1997) | S-I1, S-S1 |
| INS-08 | RECOMMENDED | UNKNOWN | Aucune statistique de volume consultée (volontairement) ; à mesurer au gate DATA | — |
| INS-09 | RECOMMENDED | PASS | Distributions trimestrielles en numéraire (« Distribution Frequency: Quarterly » ; versements « on the last Business Day of April, July, October and January ») | S-I1, S-I2 |

**Départage (§1.2).** Ont été considérés les ETF US exposés au S&P 500 :

| Candidat | Création | Source |
|----------|----------|--------|
| SPY | 1993-01-22 | S-I1 |
| IVV | 2000-05-15 | S-I3 |
| VOO | 2010-09-07 | S-I4 |

Le critère 1, **longueur d'historique propre**, suffit. L'émetteur indique que SPY « was the very
first exchange traded fund listed in the United States » (S-I1), donc aucun ETF US n'a un
historique plus long. Le classement ne change pas avec la fenêtre la plus courte des finalistes
(Sharadar, décembre 1997), puisque IVV et VOO sont postérieurs. Le critère 2 (vérifiabilité des
ajustements) n'a pas eu à être utilisé.

**Anti-snooping.** Le choix n'a utilisé que des métadonnées d'émetteur : date de création,
structure, identifiants, devise, fréquence de distribution. Aucune statistique dérivée de
$X_t$, $Y_t$, $\Delta_t$ ou $\mathcal{H}_\cdot$, aucun prix et aucun volume n'ont été consultés.
Changer d'instrument après un résultat = nouvelle investigation (§1.2).

**Dépendance à D-1.** D-2 ne présuppose aucun fournisseur. Pour le fournisseur retenu, PA-01
devra être confirmé au niveau de l'instrument, avec la première date disponible de SPY relevée
avant l'acquisition (endpoint meta chez Tiingo, table `tickers` chez Sharadar, bornes retournées
chez EODHD) et consignée dans le snapshot.

---

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| Accepter le finaliste le moins cher (EODHD) malgré PA-11 et PA-14 | Rejeté : un UNKNOWN sur un REQUIRED ne devient pas PASS, et PA-11 porte un indice défavorable (jonction possible vers 2014) |
| Réinterpréter PA-14 : « non versionné » = PASS si l'URL et la date sont enregistrées | Non retenu **ici**. Cela changerait le sens du critère et exige une révision explicite de DATA-REQ, pas une lecture silencieuse dans l'ADR |
| Lever PA-11 empiriquement au gate DATA (Q-11) | Insuffisant seul : Q-11 détecte les ruptures visibles, pas une jonction bien raccordée. Q-11 reste obligatoire après la levée documentaire |
| Recalculer soi-même l'ajustement à partir des dividendes Massive | Rejeté : PA-02 exige un `adjusted_close` fournisseur. Ce serait une méthodologie maison non spécifiée, à décider dans un autre DR |
| Deux sources (l'une pour l'historique ancien, l'autre pour le récent) | Rejeté : raboutage, soumis à Q-11 et exclu par §4.1 et §5.3 tant qu'il n'est pas prouvé cohérent |
| IVV ou VOO comme instrument | Rejeté au départage §1.2 (historique plus court) |
| QQQ, DIA ou autres ETF large-cap | Non retenus : historique plus court que SPY, qui est le premier ETF US ; le départage est donc clos |

## Rejected alternatives

- Tiingo Starter, Alpha Vantage gratuit, Sharadar gratuit, EODHD gratuit : FAIL REQUIRED (E.2).
  L'accès gratuit à une API ne vaut pas licence de conservation.
- Massive, Databento, Alpaca, Norgate, Yahoo/`yfinance` : FAIL REQUIRED ou interdiction §11 (E.2).
- Choisir un fournisseur « par défaut » pour débloquer l'implémentation : contraire à QDP
  (INCONCLUSIVE est un résultat normatif, pas un échec à contourner).

## Consequences

- **Aucune acquisition de données** n'est permise tant que D-1 n'est pas ACCEPTED.
- **SPY** est pré-enregistré comme instrument I01, indépendamment du fournisseur.
- Levée de D-1 : obtenir les déclarations écrites listées en D-1, les archiver comme preuves,
  re-noter les finalistes dans une révision de ce DR. Le statut passe à ACCEPTED seulement si un
  finaliste atteint PASS sur tous les REQUIRED.
- L'ordre prévu est maintenu : DR-003 ACCEPTED → C02 v1.1 → acquisition contrôlée → snapshot
  immuable → gate DATA → implémentation I01.
- Hypothèse de licence **A-1** : le projet est mené par un individu, pour de la R&D personnelle
  non commerciale. Si ce n'est pas le cas, les paliers notés ici ne s'appliquent pas (Tiingo
  Commercial, licence Sharadar professionnelle, EODHD commercial), et les PA-09 doivent être
  re-notés.

### Éléments requis pour C02 v1.1 (entrée pour DATA-GAP-01, non appliqués ici)

| Élément | Motif | Constat lié |
|---------|-------|-------------|
| `source.provider`, `source.product`, `source.plan` (palier de licence) | La licence dépend du palier | E.2, A-1 |
| `source.interface_version` (ou valeur explicite si non versionné, selon la future décision sur PA-14) | §7.1 | PA-14 |
| `source.endpoint` + paramètres de requête | Rejouer l'acquisition | REP-02 |
| `license.retention_terms` + `license.retention_until` (ex. fin d'abonnement + 30 j) | REP-05 | F-06 |
| `adjustment.events`, `adjustment.method = proportional`, `adjustment.reference_date = ex_date`, `adjustment.dividend_factor_formula` | §3.3, §5.3 | F-02 |
| `adjustment.vendor_reference` (ex. « CRSP », « Chicago Booth », URL du document) + date de consultation | ADJ-01 | E.3 |
| `fields.raw_close_field` (ex. `close`, `closeunadj`) et `fields.adjusted_close_field` | ADJ-02 | F-04 |
| `time.source_format` + `time.session_date_rule` (ex. « date littérale, sans conversion ») | TS-02/TS-03 | F-03 |
| `calendar.source` + `calendar.version` | CAL-01 | F-05 |
| `instrument.vendor_permanent_id` (permaTicker, permaticker) en plus du ticker, de la place, du CUSIP et de l'ISIN | INS-05 | E.3 |
| `vendor_revision_markers` (ex. `lastupdated` max, `modified` du bulk file, en-têtes HTTP) | REV-D-03 | PA-10 |
| `instrument.first_available_date` relevée avant l'acquisition | PA-01/PA-03 niveau instrument | D-2 |
| `numeric_precision` observée ou déclarée (ex. 4 décimales EODHD) | §3.3, Q-13 | E.3.3 |

## Deferred items

| ID | Objet | Déclencheur |
|----|-------|-------------|
| DEF-01 | Levée de PA-11 (les trois finalistes) | Réponses écrites des fournisseurs |
| DEF-02 | Levée de PA-14 (Tiingo, EODHD) ou révision explicite du critère dans DATA-REQ | Réponse fournisseur ou décision DATA-REQ v0.2 |
| DEF-03 | Levée de PA-05 (Sharadar, ex-date) | Réponse fournisseur |
| DEF-04 | Choix de la source de calendrier de marché versionnée (CAL-01) | Avant C02 v1.1 / loader |
| DEF-05 | Décision sur l'horizon de conservation (F-06) si Tiingo ou Sharadar est retenu | Avec l'ACCEPTED de D-1 |
| DEF-06 | Évaluation éventuelle des fournisseurs non examinés (FMP, Twelve Data, Intrinio, Barchart, Nasdaq Data Link) | Si aucun finaliste n'est levé |
| DEF-07 | Confirmation de l'hypothèse A-1 (usage individuel non commercial) | Avant souscription |

---

## Sources

Toutes consultées le 2026-09-23, sauf mention contraire.

| ID | Source officielle |
|----|-------------------|
| S-T1 | Tiingo — End-of-Day documentation (§2.1.1 Overview, §2.1.2, §2.1.3 Meta, changelog) — https://www.tiingo.com/documentation/end-of-day |
| S-T2 | Tiingo — Splits documentation (§2.11) — https://www.tiingo.com/documentation/corporate-actions/splits |
| S-T3 | Tiingo — Distributions documentation (champ `exDate`) — même module de documentation que S-T1 |
| S-T4 | Tiingo KB — « The Fastest Method to Ingest Tiingo End-of-Day Stock API Data » (mis à jour 2023-05-23) — https://www.tiingo.com/kb/article/the-fastest-method-to-ingest-tiingo-end-of-day-stock-api-data/ |
| S-T5 | Tiingo Blog — « Best Stock Price API » (source officielle à caractère promotionnel ; utilisée seulement pour la profondeur au niveau du jeu de données) — https://www.tiingo.com/blog/best-stock-price-api/ |
| S-T6 | Tiingo — Terms of Use (Last Updated 2026-08-05), §1.6, §7.3, §9.7 — https://app.tiingo.com/tos/ |
| S-T7 | Tiingo — Pricing — https://www.tiingo.com/about/pricing ; tableau des paliers : https://www.tiingo.com/blog/scaling-investment-processes-through-a-stock-api/ |
| S-S1 | Sharadar — Fund Prices documentation — https://sharadar.com/docs/funds |
| S-S2 | Sharadar — Corporate Actions documentation — https://sharadar.com/docs/actions |
| S-S3 | Sharadar — « Sharadar Stock Prices, Fund Prices and Adjustments » (2026-07-29, cité par la FAQ) — https://sharadar.com/blog/posts/sharadar-stock-prices-fund-prices-and-adjustments |
| S-S4 | Sharadar — Pricing — https://sharadar.com/pricing |
| S-S5 | Sharadar — FAQ — https://sharadar.com/docs/faqs |
| S-S6 | Sharadar — Terms of Use / License — https://sharadar.com/terms |
| S-S7 | Sharadar — page d'accueil (offre gratuite) — https://sharadar.com/ |
| S-E1 | EODHD — End-of-Day Historical Data API — https://eodhd.com/financial-apis/api-for-historical-data-and-volumes |
| S-E2 | EODHD — Splits and Dividends API — https://eodhd.com/financial-apis/api-splits-dividends |
| S-E3 | EODHD Academy — « Adjusted Close and Close: What's the Difference? » — https://eodhd.com/financial-academy/financial-faq/adjusted-close-and-close-whats-the-difference |
| S-E4 | EODHD — Terms and Conditions — https://eodhd.com/financial-apis/terms-conditions |
| S-E5 | EODHD — Pricing — https://eodhd.com/pricing |
| S-E6 | EODHD — Our Data Sources and Data Partners — https://eodhd.com/financial-apis/our-data-sources-and-data-partners |
| S-E7 | Nasdaq Data Link — U.S. Equity Daily History (USEDH) — https://data.nasdaq.com/databases/USEDH |
| S-A1 | Alpha Vantage — API documentation — https://www.alphavantage.co/documentation/ |
| S-A2 | Alpha Vantage — Support / FAQ — https://www.alphavantage.co/support/ |
| S-A3 | Alpha Vantage — Terms of Service — https://www.alphavantage.co/terms_of_service/ |
| S-A4 | Alpha Vantage — Premium — https://www.alphavantage.co/premium/ |
| S-M1 | Massive — Custom Bars (OHLC) — https://massive.com/docs/rest/stocks/aggregates/custom-bars |
| S-M2 | Massive FAQ — « Is Massive's stock data adjusted for splits or dividends? » — https://massive.com/knowledge-base/categories/faq |
| S-D1 | Databento — US Equities catalog — https://databento.com/catalog/us-equities |
| S-D2 | Databento — OHLCV schema — https://databento.com/docs/schemas-and-data-formats/ohlcv |
| S-L1 | Alpaca — Historical bars reference — https://docs.alpaca.markets/us/reference/stockbars |
| S-L2 | Alpaca — « Introducing Corporate Actions API: Announcements » — https://alpaca.markets/blog/introducing-corporate-actions-api-announcements/ |
| S-N1 | Norgate Data — Overview — https://norgatedata.com/ |
| S-N2 | Norgate Data — NDU Overview — https://norgatedata.com/ndu-overview.php |
| S-N3 | Norgate Data — FAQ — https://norgatedata.com/data-package-faq.php |
| S-Y1 | `yfinance` — README (avertissement légal du mainteneur) — https://github.com/ranaroussi/yfinance |
| S-C1 | WRDS — « What is WRDS? » — https://wrds-www.wharton.upenn.edu/pages/about/what-wrds/ |
| S-I1 | State Street — SPY product page et fact sheet (au 2026-06-30) — https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-500-etf-trust-spy |
| S-I2 | SEC EDGAR — SPY prospectus du 2026-01-26 — https://www.sec.gov/Archives/edgar/data/884394/000119312526022775/d77353d497.htm |
| S-I3 | iShares — IVV product page — https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf |
| S-I4 | Vanguard — VOO product page — https://advisors.vanguard.com/investments/products/voo/vanguard-sp-500-etf |

## Status

**INCONCLUSIVE.**

- D-1 (fournisseur) : INCONCLUSIVE. Trois finalistes, deux critères REQUIRED non résolus chacun ;
  aucun fournisseur sélectionné ; aucune acquisition autorisée.
- D-2 (instrument) : SPY pré-enregistré selon DATA-REQ §1.2 ; il devient opposable à
  l'acquisition dès que D-1 est ACCEPTED.

---

## Révision v1.1 (2026-09-24)

Ouverte depuis C02 v1.1 CLOSED (`1cda21f`). Cette révision **ne note aucun finaliste**.
Elle prépare uniquement les demandes écrites destinées à lever les UNKNOWN bloquants
(DEF-01, DEF-02, DEF-03). Le texte E.1–E.5, D-1, D-2 et les scores v1.0 restent l'autorité
historique de cette pièce.

Règles v1.1 :

- un UNKNOWN REQUIRED ne devient PASS que par une preuve datée (documentation officielle
  ou déclaration écrite du fournisseur archivée) ;
- une absence de réponse n'est pas un PASS ;
- « dernier survivant » n'est pas un critère ;
- le prix n'est pas négocié et ne départage pas ;
- DEF-04 (calendrier) est désormais porté par **DR-005**, investigation indépendante ;
  un échec ou un INCONCLUSIVE de DR-003 ne se compense pas par DR-005, et réciproquement ;
- l'acquisition n'est autorisée que si **D-1 ACCEPTED ∧ DR-005 ACCEPTED**.

Demandes : [DR-003-v1.1-vendor-inquiries.md](DR-003-v1.1-vendor-inquiries.md).
Statut global **inchangé : INCONCLUSIVE**.
