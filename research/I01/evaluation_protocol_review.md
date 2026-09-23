# I01 — Revue de cohérence contradictoire du protocole

> **Identifier :** I01-REVIEW-v0.1
> **Status :** CLOSED
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Reviewer stance :** indépendant — objectif = invalider le protocole avant data/impl
> **Documents examinés :** `hypothesis.md`, `protocol.md`, `configuration.yaml` @ `49bb65c`
> **Verdict revue :** **INCONCLUSIVE**

---

## 0. Synthèse exécutive

Le cadrage I01 est **scientifiquement bien orienté** (H₀/H₁ claires, B0 obligatoire, split test,
pas de trading). En revanche, une revue adversarial identifie **2 BLOCKER**, **7 MAJOR**, **4 MINOR**
et **3 NOTE** qui empêchent de dériver `DATA-REQ-I01.md` sans ambiguïté.

Points les plus critiques :

1. **Inférence temporelle** — les $\Delta_t$ ne sont pas iid ; un t-test (même « apparié ») est
   **non défendable** tel quel ; la permutation décrite est **sous-spécifiée**.
2. **$\mathcal{H}_\text{mpd}$ vs volatilité** — un PASS peut mesurer « futurs calmes » plutôt qu'une
   structure informative au-delà de l'amplitude.
3. **Contraintes causales implicites** — $j + h \leq t$ est vraie avec $(\tau,h)=(20,10)$ mais
   **non formalisée** ; la grille SCI-003 avec $h=20$ est limite.

**Verdict INCONCLUSIVE** signifie : le protocole est réparable, mais **des décisions explicites**
doivent être enregistrées et reflétées dans `hypothesis.md` / `protocol.md` / `configuration.yaml`
**avant** DATA-REQ et implémentation.

---

## 1. Formalisation manquante de $\mathcal{L}_t$ (préalable)

Le protocole définit :

$$
\mathcal{L}_t = \{ s \in \mathcal{T} : s < t,\ s \notin \mathcal{E}_t,\ X_s \text{ valide},\ Y_s^{(h)} \text{ valide} \}
$$

$$
\mathcal{E}_t = \{ s : |s - t| \leq \tau \}
$$

**Contrainte causale à ajouter explicitement** (actuellement implicite) :

$$
\forall s \in \mathcal{L}_t,\quad s + h \leq t
$$

Sans cette clause, si $\tau < h$, des voisins pourraient exiger des rendements post-$t$ pour
calculer $Y_s$ — fuite look-ahead. Avec $\tau=W=20$, $h=10$ : pour $s \leq t-21$,
$s+h \leq t-11 < t$ ✓. La grille $h=20$ donne $s+h \leq t-1$ ✓ (limite stricte).

---

## 2. Registre des constats

Légende **Décision** : `PENDING` = en attente de décision humaine avant modification protocole.

---

### REV-01 — Standardisation : $r_t$ dans $\hat{\mu}_t, \hat{\sigma}_t$

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | Chaque composante $\tilde{r}_\tau$ pour $\tau \in [t-W+1,t]$ utilise $\hat{\mu}_t,\hat{\sigma}_t$ estimés sur $[\max(t_0,t-M+1), t]$ **inclusif**. Donc $r_t$ influence la variance/ moyenne qui standardise $r_t$ lui-même (et toute la fenêtre $X_t$). |
| **Conséquence scientifique** | Couplage mécanique intra-$X_t$ ; comparaison L2 entre états partiellement artificielle ; à $t$ l'information « disponible à l'instant $t$ » inclut $r_t$ (cohérent clôture daily) mais **non formalisé** si la décision est à l'ouverture $t+1$. |
| **Correction proposée** | **Option A (recommandée)** : estimer $\hat{\mu}_t,\hat{\sigma}_t$ sur $[t-M+1, t-1]$ pour standardiser $r_{t-W+1},\ldots,r_t$. **Option B** : conserver inclusion de $r_t$ mais documenter « standardisation end-of-day inclusive » et interdire interprétation intraday. Préciser timestamp de disponibilité dans C02. |
| **Décision** | **PENDING** |

---

### REV-02 — Instant de disponibilité de $X_t$

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MINOR |
| **Problème** | « Information disponible au temps $t$ » non ancrée : clôture de $t$ vs ouverture de $t+1$. |
| **Conséquence scientifique** | Ambiguïté reproductibilité et alignement futur paper trading. |
| **Correction proposée** | Fixer normativement : $X_t$ et décision disponibles **après clôture** du jour $t$ (prix $P_t$ connu). |
| **Décision** | **PENDING** |

---

### REV-03 — Futur $Y_t^{(h)}$ : causalité stricte

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MINOR |
| **Problème** | $Y_t^{(h)} = (r_{t+1},\ldots,r_{t+h})$ est correctement défini ; fenêtre complète exigée implicitement. |
| **Conséquence scientifique** | Points en bordure d'échantillon ($t > T-h$) doivent être exclus — mentionné mais pas formalisé dans $\mathcal{T}_\text{eval}$. |
| **Correction proposée** | $\mathcal{T}_\text{eval} = \{ t : X_t \text{ valide},\ Y_t^{(h)} \text{ complet},\ |\mathcal{L}_t| \geq L_\min \}$. |
| **Décision** | **PENDING** |

---

### REV-04 — $Y$ n'intervient pas dans la sélection des voisins

| Champ | Contenu |
|-------|---------|
| **Sévérité** | NOTE |
| **Problème** | Aucune fuite directe : $N_k^\text{geo}$ dépend seulement de $d(X_t,X_s)$. |
| **Conséquence scientifique** | OK tel quel. |
| **Correction proposée** | Aucune ; ajouter invariant explicite dans AF-08 : « sélection voisins = fonction de $X$ uniquement ». |
| **Décision** | **PENDING** (documentation) |

---

### REV-05 — Embargo $\tau=W$ : chevauchement des fenêtres $X$

| Champ | Contenu |
|-------|---------|
| **Sévérité** | NOTE |
| **Problème** | Affirmation « $\tau \geq W$ ⇒ au plus un rendement commun » est **fausse** pour $\tau=W$ : avec $t-s=21$, overlap = $\max(0, W-(t-s)) = 0$ — **zéro** rendement commun, pas un. |
| **Conséquence scientifique** | La marge est correcte mais la justification erronée affaiblit la confiance du protocole. |
| **Correction proposée** | Corriger la règle : séparation minimale $t-s \geq W+1$ (i.e. $\tau \geq W$ avec embargo $|s-t|\leq\tau$ ⇒ $t-s \geq \tau+1 \geq W+1$). |
| **Décision** | **PENDING** |

---

### REV-06 — Embargo insuffisant pour découpler les fenêtres $Y$ **entre voisins**

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | L'embargo contrôle $X_t$ vs $X_s$, pas le chevauchement de $Y_i$ et $Y_j$ pour $i,j \in N_k(X_t)$. Deux voisins distants de 30 jours ont des $Y$ qui partagent jusqu'à $h-|\Delta j|$ rendements. |
| **Conséquence scientifique** | $\mathcal{H}_\text{mpd}(N)$ mélange pairwise comparisons **non indépendantes** ; inflation artificielle de homogénéité si voisins geo cluster temporellement. |
| **Correction proposée** | **Diagnostic obligatoire** : distribution des distances temporelles $|i-j|$ dans $N^\text{geo}$ vs $N^\text{B0}$. **Option stricte** : contraindre voisins à $|i-j| \geq h$ (réduit $|\mathcal{L}_t|$). **Option I01** : documenter comme limitation + comparer écart $|i-j|$ geo vs B0. |
| **Décision** | **PENDING** |

---

### REV-07 — Contrainte $s + h \leq t$ non formalisée

| Champ | Contenu |
|-------|---------|
| **Sévérité** | **BLOCKER** |
| **Problème** | $\mathcal{L}_t$ n'exige pas $s+h \leq t$. La validité repose sur l'inégalité dérivée $s \leq t-\tau-1$ et $h \leq \tau$ — **non prouvée** dans le protocole. Si $\tau$ ou $h$ changent (SCI-003), fuite possible. |
| **Conséquence scientifique** | Risque look-ahead silencieux en sensibilité $h=20$, $\tau=20$. |
| **Correction proposée** | Ajouter $s + h \leq t$ comme **précondition hard** de $\mathcal{L}_t$, indépendamment de $\tau$. |
| **Décision** | **PENDING** |

---

### REV-08 — Dépendance temporelle des $\Delta_t$ ; t-test naïf

| Champ | Contenu |
|-------|---------|
| **Sévérité** | **BLOCKER** |
| **Problème** | Pour $h=10$, $Y_t$ et $Y_{t+1}$ partagent 9 rendements sur 10. $X_t$ et $X_{t+1}$ partagent 19/20. $\Delta_t$ et $\Delta_{t+1}$ sont **fortement corrélés**. Le protocole prescrit un « t-test apparié » sur $\{\Delta_t\}$ — terme incorrect (c'est un **test unilatéral sur une seule série**, pas apparié) **et** suppose des observations indépendantes. |
| **Conséquence scientifique** | p-values **anti-conservatrices** ; PASS SCI-001 possible sous H₀ vraie ; invalidation de la gate bloquante. |
| **Correction proposée** | Remplacer test primaire par : **(A)** bootstrap par blocs de longueur $B \geq h + W$ (ex. $B=21$ ou $B=40$) sur $\bar{\Delta}_\text{test}$ ; **(B)** sous-échantillonnage $\mathcal{T}_\text{eval}$ tous les $h$ jours (secondaire, perte de puissance) ; **(C)** test de permutation **par blocs temporels** (pas iid). Interdire t-test iid comme gate unique. |
| **Décision** | **PENDING** |

---

### REV-09 — Test de permutation sous-spécifié

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | « Ré-alléer labels geo/B0 au niveau des paires de voisinages » — objet, unité de permutation et loi nulle **non définis**. |
| **Conséquence scientifique** | Non reproductible ; implémentations divergentes ; PASS/FAIL arbitraire. |
| **Correction proposée** | Spécifier : pour chaque $t$, la loi nulle **échange** $\mathcal{H}_\text{mpd}(N^\text{geo})$ avec $\bar{\mathcal{H}}_\text{B0}(t)$ **ou** remplace la règle k-NN par un tirage uniforme **conditionnel** à $|\mathcal{L}_t|$ ; agréger statistique $\bar{\Delta}_\text{test}$ ; permutations par blocs si REV-08 retenu. |
| **Décision** | **PENDING** |

---

### REV-10 — Baseline B0 : équité du tirage uniforme

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | (a) $|\mathcal{L}_t|$ croît avec $t$ → variance heterogène des $\bar{\mathcal{H}}_\text{B0}(t)$ en début vs fin d'échantillon. (b) B0 ignore la structure temporelle — mais geo peut exploiter la densité régionale dans le temps (clusters). (c) B0 ne matche pas la volatilité locale — asymétrie avec REV-11. |
| **Conséquence scientifique** | Geo peut gagner **par design** si B0 sur-représente des régimes hétérogènes aléatoirement ; ou perdre si B0 a chance de tirer des clusters par hasard. |
| **Correction proposée** | Exiger $|\mathcal{L}_t| \geq L_\min$ (ex. $3k$) pour $t \in \mathcal{T}_\text{eval}$. **Diagnostic** : comparer distribution temporelle des voisins geo vs B0. **Option future (I01-bis)** : B0 stratifié par tertile de vol réalisée — **non obligatoire I01** si REV-11 adressé. |
| **Décision** | **PENDING** |

---

### REV-11 — $\mathcal{H}_\text{mpd}$ confond homogénéité et faible amplitude

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | $\mathcal{H}_\text{mpd} = \frac{2}{k(k-1)}\sum \|Y_i-Y_j\|_2$. Si voisins geo sélectionnent des périodes à faible $\|Y\|$ (faible vol), $\mathcal{H}_\text{mpd}$ baisse **mécaniquement** sans similarité directionnelle. |
| **Conséquence scientifique** | SCI PASS peut signifier « voisins en régime calme » et non « futurs structurellement similaires » — **exactement le piège signalé**. |
| **Correction proposée** | (1) **Gate diagnostic obligatoire** : comparer vol réalisée $\|Y_j\|$ geo vs B0. (2) **Métrique confirmatoire secondaire** : homogénéité sur **direction normalisée** $\hat{Y}_j = Y_j / (\|Y_j\|+\epsilon)$ ou corrélation de Pearson entre $Y_i,Y_j$. (3) **Interprétation SCI PASS** : « homogénéité L2 des trajectoires futures brutes » — pas « alpha directionnel ». |
| **Décision** | **PENDING** |

---

### REV-12 — Construction et signe de $\Delta_t$

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MINOR |
| **Problème** | $\Delta_t = \bar{\mathcal{H}}_\text{B0}(t) - \mathcal{H}_\text{mpd}(N^\text{geo})$ — cohérent entre hypothesis et protocol. Terme « paired t-test » induit confusion. |
| **Conséquence scientifique** | Risque d'inversion implémentation si développeur lit « paired » littéralement avec paires $(\mathcal{H}_\text{B0,r}, \mathcal{H}_\text{geo})$ sur $R$ draws. |
| **Correction proposée** | Renommer : « one-sample test on $\Delta_t$ series ». Documenter : $\Delta_t > 0 \Leftrightarrow$ geo plus homogène. $\bar{\mathcal{H}}_\text{B0}(t) = \frac{1}{R}\sum_{r=1}^R \mathcal{H}_\text{mpd}(N_{k,r}^{B0})$. |
| **Décision** | **PENDING** |

---

### REV-13 — Séparation train / validation / test

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | Train « calibration empirique des seuils INCONCLUSIVE » est **non borné** — risque de tuning post-hoc. AF-07 « $\mathcal{L}_t$ tronquée au split courant » ambigu : pour $t$ en test, voisins historiques $s<t$ peuvent inclure périodes train **et** validation **et** début test — causalement OK mais mélange régimes. |
| **Conséquence scientifique** | Fuite méthodologique si seuils INCONCLUSIVE calibrés sur test indirectement ; interprétation OOS floue. |
| **Correction proposée** | Train : **descriptif uniquement**, interdiction de modifier seuils/gates/métriques. Figurer $L_\min$, $N_\min$, $\alpha$ **avant** data. Clarifier AF-07 : à date test $t$, $\mathcal{L}_t = \{s : s < t, s \notin \mathcal{E}_t, \ldots\}$ — **pas** de restriction à train seul (sinon impossibilité early test). |
| **Décision** | **PENDING** |

---

### REV-14 — Multiplicité et rôle des gates

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MINOR |
| **Problème** | SCI-001 exige t-test **et** permutation ($\alpha=0.05$ chacun) — même hypothèse, corrélation non nulle → multiplicité légère. SCI-002 tertiles sur **même split test** que SCI-001 — confirmatoire mais non indépendant. SCI-003 (9 configs) **absent** du verdict global — correct. SCI-AUX marquées exploratoires — correct mais pas assez contraignant. |
| **Conséquence scientifique** | Risque de sur-interprétation si AUX ou SCI-003 cités après FAIL de SCI-001. |
| **Correction proposée** | Tableau normatif : **Primaire** = SCI-001 (avec inférence REV-08) ; **Confirmatoire** = SCI-002, SCI-004 ; **Diagnostique** = SCI-003, SCI-AUX-* (interdiction de promotion si SCI-001 FAIL). |
| **Décision** | **PENDING** |

---

### REV-15 — Taille effective d'échantillon

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | Calcul brut vs indépendant non distingué. |
| **Conséquence scientifique** | $N_\min=100$ sur test **brut** peut masquer $N_\text{eff} \ll 100$ sous dépendance. |

**Calcul (jours de bourse, approximatif) :**

| Paramètre | Valeur |
|-----------|--------|
| Warmup $M + W$ | 272 |
| Queue future $h$ | 10 |
| $\|\mathcal{T}_\text{eval}\|$ | $\approx T - 282$ |

| Historique $T$ | $\|\mathcal{T}_\text{eval}\|$ | Test (20 %) brut | Blocs indép. ($\approx \text{test}/h$) |
|----------------|-------------------------------|------------------|----------------------------------------|
| 1 500 | ~1 218 | ~244 | **~24** |
| 2 520 (10 ans) | ~2 238 | ~448 | **~45** |

Premier $t$ avec $|\mathcal{L}_t| \geq k=50$ : $\approx M + \tau + k + 1 \approx 273$ — OK bien avant test.

**Conclusion calcul :** comptage brut **suffisant** pour $N_\min=100$ sur 10 ans ; crédibilité **inférentielle** faible sans correction dépendance (REV-08).

| **Correction proposée** | Remplacer $N_\min$ par critère sur **nombre de blocs** ($\geq 30$ blocs de taille $h$) **ou** exiger IC bootstrap bloc avec largeur bornée. |
| **Décision** | **PENDING** |

---

### REV-16 — Non-stationnarité

| Champ | Contenu |
|-------|---------|
| **Sévérité** | NOTE |
| **Problème** | k-NN L2 sur fenêtres standardisées compare 2024 à 2008 sans modèle de changement de régime. |
| **Conséquence scientifique** | I01 mesure : *« similarité de forme récente normalisée sur 252j prédit homogénéité future L2 sur horizon h »* — **conditionnel à un seul actif et historique joint**. |
| **Correction proposée** | Documenter dans portée SCI PASS (REV-18). SCI-002 tertiles = robustesse **temporelle partielle**, pas preuve stationnarité. |
| **Décision** | **PENDING** (documentation) |

---

### REV-17 — `adjusted_close` et point-in-time

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | Adjusted close **révisable** par le fournisseur ; ajustements utilisent information future des dividendes/splits ; pas point-in-time. |
| **Conséquence scientifique** | Biais léger en SCI long historique ; **révision rétroactive** casse reproductibilité inter-snapshots. |
| **Correction proposée** | C02 doit exiger : `adjustment_policy` documentée, `vendor_revision` ou `as_of_download`, fingerprint snapshot, interdiction comparer deux snapshots revisés sans nouvelle expérience. DATA-REQ devra inclure politique PIT ou acceptation explicite du biais. |
| **Décision** | **PENDING** |

---

### REV-18 — Falsifiabilité

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MINOR |
| **Problème** | Paramètres $(W,k,h,M)$ figés ✓. FAIL possible ✓. Failles : bucket INCONCLUSIVE large ; train non borné ; possibilité de relancer avec autre seed B0 jusqu'à passage — atténué par seeds figées. |
| **Conséquence scientifique** | Protocole **falsifiable** si REV-08/13 corrigés ; sinon risque de « significance hacking » via interprétation AUX. |
| **Correction proposée** | Interdire post-hoc : changement métrique, paramètres, ou subset dates après vue du test. Enregistrer protocole versionné avant snapshot. |
| **Décision** | **PENDING** |

---

### REV-19 — Reproductibilité

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MINOR |
| **Problème** | Seeds B0/permutation figées ✓ ; tie-break « date la plus ancienne » ✓. Non spécifié : ordre de tri dates, tolérance float, version impl, arrondi. |
| **Conséquence scientifique** | Écarts minimes possibles entre machines ; acceptable si documenté. |
| **Correction proposée** | Exiger tri lexicographique stable des dates ; documenter `numpy/pydantic` versions ; tolérance $10^{-10}$ sur distances ; test de reproductibilité bit-identique en CI. |
| **Décision** | **PENDING** |

---

### REV-20 — Portée d'un SCI PASS

| Champ | Contenu |
|-------|---------|
| **Sévérité** | MAJOR |
| **Problème** | Formulation actuelle « information géométrique détectée » trop large ; risque de glissement vers PRED/ECON. |
| **Conséquence scientifique** | Sur-interprétation commerciale ou stratégique prématurée. |
| **Correction proposée** | Texte normatif exact : |

> **SCI PASS I01 autorise uniquement** à conclure que, pour l'instrument et la période testées,
> avec $X_t$ = fenêtre de rendements log standardisés ($W=20$, $M=252$), $d$ = L2, $h=10$,
> la règle k-NN produit un voisinage dont les trajectoires futures $Y^{(h)}$ ont une
> $\mathcal{H}_\text{mpd}$ **significativement inférieure** à la baseline B0 (uniforme),
> sous l'inférence retenue post REV-08, avec anti-fuite validée.
>
> **N'autorise pas** : direction du rendement, prédictibilité OOS (PRED), profit (ECON), trading.

| **Décision** | **PENDING** |

---

## 3. Synthèse par sévérité

| Sévérité | IDs | Count |
|----------|-----|-------|
| **BLOCKER** | REV-07, REV-08 | 2 |
| **MAJOR** | REV-01, REV-06, REV-09, REV-10, REV-11, REV-13, REV-15, REV-17, REV-20 | 9 |
| **MINOR** | REV-02, REV-03, REV-12, REV-14, REV-18, REV-19 | 6 |
| **NOTE** | REV-04, REV-05, REV-16 | 3 |

---

## 4. Réponses aux 15 axes de revue demandés

| # | Axe | Verdict adversarial |
|---|-----|---------------------|
| 1 | $X_t$ causalité | MAJOR — inclusion $r_t$ dans stats ; instant clôture non fixé |
| 2 | $Y_t^{(h)}$ | MINOR/OK — strictement $t+1$ ; bordure à formaliser |
| 3 | $\mathcal{L}_t$, embargo | BLOCKER $s+h\leq t$ ; MAJOR chevauchement $Y$ inter-voisins ; NOTE justification overlap $X$ |
| 4 | Dépendance temporelle | **BLOCKER** — t-test iid indefensible |
| 5 | B0 | MAJOR — $|\mathcal{L}_t|$ variable, asymétrie vol |
| 6 | $\mathcal{H}_\text{mpd}$ | MAJOR — confusion calme vs similitude |
| 7 | $\Delta_t$ | MINOR — signe OK ; terminologie « paired » dangereuse |
| 8 | Splits | MAJOR — usage train flou |
| 9 | Multiplicité | MINOR — rôles gates à verrouiller |
| 10 | Taille effective | MAJOR — $N$ brut OK, $N_\text{eff}$ faible |
| 11 | Non-stationnarité | NOTE — documenter portée |
| 12 | adjusted_close | MAJOR — révisions fournisseur |
| 13 | Falsifiabilité | MINOR — OK si corrections |
| 14 | Reproductibilité | MINOR — détails numériques |
| 15 | Portée SCI PASS | MAJOR — texte trop permissif |

---

## 5. Décisions collectives requises (avant modification protocole)

| Priorité | Sujet | Options |
|----------|-------|---------|
| P0 | Inférence SCI-001 | Bootstrap bloc vs permutation bloc vs thinning |
| P0 | Contrainte $s+h \leq t$ | Ajout hard constraint |
| P1 | Confusion vol / homogénéité | Diagnostic vol + métrique direction normalisée |
| P1 | Standardisation $\hat{\mu},\hat{\sigma}$ | Inclusive vs exclusive $r_t$ |
| P1 | Portée SCI PASS | Texte normatif REV-20 |
| P2 | Chevauchement $Y$ inter-voisins | Diagnostic vs contrainte $|i-j|\geq h$ |
| P2 | $L_\min$, blocs effectifs | Seuils sample size |
| P2 | C02 adjusted_close | Politique snapshot / PIT |

**Aucune modification** de `hypothesis.md`, `protocol.md`, `configuration.yaml` dans cette intervention.

---

## 6. Verdict de la revue

### **INCONCLUSIVE**

| Critère | Évaluation |
|---------|------------|
| Structure H₀/H₁, B0, splits, anti-fuite partielle | Solide |
| BLOCKERs résolus | **Non** |
| Prêt pour `DATA-REQ-I01.md` | **Non** — dépendances data (PIT, profondeur blocs) liées aux corrections |
| Prêt pour implémentation | **Non** |

**PASS** (revue) serait : protocole suffisamment spécifié pour DATA-REQ sans BLOCKER ouvert.
**FAIL** (revue) serait : protocole conceptuellement invalide — **non** le cas ; réparable.

---

## 7. Prochaine étape recommandée

1. **Décision humaine** sur les 8 sujets §5 (notamment P0).
2. **Mise à jour protocole** (commit séparé, décisions enregistrées).
3. **Revue ciblée** des BLOCKERs → verdict PASS attendu.
4. **Alors seulement** : `DATA-REQ-I01.md`.

---

**STOP revue** — pas de DATA-REQ, pas de data, pas d'implémentation.
