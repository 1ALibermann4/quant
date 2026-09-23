# DATA-REQ-I01 — Contrat d'entrée data de l'expérience I01

> **Identifier :** DATA-REQ-I01-v0.1
> **Status :** ACCEPTED
> **Authority class :** RESEARCH — data requirements
> **Protocol :** QDP v0.1
> **Dérivé de :** `protocol.md` v0.2, `hypothesis.md` v0.2, `configuration.yaml` v0.2 (re-review PASS @ `a882667`)
> **Contrat lié :** C02 DatasetSnapshot v1.0

Ce document dit **ce que les données doivent garantir** pour que I01 puisse produire un verdict SCI.
Il ne sélectionne **ni fournisseur, ni API, ni ticker**. La comparaison des sources se fera dans
un ADR distinct, contre la checklist du §10.

Niveaux d'exigence :

| Niveau | Sens |
|--------|------|
| **REQUIRED** | Absence ou violation ⇒ dataset non admissible pour I01 |
| **RECOMMENDED** | Renforce la vérifiabilité ; absence documentée, non bloquante |
| **OPTIONAL** | Utile en diagnostic seulement ; jamais consommé par l'endpoint SCI-001 |

---

## 1. Instrument

### 1.1 Exigences

| ID | Exigence | Niveau |
|----|----------|--------|
| INS-01 | Un seul instrument pour I01 (univarié) | REQUIRED |
| INS-02 | ETF coté aux États-Unis, exposé à un indice actions large-cap US | REQUIRED |
| INS-03 | Ni levier, ni inverse, ni produit synthétique à swap | REQUIRED |
| INS-04 | Cotation continue sur toute la fenêtre retenue (pas de fusion, liquidation, changement de fonds sous-jacent) | REQUIRED |
| INS-05 | Identifiants stables enregistrés : ticker + place de cotation + au moins un identifiant non-ticker (ISIN, CUSIP ou FIGI) | REQUIRED |
| INS-06 | Devise de cotation USD, constante sur la fenêtre | REQUIRED |
| INS-07 | Historique disponible ≥ 10 ans (cible confirmatoire §4) ; ≥ 15–20 ans préféré | REQUIRED (10 ans) / RECOMMENDED (15–20 ans) |
| INS-08 | Liquidité élevée et continue (volume quotidien médian élevé, aucune séance sans échange sur la fenêtre) | RECOMMENDED |
| INS-09 | Distributions en numéraire ; événements sur titre (splits, etc.) documentés | RECOMMENDED |

La liquidité (INS-08) n'est pas nécessaire à la validité SCI. Elle est demandée pour que les
prix de clôture soient des prix réellement échangés et pour que l'instrument reste comparable aux
phases PRED et ECON.

### 1.2 Règles de sélection (anti data-snooping)

- Le ticker est choisi dans l'ADR source, **pas ici**.
- Le choix ne doit utiliser **aucune statistique dérivée des objets I01** ($X_t$, $Y_t$, $\Delta_t$,
  $\mathcal{H}_\cdot$). Seuls les critères INS-* et la qualité des données (§6) sont admissibles.
- Si plusieurs instruments satisfont INS-*, le départage se fait sur la **longueur d'historique
  propre** puis sur la **vérifiabilité des ajustements** (§5), et il est enregistré avant toute
  exécution.
- Changer d'instrument après avoir vu un résultat = **nouvelle investigation**, pas une révision d'I01.

---

## 2. Granularité, séance et convention temporelle

### 2.1 Définition d'une séance

| ID | Exigence | Niveau |
|----|----------|--------|
| GRA-01 | Barres **daily**, une observation par séance régulière | REQUIRED |
| GRA-02 | Une **séance** = une journée de négociation régulière du marché primaire US (heures régulières, hors pré/post-marché) | REQUIRED |
| GRA-03 | Les séances à clôture anticipée (early close) sont des séances valides ; leur clôture est la clôture anticipée | REQUIRED |
| GRA-04 | Le prix de séance est le **prix de clôture officiel** de la séance régulière, avant ajustement (§5 pour l'ajusté) | REQUIRED |

### 2.2 Calendrier de référence

| ID | Exigence | Niveau |
|----|----------|--------|
| CAL-01 | Un calendrier de marché de référence est identifié et versionné dans le snapshot (source + version) | REQUIRED |
| CAL-02 | Le calendrier couvre les jours fériés **et** les fermetures exceptionnelles non planifiées (événements, deuils nationaux, intempéries) | REQUIRED |
| CAL-03 | Toute séance attendue par le calendrier et absente des données est une **séance manquante** (§6), jamais ignorée | REQUIRED |
| CAL-04 | L'indexation temporelle d'I01 ($W$, $M$, $h$, $\tau$, $s+h$) se fait en **rang de séance du calendrier**, pas en numéro de ligne du fichier | REQUIRED |

CAL-04 est la conséquence directe de DEC-02 : si une séance manque, compter en lignes ferait
« sauter » un jour et fausserait silencieusement $s+h \leq t$ et la longueur des fenêtres.

### 2.3 Timestamp et timezone

| ID | Exigence | Niveau |
|----|----------|--------|
| TS-01 | Clé canonique d'une observation = **`session_date`** : date ISO 8601 (`YYYY-MM-DD`) de la séance, dans le fuseau de la place (America/New_York) | REQUIRED |
| TS-02 | Si la source fournit un instant (datetime) et non une date, la règle de conversion vers `session_date` est documentée et **vérifiée** sans décalage de jour | REQUIRED |
| TS-03 | Fuseau source et fuseau canonique enregistrés dans le snapshot | REQUIRED |
| TS-04 | Aucune conversion implicite UTC ↔ local qui pourrait déplacer une séance d'un jour | REQUIRED |

TS-02/TS-04 visent un défaut courant : un timestamp à minuit UTC converti en heure de New York
devient la veille, ce qui décale toute la série d'une séance.

### 2.4 `after_close_of_t` sans ambiguïté

Pour une requête à la séance $t$ :

$$
\texttt{query.information\_cutoff}(t) = \text{instant de clôture officielle de la séance } t
$$

(16:00 America/New_York en séance normale, heure de clôture anticipée sinon.)

- $P_t$ et $r_t$ sont disponibles à `information_cutoff(t)` ⇒ ils peuvent entrer dans $X_t$ (DEC-04).
- $Y_t^{(h)}$ commence à la séance $t+1$ du calendrier.
- Pour un candidat $s$ : `candidate.future_end(s)` = instant de clôture de la séance de rang $s+h$.

Le jeu de données doit permettre de calculer ces deux instants pour toute séance (CAL-01 + TS-01).

---

## 3. Champs

### 3.1 Champs par observation

| Champ | Niveau | Justification |
|-------|--------|---------------|
| `session_date` | REQUIRED | Clé temporelle (TS-01) |
| `adjusted_close` | REQUIRED | Seule entrée numérique de $X_t$ et $Y_t$ |
| `close` (non ajusté) | RECOMMENDED | Permet de recalculer et vérifier les facteurs d'ajustement (§5.4) |
| `volume` | OPTIONAL | Diagnostic de qualité uniquement (séance fictive à volume nul, INS-08) |
| `open`, `high`, `low` | Non demandé | Aucun usage dans I01 v0.2 |

### 3.2 Événements sur titre (niveau dataset)

| Élément | Niveau | Justification |
|---------|--------|---------------|
| Liste des splits (date d'effet, ratio) | RECOMMENDED | Vérification §5.4 et contrôle Q-07 |
| Liste des distributions (ex-date, montant, type) | RECOMMENDED | Vérification §5.4 |

### 3.3 Métadonnées nécessaires à l'interprétation de `adjusted_close`

| Métadonnée | Niveau |
|------------|--------|
| Événements couverts par l'ajustement (splits, distributions en numéraire, autres) | REQUIRED |
| Méthode : proportionnelle (multiplicative) ou additive | REQUIRED |
| Date de référence de l'ajustement (ex-date vs date de paiement) | REQUIRED |
| Formule du facteur de distribution si publiée | RECOMMENDED |
| Version / date de la méthodologie fournisseur | RECOMMENDED |
| Précision numérique des valeurs livrées (décimales, arrondi) | REQUIRED |
| Devise | REQUIRED |

---

## 4. Profondeur

### 4.1 Paliers

Profondeur mesurée en **séances du calendrier de référence couvertes par des `adjusted_close`
valides**, et en **durée calendaire** entre la première et la dernière séance.

| Palier | Séances | Durée | Usage |
|--------|---------|-------|-------|
| `TECHNICAL` | ≥ 1 500 | ~6 ans | Faire tourner le pipeline ; aucun verdict SCI autre qu'INCONCLUSIVE |
| `CONFIRMATORY` | ≥ 2 520 | **et** ≥ 10 ans | Seuil minimal pour SCI-001 confirmatoire |
| `PREFERRED` | 3 780 – 5 040 | 15 – 20 ans | Cible souhaitée, sans changement de méthodologie data |

`PREFERRED` n'est admissible que si la méthodologie d'ajustement et la source sont **homogènes sur
toute la fenêtre** (Q-11). Un historique plus long obtenu en raboutant des sources hétérogènes ne
vaut pas mieux qu'un historique plus court homogène.

### 4.2 Taille exploitable (dérivée du protocole)

Avec $M=252$, $W=20$, $h=10$, $\tau=20$, $k=50$, $L_\min=150$, sur $N$ séances indexées
$0 \ldots N-1$ :

- $X_s$ valide à partir du rang $M = 252$ (il faut $r_1 \ldots r_{252}$) ;
- $|\mathcal{L}_t| = t - \tau - M \geq 150$ ⇒ premier $t$ évaluable au rang **422** ;
- $Y_t$ complet ⇒ dernier $t$ évaluable au rang $N - 1 - h$ ;
- $|\mathcal{T}_\text{eval}| = N - 432$ ; split test $\approx 20\,\%$.

| $N$ (séances) | $\|\mathcal{T}_\text{eval}\|$ | Test | Blocs test ($L=30$) |
|---------------|-------------------------------|------|---------------------|
| 1 500 | 1 068 | ~214 | ~7 |
| 2 520 | 2 088 | ~418 | ~14 |
| 3 780 | 3 348 | ~670 | ~22 |
| 5 040 | 4 608 | ~922 | ~31 |

Ces chiffres supposent **zéro séance manquante** ; chaque séance manquante invalide en plus les
fenêtres qui la traversent (§6). La revue v0.2 estimait ~15 blocs à 10 ans ; le calcul exact avec
$L_\min = 150$ donne ~14. Cela ne change pas la conclusion : 10 ans reste un minimum crédible,
15–20 ans restent préférables.

### 4.3 Comportement si la cible n'est pas atteinte

Le **usage prévu** (`intended_use` ∈ {`technical`, `confirmatory`}) est déclaré dans le snapshot
**avant** l'évaluation du gate DATA.

| Usage déclaré | Palier obtenu | Gate DATA | Conséquence |
|---------------|---------------|-----------|-------------|
| `confirmatory` | `CONFIRMATORY` ou `PREFERRED` | évalué normalement | SCI-001 peut conclure |
| `confirmatory` | `TECHNICAL` | **DATA-FAIL** | Aucun run confirmatoire |
| `technical` | `TECHNICAL` ou plus | évalué normalement | Runs étiquetés techniques ; SCI-001 plafonné à INCONCLUSIVE |
| tout usage | < 1 500 séances | **DATA-FAIL** | Aucun run |

Il est interdit de requalifier un snapshot de `confirmatory` en `technical` après avoir constaté
qu'il est trop court pour produire un run « présentable ». Le palier obtenu est écrit dans le
snapshot et recopié dans les artefacts C01.

---

## 5. Ajustements

### 5.1 Ce que `adjusted_close` doit corriger

| Événement | Niveau |
|-----------|--------|
| Splits et regroupements (reverse splits) | REQUIRED |
| Distributions en numéraire (dividendes, distributions de fonds) | REQUIRED |
| Autres événements sur titre (spin-off, distributions en nature) | REQUIRED si présents sur la fenêtre ; documentés sinon |

Un ajustement **uniquement pour les splits** n'est pas admissible : chaque ex-date produirait un
saut négatif artificiel dans $r_t$, donc dans $X_t$ et $Y_t$.

### 5.2 Méthode

| Méthode | Admissibilité |
|---------|---------------|
| Proportionnelle (facteur multiplicatif appliqué à l'historique antérieur) | **Admissible** |
| Additive (soustraction d'un montant) | **Non admissible** (DATA-FAIL) |
| Non documentée / non déterminable | **DATA-INCONCLUSIVE** |

### 5.3 Pas d'hypothèse d'équivalence entre fournisseurs

Deux sources peuvent livrer des `adjusted_close` différents pour le même instrument (formule du
facteur de distribution, date de référence, arrondi, couverture des événements). Conséquences :

- la méthodologie est une propriété **du snapshot**, enregistrée avec lui ;
- deux snapshots de sources différentes ne sont pas interchangeables dans un même run ;
- mélanger des sources dans une même série = raboutage, soumis à Q-11.

### 5.4 Vérifiabilité

| ID | Exigence | Niveau |
|----|----------|--------|
| ADJ-01 | Méthodologie identifiable (document fournisseur ou description vérifiable) | REQUIRED |
| ADJ-02 | Si `close` non ajusté + événements sont disponibles, les facteurs sont recalculés et comparés à `adjusted_close` (écart relatif toléré ≤ $10^{-6}$ hors arrondi déclaré) | RECOMMENDED |
| ADJ-03 | Sans ADJ-02, l'ajustement repose sur l'attestation du fournisseur : WARN documenté | — |

### 5.5 Révisions historiques

| ID | Exigence | Niveau |
|----|----------|--------|
| REV-D-01 | Les séries back-adjustées sont supposées **révisables** (chaque nouvel événement change les niveaux passés) | REQUIRED (hypothèse de travail) |
| REV-D-02 | Un snapshot n'est jamais mis à jour en place ; une nouvelle acquisition = nouveau `snapshot_id` | REQUIRED |
| REV-D-03 | Si deux acquisitions de la même source diffèrent au-delà de l'effet attendu des nouveaux événements, l'écart est documenté avant tout usage | RECOMMENDED |
| REV-D-04 | Les dernières séances proches de la date d'acquisition peuvent être provisoires : la fenêtre utilisée s'arrête au moins **5 séances** avant l'acquisition | RECOMMENDED |

---

## 6. Qualité — contrôles d'acceptation

Classes de sortie :

| Classe | Effet sur le gate DATA |
|--------|------------------------|
| **REJECT** | DATA-FAIL |
| **INCONCLUSIVE** | DATA-INCONCLUSIVE (si aucun REJECT) |
| **WARN** | Consigné dans `quality_flags` ; n'empêche pas DATA-PASS |

Aucune séance n'est jamais **comblée** (pas d'interpolation, pas de report de la veille). Une
séance manquante invalide toute fenêtre $X$ ou $Y$ qui la contient ; le nombre de fenêtres
invalidées est publié.

Les seuils ci-dessous sont **pré-enregistrés** par ce document. Les modifier après inspection
d'un snapshot exige une décision explicite et un nouveau snapshot évalué.

| ID | Contrôle | Mesure | REJECT | INCONCLUSIVE | WARN |
|----|----------|--------|--------|--------------|------|
| Q-01 | `session_date` dupliquées | nombre de dates répétées | doublons à valeurs différentes | — | doublons strictement identiques (dédoublonnage consigné) |
| Q-02 | Ordre temporel | nombre d'inversions | — | — | série non triée mais sans doublon (tri consigné) |
| Q-03 | Valeurs nulles / non numériques | nombre et rang | valeur non interprétable comme nombre (corruption de format) | — | valeurs nulles/NaN : traitées comme séances manquantes (Q-05) |
| Q-04 | Prix non positifs ou non finis | `adjusted_close` ≤ 0, ±∞ | ≥ 1 occurrence | — | — |
| Q-05 | Séances manquantes vs calendrier | taux $m$ et plus longue suite $g$ | $m > 1\,\%$ ou $g > 5$ | $0{,}1\,\% < m \leq 1\,\%$ ou $2 \leq g \leq 5$ | $0 < m \leq 0{,}1\,\%$ et $g = 1$ |
| Q-06 | Séances hors calendrier | dates présentes mais non ouvrées | décalage systématique (majorité des dates hors calendrier ⇒ erreur de fuseau) | dates isolées hors calendrier portant une valeur | — |
| Q-07 | Discontinuités suspectes | $\|r_t\|$ | $\|r_t\| \geq 0{,}20$ **et** saut compatible avec un ratio de split non ajusté ($\|r_t - \ln q\| < 0{,}01$ pour $q \in \{2, 3, 4, 1/2, 1/3, 1/4, 3/2, 2/3\}$) | $\|r_t\| \geq 0{,}20$ sans explication documentée | $0{,}10 \leq \|r_t\| < 0{,}20$ (liste publiée, chaque cas relié à un événement de marché connu) |
| Q-08 | Prix figés | suites de `adjusted_close` identiques | — | suite ≥ 3 séances consécutives | suite de 2 séances |
| Q-09 | Couverture temporelle | séances valides, durée calendaire | selon §4.3 | — | palier `TECHNICAL` en usage `technical` |
| Q-10 | Cohérence calendrier | séances à clôture anticipée présentes, jours ouvrés corrects | — | calendrier de référence non versionné (CAL-01) | — |
| Q-11 | Homogénéité de source et de méthode | raboutage, changement de méthodologie ou de précision sur la fenêtre | raboutage non documenté détecté | raboutage documenté sans preuve de cohérence au point de jonction | changement de précision numérique documenté |
| Q-12 | Devise | devise constante USD | devise non USD ou mixte | devise non déclarée | — |
| Q-13 | Quantification | taux de $r_t = 0$ exact | — | — | taux > 2 % (arrondi excessif suspect) |
| Q-14 | Méthodologie d'ajustement | §5.1–5.2 | additive, ou splits seuls | non déterminable | ADJ-03 (attestation seule) |

Pour un ETF large-cap US, un rendement quotidien de 20 % en valeur absolue n'a pas d'équivalent
historique plausible : Q-07 le traite comme une erreur de donnée tant qu'il n'est pas expliqué.
Le seuil de 10 % en WARN couvre les séances extrêmes réelles (krachs), qui doivent rester dans la
série mais être listées.

---

## 7. C02 — métadonnées minimales du DatasetSnapshot

### 7.1 Métadonnées exigées par I01

| Métadonnée | Niveau |
|------------|--------|
| Identité de la source : fournisseur, produit/jeu de données, version d'interface | REQUIRED |
| Identifiants instrument (INS-05) | REQUIRED |
| Instant d'acquisition (UTC) | REQUIRED |
| Intervalle demandé (première et dernière `session_date`) | REQUIRED |
| Intervalle retourné (première et dernière `session_date` effectives) | REQUIRED |
| Fuseau source et fuseau canonique (TS-03) | REQUIRED |
| Calendrier de référence + version (CAL-01) | REQUIRED |
| Méthodologie d'ajustement (§3.3, §5) + version si disponible | REQUIRED |
| Empreinte cryptographique des **données brutes** telles que reçues | REQUIRED |
| Empreinte cryptographique de la **table canonique** (après transformations) | REQUIRED |
| Provenance des transformations : liste ordonnée (parsing, conversion de date, tri, dédoublonnage), avec version du code | REQUIRED |
| Nombre d'observations (brutes, canoniques, séances manquantes, séances invalidées) | REQUIRED |
| Bornes temporelles de la table canonique | REQUIRED |
| Version du schéma de la table canonique | REQUIRED |
| `availability_cutoff` = instant de clôture de la dernière séance incluse | REQUIRED |
| `intended_use` et palier de profondeur (§4.3) | REQUIRED |
| Résultats des contrôles Q-01…Q-14 et verdict DATA | REQUIRED |
| Licence / droits de conservation de la copie brute | REQUIRED |

### 7.2 Correspondance avec C02 v1.0

| Métadonnée | Champ C02 v1.0 | Couverture |
|------------|----------------|------------|
| Identité de la source | `provenance.source_label` | Partielle — une seule chaîne |
| Identifiants instrument | `instruments: list[str]` | Partielle — pas de structure ticker/place/ISIN |
| Instant d'acquisition | `as_of` (instant de figement) | Partielle — figement ≠ acquisition |
| Intervalle demandé | — | **Absent** |
| Intervalle retourné | `provenance.time_range_start/end` | Couvert |
| Fuseaux | — | **Absent** |
| Calendrier de référence | — | **Absent** |
| Méthodologie d'ajustement | `adjustments: list[AdjustmentRecord]` | Partielle — pas de méthode ni de version |
| Empreinte brute + canonique | `fingerprint` (unique) | Partielle — une seule empreinte |
| Provenance des transformations | — | **Absent** |
| Comptages | — | **Absent** |
| Version du schéma | `contract_version` (version du contrat, pas du contenu) | **Absent** |
| `availability_cutoff` | `availability_cutoff` | Couvert |
| `intended_use`, palier, verdict DATA | `quality_flags` (texte libre) | Partielle |
| Licence | — | **Absent** |

### 7.3 Écarts à traiter (non corrigés ici)

| ID | Constat | Conséquence | Action proposée |
|----|---------|-------------|-----------------|
| DATA-GAP-01 | C02 v1.0 ne peut pas porter toutes les métadonnées REQUIRED du §7.1 | Un snapshot I01 conforme ne serait pas représentable sans champs ad hoc | Proposer **C02 v1.1** (ajouts compatibles) — décision à enregistrer **avant l'implémentation** du chargeur ; non bloquant pour l'ADR source |
| DATA-GAP-02 | Le YAML C02 v1.0 énonce « `availability_cutoff <= as_of` is invalid → reject », alors que le code et les tests rejettent l'inverse (`availability_cutoff > as_of`) | Spécification contradictoire avec l'implémentation ; le code est correct | Corriger le texte du YAML dans la même révision que DATA-GAP-01 |

### 7.4 Immuabilité

- Le snapshot consommé par une expérience est **immuable** (C02 postcondition).
- Il est adressé par son empreinte canonique ; l'empreinte est vérifiée au chargement, et tout
  écart interrompt le run.
- La copie brute reçue est conservée à côté de la table canonique, pour permettre de rejouer les
  transformations.

---

## 8. Reproductibilité

| ID | Exigence | Niveau |
|----|----------|--------|
| REP-01 | Un run scientifique I01 lit **uniquement** un DatasetSnapshot identifié par empreinte ; il n'appelle aucune API et n'accède pas au réseau | REQUIRED |
| REP-02 | L'acquisition (appel source → snapshot) est une étape séparée, antérieure et journalisée | REQUIRED |
| REP-03 | Une révision ultérieure des données du fournisseur ne modifie aucun run existant : elle produit au mieux un nouveau snapshot, donc un nouveau `experiment_run_id` | REQUIRED |
| REP-04 | Les règles de canonisation servant au calcul de l'empreinte (ordre des lignes, représentation numérique, encodage) sont fixées et versionnées avec le schéma | REQUIRED |
| REP-05 | La licence de la source autorise la conservation locale de la copie brute pour la reproductibilité de la recherche | REQUIRED |

Le format de stockage (CSV, Parquet, autre) n'est pas choisi ici ; REP-04 impose seulement que
sa représentation canonique soit déterministe.

---

## 9. Anti-look-ahead

### 9.1 Invariant opérationnel

Pour toute requête $t$ et tout candidat $s \in \mathcal{L}_t$ :

```text
candidate.future_end <= query.information_cutoff
clôture(séance de rang s+h) <= clôture(séance de rang t)
```

Il est vérifiable si et seulement si :

- les rangs de séance viennent du calendrier de référence (CAL-04) ;
- `session_date` est exacte, sans décalage de fuseau (TS-01…TS-04) ;
- les heures de clôture, anticipées comprises, sont connues (GRA-03, CAL-01).

Au niveau du dataset : toute séance utilisée est antérieure ou égale à `availability_cutoff`, et
`availability_cutoff` ≤ `as_of` (C02).

### 9.2 Risques de look-ahead liés aux ajustements

Une série back-adjustée à la date d'acquisition contient, dans ses **niveaux**, des événements
postérieurs à chaque séance passée. Pour I01 :

- **Méthode proportionnelle** : $\mathrm{Adj}_\tau = P_\tau \cdot F_\tau$, où $F_\tau$ est le
  produit des facteurs des événements d'ex-date postérieure à $\tau$. Pour deux séances
  consécutives, $F_{\tau-1} = F_\tau \cdot f_\tau$ (avec $f_\tau = 1$ s'il n'y a pas d'événement
  en $\tau$), donc

$$
r_\tau = \ln\frac{\mathrm{Adj}_\tau}{\mathrm{Adj}_{\tau-1}} = \ln\frac{P_\tau}{P_{\tau-1}\, f_\tau}
$$

  Le rendement ne dépend que de l'événement de la séance $\tau$, pas des événements ultérieurs.
  Comme I01 ne consomme que des rendements (et une standardisation invariante d'échelle), le
  back-adjustment proportionnel **n'introduit pas de look-ahead** dans $X_t$ ni dans $Y_t$.
- **Condition** : le facteur $f_\tau$ ne doit utiliser que des informations connues à la clôture
  de $\tau$ (montant déclaré, prix de la veille). Un facteur calculé avec des prix postérieurs à
  l'ex-date serait un look-ahead (Q-14 ⇒ INCONCLUSIVE si non déterminable).
- **Méthode additive** : le rendement dépend du niveau ajusté, donc des événements futurs
  ⇒ non admissible (§5.2).
- **Ajustement à la date de paiement au lieu de l'ex-date** : pas un look-ahead, mais un saut
  mal daté ⇒ contrôlé par ADJ-02 quand c'est possible, sinon documenté.
- **Arrondi des niveaux anciens** : dépend de la date d'acquisition ; menace la reproductibilité
  entre snapshots (REV-D-02), pas la causalité.

Conclusion : I01 v0.2 **ne requiert pas** de prix point-in-time, à condition que la méthode soit
proportionnelle, datée à l'ex-date et documentée. Toute phase future qui consommerait des
**niveaux** de prix (et non des rendements) devra réexaminer ce point.

---

## 10. Critères d'acceptation d'une source

Checklist utilisée par l'ADR de sélection. Ce document ne note et ne classe aucune source.

| ID | Critère | Niveau | Preuve attendue |
|----|---------|--------|-----------------|
| PA-01 | Couvre un instrument satisfaisant INS-01…INS-06 | REQUIRED | Identifiants + dates de disponibilité |
| PA-02 | Fournit `adjusted_close` daily par séance régulière | REQUIRED | Documentation + échantillon de schéma |
| PA-03 | Profondeur ≥ 2 520 séances et ≥ 10 ans pour l'instrument | REQUIRED | Première date disponible documentée |
| PA-04 | Profondeur 15–20 ans avec méthode homogène | RECOMMENDED | Documentation de la couverture historique |
| PA-05 | Méthodologie d'ajustement publiée : événements couverts, méthode proportionnelle, référence ex-date | REQUIRED | Document méthodologique |
| PA-06 | Mise à disposition du `close` non ajusté et des événements (splits, distributions) | RECOMMENDED | Documentation des endpoints ou fichiers |
| PA-07 | Convention de date / fuseau documentée ou déterminable sans ambiguïté | REQUIRED | Documentation + règle TS-02 |
| PA-08 | Export des données brutes telles que reçues, conservables localement | REQUIRED | Conditions d'utilisation |
| PA-09 | Licence compatible avec un usage de recherche et la conservation locale (REP-05) | REQUIRED | Texte de licence |
| PA-10 | Politique de révision / correction des historiques documentée | RECOMMENDED | Documentation |
| PA-11 | Pas de raboutage de sources non documenté sur la fenêtre (Q-11) | REQUIRED | Documentation de l'historique de la source |
| PA-12 | Limites d'accès (quotas, taux) compatibles avec une acquisition unique de la série complète | REQUIRED | Documentation des limites |
| PA-13 | Coût compatible avec la phase R&D | À évaluer dans l'ADR | Grille tarifaire |
| PA-14 | Identité et version de l'interface enregistrables dans le snapshot (§7.1) | REQUIRED | Documentation de versionnement |

Une source qui échoue un critère REQUIRED est écartée pour I01, quel que soit son score sur les
autres critères.

---

## 11. Hors périmètre I01

| Élément | Raison |
|---------|--------|
| Temps réel, streaming, WebSocket | I01 est une étude historique hors ligne ; REP-01 interdit même l'accès réseau pendant un run |
| Tick data, intraday | $X_t$ et $Y_t$ sont définis en séances daily ; l'intraday exige un autre protocole (DEC-04) |
| Carnet d'ordres, bid/ask | Pertinents pour ECON/exécution, pas pour l'homogénéité SCI |
| API broker | Interdit avant P6 (QDP) |
| Actualités, sentiment | Absents de la définition de $X_t$ |
| Données fondamentales | Absentes de la définition de $X_t$ |
| OHLC, volume comme entrées | Non consommés par I01 v0.2 (volume seulement OPTIONAL en diagnostic) |
| Univers multi-actifs, survivorship | I01 est univarié (INS-01) |

Ajouter l'un de ces éléments demande une justification scientifique dans une nouvelle version du
protocole, pas une opportunité offerte par une API.

---

## 12. Gate DATA

Évalué sur un snapshot figé, pour l'usage déclaré (§4.3).

| Verdict | Condition |
|---------|-----------|
| **DATA-PASS** | Aucun contrôle REJECT ; aucun contrôle INCONCLUSIVE ; toutes les exigences REQUIRED des §1–§9 satisfaites ; palier de profondeur conforme à l'usage déclaré ; métadonnées §7.1 complètes ; empreintes présentes et vérifiées |
| **DATA-FAIL** | Au moins une violation certaine d'une exigence bloquante : contrôle REJECT, méthode d'ajustement non admissible, palier insuffisant pour l'usage déclaré, instrument hors INS-* |
| **DATA-INCONCLUSIVE** | Aucun REJECT, mais qualité ou provenance insuffisamment démontrée : contrôle INCONCLUSIVE, méthodologie non déterminable, calendrier non versionné, raboutage non prouvé cohérent |

Conséquences :

- Un verdict SCI I01 ne peut être produit que sur un snapshot **DATA-PASS**.
- Sur un snapshot DATA-INCONCLUSIVE ou DATA-FAIL, seul le développement du pipeline est permis ;
  ses résultats ne sont ni rapportés ni interprétés.
- Le verdict DATA et la liste des WARN sont recopiés dans les artefacts C01 du run.

Identifiants de gate : `DATA-I01-001` (verdict global), `DATA-I01-Q01` … `DATA-I01-Q14` (contrôles).

---

## 13. Cohérence avec les documents d'autorité

| Point | Source | Statut |
|-------|--------|--------|
| Champs `timestamp` + `adjusted_close` | protocol §9.1, config `data_requirements.fields` | Cohérent ; `timestamp` précisé en `session_date` (TS-01) |
| Paliers 1 500 / 2 520 / 3 780–5 040 | protocol §7.3, §9.2, config | Cohérent ; ajout de la condition de durée ≥ 10 ans et de `intended_use` |
| SCI-001 INCONCLUSIVE si < 10 ans | protocol §8 | Cohérent avec §4.3 |
| `after_close_of_t`, $Y$ à $t+1$ | hypothesis §3, config `temporal_convention` | Cohérent ; instants de clôture explicités (§2.4) |
| $s+h \leq t$ | hypothesis §4.5, protocol §3 | Cohérent ; rendu vérifiable par CAL-04 |
| Métadonnées C02 (`adjustment_policy`, `vendor_revision`, `fingerprint`) | protocol §9.3, config `c02_required_metadata` | Étendues par §7.1 ; config à aligner lors de C02 v1.1 |
| C02 v1.0 | `specs/contracts/C02/C02_v1.0.yaml` | Insuffisant — DATA-GAP-01, DATA-GAP-02 |
| protocol §9.4 « non produit dans l'intervention courante » | protocol v0.2 | Mention devenue caduque ; sans effet normatif |

---

## 14. Étape suivante

```text
DATA-REQ-I01 (ce document)
  → ADR sélection de source : comparer les sources 2026 à la checklist §10, choisir l'instrument (§1.2)
  → C02 v1.1 (DATA-GAP-01/02), avant l'implémentation du chargeur
  → acquisition d'un snapshot + gate DATA
  → implémentation pipeline I01
```

**STOP après DATA-REQ-I01** — aucune donnée téléchargée, aucune API contactée, aucun fournisseur
ni ticker sélectionné, aucune implémentation.
