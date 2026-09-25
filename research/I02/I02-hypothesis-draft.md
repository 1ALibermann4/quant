# I02 — Brouillon d'hypothèse (pré-investigation)

> **STATUS :** DRAFT / PRE-INVESTIGATION
> **I02 :** NOT OPENED
> **NO EXPERIMENT AUTHORIZED**
>
> **Authority class :** RESEARCH (brouillon, non normatif)
> **Protocol :** QDP v0.1
> **Parent :** I01 exploratoire CLOSE @ `116374b`
> **Draft v0.1 :** `0e893c2`
> **Draft v0.2 :** `1057d85`
> **Draft v0.3 :** `15865ba`
> **Draft v0.4 review :** `5980bc8`
> **Draft v0.4 accept S :** `c85476c`
> **Draft v0.5 level invariant :** `9a9cf89`
> **Draft v0.6 Q vs φ review :** `8b652f7`
> **Draft v0.7 metric robustness :** `2a92da7`
> **Draft v0.8 accept §9.16 :** `ceb224c`
> **Draft v0.9 Z_t review :** `5681916`
> **Draft v0.10 A vs D / m :** `22ddd95`
> **Draft v0.11 family A primary candidate :** `e7cecc2`
> **Draft v0.12 Disp review :** `ab6645f`
> **Draft v0.13 Disp = Std_pop :** `98ddec6`
> **Draft v0.14 temporal architecture :** `6e0b4c7`
> **Draft v0.15 W_RV := W_X :** `e3fc32c`
> **Draft v0.16 m_Z admissibility :** `52a8a4a`
> **Draft v0.17 m_Z domain + identifiability :** `08f845d`
> **Draft v0.18 multiscale governance :** `ef5d39c`
> **Draft v0.19 W_X inheritance review :** `27b8102`
> **Draft v0.20 accept W_X=20 :** `e42b3a8`
> **Draft v0.21 freeze M_Z :** `3d3d877`
> **Draft v0.22 future target review :** `38812f8`
> **Draft v0.23 accept h=10 :** `cd16496`
> **Draft v0.24 forecast object / scoring :** `c3a6909`
> **Draft v0.25 scale estimand review :** `f3c54cc`
> **Calculs dans ce document :** aucun
> **Classe données I01 :** UNQUALIFIED (DR-007 / DR-008)

Ce fichier **ne signifie pas** que I02 est ouvert.
Aucun protocole, aucun run, aucun code expérimental I02 n'est autorisé.

$$
\text{observations I01} \neq \text{preuve de cette hypothèse candidate}
$$

E01–E04 ont **généré** la piste. Ils ne peuvent pas la valider.

**Statut des adversaires \(S\) :**

```text
REPRESENTATION ACCEPTED / METRIC ROBUSTNESS SETS ACCEPTED
```

\(S_1=[RV]\), \(S_2=[RV,D]\), \(S_3=[RV,Q]\) : nature informationnelle
**acceptée** (`c85476c`).

**Invariant de niveau :** proximité multiplicative (§9.14) — accepté.
**Doctrine §9.16 :** `ACCEPTED` (locale I02) — \(\mathcal{M}_{S3}\),
\(\mathcal{M}_{S2}\) figés ; sujet métrique pré-cadrage **CLOSED**.

**État \(Z_t\) :** Disp ; \(W_X=W_{RV}=20\) ; \(\mathcal{M}_Z=\{3,12,21\}\)
no-primary. **Cible :**
\[
V_{t,10}
=
\sqrt{\frac1{10}\sum_{j=1}^{10}r_{t+j}^{2}}
\quad\texttt{ACCEPTED}
\]
\(h=10\) — `INHERITED FIXED FORECAST HORIZON` (§14I.14).
**Forecast object / CRPS :** §14J — CRPS `ACCEPTED` ;
\(D_t^{(S)}\) brute **non** estimand final.
**Échelle / estimand :** §14K — class **B** (décision humaine
entre constructions `PROMISING`) ; pas d'estimand figé.
\(Z_t\) **non** acceptée. \(k\), stride, Spearman **OPEN**.
\[
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]
I02 reste `NOT OPENED`.

---

## 0. Ce que ce draft n'est pas

- pas un SCI-PASS, pas un SCI-FAIL ;
- pas une recommandation de confirmer I01 ;
- pas une ouverture de DR-003 / DR-005 ;
- pas E05 ;
- pas un contrat empirique pour un Market-State / Regime Engine ;
- pas un choix de seuil, de source, ni d'instrument ;
- pas une acceptation de \(Z_t\), d'une **distance complète**,
  ni de \(C_t\) ; CRPS / \(h\) : voir §14J / §14I (statuts explicites) ;
- pas une ouverture d'I02 ;
- pas un remplacement des représentations \(S\) par les charts \(S^\star\).

---

## 1. Faits I01 (observations, pas un récit)

Source : [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
et rapports E01–E04. Chiffres **déjà publiés**. Aucun recalcul.

### A. E01

Sur le sandbox `SPY / yfinance 1.6.0 / daily` (UNQUALIFIED), les voisins L2
présentaient **en moyenne** des futurs plus homogènes que B0 :

`H_raw` −13,7 % ; `H_vol` −54,0 % ; `H_shape` −0,21 %.

Couverture livrée : 1993-01-29 → 2026-09-23 ; `T_eval` = 8038
(1994-09-30 → 2026-09-09).

Ceci n'était pas une preuve de H-I01.

### B. E02

L'effet vs B0 était **principalement porté par `H_vol`**. `H_shape` était
pratiquement plat. `Δ_raw` suivait `Δ_vol` (corr. 0,762), pas `Δ_shape`
(0,009).

### C. E03

Le phénomène L2 n'était **pas** expliqué par un matching simple du niveau
de volatilité passée `rv_W`. Écart `|Δ rv_W|` des voisins L2 : 95,7 %
d'un candidat typique de `L_t` ; le témoin `rv_W` : 7,7 %. Le contrôle
récupérait `H_vol` vs B0 (−41,9 %) mais presque pas `H_raw` (−2,2 % vs
−13,7 % pour L2).

### D. E04

Face au contrôle `rv_W`, \(D_t = H^{rv}(t)-H^{L2}(t)\) était fortement
asymétrique sur `D_vol` :

- médiane **négative** (−1.52e-5) ; moyenne positive (+4.09e-5) ;
- `D_vol > 0` sur **42,8 %** des dates ;
- **1 %** des dates portaient **77 %** de `∑ D_vol` (asymétrie +7,44) ;
- concentration importante autour de **2008, 2009, 2020** ;
- décennie préfixée **2010–2019** : moyenne `D_vol` (et `D_raw`) **négative** ;
- relation **descriptive** avec les tertiles à effectif égal de `rv_W`
  élevé (coupe non optimisée, pas un seuil).

Aucune de ces lignes n'est une conclusion causale.

### Distinctions à préserver

```text
observation conditionnelle
    ≠  régime identifié
    ≠  mécanisme causal
    ≠  capacité prédictive confirmée
```

Formulation acceptable :

> E04 a identifié une **concentration conditionnelle** du phénomène dans
> certaines périodes / certains états observés. Le mécanisme et sa
> généralisabilité restent inconnus.

Formulations **interdites** comme faits : « L2 fonctionne en régime de
stress » ; « un régime de crise a été identifié » ; « la géométrie
prédit la volatilité en période de stress ».

Le mot **régime** reste descriptif et provisoire.

---

## 2. I01 vs I02 candidate — deux questions distinctes

I01 demandait essentiellement :

$$
X_s \approx X_t \quad\Longrightarrow\quad Y_s \approx Y_t
$$

c'est-à-dire : **les futurs associés aux voisins sont-ils collectivement
plus homogènes** (surtout `H_raw` / `H_vol` vs B0) ?

I02 candidate demanderait :

> La structure du passé apporte-t-elle de l'information sur la
> **distribution de la volatilité future réellement observée**, au-delà
> de résumés simples du passé ?

On ne cherche plus à prédire la **trajectoire** \(Y\). On cherche une
**propriété scalaire** de \(Y\), puis une **loi prédictive** de cette
propriété. `H_shape` reste un garde-fou sémantique, pas un objectif
réintroduit.

Ces questions **ne sont pas équivalentes**.

Exemple obligatoire : un voisinage peut avoir un `H_vol` très bas
(tous les voisins « prédisent » une faible volatilité) et être
**entièrement faux** si \(V_{t,h}\) réalisé est élevé. Homogénéité entre
voisins ≠ qualité de la prévision du futur de \(t\).

Un voisinage peut être :

```text
très homogène mais complètement faux
```

**Conclusion :** `H_vol` ne doit pas automatiquement devenir l'observable
principal d'I02. C'est une propriété **d'un ensemble de voisins**, pas
une variable attachée à \(t\). H3 porte précisément sur le comportement
de cette métrique dans les queues.

---

## 3. Variable future \(V_{t,10}\)

**Statut :** formule et \(h=10\) **`ACCEPTED`** (§14I.5, §14I.14).

$$
V_{t,10}
=
\sqrt{
\frac{1}{10}
\sum_{j=1}^{10}
r_{t+j}^{2}
}
$$

Terminologie : *future realized RMS volatility (undemeaned)*.
Hard availability : \(s+10\le t\). Revue : §14I.

---

## 4. Formulation informationnelle (pas encore opérationnelle)

Objets :

- \(X_t\in\mathbb{R}^{W}\) — structure multivariée du passé (**définition
  finale OPEN**) ;
- \(S_t\) — famille de résumés simples (**candidats \(S_1,S_2,S_3\)
  documentés, §8–9 ; métrique / scaling OPEN**) ;
- \(C_t\) — condition de marché (**non définie**, §14) ;
- \(V_{t,h}\) — observable futur **candidat**.

Question :

$$
\mathcal{L}(V_{t,h}\mid X_t,S_t,C_t=1)
\quad\text{versus}\quad
\mathcal{L}(V_{t,h}\mid S_t,C_t=1)
$$

La connaissance de \(X_t\) apporte-t-elle une information **incrémentale**
sur \(V_{t,h}\), conditionnellement à \(S_t\) et \(C_t\) ?

Un \(\neq\) statistique minuscule ne suffirait pas. Le sens *utile* d'une
information incrémentale est renvoyé au score prédictif (§6), **s'il**
est accepté.

Cette écriture **n'est pas** encore un protocole.

---

## 5. Distributions empiriques par voisinage (mécanisme candidat)

**Revue complète :** §14J. Aucun \(k\) choisi. Aucun calcul.

Distance et scaling de \(S\) : ensembles de robustesse §9.16
`ACCEPTED` ; détail d'opérateur kNN / agrégation \(L\)+forme :
protocole futur. Composition informationnelle : **acceptée** (§9).

**Pool commun \(A_t\)** (blocking, §14J.2) : \(X\) et chaque \(S\)
sélectionnent dans le **même** ensemble admissible — pas de pool
spécifique à une représentation ; pas de filtrage par \(Z_t\).

Pour une requête \(t\) et une représentation \(R\in\{X,S_1,S_2,S_3\}\),
objet canonique (§14J) :

\[
\widehat{\mathbb{P}}_t^{R}
=
\frac1k\sum_{i=1}^{k}\delta_{V_{s_i,10}},
\qquad
s_i\in N_k^{R}(t)\subset A_t
\]

ECDF dérivée : \(\widehat F_t^{R}(v)=(1/k)\sum_i\mathbf{1}\{V_{s_i,10}\le v\}\).

Ce sont des **prévisions probabilistes empiriques** de \(V_{t,10}\),
**pas** la loi conditionnelle vraie. Sélection = fonction de \(R\)
seulement (discipline AF-08).

Le voisinage reste l'**opérateur expérimental**. On n'ouvre pas une
course XGBoost(\(X\)) vs forêt(\(rv\)).

B0 (tirage dans \(\mathcal{L}_t\)) peut fournir une troisième mesure
de référence. Il n'est pas l'adversaire suffisant de H1.

---

## 6. CRPS — métrique principale **`ACCEPTED`**

**Statut :** `ACCEPTED` comme proper scoring rule primaire pour
évaluer \(\widehat{\mathbb{P}}_t^{R}\) (§14J.8–§14J.10). **Pas
calculé. Pas un gate numérique.** Différence brute
\(D_t^{(S)}=\operatorname{CRPS}_S-\operatorname{CRPS}_X\) :
orientation OK ; **pas** estimand final (§14J.13, revue §14K).

$$
\operatorname{CRPS}(F,y)
=
\int_{-\infty}^{+\infty}
\bigl(F(z)-\mathbf{1}\{y\le z\}\bigr)^{2}\,dz
$$

Convention : **plus faible = meilleure** prévision probabiliste.

Pour mesure empirique uniforme (§14J.8) :

\[
\operatorname{CRPS}(\widehat{\mathbb{P}},y)
=
\frac1k\sum_i|V_i-y|
-
\frac1{2k^2}\sum_i\sum_j|V_i-V_j|
\]

Opérationnel :

$$
\operatorname{CRPS}_R(t)=\operatorname{CRPS}(\widehat{\mathbb{P}}_t^{R},V_{t,10})
$$

Différence brute **candidate descriptive** (synonyme historique
\(\Delta_t^{(S)}\)) :

$$
D_t^{(S)}
=
\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)
$$

\(D_t^{(S)}>0\) : \(X\) mieux scorée que \(S\) en \(t\).
**Estimand scientifique principal :** **OPEN** — §14K
(class **B** ; décision humaine).

Revue adversariale antérieure (§6.1) : historique ;
verdicts score : §14J ; estimand : §14K.

### 6.1 CRPS adversarial review (historique pré-§14J)

Objectif : CRPS peut-il devenir métrique confirmatoire principale
**sans** ouvrir une sélection post hoc ? Aucune alternative n'est
testée sur les données. **Supersédé / complété par §14J.**

| Point | Lecture |
|-------|---------|
| Variable continue \(\geq 0\) | CRPS est défini pour toute loi réelle. Le support \([0,\infty)\) n'est pas imposé par l'intégrale ; l'ECDF empirique est portée par des \(V_{s,h}\geq 0\), donc le support effectif est correct. Pas un motif de rejet. |
| Calibration | Proper scoring rule : l'espérance est minimisée par la vraie loi. Une ECDF mal calibrée est pénalisée. |
| Sharpness / dispersion | Pénalise à la fois le biais et l'excès de largeur. Une loi trop plate (contrôle « 0.8 … 6.1 ») est battue par une loi concentrée autour de \(y\), *si* \(y\) tombe dedans. |
| Ensemble de \(k\) points | Avec \(k\) petit, \(\widehat F\) est en escalier. Le CRPS reste bien défini ; la variance du score est plus grande. Hériter \(k=50\) (OPEN) n'est pas anodin : trop peu d'atomes ⇒ loi rugueuse. Ce n'est pas une raison de changer \(k\) après un chiffre. |
| Queues | Moins dominé par les queues que le log-score (qui explose si \(y\) sort d'une densité paramétrique). Inversement, un miss extrême est moins punitif qu'en vraisemblance. Compatible avec H3 : il faudra regarder si \(\mathbb{E}[D\mid C=1]\) est une moyenne de queue. |
| Échelle de \(V\) | Le CRPS est **dans les unités de \(V\)**. Les jours à \(V\) élevé pèsent plus sur la moyenne. Si \(C_t=1\) sélectionne des états déjà volatils, \(\mathbb{E}[D\mid C=1]\) peut être dominé par quelques \(V\) grands — cousin d'H3. Une normalisation (CRPS / \(V\), rang, …) **n'est pas choisie** ici : la choisir après un run serait du snooping. Risque **documenté**, pas un motif de tester une autre métrique maintenant. **§14J.13 :** classé **C** pour l'estimand \(Z\)-lié. |
| vs erreur absolue ponctuelle | MAE de la moyenne ou de la médiane d'ensemble = cas dégénéré (prévision d'un point). Plus faible philosophiquement : on perd calibration/sharpness. Utile comme **diagnostic**, pas comme remplaçant silencieux. |
| vs log-score | Exige une densité. Imposer une loi paramétrique sur \(k\) voisins ajoute un modèle. Contredit « pas de ML / pas de loi inventée ». Écarté comme primaire (§14J.10). |
| vs calibration + sharpness séparées | Plus riches, plus de degrés de liberté ⇒ plus de tentation post hoc. Le CRPS les **combine** en une proper rule. Les séparer reste un diagnostic possible, pas une batterie de gates. |

**Verdict historique (§6.1) :** `ACCEPTABLE CANDIDATE`.
**Verdict figé (§14J) :** CRPS `ACCEPTED` ; \(\Delta\) définitif OPEN (échelle **C**).

---

## 7. H1 candidate v0.2

> **H1-I02 candidate v0.2 — information géométrique conditionnelle**
>
> Sous une condition de marché \(C_t\) causale, définie ex ante et
> observable après la clôture de \(t\), un voisinage historique
> construit à partir de la structure multivariée de \(X_t\) fournit une
> distribution prédictive de la volatilité réalisée future \(V_{t,h}\)
> contenant une information **hors échantillon** supérieure à celle
> obtenue à partir de voisinages construits sur des résumés simples
> pré-enregistrés \(S\) (famille candidate \(S_1,S_2,S_3\), §9).

Si CRPS était retenu plus tard, une opérationnalisation **possible**
serait :

$$
\mathbb{E}\bigl[\operatorname{CRPS}_X(t)-\operatorname{CRPS}_S(t) \bigm| C_t=1\bigr]
< 0
$$

sur l'information indépendante prévue par un protocole **non écrit**.

$$
\text{H1} \neq \text{« L2 bat B0 »}
$$

**Hypothèse candidate.** Aucun gate.

---

## 8. Concurrentes — H2 devient une famille

### H1 — Structure géométrique conditionnelle

Voir §7. Non établie. H1 n'est intéressante que si \(X\) survit à des
adversaires simples **raisonnables** des familles ci-dessous.

### H2 — Explications simples (plus seulement « `rv_W` »)

H2 ne signifie plus : « `rv_W` explique peut-être L2. »

| | Explication | Adversaire candidat |
|--|--|--|
| **H2a — LEVEL** | Le niveau de volatilité récente suffit. | \(S_1\) |
| **H2b — VOL DYNAMICS** | Niveau + dynamique récente de vol suffisent. | \(S_2\) |
| **H2c — AMPLITUDE DISTRIBUTION** | Les propriétés **sans ordre** de la distribution d'amplitudes suffisent. | \(S_3\) |

`rv_W` / \(S_1\) a déjà été insuffisant *pour `H_vol`* (E03). Cela ne
dit pas qu'un \(S_2\) ou \(S_3\) échoue pour \(\widehat F(V)\).

### H3 — Queue / métrique

Le gain de score (ou l'ancien `H_vol`) est porté par des épisodes
extrêmes / par le comportement de la métrique. Pas d'information
généralisable.

### H4 — Absence de structure reproductible

Pas de reproduction sur information indépendante. Issue normale.

---

## 9. Batterie d'adversaires \(S_1,S_2,S_3\)

**Statut :** `REPRESENTATION ACCEPTED / METRIC ROBUSTNESS SETS ACCEPTED`
(représentations @ `c85476c` ; doctrine §9.16 @ `ceb224c`).

Ce qui est accepté : la **nature informationnelle** des trois
adversaires ; \(\mathcal{M}_{S2}\), \(\mathcal{M}_{S3}\) (§9.16).
Ce qui **ne** l'est **pas** : \(W\), partage 10+10, convention aux
singularités, \(C_t\), détail protocolaire du désaccord matériel.

Les redondances éliminées sont **algébriques**. Aucun calcul sur
données pour les choisir.

```text
B0     hasard admissible / référence faible
S1     niveau de volatilité
S2     niveau + dynamique de volatilité
S3     distribution d'amplitude sans ordre
X      séquence multivariée ordonnée
```

**Ce n'est pas** \(S_1\subset S_2\subset S_3\subset X\).

\(S_2\) et \(S_3\) sont des **adversaires à explications distinctes**,
pas des marches d'un même modèle. Ils **partagent** la coordonnée de
niveau \(RV_t\) (pas des vecteurs orthogonaux, pas une indépendance
statistique). \(S_2\) conserve un ordre **grossier** (demi-fenêtres).
\(S_3\) détruit volontairement l'ordre et décrit davantage la forme
des amplitudes.

Interdit : dire « les axes sont orthogonaux » sauf démonstration
stricte. Préférer : **séparation conceptuelle** / **reparamétrisation
niveau / forme** (ou niveau / dynamique).

H1 **ne** se soutient **pas** parce que \(X\) bat B0.

### 9.1 Domaine : rendements bruts, pas \(X\) standardisé

Tous les \(S\) sont des fonctions de

\[
(r_{t-W+1},\ldots,r_t)
\]

information \(\mathcal{O}_{\le t}\) seulement. **Pas** des coordonnées
de \(X\) standardisé (\(M=252\)). Sinon \(S\) devient une projection
de \(X\) : un mini-\(X\), et le contrôle n'est plus une explication
indépendante.

\(W\) n'est **pas** figé. Les formules ci-dessous sont pour une
fenêtre de longueur \(W\) ; le partage 10+10 de \(S_2\) n'est
défini que **si** \(W=20\) est ultérieurement hérité.

### 9.2 Fausses dimensions

\[
RV_t=\sqrt{\frac1W\sum_{i=0}^{W-1}r_{t-i}^{2}},
\qquad
E_t=\sum_{i=0}^{W-1}r_{t-i}^{2}
=W\,RV_t^{2}
\]

\(RV\) et \(E\) **ne** sont **pas** deux informations. Interdit :
présenter \([RV,E]\) comme un contrôle plus riche.

\[
MA_t=\frac1W\sum_{i=0}^{W-1}|r_{t-i}|,
\qquad
A_t=\sum_{i=0}^{W-1}|r_{t-i}|
=W\,MA_t
\]

\(A\) et \(MA\) sont la même information. Un seul descripteur.

### 9.3 Relation \(RV\) / \(MA\) (famille S3, pas S2)

Inégalité RMS–AM sur les \(|r|\) :

\[
MA_t\le RV_t
\]

Égalité ssi toutes les amplitudes \(|r|\) de la fenêtre sont égales.

Variance **population** sur les \(W\) observations :

\[
\operatorname{Var}_{\mathrm{win}}(|r|)
=\frac1W\sum_{i=0}^{W-1}(|r_{t-i}|-MA_t)^{2}
=RV_t^{2}-MA_t^{2}
\]

Donc \([RV,MA]\) = niveau d'amplitude + hétérogénéité des amplitudes,
**sans ordre**. Appartient à **S3**, pas à S2. Ne pas mettre \(MA\)
dans \(S_2\).

### 9.4 \(S_1\) — niveau (H2a)

\[
S^{(1)}_t=[RV_t]
\]

Niveau récent de volatilité / amplitude quadratique. Attaché à \(t\),
indépendant du voisinage. Conceptuellement le témoin simple d'E03.

Question : \(X\) apporte-t-il quelque chose **au-delà** du niveau ?

### 9.5 \(S_2\) — niveau + dynamique (H2b)

Question testée : L2 ne reconnaît peut-être que le niveau et le fait
que la vol **monte ou descend**.

Si \(W=20\) est hérité : division **égale** 10+10 (anti-retuning :
on refuse 5/15, 8/12, …). Ce n'est pas une preuve que 10+10 est
optimal. Si \(W\neq 20\) : règle de partage **OPEN**.

Fenêtre ordonnée dans le temps : \(r_{t-W+1},\ldots,r_t\).
**Early** = première moitié (plus ancienne) ; **late** = seconde
(plus récente, inclut \(r_t\)).

\[
RV^{\mathrm{early}\,2}+RV^{\mathrm{late}\,2}=2\,RV_t^{2}
\]

(moitiés de même longueur). Le triplet \([RV,\,RV^{early},\,RV^{late}]\)
est redondant.

**Paramétrage OLD (référence algébrique / secours aux singularités) :**

\[
S^{(2)}_{\mathrm{old}}=[RV_t,\;\Delta RV_t],
\qquad
\Delta RV_t=RV^{\mathrm{late}}_t-RV^{\mathrm{early}}_t
\]

Sous positivité et la relation quadratique, \((RV,\Delta RV)\)
permet de retrouver les deux demi-volatilités (équation du second
degré ; racine physique \(RV^{early},RV^{late}\ge 0\), admissible
dès que \(|\Delta RV|\le 2\,RV\)).

**Paramétrage NEW — `REPRESENTATION ACCEPTED` (métrique unresolved) :**

\[
S^{(2)}_t=[RV_t,\;D_t],
\qquad
D_t=\log\!\left(\frac{RV^{\mathrm{late}}_t}{RV^{\mathrm{early}}_t}\right)
\]

même information H2b (niveau + dynamique), dynamique en **ratio**.
Revue §9.13 : `PREFER NEW` → acceptation humaine de la représentation.
Domaines / singularités : §9.13.1. **Pas** d'\(\varepsilon\).

**Pas de \(MA\) dans \(S_2\).** Ciblé : niveau + dynamique.

### 9.6 \(S_3\) — distribution sans ordre (H2c)

Question testée : le sac d'amplitudes suffit-il, sans séquence ?

**Paramétrage OLD (référence algébrique) :**

\[
S^{(3)}_{\mathrm{old}}=[RV_t,\;MA_t]
\]

**Paramétrage NEW — `REPRESENTATION ACCEPTED` (métrique unresolved) :**

\[
S^{(3)}_t=[RV_t,\;Q_t],
\qquad
Q_t=\frac{MA_t}{RV_t}\quad(RV_t>0)
\]

Aucun ordre. **Pas de \(\Delta RV\) ni \(D\).** **Pas** un sur-ensemble
de \(S_2\). Revue §9.13 : `PREFER NEW` → acceptation humaine.
Domaines / singularités : §9.13.2.

### 9.7 Extra de queue — non retenu

\(\max_i|r_{t-i}|\) : **OPEN QUESTION**, pas une composante.
Pourrait tester une observation extrême récente. L'ajouter maintenant
fabriquerait progressivement un mini-\(X\). Décision séparée avant
ouverture, pas ici.

### 9.8 Pas de drift dans \(S_3\)

Pas de \(\sum r\) ni de rendement cumulé signé. \(S_3\) est un
adversaire **volatilité / amplitude**. Un contrôle de drift /
momentum serait une **autre** hypothèse, à nommer séparément.

### 9.9 Distance / normalisation — OPEN (partiellement)

**Accepté (§9.14) :** l'écart de **niveau** doit être multiplicatif
(\(|\log RV_a-\log RV_b|\) sur \(RV>0\)).

**Non accepté :** forme complète de \(d\) ; pondération entre axes ;
Euclidienne / \(L_1\) ; z-score ; rangs ; CDF ; Mahalanobis ;
standardisation historique.

Un kNN euclidien brut sur \([RV,D]\), \([L,D]\), \([L,Q]\), etc. reste
un choix scientifique **non** autorisé par l'invariant seul.

\[
\text{REPRESENTATION} \neq \text{METRIC CHART}
\]

Voir §9.14.

### 9.10 Interdiction de snooping de conception

**Ne pas** calculer sur SPY : \(\operatorname{corr}(RV,MA)\) ;
performance \(S_1/S_2/S_3\) ; loi de \(\Delta RV\) ; « meilleur »
early/late ; utilité de \(\max|r|\) ; « meilleur » scaling ou
distance. Ces choix se décident **ex ante**, pas sur le sandbox I01.

### 9.11 Matrice d'interprétation (qualitative, sans résultat)

| Cas | Lecture candidate |
|-----|-------------------|
| **A.** \(X\) bat B0 seulement | Preuve insuffisante d'une information géométrique spécifique. |
| **B.** \(X\) bat \(S_1\), pas \(S_2\) | La dynamique récente de vol **peut** suffire (H2b). |
| **C.** \(X\) bat \(S_2\), pas \(S_3\) | La distribution / hétérogénéité d'amplitudes **peut** suffire ; l'ordre complet n'est pas nécessaire (H2c). |
| **D.** \(X\) bat \(S_2\) **et** \(S_3\) | La séquence multivariée **devient une question sérieuse**. |

Le cas D **ne prouve pas** que « l'ordre compte ». Il dit seulement
que \(S_2\) et \(S_3\) **n'ont pas suffi**. D'autres explications
restent possibles (autre \(S\), métrique, queues, \(C_t\), H3, H4).

### 9.12 Revue adversariale de la batterie

| Risque | Statut |
|--------|--------|
| Redondance \(E\leftrightarrow RV\), \(A\leftrightarrow MA\) | Éliminée algébriquement. |
| \([RV,MA]\) mis dans \(S_2\) | Interdit ; famille S3. |
| Triplet early/late/\(RV\) | Réduit à \((RV,\Delta RV)\). |
| Langage \(S_1\subset S_2\subset S_3\) | Interdit. |
| \(S_2\perp S_3\) au sens vectoriel | Faux : les deux contiennent \(RV\). Orthogonalité = **explications**, pas produits scalaires. |
| Ordre accidentel dans \(S_3\) | \([RV,MA]\) est invariant par permutation de la fenêtre. |
| Dynamique perdue dans \(S_2\) | Conservée via early/late (si \(W=20\)). |
| Drift dans \(S_3\) | Exclu. |
| \(S\) projeté depuis \(X\) standardisé | Interdit. |
| Cas D = preuve de l'ordre | Interdit. |
| \(W\) impair / non 20 | Partage \(S_2\) sans règle. OPEN si \(W\neq 20\). |
| Scaling silencieux du kNN | OPEN, prochaine décision scientifique probable. |
| Choix numérique issu d'E01–E04 | Aucun (pas de corrélation, pas de 5/15). |
| Extra \(\max\lvert r\rvert\) glissé dans \(S_3\) | Non retenu. |
| « Axes orthogonaux » (niveau / forme) | Interdit sans preuve. Dire **séparation conceptuelle**. |

### 9.13 Reparamétrisations candidates — revue mathématique

**Objet :** comparer OLD vs NEW pour \(S_2\) et \(S_3\). Même H2b / H2c.
Aucune donnée. Aucun \(\varepsilon\). Aucune distance.

Question centrale (pour chaque) :

| | |
|--|--|
| **A** | Conserve-t-elle l'information OLD sur le domaine régulier ? |
| **B** | Sépare-t-elle mieux niveau vs dynamique relative / forme relative ? |
| **C** | Introduit-elle une nouvelle hypothèse scientifique ? |
| **D** | Singularités / conventions qui rendraient OLD préférable ? |

#### 9.13.1 \(S_2\) : \(\Delta RV\) vs \(D=\log(RV^{late}/RV^{early})\)

Domaine régulier : \(RV^{early}>0\), \(RV^{late}>0\) (moitiés égales).

Propriétés de \(D\) :

- \(D=0\) iff \(RV^{late}=RV^{early}\) ;
- \(D>0\) iff \(RV^{late}>RV^{early}\) ; \(D<0\) sinon ;
- si tous les rendements de la fenêtre sont multipliés par
  \(\lambda>0\), alors \(RV\), \(RV^{early}\), \(RV^{late}\) scalent
  par \(\lambda\) et **\(D\) est inchangé** ;
- \(\Delta RV\) **scale** par \(\lambda\) (pas invariant d'échelle).

Reconstruction (\(\rho=e^{D}=RV^{late}/RV^{early}\)) :

\[
RV^{early}=RV\sqrt{\frac{2}{1+\rho^{2}}},
\qquad
RV^{late}=\rho\,RV^{early}
\]

donc \((RV,D)\mapsto(RV^{early},RV^{late})\) est bijective sur le
domaine régulier. Comme \((RV,\Delta RV)\) l'est déjà (sous
\(|\Delta RV|\le 2\,RV\) et positivité), **A : même information** sur
ce domaine.

Singularités NEW (OLD reste fini) :

| Cas | OLD \(\Delta RV\) | NEW \(D\) |
|-----|-------------------|-----------|
| \(RV^{early}=0\), \(RV^{late}>0\) | \(=RV^{late}\) | \(\to+\infty\) |
| \(RV^{late}=0\), \(RV^{early}>0\) | \(=-RV^{early}\) | \(\to-\infty\) |
| les deux \(=0\) (\(\Rightarrow RV=0\)) | \(=0\) | indéfini (\(0/0\)) |

**Ne pas** inventer un \(\varepsilon\). Traiter les zéros serait une
**convention supplémentaire** (choix scientifique séparé), pas une
partie de la reparamétrisation.

**B :** oui — \(RV\) = niveau absolu ; \(D\) = dynamique **relative**
(séparation conceptuelle niveau / dynamique). Pas une orthogonalité
géométrique ni une corrélation nulle.

**C :** non. Toujours H2b.

**D :** singularités log près de demi-fenêtres plates. OLD reste
défini partout. En pratique, pour des rendements quotidiens non
identiquement nuls sur \(W/2\) séances, le domaine régulier couvre
presque tout ; le cas pathologique reste **documenté**.

Risques adversariaux NEW : (i) deux régimes de niveaux très différents
avec le **même ratio** late/early sont indiscernables sur \(D\) —
voulu pour une dynamique relative, mais **masque** des écarts
absolus que \(\Delta RV\) distinguerait ; (ii) \(D\) peut devenir
grand en magnitude près de zéro — « sophistication » apparente si
on oublie le domaine ; (iii) sans convention zéro, le kNN devra
un jour traiter ces points (OPEN, pas ici).

**Verdict \(S_2\) : `PREFER NEW`.**

Même information sur le domaine régulier ; meilleure séparation
conceptuelle niveau / dynamique relative ; singularités
pathologiques documentées, sans \(\varepsilon\). Pas `ACCEPTED`.

#### 9.13.2 \(S_3\) : \(MA\) vs \(Q=MA/RV\)

Domaine régulier : \(RV>0\). Alors au moins un \(r\neq 0\), donc
\(MA>0\) et

\[
0 < Q_t \le 1
\]

\(Q=1\) iff toutes les amplitudes \(|r|\) de la fenêtre sont égales
(égalité RMS–AM). \(Q\to 0^{+}\) quand l'hétérogénéité relative des
\(|r|\) croît.

Invariance : si \(r\mapsto\lambda r\) pour \(\lambda\neq 0\), \(RV\)
et \(MA\) scalent par \(|\lambda|\) ; **\(Q\) inchangé**.

Relation déjà établie :

\[
\operatorname{Var}_{\mathrm{win}}(|r|)=RV^{2}-MA^{2}
\quad\Rightarrow\quad
\frac{\operatorname{Var}_{\mathrm{win}}(|r|)}{RV^{2}}=1-Q^{2}
\quad(RV>0)
\]

Bijectivité : pour \(RV>0\), \(MA=Q\cdot RV\) avec \(Q\in(0,1]\).
Donc **A : même information** que \((RV,MA)\) sur \(\{RV>0\}\).

Singularité : \(RV=0\) (fenêtre plate) \(\Rightarrow MA=0\) ; OLD =
\((0,0)\) bien défini ; NEW = \(0/0\) indéfini. **Pas d'\(\varepsilon\).**

**B :** oui — \(RV\) = niveau ; \(Q\) = forme / homogénéité
**relative** des amplitudes (séparation conceptuelle niveau / forme).
Pas orthogonalité statistique.

**C :** non. Toujours H2c.

**D :** une seule singularité (\(RV=0\)), plus douce que le log de
\(S_2\). OLD préférable **uniquement** si l'on veut un vecteur défini
y compris sur la fenêtre nulle sans convention.

Risques adversariaux NEW : (i) \(Q\) ignore l'échelle absolue de
l'hétérogénéité (\(MA\) fixe à \(RV\) différent) — voulu pour la
forme relative ; (ii) ne transforme pas \(S_3\) en objet
sophistiqué au-delà d'un ratio borné ; (iii) ne résout toujours pas
le scaling pour le kNN.

**Verdict \(S_3\) : `PREFER NEW`.**

Même information pour \(RV>0\) ; meilleure séparation conceptuelle
niveau / forme ; singularité \(RV=0\) mineure et documentée. Pas
`ACCEPTED`.

#### 9.13.3 Synthèse et acceptation humaine

| Contrôle | Verdict revue | Acceptation humaine |
|----------|---------------|---------------------|
| \(S_2\) | `PREFER NEW` | **oui** — représentation |
| \(S_3\) | `PREFER NEW` | **oui** — représentation |

**Représentations acceptées** ; métriques de robustesse : §9.16 :

\[
\boxed{S_1(t)=[RV_t]}
\]

\[
\boxed{
S_2(t)=\bigl[RV_t,\;D_t\bigr],
\qquad
D_t=\log\Bigl(\frac{RV_t^{\mathrm{late}}}{RV_t^{\mathrm{early}}}\Bigr)
}
\]

\[
\boxed{
S_3(t)=\bigl[RV_t,\;Q_t\bigr],
\qquad
Q_t=\frac{MA_t}{RV_t}
}
\]

Domaines / singularités : §9.13.1–9.13.2. OLD reste la référence
algébrique et le secours aux singularités.

**Ce que cette acceptation signifie**

- \(S_1\) : niveau ;
- \(S_2\) : niveau + dynamique **relative** ;
- \(S_3\) : niveau + forme **relative** des amplitudes ;
- \(S_2\) et \(S_3\) = **deux attaques distinctes** contre H1, pas
  deux marches d'un même modèle.

**Ce qu'elle ne signifie pas**

- ni \(W=20\), ni découpage 10+10, ni distance complète, ni pondération ;
- ni convention \(\varepsilon\) aux zéros ;
- ni ouverture d'I02.

Invariant multiplicatif du niveau et charts \(S^\star\) : §9.14
(ne remplacent **pas** \(S_1/S_2/S_3\)).

### 9.14 Invariant multiplicatif du niveau + charts métriques

**Décision humaine a priori** (aucune observation SPY, aucun CRPS,
aucun chiffre E01–E04).

#### 9.14.1 Décision acceptée

Sur le domaine régulier \(RV_a>0\), \(RV_b>0\), la proximité en
**niveau** de volatilité est **multiplicative**, non additive :

\[
\delta_{\mathrm{level}}(a,b)
=
\bigl|\log RV_a-\log RV_b\bigr|
=
\Bigl|\log\frac{RV_a}{RV_b}\Bigr|
\]

Exemple conceptuel : \(1\to 2\) et \(2\to 4\) réalisent le même
facteur \(2\), donc le **même** écart de niveau. Alors que
\(|2-1|=|3-2|\) (additive) traite autrement \(2\to 3\).

Toute composante « niveau » d'une **future** métrique devra respecter
cet invariant.

#### 9.14.2 Justification

\(RV\) est strictement positif sur son domaine régulier. Sous

\[
r\mapsto c r,\qquad c>0
\]

on a \(RV\mapsto c\,RV\), mais

\[
\log(c\,RV_a)-\log(c\,RV_b)=\log RV_a-\log RV_b
\]

L'écart de niveau est invariant à une multiplication commune de
l'échelle des rendements (décimal vs pourcentage, etc.).

Cohérence avec les représentations déjà acceptées :

- \(D=\log(RV^{\mathrm{late}}/RV^{\mathrm{early}})\) — dynamique relative ;
- \(Q=MA/RV\) — forme relative.

#### 9.14.3 Gouvernance : représentation \(\neq\) chart

**Ne pas** remplacer ni rouvrir `c85476c`.

Conservé **inchangé** :

\[
S_1=[RV],\qquad S_2=[RV,D],\qquad S_3=[RV,Q]
\]

Introduit séparément — **METRIC COORDINATE / CHART CANDIDATE**
seulement :

\[
L=\log RV
\qquad(RV>0)
\]

\[
S_1^\star=[L],
\qquad
S_2^\star=[L,D],
\qquad
S_3^\star=[L,Q]
\]

Ces objets servent à raisonner sur le calcul de proximité. Ils
**ne** sont **pas** de nouvelles représentations informationnelles
acceptées.

\[
\boxed{\text{REPRESENTATION} \neq \text{METRIC CHART}}
\]

#### 9.14.4 Accepté / non accepté

| Accepté | Non accepté |
|---------|-------------|
| proximité de niveau multiplicative | distance Euclidienne / \(L_1\) / \(L_2\) complète |
| \(\delta_{\mathrm{level}}=|\Delta L|\) sur \(RV>0\) | \(\sqrt{(\Delta L)^2+(\Delta D)^2}\), idem \(Q\) |
| charts \(S^\star\) comme candidats de réflexion | poids égaux ou quelconques |
| | z-score, rangs, CDF, Mahalanobis, std historique |
| | kNN final, \(W\), 10+10, \(k\), \(\varepsilon\), \(C_t\), CRPS, I02 |

#### 9.14.5 \(S_2^\star\) — encore ouvert

\([L,D]\) : deux coordonnées logarithmiques / relatives. Cela
**ne** justifie **pas** automatiquement

\[
1\text{ unité de }L \equiv 1\text{ unité de }D
\]

Le candidat euclidien non pondéré \(d_{S2}^{(E)}=\sqrt{(\Delta L)^2+(\Delta D)^2}\)
est **audité** en §9.15.2 — **non accepté**.

#### 9.14.6 \(S_3^\star\) — \(Q\) vs géométrie de forme

\([L,Q]\) combine \(L\in\mathbb{R}\) et \(Q\in(0,1]\). Une Euclidienne
brute sur \((L,Q)\) n'est **pas** neutre.

\(Q=MA/RV\) reste la **statistique informationnelle** de \(S_3\).
L'interprétation angulaire \(\phi=\arccos Q\) et le choix
métrique \(|\Delta Q|\) vs \(|\Delta\phi|\) : §9.15.1 — **OPEN**.

#### 9.14.7 Singularité \(RV=0\)

\(L=\log RV\) est **indéfini** si \(RV=0\). Aucun \(\varepsilon\),
clipping, sentinelle, ni convention empirique. Problème de domaine
à résoudre avant toute implémentation — relié aux singularités de
\(D\) et \(Q\) (§9.13), **sans** les fusionner abusivement.

#### 9.14.8 Exigences de conception M1–M9 (candidates)

Pas toutes indépendantes mathématiquement. Exigences de conception
pour une future métrique :

| ID | Exigence | Sens |
|----|----------|------|
| **M1** | Causality | Aucun futur dans la définition de la proximité. |
| **M2** | Unit / common-scale invariance | \(r\mapsto c r\) (\(c>0\)) ne change pas la proximité en **niveau** (déjà partiellement imposé par \(\delta_{\mathrm{level}}\)). |
| **M3** | Symmetry | \(d(a,b)=d(b,a)\). |
| **M4** | Identity | États identiques ⇒ distance nulle. |
| **M5** | Local monotonicity | Toutes choses égales, augmenter un écart d'axe ne rapproche pas. |
| **M6** | No predictive tuning | Aucun poids / scaling choisi pour améliorer CRPS ou un résultat I02. |
| **M7** | Interpretability | Chaque terme de \(d\) a une interprétation explicite. |
| **M8** | Temporal consistency | La règle ne change pas selon la date ou \(C_t\). |
| **M9** | Adversary preservation | La métrique n'efface pas artificiellement ce que \(S_1/S_2/S_3\) représentent. |

**Prochaine question OPEN :** géométrie de forme \(Q\) vs \(\phi\)
et agrégation avec \(L\) — §9.15. Puis pondération \(S_2^\star\).

#### 9.14.9 Revue de cohérence

| Contrôle | OK |
|----------|-----|
| H1 / H2a–c inchangés | oui |
| \(S_1/S_2/S_3\) non remplacés | oui |
| Aucun résultat empirique | oui |
| Pas de distance complète ni de poids | oui |
| \(S^\star\) ≠ représentation acceptée | oui |
| Pas d'\(\varepsilon\) | oui |

### 9.15 Revue adversariale — métriques de forme \(Q\) vs \(\phi\) ; candidat \(S_2\)

**Nature :** documentaire uniquement. Aucune donnée. Aucune métrique
acceptée. Objectif : quelles géométries ont une justification
**indépendante des données** — pas laquelle « performe ».

#### 9.15.0 Identités de base (domaine régulier \(RV>0\))

\[
Q=\frac{MA}{RV}\in(0,1],
\qquad
1-Q^{2}=\frac{\operatorname{Var}_{\mathrm{win}}(|r|)}{RV^{2}}
\]

Soit \(\mathbf{u}=(|r_{t-W+1}|,\ldots,|r_t|)\in\mathbb{R}^{W}_{\ge 0}\)
et \(\mathbf{1}=(1,\ldots,1)\). Alors

\[
\cos\varphi
=
\frac{\mathbf{u}\cdot\mathbf{1}}{\|\mathbf{u}\|_{2}\,\|\mathbf{1}\|_{2}}
=\frac{MA}{RV}=Q
\]

avec \(\varphi=\arccos Q\in[0,\pi/2]\). Donc \(Q=\cos\varphi\) :
**angle entre le profil d'amplitudes et le rayon uniforme**.

Niveaux de gouvernance (à ne pas confondre) :

| Niveau | Objet | Statut |
|--------|-------|--------|
| Informationnel | \(Q=MA/RV\) dans \(S_3\) | **ACCEPTED** (représentation) |
| Interprétation | \(\phi=\arccos Q\) | **documentée** — angle à l'uniforme |
| Métrique de forme | \(\lvert\Delta Q\rvert\) vs \(\lvert\Delta\phi\rvert\) | **OPEN** |

\[
\boxed{Q\text{ (statistique)} \neq \phi\text{ (interprétation)} \neq d_{\mathrm{forme}}}
\]

#### 9.15.1 \(Q\) vs \(\phi\) — deux géométries, aucune « neutre »

**A. Dérivée et développement près de l'uniforme**

\[
\Bigl|\frac{d\phi}{dQ}\Bigr|=\frac{1}{\sqrt{1-Q^{2}}}
\quad\text{diverge quand }Q\to 1^{-}
\]

Près de \(\phi=0\) (\(Q\to 1\)) :

\[
Q=\cos\phi=1-\frac{\phi^{2}}{2}+O(\phi^{4})
\quad\Rightarrow\quad
\phi\approx\sqrt{2(1-Q)}
\]

Donc \(Q\) **compresse quadratiquement** les petites déviations
angulaires ; \(\phi\) les remet au premier ordre en angle. La dérivée
infinie n'implique **pas** à elle seule une hypersensibilité
pathologique de \(\phi\) : elle peut aussi corriger la dégénérescence
locale de \(Q=\cos\phi\).

Réciproquement, pour un écart angulaire fixe \(\delta\) près de
\(\phi\),

\[
\Delta Q\approx-\sin(\phi)\,\delta
\]

Lorsque \(\phi\to 0\), \(\Delta Q\to 0\) pour un même \(\delta\).
Donc **\(Q\) sous-discrimine** les différences de forme près de
l'uniformité si l'on considère l'angle comme référence — autant que
\(\phi\) peut sembler les sur-discriminer si l'on considère le cosinus
comme référence.

**B. Deux métriques extrinsèques distinctes**

\[
d_Q(a,b)=\lvert Q_a-Q_b\rvert
\quad\text{vs}\quad
d_\phi(a,b)=\lvert\phi_a-\phi_b\rvert=\lvert\arccos Q_a-\arccos Q_b\rvert
\]

- \(d_Q\) : différences égales de **ratio \(\ell_1/\ell_2\)** (cosinus)
  équivalentes ;
- \(d_\phi\) : différences égales d'**angle à l'uniforme** équivalentes.

Aucune n'est « neutre ». Choisir l'une, c'est choisir une géométrie.

**C. Terminologie — ce que \(Q\approx 1\) n'est pas**

\(Q\approx 1\) signifie que les amplitudes \(|r_i|\) de la fenêtre sont
**proches les unes des autres** (profil plat). Ce n'est **pas**
« bruit blanc gaussien ». Pour une grande fenêtre i.i.d. gaussienne
centrée, asymptotiquement

\[
Q\to\frac{\mathbb{E}|Z|}{\sqrt{\mathbb{E}[Z^{2}]}}=\sqrt{\frac{2}{\pi}}\approx 0.798
\]

pas \(1\). Interdit d'assimiler quasi-uniforme à gaussien.

**D. Stabilité / perturbations de \(\mathbf{u}\)**

- Petite perturbation angulaire près de \(\phi=0\) : \(\Delta Q=O(\phi\,\delta)=O(\delta^{2})\)
  si \(\phi\sim\delta\) — \(d_Q\) voit peu ; \(d_\phi\) voit \(\delta\).
- Près de \(Q\to 0^{+}\) (\(\phi\to\pi/2\)) : \(\lvert d\phi/dQ\rvert\to 1\),
  les deux métriques sont localement comparables à une constante.
- Une seule coordonnée grande dans \(\mathbf{u}\) (spike) pousse \(Q\)
  vers le bas ; les deux distances augmentent, mais pas au même rythme.

**E. Borne \(1/\sqrt{W}\) (rappel, pas un seuil)**

Par Cauchy–Schwarz / RMS–AM, \(Q\le 1\) toujours. La valeur typique
sous i.i.d. dépend de la loi des \(r\) et de \(W\) ; ce n'est **pas**
une justification pour caler une métrique, ni pour choisir entre \(Q\)
et \(\phi\). Mention seulement pour éviter de lire \(Q=0.8\) comme
« loin de l'uniforme » sans modèle.

**F. Extrinsèque vs intrinsèque**

- Extrinsèque sur le cosinus : \(d_Q\) (plongement \(Q\in(0,1]\)).
- Intrinsèque sur le cercle / cône des directions de \(\mathbf{u}\) :
  écart angulaire \(d_\phi\) au rayon \(\mathbf{1}\).

Les deux sont défendables a priori. **Aucune raison** de déclarer \(Q\)
référence métrique et \(\phi\) variante (ni l'inverse) sans décision
géométrique explicite.

**Question géométrique exacte (sans SPY / CRPS) :**

> Pour l'adversaire \(S_3\), veut-on préserver une différence linéaire
> du ratio \(\ell_1/\ell_2\), ou une différence linéaire de l'angle à
> l'uniformité ?

**Verdict documentaire \(Q\) vs \(\phi\) :** `INCONCLUSIVE` —
les deux sont des géométries légitimes ; aucune n'est neutre ;
la statistique \(Q\) reste acceptée ; la métrique de forme reste OPEN.

#### 9.15.2 Audit du candidat \(S_2\) : \(d_{S2}^{(E)}\)

Candidat **non accepté** :

\[
d_{S2}^{(E)}(a,b)
=
\sqrt{(\Delta L)^{2}+(\Delta D)^{2}},
\qquad
L=\log RV,\quad D=\log\frac{RV^{\mathrm{late}}}{RV^{\mathrm{early}}}
\]

(domaine : demi-vol \(>0\), \(RV>0\)).

| Argument pour | Argument contre |
|---------------|-----------------|
| \(L\) et \(D\) sont des log-ratios de volatilité — type d'objet comparable | « facteur \(e\) sur le niveau ≡ facteur \(e\) sur la dynamique » reste une **pondération** `1:1` |
| Invariance commune \(r\mapsto c r\) (\(c>0\)) | \(L\) et \(D\) ne sont pas indépendants (\(RV_e^{2}+RV_l^{2}=2\,RV^{2}\)) |
| Pas de z-score / rang / donnée | Norme \(L_2\) vs \(L_1\) non tranchée ; M5 OK pour les deux |
| Cohérent avec M2 (niveau) et structure relative de \(D\) | N'implique pas l'agrégation avec une future forme \(S_3\) |

**Verdict documentaire \(d_{S2}^{(E)}\) (historique) :** devenu
\(d_2\in\mathcal{M}_{S2}\) — **PRIMARY** sous §9.16 `ACCEPTED`.

#### 9.15.3 Suite — §9.16

Choix unique \(Q\) vs \(\phi\) **abandonné** au profit de
\(\mathcal{M}_{S3}=\{d_Q,d_\phi\}\). Voir §9.16 (`ACCEPTED`).

#### 9.15.4 Cohérence

| Contrôle | OK |
|----------|-----|
| \(S_3=[RV,Q]\) non modifié | oui |
| \(\phi\) ≠ nouvelle représentation acceptée | oui |
| Pas de « \(Q\) = métrique neutre » | oui |
| Pas de gaussien = \(Q\approx1\) | oui |
| Suite métierrique : §9.16 | oui |
| Aucune donnée / CRPS | oui |

### 9.16 Doctrine — incertitude métrique → robustesse préenregistrée

**Nature :** méthodologique, documentaire. Aucune donnée. I02 reste
`NOT OPENED`.

**Statut :** `ACCEPTED` (décision humaine) — **locale à I02**.
Promotion éventuelle en principe QDP général : **hors scope** ;
prématuré.

\[
\boxed{\text{Metric uncertainty} \rightarrow \text{pre-registered robustness}}
\]

#### 9.16.0 Constat d'asymétrie (historique, post-`8b652f7`)

§9.15 a montré qu'on **ne** déduit **pas** une métrique \(S_3\) de
la seule interprétation \(\phi=\arccos Q\). Chemin « chart suivant »
**fermé**.

#### 9.16.1 Principe accepté

Lorsqu'il existe plusieurs métriques **a priori défendables** pour un
même adversaire informationnel et qu'aucune justification mathématique
ne désigne une canonique :

1. on **ne** sélectionne **pas** celle qui produit le résultat souhaité ;
2. on **préenregistre** l'ensemble admissible \(\mathcal{M}\) ;
3. la **conclusion scientifique** préenregistrée doit survivre à
   \(\mathcal{M}\).

**Nuance :** la robustesse porte sur la **conclusion scientifique**
préenregistrée (ex. « \(X\) résiste à H2c »), **pas** sur l'égalité
des valeurs numériques ni des tailles d'effet. Le protocole futur
devra définir précisément ce qu'est un « désaccord matériel » sur
cette conclusion — **sans** ouvrir ici de seuil.

**Interdit explicite :**

\[
\text{run}\rightarrow\text{voir laquelle gagne}\rightarrow\text{retenir celle-là}.
\]

**Interdit explicite :** introduire une métrique **après** observation
du résultat. Toute métrique additionnelle = **nouvelle investigation**,
pas un amendement silencieux de \(\mathcal{M}\).

#### 9.16.2 \(\mathcal{M}_{S3}\) — accepté (aucune primaire)

\[
\mathcal{M}_{S3}=\{d_Q,\,d_\phi\}
\]

\[
d_Q(a,b)=\lvert Q_a-Q_b\rvert,
\qquad
d_\phi(a,b)=\lvert\arccos Q_a-\arccos Q_b\rvert
\]

Ensemble de **metric robustness** : les deux membres sont égaux en
statut ; **aucune** primaire. \(Q\) reste la statistique
informationnelle de \(S_3\) ; \(\phi\) reste l'interprétation
angulaire — ni l'une ni l'autre n'est « la » métrique canonique.

**Règle H2c :** pour conclure que \(X\) résiste à H2c, la conclusion
doit être **compatible sous les deux** métriques.

\[
\boxed{\text{désaccord matériel}\Rightarrow\text{H2c comparison = INCONCLUSIVE}}
\]

Pas d'invitation à retenir le membre favorable à \(X\).

#### 9.16.3 \(\mathcal{M}_{S2}\) — accepté (primaire + variante)

\[
\mathcal{M}_{S2}=\{d_2,\,d_1\}
\]

\[
d_2=\sqrt{(\Delta L)^{2}+(\Delta D)^{2}}
\quad\text{(PRIMARY)}
\]

\[
d_1=\lvert\Delta L\rvert+\lvert\Delta D\rvert
\quad\text{(ROBUSTNESS VARIANT)}
\]

Ce n'est **pas** un vote \(L_1\) vs \(L_2\). \(d_2\) est la première
candidature géométriquement motivée (ex-\(d_{S2}^{(E)}\)) ; \(d_1\)
teste la robustesse de la **conclusion** H2b, pas un concurrent à
optimiser.

Même règle : désaccord matériel sur la conclusion H2b ⇒
`INCONCLUSIVE` (H2b comparison), jamais sélection post-hoc.

#### 9.16.4 Portée et clôture pré-cadrage

| Objet | Statut |
|-------|--------|
| Doctrine §9.16 | `ACCEPTED` (I02 only) |
| \(\mathcal{M}_{S3}\) | `ACCEPTED` |
| \(\mathcal{M}_{S2}\) | `ACCEPTED` |
| Sujet métrique (pré-cadrage) | **CLOSED** |
| Définition protocolaire du « désaccord matériel » | OPEN (protocole futur) |
| Agrégation exacte \(L\)+forme dans l'opérateur kNN | OPEN (protocole ; pas de chart nouveau) |
| \(C_t\) | **prochaine** décision conceptuelle |
| Promotion QDP générale | **non** |

#### 9.16.5 Cohérence

| Contrôle | OK |
|----------|-----|
| Pas de nouvelle transformation \(S_3\) | oui |
| \(S_1/S_2/S_3\) informationnels inchangés | oui |
| Pas de sélection empirique / post-hoc | oui |
| `INCONCLUSIVE` = verdict, pas cherry-pick | oui |
| Locale I02 ; pas de règle QDP globale | oui |
| I02 NOT OPENED | oui |

---

## 10. Statut de `H_vol` et `H_shape`

| Rôle | Objet |
|------|--------|
| **PRIMARY CANDIDATE** | Score probabiliste du futur **réellement observé** (CRPS *si* accepté après revue humaine) |
| **MECHANISTIC DIAGNOSTIC** | `H_vol` — les voisins sont-ils homogènes en volatilité ? |
| **NEGATIVE / SEMANTIC CONTROL** | `H_shape` — un canal volatilité ne autorise **pas** « trajectoires futures similaires » |
| **B0** | Référence secondaire, pas adversaire suffisant de H1 |

`H_shape` : même discipline que le draft v0.1 (DEC-03). Rôle-gate :
**OPEN**. Pas de seuil ici.

---

## 11. Revue adversariale de H1-v0.2

Qu'est-ce qui pourrait rendre cette formulation **trompeuse** ?

**A. Dimension.** \(X\in\mathbb{R}^{W}\) a plus de coordonnées que
chaque \(S_i\). Un gain peut être « plus de dimensions », pas
« géométrie ». D'où \(S_1,S_2,S_3\) (H2a–c), pas seulement `rv_W`.
Battre les trois ne **prouve** toujours pas l'ordre temporel.

**B. kNN en haute dimension.** Localité faible, distances concentrées
(E02 : rang 50 / médiane bibliothèque ≈ 0,67 — observation I01, pas
un calibrage). Instabilité possible. Hériter \(k=50\), \(W=20\) est un
héritage générateur (§11.H).

**C. ECDF à \(k\) atomes.** Mal calibrée par construction (granularité
\(1/k\)). Le CRPS le voit ; un « gain » peut être de la variance de
score, pas de la structure.

**D. CRPS et dispersion.** Peut récompenser une sharpness heureuse
sans structure économique (ni alpha, ni régime interprétable). Voir
§6.1 (échelle, queues).

**E. Sélection par \(C_t\).** Conditionner à \(C_t=1\) change
l'échantillon. Une \(C_t\) trop rare ou trop alignée sur les crises
vues en E04 recrée I01. \(C_t\) reste **non définie**.

**F. Taille de \(\{C_t=1\}\).** Trop peu de dates ⇒ moyenne de \(D\)
instable, H3 indiscernable. Impossible à chiffrer avant de définir
\(C_t\). **OPEN** lié à \(C_t\).

**G. Pas une stratégie.** Un meilleur CRPS sur \(V\) n'est ni un signe
de rendement, ni un alpha, ni une éligibilité de stratégie, ni un
Market-State Engine.

**H. Héritage générateur I01.** Réutiliser \(W=20\), \(h=10\), \(k=50\)
et la forme de \(X\) (rendements standardisés) **évite le retuning**
et **hérite du générateur**. Les deux sont vrais. À documenter dans
tout protocole futur, pas à « corriger » après un premier CRPS.

---

## 12. Holdout et réplication (conceptuel)

Le dataset SPY d'E01–E04 couvre **1993-01-29 → 2026-09-23**.

**Post-2022 n'est pas un holdout vierge** pour cette famille
d'hypothèses.

Catégories possibles — **aucune sélectionnée** : futur réellement non
observé ; autre instrument ; autre univers ; séparation
pré-enregistrée non choisie pour isoler 2008/2009/2020.

Ne pas : choisir une source ; rouvrir DR-003 / DR-005 ; contacter un
fournisseur ; requalifier yfinance.

Un I02 exploratoire UNQUALIFIED, s'il est un jour autorisé, ne produit
aucun SCI-PASS / SCI-FAIL (DR-007).

---

## 13. Falsification / kill criteria

Qualitatif. **Aucun seuil numérique.**

1. Disparition du gain de score annoncé hors information indépendante (H4).
2. Un adversaire \(S_1\), \(S_2\) ou \(S_3\) reproduit \(N_X\) au
   sens du score (H2a / H2b / H2c).
3. Gain porté par quelques événements, sans reproductibilité sous \(C_t\)
   pré-enregistrée (H3).
4. Dépendance à une définition de « stress » choisie après 2008/2009/2020
   ou après maximisation de \(D\) ou de \(D^{\mathrm{CRPS}}\).
5. Résultat entièrement dû au comportement de la métrique (CRPS à
   échelle brute, ou `H_vol`) sans structure de voisinage.
6. Instabilité à des choix **pré-enregistrés** raisonnables (pas :
   chercher \(W\) après coup) — en particulier, sous §9.16
   `ACCEPTED` : dépendance du verdict H2c (resp. H2b) au seul
   membre favorable de \(\mathcal{M}_{S3}\) (resp. \(\mathcal{M}_{S2}\))
   ⇒ `INCONCLUSIVE` / non-résistance, **pas** sélection post-hoc ;
   ajout d'une métrique après observation ⇒ nouvelle investigation.

Un kill n'est pas un SCI-FAIL d'I01.

---

## 14. Candidate causal state variable \(Z_t\) — volatility-regime instability review

**Nature :** documentaire / adversariale. **Aucune donnée.** Aucune
\(Z_t\) acceptée. I02 reste `NOT OPENED`.

**Décisions antérieures non rouvertes :** \(S_1/S_2/S_3\), invariant
multiplicatif, §9.16 / \(\mathcal{M}_{S2}\), \(\mathcal{M}_{S3}\).

### 14.0 Pivot conceptuel — abandonner \(C_t\) binaire comme framing principal

E04 a généré une observation exploratoire : l'intérêt relatif de la
géométrie \(X\) **semblait** dépendre de l'état du marché et se
concentrer dans certaines périodes de forte turbulence.

E04 **n'a pas** identifié :

- qu'un régime « stress » binaire existe ;
- un seuil de stress ;
- que 2008 / 2009 / 2020 définissent ce régime ;
- que le tertile supérieur observé soit une frontière ;
- la cause du phénomène.

\[
\text{E04 generated « state dependence ».}
\quad
\text{E04 did NOT identify the nature of the state.}
\]

Tout choix visant à **reproduire** les épisodes favorables d'E04 =
**conceptual snooping**.

**Framing abandonné comme primaire :** \(C_t=\) condition binaire de
stress.

**Problème candidat :**

\[
Z_t=\text{causal market-state variable}
\]

**Sémantique primaire candidate :**

\[
\text{VOLATILITY-REGIME INSTABILITY STATE}
\]

\(Z_t\) doit représenter à quel point le **niveau local de volatilité
est stable ou instable dans le temps** — pas le niveau lui-même, pas
« stress » général, pas drawdown, panique, crise, direction baissière,
ni mémoire sérielle générale.

Exemples **sémantiques uniquement** (non calculés) :

| \(L\) | \(Z\) | Lecture candidate |
|-------|-------|-------------------|
| bas | bas | faible volatilité stable |
| haut | bas | volatilité élevée, régime **établi** |
| bas / modéré | haut | transition / instabilité |
| haut | haut | volatilité élevée **et** instable |

### 14.1 Ce que capturent déjà les adversaires (rappel)

| Objet | Rôle | N'est pas |
|-------|------|-----------|
| \(RV\) / \(L=\log RV\) | niveau d'amplitude | instabilité du régime |
| \(D=\log(RV^{\mathrm{late}}/RV^{\mathrm{early}})\) | dynamique relative **grossière** (deux blocs) | roughness fine du chemin de \(L\) |
| \(Q=MA/RV=\cos\phi\) | hétérogénéité du profil d'amplitudes \(\lvert r\rvert\) | **entropie** (interdit) ; pas \(\phi\)-métrique seule |

Information partagée avec \(Z\) : acceptable. Identité triviale
avec \(L\), \(D\) ou \(Q\) : **non**.

### 14.2 Exigences Z1–Z8 (grille d'examen)

| ID | Exigence |
|----|----------|
| **Z1** | Causalité : \(Z_t\) \(\mathcal{F}_t\)-mesurable |
| **Z2** | Invariance d'échelle sous \(r\mapsto c r\) (\(c>0\)), alignée sur l'invariant multiplicatif |
| **Z3** | Non-identité monotone / quasi-identique avec \(L\), \(D\), \(Q\) |
| **Z4** | Fidélité : instabilité de régime, pas niveau / stress directionnel / drawdown / mémoire / crise |
| **Z5** | Faible paramétrisation |
| **Z6** | Aucune calibration E04 / 2008–2020 / tertile / \(D_{vol}\) / CRPS |
| **Z7** | Interprétabilité mathématique explicite |
| **Z8** | Domaines et singularités **identifiés** ; **aucun** \(\varepsilon\) choisi |

### 14.3 Point central — trend vs instability

Séquences conceptuelles de \(L\) (pas de données marché) :

\[
\text{A (tendance régulière) :}\quad
1.0,\;1.1,\;1.2,\;1.3,\;1.4
\]

\[
\text{B (erratique) :}\quad
1.0,\;1.4,\;0.9,\;1.5,\;1.1
\]

Une bonne \(Z\) d'instabilité de régime doit expliquer **pourquoi**
elle traite (ou non) A et B différemment. Une \(Z\) élevée pour A
**et** B n'opérationnalise probablement **pas** la sémantique
retenue.

### 14.4 Famille A — variation de la log-volatilité

**Objets types (non figés) :** \(\Delta L_t=L_t-L_{t-1}\) ;
puis mesure causale de variabilité récente de \(\{\Delta L\}\)
(RMS, MAD, écart-type empirique, moyenne de \(\lvert\Delta L\rvert\), …)
sur une fenêtre \(m\).

| Q | Réponse |
|---|---------|
| A. Mesure | Amplitude des **changements** du niveau multiplicatif |
| B. \(r\mapsto cr\) | \(L\mapsto L+\log c\) ⇒ \(\Delta L\) invariant ⇒ variabilité de \(\Delta L\) invariante |
| C. ≠ \(L\) | oui (niveau vs dynamique locale) |
| D. ≠ \(D\) | oui en général : \(D\) = contraste **deux blocs** ; A = roughness du chemin. Risque de redondance partielle si \(m\) et la construction collapsent vers un contraste biparti |
| E. ≠ \(Q\) | oui : \(Q\) porte sur le profil \(\lvert r\rvert\), pas sur la trajectoire de \(L\) |
| F. high-\(L\) stable vs instable | un régime élevé **plat** : \(\Delta L\approx 0\) ⇒ \(Z\) bas ; erratique ⇒ \(Z\) haut |
| G. Trend A | \(\Delta L\) **constant** ⇒ dispersion de \(\Delta L\) **basse** ⇒ A **non** « instable ». Souhaitable pour Z4 |
| H. Params | au moins \(m\) ; choix de la fonctionnelle de dispersion |
| I. Singularités | \(RV=0\) ⇒ \(L\) indéfini ; fenêtre trop courte ; demi-vols nulles si \(RV\) hérite de singularités amont |
| J. Causal | oui si indices \(\le t\) |
| K. Fenêtre | oui — \(m\) libre (Z5) |
| L. ≈ \(D\) ? | pas identité ; cousin possible si on ne retient que des agrégats grossiers |

**Trend vs instability :** A faible, B élevé (si dispersion de
\(\Delta L\)). Aligné.

**Verdict A :** `PROMISING` — **≠** `ACCEPTED`.

### 14.5 Famille B — dispersion des niveaux de log-volatilité

**Objets types :** \(\operatorname{disp}(L_{t-m+1},\ldots,L_t)\)
(écart-type, range, IQR, …).

| Q | Réponse |
|---|---------|
| A. Mesure | Étendue / dispersion des **niveaux** \(L\) dans la fenêtre |
| B. Invariance | oui (translation de \(L\) sous \(r\mapsto cr\)) |
| C–E. ≠ \(L,D,Q\) | ≠ \(L\) (dispersion) ; cousin de \(D\)/range pour trends ; ≠ \(Q\) |
| F–G. Trend | **échec sémantique central** : la séquence A a un **range** de \(L\) élevé (0,4) alors que le régime « change » de façon parfaitement régulière. Confond **drift / trend** avec **instabilité erratique** |
| H–K. | \(m\) + choix de disp ; causal OK ; forte dépendance à \(m\) |
| L. ≈ \(D\) | range / contraste biparti voisins de \(D\) sous trend monotone |

**Verdict B :** `REJECT` comme opérationnalisation de *volatility-regime
instability* (échoue le test trend vs instability). Utile seulement
comme **contre-exemple** documentaire.

### 14.6 Famille C — vol-of-vol relatif (échelle RV)

**Objets types :** \(\operatorname{variability}(RV)/\operatorname{level}(RV)\)
sans formule figée (CV, std/mean, …).

| Q | Réponse |
|---|---------|
| A. Mesure | Variabilité relative du niveau **additif** de \(RV\) |
| B. Invariance | oui si numérateur et dénominateur homogènes de degré 1 en \(RV\) |
| C–E. | distincts de \(L,D,Q\) en général |
| F–G. Trend | drift régulier de \(RV\) gonfle encore la variabilité des niveaux — même confusion drift/instabilité que B, souvent pire hors espace log |
| H. | \(m\) + choix var/level |
| I. | \(RV=0\) au dénominateur ; non choisi \(\varepsilon\) |
| L. | risque de faux vol-of-vol porté par le niveau si forme mal homogène ; moins aligné que A sur l'invariant multiplicatif |

**Verdict C :** `WEAK` — invariance possible, mais sémantique et
alignement multiplicatif **inférieurs** à une formulation dans
l'espace \(\Delta L\) (famille A).

### 14.7 Famille D — alternatives à faible paramétrisation

Revue **mathématique** uniquement (pas SPY). Candidats conceptuels :

1. **\(\lvert\Delta L_t\rvert\) instantané** — 0 paramètre de fenêtre
   extra (au-delà de la définition de \(RV\)/\(W\) déjà héritée).
   Causal, invariant. Très local ; bruyant ; ne résume pas une
   « instabilité de régime » sur plusieurs pas.

2. **Variation totale vs déplacement net** sur \(m\) pas :
   \[
   \mathrm{TV}_m(L)=\sum_{j=0}^{m-2}\lvert\Delta L_{t-j}\rvert,
   \qquad
   \lvert L_t-L_{t-m+1}\rvert
   \]
   L'écart \(\mathrm{TV}_m-\lvert\mathrm{net}\rvert\) (ou le ratio
   quand le net \(\neq 0\)) isole le **détour** au-delà de la tendance
   monotone. Sépare A (TV≈|net|) de B (TV≫|net|). Un paramètre \(m\).
   Singularité du ratio si net\(=0\) (régime plat oscillant) — le
   résidu \(\mathrm{TV}-\lvert\mathrm{net}\rvert\) évite une division.

3. **Comptage de changements de signe de \(\Delta L\)** (réversions)
   dans une fenêtre — invariant d'échelle, discrete, distingue tendance
   monotone (0 réversion) d'un chemin erratique. Paramètre \(m\) ;
   sensible à la quantification / bruits de signe.

| Q | Réponse synthétique |
|---|---------------------|
| Trend vs instability | (2) et (3) **conçus** pour le test A vs B |
| ≠ \(L,D,Q\) | oui en général ; (2) n'est pas \(D\) |
| Params | souvent 1 (\(m\)), parfois 0 pour \(\lvert\Delta L\rvert\) |
| Risque | sophistication inutile si on empile trop ; \(m\) reste libre |

**Verdict D :** `PROMISING` pour les formes (2)–(3) ; `INCONCLUSIVE`
sur **quelle** forme exacte — **aucune** formule acceptée.

### 14.8 Tableau comparatif

| Famille | Sémantique | Inv. échelle | Causal | vs \(L/D/Q\) | Params | Singularités | Trend vs instab. | Avantage | Objection |
|---------|------------|--------------|--------|--------------|--------|--------------|------------------|----------|-----------|
| **A** \(\operatorname{disp}(\Delta L)\) | roughness du niveau multiplicatif | oui | oui | ≠ ; cousin partiel de \(D\) | \(m\), fonctionnelle | \(RV=0\) | A bas / B haut | aligné Z2–Z4 | \(m\) libre ; bruit |
| **B** \(\operatorname{disp}(L)\) | étendue des niveaux | oui | oui | cousin \(D\) sous trend | \(m\) | \(RV=0\) | **échoue** (A haut) | simple | confond drift et instabilité |
| **C** var\((RV)\)/level\((RV)\) | vol-of-vol relatif additif | si homogène | oui | distinct | \(m\) | div. par 0 | faible / confus | classique | inférieur au log ; faux voV |
| **D** TV−\|net\| / sign flips | détour / réversions | oui | oui | distinct | \(0\)–\(1\) | net\(=0\) si ratio | **conçu** pour A≠B | faible param ; test clair | forme exacte non unique |

### 14.9 Revue adversariale (tentative de réfutation)

| Attaque | Cible | Évaluation |
|---------|-------|------------|
| Redondance cachée avec \(D\) | A, B | B : fort sous trend. A/D : faible si on mesure la roughness / les réversions, pas un contraste biparti |
| Fenêtre obligatoire | A, B, C, D(2–3) | vrai — Z5 non trivial ; seul \(\lvert\Delta L_t\rvert\) échappe en partie |
| Non-stationnarité | tous | \(Z\) décrit un état local ; ne « résout » pas la non-stationnarité globale |
| Amplification du bruit | A, D | \(\Delta L\) différencie — bruit haute fréquence ↑ \(Z\) ; peut être fidèle ou indésirable selon sémantique |
| Singularités | tous | \(L=\log RV\) hérite de \(RV=0\) ; pas d'\(\varepsilon\) |
| Faux vol-of-vol par niveau élevé | C surtout ; B | A/D en \(\Delta L\) résistent mieux (Z2) |
| Confusion trend / instabilité | **B**, souvent **C** | éliminatoire pour B |
| Sophistication inutile | D empilé | préférer une forme minimale si D retenu |
| Paramètre caché | tout « lissage » non déclaré | interdit |
| Incohérence invariant multiplicatif | objets en \(RV\) brut mal normalisés | préférer espace \(L\) / \(\Delta L\) |

**Mécanismes alternatifs — documentés, non promus comme \(Z\) principal :**

| Mécanisme | Raison de ne pas fusionner avec I02 maintenant |
|-----------|--------------------------------------------------|
| Asymétrie downside / directionnelle | ajoute le signe absent des adversaires magnitude-only ; risque de favoriser structurellement \(X\) |
| État de mémoire sérielle / ordre temporel | intéressant, trop proche de l'avantage structurel potentiel d'un \(X\) ordonné |

Pistes **disponibles** pour de futures investigations — **pas** fusionnées
ici.

### 14.10 Rappels structurels (non acceptés ici)

Structure statistique **candidate** seulement :

\[
Z_t \;\longrightarrow\;
\Delta_t^{(S)}=\operatorname{Score}_S(t)-\operatorname{Score}_X(t)
\;\longrightarrow\;
\operatorname{Spearman}(Z,\Delta^{(S)})
\]

(si score « lower is better » : \(\Delta>0\) ⇒ \(X\) meilleur que \(S\) ;
\(\rho>0\) ⇒ avantage relatif de \(X\) tend à croître avec \(Z\)).

Spearman, CRPS, inférence sous dépendance temporelle : **OPEN** —
pas de protocole statistique dans ce mandat.

**Pool de voisins (doctrine candidate) :** \(Z_t\) décrit l'état de la
**query** ; \(Z_t\) **ne filtre pas** les voisins. Pool commun
\(P_t^X=P_t^{S_1}=P_t^{S_2}=P_t^{S_3}\) avec au minimum
\(s+h\le t\). Contrôle de redondance temporelle : **OPEN**.

### 14.11 Verdicts documentaires (aucune acceptation)

| Famille | Verdict | Note |
|---------|---------|------|
| **A** | `PROMISING` | meilleure alignement sémantique + invariant multiplicatif parmi les familles « classiques » |
| **B** | `REJECT` | échoue trend vs instability |
| **C** | `WEAK` | possible mais dominé par A en espace log |
| **D** | `PROMISING` / forme exacte `INCONCLUSIVE` | TV−\|net\| et sign-flips : candidats mathématiques forts |

\[
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Meilleur(s) candidat(s) purement mathématiques (non acceptés) :**
dispersion causale de \(\Delta L\) (A) ; résidu de variation totale
ou comptage de réversions (D). **Prochaine décision humaine :**
choisir sémantiquement/mathématiquement **sans** valeur SPY.

### 14.12 Cohérence

| Contrôle | OK |
|----------|-----|
| Pas de donnée / SPY / run | oui |
| Pas de seuil / quantile / 2008–2020 | oui |
| Pas d'\(\varepsilon\) | oui |
| \(S_1/S_2/S_3\) / §9.16 inchangés | oui |
| \(C_t\) binaire non choisi | oui |
| Aucune \(Z_t\) acceptée | oui |
| I02 NOT OPENED | oui |

---

## 14A. A vs D mathematical review and temporal-scale problem

**Nature :** documentaire / mathématique / adversariale. **Aucune
donnée marché.** B et C **non rouverts.** Aucune \(Z_t\) acceptée.
I02 reste `NOT OPENED`.

**Baseline :** §14 @ `5681916` — A `PROMISING`, D `PROMISING`
(forme `INCONCLUSIVE`), B `REJECT`, C `WEAK`.

**Notation :** \(L_t=\log(RV_t)\) sur \(RV_t>0\) ;
\(\Delta L_t=L_t-L_{t-1}\). Aucune valeur de \(W\), \(m\), Disp, ni
\(\varepsilon\).

### 14A.1 Famille A — increment instability

**Forme générique (Disp non fixée) :**

\[
Z_A(t)
=
\operatorname{Disp}\bigl(\Delta L_{t-m+2},\ldots,\Delta L_t\bigr)
\]

(\(m\) niveaux \(L\) ⇒ \(m-1\) incréments.)

| ID | Propriété | Statut |
|----|-----------|--------|
| **A1** | \(r\mapsto c r\) (\(c>0\)) | \(L\mapsto L+\log c\) ⇒ \(\Delta L\) inchangé ⇒ \(Z_A\) invariant |
| **A2** | \(L\mapsto L+\mathrm{const}\) | idem ; invariant |
| **A3** | \(L_i=a\) constant | tous \(\Delta L=0\) ⇒ Disp\(=0\) (toute Disp raisonnable nulle sur vecteur nul) |
| **A4** | \(L_i=a+b i\) affine | \(\Delta L\equiv b\) ⇒ Disp autour de ce centre **= 0** si Disp mesure la **dispersion** (var, écart-type, MAD autour de la médiane/moyenne des \(\Delta L\)). Une « Disp » = moyenne de \(\lvert\Delta L\rvert\) **sans centrage** reste \(\lvert b\rvert\) — ce n'est plus une dispersion d'instabilité d'incréments, c'est une intensité de drift |
| **A5** | accélération monotone (\(\Delta L\) même signe, non constant) | Disp **centrée** > 0 : A classe l'accélération comme instabilité d'incréments **sans** retournement |
| **A6** | oscillation (signes alternants) | Disp typiquement élevée |
| **A7** | outliers \(\Delta L\) | var / écart-type : sensibles ; MAD : plus résistant — **Disp non choisie** |
| **A8** | lien avec \(D\) de \(S_2\) | \(D=\log(RV^{\mathrm{late}}/RV^{\mathrm{early}})\) = contraste **biparti** de niveaux, pas Disp\((\Delta L)\). Pas d'identité |
| **A9** | A ≈ \(D\) complexe ? | seulement si Disp et \(m\) collapsent vers un contraste deux blocs (ex. moyenne des \(\Delta L\) sur early vs late ≈ \(D\)). Ce n'est **pas** la forme générique Disp |

**Disp (statut) :** `UNFIXED`. Comparaison conceptuelle seulement :

| Disp | Sous trend affine (A4) | Sous choc unique | Remarque |
|------|------------------------|------------------|----------|
| variance / σ | 0 | > 0 | classique ; outliers |
| MAD (autour centre empirique) | 0 | > 0 | plus robuste |
| mean \(\lvert\Delta L\rvert\) **non centré** | \(\lvert b\rvert\) | > 0 | **échoue** A4 comme « instabilité » — mesure l'intensité du drift |

**Implication :** pour que A opérationnalise *increment instability* et non
*drift intensity*, Disp doit être une **vraie dispersion** (centrée),
pas une norme brute des incréments.

### 14A.2 Famille D — excess path length \(E=\mathrm{TV}-\mathrm{NET}\)

Sur \(m\) niveaux \(L_{t-m+1},\ldots,L_t\) :

\[
\mathrm{TV}_t=\sum_{j=0}^{m-2}\lvert\Delta L_{t-j}\rvert,
\qquad
\mathrm{NET}_t=\lvert L_t-L_{t-m+1}\rvert,
\qquad
E_t=\mathrm{TV}_t-\mathrm{NET}_t
\]

| ID | Affirmation | Statut |
|----|-------------|--------|
| **D1** | \(E_t\ge 0\) | **prouvé** : inégalité triangulaire \(\sum\lvert a_i\rvert\ge\lvert\sum a_i\rvert\) avec \(a_i=\Delta L\) |
| **D2** | \(E_t=0\) sur toute trajectoire monotone | **prouvé** au sens faible : \(E=0\) **ssi** tous les \(\Delta L\) sont \(\ge 0\) ou tous \(\le 0\) (zéros admis). Toute trajectoire monotone (non-stricte) ⇒ \(E=0\) |
| **D3** | \(E>0\) ⇒ retournement ? | **oui** : \(E>0\) **ssi** il existe au moins un \(\Delta L>0\) **et** un \(\Delta L<0\) dans la fenêtre. Les plateaux \(\Delta L=0\) n'empêchent ni n'imposent \(E>0\). Sens précis : **backtracking / changement de sens du chemin de \(L\)**, pas nécessairement deux incréments consécutifs non nuls de signes opposés si des zéros s'intercalent |
| **D4** | invariant \(L\mapsto L+c\) / \(r\mapsto cr\) | **oui** (\(\Delta L\) et différences de \(L\) inchangés) |
| **D5** | sens géométrique | **longueur de chemin en excès** par rapport au déplacement net : *excess path length* / *backtracking*. Termes **non** démontrés comme synonymes de « regime instability » — seulement le backtracking du chemin \(L\) |
| **D6** | \(E/\mathrm{TV}\) | domaine : \(\mathrm{TV}>0\) ; si \(\mathrm{TV}=0\) (chemin plat) : **indéfini** (pas d'\(\varepsilon\)). Invariance d'échelle supplémentaire (homogène de degré 0). **Perd** l'amplitude absolue du détour. **Non accepté** |
| **D7** | sign-flips | comptage de changements de signe de \(\Delta L\) (règle pour \(\Delta L=0\) : **OPEN** / indéfini ou ignore les zéros). Information **ordinale** grossière du même concept de retournement ; **pas** l'amplitude du backtracking. Discrétisation, pas un objet orthogonal à \(E\) |

### 14A.3 Contre-exemples synthétiques (aucune donnée marché)

Convention : \(m=5\) niveaux ; Disp = écart-type empirique des
\(\Delta L\) (illustratif, **non choisi**) ; SF = nombre de passages
d'un signe strict à l'autre en ignorant les zéros.

| Cas | \(L\) | \(\Delta L\) | A (σ) | \(E=\mathrm{TV}-\mathrm{NET}\) | SF | Lecture |
|-----|-------|--------------|-------|--------------------------------|-----|---------|
| **1** constant | \([1,1,1,1,1]\) | \([0,0,0,0]\) | 0 | \(0-0=0\) | 0 | stable |
| **2** trend linéaire | \([1,1.1,1.2,1.3,1.4]\) | \([0.1]{\times}4\) | 0 | \(0.4-0.4=0\) | 0 | A : pas d'instabilité d'incréments ; D : pas de backtracking |
| **3** accélération monotone | \([1,1.1,1.3,1.6,2.0]\) | \([0.1,0.2,0.3,0.4]\) | > 0 | \(1.0-1.0=0\) | 0 | **A↑, E=0** : A voit instabilité d'incréments ; D : transition monotone |
| **4** oscillation | \([1,1.2,1.0,1.2,1.0]\) | \([+0.2,-0.2,+0.2,-0.2]\) | > 0 | \(0.8-0=0.8\) | 3 | A↑ et E↑ |
| **5** single jump then stable | \([1,1,1,2,2]\) | \([0,0,1,0]\) | > 0 | \(1-1=0\) | 0 | **discriminant** — voir §14A.4 |
| **6** single reversal | \([1,1.2,1.4,1.2,1.0]\) | \([+0.2,+0.2,-0.2,-0.2]\) | > 0 | \(0.8-0=0.8\) | 1 | A↑ et E↑ |

### 14A.4 Cas 5 — saut unique puis stable (question scientifique)

\[
L=[1,1,1,2,2]
\quad\Rightarrow\quad
\mathrm{TV}=1,\;\mathrm{NET}=1,\;E=0
\]

mais Disp\((\Delta L)>0\) dès que Disp voit le choc \(+1\) hors
d'un centre proche de 0.

**Ce que chaque mesure appelle « instabilité » :**

| Mesure | Sur le cas 5 |
|--------|----------------|
| **A** | le **changement** du niveau multiplicatif (intensité / dispersion des incréments) — y compris une **transition unidirectionnelle** |
| **\(E\)** | uniquement le **backtracking** — un changement brutal mais monotone n'en est **pas** |
| **SF** | aucun retournement |

**Question forcée (tranchée en §14A.12) :**

> Un changement brutal mais unidirectionnel de régime est-il une
> *instabilité*, ou seulement une *transition* ?

**Décision humaine :** ce sont des manifestations **pertinentes**
d'instabilité locale du régime (avec l'accélération monotone,
cas 3). ⇒ famille **A** retenue comme primaire candidate ;
voir §14A.12. **Pas** d'acceptation de \(Z_t\).

### 14A.5 A vs D — concepts irréductibles ?

\[
\text{A : instability of volatility \emph{changes} (dispersion des incréments)}
\]

\[
\text{D-\(E\) : reversal / backtracking of the volatility \emph{path}}
\]

**Affirmation :** « A high ⇏ D high » et « D high ⇏ A high ».

| Direction | Statut | Contre-exemple |
|-----------|--------|----------------|
| A haut ⇏ E haut | **prouvé** (nuancé) | **Cas 3** et **cas 5** : A > 0, \(E=0\) |
| E haut ⇏ A haut | **nuancé** | difficile avec Disp = σ : un retournement d'amplitude non nulle force souvent Disp > 0. Contre-exemple limite : deux incréments opposés égaux et le reste nul — A > 0 aussi. En pratique, \(E>0\) ⇒ Disp centrée **souvent** > 0 ; l'implication inverse est la faille claire |

**Conclusion :** A et D sont **mathématiquement distincts**. La distinction
irréductible se lit sur les trajectoires **monotones non-stationnaires
en incréments** (accélération, saut unique). **Aucun** score combiné
A+D.

### 14A.6 Échelle \(m\) — trois statuts

| Option | Contenu | Évaluation |
|--------|---------|------------|
| **M1** \(m\) indépendant | nouvel hyperparamètre de \(Z\) | liberté max ; snooping max ; justification lourde |
| **M2** \(m:=W\) (ou lien déterministe) | dérivé de la fenêtre de représentation | parcimonieux ; couple horizon d'état et horizon de \(X\)/\(S\) ; **\(W\) non accepté** pour I02 |
| **M3** minimal structurel | ex. \(\lvert\Delta L_t\rvert\) seul | élimine \(m\) mais détruit la sémantique « régime » (trop local, pas de chemin) |

**\(m=W\) — arguments :**

| Pour | Contre |
|------|--------|
| même cutoff informationnel | horizon d'état ≠ horizon de représentation |
| même échelle locale | couplage artificiel |
| pas d'hyperparamètre temporel **supplémentaire** | \(W\) lui-même OPEN pour I02 |
| alignement conceptuel query/état | l'instabilité peut exiger une autre profondeur |

**Verdict documentaire \(m=W\) :** `DEFENSIBLE BUT NOT FORCED`.

**Statut de \(m\) :** `UNRESOLVED` — pas de valeur ; pas d'acceptation
de M1/M2/M3. Recommandation documentaire : **ne pas** inventer un
\(m\) libre avant d'avoir tranché A vs D sémantiquement ; si une
échelle est nécessaire, **M2 est la seule option parcimonieuse
non rejetée**, sans être forcée.

### 14A.7 Double fenêtre

Chaîne :

\[
(r_s)_{s\le t}
\;\longrightarrow\;
RV_t\ ({\sim}W)
\;\longrightarrow\;
(L_{t-m+1},\ldots,L_t)
\;\longrightarrow\;
Z_t
\]

| Effet | Conséquence |
|-------|-------------|
| Mémoire effective | empan historique \(\approx W+(m-1)\) pas (chevauchements de fenêtres \(RV\)) — **plus long** que \(m\) nominal |
| Chevauchement | \(RV_t\) et \(RV_{t-1}\) partagent \(W-1\) rendements ⇒ \(\Delta L\) **sériellement dépendant** même si \(r\) est faible mémoire |
| Lissage implicite | \(RV\) agrège déjà ; \(Z\) agrège des \(RV\) — double lissage |
| \(W\) multi-rôles | même lettre pour représentation \(X/S\) et pour construction de \(L\) : risque de confusion de rôles si \(m=W\) |

Pas de résolution empirique.

### 14A.8 Singularités (aucun \(\varepsilon\))

| Cas | Statut |
|-----|--------|
| \(RV=0\) | \(L\) **indéfini** |
| \(\mathrm{TV}=0\) | \(E=0\) ; \(E/\mathrm{TV}\) **indéfini** |
| \(\Delta L=0\) | neutre pour \(E\) ; pour SF : règle de signe **non fixée** |
| Disp avec < 2 incréments non triviaux | Disp centrée mal définie / dégénérée selon Disp |
| Plateaux | admissibles ; cas 5 |

### 14A.9 Revue adversariale

**Attaques sur A :**

| Attaque | Évaluation |
|---------|------------|
| Version multi-point de \(D\) ? | **non** en généricité Disp ; oui seulement sous collapse biparti |
| Bruit par différenciation | **oui** — coût réel |
| Choc unique domine Disp | **oui** (cas 5) — peut être fidèle ou indésirable selon sémantique |
| Accélération monotone = « instable » | **oui** (cas 3) — tension avec « régime établi en transition » |
| Dépendance Disp et \(m\) | **oui** — tous deux UNFIXED |

**Attaques sur D-\(E\) :**

| Attaque | Évaluation |
|---------|------------|
| Ignore accélération / saut monotone | **oui** (cas 3, 5) — **feature ou bug** selon réponse §14A.4 |
| SF trop sensibles au bruit | **oui** pour D-sign-flips |
| \(E\) dominé par amplitude | \(E\) croît avec l'ampleur des allers-retours ; \(E/\mathrm{TV}\) y remédie au prix de \(\mathrm{TV}=0\) |
| Backtracking ≠ regime instability | objection sémantique restante — le terme démontré est backtracking, pas « instabilité » au sens large |
| Dépendance à \(m\) | **oui** |

### 14A.10 Verdicts documentaires (§14A, avant décision §14A.12)

| Objet | Verdict §14A |
|-------|----------------|
| **A** | `PROMISING` |
| **D-TV-NET** (\(E\)) | `PROMISING` |
| **D-sign-flips** | `WEAK` |
| **\(m=W\)** | `DEFENSIBLE BUT NOT FORCED` |

A et \(E\) **distincts** (cas 3, 5). Suite : §14A.12.

### 14A.12 Décision humaine — famille A primaire candidate

**Statut :** décision sémantique humaine. **Pas** une acceptation de
\(Z_t\).

| Objet | Statut figé |
|-------|-------------|
| Famille **A** (\(\operatorname{Disp}(\Delta L)\)) | `PRIMARY SEMANTIC CANDIDATE` pour \(Z_t\) |
| Cas 3 (accélération monotone) | manifestation **pertinente** d'instabilité locale |
| Cas 5 (saut unidirectionnel brutal) | manifestation **pertinente** d'instabilité locale |
| \(E=\mathrm{TV}-\lvert\mathrm{net}\rvert\) | **mécanisme alternatif** (backtracking / path reversal) — **pas** métrique de robustesse de A |
| D-sign-flips | `WEAK` (inchangé) |
| Disp | `ACCEPTED` = \(\mathrm{Std}_{\mathrm{pop}}\) (§14B.11) |
| \(m\) | `UNRESOLVED` |
| Formule \(Z_t\) | **non acceptée** (incomplete sans \(m\)) |

\[
\boxed{\text{Family A = primary semantic candidate}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Clarification §9.16 :** \(E\) n'entre **pas** dans un ensemble de
robustesse métrique pour A. Ce sont deux **mécanismes** distincts ;
A est le candidat sémantique primaire ; \(E\) reste disponible comme
piste alternative / future investigation, sans obligation de
co-survie avec A pour interpréter un résultat sur A.

**Prochaines questions OPEN (étroit) :** \(m\) (dont statut \(m=W\)).
Disp figée §14B.11. Toujours sans donnée, sans \(\varepsilon\), sans
acceptation \(Z_t\).

### 14A.13 Cohérence

| Contrôle | OK |
|----------|-----|
| B/C non rouverts | oui |
| Pas de nouveau candidat diluant | oui |
| Pas de Disp / \(m\) / \(W\) / \(\varepsilon\) choisis | oui |
| Pas de données marché | oui |
| Décisions ACCEPTED antérieures intactes | oui |
| A primaire candidate ; \(Z_t\) non acceptée | oui |
| \(E\) = alternatif, ≠ robustesse de A | oui |
| I02 NOT OPENED | oui |

---

## 14B. Dispersion functional for family A — MAD / Std / MeanAD

**Nature :** mathématique / adversariale. **Aucune donnée.** Décisions
§14A.12 **non rouvertes.** Aucune \(Z_t\) acceptée. I02 =
`NOT OPENED`.

**Baseline sémantique :** A = variabilité des changements du niveau
de log-volatilité ; saut unidirectionnel **doit** être détecté ;
accélération monotone **peut** compter ; \(E\) = mécanisme alternatif
(≠ robustesse de A).

**Notation :** \(y=(y_1,\ldots,y_n)\), \(y_i=\Delta L\) sur la fenêtre ;
\(\bar y=n^{-1}\sum y_i\). Critère « différentiabilité / \(C^\infty\) »
**retiré** — non pertinent ; \(\sqrt{\mathrm{Var}}\) n'est d'ailleurs
pas régulier en variance nulle.

### 14B.1 MAD (médiane) — rejet pour I02/A

Cas canonique (sémantique humaine) :

\[
L=[1,1,1,2,2]
\quad\Rightarrow\quad
y=[0,0,1,0]
\quad(n=4)
\]

Médiane de \(y\) : \(0\). Écarts absolus à la médiane :
\([0,0,1,0]\). Médiane de ceux-ci : \(0\).

\[
\operatorname{MAD}_{\mathrm{median}}(y)=0
\]

Le saut unique exigé **n'est pas détecté** (breakdown : majorité
d'incréments nuls). Cela **suffit** à classer :

\[
\boxed{\operatorname{MAD}_{\mathrm{median}}=\texttt{REJECT}\text{ pour I02/A}}
\]

**Portée :** rejet **local** à I02/famille A. Pas de généralisation
à d'autres usages de la MAD.

### 14B.2 Deux candidats restants

\[
Z_t^{(2)}=\operatorname{Std}(y),
\qquad
Z_t^{(1)}=\operatorname{MeanAD}(y)
=\frac1n\sum_{i=1}^n\lvert y_i-\bar y\rvert
\]

MeanAD = déviation absolue moyenne **autour de la moyenne
arithmétique** — **pas** MAD médiane.

Propriété commune fondamentale :

\[
y_i=c\ \forall i
\quad\Longrightarrow\quad
Z^{(1)}=Z^{(2)}=0.
\]

### 14B.3 Propriétés comparées

| Propriété | Std | MeanAD |
|-----------|-----|--------|
| Translation \(y\mapsto y+b\) | invariant | invariant |
| Équivariance \(y\mapsto a y\) | \(\lvert a\rvert\,\mathrm{Std}\) | \(\lvert a\rvert\,\mathrm{MeanAD}\) |
| \(y\) constant | 0 | 0 |
| Saut unique | > 0 (§14B.4) | > 0 (§14B.4) |
| Plusieurs chocs | ↑ avec énergie \(L_2\) | ↑ plus linéaire en \(L_1\) |
| Oscillation régulière | > 0 | > 0 |
| Accélération monotone | > 0 si \(\Delta L\) non constant | > 0 idem |
| Incrément extrême | dominance **quadratique** | réponse **linéaire** en \(\lvert y_i-\bar y\rvert\) |
| Dépendance à \(n\) | oui (formule saut ; facteur \(n\) vs \(n-1\)) | oui |
| Géométrie | \(L_2\) (Euclidienne centrée) | \(L_1\) centrée (mean) |
| Singularité | \(n=1\) indéfini / dégénéré ; \(RV=0\) amont | idem ; pas de racine |

### 14B.4 Saut unique — formules exactes (\(n\ge 2\), \(\delta\neq 0\))

\[
y=(0,\ldots,0,\delta,0,\ldots,0)
\quad\text{(un seul nonzero)}
\qquad
\bar y=\delta/n
\]

Somme des carrés centrés :

\[
\sum(y_i-\bar y)^2
=\frac{(n-1)\delta^2}{n}.
\]

**Std population** (dénominateur \(n\)) :

\[
\operatorname{Std}_n(y)
=\lvert\delta\rvert\,\frac{\sqrt{n-1}}{n}.
\]

**Std sample** (dénominateur \(n-1\)) :

\[
\operatorname{Std}_{n-1}(y)
=\frac{\lvert\delta\rvert}{\sqrt{n}}.
\]

Relation : \(\operatorname{Std}_{n-1}=\sqrt{n/(n-1)}\,\operatorname{Std}_n\).

**MeanAD :**

\[
\operatorname{MeanAD}(y)
=\frac{2(n-1)}{n^2}\,\lvert\delta\rvert.
\]

Les deux détectent le saut (\(\propto\lvert\delta\rvert\)) ; seuls les
préfacteurs en \(n\) diffèrent.

### 14B.5 Population vs sample (\(n\) vs \(n-1\))

Si \(n\) est **fixe** pour toutes les queries \(t\) (même \(m\)), alors

\[
\operatorname{Std}_{n-1}(y_t)
=
\sqrt{\frac{n}{n-1}}
\,\operatorname{Std}_n(y_t)
\]

est une **re-échelle déterministe** indépendante de \(y_t\). Les
**rangs** de \(Z_t\) (donc Spearman avec tout \(\Delta_t\)) sont
**identiques**.

**Verdict :** pour un état déterministe à \(n\) fixé, \(n\) vs \(n-1\)
est une **convention de définition**, **pas** une question
scientifique matérielle pour un estimand ordinal. Devient matériel
seulement si \(n\) varie entre comparaisons ou si l'échelle absolue
de \(Z\) (hors rangs) est utilisée. **Rien n'est choisi ici.**

### 14B.6 Attaque queues / multi-chocs (synthétique)

| Fenêtre | Lecture |
|---------|---------|
| \(y=(10,0,0,0)\) | Std élevé (quadratique) ; MeanAD proportionnel à \(\lvert\delta\rvert\) mais plus bas relativement |
| \(y=(2,2,-2,-2)\) | instabilité « répartie » : MeanAD plus compétitif vs un mega-choc de même énergie \(L_2\) |

Std peut être **dominé par un seul** \(\lvert\Delta L\rvert\) extrême
(détecteur de choc \(L_2\)). MeanAD peut **sous-représenter** une
instabilité très concentrée que la sémantique (saut unique pertinent)
considère pourtant forte — tension, pas élimination (le saut simple
reste détecté).

### 14B.7 Rank equivalence — BLOCKING pour Spearman

Question : \(\operatorname{Std}\) et \(\operatorname{MeanAD}\) sont-ils
des transformées **monotones** l'un de l'autre sur l'espace des
fenêtres \(y\) ?

**Non.** Contre-exemple explicite (\(n=4\), moyennes nulles) :

\[
y^{(A)}=(2,-2,0.1,-0.1),
\qquad
y^{(B)}=(1.2,1.2,-1.2,-1.2)
\]

| | \(\operatorname{Std}_n\) | MeanAD |
|--|--------------------------|--------|
| \(y^{(A)}\) | \(\sqrt{2.005}\approx 1.416\) | \(1.05\) |
| \(y^{(B)}\) | \(1.2\) | \(1.2\) |

\[
\operatorname{Std}(y^{(A)})>\operatorname{Std}(y^{(B)})
\quad\text{mais}\quad
\operatorname{MeanAD}(y^{(A)})<\operatorname{MeanAD}(y^{(B)}).
\]

**Rank reversal.** Donc pour

\[
\rho_{\mathrm{Spearman}}(Z,\Delta),
\]

le choix Std vs MeanAD peut **changer l'estimand observé**. MeanAD
**n'est pas** une simple « variante de robustesse » au sens §9.16
(co-survie d'une même conclusion sous géométries équivalentes pour
un même contrôle) : ce sont deux définitions potentiellement
**ordinalement distinctes** de « davantage d'instabilité ».

### 14B.8 Revue adversariale

**Attaques Std :** dominance de queue \(L_2\) ; domination par un choc ;
convention \(n\) vs \(n-1\) (immaterial si \(n\) fixe) ; dérive conceptuelle
vers « détecteur de choc ».

**Attaques MeanAD :** moindre sensibilité aux extrêmes (peut sous-peser
une instabilité concentrée) ; \(\bar y\) encore influencé par outliers ;
pas d'interprétation Euclidienne canonique ; **rank disagreement** avec
Std ; appeler cela « robustesse » **masque** un changement d'estimand.

### 14B.9 Verdicts (aucune acceptation de \(Z_t\))

| Fonctionnelle | Verdict |
|---------------|---------|
| **MAD** (médiane) | `REJECT` (I02/A only) |
| **Std** | `PROMISING` |
| **MeanAD** (autour de la moyenne) | `PROMISING` |

**Réponses imposées :**

1. **Plus directe sémantiquement ?** Les deux implémentent une
   Disp **centrée** détectant saut et accélération. Std = géométrie
   \(L_2\) (chocs amplifiés) ; MeanAD = \(L_1\) (plus linéaire). Aucune
   n'est encore PRIMARY figée — **décision humaine** suivante.
2. **Rank-equivalent ?** **Non** (§14B.7).
3. **MeanAD = robustness variant ?** **Non** légitimement au sens
   §9.16, tant que Spearman est l'estimand candidat.
4. **PRIMARY + ROBUSTNESS vs incertitude sémantique ?** Un désaccord
   de rang implique **incertitude sémantique** sur la géométrie
   (\(L_2\) vs \(L_1\)) de « davantage d'instabilité », **pas** un
   schéma robustesse gratuit. Préenregistrer le rôle de chaque
   fonctionnelle **avant** toute donnée. Options documentaires :
   (i) choisir PRIMARY unique ; (ii) préenregistrer
   \(\{Z^{(2)},Z^{(1)}\}\) avec règle type §9.16 sur la **conclusion**
   — mais ce n'est **pas** automatique.
5. **Population vs sample ?** **Non matériel** pour rangs à \(n\) fixe
   (§14B.5).

\[
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Recommandation documentaire (§14B, historique) :** tranchée en
§14B.11 — géométrie \(L_2\) / \(\mathrm{Std}_{\mathrm{pop}}\).

### 14B.10 Cohérence (revue)

| Contrôle | OK |
|----------|-----|
| §14A.12 non rouvert | oui |
| MAD rejetée localement seulement | oui |
| Pas de critère \(C^\infty\) | oui |
| Rank reversal documenté | oui |
| Pas de \(m\)/\(W\)/\(\varepsilon\)/données | oui |
| I02 NOT OPENED | oui |

### 14B.11 Décision humaine — \(\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\)

**Statut :** `ACCEPTED` pour I02 / famille A. **Pas** d'acceptation
de \(Z_t\). \(L_1/L_2\) **ne se rediscute plus** sauf contradiction
mathématique nouvelle.

\[
\operatorname{Disp}(y)
=
\mathrm{Std}_{\mathrm{pop}}(y)
=
\sqrt{
\frac1n\sum_{i=1}^{n}(y_i-\bar y)^{2}
}
=
\frac{\lVert y-\bar y\,\mathbf{1}\rVert_{2}}{\sqrt{n}}
\]

avec \(y_i=\Delta L_i\), \(L_t=\log(RV_t)\) sur \(RV_t>0\).

**Géométrie :** distance euclidienne normalisée du vecteur
d'incréments à l'espace des incréments constants
\(S=\{c\mathbf{1}:c\in\mathbb{R}\}\).

**Justification acceptée :**

1. \(\operatorname{Disp}=0\) si \(\Delta L_i=c\) pour tout \(i\)
   (volatilité constante, hausse ou baisse **régulière**) ;
2. \(\operatorname{Disp}>0\) si le taux de changement varie
   (accélération, décélération, saut unidirectionnel, oscillation) ;
3. un choc isolé **appartient** à la sémantique — ne pas l'éliminer
   comme outlier ;
4. géométrie euclidienne explicite sur les écarts à une dynamique
   constante ;
5. dénominateur **population** \(n\) : la fenêtre **est** l'objet
   d'état, pas un échantillon pour estimer sans biais une variance
   hypothétique.

| Fonctionnelle | Statut figé |
|---------------|-------------|
| \(\mathrm{Std}_{\mathrm{pop}}\) | **`ACCEPTED`** (Disp pour I02/A) |
| MAD (médiane) | `REJECTED FOR I02/A` |
| MeanAD (autour de la moyenne) | `VALID ALTERNATIVE GEOMETRY` — **not retained** for I02/A ; **≠** robustness variant |
| \(E=\mathrm{TV}-\lvert\mathrm{net}\rvert\) | `ALTERNATIVE MECHANISM` (path reversal) — pas composante de A, pas à combiner / tester maintenant |

**Formules saut unique (§14B.4) :** déjà correctes
(\(\lvert\delta\rvert\sqrt{n-1}/n\), \(\lvert\delta\rvert/\sqrt{n}\),
\(2(n-1)\lvert\delta\rvert/n^{2}\)) — **aucune correction**.

\[
\boxed{\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\ \texttt{ACCEPTED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Encore OPEN :** architecture §14C \((W_X,W_{RV},m_Z)\) ; CRPS ;
Spearman ; inférence ; ouverture I02. Formule \(Z_t\) **incomplète**
sans horizons.

### 14B.12 Cohérence (post-décision)

| Contrôle | OK |
|----------|-----|
| Disp = Std_pop ACCEPTED | oui |
| MeanAD ≠ robustesse ; MAD REJECT | oui |
| \(E\) inchangé (alternatif) | oui |
| Pas de choix \(m\)/\(W\) | oui |
| `NO Z_t ACCEPTED` ; I02 NOT OPENED | oui |

---

## 14C. Architecture temporelle de \(Z_t\) — trois horizons

**Nature :** documentaire / mathématique. **Aucun chiffre**
(pas 10 / 20 / 63 / 252). Disp §14B.11 **non rouverte.** Aucune
\(Z_t\) acceptée. I02 = `NOT OPENED`.

### 14C.0 Chaîne causale candidate

\[
r
\xrightarrow[\text{estimation}]{W_{RV}}
RV
\xrightarrow{\log}
L
\xrightarrow{\Delta}
\Delta L
\xrightarrow[\mathrm{Std}_{\mathrm{pop}}]{m_Z}
Z
\]

Trois symboles **obligatoires** (rôles distincts) :

| Symbole | Rôle |
|---------|------|
| \(\boxed{W_X}\) | horizon de **représentation** : combien de rendements constituent l'objet géométrique \(X_t\) (et, par alignement, les adversaires \(S\) si même \(W\)) |
| \(\boxed{W_{RV}}\) | horizon d'**estimation du niveau** de volatilité : échelle de \(RV_t\), donc de \(L_t\) |
| \(\boxed{m_Z}\) | horizon d'**observation de l'instabilité** de ce niveau : combien d'incréments \(\Delta L\) entrent dans \(\mathrm{Std}_{\mathrm{pop}}\) |

**Aucune raison mathématique** qu'ils soient égaux *par nature*. Une
égalité éventuelle serait une **convention de parcimonie** à justifier,
pas une identité structurelle.

**Ordre de décision :** \(m_Z\) **ne** se résout **pas** avant
\(W_{RV}\). Dépendance :

\[
W_{RV}\;\rightarrow\;L_t\;\rightarrow\;\Delta L_t\;\rightarrow\;
\mathrm{Std}_{\mathrm{pop}}^{(m_Z)}\;\rightarrow\;Z_t.
\]

Choisir \(m_Z\) sans savoir ce qu'est une observation élémentaire
\(\Delta L_t\) serait prématuré.

### 14C.1 Identités rolling (stride 1) — overlap mécanique

Construction candidate **explicite** (pas encore acceptée comme seule
possible) : \(RV\) rolling, pas journalier = 1.

\[
RV_t
=
\sqrt{
\frac1{W_{RV}}
\sum_{j=0}^{W_{RV}-1}r_{t-j}^{2}
}
\quad(RV_t>0)
\]

Différence de variance réalisée au carré :

\[
RV_t^{2}-RV_{t-1}^{2}
=
\frac{r_t^{2}-r_{t-W_{RV}}^{2}}{W_{RV}}.
\]

Deux \(RV\) consécutifs ne diffèrent que par **une sortie et une
entrée**. Propriété structurelle forte : une grande partie du
« mouvement » de \(RV_t\) est la **rotation** des observations dans
la fenêtre.

Après log :

\[
\Delta L_t
=
\log RV_t-\log RV_{t-1}
=
\frac12
\log\!
\left(
\frac{\sum_{j=0}^{W_{RV}-1}r_{t-j}^{2}}
{\sum_{j=1}^{W_{RV}}r_{t-j}^{2}}
\right).
\]

**Conséquence sémantique :** \(Z_t=\mathrm{Std}_{\mathrm{pop}}\) sur une
fenêtre de \(\Delta L\) ne mesure **pas** une mystérieuse « vol-of-vol »
abstraite. Il mesure la dispersion d'une **variation de volatilité
rolling**, dont la dynamique dépend structurellement de \(W_{RV}\).

### 14C.2 Empan causal et observations non indépendantes

Pour produire \(Z_t\) à la date \(t\) (sous rolling / stride 1) :

| Étape | Empan en rendements (ordre de grandeur) |
|-------|----------------------------------------|
| Un \(RV_s\) | \(W_{RV}\) sessions |
| Un \(\Delta L_s\) | implique deux \(RV\) ⇒ empan \(W_{RV}+1\) |
| \(m_Z\) niveaux \(L\) (donc \(n=m_Z-1\) incréments) | du plus ancien rendement dans \(RV_{t-m_Z+1}\) au plus récent dans \(RV_t\) |

Empan calendaire causal exact (rendements) :

\[
\operatorname{span}(Z_t)
=
W_{RV}+(m_Z-1)
\]

sessions (du rendement d'indice \(t-W_{RV}-m_Z+2\) à \(t\), selon
convention d'indexation inclusive — l'ordre de grandeur est
\(W_{RV}+m_Z\), **pas** \(m_Z\) seul).

**Point critique :** cet empan calendaire **ne** signifie **pas**
autant d'observations **indépendantes** d'information sur
l'instabilité. Les \(\Delta L\) successifs sont **fortement
dépendants** via l'overlap des fenêtres \(RV\) (rotation d'une seule
observation). Nominal \(m_Z\) ≠ taille d'échantillon i.i.d.

### 14C.3 Stride / blocs — liberté à ne pas multiplier

Constructions conceptuellement possibles :

| Construction | Propriété |
|--------------|-----------|
| Rolling, stride 1 | \(Z_t\) disponible chaque jour ; overlap maximal |
| Blocs non chevauchants | \(\Delta L\) moins mécaniquement corrélés ; \(Z\) moins fréquemment défini / ou sur grille |
| Autre stride préspécifié | paramètre supplémentaire |

**Baseline naturelle candidate :** rolling / stride 1, parce que
\(Z_t\) doit être un état de **query journalière**. Ce n'est **pas**
encore une acceptation formelle — mais c'est le défaut à rendre
**explicite** plutôt qu'accidentel.

**Interdit dans ce mandat :** introduire un hyperparamètre `stride`
à optimiser. Identifier le nécessaire ; éliminer les libertés
inutiles. Si stride 1 est retenu plus tard, le figer comme
construction, pas comme bouton.

### 14C.4 \(W_{RV}\) peut-il être dérivé de \(W_X\) ?

**Question déterminante.**

| Argument pour dériver (\(W_{RV}:=W_X\) ou lien déterministe) | Argument contre (décision indépendante) |
|---------------------------------------------------------------|------------------------------------------|
| Parcimonie : un seul horizon « local » | Rôles distincts : représentation géométrique ≠ estimation du **niveau** de vol |
| Même cutoff informationnel que \(X\) | \(X\) encode la trajectoire des \(r\) ; \(RV\) **agrège** les \(r^{2}\) — sémantiques différentes |
| Alignement adversaires \(S\) si \(S\) utilise le même \(RV\) | Les adversaires \(S_1/S_2/S_3\) **utilisent déjà** un \(RV\) de fenêtre \(W\) (héritage I01 candidat) — coupler \(W_{RV}\) à \(W_X\) est naturel **pour la cohérence \(X\) vs \(S\)**, mais ce n'est pas une preuve que ce \(W\) est l'échelle juste pour \(L\) dans \(Z\) |
| Évite un hyperparamètre | Dénaturer l'expérience : si \(W_X\) est choisi pour la géométrie kNN / dimension, forcer la même échelle pour le **niveau** de vol peut fausser ce que \(\Delta L\) signifie |

**Verdict documentaire :**

\[
\boxed{W_{RV}\text{ vs }W_X:\ \texttt{DEFENSIBLE TO COUPLE},\ \texttt{NOT FORCED}}
\]

Plus précisément :

- Pour l'expérience **adversariale** \(X\) vs \(S\) : utiliser le
  **même** estimateur \(RV\) (donc même \(W_{RV}\)) dans \(S\) et dans
  la construction de \(L\) pour \(Z\) est **fortement défendable** —
  sinon \(Z\) et \(S\) ne parlent pas du même « niveau ».
- Identifier ce \(W_{RV}\) commun avec \(W_X\) (longueur du vecteur
  \(X\)) est une **convention de parcimonie / héritage**, **pas** une
  nécessité mathématique. Ce peut être la même décision humaine
  (« un seul \(W\) local ») ou deux décisions si l'on sépare
  représentation et estimation de niveau.

**Ne pas** résoudre \(W_{RV}\) par calibration. **Ne pas** choisir de
valeur.

### 14C.5 Une fois \(W_{RV}\) fixé — justification structurelle de \(m_Z\) ?

| Option | Contenu | Évaluation |
|--------|---------|------------|
| \(m_Z:=W_{RV}\) | même profondeur que l'estimation de niveau | parcimonieux ; **non forcé** — horizon d'instabilité ≠ horizon d'agrégation \(r^{2}\) |
| \(m_Z:=W_X\) | aligné sur la représentation | idem ; confond encore les rôles |
| \(m_Z=2\) (minimal : un seul \(\Delta L\)) | \(\mathrm{Std}_{\mathrm{pop}}\) sur \(n=1\) **dégénéré** / indéfini | élimine « régime » ; **REJECT** comme seule définition |
| \(m_Z\) indépendant | horizon propre d'instabilité | liberté maximale ; snooping si non préenregistré |

Sous rolling stride 1, même \(m_Z=W_{RV}\) **ne** donne **pas**
\(W_{RV}\) « degrés de liberté » indépendants — l'overlap demeure.

**Verdict documentaire :**

\[
\boxed{m_Z:\ \texttt{NO STRUCTURAL FORCING};\ \texttt{OWN HORIZON OR PARSIMONY CONVENTION}}
\]

Il n'existe **pas**, dans cette revue, de dérivation qui fixe \(m_Z\)
uniquement à partir de \(W_{RV}\) sans convention supplémentaire.
\(m_Z\) reste soit un **horizon propre** à préenregistrer, soit une
**convention de parcimonie** explicite (\(m_Z=W_{RV}\) ou
\(m_Z=W_X\)) — à trancher **après** (ou conjointement avec) le
statut de \(W_{RV}\), **pas avant**.

### 14C.6 Implications pour le pré-cadrage

1. Remplacer le framing « problème de \(m\) » par
   **architecture temporelle à trois horizons**.
2. Ordre : clarifier / figer le rôle de \(W_{RV}\) (et son lien éventuel
   à \(W_X\) et aux \(RV\) des adversaires) **avant** ou **avec**
   \(m_Z\), jamais \(m_Z\) isolément.
3. Rendre explicite rolling / stride 1 comme baseline candidate.
4. Aucune valeur numérique ; aucun test.

### 14C.7 Verdicts

| Question | Verdict |
|----------|---------|
| Trois rôles distincts \(W_X,W_{RV},m_Z\) ? | **Oui** — établi |
| Empan calendaire = info i.i.d. ? | **Non** — overlap mécanique |
| \(W_{RV}\) vs \(W_X\) (revue §14C.4) | `DEFENSIBLE TO COUPLE`, `NOT FORCED` — **tranché** §14C.9 |
| \(m_Z\) forcé une fois \(W_{RV}\) fixé ? | `NO` — convention ou horizon propre |
| Stride 1 | baseline candidate explicite ; **non** accepté ici |
| Valeurs numériques | **interdites** / non choisies |

\[
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

### 14C.8 Cohérence (revue)

| Contrôle | OK |
|----------|-----|
| Disp / A / \(E\) non rouverts | oui |
| Aucun chiffre d'horizon | oui |
| Pas de stride à optimiser | oui |
| I02 NOT OPENED | oui |

### 14C.9 Décision humaine — \(W_{RV}:=W_X\) (comparability coupling)

**Statut :** `ACCEPTED` pour I02.

\[
\boxed{W_{RV}:=W_X}
\]

**Classification :**

```text
METHODOLOGICAL COMPARABILITY COUPLING
```

**Pas** une identité conceptuelle. Les rôles §14C.0 restent
**distincts** :

| Symbole | Sémantique (inchangée) |
|---------|------------------------|
| \(W_X\) | horizon de **représentation** de \(X_t\) |
| \(W_{RV}\) | horizon d'**estimation du niveau** (\(RV\to L\)) |
| \(m_Z\) | horizon d'**observation de l'instabilité** (\(\mathrm{Std}_{\mathrm{pop}}\) sur \(\Delta L\)) |

**Justification acceptée :** I02 compare \(X\) à \(S_1/S_2/S_3\).
Des supports historiques nominaux **différents** mélangeraient
(1) contenu / structure de représentation et (2) échelle temporelle
observée — affaiblissant l'interprétation. Le couplage impose un
**support historique nominal commun** et évite un hyperparamètre
temporel indépendant pour les résumés de volatilité.

**Ce que le couplage n'implique pas :**

- \(W_X\) et \(W_{RV}\) « mesurent la même chose » conceptuellement ;
- même mémoire effective des transformations ;
- observations dérivées indépendantes ;
- disparition de l'overlap rolling (§14C.1 inchangé) ;
- empan de \(Z\) égal à \(W_X\) seulement
  (\(\operatorname{span}\approx W_{RV}+m_Z\) demeure) ;
- \(m_Z:=W_X\) ou \(m_Z:=W_{RV}\) — **interdit** comme conséquence
  implicite.

**Relation avec \(S_1/S_2/S_3\) :** les adversaires acceptés
\([RV]\), \([RV,D]\), \([RV,Q]\) utilisent, pour I02, le **même**
\(W_{RV}\) couplé à \(W_X\). Couplage **commun** — pas un avantage
spécifique à l'un d'eux.

**Statut numérique :**

| Objet | Statut |
|-------|--------|
| Relation \(W_{RV}:=W_X\) | `ACCEPTED` |
| Valeur numérique de \(W_X\) | **OPEN** (sauf gel indépendant ultérieur) |
| Valeur numérique de \(W_{RV}\) | **OPEN** — dérivée de \(W_X\) dès que \(W_X\) est figé |
| \(m_Z\) | **OPEN** — horizon **distinct** ; prochaine question : *combien de trajectoire de \(\Delta L\) rolling pour définir l'instabilité locale de régime ?* — **pas** tranchée ici |
| Stride 1 | `BASELINE CANDIDATE` ; **NOT ACCEPTED** |

\[
\boxed{W_{RV}:=W_X\ \texttt{ACCEPTED}}
\quad
\boxed{m_Z\ \text{reste indépendant et OPEN}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Prochaine étape documentaire :** revue §14D (admissibilité
\(m_Z\)) — **faite** ; valeur \(m_Z\) encore OPEN.

### 14C.10 Cohérence (post-décision)

| Contrôle | OK |
|----------|-----|
| Couplage = comparability, ≠ identité conceptuelle | oui |
| \(m_Z\) non posé égal à \(W_X\) | oui |
| Overlap / empan §14C.1–2 inchangés | oui |
| Pas de valeur numérique ; stride non accepté | oui |
| I02 NOT OPENED | oui |

---

## 14D. Temporal response and admissibility of \(m_Z\)

**Nature :** mathématique / documentaire. **Aucune donnée.** Aucune
valeur de \(m_Z\), \(W_X\), \(W_{RV}\). Décisions ACCEPTED non
rouvertes. I02 = `NOT OPENED`.

**Objectif :** ce que \(m_Z\) contrôle (détection, mémoire, dilution,
récupération) ; propriétés d'admissibilité ; classification
structurelle — **pas** un choix numérique.

### 14D.0 Convention documentaire (anti off-by-one)

\[
\boxed{m_Z=\text{nombre de niveaux successifs }L\text{ utilisés}}
\]

\[
n_Z=m_Z-1
=\text{nombre d'incréments }\Delta L
\]

Fenêtre à la date \(t\) (exiger \(m_Z\ge 3\) i.e. \(n_Z\ge 2\) pour
une Disp non dégénérée — MZ-1) :

\[
\bigl(L_{t-m_Z+1},\ldots,L_t\bigr)
\quad\longrightarrow\quad
y
=
\bigl(\Delta L_{t-n_Z+1},\ldots,\Delta L_t\bigr)
=
\bigl(\Delta L_{t-m_Z+2},\ldots,\Delta L_t\bigr)
\]

\[
Z_t=\mathrm{Std}_{\mathrm{pop}}(y)
=
\sqrt{\frac1{n_Z}\sum_{i=1}^{n_Z}(y_i-\bar y)^{2}}
\]

**Interdit :** confondre \(m_Z\) et \(n_Z\) sans le dire.

### 14D.1 Niveau I — réponse intrinsèque de \(\mathrm{Std}_{\mathrm{pop}}\)

Espace \(y_i=\Delta L_i\) **sans** construction \(RV\).

#### A. Constant-rate — \(y_i=c\)

\[
Z=0
\quad\text{pour tout }c\text{ (Disp centrée).}
\]

#### B. Single impulse dans \(y\)

Fond \(0\), un seul \(y_\tau=\delta\neq 0\), \(n_Z\ge 2\) :

\[
Z
=
\lvert\delta\rvert\,\frac{\sqrt{n_Z-1}}{n_Z}
\]

Dilution : ordre \(\lvert\delta\rvert/\sqrt{n_Z}\). Présence à \(t\) ssi
\(t-n_Z+1\le\tau\le t\), i.e. \(\tau\le t\le\tau+n_Z-1\).
Durée exacte \(Z>0\) : **\(n_Z\)** dates. Retour à \(0\) dès
\(t=\tau+n_Z\).

#### C. Step dans \(y\)

\(y=0\) avant \(\tau\), \(y=c\neq 0\) après. Avec \(k\) incréments à
\(c\) et \(n_Z-k\) à \(0\) :

\[
Z
=
\lvert c\rvert
\sqrt{\frac{k(n_Z-k)}{n_Z^{2}}}.
\]

Pic vers \(k\sim n_Z/2\). Quand \(k=n_Z\) (nouveau taux entièrement
établi) : \(Z=0\). Récupération exacte après \(n_Z\) pas.

#### D. Accélération finie

Support fini de non-constance de \(y\), puis \(y\equiv c'\).
Détection / persistance \(\le n_Z\) après la fin de l'épisode ;
récupération exacte (MZ-4).

#### E. Oscillation \(y_i=(-1)^i a\) (\(a\neq 0\), \(n_Z\ge 2\))

| \(n_Z\) | \(\bar y\) | \(Z\) |
|---------|------------|-------|
| pair | \(0\) | \(\lvert a\rvert\) |
| impair | \(\pm a/n_Z\) | \(\lvert a\rvert\sqrt{1-1/n_Z^{2}}\) |

\(Z>0\) toujours — MZ-6. Effet pair/impair : mineur, pas un critère
de choix de \(m_Z\).

### 14D.2 Propriétés d'admissibilité

| ID | Propriété | Statut |
|----|-----------|--------|
| **MZ-1** Identifiability | \(n_Z\ge 2\) (\(m_Z\ge 3\)) | **contrainte dure** |
| **MZ-2** Locality | état local ⇒ \(m_Z\) pas « arbitrairement grand » | **qualitative** ; pas de borne chiffrée ici |
| **MZ-3** Shock detection | saut isolé ⇒ \(Z>0\) | **OK** \(\forall n_Z\ge 2\) |
| **MZ-4** Finite memory | retour exact à \(0\) après durée déterminable | **OK** (\(=n_Z\) après fin de perturbation dans \(y\)) |
| **MZ-5** No drift confusion | \(y_i=c\Rightarrow Z=0\) | **OK** |
| **MZ-6** Persistent instability | oscillation ⇒ \(Z>0\) | **OK** |
| **MZ-7** No empirical tuning | pas SPY / E01–E04 / crises / CRPS | **méthodologique** |
| **MZ-8** Interpretable memory | mémoire Disp = \(n_Z\) incréments / sessions de présence | **OK** |

### 14D.3 Niveau II — rolling \(RV\) (stride 1 = hypothèse de travail, NOT ACCEPTED)

\[
W_{RV}:=W_X,
\quad
RV_t^{2}=\frac1{W_{RV}}\sum_{j=0}^{W_{RV}-1}r_{t-j}^{2}.
\]

#### Choc synthétique dans \(r^{2}\)

Baseline \(r_u^{2}=a>0\) ; une seule date \(s\) : \(r_s^{2}=a+\delta\)
(\(\delta\neq 0\), \(a+\delta>0\)) ; retour immédiat à \(a\).

| Quantité | Comportement |
|----------|--------------|
| Présence dans \(RV\) | \(t\in\{s,\ldots,s+W_{RV}-1\}\) — **\(W_{RV}\) sessions** |
| \(RV_t^{2}\) | \(a+\delta/W_{RV}\) sur cet intervalle ; \(a\) sinon |
| \(\Delta L\) non nuls | **dipôle** : entrée \(t=s\) (signe de \(\delta\)) ; sortie \(t=s+W_{RV}\) (signe **opposé**) |
| Séparation | **\(W_{RV}\)** pas entre les deux impulsions \(y\) |
| Entre les deux | \(\Delta L=0\) ( \(L\) plat tant que le choc est entièrement dans \(RV\) ) |

Un choc unique de \(r^{2}\) **n'est pas** une seule impulsion dans
\(y\) : c'est une structure **entrée/sortie** produite par la mémoire
rolling (mémoire A).

Retour baseline complet de \(Z\) : après sortie de la dernière
signature hors de la fenêtre Disp — horizon d'ordre
\(s+W_{RV}+n_Z\).

### 14D.4 Empan causal vs mémoire effective

\[
\operatorname{span}_{\mathrm{causal}}(Z_t)
=
W_{RV}+m_Z-1
\]

(ordre \(W_{RV}+m_Z\) ; surveiller l'inclusion des bornes —
off-by-one documentaire, pas une liberté de tuning).

| Notion | |
|--------|--|
| Empan brut | \(W_{RV}+m_Z-1\) |
| Nb d'incréments \(y\) | \(n_Z=m_Z-1\) |
| Info indépendante | **≪** \(n_Z\) (overlap) |
| Persistance d'une impulsion \(y\) dans \(Z\) | \(n_Z\) dates |

**Interdit :** assimiler \(W_{RV}+m_Z\) à un effectif i.i.d.

### 14D.5 Deux mémoires

| Mémoire | Contrôle | Effet |
|---------|----------|-------|
| **A** | \(W_{RV}\) | rolling \(RV\) ; **dipôle** entrée/sortie espacé de \(W_{RV}\) |
| **B** | \(m_Z\) / \(n_Z\) | \(\mathrm{Std}_{\mathrm{pop}}\) ; dilution / rétention pendant \(n_Z\) dates |

Mémoire totale de \(Z\) = **composition** A puis B.

### 14D.6 Classes \(m_Z\) vs \(W_{RV}\) — seuil exact du dipôle

Indices des signatures : \(s\) et \(s+W_{RV}\) (écart \(W_{RV}\)).
Les deux tiennent dans une fenêtre de \(n_Z\) incréments ssi

\[
n_Z\ge W_{RV}+1
\quad\Leftrightarrow\quad
m_Z\ge W_{RV}+2.
\]

**Attention :** les classes naïves \(m_Z\lessgtr W_{RV}\) **ne**
coïncident **pas** avec ce seuil (off-by-one structurel).

| Classe | Dual-signature dans \(Z\) ? | Interprétation |
|--------|----------------------------|----------------|
| \(m_Z\le W_{RV}+1\) i.e. \(n_Z\le W_{RV}\) | **non** | au plus une signature du dipôle à la fois |
| \(m_Z=W_{RV}\) | **non** (\(n_Z=W_{RV}-1\)) | idem — **\(m_Z=W_{RV}\) n'aligne pas entrée/sortie** |
| \(m_Z=W_{RV}+2\) i.e. \(n_Z=W_{RV}+1\) | **oui**, aux extrémités quand \(t=s+W_{RV}\) | fenêtre exacte du dipôle |
| \(m_Z>W_{RV}+2\) | **oui**, avec slack | entrée et sortie simultanées + zéros entre |

**Conséquences sémantiques :**

- Sous \(m_Z\le W_{RV}+1\), \(Z\) ne « voit » jamais le dipôle complet
  d'un choc \(r^{2}\) : plutôt des fronts séparés (entrée puis, plus
  tard, sortie).
- Sous \(m_Z\ge W_{RV}+2\), \(Z\) peut classifier comme instabilité
  la **coexistence** entrée+sortie du **même** choc rolling — objet
  différent d'une instabilité de régime « purement locale » en
  \(\Delta L\).
- **Aucune classe interdite par théorème** ; la distinction change
  l'interprétation. Pas de forçage \(m_Z=W_{RV}\) (esthétique /
  symétrie) — cette égalité **ne** réalise **pas** l'alignement
  dipôle.

### 14D.7 Classification de \(m_Z\)

\[
\boxed{m_Z:\ \texttt{STRUCTURALLY CONSTRAINED}\ (B)}
\]

| Éliminé / contraint | Reste ouvert |
|---------------------|--------------|
| \(n_Z=1\) (\(m_Z=2\)) — MZ-1 | tout \(m_Z\ge 3\) |
| \(m_Z=W_{RV}\) comme « identité naturelle » — **non justifié** par le dipôle | horizon propre vs conventions explicites préenregistrées |
| localité qualitative (MZ-2) sans borne chiffrée | choix humain non empirique |

**Pas** `STRUCTURALLY DETERMINED` : pas de construction unique.
**Pas** `FREE` pur : MZ-1 et la sémantique dual-signature vs
front-unique **contrainent** la discussion.

Aucune valeur numérique.

### 14D.8 Revue adversariale

| Attaque | Évaluation |
|---------|------------|
| \(m_Z\) minimal pour « éviter un paramètre » | \(m_Z=3\) (\(n_Z=2\)) admissible MZ-1 mais proche d'un détecteur de choc / contraste — tension MZ-2 |
| \(m_Z=W_{RV}\) par symétrie | **esthétique** ; n'aligne pas le dipôle ; ne pas adopter sans justification séparée |
| Grand \(m_Z\) | détruit la localité ; dilue les impulsions (\(1/\sqrt{n_Z}\)) |
| Petit \(m_Z\) | détecteur de choc ; peu de « régime » |
| Double smoothing | mémoire A + B — **réel** ; à assumer, pas nier |
| Empan = info i.i.d. | **faux** |
| Autocorrélation rolling | **structurelle** |
| Off-by-one \(m_Z\)/\(n_Z\) / seuil dipôle | documenté §14D.0 et §14D.6 |
| Tuning futur de \(m_Z\) | interdit (MZ-7) |

### 14D.9 Verdicts

| Item | Résultat |
|------|----------|
| Convention | \(m_Z\) = # niveaux \(L\) ; \(n_Z=m_Z-1\) |
| Impulse \(y\) | \(Z=\lvert\delta\rvert\sqrt{n_Z-1}/n_Z\) ; durée \(n_Z\) |
| Step \(y\) | \(Z=\lvert c\rvert\sqrt{k(n_Z-k)}/n_Z\) ; \(Z=0\) si \(k=n_Z\) |
| Oscillation | \(Z\approx\lvert a\rvert\) ; toujours \(>0\) |
| Empan causal | \(W_{RV}+m_Z-1\) |
| Choc \(r^{2}\) | dipôle \(\Delta L\) séparé de \(W_{RV}\) |
| Dual-signature | ssi \(m_Z\ge W_{RV}+2\) |
| Classification | **`STRUCTURALLY CONSTRAINED`** |

\[
\boxed{\text{NO }m_Z\text{ VALUE SELECTED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Étape suivante :** §14E — domaine admissible + identifiabilité.

### 14D.10 Cohérence

| Contrôle | OK |
|----------|-----|
| Pas de valeur \(m_Z\)/\(W\) | oui |
| Couplage / Disp / A non rouverts | oui |
| Stride 1 non accepté | oui |
| Deux mémoires distinguées | oui |
| I02 NOT OPENED | oui |

---

## 14E. Domaine admissible de \(m_Z\) et identifiabilité structurelle

**Nature :** documentaire / mathématique. **Aucune donnée.** Aucune
valeur de \(m_Z\). I02 = `NOT OPENED`.

### 14E.1 Décision humaine — domaine admissible

**Statut :** `ACCEPTED` pour I02.

\[
\boxed{3\le m_Z\le W_{RV}+1}
\]

avec \(m_Z=\#\{L\}\), \(n_Z=m_Z-1\), \(W_{RV}:=W_X\) déjà
`ACCEPTED`.

**Classification :**

```text
STRUCTURAL ADMISSIBILITY CONSTRAINT
```

**Justification acceptée :**

| Borne | Motif |
|-------|--------|
| \(m_Z\ge 3\) | \(n_Z\ge 2\) — \(\mathrm{Std}_{\mathrm{pop}}\) sur ≥2 incréments (MZ-1) |
| \(m_Z\le W_{RV}+1\) | empêche la **dual-signature** dans une même fenêtre \(Z_t\) (seuil §14D.6 : coexistence possible si \(m_Z\ge W_{RV}+2\)) |

Interprétation : \(W_{RV}\) = mémoire A (rolling \(RV\)) ; \(m_Z\) =
mémoire B (état d'instabilité). \(Z_t\) ne doit pas agréger dans le
même état local l'entrée d'un choc dans \(RV\) **et** sa sortie
mécanique \(W_{RV}\) sessions plus tard.

**Ce qui n'est pas accepté :**

- la plage comme **grille de tuning** ;
- toute valeur particulière (\(m_Z=3\), \(W_{RV}\), \(W_{RV}+1\), …)
  sans justification structurelle **supplémentaire** ;
- \(Z_t\) complète.

### 14E.2 Identifiabilité dans \([3,\,W_{RV}+1]\)

Question : existe-t-il un principe **a priori** (sans données,
performance, calibration, esthétique, E01–E04) qui fixe une unique
\(m_Z\) dans la plage ?

#### A. Minimality — \(m_Z=3\)

Mesure une Disp sur \(n_Z=2\) incréments. Admissible MZ-1, mais
sémantiquement proche d'un **détecteur de contraste local / choc**,
pas d'un « régime » observé sur une trajectoire. **Parcimonie ≠
fidélité sémantique.** Verdict : **ne détermine pas** \(m_Z\).

#### B. Matching — \(m_Z=W_{RV}\)

Aucune raison mathématique au-delà de la **symétrie esthétique**
(§14D : n'aligne même pas le dipôle). Les rôles A/B restent
distincts. Verdict : **ne détermine pas** \(m_Z\).

#### C. Maximal local memory — \(m_Z=W_{RV}+1\)

Borne haute du domaine : maximal sans dual-signature. C'est une
**borne**, pas une propriété qui sélectionne un optimum unique
(« le plus grand permis » n'est pas un théorème). Verdict : **ne
détermine pas** \(m_Z\).

#### D. Fractional coupling — \(m_Z\) proportionnel à \(W_{RV}\)

Aucune loi d'échelle structurelle dérivée des axiomes acceptés.
Tout coefficient serait une **convention arbitraire**. Verdict :
**ne détermine pas** (et aucun coefficient proposé ici).

#### E. Fixed independent horizon

\(m_Z\) constant (indépendant de \(W_{RV}\)) dans la plage quand
\(W_{RV}\) varie : conceptuellement possible, mais **aucune**
justification supérieure a priori vs une relation à \(W_{RV}\).
Verdict : **option de gouvernance**, pas identification.

### 14E.3 Conclusion d'identifiabilité

Toutes les valeurs entières de la plage (dès que \(W_{RV}\ge 2\)
autorise un intervalle non vide) restent **compatibles** avec les
propriétés acceptées. Aucune n'est forcée.

\[
\boxed{m_Z\text{ IS NOT STRUCTURALLY IDENTIFIABLE}}
\]

Arrêt de la quête d'une « valeur naturelle ».

### 14E.4 Gouvernance scientifique (forme seulement)

| Forme | Contenu | Évaluation |
|-------|---------|------------|
| **A.** Une valeur unique préenregistrée | convention explicite | licite **si** étiquetée convention, **pas** « naturelle » |
| **B.** Petit ensemble préenregistré (sensitivity family) | plusieurs échelles | voir §14E.5 |
| **C.** Relation à \(W_{RV}\) avant données | ex. matching / fraction | **sans** loi d'échelle = déguisement de A |

**Recommandation documentaire de forme :** la situation appelle une
**sensibilité multi-échelle préenregistrée** (forme B du tableau
ci-dessus), éventuellement avec une échelle **primaire**
conventionnelle explicite — mais la primaire, si elle existe, est
une **étiquette de reporting**, pas une identification structurelle.

**Aucune** valeur ni ensemble numérique choisis ici.

### 14E.5 Robustesse §9.16 vs sensibilité multi-échelle

| | §9.16 (\(\mathcal{M}_{S3}\)) | Famille de \(m_Z\) |
|--|------------------------------|-------------------|
| Objet | même adversaire informationnel ; géométries \(d_Q\) vs \(d_\phi\) | **échelles temporelles réellement différentes** de l'instabilité |
| Désaccord | incertitude géométrique sur un même contrôle | désaccord sur « à quelle profondeur le régime est local » |
| Lecture correcte | robustesse préenregistrée du **même** estimand | **multi-scale scientific sensitivity** |
| Lecture incorrecte | — | appeler cela « robustesse » comme si \(m_Z\) étaient interchangeables |

Donc : une « \(m_Z\) sensitivity family » ≠ doctrine §9.16. Ce sont
des **questions scientifiques d'échelle**, pas des variantes
métriques d'un même \(Z\).

### 14E.6 Attaques

| Attaque | Rejet |
|---------|--------|
| \(m_Z=3\) « le plus simple » | faux argument de parcimonie / détecteur de choc |
| \(m_Z=W_{RV}\) « même échelle » | faux matching / esthétique |
| \(m_Z=W_{RV}+1\) « le plus grand permis » | borne ≠ optimum |
| Fraction arbitraire de \(W_{RV}\) | pas de loi d'échelle |
| Symétrie / parcimonie / pseudo-naturel | non structurel |
| Sélection future via CRPS / Spearman / crises | **interdit** (MZ-7) |

### 14E.7 Classification finale

\[
\boxed{\texttt{C — NOT IDENTIFIED, PRE-REGISTERED MULTI-SCALE SENSITIVITY REQUIRED}}
\]

**Justification :** le domaine \(3\le m_Z\le W_{RV}+1\) est
structurellement motivé ; **aucune** valeur unique n'en découle ;
différents \(m_Z\) sont des échelles distinctes (pas une robustesse
§9.16). La gouvernance scientifiquement appropriée est une
**sensibilité multi-échelle préenregistrée** (éventuellement avec
primaire conventionnelle explicite), **sans** inventer une valeur
naturelle et **sans** tuning empirique.

*(La catégorie B — horizon unique préenregistré — reste une option
humaine de reporting, mais uniquement comme **convention assumée**,
pas comme issue de ce mandat d'identifiabilité.)*

\[
\boxed{\text{NO }m_Z\text{ VALUE SELECTED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

### 14E.8 Cohérence

| Contrôle | OK |
|----------|-----|
| Domaine \(3\le m_Z\le W_{RV}+1\) ACCEPTED | oui |
| Aucune valeur / grille numérique | oui |
| Pas de confusion avec §9.16 | oui |
| I02 NOT OPENED | oui |

---

## 14F. Gouvernance multi-échelle de \(m_Z\)

**Nature :** mathématique / méthodologique / documentaire. **Aucune
donnée.** Aucune valeur / fraction / grille de \(m_Z\). Bases §14E
**non rouvertes.** I02 = `NOT OPENED`.

**Objectif :** comment construire une petite famille préenregistrée
\(\mathcal{M}_Z=\{m_Z^{(1)},\ldots,m_Z^{(q)}\}\) **sans** tuning,
optimisation, sélection post-hoc, CRPS/Spearman/SPY/E01–E04, ni
« best \(m_Z\) ».

### 14F.0 Distinguer POLICY FREEZE et NUMERICAL FREEZE

| Couche | Contenu | Figement |
|--------|---------|----------|
| **POLICY FREEZE** | règles de construction, taxonomie MS, no-primary, multiplicité, réplication | **maintenant** possible |
| **NUMERICAL SCALE FREEZE** | valeurs concrètes de \(\mathcal{M}_Z\) | **après** \(W_X\) (car \(W_{RV}:=W_X\) borne le domaine) |

### 14F.1 Couverture d'échelle — trois philosophies

#### A. Absolute spacing

Valeurs absolues prédéfinies dans \([3,W_{RV}+1]\).

**Verdict :** `WEAK` / non retenu comme politique. Dépend de la
valeur future de \(W_{RV}\) ; mauvaise transférabilité si \(W_X\)
change ; « evenly spaced » = fausse neutralité.

#### B. Relative-to-\(W_{RV}\)

Positions relatives dans \([3,W_{RV}+1]\) (sans fractions figées
ici).

**Verdict :** `PROMISING` pour la **politique**. Invariance de forme
quand \(W_{RV}\) change ; attention arrondis / doublons si \(W_{RV}\)
petit (domaine étroit) ; interprétable comme « short / mid / long
dans le domaine admissible ».

#### C. Semantic scale classes — SHORT / INTERMEDIATE / LONG-LOCAL

LONG-LOCAL reste \(\le W_{RV}+1\).

**Verdict :** `PROMISING` comme **vocabulaire**, `WEAK` s'il cache
des fractions arbitraires non déclarées. Admissible seulement si les
classes sont **définies comme** des positions relatives explicites
dans le domaine (cas B) — sinon short/medium/long = catégories
ornementales.

**Synthèse couverture :** politique = **relative-to-\(W_{RV}\)**
(éventuellement labellisée sémantiquement) ; pas absolute spacing.

### 14F.2 Combien d'échelles \(q\) ?

| Trop peu | Trop |
|----------|------|
| fausse robustesse / mauvaise info d'échelle | multiplicité, flexibilité analytique, **grid-search déguisé** |

Aucune \(q\) structurellement identifiable. Exigence qualitative :
**petit** ensemble représentatif des extrémités du domaine et d'au
moins une position intérieure — **sans** chiffrer \(q\) ici.

**Verdict \(q\) :** `NOT STRUCTURALLY IDENTIFIABLE` ; borne
supérieure conceptuelle « assez petit pour ne pas être une grille ».

### 14F.3 PRIMARY vs no-primary — BLOCKING

| Architecture | Contenu | Cohérence avec « not identifiable » |
|--------------|---------|-------------------------------------|
| **A** PRIMARY + sensitivity | une échelle « principale » + autres | **incohérente** si PRIMARY prétend être naturelle / meilleure ; **tolérable** seulement si PRIMARY = **étiquette de reporting conventionnelle** préenregistrée, jamais « parce que meilleure » |
| **B** co-préenregistrées, **aucune** PRIMARY | toutes les \(m_Z\in\mathcal{M}_Z\) de même statut | **cohérente** avec non-identifiabilité |

**Verdict :** architecture **B** (no-primary / co-primary scales)
retenue comme gouvernance par défaut. Architecture A **interdite**
sauf convention de reporting **explicite** et non performative.

**Interdit absolu :** PRIMARY parce qu'elle a le mieux performé.

### 14F.4 Taxonomie cross-scale (avant expérimentation)

« Même conclusion scientifique » ≠ valeurs numériques identiques.
Indépendant du score final (CRPS / Spearman **non** acceptés) :
porte sur le **verdict** préenregistré concernant \(X\) vs \(S\)
sous \(Z(\cdot)\), quelle que soit la mesure ultérieure.

| Code | Cas | Signification | Interdit |
|------|-----|---------------|----------|
| **MS-1** | Cross-scale consistent | même conclusion sur **toutes** les \(m_Z\in\mathcal{M}_Z\) | — |
| **MS-2** | Scale-localized | effet seulement sur une **partie** préidentifiée des échelles | **ne pas** promouvoir cette partie en PRIMARY ; ≠ autorisation de retune |
| **MS-3** | Cross-scale contradictory | conclusions **opposées** selon l'échelle | verdict d'ensemble `INCONCLUSIVE` / non-résistance selon protocole futur — pas de vote opportuniste |
| **MS-4** | Cross-scale inconclusive | information insuffisante / instable | ne pas « sauver » via une échelle |

### 14F.5 Scale-localized ≠ échec ; ≠ retune

\[
\text{observation of scale localization}
\;\neq\;
\text{authorization to retune }m_Z
\]

La localisation d'échelle peut être une **propriété scientifique**
du phénomène (effet à courte / longue mémoire locale dans le
domaine). Elle **n'autorise pas** de sélectionner l'échelle
favorable et de continuer comme si elle était primaire.

### 14F.6 Multiplicité — exigences (pas de correction choisie)

La future inférence **devra** respecter (sans méthode figée ici) :

- pas de minimum \(p\)-value / maximum effect size sur \(\mathcal{M}_Z\) ;
- pas de majority vote opportuniste ;
- pas de « best \(m_Z\) » ;
- dépendance forte entre échelles **reconnue** (pas traiter comme
  tests indépendants naïfs) ;
- toute correction / agrégation = **préenregistrée**, pas post-hoc.

### 14F.7 Réplication

\[
\text{discovered scale dependence}
\;\longrightarrow\;
\text{new hypothesis / independent replication}
\]

Une échelle devenue « intéressante » **après** observation ne se
confirme **pas** sur les mêmes données en la déclarant primaire.

### 14F.8 Revue adversariale

| Attaque | Rejet |
|---------|--------|
| evenly / log spaced = neutralité / naturalité | faux |
| short/medium/long ornemental | fractions cachées |
| \(q\) élevé | grid search |
| \(q=1\) déguisé en multi-scale | fausse robustesse |
| PRIMARY sans fondement / post-hoc | interdit |
| majority vote / best \(m_Z\) / min-\(p\) / max-effect | interdit |
| sélection d'échelle localisée | interdit (§14F.5–7) |
| changer \(\mathcal{M}_Z\) après résultat | nouvelle investigation |

### 14F.9 Verdicts

| Question | Verdict |
|----------|---------|
| Absolute spacing | `WEAK` |
| Relative-to-\(W_{RV}\) | `PROMISING` (politique) |
| Semantic classes | `PROMISING` si = labels de B ; sinon `WEAK` |
| PRIMARY + sensitivity | `WEAK` par défaut ; convention reporting seulement |
| No-primary / co-registered | **`RETAINED`** |
| Scale-localized | propriété possible ; ≠ retune |
| Multiplicité | exigences §14F.6 ; pas de correction choisie |
| \(q\) | not identifiable ; « petit » qualitative |

### 14F.10 Classification — \(W_X\) et figement

\[
\boxed{\texttt{B — SPECIFIABLE AFTER }W_X\text{ IS FIXED}}
\]

**Précision :**

- **POLICY FREEZE** (relative coverage, no-primary, taxonomie MS-1…4,
  règles multiplicité / réplication) : **SPECIFIABLE NOW** ;
- **NUMERICAL \(\mathcal{M}_Z\)** : **SPECIFIABLE AFTER \(W_X\)**
  (domaine \([3,W_X+1]\) ; positions relatives → entiers après
  arrondi / dédoublonnage).

**Implication pré-cadrage :** arrêter de travailler les **valeurs**
de \(m_Z\) ; passer à la décision sur \(W_X\) (et stride / reste de
\(Z_t\)). La politique multi-échelle reste en vigueur comme
contrainte méthodologique.

\[
\boxed{\text{NO }m_Z\text{ VALUE SELECTED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

### 14F.11 Cohérence

| Contrôle | OK |
|----------|-----|
| §14E non rouvert | oui |
| Pas de fraction / grille / valeur | oui |
| ≠ §9.16 | oui |
| POLICY vs NUMERICAL distingués | oui |
| I02 NOT OPENED | oui |

---

## 14G. Identifiabilité et héritage de \(W_X\)

**Nature :** mathématique / méthodologique / documentaire. **Aucune
donnée.** Aucune valeur de \(W_X\) acceptée. \(m_Z\) POLICY FREEZE
(§14F) ; NUMERICAL \(\mathcal{M}_Z\) attend \(W_X\). I02 =
`NOT OPENED`.

**Objectif :** A hériter d'I01 / B redéfinir / C non identifiable +
gouvernance — **sans** choisir un chiffre.

**Fait historique (pas une acceptation) :** I01 utilisait \(W=20\),
préspécifié avant E01–E04. I02 est une **nouvelle** investigation
**générée** par I01 ; \(W_{RV}:=W_X\) propage désormais \(W_X\) vers
\(RV\), \(\Delta L\), domaine \(m_Z\), \(\mathcal{M}_Z\) numérique.

### 14G.0 Rôles de \(W_X\) dans I02

| # | Conséquence |
|---|-------------|
| 1 | dimension de \(X_t\) |
| 2 | quantité d'histoire représentée |
| 3 | géométrie kNN / curse of dimensionality |
| 4 | pool de candidats historiques (taille relative) |
| 5 | \(W_{RV}:=W_X\) |
| 6 | lissage du niveau \(RV\) |
| 7 | structure mécanique de \(\Delta L\) (rotation / dipôle) |
| 8 | borne \(m_Z\le W_X+1\) |
| 9 | matérialisation numérique de \(\mathcal{M}_Z\) |
| 10 | empan causal de \(Z\) (\(\approx W_X+m_Z\)) |
| 11 | comparabilité \(X\) vs \(S_1/S_2/S_3\) (même support nominal) |

**Effet net sur l'héritage :** plus **lourd** qu'en I01 — hériter
propage une convention dans toute l'architecture d'état ; **mais**
changer \(W_X\) en même temps que question / adversaires / score
casse l'attribution. Les deux tensions coexistent.

### 14G.1 Arguments pour héritage (adversariaux)

| ID | Argument | Évaluation |
|----|----------|------------|
| **H1** Anti-retuning | ne pas retoucher \(W\) après E01–E04 | **fort** si on hérite le choix *préenregistré* I01, pas s'il est « retenu parce que E04 a marché » |
| **H2** Continuité de représentation | phénomène découvert sous \(X\) de longueur 20 | **fort** pour une investigation de *disséction* du même objet générateur |
| **H3** Attribution causale | différences I01↔I02 attribuables à la question, pas à une nouvelle \(X\) | **fort** méthodologiquement |
| **H4** Simplicité de gouvernance | pas de nouvelle liberté | **défendable** ; insuffisant seul |

### 14G.2 Arguments contre héritage (adversariaux)

| ID | Argument | Évaluation |
|----|----------|------------|
| **C1** Nouvel objet scientifique | I02 ≠ I01 | **vrai** pour la *cible* ; n'implique pas automatiquement un nouveau \(W\) |
| **C2** Propagation architecturale | \(W\) irrigue \(W_{RV}\), \(m_Z\), \(\mathcal{M}_Z\) | **vrai et sérieux** — coût de l'héritage élevé ; motive une revue, pas un rejet automatique |
| **C3** Géométrie haute dimension | kNN / tâche probabiliste | **ouvert** ; pas de forçage a priori vers une autre valeur sans critère |
| **C4** Accident historique | 20 raisonnable pour I01 ≠ structurel pour I02 | **vrai** que 20 n'est pas structurel ; n'implique pas qu'un autre chiffre le soit |

### 14G.3 Contamination / snooping — BLOCKING

| Option | Nature de la contamination |
|--------|----------------------------|
| **Hériter \(W=20\)** | le générateur I01 (préenregistré) est **exposé** aux résultats E01–E04 ; l'héritage pour *disséquer* le même phénomène est une contamination de **continuité** (même objet), pas une optimisation post-hoc de \(W\) **si** on ne le justifie pas par la performance E04 |
| **Choisir un nouveau \(W_X\) maintenant** | sans critère structurel = liberté de recherche **après** avoir vu E04 — contamination de **sélection** plus dangereuse (shopping d'échelle) |

**Verdict contamination :** hériter le choix **préenregistré** du
générateur est **différemment** contaminé (continuité d'objet), en
général **moins** dangereux que sélectionner une nouvelle valeur
aujourd'hui **sans** axiome nouveau. Condition : formuler l'héritage
comme *inherited fixed design constraint*, **pas** comme « 20 a
marché en E04 ».

### 14G.4 Alternatives à une valeur unique

| Option | Évaluation |
|--------|------------|
| **A** Hériter single \(W_X\) d'I01 | parcimonieux ; attribution propre ; propage l'architecture |
| **B** Nouveau single préenregistré | exige un critère a priori **non** empirique — actuellement **absent** |
| **C** Multi-\(W_X\) sensitivity | chaque \(W_X\) ⇒ \(W_{RV}\), domaine \(m_Z\), \(\mathcal{M}_Z\), dim \(X\) — **explosion combinatoire** avec la multi-échelle \(m_Z\) déjà requise |
| **D** Famille représentation multi-\(W_X\) | pire que C pour I02 au stade actuel |

**Risque combinatoire :** multi-\(W_X\) × multi-\(m_Z\) ≈ grille
2D déguisée. **Rejet** de C/D comme politique par défaut pour I02
pré-cadrage.

### 14G.5 Principle of minimal change

> Parce qu'I02 est générée pour expliquer / raffiner un phénomène
> observé sous la représentation \(X\) d'I01, préserver \(W_X\)
> d'I01 **sauf** si la nouvelle hypothèse **exige logiquement** de
> le changer.

**Classification du principe :** `DEFENSIBLE`.

Pas `STRONG` (la propagation \(W_{RV}\)/\(m_Z\) affaiblit
l'automaticité). Pas `REJECT` (attribution scientifique réelle).

La nouvelle hypothèse (état \(Z\), adversaires \(S\), score candidat)
**n'exige pas logiquement** un autre \(W_X\) : elle exige un état et
des contrôles, construits **sur** le même support de représentation
si l'on veut isoler leur contribution.

### 14G.6 Contre-factual

> Si I01 avait utilisé un autre \(W\) **préenregistré** et produit
> la même découverte qualitative E04, aurions-nous une raison
> principée de changer ce \(W\) avant I02 ?

**Réponse :** non — sauf exigence logique nouvelle. Donc toute
envie de « corriger 20 » *parce qu'on a vu E04* est un signal de
justification **post-hoc**. Symétriquement, garder 20 *parce que*
E04 est favorable serait aussi contaminé — d'où la formulation
**design constraint héritée**, pas performance.

### 14G.7 Justifications interdites

CRPS / Spearman / \(D^{\mathrm{CRPS}}\) ; séparation stress ;
2008/2009/2020 ; tertile E04 ; trading ; « un mois » seul ;
littérature cherchée après coup pour justifier 20.

### 14G.8 Identifiabilité

\[
W_X\text{ IS NOT STRUCTURALLY IDENTIFIABLE}
\]

Aucune valeur unique ne découle des axiomes I02 seuls.

### 14G.9 Classification

\[
\boxed{\texttt{B — NOT STRUCTURALLY IDENTIFIED, BUT I01 INHERITANCE IS METHODOLOGICALLY PREFERRED}}
\]

**Statut exact recommandé (pas encore décision d'acceptation de
valeur) :**

```text
inherited fixed design constraint (candidate)
```

— héritage du \(W\) **préenregistré** d'I01 comme contrainte de
continuité expérimentale / anti-retuning / attribution, **sous réserve
d'acceptation humaine formelle**.

**Cette revue (§14G) n'acceptait pas \(W_X=20\).** Acceptation
formelle : §14G.14.

### 14G.10 Conséquences conditionnelles (devenues déterministes §14G.14)

| Objet | Conséquence |
|-------|-------------|
| \(W_{RV}\) | \(:=W_X\) hérité |
| Domaine \(m_Z\) | \([3,W_X+1]\) |
| \(\mathcal{M}_Z\) numérique | matérialisable (politique §14F) — **pas** dans §14G |
| Comparateurs \(S\) | même \(W_{RV}\) |
| Sensibilité | **pas** multi-\(W_X\) par défaut ; multi-\(m_Z\) seulement |

Sensibilité ultérieure sur \(W_X\) = **nouvelle investigation** /
réplication, pas un amendement silencieux.

### 14G.11 Si héritage rejeté (historique)

Procédure documentée avant acceptation §14G.14 ; **non applicable**
après acceptation.

### 14G.12 Verdicts synthétiques (revue)

| Item | Verdict |
|------|---------|
| Classification revue | **`B`** |
| Valeur dans la revue | **aucune acceptée** |

**Décision humaine suivante :** §14G.14.

### 14G.13 Cohérence (revue)

| Contrôle | OK |
|----------|-----|
| Pas d'acceptation automatique de 20 dans la revue | oui |
| Multi-\(W_X\) non promu | oui |
| I02 NOT OPENED | oui |

### 14G.14 Décision humaine — \(W_X=20\) hérité

**Statut :** `ACCEPTED` pour I02.

\[
\boxed{W_X=20}
\quad
\boxed{\texttt{INHERITED FIXED DESIGN CONSTRAINT}}
\]

**Justification acceptée :** I02 disséque un phénomène découvert avec
la représentation I01 de longueur \(W=20\). Minimal change /
anti-retuning / attribution — **pas** optimalité structurelle,
empirique, universelle, ni « 20 ≈ un mois ».

**Conséquences déterministes (pas de secondes décisions) :**

| Objet | Valeur / statut |
|-------|-----------------|
| \(W_{RV}\) | \(=20\) — `DERIVED FROM ACCEPTED COUPLING` (\(W_{RV}:=W_X\)) |
| Domaine \(m_Z\) | \(\boxed{3\le m_Z\le 21}\) — mécanique ; **pas** une grille de tuning |
| \(\mathcal{M}_Z\) numérique | **non** matérialisée ici ; prochaine étape autorisée (§14F) |
| Politique §14F | relative-to-\(W_{RV}\), no-primary, MS-1…4 — **inchangée** |

**Anti-retuning :** un résultat ultérieur défavorable sous \(W_X=20\)
**n'autorise pas** d'essayer un autre \(W_X\) dans I02. Changement
de \(W_X\) après observation ⇒ nouvelle hypothèse / investigation /
réplication.

\[
\boxed{W_X=W_{RV}=20\ \texttt{ACCEPTED / DERIVED}}
\quad
\boxed{3\le m_Z\le 21\text{ (no }m_Z\text{ value selected)}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Prochaine étape autorisée :** matérialiser \(\mathcal{M}_Z\) sous
§14F dans \([3,21]\) — **hors** ce mandat.

### 14G.15 Cohérence (post-acceptation)

| Contrôle | OK |
|----------|-----|
| \(W_X=20\) ACCEPTED as inherited constraint | oui |
| \(W_{RV}=20\) derived, not independent | oui |
| Domaine \(m_Z\) [3,21] ; no \(m_Z\) value | oui |
| Pas de \(\mathcal{M}_Z\) numérique ici | oui |
| I02 NOT OPENED | oui |

---

## 14H. Famille numérique multi-échelle \(\mathcal{M}_Z\)

**Nature :** mathématique / documentaire. **Aucune donnée.**
Prérequis : \(W_X=W_{RV}=20\), domaine \([3,21]\), politique §14F.
I02 = `NOT OPENED`.

### 14H.0 Objectif et contraintes

Matérialiser une **petite** famille préenregistrée

\[
\mathcal{M}_Z=\{m_Z^{(1)},\ldots,m_Z^{(q)}\}
\subset\{3,4,\ldots,21\}
\]

**CO-PRE-REGISTERED**, **NO PRIMARY**. Pas une grille, pas de
sélection post-run, pas de « best \(m_Z\) ».

### 14H.1 \(q\)

| \(q\) | Évaluation |
|-------|------------|
| 2 | bornes seules — trop peu d'info d'échelle ; fausse robustesse |
| **3** | couverture minimale SHORT / INTERMEDIATE / LONG-LOCAL |
| \(>3\) | risque grid-search ; multiplicité sans gain d'identifiabilité |

**Verdict :** \(q=3\) retenu comme couverture minimale de gouvernance.

### 14H.2 Constructions candidates (a priori)

Domaine admissible \(D=[L,U]\) avec \(L=3\), \(U=W_{RV}+1\).

| ID | Règle | Pour \(W_{RV}=20\) |
|----|-------|---------------------|
| **A** Linéaire dans \(D\) | \(\{L,\;\mathrm{mid}(L,U),\;U\}\) | \(\{3,12,21\}\) |
| **B** Relative / \(W_{RV}\) | ex. \(\{L,\;W_{RV}/2,\;U\}\) | \(\{3,10,21\}\) |
| **C** Bornes + centre « matching » | \(\{L,\;W_{RV},\;U\}\) | \(\{3,20,21\}\) |

**Adversarial :**

| Construction | Objection |
|--------------|-----------|
| **B** (\(W_{RV}/2\)) | centre collé à l'horizon d'estimation — préférence cachée pour l'échelle \(W_{RV}\) |
| **C** (\(W_{RV}\)) | matching esthétique déjà rejeté comme identification (§14E) ; LONG et mid presque collés (20≈21) — **pas** trois mémoires distinctes |
| **A** (midpoint de \(D\)) | voisins 11/13 ? le midpoint est l'unique centre affine du domaine admissible, sans référence à \(W_{RV}\) comme valeur préférée |

**Verdict construction :** **A** retenue.

### 14H.3 Bornes dans \(\mathcal{M}_Z\)

| Borne | Rôle |
|-------|------|
| \(m_Z=3\) | SHORT extrême ; proche détecteur minimal — **informatif** pour MS-2 (localisation courte) |
| \(m_Z=21\) | LONG-LOCAL maximal avant dual-signature — **informatif** pour MS-2 (localisation longue) |

**Verdict :** inclusion des **deux** bornes **retenue** (cas limites
scientifiquement utiles, pas de tuning).

### 14H.4 Intermediate

Centre affine du domaine :

\[
m_{\mathrm{mid}}
=
\operatorname{round}_{\ast}\!\left(\frac{L+U}{2}\right)
=
\operatorname{round}_{\ast}\!\left(\frac{W_{RV}+4}{2}\right)
\]

Pour \(W_{RV}=20\) : \((20+4)/2=12\) exact.

Centre géométrique \(\sqrt{L\cdot U}\) : pour \((3,21)\) ≈ 7,94 → 8 ;
moins naturel pour une mémoire **additive** d'incréments. Non retenu.

### 14H.5 Règle d'arrondi (déterministe, future-proof)

Pour tout \(W_{RV}\ge 2\) autorisant un domaine non dégénéré :

1. \(m_{\mathrm{short}}:=3\) (si \(3\le W_{RV}+1\) ; sinon domaine
   dégénéré — hors I02 actuel) ;
2. \(m_{\mathrm{long}}:=W_{RV}+1\) ;
3. \(m_{\mathrm{mid}}:=\operatorname{round}_{\ast}((3+W_{RV}+1)/2)\)
   où \(\operatorname{round}_{\ast}\) = arrondi au plus proche entier ;
   en cas de **tie** (.5) : arrondir **vers le haut** (away from
   \(-\infty\), i.e. \(\lceil x\rceil\) sur les demi-entiers positifs) ;
4. former l'ensemble \(\{m_{\mathrm{short}},m_{\mathrm{mid}},m_{\mathrm{long}}\}\) ;
5. **dédoublonnage** : si collision après arrondi, supprimer les
   doublons et conserver l'ordre croissant ; si \(\lvert\mathcal{M}_Z\rvert<3\)
   (domaine trop étroit), la famille se réduit mécaniquement — documenter
   à l'ouverture d'une investigation avec autre \(W_X\) ;
6. **ordre** : strictement croissant après dédoublonnage.

### 14H.6 Famille figée pour I02

\[
\boxed{\mathcal{M}_Z=\{3,\,12,\,21\}}
\]

| Label | \(m_Z\) | \(n_Z=m_Z-1\) |
|-------|---------|---------------|
| SHORT | 3 | 2 |
| INTERMEDIATE | 12 | 11 |
| LONG-LOCAL | 21 | 20 |

**Statut :** `ACCEPTED` — **CO-PRE-REGISTERED**, **NO PRIMARY**.

Mémoires distinctes : 2 / 11 / 20 incréments — espacement clair,
pas de cluster près de \(W_{RV}\).

### 14H.7 Taxonomie MS (inchangée)

| Code | Cas |
|------|-----|
| MS-1 | Cross-scale consistent |
| MS-2 | Scale-localized — **≠** retune / PRIMARY |
| MS-3 | Cross-scale contradictory |
| MS-4 | Cross-scale inconclusive |

### 14H.8 Attaques

| Attaque | Réponse |
|---------|---------|
| Pourquoi pas 11/13 ? | mid = unique centre affine de \([3,21]\) |
| Grid search ? | \(q=3\) fixe, préenregistré, no selection |
| Préférence \(W_{RV}\) ? | mid ≠ 20 ; construction A évite B/C |
| \(m_Z=3\) trop local ? | inclus comme SHORT extrême pour MS-2 |
| Sur-représentation ? | une échelle par régime de longueur |

### 14H.9 Horizons — clôture pré-cadrage

| Objet | Statut |
|-------|--------|
| \(W_X\) | \(20\) ACCEPTED |
| \(W_{RV}\) | \(20\) DERIVED |
| Domaine \(m_Z\) | \([3,21]\) |
| \(\mathcal{M}_Z\) | \(\{3,12,21\}\) ACCEPTED |

**Prochain bloc pré-cadrage :** objet prédictif / évaluation
(\(V_{t,h}\), \(h\), CRPS candidat) — pas de retouche d'horizons
sauf contradiction mathématique.

\[
\boxed{\text{NO DATA USED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

### 14H.10 Cohérence

| Contrôle | OK |
|----------|-----|
| §14F / \(W_X\) non rouverts | oui |
| No-primary ; pas de sélection post-hoc | oui |
| Règle relative + arrondi déterministe | oui |
| I02 NOT OPENED | oui |

---

## 14I. Future volatility target \(V_{t,h}\) and horizon \(h\)

**Nature :** mathématique / méthodologique / documentaire. **Aucune
donnée.** Horizons \(W_X/W_{RV}/\mathcal{M}_Z\) **non rouverts.**
CRPS **non** accepté. \(Z_t\) **non** acceptée. I02 = `NOT OPENED`.

**Ordre de décision :** quoi prédire → sur quelle durée → comment
juger. Ce mandat : les deux premiers ; **pas** le score.

### 14I.1 Question scientifique

I02 teste si \(X_t\) porte de l'information sur la **distribution
future de volatilité / énergie réalisée** non expliquée par
\(S_1/S_2/S_3\).

La cible **n'est pas** : direction, rendement cumulé, drawdown, label
de stress, régime futur post-hoc.

### 14I.2 Formule candidate — propriétés

\[
V_{t,h}
=
\sqrt{\frac1h\sum_{j=1}^{h}r_{t+j}^{2}}
\]

| Propriété | Statut |
|-----------|--------|
| Causalité de l'*évaluation* | \(V_{t,h}\) utilise \(r_{t+1:t+h}\) — **futur** ; les prévisions \(\widehat F\) ne l'utilisent qu'à l'évaluation |
| Positivité | \(V_{t,h}\ge 0\) |
| Interprétation | RMS des rendements futurs (énergie moyenne par séance, racine) |
| Grands \(\lvert r\rvert\) | sensibilité **quadratique** puis racine — queues amplifiées vs \(\mathrm{mean}\lvert r\rvert\) |
| Moyenne soustraite | **non** — ce n'est pas un écart-type d'échantillon |
| \(h\) | échelle temporelle de l'objet ; change la cible |
| Comparabilité | à \(h\) fixé, comparable entre dates |

**Terminologie :** « future realized volatility » est **acceptable**
au sens finance (RV close-to-close undemeaned). Plus précis :

```text
future realized RMS volatility (undemeaned)
```

Réserver « sample standard deviation » à la variante démeanée.

Sans le facteur \(1/h\) : si \(h\) fixe, monotone en
\(\sqrt{\sum r^{2}}\) — même rangs de réalisations ; l'échelle
change. La forme RMS par séance est retenue pour la lecture.

### 14I.3 Alternatives minimales

| ID | Objet | Verdict |
|----|-------|---------|
| **A** \(\sqrt{\mathrm{mean}(r^{2})}\) | RMS / RV classique | **`RETAINED`** |
| **B** \(\mathrm{mean}(\lvert r\rvert)\) | amplitude \(L_1\) | `WEAK` pour I02 — moins aligné énergie/\(RV\) des adversaires |
| **C** \(\mathrm{mean}(r^{2})\) | realized variance | voir §14I.4 — informationnellement lié ; échelle différente pour scoring |
| **D** \(\mathrm{std}(r_{t+1:t+h})\) | écart-type (démeané) | `WEAK` — soustrait un drift futur ; mélange niveau et forme |

### 14I.4 Variance vs volatility

\[
C=\mathrm{mean}(r^{2}),
\qquad
V=\sqrt{C}
\]

**Informational equivalence (pointwise monotone) :** \(V=\sqrt{C}\) est
strictement croissante en \(C\) sur \(C\ge 0\) ⇒ même **ordre** des
réalisations ; même partition qualitative « plus grand / plus petit ».

**Scoring equivalence :** **non.** Un score probabiliste (ex. CRPS)
dépend de l'échelle de \(y\). Prévoir la loi de \(C\) ≠ prévoir la
loi de \(\sqrt{C}\) (transformation non linéaire des lois).

**Décision :** retenir \(V=\sqrt{\mathrm{mean}(r^{2})}\) comme **échelle
de volatilité** (cohérente avec \(RV\) passé). Ne **pas** utiliser
cet argument pour accepter CRPS.

### 14I.5 Décision — définition de \(V_{t,h}\)

\[
\boxed{
V_{t,h}=\sqrt{\frac1h\sum_{j=1}^{h}r_{t+j}^{2}}
\quad\texttt{ACCEPTED}
}
\]

Nom : future realized RMS volatility (undemeaned). \(h\) reste OPEN.

### 14I.6 Horizon \(h\) — héritage vs redéfinition

I01 : \(h=10\) (préspécifié avant E01–E04). \(W_X=20\) déjà hérité.

| Pour héritage | Contre |
|---------------|--------|
| Continuité / minimal change / anti-retuning | \(h\) **définit** l'objet prédit — plus « objet scientifique » que \(W_X\) seul |
| Phénomène générateur observé à \(h=10\) | Nouvelle question distributionnelle peut vouloir un autre horizon |
| Attribution I01↔I02 | Hériter propage un horizon générateur dans la cible |

**Contamination :** hériter le \(h\) **préenregistré** du générateur <
choisir un nouveau \(h\) post-E04 sans axiome. Même logique que
§14G, avec en plus : \(h\) est la durée de **l'observable**.

### 14I.7 Identifiabilité de \(h\)

\[
h\text{ IS NOT STRUCTURALLY IDENTIFIABLE}
\]

\[
\boxed{\texttt{B — NOT STRUCTURALLY IDENTIFIED, BUT I01 INHERITANCE IS METHODOLOGICALLY PREFERRED}}
\]

Candidat : `inherited fixed design constraint (candidate)` pour
\(h=10\). **Cette revue (§14I.7) n'acceptait pas \(h=10\).**
Acceptation formelle : §14I.14.

### 14I.8 Multi-\(h\)

| Risque | |
|--------|--|
| Multiplicité × \(\mathcal{M}_Z\) × \(S_i\) | explosion |
| Sélection post-hoc du « meilleur » \(h\) | snooping |
| Plusieurs objets scientifiques distincts | I02 s'égare |

**Verdict :** multi-\(h\) **rejeté** pour I02 pré-cadrage ;
éventuelle investigation ultérieure / réplication.

### 14I.9 Overlap temporel

Pour \(h=10\), \(V_{t,10}\) et \(V_{t+1,10}\) partagent jusqu'à
**9** rendements futurs ⇒ dépendance sérielle forte des targets et
des scores.

| Effet | Remet en cause… |
|-------|-----------------|
| Effective sample size ↓ | **inférence** / bootstrap futur |
| Stride 1 | interaction des scores — **OPEN** |
| Définition de \(V\) | **non** — overlap ≠ mauvaise cible |

### 14I.10 Hard availability

\[
s+h\le t
\qquad\xrightarrow{h=10}\qquad
s+10\le t
\]

pour tout voisin historique de la query \(t\) : **nécessaire et
suffisant** comme garde anti-fuite pour \(V_{s,10}\) dans
\(\widehat F(\cdot\mid t)\). Autres fuites : futures features dans
\(X/S/Z\), fuite via \(C_t\)/labels — hors formule \(V\) ; discipline
AF-08 inchangée.

### 14I.11 Attaques

| Attaque | Rejet |
|---------|--------|
| \(h=10\) par inertie | non — seulement design héritage |
| Nouveau \(h\) parce qu'I02 est nouveau | non sans axiome |
| « deux semaines » seul | interdit |
| Multi-\(h\) grid | rejeté §14I.8 |
| Target choisie pour le score | interdit (ordre target→score) |
| Confusion RMS / std / variance | documentée §14I.2–4 |
| Influence E01–E04 sur la formule | formule a priori ; héritage \(h\) = anti-retuning |

### 14I.12 Verdicts

| Item | Verdict |
|------|---------|
| Target A | **`ACCEPTED`** |
| B / D | `WEAK` |
| C (variance) | lié info ; non retenu comme échelle primaire |
| Terminologie | future realized RMS volatility (undemeaned) |
| Info equiv. \(C\) vs \(\sqrt{C}\) | oui (ordre) ; scoring **non** |
| \(h\) classification | **`B`** preferred inheritance |
| \(h=10\) | **non accepté** dans la revue §14I ; accepté §14I.14 |
| Multi-\(h\) | rejeté pour I02 |
| Overlap | inférence, pas définition |
| Hard availability | \(s+10\le t\) OK |

\[
\boxed{\text{NO DATA USED}}
\quad
\boxed{\text{NO CRPS ACCEPTED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Décision humaine \(h\) :** §14I.14.

### 14I.13 Cohérence (revue)

| Contrôle | OK |
|----------|-----|
| Horizons non rouverts | oui |
| Score non choisi | oui |
| \(h\) non accepté implicitement dans la revue | oui |
| I02 NOT OPENED | oui |

### 14I.14 Décision humaine — \(h=10\) hérité

**Statut :** `ACCEPTED` pour I02.

\[
\boxed{h=10}
\quad
\boxed{\texttt{INHERITED FIXED FORECAST HORIZON}}
\]

**Justification acceptée :** continuité expérimentale avec I01 ;
minimal change ; anti-retuning ; I02 caractérise un phénomène
découvert sous \(h=10\) ; aucun argument structurel pour un
changement ; multi-\(h\) rejeté (§14I.8).

**N'est pas :** optimal ; structurellement identifié ; universel ;
« 10 ≈ deux semaines » ; sélection empirique.

**Target finale :**

\[
\boxed{
V_{t,10}
=
\sqrt{\frac1{10}\sum_{j=1}^{10}r_{t+j}^{2}}
}
\]

Terminologie : *future realized RMS volatility (undemeaned)*.

**Hard availability :** \(s+10\le t\).

**Overlap :** sous stride 1, targets successives partagent jusqu'à
9 rendements futurs — **n'invalide pas** la définition ; impose que
la future inférence traite la dépendance sérielle (stride /
bootstrap **OPEN**).

**Anti-retuning :** un résultat défavorable sous \(h=10\) **n'autorise
pas** de relancer I02 avec un autre \(h\). Autre horizon ⇒ nouvelle
investigation / réplication.

\[
\boxed{h=10\ \texttt{ACCEPTED}}
\quad
\boxed{V_{t,10}\ \text{fully specified}}
\quad
\boxed{\text{NO CRPS ACCEPTED}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

**Prochaine étape :** forecast object / CRPS — §14J.

### 14I.15 Cohérence (post-acceptation)

| Contrôle | OK |
|----------|-----|
| \(h=10\) ACCEPTED as inherited forecast horizon | oui |
| \(V_{t,10}\) fully specified | oui |
| Multi-\(h\) non rouvert | oui |
| Pas de CRPS / \(Z_t\) acceptés | oui *(à la date de §14I ; CRPS mis à jour §14J)* |
| I02 NOT OPENED | oui |

---

## 14J. Forecast object probabiliste et scoring

> **Nature :** mathématique / méthodologique / documentaire.
> **NO DATA. NO EXPERIMENT. NO CODE.**
> \(k=\texttt{OPEN}\). stride=\texttt{OPEN}. \(\texttt{NO }Z_t\texttt{ ACCEPTED}\).
> I02 = `NOT OPENED`.

Chaîne à **ne pas mélanger** :

\[
\text{voisins historiques}
\;\rightarrow\;
\text{distribution prédictive}
\;\rightarrow\;
\text{proper scoring}
\;\rightarrow\;
\text{comparaison }X\text{ vs }S.
\]

Baseline figée en amont : \(W_X=W_{RV}=20\),
\(\mathcal{M}_Z=\{3,12,21\}\), \(h=10\), \(V_{t,10}\) défini,
\(s+10\le t\).

### 14J.1 Objectif

Pour une représentation \(R\in\{X,S_1,S_2,S_3\}\) à la query \(t\) :

1. voisins historiques admissibles \(N_k^{R}(t)=\{s_1,\ldots,s_k\}\) ;
2. targets déjà observables \(V_{s_i,10}\) ;
3. mesure prédictive empirique \(\widehat{\mathbb{P}}_t^{R}\) ;
4. proper score contre \(y=V_{t,10}\) ;
5. comparaison \(X\) vs chaque \(S\).

Question : cette architecture est-elle mathématiquement et
méthodologiquement propre pour I02 ?

### 14J.2 Ensemble admissible commun \(A_t\) — BLOCKING

Pour chaque query \(t\), un **seul** pool :

\[
A_t
=
\bigl\{
s :
\;
s < t,\;
s+10\le t,\;
R_s\text{ constructible pour tout }
R\in\{X,S_1,S_2,S_3\}
\bigr\}.
\]

« Constructible » inclut au minimum l'historique passé requis par
\(W_X=20\) (et les features \(S\) dérivées du même passé). Autres
contraintes éventuelles (calendrier, gaps) : protocole futur, mais
**communes** à toutes les \(R\).

\[
\boxed{N_k^{R}(t)\subset A_t
\quad\text{pour toute }R}
\]

**Interdit :** pool spécifique à \(X\) ou à un \(S\) ; filtrage
historique par \(Z_t\).

Sans \(A_t\) commun, \(\operatorname{Score}_S-\operatorname{Score}_X\)
n'est **pas** une comparaison paired propre.

### 14J.3 Forecast empirique

\[
\boxed{
\widehat{\mathbb{P}}_t^{R}
=
\frac1k\sum_{i=1}^{k}\delta_{V_{s_i,10}}
}
\quad
s_i\in N_k^{R}(t)
\]

**Verdict :** mesure de probabilité **valide** sur \(\mathbb{R}\)
(support effectif \(\subset[0,\infty)\)) — *empirical predictive
distribution*.

\[
\widehat{\mathbb{P}}_t^{R}
\;\neq\;
\mathcal{L}(V_{t,10}\mid R_t,\mathcal{F}_t)
\]

C'est un **objet de forecast** construit par voisinage, **pas** une
estime de la loi conditionnelle inconnue. Confondre les deux est une
attaque (§14J.19).

### 14J.4 Mesure vs ECDF

\[
\widehat F_t^{R}(v)
=
\widehat{\mathbb{P}}_t^{R}\bigl((-\infty,v]\bigr)
=
\frac1k\sum_{i=1}^{k}\mathbf{1}\{V_{s_i,10}\le v\}
\]

Même forecast sous deux formes.

| Forme | Rôle |
|-------|------|
| \(\widehat{\mathbb{P}}_t^{R}\) (mesure empirique / atomes) | **canonique** dans la spécification |
| \(\widehat F_t^{R}\) (ECDF) | représentation dérivée (intégrale CRPS, plots) |

### 14J.5 Pondération

**Baseline recommandée :** poids uniformes \(1/k\).

Distance weighting ⇒ bandwidth implicite, transformation de distance,
liberté méthodologique **non nécessaire** pour tester H1-I02, et
risque de tuning silencieux.

\[
\boxed{\texttt{UNIFORM WEIGHTING = MINIMAL BASELINE}}
\]

Distance weighting : **non retenu** comme baseline. Aucune
optimisation de poids.

### 14J.6 Ties de distance

Règle requise : déterministe ; indépendante de la représentation
*au niveau de la règle* (même procédure pour toute \(R\)) ;
indépendante de \(V\) futur et des scores.

| Option | Taille fixe \(k\) | Repro | Risque |
|--------|-------------------|-------|--------|
| **A.** ordre secondaire par index de session historique | oui | oui | léger biais temporel de tie-break |
| **B.** inclure tous les ties de frontière | non (\(\lvert N\rvert\ge k\)) | oui | CRPS/\(1/k\) non comparable |
| **C.** ordre secondaire par identifiant déterministe | oui | oui | proche de A |

**Verdict recommandé :** **A** — tri stable
\((\mathrm{distance}\uparrow,\; s\uparrow)\) ; garder exactement \(k\)
voisins. B rejeté (casse la taille fixe). C admissible équivalent si
l'identifiant = index de session.

Tie-break **par \(V_{s,10}\)** ou par score : **interdit**.

### 14J.7 Valeurs \(V\) dupliquées

Si \(V_{s_i,10}=V_{s_j,10}\) pour \(i\neq j\) : **deux atomes
distincts** (masse \(2/k\) au même point). Ce sont des observations
de forecast répétées, **pas** la fusion de voisins historiques.

Duplicate forecast values ≠ duplicate neighbors.

### 14J.8 CRPS — identité et propriétés

\[
\operatorname{CRPS}(F,y)
=
\int_{-\infty}^{+\infty}
\bigl(F(v)-\mathbf{1}\{y\le v\}\bigr)^{2}\,dv
\]

Pour \(F=\frac1k\sum_i\delta_{V_i}\) (équipondéré), identité
classique (ensemble / energy form) :

\[
\boxed{
\operatorname{CRPS}(F,y)
=
\frac1k\sum_i|V_i-y|
-
\frac1{2k^2}\sum_i\sum_j|V_i-V_j|
}
\]

**Vérification :** l'intégrale du CRPS pour une mesure empirique
finie se réduit à cette forme close (littérature proper scoring /
ensemble CRPS). Les termes diagonaux \(i=j\) du double somme sont
nuls ; les paires \(V_i=V_j\) réduisent la pénalité de dispersion —
comportement correct (sharpness).

| Propriété | Lecture |
|-----------|---------|
| Propriety | oui — espérance minimisée si \(F=\) vraie loi |
| Strict propriety | oui sur les lois à premier moment fini (cadre pertinent pour \(V\ge 0\)) |
| Unités | celles de \(V\) (RMS) |
| Orientation | **lower is better** |
| Échelle | sensible — §14J.13 |
| Queues | moins explosives que log-score ; miss extrême moins punitif |
| Forecast discret / petit \(k\) | bien défini ; variance du score ↑ si \(k\) petit |
| Doublons / outliers | gérés naturellement par la forme close |

**Verdict CRPS :** `ACCEPTED` comme proper scoring rule **primaire**
pour \(\widehat{\mathbb{P}}_t^{R}\) sous I02 pré-cadrage.

### 14J.9 Pourquoi CRPS ? (alternatives minimales)

| Score | Verdict pour I02 |
|-------|------------------|
| **CRPS** | évalue directement une loi empirique discrète **sans** densité |
| **A. log-score** | mal défini sur atomes (§14J.10) |
| **B. pinball / quantiles** | famille multi-niveaux ⇒ multiplicité ; utile en diagnostic, pas primaire |
| **C. MAE/MSE ponctuels** | dégénèrent le forecast en un point ; perdent calibration/sharpness |

Pas de zoo de benchmarks.

### 14J.10 Log-score et ECDF discrète

Une réalisation continue \(y\notin\{V_i\}\) a masse **nulle** sous
\(\widehat{\mathbb{P}}\) ⇒ log-score \(+\infty\) sans KDE / loi
paramétrique / lissage — **nouveaux** choix méthodologiques.

\[
\boxed{\texttt{LOG-SCORE REJECTED AS PRIMARY}}
\]

Argument **structurel** en faveur de CRPS pour I02.

### 14J.11 Comparaison \(X\) vs \(S\)

Pour \(S\in\{S_1,S_2,S_3\}\) :

\[
\Delta_t^{(S)}
:=
\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)
\]

| Signe | Lecture (CRPS lower-is-better) |
|-------|--------------------------------|
| \(\Delta>0\) | forecast \(X\) meilleur en \(t\) |
| \(\Delta=0\) | égalité |
| \(\Delta<0\) | forecast \(S\) meilleur en \(t\) |

\(\Delta_t^{(S)}\) = **différence de proper score**. Ce n'est **pas** :
information gain Shannon ; likelihood ratio ; effet causal ; valeur
économique.

**Orientation :** vérifiée. **Figé comme estimand I02 :** **non** —
voir §14J.13.

### 14J.12 « Extra information » — terminologie

H1 demande conceptuellement : \(X\) contient-il de l'information
prédictive **au-delà** de \(S\) ?

Sous un proper score, l'amélioration espérée

\[
\mathbb{E}[\Delta_t^{(S)}\mid \cdot]
\]

opérationnalise une **valeur prédictive incrémentale**
(*incremental predictive value under a proper score*), **pas** :

- information de Shannon / mutuelle ;
- « information causale ».

**Terminologie recommandée :**

```text
proper-score incremental predictive value
```

(abrégé acceptable : *incremental predictive value*). Éviter
« information gain » sans qualificatif.

### 14J.13 Dépendance d'échelle du CRPS — verdict clé

CRPS (et donc \(\Delta\)) a les **unités de \(V\)**.

Conséquences :

- régimes à \(V_{t,10}\) élevé → différences absolues mécaniquement
  plus grandes ;
- \(Z_t\) (instabilité / dynamique de volatilité) peut corréler avec
  \(|\Delta|\) **via l'échelle**, pas seulement via l'avantage
  prédictif ;
- normaliser \(\Delta\) **change l'estimand**.

**Aucune normalisation proposée ni acceptée ici.**

| Classe | |
|--------|--|
| A — harmless | non |
| B — diagnostic only | insuffisant pour I02 |
| **C — blocking estimand issue** | **oui** pour figer \(\Delta\) comme objet lié à \(Z\) / agrégation cross-\(t\) |

Nuance : à \(t\) fixé, même \(y\), \(\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)\)
reste une comparaison proper-score **paired valide**. Le blocage
porte sur l'**estimand scientifique** qui relie \(\Delta\) à la
dynamique de volatilité / \(Z_t\) / moyennes conditionnelles sans
traiter l'échelle.

\[
\boxed{
\texttt{SCALE DEPENDENCE = C (BLOCKING ESTIMAND ISSUE)}
}
\]

\[
\boxed{
\texttt{CRPS ACCEPTED};\quad
\Delta_t^{(S)}\ \texttt{NOT FROZEN AS FINAL ESTIMAND}
}
\]

**Prochaine étape logique (humaine) :** résoudre le statut d'échelle
de \(\Delta\) **avant** de figer l'estimand — sans improvisation de
normalisation post-hoc.

### 14J.14 Common target / common query

Conditions **nécessaires** pour un paired propre :

| Condition | Statut |
|-----------|--------|
| Même \(y=V_{t,10}\) | requis |
| Même \(A_t\) | requis (blocking) |
| Même \(k\) pour \(X\) et \(S\) | **STRUCTURAL** (§14J.15) |
| Même règle de ties | requis |
| Même weighting (uniforme) | requis |
| Même disponibilité / constructibilité | dans \(A_t\) |
| \(Z_t\) hors construction du forecast | requis (§14J.17) |

Same \(y\) + same \(A_t\) **ne suffisent pas** seuls.

### 14J.15 \(k\) reste OPEN — contraintes imposées

**Aucune valeur de \(k\) choisie.**

| Contrainte | Classe |
|------------|--------|
| \(k_X=k_S=k\) (identique pour toutes les \(R\) comparées) | **STRUCTURAL** |
| Règle de ties / weighting indépendantes de \(k\)'s choix numérique | STRUCTURAL (procédure) |
| \(k\) assez petit pour localité kNN | METHODOLOGICAL |
| \(k\) assez grand pour ECDF exploitable | METHODOLOGICAL |
| Interaction \(k\) vs \(\lvert A_t\rvert\) / début d'historique | METHODOLOGICAL + §14J.16 |
| Valeur numérique exacte ; héritage \(k=50\) | **OPEN** |

### 14J.16 Early history — \(\lvert A_t\rvert < k\)

| Politique | Comparabilité |
|-----------|----------------|
| **A. skip query \(t\)** | préserve taille \(k\) et CRPS comparable |
| B. fewer than \(k\) neighbors | change la loi empirique / score |
| C. adaptive \(k\) | liberté silencieuse ; casse le paired |

**Verdict :** **A — skip** lorsque \(\lvert A_t\rvert < k\).
B/C rejetés comme baseline. Ne sélectionne **pas** \(k\).

### 14J.17 \(Z_t\) et forecast object

Invariant :

\[
Z_t\text{ indexe / décrit l'état de la query ;\ ne construit pas le forecast.}
\]

\(Z_t\) **ne** filtre **pas** \(A_t\) ; **ne** sélectionne **pas**
des voisins « même \(Z\) » ; **ne** modifie **pas** \(k\), poids, ni
\(\widehat{\mathbb{P}}\). Relation \(Z\leftrightarrow\Delta\) : analyse
**ultérieure**, après résolution d'échelle (§14J.13).

### 14J.18 Dépendance temporelle

Documenté, non résolu :

- overlap des \(V_{\cdot,10}\) (jusqu'à 9 rendements) ;
- voisinages à évolution lente ;
- scores / \(\Delta\) successifs dépendants.

Affecte l'**inférence** future. **OPEN :** stride, blocks, bootstrap,
HAC, ESS — **non choisis**.

### 14J.19 Attaques

| Attaque | Rejet |
|---------|--------|
| ECDF = vraie loi conditionnelle | oui — §14J.3 |
| Distance weighting / tuning des poids | non baseline — §14J.5 |
| Ties résolus via target / score | interdit — §14J.6 |
| Log-score naïf sur ECDF | rejeté — §14J.10 |
| \(k\) différent \(X\) vs \(S\) | interdit — STRUCTURAL |
| Adaptive \(k\) silencieux | rejeté — §14J.16 |
| Pool différent selon \(R\) | interdit — §14J.2 |
| Filtrage par \(Z\) | interdit — §14J.17 |
| Normalisation post-hoc de \(\Delta\) | interdit sans décision d'estimand |
| « Information gain » abusif | terminologie §14J.12 |
| Score choisi pour le résultat souhaité | interdit (ordre objet→score) |

### 14J.20 Verdicts

| # | Item | Verdict |
|---|------|---------|
| 1 | Empirical predictive measure | **VALID forecast object** ; ≠ vraie loi cond. |
| 2 | ECDF | dérivée ; mesure **canonique** |
| 3 | Uniform weighting | **baseline minimale retenue** |
| 4 | Distance weighting | **non retenu** (baseline) |
| 5 | Tie policy | **A** — \((\mathrm{dist}\uparrow,s\uparrow)\), \(\lvert N\rvert=k\) |
| 6 | Duplicate \(V\) | **atomes distincts** (multiplicité) |
| 7 | CRPS | **`ACCEPTED`** (primary proper score) |
| 8 | Log-score | **`REJECTED`** as primary |
| 9 | Paired \(\mathrm{Score}_S-\mathrm{Score}_X\) | orientation OK ; conditions §14J.14 |
| 10 | Terminologie | *proper-score incremental predictive value* |
| 11 | Scale dependence | **`C` — BLOCKING ESTIMAND ISSUE** |
| 12 | Common-\(k\) | **STRUCTURAL** |
| 13 | Early history | **skip** si \(\lvert A_t\rvert < k\) |

### 14J.21 Décisions de cette revue

**Retenu / accepté :**

- forecast object canonique \(\widehat{\mathbb{P}}_t^{R}\) ;
- weighting uniforme ;
- tie rule A ;
- duplicate handling (atomes distincts) ;
- CRPS `ACCEPTED` ;
- orientation de \(\Delta_t^{(S)}\) ;
- early-history = skip ;
- \(A_t\) commun blocking ;
- terminologie incremental predictive value.

**Non décidé :**

- valeur de \(k\) ; stride ; \(Z_t\) finale ; Spearman ;
- procédure d'inférence ;
- **forme définitive de \(\Delta\) comme estimand** (bloque sur **C**).

### 14J.22 Cohérence

| Contrôle | OK |
|----------|-----|
| \(k\) OPEN | oui |
| stride OPEN | oui |
| NO \(Z_t\) ACCEPTED | oui |
| CRPS ACCEPTED ; \(\Delta\) not frozen | oui |
| NO DATA / NO EXPERIMENT | oui |
| I02 NOT OPENED | oui |

\[
\boxed{\texttt{CRPS ACCEPTED}}
\quad
\boxed{\texttt{SCALE DEPENDENCE = C}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\quad
\boxed{k=\texttt{OPEN}}
\]

**Suite :** revue d'estimand §14K (pas un nouveau score).

---

## 14K. Scale-adjusted score estimand

> **Nature :** mathématique / méthodologique / documentaire.
> **NO DATA. NO EXPERIMENT. NO CODE.**
> CRPS reste `ACCEPTED`. \(k\), stride, Spearman = `OPEN`.
> \(\texttt{NO }Z_t\texttt{ ACCEPTED}\). I02 = `NOT OPENED`.

Cette revue porte sur l'**estimand**, pas sur le score.

Notation : \(D_t^{(S)}=\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)\)
(synonyme historique \(\Delta_t^{(S)}\)). \(D\) brute **n'est pas**
acceptée comme estimand final (§14J.13).

### 14K.1 Objectif

Opérationnaliser

```text
proper-score incremental predictive value
```

de \(X\) relativement à \(S\), **sans** confondre :

- amélioration prédictive relative **authentique** ;
- agrandissement **mécanique** des différences CRPS quand l'échelle
  de volatilité est plus grande.

### 14K.2 Propriété d'échelle du CRPS

Soit \(F=\frac1k\sum_i\delta_{V_i}\) et \(a>0\). La loi mise à
l'échelle \(aF\) a des atomes en \(aV_i\). Forme ensemble :

\[
\operatorname{CRPS}(aF,ay)
=
\frac1k\sum_i|aV_i-ay|
-
\frac1{2k^2}\sum_i\sum_j|aV_i-aV_j|
=
a\,\operatorname{CRPS}(F,y).
\]

Donc \(D\) transforme comme

\[
D_t^{(S)}\;\longmapsto\; a\,D_t^{(S)}
\]

sous mise à l'échelle **commune** des forecasts et de \(y\).

| Concept | |
|---------|--|
| *Scale equivariance* du CRPS | \(\operatorname{CRPS}(aF,ay)=a\operatorname{CRPS}(F,y)\) |
| *Scale invariance* d'un estimand \(E\) | \(E\mapsto E\) sous \(r\mapsto a r\) (\(a>0\)) |

Le CRPS est équivariant ; un estimand de **comparaison relative**
peut (ou non) être invariant. Ce n'est **pas** automatique que
invariant = meilleur — il faut savoir **quelle question** \(E\) pose.

### 14K.3 Pourquoi blocking pour I02

Analyse future candidate : relation entre \(Z_t(m_Z)\) et l'avantage
prédictif de \(X\) sur \(S\). Or \(Z\) dérive de \(L=\log RV\) et de
la dynamique de \(\Delta L\).

Chemins de confounding d'échelle (sans données) :

1. **Niveau** : \(V\) et CRPS plus grands en régime volatile ⇒
   \(|D|\) mécaniquement plus grand même si le *rapport* de
   performance est stable.
2. **Chevauchement sémantique** : \(RV_t\) entre dans \(S_1/S_2/S_3\)
   *et* dans \(L_t\) ; corréler \(Z\) (voisin de \(L\)) à \(D\) brut
   mélange niveau, instabilité, et unités du score.
3. **Agrégation cross-\(t\)** : \(\mathbb{E}[D]\) ou rangs de \(D\)
   pondèrent implicitement les jours à haute volatilité.

Le paired day-\(t\) reste valide ; le blocage est l'**estimand**
scientifique \(Z\)-lié / agrégé.

### 14K.4 Familles d'estimands

#### A — Raw difference

\[
D_t^{(S)}=\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)
\]

**Question estimée :** gain absolu de proper score (unités de \(V\)).

| | |
|--|--|
| Scale test \(r\mapsto a r\) | \(D\mapsto a D\) |
| Orientation | \(D>0\) ⇒ \(X\) meilleur |
| Bornes | non borné |
| Singularité | aucune |
| Verdict primaire | **`REJECT`** comme estimand final |
| Statut secondaire | **retenir** (§14K.12) |

#### B — Comparator-relative

\[
R_t^{(S)}
=
\frac{\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)}{\operatorname{CRPS}_S(t)}
=
1-\frac{\operatorname{CRPS}_X(t)}{\operatorname{CRPS}_S(t)}
\]

**Question estimée :** *quelle fraction de l'erreur probabiliste de
\(S\) \(X\) élimine-t-il ?* — proche de « \(X\) beyond \(S\) »,
asymétrique par construction.

| | |
|--|--|
| Scale test | \(R\mapsto R\) (invariant) |
| Orientation | même signe que \(D\) si \(\operatorname{CRPS}_S>0\) |
| Bornes | \(R\le 1\) ; \(R\to-\infty\) possible si \(X\) bien pire |
| Singularité | \(\operatorname{CRPS}_S=0\) |
| Verdict | **`PROMISING`** |

#### C — Symmetric relative

\[
Q_t^{(S)}
=
\frac{\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)}{\operatorname{CRPS}_S(t)+\operatorname{CRPS}_X(t)}
\]

(\(\operatorname{CRPS}_S+\operatorname{CRPS}_X\) comme échelle
symétrique naturelle ; **pas** d'\(\varepsilon\).)

**Question estimée :** avantage relatif **entre** les deux
performances réalisées — le dénominateur dépend des **deux** scores.

| | |
|--|--|
| Scale test | \(Q\mapsto Q\) |
| Orientation | signe\((Q)=\)signe\((D)\) si dénominateur \(>0\) |
| Bornes | \(Q\in(-1,1)\) si scores \(\ge 0\) non tous nuls |
| Singularité | \(\operatorname{CRPS}_S=\operatorname{CRPS}_X=0\) |
| Verdict | **`PROMISING`** |

Élégant et bornable ; **change** légèrement la question (unité =
somme des erreurs des deux modèles, pas l'erreur du comparator).

#### D — Ex-ante volatility normalization

\[
N_t^{(S)}
=
\frac{\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)}{G_t},
\qquad
G_t=RV_t
\quad\text{(candidat ; non accepté automatiquement)}
\]

\(G_t\) exigé : \(\mathcal{F}_t\)-mesurable ; commun \(X\)/\(S\) ;
défini avant \(V_{t,10}\) ; lié à l'échelle courante.

**Question estimée :** gain de proper score **par unité** de
volatilité réalisée *passée* (\(W_{RV}=20\)).

| | |
|--|--|
| Scale test \(r\mapsto a r\) | \(RV\mapsto a\,RV\), \(D\mapsto a D\) ⇒ \(N\mapsto N\) |
| Orientation | signe\((N)=\)signe\((D)\) si \(RV_t>0\) |
| Singularité | \(RV_t=0\) |
| Verdict | **`PROMISING`** |

### 14K.5 Future-realized normalization — REJECT

Normaliser par \(V_{t,10}\) (ou tout fonctionnel de
\(r_{t+1},\ldots,r_{t+10}\)) :

- rend le dénominateur **outcome-dependent** ;
- mélange l'échelle *ex ante* avec la réalisation *future* scorée ;
- change l'estimand selon \(y\) lui-même (pas seulement selon
  l'état courant).

Même si \(V_{t,10}\) est connu *ex post* au scoring, ce n'est **pas**
une normalisation d'unité d'état.

\[
\boxed{\texttt{FUTURE-}V\text{ NORMALIZATION = REJECT}}
\]

### 14K.6 Scale invariance test (résumé)

Sous \(r_u\mapsto a r_u\) pour tout \(u\) (\(a>0\)) :
\(V\mapsto a V\), atomes \(\mapsto a\cdot\), CRPS \(\mapsto a\cdot\),
\(RV\mapsto a\cdot\).

| Estimand | Transformation |
|----------|----------------|
| \(D\) | \(\times a\) |
| \(R\) | invariant |
| \(Q\) | invariant |
| \(N=D/RV_t\) | invariant |
| \(D/V_{t,10}\) | invariant **mais REJECT** (§14K.5) |

### 14K.7 Orientation, bornes, extrêmes

| | \(D\) | \(R\) | \(Q\) | \(N\) |
|--|-------|-------|-------|-------|
| Zéro | scores égaux | idem (si dén. OK) | idem | idem |
| Deux forecasts parfaits | \(0\) | **singulier** / indéfini | **singulier** | \(0\) si \(RV>0\) |
| Seul \(X\) parfait, \(S>0\) | \(>0\) | \(=1\) | \(\in(0,1)\) | \(>0\) |
| Scores \(\approx 0^+\) | petit | **instable** | borné mais sensible | dépend de \(RV\) |
| Interprétation | unités \(V\) | fraction d'erreur \(S\) | part relative bornée | unités « par \(RV\) » |

### 14K.8 Symétrie vs question scientifique

I02 est **directionnel** : \(X\) ajoute-t-il de la valeur au-delà de
\(S\) ?

- **Asymétrie \(R\)** : scientifiquement cohérente avec « beyond \(S\) »
  — le comparator définit l'unité. Coût : singularité /
  instabilité quand \(S\) est déjà excellent.
- **Symétrie \(Q\)** : méthodologiquement propre, bornée ; l'unité
  n'est plus « l'erreur de \(S\) » mais « la somme des erreurs ».
  Moins alignée mot à mot avec « beyond \(S\) », plus stable.

Les deux restent **défendables** ; ce n'est pas un tie-break
automatique.

### 14K.9 Normalisation par \(RV_t\) — examen

1. **Causal / \(\mathcal{F}_t\)** : oui — \(RV_t\) sur
   \(\{r_{t-W_{RV}+1},\ldots,r_t\}\), \(W_{RV}=20\).
2. **Commun \(X\)/\(S\)** : oui.
3. **Scale-invariant** sous \(r\mapsto a r\) : oui (§14K.6).
4. **Singularité \(RV_t=0\)** : théorique si tous les \(r\) de la
   fenêtre sont nuls ; rare empiriquement, **pas** impossible
   mathématiquement.
5. **Conditionnement sur une composante de \(S\)** : oui partiellement
   — \(RV\) *est* \(S_1\) (et entre dans \(S_2/S_3\)). Normaliser par
   \(RV_t\) ancre l'unité sur une feature déjà adversariale.
6. **Retrait de phénomène** : risque de retirer l'effet *de niveau*
   tout en gardant ce qui est relatif à ce niveau ; si une partie du
   signal scientifique est « \(X\) aide surtout quand \(RV\) est
   haut/bas *en niveau* », \(N\) le rescale. Ce n'est pas
   automatiquement mauvais — c'est une **autre question**.
7. **Unité vs question** : les deux — retire la dimension, **et**
   reformule l'estimand en « par unité de \(RV\) courant ».

Lien avec \(Z\) (§14K.10) : normaliser par le **niveau** \(RV\) peut
permettre de demander si l'**instabilité** (\(\Delta L\)) s'associe à
un avantage *à échelle comparable* — interprétation **plausible mais
trop forte** pour être déclarée ici sans \(Z_t\) acceptée.

### 14K.10 \(Z\) ≠ niveau \(RV\)

\(L_t=\log RV_t\) ; \(Z_t\) vise l'instabilité locale de \(\Delta L\),
pas \(L_t\) seul. \(N=D/RV_t\) traite l'échelle de **niveau**, pas
l'instabilité. Utile comme *candidat* d'unité ; **ne valide pas** et
**n'accepte pas** \(Z_t\).

### 14K.11 Zero / near-zero — politique structurelle

**Interdit :** \(\mathrm{denom}+10^{-8}\) sans axiome.

| Dénominateur | Nul quand | Politique structurelle candidate |
|--------------|-----------|----------------------------------|
| \(\operatorname{CRPS}_S\) | forecast \(S\) parfait (masse exacte en \(y\)) | **skip** \(t\) pour \(R\) *ou* laisser indéfini — pas d'\(\varepsilon\) |
| \(\operatorname{CRPS}_S+\operatorname{CRPS}_X\) | les deux parfaits | idem pour \(Q\) |
| \(RV_t\) | fenêtre de rendements tous nuls | **skip** \(t\) pour \(N\) (cohérent avec skip \(\lvert A_t\rvert<k\)) |

Impossibilité théorique vs rareté : CRPS exact zéro est possible pour
mesure empirique (un atome = \(y\), ou tous égaux à \(y\)) ; \(RV=0\)
possible sur données discrètes/arrondies. Politique = **skip** /
undefined, figée *avant* données — détail protocolaire ouvert tant
que l'estimand n'est pas choisi.

### 14K.12 Raw \(D\) secondaire

Même si un estimand scale-adjusted est retenu plus tard :

\[
\boxed{D_t^{(S)}\ \texttt{= DESCRIPTIVE SECONDARY ONLY}}
\]

Conserve unités naturelles, magnitude absolue, diagnostic de
l'effet de normalisation. **Ne récupère pas** le statut d'estimand
principal.

### 14K.13 Spearman (OPEN) — dépendance conceptuelle

\(\operatorname{Spearman}(Z,D)\) et
\(\operatorname{Spearman}(Z,D/G)\) **ne coïncident pas** en général
si \(G_t\) varie avec \(t\) (transformation observation-par-observation
non monotone commune).

⇒ la question d'échelle / d'estimand doit être **résolue avant**
Spearman. Spearman reste `OPEN` ; **non accepté**.

### 14K.14 \(k\) (OPEN)

Les quatre constructions (et leurs invariances) sont valides pour
tout \(k\) admissible sous le forecast object §14J. Aucune ne force
structurellement une valeur de \(k\). Near-zero CRPS peut être un
peu plus fréquent si \(k=1\) et atome = \(y\) — reste méthodologique,
pas un choix de \(k\).

### 14K.15 Terminologie

Conserver le genre :

```text
proper-score incremental predictive value
```

Selon construction (si retenue plus tard) :

| Estimand | Nom candidat |
|----------|----------------|
| \(D\) | absolute proper-score incremental value *(secondaire)* |
| \(R\) | comparator-relative proper-score incremental value |
| \(Q\) | symmetric relative proper-score incremental value |
| \(N\) | ex-ante scale-adjusted proper-score incremental value |

Éviter « information gain » information-théorique.

### 14K.16 Attaques

| Attaque | Rejet |
|---------|--------|
| \(D\) brut comme estimand \(Z\)-lié malgré confounding | oui — REJECT primaire |
| Ratio seul parce que dimensionless | insuffisant — il faut la *question* |
| Division par \(V_{t,10}\) | REJECT |
| \(\varepsilon\) arbitraire | interdit |
| Dénominateur \(\approx 0\) ignoré | politique skip requise |
| Asymétrie / symétrie cachée | documentées §14K.8 |
| \(RV_t\) qui retire le signal sans le dire | risque documenté §14K.9 |
| Normalisation choisie pour corréler mieux avec \(Z\) | snooping — interdit |
| Multi-normalisations testées puis meilleure | interdit |

### 14K.17 Verdicts et classification

| Construction | Verdict |
|--------------|---------|
| Raw \(D\) | **`REJECT`** (primaire) ; secondaire OK |
| Comparator-relative \(R\) | **`PROMISING`** |
| Symmetric-relative \(Q\) | **`PROMISING`** |
| Ex-ante \(D/RV_t\) | **`PROMISING`** |
| Future-\(V\) normalized | **`REJECT`** |

**Classification de clôture de l'estimand :**

\[
\boxed{\texttt{B — HUMAN DECISION REQUIRED}}
\]

Trois constructions restent **réellement défendables** et
estiment des questions **distinctes** :

1. \(R\) — fraction de l'erreur de \(S\) éliminée ;
2. \(Q\) — avantage relatif borné entre deux performances ;
3. \(N\) — gain par unité de \(RV\) ex ante.

Aucune n'est éliminée par mathématique pure. **STOP** — décision
humaine avant données. Pas A (identifiable maintenant). Pas C
(pas besoin d'hypothèse scientifique *nouvelle* au-delà du choix
d'estimand). Pas D.

**Aucun estimand final accepté dans cette revue.**

### 14K.18 Décision autorisée — non exercée

La revue **pourrait** recommander un final ; elle **s'abstient** :
plusieurs constructions `PROMISING` restent légitimes. Demande
explicite : **décision humaine** parmi \(\{R,Q,N\}\) (ou raffinement
explicite), avec \(D\) secondaire.

### 14K.19 Cohérence

| Contrôle | OK |
|----------|-----|
| CRPS inchangé / ACCEPTED | oui |
| Pas de nouvel estimand figé | oui |
| \(k\) / stride / Spearman OPEN | oui |
| NO \(Z_t\) ACCEPTED | oui |
| NO DATA / NO EXPERIMENT | oui |
| I02 NOT OPENED | oui |

\[
\boxed{\texttt{ESTIMAND CLASS = B}}
\quad
\boxed{R,\;Q,\;N\ \texttt{= PROMISING}}
\quad
\boxed{D\ \texttt{= SECONDARY}}
\quad
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

---

## 15. Market-State / Regime Engine

**Aucun contrat empirique n'est dérivé d'I01.** Aucune architecture
modifiée. I02, s'il est autorisé plus tard, pourra ou non informer
ce contrat. \(Z_t\) **n'est pas** un Market-State Engine.

---

## 16. OPEN QUESTION — liste exacte

Ne pas résoudre dans ce draft :

- **estimand principal** parmi \(\{R,Q,N\}\) — décision humaine
  (§14K class **B**) ; politique skip exacte du dénominateur nul ;
- stride 1 ; formule \(Z_t\) complète ;
- correction multiplicité ; pool redundancy ;
- désaccord matériel §9.16 ; agrégation \(L\)+forme ;
- singularités métriques — pas d'\(\varepsilon\) ;
- \(k\) ; holdout ; Market-State Engine ;
- Spearman ; procédure d'inférence (bootstrap / HAC).

**CLOSED :**

- horizons \(W_X/W_{RV}/\mathcal{M}_Z\) ;
- **\(h=10\)** ; **\(V_{t,10}\)** ; multi-\(h\) rejeté ;
- forecast object ; CRPS `ACCEPTED` ; log-score primary rejected ;
- \(D\) brut = REJECT primaire / secondaire OK ;
- future-\(V\) normalization REJECT ;
- cartographie \(R,Q,N\) = `PROMISING` (questions distinctes).

\[
\boxed{\text{NO }Z_t\text{ ACCEPTED}}
\]

---

## 17. Before I02 can open

Décisions **humaines**. Tant que la dernière case n'est pas cochée :

**I02 = NOT OPENED.**

- [ ] Hypothèse finale approuvée (H1-v0.2 reste une candidate)
- [x] Doctrine §9.16 **acceptée** ; métriques pré-cadrage **CLOSED**
- [x] Revue documentaire \(Z_t\) (§14–§14A)
- [x] Décision sémantique cas 3 / cas 5 : famille **A** =
      `PRIMARY SEMANTIC CANDIDATE` ; \(E\) = mécanisme alternatif
      (≠ robustesse de A) — **pas** de \(Z_t\) acceptée (§14A.12)
- [x] Revue Disp §14B ; **\(\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\)
      `ACCEPTED`** (§14B.11) ; MAD REJECT ; MeanAD non retenue
- [x] Revue architecture temporelle §14C
- [x] **\(W_{RV}:=W_X\)** `ACCEPTED` (§14C.9) —
      `METHODOLOGICAL COMPARABILITY COUPLING` ; sémantiques distinctes
- [x] Revue admissibilité \(m_Z\) (§14D) —
      `STRUCTURALLY CONSTRAINED`
- [x] Domaine **\(3\le m_Z\le W_{RV}+1\)** `ACCEPTED` (§14E.1) ;
      not identifiable ; classification **C** (§14E.7)
- [x] Gouvernance multi-échelle §14F : POLICY FREEZE ;
      NUMERICAL \(\mathcal{M}_Z\) **après \(W_X\)** (`B`) ;
      no-primary ; MS-1…4
- [x] Revue \(W_X\) §14G : class `B` preferred
- [x] **\(W_X=20\)** `ACCEPTED` ; \(W_{RV}=20\) ; domaine
      \(3\le m_Z\le 21\)
- [x] \(\mathcal{M}_Z=\{3,12,21\}\) `ACCEPTED` (§14H) — no-primary
- [x] **\(V_{t,10}\)** fully specified ; **\(h=10\)** `ACCEPTED`
      (§14I.14) — `INHERITED FIXED FORECAST HORIZON`
- [x] Forecast object + **CRPS `ACCEPTED`** (§14J)
- [x] Revue échelle / estimand §14K — class **B** ;
      \(D\) secondaire ; future-\(V\) REJECT
- [ ] **Décision humaine** estimand principal \(\in\{R,Q,N\}\)
- [ ] stride 1 ; \(Z_t\) complète ; \(k\)
- [x] Représentations \(S_1/S_2/S_3\) **acceptées**
- [x] Invariant multiplicatif **accepté**
- [x] Observable futur **approuvé** — \(V_{t,10}\) + \(h=10\)
- [x] Score probabiliste **approuvé** — CRPS (§14J)
- [ ] Rôle de `H_shape` défini
- [ ] Kill criteria approuvés
- [ ] Stratégie de données / réplication définie
- [ ] Risque de data snooping documenté
- [ ] Protocole de gel avant premier résultat
- [ ] Décision explicite **OPEN I02**

---

## 18. Revue de cohérence (auteur)

| Contrôle | Statut |
|----------|--------|
| Aucun chiffre / donnée / calcul | oui |
| \(S_1/S_2/S_3\) / §9.16 inchangés | oui |
| Famille A = primary semantic candidate (§14A.12) | oui |
| \(\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\) `ACCEPTED` | oui |
| \(W_{RV}:=W_X\) comparability coupling `ACCEPTED` | oui |
| \(3\le m_Z\le W_{RV}+1\) `ACCEPTED` ; not identifiable ; class C | oui |
| §14F multi-scale policy ; NUMERICAL after \(W_X\) | oui |
| \(V_{t,10}\) + \(h=10\) ACCEPTED | oui |
| CRPS ACCEPTED ; estimand class B ; no \(Z_t\) | oui |
| \(k\) / stride / Spearman OPEN ; I02 NOT OPENED | oui |

---

## Références (lecture, pas autorité de validation)

- [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
- E01–E04 ; [hypothesis.md](../I01/hypothesis.md) ; [protocol.md](../I01/protocol.md)
- [DR-007](../../docs/adr/DR-007-exploratory-vs-confirmatory-data.md)
- [DR-008](../../docs/adr/DR-008-i01-e01-exploratory-source.md)
- CRPS : proper scoring rule pour lois réelles (littérature ; pas un
  calcul sur SPY) ; forme ensemble / energy score empirique ;
  homogénéité de degré 1
