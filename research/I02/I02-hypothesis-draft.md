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

**État \(Z_t\) :** famille **A** ; \(\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\)
`ACCEPTED` ; \(W_{RV}:=W_X\) `ACCEPTED` (§14C.9) —
**comparability coupling**, pas identité conceptuelle ; \(m_Z\) OPEN
et **distinct** ; stride 1 = baseline candidate non acceptée ;
formule \(Z_t\) **incomplète**.
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
- pas une acceptation de CRPS, de \(h\), d'une **distance complète**,
  de **poids**, ni de \(C_t\) ;
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
Distance et scaling de \(S\) : ensembles de robustesse §9.16
`ACCEPTED` ; détail d'opérateur kNN / agrégation \(L\)+forme :
protocole futur. Composition informationnelle : **acceptée** (§9).

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

**Prochaine étape documentaire (hors mandat) :** propriétés
d'admissibilité d'un \(m_Z\), plutôt qu'une valeur à tuner.

### 14C.10 Cohérence (post-décision)

| Contrôle | OK |
|----------|-----|
| Couplage = comparability, ≠ identité conceptuelle | oui |
| \(m_Z\) non posé égal à \(W_X\) | oui |
| Overlap / empan §14C.1–2 inchangés | oui |
| Pas de valeur numérique ; stride non accepté | oui |
| I02 NOT OPENED | oui |

---

## 15. Market-State / Regime Engine

**Aucun contrat empirique n'est dérivé d'I01.** Aucune architecture
modifiée. I02, s'il est autorisé plus tard, pourra ou non informer
ce contrat. \(Z_t\) **n'est pas** un Market-State Engine.

---

## 16. OPEN QUESTION — liste exacte

Ne pas résoudre dans ce draft :

- **\(m_Z\)** — horizon distinct ; propriétés d'admissibilité puis
  éventuelle valeur (pas \(m_Z=W_X\) implicite) ;
- valeur numérique de \(W_X\) (donc de \(W_{RV}\)) ;
- acceptation formelle rolling / stride 1 ;
- formule complète \(Z_t\) ;
- empan / redondance temporelle du **pool** de voisins ;
- définition protocolaire du « désaccord matériel » sous §9.16 ;
- détail d'agrégation \(L\)+forme dans l'opérateur kNN ;
- Spearman / CRPS / inférence dépendance temporelle ;
- z-score / rangs / CDF / Mahalanobis / poids appris ;
- singularités (\(RV=0\), …) — pas d'\(\varepsilon\) ;
- \(h\), \(k\) ; holdout ; Market-State Engine.

**CLOSED :**

- doctrine §9.16 ; \(\mathcal{M}_{S2}\), \(\mathcal{M}_{S3}\) ;
- famille A ; \(\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\) ;
- MAD REJECT ; MeanAD non retenue ; \(E\) = alternatif ;
- **\(W_{RV}:=W_X\)** `ACCEPTED` (§14C.9) —
  `METHODOLOGICAL COMPARABILITY COUPLING` ;
- framing \(C_t\) binaire stress.

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
- [ ] \(m_Z\) (propriétés d'admissibilité / valeur) ; stride 1 ;
      valeur \(W_X\) ; formule \(Z_t\) éventuellement acceptée
- [x] Représentations \(S_1/S_2/S_3\) **acceptées**
- [x] Invariant multiplicatif **accepté**
- [ ] Observable futur **approuvé** (\(V_{t,h}\) candidat)
- [ ] Score probabiliste **approuvé** (CRPS = acceptable candidate)
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
| Aucun chiffre / donnée / CRPS | oui |
| \(S_1/S_2/S_3\) / §9.16 inchangés | oui |
| Famille A = primary semantic candidate (§14A.12) | oui |
| \(\operatorname{Disp}=\mathrm{Std}_{\mathrm{pop}}\) `ACCEPTED` | oui |
| \(W_{RV}:=W_X\) comparability coupling `ACCEPTED` | oui |
| \(m_Z\) indépendant OPEN ; `NO Z_t ACCEPTED` | oui |
| I01 CLOSED ; I02 NOT OPENED | oui |

---

## Références (lecture, pas autorité de validation)

- [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
- E01–E04 ; [hypothesis.md](../I01/hypothesis.md) ; [protocol.md](../I01/protocol.md)
- [DR-007](../../docs/adr/DR-007-exploratory-vs-confirmatory-data.md)
- [DR-008](../../docs/adr/DR-008-i01-e01-exploratory-source.md)
- CRPS : proper scoring rule pour lois réelles (littérature ; pas un
  calcul sur SPY)
