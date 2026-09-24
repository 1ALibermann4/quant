# I02 â€” Brouillon d'hypothÃ¨se (prÃ©-investigation)

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
> **Draft v0.6 Q vs Ï† review :** `8b652f7`
> **Draft v0.7 metric robustness :** `2a92da7`
> **Calculs dans ce document :** aucun
> **Classe donnÃ©es I01 :** UNQUALIFIED (DR-007 / DR-008)

Ce fichier **ne signifie pas** que I02 est ouvert.
Aucun protocole, aucun run, aucun code expÃ©rimental I02 n'est autorisÃ©.

$$
\text{observations I01} \neq \text{preuve de cette hypothÃ¨se candidate}
$$

E01â€“E04 ont **gÃ©nÃ©rÃ©** la piste. Ils ne peuvent pas la valider.

**Statut des adversaires \(S\) :**

```text
REPRESENTATION ACCEPTED / METRIC UNRESOLVED
```

\(S_1=[RV]\), \(S_2=[RV,D]\), \(S_3=[RV,Q]\) : nature informationnelle
**acceptÃ©e** (`c85476c`).

**Invariant de niveau :** proximitÃ© multiplicative (Â§9.14) â€” acceptÃ©.
**Forme \(S_3\) :** pas de Â« vraie gÃ©omÃ©trie Â» dÃ©duite (Â§9.15) ;
doctrine candidat Â§9.16 â€” incertitude mÃ©trique â†’ robustesse
prÃ©enregistrÃ©e (pas chart suivant). **\(d_{S2}^{(E)}\) :**
`ACCEPTABLE CANDIDATE`, non acceptÃ©. **Avant \(C_t\).**
I02 reste `NOT OPENED`.

---

## 0. Ce que ce draft n'est pas

- pas un SCI-PASS, pas un SCI-FAIL ;
- pas une recommandation de confirmer I01 ;
- pas une ouverture de DR-003 / DR-005 ;
- pas E05 ;
- pas un contrat empirique pour un Market-State / Regime Engine ;
- pas un choix de seuil, de source, ni d'instrument ;
- pas une acceptation de CRPS, de \(h\), d'une **distance complÃ¨te**,
  de **poids**, ni de \(C_t\) ;
- pas une ouverture d'I02 ;
- pas un remplacement des reprÃ©sentations \(S\) par les charts \(S^\star\).

---

## 1. Faits I01 (observations, pas un rÃ©cit)

Source : [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
et rapports E01â€“E04. Chiffres **dÃ©jÃ  publiÃ©s**. Aucun recalcul.

### A. E01

Sur le sandbox `SPY / yfinance 1.6.0 / daily` (UNQUALIFIED), les voisins L2
prÃ©sentaient **en moyenne** des futurs plus homogÃ¨nes que B0 :

`H_raw` âˆ’13,7 % ; `H_vol` âˆ’54,0 % ; `H_shape` âˆ’0,21 %.

Couverture livrÃ©e : 1993-01-29 â†’ 2026-09-23 ; `T_eval` = 8038
(1994-09-30 â†’ 2026-09-09).

Ceci n'Ã©tait pas une preuve de H-I01.

### B. E02

L'effet vs B0 Ã©tait **principalement portÃ© par `H_vol`**. `H_shape` Ã©tait
pratiquement plat. `Î”_raw` suivait `Î”_vol` (corr. 0,762), pas `Î”_shape`
(0,009).

### C. E03

Le phÃ©nomÃ¨ne L2 n'Ã©tait **pas** expliquÃ© par un matching simple du niveau
de volatilitÃ© passÃ©e `rv_W`. Ã‰cart `|Î” rv_W|` des voisins L2 : 95,7 %
d'un candidat typique de `L_t` ; le tÃ©moin `rv_W` : 7,7 %. Le contrÃ´le
rÃ©cupÃ©rait `H_vol` vs B0 (âˆ’41,9 %) mais presque pas `H_raw` (âˆ’2,2 % vs
âˆ’13,7 % pour L2).

### D. E04

Face au contrÃ´le `rv_W`, \(D_t = H^{rv}(t)-H^{L2}(t)\) Ã©tait fortement
asymÃ©trique sur `D_vol` :

- mÃ©diane **nÃ©gative** (âˆ’1.52e-5) ; moyenne positive (+4.09e-5) ;
- `D_vol > 0` sur **42,8 %** des dates ;
- **1 %** des dates portaient **77 %** de `âˆ‘ D_vol` (asymÃ©trie +7,44) ;
- concentration importante autour de **2008, 2009, 2020** ;
- dÃ©cennie prÃ©fixÃ©e **2010â€“2019** : moyenne `D_vol` (et `D_raw`) **nÃ©gative** ;
- relation **descriptive** avec les tertiles Ã  effectif Ã©gal de `rv_W`
  Ã©levÃ© (coupe non optimisÃ©e, pas un seuil).

Aucune de ces lignes n'est une conclusion causale.

### Distinctions Ã  prÃ©server

```text
observation conditionnelle
    â‰   rÃ©gime identifiÃ©
    â‰   mÃ©canisme causal
    â‰   capacitÃ© prÃ©dictive confirmÃ©e
```

Formulation acceptable :

> E04 a identifiÃ© une **concentration conditionnelle** du phÃ©nomÃ¨ne dans
> certaines pÃ©riodes / certains Ã©tats observÃ©s. Le mÃ©canisme et sa
> gÃ©nÃ©ralisabilitÃ© restent inconnus.

Formulations **interdites** comme faits : Â« L2 fonctionne en rÃ©gime de
stress Â» ; Â« un rÃ©gime de crise a Ã©tÃ© identifiÃ© Â» ; Â« la gÃ©omÃ©trie
prÃ©dit la volatilitÃ© en pÃ©riode de stress Â».

Le mot **rÃ©gime** reste descriptif et provisoire.

---

## 2. I01 vs I02 candidate â€” deux questions distinctes

I01 demandait essentiellement :

$$
X_s \approx X_t \quad\Longrightarrow\quad Y_s \approx Y_t
$$

c'est-Ã -dire : **les futurs associÃ©s aux voisins sont-ils collectivement
plus homogÃ¨nes** (surtout `H_raw` / `H_vol` vs B0) ?

I02 candidate demanderait :

> La structure du passÃ© apporte-t-elle de l'information sur la
> **distribution de la volatilitÃ© future rÃ©ellement observÃ©e**, au-delÃ 
> de rÃ©sumÃ©s simples du passÃ© ?

On ne cherche plus Ã  prÃ©dire la **trajectoire** \(Y\). On cherche une
**propriÃ©tÃ© scalaire** de \(Y\), puis une **loi prÃ©dictive** de cette
propriÃ©tÃ©. `H_shape` reste un garde-fou sÃ©mantique, pas un objectif
rÃ©introduit.

Ces questions **ne sont pas Ã©quivalentes**.

Exemple obligatoire : un voisinage peut avoir un `H_vol` trÃ¨s bas
(tous les voisins Â« prÃ©disent Â» une faible volatilitÃ©) et Ãªtre
**entiÃ¨rement faux** si \(V_{t,h}\) rÃ©alisÃ© est Ã©levÃ©. HomogÃ©nÃ©itÃ© entre
voisins â‰  qualitÃ© de la prÃ©vision du futur de \(t\).

Un voisinage peut Ãªtre :

```text
trÃ¨s homogÃ¨ne mais complÃ¨tement faux
```

**Conclusion :** `H_vol` ne doit pas automatiquement devenir l'observable
principal d'I02. C'est une propriÃ©tÃ© **d'un ensemble de voisins**, pas
une variable attachÃ©e Ã  \(t\). H3 porte prÃ©cisÃ©ment sur le comportement
de cette mÃ©trique dans les queues.

---

## 3. Variable future candidate \(V_{t,h}\)

**Proposition Ã  Ã©valuer, non figÃ©e.**

$$
V_{t,h}
=
\sqrt{
\frac{1}{h}
\sum_{j=1}^{h}
r_{t+j}^{2}
}
$$

InterprÃ©tation : amplitude / volatilitÃ© rÃ©alisÃ©e sur les \(h\) sÃ©ances
**suivant** \(t\) (aprÃ¨s clÃ´ture de \(t\) ; \(Y\) commence Ã  \(t+1\)).

PropriÃ©tÃ©s voulues :

- attachÃ©e Ã  **chaque** date \(t\), pas Ã  un voisinage ;
- existe **indÃ©pendamment** de L2 et de `H_vol` ;
- ne prÃ©juge pas de la mÃ©thode de prÃ©diction ;
- \(V_{t,h}\geq 0\).

La variante sans \(1/h\) n'en diffÃ¨re que par la constante \(\sqrt{h}\)
si \(h\) est fixÃ©. La forme ci-dessus est prÃ©fÃ©rÃ©e pour la lecture
(Â« amplitude par sÃ©ance Â», au sens RMS).

\(h\) **n'est pas figÃ©**. Voir Â§3.1.

### 3.1 HÃ©riter \(h=10\) d'I01 ? â€” pour et contre

| Pour | Contre |
|------|--------|
| I02 est **dÃ©rivÃ©e** d'une observation gÃ©nÃ©rÃ©e Ã  \(h=10\). Conserver l'horizon Ã©vite de chercher l'horizon qui maximise le nouvel effet. | Reprendre 10 par habitude n'est pas neutre (OPEN du draft v0.1). |
| Justification explicite possible : *on refuse d'optimiser \(h\)*, pas Â« 10 est optimal Â». | Un autre \(h\) prÃ©-annoncÃ© (5, 21, â€¦) serait aussi non optimisÃ©, et n'hÃ©riterait pas du gÃ©nÃ©rateur. |
| Alignement avec \(Y_t^{(h)}\) dÃ©jÃ  dÃ©fini (DEC-04, protocole I01). | Si le phÃ©nomÃ¨ne I01 est spÃ©cifique Ã  10 sÃ©ances, I02 le reproduit par construction d'horizon. |

Ã‰tat : **OPEN QUESTION**. Candidat documentÃ© : hÃ©riter \(h=10\) *parce
qu'on refuse de l'optimiser*. MÃªme logique possible plus tard pour
\(W=20\), sous rÃ©serve de la dÃ©cision sur \(X_t\).

---

## 4. Formulation informationnelle (pas encore opÃ©rationnelle)

Objets :

- \(X_t\in\mathbb{R}^{W}\) â€” structure multivariÃ©e du passÃ© (**dÃ©finition
  finale OPEN**) ;
- \(S_t\) â€” famille de rÃ©sumÃ©s simples (**candidats \(S_1,S_2,S_3\)
  documentÃ©s, Â§8â€“9 ; mÃ©trique / scaling OPEN**) ;
- \(C_t\) â€” condition de marchÃ© (**non dÃ©finie**, Â§14) ;
- \(V_{t,h}\) â€” observable futur **candidat**.

Question :

$$
\mathcal{L}(V_{t,h}\mid X_t,S_t,C_t=1)
\quad\text{versus}\quad
\mathcal{L}(V_{t,h}\mid S_t,C_t=1)
$$

La connaissance de \(X_t\) apporte-t-elle une information **incrÃ©mentale**
sur \(V_{t,h}\), conditionnellement Ã  \(S_t\) et \(C_t\) ?

Un \(\neq\) statistique minuscule ne suffirait pas. Le sens *utile* d'une
information incrÃ©mentale est renvoyÃ© au score prÃ©dictif (Â§6), **s'il**
est acceptÃ©.

Cette Ã©criture **n'est pas** encore un protocole.

---

## 5. Distributions empiriques par voisinage (mÃ©canisme candidat)

**Aucun \(k\) nouveau. Aucun calcul. Aucune implÃ©mentation.**
Distance et scaling de \(S\) : **OPEN** (`METRIC UNRESOLVED`).
Composition informationnelle : **acceptÃ©e** (Â§9).

Pour une requÃªte \(t\), candidat :

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

Ce sont des **prÃ©visions probabilistes** candidates de \(V_{t,h}\),
construites uniquement Ã  partir de \(V_{s,h}\) **historiques** des
voisins (sÃ©lection = fonction de \(X\) ou de \(S\), pas de \(V_{t,h}\)
â€” mÃªme discipline AF-08 qu'I01).

Le voisinage reste l'**opÃ©rateur expÃ©rimental**. On n'ouvre pas une
course XGBoost(\(X\)) vs forÃªt(\(rv\)).

B0 (tirage dans \(\mathcal{L}_t\)) peut fournir une troisiÃ¨me \(\widehat F\)
de rÃ©fÃ©rence. Il n'est pas l'adversaire suffisant de H1.

---

## 6. CRPS â€” mÃ©trique principale **candidate**

**Pas calculÃ©. Pas un gate.**

$$
\operatorname{CRPS}(F,y)
=
\int_{-\infty}^{+\infty}
\bigl(F(z)-\mathbf{1}\{y\le z\}\bigr)^{2}\,dz
$$

Convention : **plus faible = meilleure** prÃ©vision probabiliste.

Candidats opÃ©rationnels :

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

\(D^{\mathrm{CRPS}}_t>0\) signifierait : ce jour-lÃ , \(\widehat F_X\) a
mieux dÃ©crit \(V_{t,h}\) observÃ© que \(\widehat F_S\).

QuantitÃ© centrale **candidate** (si CRPS et \(C_t\) Ã©taient un jour
retenus) :

$$
\mathbb{E}\bigl[D^{\mathrm{CRPS}}_t \bigm| C_t=1\bigr]
$$

sur information indÃ©pendante. **Aucun seuil. Aucun calcul.**

Pour un ensemble fini de \(k\) atomes, le CRPS a une forme close
classique (moyenne des Ã©carts Ã  \(y\) moins la demi-dispersion interne
de l'ensemble). Le mentionner n'autorise pas Ã  l'implÃ©menter ici.

### 6.1 CRPS adversarial review

Objectif : CRPS peut-il devenir mÃ©trique confirmatoire principale
**sans** ouvrir une sÃ©lection post hoc ? Aucune alternative n'est
testÃ©e sur les donnÃ©es.

| Point | Lecture |
|-------|---------|
| Variable continue \(\geq 0\) | CRPS est dÃ©fini pour toute loi rÃ©elle. Le support \([0,\infty)\) n'est pas imposÃ© par l'intÃ©grale ; l'ECDF empirique est portÃ©e par des \(V_{s,h}\geq 0\), donc le support effectif est correct. Pas un motif de rejet. |
| Calibration | Proper scoring rule : l'espÃ©rance est minimisÃ©e par la vraie loi. Une ECDF mal calibrÃ©e est pÃ©nalisÃ©e. |
| Sharpness / dispersion | PÃ©nalise Ã  la fois le biais et l'excÃ¨s de largeur. Une loi trop plate (contrÃ´le Â« 0.8 â€¦ 6.1 Â») est battue par une loi concentrÃ©e autour de \(y\), *si* \(y\) tombe dedans. |
| Ensemble de \(k\) points | Avec \(k\) petit, \(\widehat F\) est en escalier. Le CRPS reste bien dÃ©fini ; la variance du score est plus grande. HÃ©riter \(k=50\) (OPEN) n'est pas anodin : trop peu d'atomes â‡’ loi rugueuse. Ce n'est pas une raison de changer \(k\) aprÃ¨s un chiffre. |
| Queues | Moins dominÃ© par les queues que le log-score (qui explose si \(y\) sort d'une densitÃ© paramÃ©trique). Inversement, un miss extrÃªme est moins punitif qu'en vraisemblance. Compatible avec H3 : il faudra regarder si \(\mathbb{E}[D\mid C=1]\) est une moyenne de queue. |
| Ã‰chelle de \(V\) | Le CRPS est **dans les unitÃ©s de \(V\)**. Les jours Ã  \(V\) Ã©levÃ© pÃ¨sent plus sur la moyenne. Si \(C_t=1\) sÃ©lectionne des Ã©tats dÃ©jÃ  volatils, \(\mathbb{E}[D\mid C=1]\) peut Ãªtre dominÃ© par quelques \(V\) grands â€” cousin d'H3. Une normalisation (CRPS / \(V\), rang, â€¦) **n'est pas choisie** ici : la choisir aprÃ¨s un run serait du snooping. Risque **documentÃ©**, pas un motif de tester une autre mÃ©trique maintenant. |
| vs erreur absolue ponctuelle | MAE de la moyenne ou de la mÃ©diane d'ensemble = cas dÃ©gÃ©nÃ©rÃ© (prÃ©vision d'un point). Plus faible philosophiquement : on perd calibration/sharpness. Utile comme **diagnostic**, pas comme remplaÃ§ant silencieux. |
| vs log-score | Exige une densitÃ©. Imposer une loi paramÃ©trique sur \(k\) voisins ajoute un modÃ¨le. Contredit Â« pas de ML / pas de loi inventÃ©e Â». Ã‰cartÃ© comme primaire. |
| vs calibration + sharpness sÃ©parÃ©es | Plus riches, plus de degrÃ©s de libertÃ© â‡’ plus de tentation post hoc. Le CRPS les **combine** en une proper rule. Les sÃ©parer reste un diagnostic possible, pas une batterie de gates. |

**Verdict documentaire sur le CRPS :** `ACCEPTABLE CANDIDATE`.

Pas `ACCEPTÃ‰`. Pas `REJECT`. Les rÃ©serves d'Ã©chelle et de queue
doivent rester visibles si une dÃ©cision humaine le retient. Aucun
gate numÃ©rique.

---

## 7. H1 candidate v0.2

> **H1-I02 candidate v0.2 â€” information gÃ©omÃ©trique conditionnelle**
>
> Sous une condition de marchÃ© \(C_t\) causale, dÃ©finie ex ante et
> observable aprÃ¨s la clÃ´ture de \(t\), un voisinage historique
> construit Ã  partir de la structure multivariÃ©e de \(X_t\) fournit une
> distribution prÃ©dictive de la volatilitÃ© rÃ©alisÃ©e future \(V_{t,h}\)
> contenant une information **hors Ã©chantillon** supÃ©rieure Ã  celle
> obtenue Ã  partir de voisinages construits sur des rÃ©sumÃ©s simples
> prÃ©-enregistrÃ©s \(S\) (famille candidate \(S_1,S_2,S_3\), Â§9).

Si CRPS Ã©tait retenu plus tard, une opÃ©rationnalisation **possible**
serait :

$$
\mathbb{E}\bigl[\operatorname{CRPS}_X(t)-\operatorname{CRPS}_S(t) \bigm| C_t=1\bigr]
< 0
$$

sur l'information indÃ©pendante prÃ©vue par un protocole **non Ã©crit**.

$$
\text{H1} \neq \text{Â« L2 bat B0 Â»}
$$

**HypothÃ¨se candidate.** Aucun gate.

---

## 8. Concurrentes â€” H2 devient une famille

### H1 â€” Structure gÃ©omÃ©trique conditionnelle

Voir Â§7. Non Ã©tablie. H1 n'est intÃ©ressante que si \(X\) survit Ã  des
adversaires simples **raisonnables** des familles ci-dessous.

### H2 â€” Explications simples (plus seulement Â« `rv_W` Â»)

H2 ne signifie plus : Â« `rv_W` explique peut-Ãªtre L2. Â»

| | Explication | Adversaire candidat |
|--|--|--|
| **H2a â€” LEVEL** | Le niveau de volatilitÃ© rÃ©cente suffit. | \(S_1\) |
| **H2b â€” VOL DYNAMICS** | Niveau + dynamique rÃ©cente de vol suffisent. | \(S_2\) |
| **H2c â€” AMPLITUDE DISTRIBUTION** | Les propriÃ©tÃ©s **sans ordre** de la distribution d'amplitudes suffisent. | \(S_3\) |

`rv_W` / \(S_1\) a dÃ©jÃ  Ã©tÃ© insuffisant *pour `H_vol`* (E03). Cela ne
dit pas qu'un \(S_2\) ou \(S_3\) Ã©choue pour \(\widehat F(V)\).

### H3 â€” Queue / mÃ©trique

Le gain de score (ou l'ancien `H_vol`) est portÃ© par des Ã©pisodes
extrÃªmes / par le comportement de la mÃ©trique. Pas d'information
gÃ©nÃ©ralisable.

### H4 â€” Absence de structure reproductible

Pas de reproduction sur information indÃ©pendante. Issue normale.

---

## 9. Batterie d'adversaires \(S_1,S_2,S_3\)

**Statut :** `REPRESENTATION ACCEPTED / METRIC UNRESOLVED`
(acceptation humaine aprÃ¨s revue Â§9.13 @ `5980bc8`).

Ce qui est acceptÃ© : la **nature informationnelle** des trois
adversaires et leurs coordonnÃ©es NEW. Ce qui **ne** l'est **pas** :
distance, scaling, \(W\), partage 10+10, convention aux singularitÃ©s,
\(C_t\).

Les redondances Ã©liminÃ©es sont **algÃ©briques**. Aucun calcul sur
donnÃ©es pour les choisir.

```text
B0     hasard admissible / rÃ©fÃ©rence faible
S1     niveau de volatilitÃ©
S2     niveau + dynamique de volatilitÃ©
S3     distribution d'amplitude sans ordre
X      sÃ©quence multivariÃ©e ordonnÃ©e
```

**Ce n'est pas** \(S_1\subset S_2\subset S_3\subset X\).

\(S_2\) et \(S_3\) sont des **adversaires Ã  explications distinctes**,
pas des marches d'un mÃªme modÃ¨le. Ils **partagent** la coordonnÃ©e de
niveau \(RV_t\) (pas des vecteurs orthogonaux, pas une indÃ©pendance
statistique). \(S_2\) conserve un ordre **grossier** (demi-fenÃªtres).
\(S_3\) dÃ©truit volontairement l'ordre et dÃ©crit davantage la forme
des amplitudes.

Interdit : dire Â« les axes sont orthogonaux Â» sauf dÃ©monstration
stricte. PrÃ©fÃ©rer : **sÃ©paration conceptuelle** / **reparamÃ©trisation
niveau / forme** (ou niveau / dynamique).

H1 **ne** se soutient **pas** parce que \(X\) bat B0.

### 9.1 Domaine : rendements bruts, pas \(X\) standardisÃ©

Tous les \(S\) sont des fonctions de

\[
(r_{t-W+1},\ldots,r_t)
\]

information \(\mathcal{O}_{\le t}\) seulement. **Pas** des coordonnÃ©es
de \(X\) standardisÃ© (\(M=252\)). Sinon \(S\) devient une projection
de \(X\) : un mini-\(X\), et le contrÃ´le n'est plus une explication
indÃ©pendante.

\(W\) n'est **pas** figÃ©. Les formules ci-dessous sont pour une
fenÃªtre de longueur \(W\) ; le partage 10+10 de \(S_2\) n'est
dÃ©fini que **si** \(W=20\) est ultÃ©rieurement hÃ©ritÃ©.

### 9.2 Fausses dimensions

\[
RV_t=\sqrt{\frac1W\sum_{i=0}^{W-1}r_{t-i}^{2}},
\qquad
E_t=\sum_{i=0}^{W-1}r_{t-i}^{2}
=W\,RV_t^{2}
\]

\(RV\) et \(E\) **ne** sont **pas** deux informations. Interdit :
prÃ©senter \([RV,E]\) comme un contrÃ´le plus riche.

\[
MA_t=\frac1W\sum_{i=0}^{W-1}|r_{t-i}|,
\qquad
A_t=\sum_{i=0}^{W-1}|r_{t-i}|
=W\,MA_t
\]

\(A\) et \(MA\) sont la mÃªme information. Un seul descripteur.

### 9.3 Relation \(RV\) / \(MA\) (famille S3, pas S2)

InÃ©galitÃ© RMSâ€“AM sur les \(|r|\) :

\[
MA_t\le RV_t
\]

Ã‰galitÃ© ssi toutes les amplitudes \(|r|\) de la fenÃªtre sont Ã©gales.

Variance **population** sur les \(W\) observations :

\[
\operatorname{Var}_{\mathrm{win}}(|r|)
=\frac1W\sum_{i=0}^{W-1}(|r_{t-i}|-MA_t)^{2}
=RV_t^{2}-MA_t^{2}
\]

Donc \([RV,MA]\) = niveau d'amplitude + hÃ©tÃ©rogÃ©nÃ©itÃ© des amplitudes,
**sans ordre**. Appartient Ã  **S3**, pas Ã  S2. Ne pas mettre \(MA\)
dans \(S_2\).

### 9.4 \(S_1\) â€” niveau (H2a)

\[
S^{(1)}_t=[RV_t]
\]

Niveau rÃ©cent de volatilitÃ© / amplitude quadratique. AttachÃ© Ã  \(t\),
indÃ©pendant du voisinage. Conceptuellement le tÃ©moin simple d'E03.

Question : \(X\) apporte-t-il quelque chose **au-delÃ ** du niveau ?

### 9.5 \(S_2\) â€” niveau + dynamique (H2b)

Question testÃ©e : L2 ne reconnaÃ®t peut-Ãªtre que le niveau et le fait
que la vol **monte ou descend**.

Si \(W=20\) est hÃ©ritÃ© : division **Ã©gale** 10+10 (anti-retuning :
on refuse 5/15, 8/12, â€¦). Ce n'est pas une preuve que 10+10 est
optimal. Si \(W\neq 20\) : rÃ¨gle de partage **OPEN**.

FenÃªtre ordonnÃ©e dans le temps : \(r_{t-W+1},\ldots,r_t\).
**Early** = premiÃ¨re moitiÃ© (plus ancienne) ; **late** = seconde
(plus rÃ©cente, inclut \(r_t\)).

\[
RV^{\mathrm{early}\,2}+RV^{\mathrm{late}\,2}=2\,RV_t^{2}
\]

(moitiÃ©s de mÃªme longueur). Le triplet \([RV,\,RV^{early},\,RV^{late}]\)
est redondant.

**ParamÃ©trage OLD (rÃ©fÃ©rence algÃ©brique / secours aux singularitÃ©s) :**

\[
S^{(2)}_{\mathrm{old}}=[RV_t,\;\Delta RV_t],
\qquad
\Delta RV_t=RV^{\mathrm{late}}_t-RV^{\mathrm{early}}_t
\]

Sous positivitÃ© et la relation quadratique, \((RV,\Delta RV)\)
permet de retrouver les deux demi-volatilitÃ©s (Ã©quation du second
degrÃ© ; racine physique \(RV^{early},RV^{late}\ge 0\), admissible
dÃ¨s que \(|\Delta RV|\le 2\,RV\)).

**ParamÃ©trage NEW â€” `REPRESENTATION ACCEPTED` (mÃ©trique unresolved) :**

\[
S^{(2)}_t=[RV_t,\;D_t],
\qquad
D_t=\log\!\left(\frac{RV^{\mathrm{late}}_t}{RV^{\mathrm{early}}_t}\right)
\]

mÃªme information H2b (niveau + dynamique), dynamique en **ratio**.
Revue Â§9.13 : `PREFER NEW` â†’ acceptation humaine de la reprÃ©sentation.
Domaines / singularitÃ©s : Â§9.13.1. **Pas** d'\(\varepsilon\).

**Pas de \(MA\) dans \(S_2\).** CiblÃ© : niveau + dynamique.

### 9.6 \(S_3\) â€” distribution sans ordre (H2c)

Question testÃ©e : le sac d'amplitudes suffit-il, sans sÃ©quence ?

**ParamÃ©trage OLD (rÃ©fÃ©rence algÃ©brique) :**

\[
S^{(3)}_{\mathrm{old}}=[RV_t,\;MA_t]
\]

**ParamÃ©trage NEW â€” `REPRESENTATION ACCEPTED` (mÃ©trique unresolved) :**

\[
S^{(3)}_t=[RV_t,\;Q_t],
\qquad
Q_t=\frac{MA_t}{RV_t}\quad(RV_t>0)
\]

Aucun ordre. **Pas de \(\Delta RV\) ni \(D\).** **Pas** un sur-ensemble
de \(S_2\). Revue Â§9.13 : `PREFER NEW` â†’ acceptation humaine.
Domaines / singularitÃ©s : Â§9.13.2.

### 9.7 Extra de queue â€” non retenu

\(\max_i|r_{t-i}|\) : **OPEN QUESTION**, pas une composante.
Pourrait tester une observation extrÃªme rÃ©cente. L'ajouter maintenant
fabriquerait progressivement un mini-\(X\). DÃ©cision sÃ©parÃ©e avant
ouverture, pas ici.

### 9.8 Pas de drift dans \(S_3\)

Pas de \(\sum r\) ni de rendement cumulÃ© signÃ©. \(S_3\) est un
adversaire **volatilitÃ© / amplitude**. Un contrÃ´le de drift /
momentum serait une **autre** hypothÃ¨se, Ã  nommer sÃ©parÃ©ment.

### 9.9 Distance / normalisation â€” OPEN (partiellement)

**AcceptÃ© (Â§9.14) :** l'Ã©cart de **niveau** doit Ãªtre multiplicatif
(\(|\log RV_a-\log RV_b|\) sur \(RV>0\)).

**Non acceptÃ© :** forme complÃ¨te de \(d\) ; pondÃ©ration entre axes ;
Euclidienne / \(L_1\) ; z-score ; rangs ; CDF ; Mahalanobis ;
standardisation historique.

Un kNN euclidien brut sur \([RV,D]\), \([L,D]\), \([L,Q]\), etc. reste
un choix scientifique **non** autorisÃ© par l'invariant seul.

\[
\text{REPRESENTATION} \neq \text{METRIC CHART}
\]

Voir Â§9.14.

### 9.10 Interdiction de snooping de conception

**Ne pas** calculer sur SPY : \(\operatorname{corr}(RV,MA)\) ;
performance \(S_1/S_2/S_3\) ; loi de \(\Delta RV\) ; Â« meilleur Â»
early/late ; utilitÃ© de \(\max|r|\) ; Â« meilleur Â» scaling ou
distance. Ces choix se dÃ©cident **ex ante**, pas sur le sandbox I01.

### 9.11 Matrice d'interprÃ©tation (qualitative, sans rÃ©sultat)

| Cas | Lecture candidate |
|-----|-------------------|
| **A.** \(X\) bat B0 seulement | Preuve insuffisante d'une information gÃ©omÃ©trique spÃ©cifique. |
| **B.** \(X\) bat \(S_1\), pas \(S_2\) | La dynamique rÃ©cente de vol **peut** suffire (H2b). |
| **C.** \(X\) bat \(S_2\), pas \(S_3\) | La distribution / hÃ©tÃ©rogÃ©nÃ©itÃ© d'amplitudes **peut** suffire ; l'ordre complet n'est pas nÃ©cessaire (H2c). |
| **D.** \(X\) bat \(S_2\) **et** \(S_3\) | La sÃ©quence multivariÃ©e **devient une question sÃ©rieuse**. |

Le cas D **ne prouve pas** que Â« l'ordre compte Â». Il dit seulement
que \(S_2\) et \(S_3\) **n'ont pas suffi**. D'autres explications
restent possibles (autre \(S\), mÃ©trique, queues, \(C_t\), H3, H4).

### 9.12 Revue adversariale de la batterie

| Risque | Statut |
|--------|--------|
| Redondance \(E\leftrightarrow RV\), \(A\leftrightarrow MA\) | Ã‰liminÃ©e algÃ©briquement. |
| \([RV,MA]\) mis dans \(S_2\) | Interdit ; famille S3. |
| Triplet early/late/\(RV\) | RÃ©duit Ã  \((RV,\Delta RV)\). |
| Langage \(S_1\subset S_2\subset S_3\) | Interdit. |
| \(S_2\perp S_3\) au sens vectoriel | Faux : les deux contiennent \(RV\). OrthogonalitÃ© = **explications**, pas produits scalaires. |
| Ordre accidentel dans \(S_3\) | \([RV,MA]\) est invariant par permutation de la fenÃªtre. |
| Dynamique perdue dans \(S_2\) | ConservÃ©e via early/late (si \(W=20\)). |
| Drift dans \(S_3\) | Exclu. |
| \(S\) projetÃ© depuis \(X\) standardisÃ© | Interdit. |
| Cas D = preuve de l'ordre | Interdit. |
| \(W\) impair / non 20 | Partage \(S_2\) sans rÃ¨gle. OPEN si \(W\neq 20\). |
| Scaling silencieux du kNN | OPEN, prochaine dÃ©cision scientifique probable. |
| Choix numÃ©rique issu d'E01â€“E04 | Aucun (pas de corrÃ©lation, pas de 5/15). |
| Extra \(\max\lvert r\rvert\) glissÃ© dans \(S_3\) | Non retenu. |
| Â« Axes orthogonaux Â» (niveau / forme) | Interdit sans preuve. Dire **sÃ©paration conceptuelle**. |

### 9.13 ReparamÃ©trisations candidates â€” revue mathÃ©matique

**Objet :** comparer OLD vs NEW pour \(S_2\) et \(S_3\). MÃªme H2b / H2c.
Aucune donnÃ©e. Aucun \(\varepsilon\). Aucune distance.

Question centrale (pour chaque) :

| | |
|--|--|
| **A** | Conserve-t-elle l'information OLD sur le domaine rÃ©gulier ? |
| **B** | SÃ©pare-t-elle mieux niveau vs dynamique relative / forme relative ? |
| **C** | Introduit-elle une nouvelle hypothÃ¨se scientifique ? |
| **D** | SingularitÃ©s / conventions qui rendraient OLD prÃ©fÃ©rable ? |

#### 9.13.1 \(S_2\) : \(\Delta RV\) vs \(D=\log(RV^{late}/RV^{early})\)

Domaine rÃ©gulier : \(RV^{early}>0\), \(RV^{late}>0\) (moitiÃ©s Ã©gales).

PropriÃ©tÃ©s de \(D\) :

- \(D=0\) iff \(RV^{late}=RV^{early}\) ;
- \(D>0\) iff \(RV^{late}>RV^{early}\) ; \(D<0\) sinon ;
- si tous les rendements de la fenÃªtre sont multipliÃ©s par
  \(\lambda>0\), alors \(RV\), \(RV^{early}\), \(RV^{late}\) scalent
  par \(\lambda\) et **\(D\) est inchangÃ©** ;
- \(\Delta RV\) **scale** par \(\lambda\) (pas invariant d'Ã©chelle).

Reconstruction (\(\rho=e^{D}=RV^{late}/RV^{early}\)) :

\[
RV^{early}=RV\sqrt{\frac{2}{1+\rho^{2}}},
\qquad
RV^{late}=\rho\,RV^{early}
\]

donc \((RV,D)\mapsto(RV^{early},RV^{late})\) est bijective sur le
domaine rÃ©gulier. Comme \((RV,\Delta RV)\) l'est dÃ©jÃ  (sous
\(|\Delta RV|\le 2\,RV\) et positivitÃ©), **A : mÃªme information** sur
ce domaine.

SingularitÃ©s NEW (OLD reste fini) :

| Cas | OLD \(\Delta RV\) | NEW \(D\) |
|-----|-------------------|-----------|
| \(RV^{early}=0\), \(RV^{late}>0\) | \(=RV^{late}\) | \(\to+\infty\) |
| \(RV^{late}=0\), \(RV^{early}>0\) | \(=-RV^{early}\) | \(\to-\infty\) |
| les deux \(=0\) (\(\Rightarrow RV=0\)) | \(=0\) | indÃ©fini (\(0/0\)) |

**Ne pas** inventer un \(\varepsilon\). Traiter les zÃ©ros serait une
**convention supplÃ©mentaire** (choix scientifique sÃ©parÃ©), pas une
partie de la reparamÃ©trisation.

**B :** oui â€” \(RV\) = niveau absolu ; \(D\) = dynamique **relative**
(sÃ©paration conceptuelle niveau / dynamique). Pas une orthogonalitÃ©
gÃ©omÃ©trique ni une corrÃ©lation nulle.

**C :** non. Toujours H2b.

**D :** singularitÃ©s log prÃ¨s de demi-fenÃªtres plates. OLD reste
dÃ©fini partout. En pratique, pour des rendements quotidiens non
identiquement nuls sur \(W/2\) sÃ©ances, le domaine rÃ©gulier couvre
presque tout ; le cas pathologique reste **documentÃ©**.

Risques adversariaux NEW : (i) deux rÃ©gimes de niveaux trÃ¨s diffÃ©rents
avec le **mÃªme ratio** late/early sont indiscernables sur \(D\) â€”
voulu pour une dynamique relative, mais **masque** des Ã©carts
absolus que \(\Delta RV\) distinguerait ; (ii) \(D\) peut devenir
grand en magnitude prÃ¨s de zÃ©ro â€” Â« sophistication Â» apparente si
on oublie le domaine ; (iii) sans convention zÃ©ro, le kNN devra
un jour traiter ces points (OPEN, pas ici).

**Verdict \(S_2\) : `PREFER NEW`.**

MÃªme information sur le domaine rÃ©gulier ; meilleure sÃ©paration
conceptuelle niveau / dynamique relative ; singularitÃ©s
pathologiques documentÃ©es, sans \(\varepsilon\). Pas `ACCEPTED`.

#### 9.13.2 \(S_3\) : \(MA\) vs \(Q=MA/RV\)

Domaine rÃ©gulier : \(RV>0\). Alors au moins un \(r\neq 0\), donc
\(MA>0\) et

\[
0 < Q_t \le 1
\]

\(Q=1\) iff toutes les amplitudes \(|r|\) de la fenÃªtre sont Ã©gales
(Ã©galitÃ© RMSâ€“AM). \(Q\to 0^{+}\) quand l'hÃ©tÃ©rogÃ©nÃ©itÃ© relative des
\(|r|\) croÃ®t.

Invariance : si \(r\mapsto\lambda r\) pour \(\lambda\neq 0\), \(RV\)
et \(MA\) scalent par \(|\lambda|\) ; **\(Q\) inchangÃ©**.

Relation dÃ©jÃ  Ã©tablie :

\[
\operatorname{Var}_{\mathrm{win}}(|r|)=RV^{2}-MA^{2}
\quad\Rightarrow\quad
\frac{\operatorname{Var}_{\mathrm{win}}(|r|)}{RV^{2}}=1-Q^{2}
\quad(RV>0)
\]

BijectivitÃ© : pour \(RV>0\), \(MA=Q\cdot RV\) avec \(Q\in(0,1]\).
Donc **A : mÃªme information** que \((RV,MA)\) sur \(\{RV>0\}\).

SingularitÃ© : \(RV=0\) (fenÃªtre plate) \(\Rightarrow MA=0\) ; OLD =
\((0,0)\) bien dÃ©fini ; NEW = \(0/0\) indÃ©fini. **Pas d'\(\varepsilon\).**

**B :** oui â€” \(RV\) = niveau ; \(Q\) = forme / homogÃ©nÃ©itÃ©
**relative** des amplitudes (sÃ©paration conceptuelle niveau / forme).
Pas orthogonalitÃ© statistique.

**C :** non. Toujours H2c.

**D :** une seule singularitÃ© (\(RV=0\)), plus douce que le log de
\(S_2\). OLD prÃ©fÃ©rable **uniquement** si l'on veut un vecteur dÃ©fini
y compris sur la fenÃªtre nulle sans convention.

Risques adversariaux NEW : (i) \(Q\) ignore l'Ã©chelle absolue de
l'hÃ©tÃ©rogÃ©nÃ©itÃ© (\(MA\) fixe Ã  \(RV\) diffÃ©rent) â€” voulu pour la
forme relative ; (ii) ne transforme pas \(S_3\) en objet
sophistiquÃ© au-delÃ  d'un ratio bornÃ© ; (iii) ne rÃ©sout toujours pas
le scaling pour le kNN.

**Verdict \(S_3\) : `PREFER NEW`.**

MÃªme information pour \(RV>0\) ; meilleure sÃ©paration conceptuelle
niveau / forme ; singularitÃ© \(RV=0\) mineure et documentÃ©e. Pas
`ACCEPTED`.

#### 9.13.3 SynthÃ¨se et acceptation humaine

| ContrÃ´le | Verdict revue | Acceptation humaine |
|----------|---------------|---------------------|
| \(S_2\) | `PREFER NEW` | **oui** â€” reprÃ©sentation |
| \(S_3\) | `PREFER NEW` | **oui** â€” reprÃ©sentation |

**ReprÃ©sentations acceptÃ©es** (`REPRESENTATION ACCEPTED / METRIC UNRESOLVED`) :

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

Domaines / singularitÃ©s : Â§9.13.1â€“9.13.2. OLD reste la rÃ©fÃ©rence
algÃ©brique et le secours aux singularitÃ©s.

**Ce que cette acceptation signifie**

- \(S_1\) : niveau ;
- \(S_2\) : niveau + dynamique **relative** ;
- \(S_3\) : niveau + forme **relative** des amplitudes ;
- \(S_2\) et \(S_3\) = **deux attaques distinctes** contre H1, pas
  deux marches d'un mÃªme modÃ¨le.

**Ce qu'elle ne signifie pas**

- ni \(W=20\), ni dÃ©coupage 10+10, ni distance complÃ¨te, ni pondÃ©ration ;
- ni convention \(\varepsilon\) aux zÃ©ros ;
- ni ouverture d'I02.

Invariant multiplicatif du niveau et charts \(S^\star\) : Â§9.14
(ne remplacent **pas** \(S_1/S_2/S_3\)).

### 9.14 Invariant multiplicatif du niveau + charts mÃ©triques

**DÃ©cision humaine a priori** (aucune observation SPY, aucun CRPS,
aucun chiffre E01â€“E04).

#### 9.14.1 DÃ©cision acceptÃ©e

Sur le domaine rÃ©gulier \(RV_a>0\), \(RV_b>0\), la proximitÃ© en
**niveau** de volatilitÃ© est **multiplicative**, non additive :

\[
\delta_{\mathrm{level}}(a,b)
=
\bigl|\log RV_a-\log RV_b\bigr|
=
\Bigl|\log\frac{RV_a}{RV_b}\Bigr|
\]

Exemple conceptuel : \(1\to 2\) et \(2\to 4\) rÃ©alisent le mÃªme
facteur \(2\), donc le **mÃªme** Ã©cart de niveau. Alors que
\(|2-1|=|3-2|\) (additive) traite autrement \(2\to 3\).

Toute composante Â« niveau Â» d'une **future** mÃ©trique devra respecter
cet invariant.

#### 9.14.2 Justification

\(RV\) est strictement positif sur son domaine rÃ©gulier. Sous

\[
r\mapsto c r,\qquad c>0
\]

on a \(RV\mapsto c\,RV\), mais

\[
\log(c\,RV_a)-\log(c\,RV_b)=\log RV_a-\log RV_b
\]

L'Ã©cart de niveau est invariant Ã  une multiplication commune de
l'Ã©chelle des rendements (dÃ©cimal vs pourcentage, etc.).

CohÃ©rence avec les reprÃ©sentations dÃ©jÃ  acceptÃ©es :

- \(D=\log(RV^{\mathrm{late}}/RV^{\mathrm{early}})\) â€” dynamique relative ;
- \(Q=MA/RV\) â€” forme relative.

#### 9.14.3 Gouvernance : reprÃ©sentation \(\neq\) chart

**Ne pas** remplacer ni rouvrir `c85476c`.

ConservÃ© **inchangÃ©** :

\[
S_1=[RV],\qquad S_2=[RV,D],\qquad S_3=[RV,Q]
\]

Introduit sÃ©parÃ©ment â€” **METRIC COORDINATE / CHART CANDIDATE**
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

Ces objets servent Ã  raisonner sur le calcul de proximitÃ©. Ils
**ne** sont **pas** de nouvelles reprÃ©sentations informationnelles
acceptÃ©es.

\[
\boxed{\text{REPRESENTATION} \neq \text{METRIC CHART}}
\]

#### 9.14.4 AcceptÃ© / non acceptÃ©

| AcceptÃ© | Non acceptÃ© |
|---------|-------------|
| proximitÃ© de niveau multiplicative | distance Euclidienne / \(L_1\) / \(L_2\) complÃ¨te |
| \(\delta_{\mathrm{level}}=|\Delta L|\) sur \(RV>0\) | \(\sqrt{(\Delta L)^2+(\Delta D)^2}\), idem \(Q\) |
| charts \(S^\star\) comme candidats de rÃ©flexion | poids Ã©gaux ou quelconques |
| | z-score, rangs, CDF, Mahalanobis, std historique |
| | kNN final, \(W\), 10+10, \(k\), \(\varepsilon\), \(C_t\), CRPS, I02 |

#### 9.14.5 \(S_2^\star\) â€” encore ouvert

\([L,D]\) : deux coordonnÃ©es logarithmiques / relatives. Cela
**ne** justifie **pas** automatiquement

\[
1\text{ unitÃ© de }L \equiv 1\text{ unitÃ© de }D
\]

Le candidat euclidien non pondÃ©rÃ© \(d_{S2}^{(E)}=\sqrt{(\Delta L)^2+(\Delta D)^2}\)
est **auditÃ©** en Â§9.15.2 â€” **non acceptÃ©**.

#### 9.14.6 \(S_3^\star\) â€” \(Q\) vs gÃ©omÃ©trie de forme

\([L,Q]\) combine \(L\in\mathbb{R}\) et \(Q\in(0,1]\). Une Euclidienne
brute sur \((L,Q)\) n'est **pas** neutre.

\(Q=MA/RV\) reste la **statistique informationnelle** de \(S_3\).
L'interprÃ©tation angulaire \(\phi=\arccos Q\) et le choix
mÃ©trique \(|\Delta Q|\) vs \(|\Delta\phi|\) : Â§9.15.1 â€” **OPEN**.

#### 9.14.7 SingularitÃ© \(RV=0\)

\(L=\log RV\) est **indÃ©fini** si \(RV=0\). Aucun \(\varepsilon\),
clipping, sentinelle, ni convention empirique. ProblÃ¨me de domaine
Ã  rÃ©soudre avant toute implÃ©mentation â€” reliÃ© aux singularitÃ©s de
\(D\) et \(Q\) (Â§9.13), **sans** les fusionner abusivement.

#### 9.14.8 Exigences de conception M1â€“M9 (candidates)

Pas toutes indÃ©pendantes mathÃ©matiquement. Exigences de conception
pour une future mÃ©trique :

| ID | Exigence | Sens |
|----|----------|------|
| **M1** | Causality | Aucun futur dans la dÃ©finition de la proximitÃ©. |
| **M2** | Unit / common-scale invariance | \(r\mapsto c r\) (\(c>0\)) ne change pas la proximitÃ© en **niveau** (dÃ©jÃ  partiellement imposÃ© par \(\delta_{\mathrm{level}}\)). |
| **M3** | Symmetry | \(d(a,b)=d(b,a)\). |
| **M4** | Identity | Ã‰tats identiques â‡’ distance nulle. |
| **M5** | Local monotonicity | Toutes choses Ã©gales, augmenter un Ã©cart d'axe ne rapproche pas. |
| **M6** | No predictive tuning | Aucun poids / scaling choisi pour amÃ©liorer CRPS ou un rÃ©sultat I02. |
| **M7** | Interpretability | Chaque terme de \(d\) a une interprÃ©tation explicite. |
| **M8** | Temporal consistency | La rÃ¨gle ne change pas selon la date ou \(C_t\). |
| **M9** | Adversary preservation | La mÃ©trique n'efface pas artificiellement ce que \(S_1/S_2/S_3\) reprÃ©sentent. |

**Prochaine question OPEN :** gÃ©omÃ©trie de forme \(Q\) vs \(\phi\)
et agrÃ©gation avec \(L\) â€” Â§9.15. Puis pondÃ©ration \(S_2^\star\).

#### 9.14.9 Revue de cohÃ©rence

| ContrÃ´le | OK |
|----------|-----|
| H1 / H2aâ€“c inchangÃ©s | oui |
| \(S_1/S_2/S_3\) non remplacÃ©s | oui |
| Aucun rÃ©sultat empirique | oui |
| Pas de distance complÃ¨te ni de poids | oui |
| \(S^\star\) â‰  reprÃ©sentation acceptÃ©e | oui |
| Pas d'\(\varepsilon\) | oui |

### 9.15 Revue adversariale â€” mÃ©triques de forme \(Q\) vs \(\phi\) ; candidat \(S_2\)

**Nature :** documentaire uniquement. Aucune donnÃ©e. Aucune mÃ©trique
acceptÃ©e. Objectif : quelles gÃ©omÃ©tries ont une justification
**indÃ©pendante des donnÃ©es** â€” pas laquelle Â« performe Â».

#### 9.15.0 IdentitÃ©s de base (domaine rÃ©gulier \(RV>0\))

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

Niveaux de gouvernance (Ã  ne pas confondre) :

| Niveau | Objet | Statut |
|--------|-------|--------|
| Informationnel | \(Q=MA/RV\) dans \(S_3\) | **ACCEPTED** (reprÃ©sentation) |
| InterprÃ©tation | \(\phi=\arccos Q\) | **documentÃ©e** â€” angle Ã  l'uniforme |
| MÃ©trique de forme | \(\lvert\Delta Q\rvert\) vs \(\lvert\Delta\phi\rvert\) | **OPEN** |

\[
\boxed{Q\text{ (statistique)} \neq \phi\text{ (interprÃ©tation)} \neq d_{\mathrm{forme}}}
\]

#### 9.15.1 \(Q\) vs \(\phi\) â€” deux gÃ©omÃ©tries, aucune Â« neutre Â»

**A. DÃ©rivÃ©e et dÃ©veloppement prÃ¨s de l'uniforme**

\[
\Bigl|\frac{d\phi}{dQ}\Bigr|=\frac{1}{\sqrt{1-Q^{2}}}
\quad\text{diverge quand }Q\to 1^{-}
\]

PrÃ¨s de \(\phi=0\) (\(Q\to 1\)) :

\[
Q=\cos\phi=1-\frac{\phi^{2}}{2}+O(\phi^{4})
\quad\Rightarrow\quad
\phi\approx\sqrt{2(1-Q)}
\]

Donc \(Q\) **compresse quadratiquement** les petites dÃ©viations
angulaires ; \(\phi\) les remet au premier ordre en angle. La dÃ©rivÃ©e
infinie n'implique **pas** Ã  elle seule une hypersensibilitÃ©
pathologique de \(\phi\) : elle peut aussi corriger la dÃ©gÃ©nÃ©rescence
locale de \(Q=\cos\phi\).

RÃ©ciproquement, pour un Ã©cart angulaire fixe \(\delta\) prÃ¨s de
\(\phi\),

\[
\Delta Q\approx-\sin(\phi)\,\delta
\]

Lorsque \(\phi\to 0\), \(\Delta Q\to 0\) pour un mÃªme \(\delta\).
Donc **\(Q\) sous-discrimine** les diffÃ©rences de forme prÃ¨s de
l'uniformitÃ© si l'on considÃ¨re l'angle comme rÃ©fÃ©rence â€” autant que
\(\phi\) peut sembler les sur-discriminer si l'on considÃ¨re le cosinus
comme rÃ©fÃ©rence.

**B. Deux mÃ©triques extrinsÃ¨ques distinctes**

\[
d_Q(a,b)=\lvert Q_a-Q_b\rvert
\quad\text{vs}\quad
d_\phi(a,b)=\lvert\phi_a-\phi_b\rvert=\lvert\arccos Q_a-\arccos Q_b\rvert
\]

- \(d_Q\) : diffÃ©rences Ã©gales de **ratio \(\ell_1/\ell_2\)** (cosinus)
  Ã©quivalentes ;
- \(d_\phi\) : diffÃ©rences Ã©gales d'**angle Ã  l'uniforme** Ã©quivalentes.

Aucune n'est Â« neutre Â». Choisir l'une, c'est choisir une gÃ©omÃ©trie.

**C. Terminologie â€” ce que \(Q\approx 1\) n'est pas**

\(Q\approx 1\) signifie que les amplitudes \(|r_i|\) de la fenÃªtre sont
**proches les unes des autres** (profil plat). Ce n'est **pas**
Â« bruit blanc gaussien Â». Pour une grande fenÃªtre i.i.d. gaussienne
centrÃ©e, asymptotiquement

\[
Q\to\frac{\mathbb{E}|Z|}{\sqrt{\mathbb{E}[Z^{2}]}}=\sqrt{\frac{2}{\pi}}\approx 0.798
\]

pas \(1\). Interdit d'assimiler quasi-uniforme Ã  gaussien.

**D. StabilitÃ© / perturbations de \(\mathbf{u}\)**

- Petite perturbation angulaire prÃ¨s de \(\phi=0\) : \(\Delta Q=O(\phi\,\delta)=O(\delta^{2})\)
  si \(\phi\sim\delta\) â€” \(d_Q\) voit peu ; \(d_\phi\) voit \(\delta\).
- PrÃ¨s de \(Q\to 0^{+}\) (\(\phi\to\pi/2\)) : \(\lvert d\phi/dQ\rvert\to 1\),
  les deux mÃ©triques sont localement comparables Ã  une constante.
- Une seule coordonnÃ©e grande dans \(\mathbf{u}\) (spike) pousse \(Q\)
  vers le bas ; les deux distances augmentent, mais pas au mÃªme rythme.

**E. Borne \(1/\sqrt{W}\) (rappel, pas un seuil)**

Par Cauchyâ€“Schwarz / RMSâ€“AM, \(Q\le 1\) toujours. La valeur typique
sous i.i.d. dÃ©pend de la loi des \(r\) et de \(W\) ; ce n'est **pas**
une justification pour caler une mÃ©trique, ni pour choisir entre \(Q\)
et \(\phi\). Mention seulement pour Ã©viter de lire \(Q=0.8\) comme
Â« loin de l'uniforme Â» sans modÃ¨le.

**F. ExtrinsÃ¨que vs intrinsÃ¨que**

- ExtrinsÃ¨que sur le cosinus : \(d_Q\) (plongement \(Q\in(0,1]\)).
- IntrinsÃ¨que sur le cercle / cÃ´ne des directions de \(\mathbf{u}\) :
  Ã©cart angulaire \(d_\phi\) au rayon \(\mathbf{1}\).

Les deux sont dÃ©fendables a priori. **Aucune raison** de dÃ©clarer \(Q\)
rÃ©fÃ©rence mÃ©trique et \(\phi\) variante (ni l'inverse) sans dÃ©cision
gÃ©omÃ©trique explicite.

**Question gÃ©omÃ©trique exacte (sans SPY / CRPS) :**

> Pour l'adversaire \(S_3\), veut-on prÃ©server une diffÃ©rence linÃ©aire
> du ratio \(\ell_1/\ell_2\), ou une diffÃ©rence linÃ©aire de l'angle Ã 
> l'uniformitÃ© ?

**Verdict documentaire \(Q\) vs \(\phi\) :** `INCONCLUSIVE` â€”
les deux sont des gÃ©omÃ©tries lÃ©gitimes ; aucune n'est neutre ;
la statistique \(Q\) reste acceptÃ©e ; la mÃ©trique de forme reste OPEN.

#### 9.15.2 Audit du candidat \(S_2\) : \(d_{S2}^{(E)}\)

Candidat **non acceptÃ©** :

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
| \(L\) et \(D\) sont des log-ratios de volatilitÃ© â€” type d'objet comparable | Â« facteur \(e\) sur le niveau â‰¡ facteur \(e\) sur la dynamique Â» reste une **pondÃ©ration** `1:1` |
| Invariance commune \(r\mapsto c r\) (\(c>0\)) | \(L\) et \(D\) ne sont pas indÃ©pendants (\(RV_e^{2}+RV_l^{2}=2\,RV^{2}\)) |
| Pas de z-score / rang / donnÃ©e | Norme \(L_2\) vs \(L_1\) non tranchÃ©e ; M5 OK pour les deux |
| CohÃ©rent avec M2 (niveau) et structure relative de \(D\) | N'implique pas l'agrÃ©gation avec une future forme \(S_3\) |

**Verdict documentaire \(d_{S2}^{(E)}\) :** `ACCEPTABLE CANDIDATE` pour
*Ã©tude* â€” **pas** `ACCEPTED`. PremiÃ¨re mÃ©trique a priori digne
d'examen pour \(S_2^\star\) ; n'isole pas encore l'opÃ©rateur kNN du
choix de norme.

#### 9.15.3 Ce qui reste strictement OPEN (reframÃ© par Â§9.16)

- choix **unique** \(|\Delta Q|\) vs \(|\Delta\phi|\) : **ne plus**
  chercher Ã  le forcer par une nouvelle transformation â€” voir doctrine
  candidat Â§9.16 ;
- agrÃ©gation \(L\) avec forme (sous la mÃªme discipline de robustesse) ;
- acceptation de \(d_{S2}^{(E)}\) comme primaire, avec Ã©ventuelle
  variante \(L_1\) prÃ©enregistrÃ©e (Â§9.16.3) ;
- z-scores, rangs, poids appris â€” **interdits** comme rÃ©solution de
  l'incertitude mÃ©trique.

#### 9.15.4 CohÃ©rence

| ContrÃ´le | OK |
|----------|-----|
| \(S_3=[RV,Q]\) non modifiÃ© | oui |
| \(\phi\) â‰  nouvelle reprÃ©sentation acceptÃ©e | oui |
| Pas de Â« \(Q\) = mÃ©trique neutre Â» | oui |
| Pas de gaussien = \(Q\approx1\) | oui |
| \(d_{S2}^{(E)}\) non acceptÃ© | oui |
| Aucune donnÃ©e / CRPS | oui |

### 9.16 Doctrine candidat â€” incertitude mÃ©trique â†’ robustesse prÃ©enregistrÃ©e

**Nature :** mÃ©thodologique, documentaire. **Avant \(C_t\).** Aucune
donnÃ©e. Aucune mÃ©trique unique imposÃ©e. I02 reste `NOT OPENED`.

**Statut :** `METHODOLOGICAL CANDIDATE` â€” pas encore acceptation
humaine formelle.

#### 9.16.0 Constat d'asymÃ©trie (post-`8b652f7`)

\[
S_2^\star=[L,D]
\quad\text{dispose d'un candidat complet dÃ©fendable non acceptÃ© :}\quad
d_{S2}^{(E)}=\sqrt{(\Delta L)^{2}+(\Delta D)^{2}}
\]

\[
S_3^\star=[L,Q]
\quad\text{n'a pas de composante de forme arrÃªtÃ©e :}\quad
\lvert\Delta Q\rvert
\;\text{vs}\;
\lvert\Delta\phi\rvert,\quad
\phi=\arccos Q
\]

Â§9.15 a montrÃ© qu'on **ne** dÃ©duit **pas** une mÃ©trique \(S_3\) de
la seule interprÃ©tation gÃ©omÃ©trique \(\phi=\arccos Q\). C'est un
rÃ©sultat utile : la belle gÃ©omÃ©trie ne tranche pas.

**Interdit dÃ©sormais (chemin fermÃ©) :** enchaÃ®ner de nouvelles
transformations / charts Â« Ã©lÃ©gants Â» pour dÃ©partager \(Q\) et \(\phi\)
sans critÃ¨re a priori indÃ©pendant des donnÃ©es. Risque : succession
infinie de coordonnÃ©es mathÃ©matiquement dÃ©fendables.

#### 9.16.1 Ce qu'on exige rÃ©ellement d'un adversaire

Pour I02, \(S_3\) n'a **pas** besoin d'Ãªtre Â« la vraie gÃ©omÃ©trie Â» du
profil d'amplitudes. Il doit Ãªtre un **contrÃ´le simple, crÃ©dible et
difficile Ã  battre artificiellement** pour H2c.

Question mÃ©thodologique (remplace la quÃªte de la mÃ©trique parfaite) :

> Parmi plusieurs mÃ©triques a priori Ã©galement dÃ©fendables pour un
> mÃªme contrÃ´le informationnel, faut-il en sÃ©lectionner arbitrairement
> une, ou exiger que la conclusion concernant \(X\) survive aux
> variantes raisonnables **prÃ©enregistrÃ©es** ?

La seconde voie est la doctrine candidat.

\[
\boxed{\text{incertitude mÃ©trique} \rightarrow \text{robustesse prÃ©enregistrÃ©e}}
\]

plutÃ´t que

\[
\text{incertitude mÃ©trique} \rightarrow \text{chercher la mÃ©trique parfaite}.
\]

#### 9.16.2 RÃ¨gle candidat pour H2c / \(S_3\)

Soit \(\mathcal{M}_{S3}\) un **ensemble fini prÃ©enregistrÃ©** de
mÃ©triques de forme raisonnables partageant le mÃªme contrÃ´le
informationnel \(S_3=[RV,Q]\) â€” au minimum les deux gÃ©omÃ©tries dÃ©jÃ 
auditÃ©es :

\[
d_Q=\lvert\Delta Q\rvert,
\qquad
d_\phi=\lvert\Delta\phi\rvert=\lvert\arccos Q_a-\arccos Q_b\rvert
\]

(plus, le cas Ã©chÃ©ant, une rÃ¨gle d'agrÃ©gation avec \(L\) **identique**
pour chaque membre, elle aussi prÃ©enregistrÃ©e â€” non choisie ici).

**InterprÃ©tation candidat de Â« \(X\) rÃ©siste Ã  H2c Â» :**

\[
X \succ S_3
\quad\text{n'est interprÃ©table comme rÃ©sistance Ã  H2c}
\quad\text{que si le rÃ©sultat ne dÃ©pend pas du choix}
\quad\text{raisonnable dans }\mathcal{M}_{S3}.
\]

ConsÃ©quences :

| Observation | Verdict candidat |
|-------------|------------------|
| \(X\) bat \(S_3\) sous **toutes** les \(d\in\mathcal{M}_{S3}\) | rÃ©sistance Ã  H2c **interprÃ©table** (sous les autres gates) |
| \(X\) bat \(S_3\) sous **une** \(d\), pas sous une autre | **`INCONCLUSIVE`** â€” **pas** une invitation Ã  retenir celle qui arrange \(X\) |
| \(S_3\) reproduit \(N_X\) sous **au moins une** \(d\in\mathcal{M}_{S3}\) | H2c **non Ã©cartÃ©e** (kill / non-rÃ©sistance) |

`INCONCLUSIVE` reÃ§oit ici un rÃ´le **exactement adaptÃ©** : l'incertitude
gÃ©omÃ©trique a priori, une fois prÃ©enregistrÃ©e comme famille, devient
un test de robustesse, pas un levier de sÃ©lection empirique.

**Ce que cette rÃ¨gle n'est pas :**

- pas une optimisation sur CRPS pour choisir \(d_Q\) ou \(d_\phi\) ;
- pas un z-score, rang, CDF, Mahalanobis, poids appris ;
- pas une acceptation de \(d_Q\) ni de \(d_\phi\) comme Â« la Â» mÃ©trique ;
- pas une ouverture de I02 ni un seuil numÃ©rique.

#### 9.16.3 Extension candidat pour \(S_2\)

MÃªme logique **potentielle**, sans symÃ©trie forcÃ©e avec \(S_3\) :

- \(d_{S2}^{(E)}\) reste le **candidat primaire** (`ACCEPTABLE
  CANDIDATE`, non acceptÃ©) ;
- une norme alternative **prÃ©enregistrÃ©e** (ex. \(L_1\) :
  \(\lvert\Delta L\rvert+\lvert\Delta D\rvert\)) peut servir de
  **test de robustesse gÃ©omÃ©trique**, non de concurrent Ã  optimiser
  aprÃ¨s coup.

Si retenue : Â« \(X\succ S_2\) Â» interprÃ©table comme rÃ©sistance Ã  H2b
seulement si le rÃ©sultat survit Ã  la variante prÃ©enregistrÃ©e ; sinon
`INCONCLUSIVE` / non-rÃ©sistance selon la mÃªme grille logique que
Â§9.16.2. **Non figÃ©** ici â€” parallÃ¨le mÃ©thodologique seulement.

#### 9.16.4 Ce qui doit encore Ãªtre dÃ©cidÃ© humainement (sans \(C_t\))

Avant toute dÃ©finition de \(C_t\) :

1. **Accepter ou rejeter** la doctrine Â§9.16
   (`incertitude â†’ robustesse prÃ©enregistrÃ©e`) ;
2. si acceptÃ©e : figer \(\mathcal{M}_{S3}\) (au minimum
   \(\{d_Q,d_\phi\}\)) et la rÃ¨gle d'agrÃ©gation avec \(L\) **commune**
   aux membres ;
3. dÃ©cider si \(S_2\) adopte le mÃªme schÃ©ma (primaire + variante) ;
4. **ne pas** ouvrir la boÃ®te des charts suivants pour \(S_3\).

\(C_t\), holdout, \(W/k/h\), CRPS final : **aprÃ¨s** cette discipline,
pas avant comme substitut.

#### 9.16.5 CohÃ©rence

| ContrÃ´le | OK |
|----------|-----|
| Pas de nouvelle transformation \(S_3\) | oui |
| \(S_1/S_2/S_3\) informationnels inchangÃ©s | oui |
| Pas de sÃ©lection empirique de mÃ©trique | oui |
| `INCONCLUSIVE` dÃ©fini comme verdict, pas comme invitation Ã  cherry-pick | oui |
| Avant \(C_t\) | oui |
| I02 NOT OPENED | oui |

---

## 10. Statut de `H_vol` et `H_shape`

| RÃ´le | Objet |
|------|--------|
| **PRIMARY CANDIDATE** | Score probabiliste du futur **rÃ©ellement observÃ©** (CRPS *si* acceptÃ© aprÃ¨s revue humaine) |
| **MECHANISTIC DIAGNOSTIC** | `H_vol` â€” les voisins sont-ils homogÃ¨nes en volatilitÃ© ? |
| **NEGATIVE / SEMANTIC CONTROL** | `H_shape` â€” un canal volatilitÃ© ne autorise **pas** Â« trajectoires futures similaires Â» |
| **B0** | RÃ©fÃ©rence secondaire, pas adversaire suffisant de H1 |

`H_shape` : mÃªme discipline que le draft v0.1 (DEC-03). RÃ´le-gate :
**OPEN**. Pas de seuil ici.

---

## 11. Revue adversariale de H1-v0.2

Qu'est-ce qui pourrait rendre cette formulation **trompeuse** ?

**A. Dimension.** \(X\in\mathbb{R}^{W}\) a plus de coordonnÃ©es que
chaque \(S_i\). Un gain peut Ãªtre Â« plus de dimensions Â», pas
Â« gÃ©omÃ©trie Â». D'oÃ¹ \(S_1,S_2,S_3\) (H2aâ€“c), pas seulement `rv_W`.
Battre les trois ne **prouve** toujours pas l'ordre temporel.

**B. kNN en haute dimension.** LocalitÃ© faible, distances concentrÃ©es
(E02 : rang 50 / mÃ©diane bibliothÃ¨que â‰ˆ 0,67 â€” observation I01, pas
un calibrage). InstabilitÃ© possible. HÃ©riter \(k=50\), \(W=20\) est un
hÃ©ritage gÃ©nÃ©rateur (Â§11.H).

**C. ECDF Ã  \(k\) atomes.** Mal calibrÃ©e par construction (granularitÃ©
\(1/k\)). Le CRPS le voit ; un Â« gain Â» peut Ãªtre de la variance de
score, pas de la structure.

**D. CRPS et dispersion.** Peut rÃ©compenser une sharpness heureuse
sans structure Ã©conomique (ni alpha, ni rÃ©gime interprÃ©table). Voir
Â§6.1 (Ã©chelle, queues).

**E. SÃ©lection par \(C_t\).** Conditionner Ã  \(C_t=1\) change
l'Ã©chantillon. Une \(C_t\) trop rare ou trop alignÃ©e sur les crises
vues en E04 recrÃ©e I01. \(C_t\) reste **non dÃ©finie**.

**F. Taille de \(\{C_t=1\}\).** Trop peu de dates â‡’ moyenne de \(D\)
instable, H3 indiscernable. Impossible Ã  chiffrer avant de dÃ©finir
\(C_t\). **OPEN** liÃ© Ã  \(C_t\).

**G. Pas une stratÃ©gie.** Un meilleur CRPS sur \(V\) n'est ni un signe
de rendement, ni un alpha, ni une Ã©ligibilitÃ© de stratÃ©gie, ni un
Market-State Engine.

**H. HÃ©ritage gÃ©nÃ©rateur I01.** RÃ©utiliser \(W=20\), \(h=10\), \(k=50\)
et la forme de \(X\) (rendements standardisÃ©s) **Ã©vite le retuning**
et **hÃ©rite du gÃ©nÃ©rateur**. Les deux sont vrais. Ã€ documenter dans
tout protocole futur, pas Ã  Â« corriger Â» aprÃ¨s un premier CRPS.

---

## 12. Holdout et rÃ©plication (conceptuel)

Le dataset SPY d'E01â€“E04 couvre **1993-01-29 â†’ 2026-09-23**.

**Post-2022 n'est pas un holdout vierge** pour cette famille
d'hypothÃ¨ses.

CatÃ©gories possibles â€” **aucune sÃ©lectionnÃ©e** : futur rÃ©ellement non
observÃ© ; autre instrument ; autre univers ; sÃ©paration
prÃ©-enregistrÃ©e non choisie pour isoler 2008/2009/2020.

Ne pas : choisir une source ; rouvrir DR-003 / DR-005 ; contacter un
fournisseur ; requalifier yfinance.

Un I02 exploratoire UNQUALIFIED, s'il est un jour autorisÃ©, ne produit
aucun SCI-PASS / SCI-FAIL (DR-007).

---

## 13. Falsification / kill criteria

Qualitatif. **Aucun seuil numÃ©rique.**

1. Disparition du gain de score annoncÃ© hors information indÃ©pendante (H4).
2. Un adversaire \(S_1\), \(S_2\) ou \(S_3\) reproduit \(N_X\) au
   sens du score (H2a / H2b / H2c).
3. Gain portÃ© par quelques Ã©vÃ©nements, sans reproductibilitÃ© sous \(C_t\)
   prÃ©-enregistrÃ©e (H3).
4. DÃ©pendance Ã  une dÃ©finition de Â« stress Â» choisie aprÃ¨s 2008/2009/2020
   ou aprÃ¨s maximisation de \(D\) ou de \(D^{\mathrm{CRPS}}\).
5. RÃ©sultat entiÃ¨rement dÃ» au comportement de la mÃ©trique (CRPS Ã 
   Ã©chelle brute, ou `H_vol`) sans structure de voisinage.
6. InstabilitÃ© Ã  des choix **prÃ©-enregistrÃ©s** raisonnables (pas :
   chercher \(W\) aprÃ¨s coup) â€” y compris, si Â§9.16 est acceptÃ©e,
   dÃ©pendance du verdict H2c (resp. H2b) au seul membre favorable
   de \(\mathcal{M}_{S3}\) (resp. variante \(S_2\)) : alors
   `INCONCLUSIVE` / non-rÃ©sistance, **pas** sÃ©lection de la mÃ©trique
   qui arrange \(X\).

Un kill n'est pas un SCI-FAIL d'I01.

---

## 14. Stress / market condition â€” dÃ©finition non rÃ©solue

**OPEN QUESTION.** InchangÃ© dans l'esprit du draft v0.1.

Interdit comme dÃ©finition : annÃ©es 2008 / 2009 / 2020 ; seuil `rv_W`
ou tertile relu en rÃ¨gle aprÃ¨s E04.

Principes toujours exigÃ©s : causalitÃ© ; disponibilitÃ© Ã  \(t\) ; gel
avant expÃ©rimentation ; indÃ©pendance maximale vis-Ã -vis du gÃ©nÃ©rateur ;
simplicitÃ© ; interprÃ©tabilitÃ© ; **pas** d'optimisation sur \(D_{vol}\)
ni sur \(D^{\mathrm{CRPS}}\).

**Aucune dÃ©finition n'est choisie.**

---

## 15. Market-State / Regime Engine

**Aucun contrat empirique n'est dÃ©rivÃ© d'I01.** Aucune architecture
modifiÃ©e. I02, s'il est autorisÃ© plus tard, pourra ou non informer
ce contrat.

---

## 16. OPEN QUESTION â€” liste exacte

Ne pas rÃ©soudre dans ce draft :

- **acceptation de la doctrine Â§9.16** (prioritaire, **avant \(C_t\)**) ;
- si doctrine acceptÃ©e : figement de \(\mathcal{M}_{S3}\) et rÃ¨gle
  d'agrÃ©gation \(L\)+forme commune ; parallÃ¨le \(S_2\) oui/non ;
- dÃ©finition de \(C_t\) (**aprÃ¨s** discipline mÃ©trique) ;
- acceptation de \(d_{S2}^{(E)}\) comme primaire
  (`ACCEPTABLE CANDIDATE`) ;
- z-score / rangs / CDF / Mahalanobis / poids appris ;
- convention aux singularitÃ©s (\(RV=0\), demi-vol nulle) â€” pas d'\(\varepsilon\) ;
- \(W\), \(h\), \(k\), partage 10+10 ; holdout ; CRPS final ; Market-State Engine.

**Chemin fermÃ© :** dÃ©partager \(Q\) vs \(\phi\) par une nouvelle
transformation / chart Â« plus fondamental Â».

**AcceptÃ© :**

- \(S_1=[RV]\), \(S_2=[RV,D]\), \(S_3=[RV,Q]\) ;
- invariant multiplicatif \(\delta_{\mathrm{level}}=\lvert\Delta L\rvert\) ;
- charts \(S^\star\) (â‰  reprÃ©sentations) ;
- \(Q\) statistique ; \(\phi=\arccos Q\) interprÃ©tation (pas mÃ©trique
  unique figÃ©e).

**DocumentÃ©s :** H1-v0.2 ; \(V_{t,h}\) ; CRPS ; M1â€“M9 ; Â§9.15 ;
doctrine candidat Â§9.16.

---

## 17. Before I02 can open

DÃ©cisions **humaines**. Tant que la derniÃ¨re case n'est pas cochÃ©e :

**I02 = NOT OPENED.**

- [ ] HypothÃ¨se finale approuvÃ©e (H1-v0.2 reste une candidate)
- [ ] Doctrine Â§9.16 (robustesse mÃ©trique prÃ©enregistrÃ©e) **acceptÃ©e
      ou rejetÃ©e** â€” **avant \(C_t\)**
- [ ] Si doctrine acceptÃ©e : \(\mathcal{M}_{S3}\) (+ agrÃ©gation \(L\))
      figÃ© ; dÃ©cision parallÃ¨le \(S_2\)
- [ ] Condition de marchÃ© \(C_t\) dÃ©finie ex ante (Â§14) â€” **aprÃ¨s**
      discipline mÃ©trique
- [x] ReprÃ©sentations adversaires \(S_1/S_2/S_3\) **acceptÃ©es**
- [x] Invariant multiplicatif du niveau **acceptÃ©** ; charts \(S^\star\)
- [x] Chemin Â« chart suivant pour \(S_3\) Â» **fermÃ©** (Â§9.16.0)
- [ ] \(d_{S2}^{(E)}\) acceptÃ©/rejetÃ© comme primaire (Ã©vent. + variante)
- [ ] Observable futur **approuvÃ©** (\(V_{t,h}\) candidat)
- [ ] Score probabiliste **approuvÃ©** (CRPS = acceptable candidate)
- [ ] RÃ´le de `H_shape` dÃ©fini
- [ ] Kill criteria approuvÃ©s (dont Â§13.6 alignÃ© Â§9.16)
- [ ] StratÃ©gie de donnÃ©es / rÃ©plication dÃ©finie
- [ ] Risque de data snooping documentÃ©
- [ ] Protocole de gel avant premier rÃ©sultat
- [ ] DÃ©cision explicite **OPEN I02**

---

## 18. Revue de cohÃ©rence (auteur)

| ContrÃ´le | Statut |
|----------|--------|
| Aucun chiffre / donnÃ©e / CRPS | oui |
| \(S_1/S_2/S_3\) inchangÃ©s | oui |
| Pas de nouvelle transformÃ©e \(S_3\) | oui |
| Doctrine Â§9.16 = candidat, non acceptÃ©e | oui |
| Avant \(C_t\) | oui |
| \(d_{S2}^{(E)}\) non acceptÃ© | oui |
| I01 CLOSED ; I02 NOT OPENED | oui |

---

## RÃ©fÃ©rences (lecture, pas autoritÃ© de validation)

- [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
- E01â€“E04 ; [hypothesis.md](../I01/hypothesis.md) ; [protocol.md](../I01/protocol.md)
- [DR-007](../../docs/adr/DR-007-exploratory-vs-confirmatory-data.md)
- [DR-008](../../docs/adr/DR-008-i01-e01-exploratory-source.md)
- CRPS : proper scoring rule pour lois rÃ©elles (littÃ©rature ; pas un
  calcul sur SPY)
