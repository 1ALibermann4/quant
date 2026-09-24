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
> **Calculs dans ce document :** aucun
> **Classe données I01 :** UNQUALIFIED (DR-007 / DR-008)

Ce fichier **ne signifie pas** que I02 est ouvert.
Aucun protocole, aucun run, aucun code expérimental I02 n'est autorisé.

$$
\text{observations I01} \neq \text{preuve de cette hypothèse candidate}
$$

E01–E04 ont **généré** la piste. Ils ne peuvent pas la valider.

**Statut des adversaires \(S\) (acceptation humaine) :**

```text
REPRESENTATION ACCEPTED / METRIC UNRESOLVED
```

\(S_1\), \(S_2^{\mathrm{NEW}}\), \(S_3^{\mathrm{NEW}}\) : nature informationnelle
**acceptée**. Distance, scaling, \(W\), découpage 10+10, \(C_t\), CRPS :
**non** acceptés. CRPS reste `ACCEPTABLE CANDIDATE`. I02 reste
`NOT OPENED`.

---

## 0. Ce que ce draft n'est pas

- pas un SCI-PASS, pas un SCI-FAIL ;
- pas une recommandation de confirmer I01 ;
- pas une ouverture de DR-003 / DR-005 ;
- pas E05 ;
- pas un contrat empirique pour un Market-State / Regime Engine ;
- pas un choix de seuil, de source, ni d'instrument ;
- pas une acceptation de CRPS, de \(h\), de la **distance** / du
  **scaling** de \(S\), ni de \(C_t\) ;
- pas une ouverture d'I02 (même après acceptation des représentations \(S\)).

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

## 3. Variable future candidate \(V_{t,h}\)

**Proposition à évaluer, non figée.**

$$
V_{t,h}
=
\sqrt{
\frac{1}{h}
\sum_{j=1}^{h}
r_{t+j}^{2}
}
$$

Interprétation : amplitude / volatilité réalisée sur les \(h\) séances
**suivant** \(t\) (après clôture de \(t\) ; \(Y\) commence à \(t+1\)).

Propriétés voulues :

- attachée à **chaque** date \(t\), pas à un voisinage ;
- existe **indépendamment** de L2 et de `H_vol` ;
- ne préjuge pas de la méthode de prédiction ;
- \(V_{t,h}\geq 0\).

La variante sans \(1/h\) n'en diffère que par la constante \(\sqrt{h}\)
si \(h\) est fixé. La forme ci-dessus est préférée pour la lecture
(« amplitude par séance », au sens RMS).

\(h\) **n'est pas figé**. Voir §3.1.

### 3.1 Hériter \(h=10\) d'I01 ? — pour et contre

| Pour | Contre |
|------|--------|
| I02 est **dérivée** d'une observation générée à \(h=10\). Conserver l'horizon évite de chercher l'horizon qui maximise le nouvel effet. | Reprendre 10 par habitude n'est pas neutre (OPEN du draft v0.1). |
| Justification explicite possible : *on refuse d'optimiser \(h\)*, pas « 10 est optimal ». | Un autre \(h\) pré-annoncé (5, 21, …) serait aussi non optimisé, et n'hériterait pas du générateur. |
| Alignement avec \(Y_t^{(h)}\) déjà défini (DEC-04, protocole I01). | Si le phénomène I01 est spécifique à 10 séances, I02 le reproduit par construction d'horizon. |

État : **OPEN QUESTION**. Candidat documenté : hériter \(h=10\) *parce
qu'on refuse de l'optimiser*. Même logique possible plus tard pour
\(W=20\), sous réserve de la décision sur \(X_t\).

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

**Aucun \(k\) nouveau. Aucun calcul. Aucune implémentation.**
Distance et scaling de \(S\) : **OPEN** (`METRIC UNRESOLVED`).
Composition informationnelle : **acceptée** (§9).

Pour une requête \(t\), candidat :

$$
N_X(t)=\operatorname{kNN}(X_t),\qquad
\widehat F_X(v\mid t)
=
\frac{1}{k}\sum_{s\in N_X(t)}\mathbf{1}\{V_{s,h}\le v\}
$$

$$
N_S(t)=\operatorname{kNN}(S_t),\qquad
\widehat F_S(v\mid t)
=
\frac{1}{k}\sum_{s\in N_S(t)}\mathbf{1}\{V_{s,h}\le v\}
$$

Ce sont des **prévisions probabilistes** candidates de \(V_{t,h}\),
construites uniquement à partir de \(V_{s,h}\) **historiques** des
voisins (sélection = fonction de \(X\) ou de \(S\), pas de \(V_{t,h}\)
— même discipline AF-08 qu'I01).

Le voisinage reste l'**opérateur expérimental**. On n'ouvre pas une
course XGBoost(\(X\)) vs forêt(\(rv\)).

B0 (tirage dans \(\mathcal{L}_t\)) peut fournir une troisième \(\widehat F\)
de référence. Il n'est pas l'adversaire suffisant de H1.

---

## 6. CRPS — métrique principale **candidate**

**Pas calculé. Pas un gate.**

$$
\operatorname{CRPS}(F,y)
=
\int_{-\infty}^{+\infty}
\bigl(F(z)-\mathbf{1}\{y\le z\}\bigr)^{2}\,dz
$$

Convention : **plus faible = meilleure** prévision probabiliste.

Candidats opérationnels :

$$
\operatorname{CRPS}_X(t)=\operatorname{CRPS}(\widehat F_X(\cdot\mid t),V_{t,h})
$$

$$
\operatorname{CRPS}_S(t)=\operatorname{CRPS}(\widehat F_S(\cdot\mid t),V_{t,h})
$$

$$
D^{\mathrm{CRPS}}_t
=
\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)
$$

\(D^{\mathrm{CRPS}}_t>0\) signifierait : ce jour-là, \(\widehat F_X\) a
mieux décrit \(V_{t,h}\) observé que \(\widehat F_S\).

Quantité centrale **candidate** (si CRPS et \(C_t\) étaient un jour
retenus) :

$$
\mathbb{E}\bigl[D^{\mathrm{CRPS}}_t \bigm| C_t=1\bigr]
$$

sur information indépendante. **Aucun seuil. Aucun calcul.**

Pour un ensemble fini de \(k\) atomes, le CRPS a une forme close
classique (moyenne des écarts à \(y\) moins la demi-dispersion interne
de l'ensemble). Le mentionner n'autorise pas à l'implémenter ici.

### 6.1 CRPS adversarial review

Objectif : CRPS peut-il devenir métrique confirmatoire principale
**sans** ouvrir une sélection post hoc ? Aucune alternative n'est
testée sur les données.

| Point | Lecture |
|-------|---------|
| Variable continue \(\geq 0\) | CRPS est défini pour toute loi réelle. Le support \([0,\infty)\) n'est pas imposé par l'intégrale ; l'ECDF empirique est portée par des \(V_{s,h}\geq 0\), donc le support effectif est correct. Pas un motif de rejet. |
| Calibration | Proper scoring rule : l'espérance est minimisée par la vraie loi. Une ECDF mal calibrée est pénalisée. |
| Sharpness / dispersion | Pénalise à la fois le biais et l'excès de largeur. Une loi trop plate (contrôle « 0.8 … 6.1 ») est battue par une loi concentrée autour de \(y\), *si* \(y\) tombe dedans. |
| Ensemble de \(k\) points | Avec \(k\) petit, \(\widehat F\) est en escalier. Le CRPS reste bien défini ; la variance du score est plus grande. Hériter \(k=50\) (OPEN) n'est pas anodin : trop peu d'atomes ⇒ loi rugueuse. Ce n'est pas une raison de changer \(k\) après un chiffre. |
| Queues | Moins dominé par les queues que le log-score (qui explose si \(y\) sort d'une densité paramétrique). Inversement, un miss extrême est moins punitif qu'en vraisemblance. Compatible avec H3 : il faudra regarder si \(\mathbb{E}[D\mid C=1]\) est une moyenne de queue. |
| Échelle de \(V\) | Le CRPS est **dans les unités de \(V\)**. Les jours à \(V\) élevé pèsent plus sur la moyenne. Si \(C_t=1\) sélectionne des états déjà volatils, \(\mathbb{E}[D\mid C=1]\) peut être dominé par quelques \(V\) grands — cousin d'H3. Une normalisation (CRPS / \(V\), rang, …) **n'est pas choisie** ici : la choisir après un run serait du snooping. Risque **documenté**, pas un motif de tester une autre métrique maintenant. |
| vs erreur absolue ponctuelle | MAE de la moyenne ou de la médiane d'ensemble = cas dégénéré (prévision d'un point). Plus faible philosophiquement : on perd calibration/sharpness. Utile comme **diagnostic**, pas comme remplaçant silencieux. |
| vs log-score | Exige une densité. Imposer une loi paramétrique sur \(k\) voisins ajoute un modèle. Contredit « pas de ML / pas de loi inventée ». Écarté comme primaire. |
| vs calibration + sharpness séparées | Plus riches, plus de degrés de liberté ⇒ plus de tentation post hoc. Le CRPS les **combine** en une proper rule. Les séparer reste un diagnostic possible, pas une batterie de gates. |

**Verdict documentaire sur le CRPS :** `ACCEPTABLE CANDIDATE`.

Pas `ACCEPTÉ`. Pas `REJECT`. Les réserves d'échelle et de queue
doivent rester visibles si une décision humaine le retient. Aucun
gate numérique.

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

**Statut :** `REPRESENTATION ACCEPTED / METRIC UNRESOLVED`
(acceptation humaine après revue §9.13 @ `5980bc8`).

Ce qui est accepté : la **nature informationnelle** des trois
adversaires et leurs coordonnées NEW. Ce qui **ne** l'est **pas** :
distance, scaling, \(W\), partage 10+10, convention aux singularités,
\(C_t\).

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

### 9.9 Distance / normalisation — OPEN

\(RV\), \(\Delta RV\), \(D\), \(MA\) et \(Q\) n'ont pas les mêmes
échelles ni les mêmes lois. Un kNN euclidien **brut** sur
\([RV,\Delta RV]\), \([RV,D]\), \([RV,MA]\) ou \([RV,Q]\) est déjà un
choix scientifique — y compris après reparamétrisation.

Restent OPEN : métrique ; scaling ; standardisation éventuelle ;
fenêtre de cette standardisation ; causalité de cette
normalisation. **Aucun choix.** La reparamétrisation **ne** résout
**pas** le problème de distance.

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

**Représentations acceptées** (`REPRESENTATION ACCEPTED / METRIC UNRESOLVED`) :

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

- ni \(W=20\), ni découpage 10+10, ni distance, ni scaling ;
- ni convention \(\varepsilon\) aux zéros ;
- ni ouverture d'I02.

**Prochaine question (OPEN, non acceptée) :** avant z-score ou rangs,
étudier les **invariances** que la distance doit satisfaire. En
particulier, puisque \(D\) et \(Q\) sont déjà invariants d'échelle,
traiter éventuellement le niveau en forme relative

\[
S_2^\star=[\log RV,\,D],
\qquad
S_3^\star=[\log RV,\,Q]
\]

de sorte que \(|\log RV_a-\log RV_b|=|\log(RV_a/RV_b)|\). **Non
accepté.** À examiner documentairement **avant** z-score causal et
rangs — pas ici.

Distance / scaling : **toujours OPEN**.

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
   chercher \(W\) après coup).

Un kill n'est pas un SCI-FAIL d'I01.

---

## 14. Stress / market condition — définition non résolue

**OPEN QUESTION.** Inchangé dans l'esprit du draft v0.1.

Interdit comme définition : années 2008 / 2009 / 2020 ; seuil `rv_W`
ou tertile relu en règle après E04.

Principes toujours exigés : causalité ; disponibilité à \(t\) ; gel
avant expérimentation ; indépendance maximale vis-à-vis du générateur ;
simplicité ; interprétabilité ; **pas** d'optimisation sur \(D_{vol}\)
ni sur \(D^{\mathrm{CRPS}}\).

**Aucune définition n'est choisie.**

---

## 15. Market-State / Regime Engine

**Aucun contrat empirique n'est dérivé d'I01.** Aucune architecture
modifiée. I02, s'il est autorisé plus tard, pourra ou non informer
ce contrat.

---

## 16. OPEN QUESTION — liste exacte

Ne pas résoudre dans ce draft :

- définition de \(C_t\) ;
- métrique / scaling / standardisation de \(S_2\) et \(S_3\) ;
- invariances souhaitées de la distance ; candidat non accepté
  \(\log RV\) (§9.13.3) ;
- convention pour \(D\) / \(Q\) aux singularités (zéros) — **pas**
  d'\(\varepsilon\) choisi ici ;
- extra \(\max\lvert r\rvert\) (non retenu, OPEN) ;
- définition finale de \(X_t\) ;
- valeur finale de \(W\), \(h\), \(k\) (héritages 20 / 10 / 50 =
  candidats anti-retuning, non décidés) ;
- règle de partage \(S_2\) si \(W\neq 20\) ;
- source de données ; instrument / univers de réplication ; holdout ;
- gates statistiques ; seuil de « stress » ;
- acceptation finale du CRPS (seulement `ACCEPTABLE CANDIDATE`) ;
- architecture Market-State Engine.

**Accepté (représentation seulement) :**

- \(S_1=[RV]\) ; \(S_2=[RV,D]\) ; \(S_3=[RV,Q]\) sur rendements bruts
  — statut `REPRESENTATION ACCEPTED / METRIC UNRESOLVED` ;
- H2a / H2b / H2c comme famille d'attaques distinctes.

**Documentés comme candidats**, non décisions :

- observable \(V_{t,h}\) ;
- information supplémentaire = meilleur score de \(\widehat F\) vs \(S\)
  (CRPS si retenu) ;
- H1-v0.2 ;
- rétrogradation de `H_vol` / `H_shape`.

---

## 17. Before I02 can open

Décisions **humaines**. Tant que la dernière case n'est pas cochée :

**I02 = NOT OPENED.**

- [ ] Hypothèse finale approuvée (H1-v0.2 reste une candidate)
- [ ] Condition de marché \(C_t\) définie ex ante (§14)
- [x] Représentations adversaires \(S_1/S_2/S_3\) **acceptées**
      (`REPRESENTATION ACCEPTED` ; NEW)
- [ ] Métrique / scaling / distance sur \(S\) **résolus**
      (`METRIC UNRESOLVED`)
- [ ] Observable futur **approuvé** (\(V_{t,h}\) est seulement candidat)
- [ ] Score probabiliste **approuvé** (CRPS = acceptable candidate)
- [ ] Rôle de `H_shape` défini (témoin / mesure / non-gate)
- [ ] Kill criteria approuvés
- [ ] Stratégie de données indépendantes / réplication définie
- [ ] Risque de data snooping documenté (héritage I01 + holdout + score)
- [ ] Protocole de gel avant premier résultat défini
- [ ] Décision explicite **OPEN I02**

L'acceptation des représentations \(S\) **n'ouvre pas** I02.

---

## 18. Revue de cohérence (auteur)

| Contrôle | Statut |
|----------|--------|
| Aucun chiffre nouveau calculé | oui |
| Aucune donnée nouvelle téléchargée | oui |
| CRPS non calculé ; aucune métrique testée sur données | oui |
| \(C_t\) / seuil de stress non définis | oui |
| Représentations \(S\) acceptées ; métrique unresolved | oui |
| Aucune corrélation / performance \(S\) calculée sur SPY | oui |
| Aucun \(\varepsilon\), aucune distance, aucun scaling choisi | oui |
| \(W/k/h\) non optimisés | oui |
| Aucun code / test expérimental I02 | oui |
| Pas de `protocol.md` I02 | oui |
| DR-003 / DR-005 non modifiés | oui |
| Aucun fournisseur contacté | oui |
| I01 reste CLOSED | oui (`116374b`) |
| I02 reste NOT OPENED | oui |

---

## Références (lecture, pas autorité de validation)

- [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
- E01–E04 ; [hypothesis.md](../I01/hypothesis.md) ; [protocol.md](../I01/protocol.md)
- [DR-007](../../docs/adr/DR-007-exploratory-vs-confirmatory-data.md)
- [DR-008](../../docs/adr/DR-008-i01-e01-exploratory-source.md)
- CRPS : proper scoring rule pour lois réelles (littérature ; pas un
  calcul sur SPY)
