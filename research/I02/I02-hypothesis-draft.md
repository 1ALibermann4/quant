# I02 — Brouillon d'hypothèse (pré-investigation)

> **STATUS :** DRAFT / PRE-INVESTIGATION
> **I02 :** NOT OPENED
> **NO EXPERIMENT AUTHORIZED**
>
> **Authority class :** RESEARCH (brouillon, non normatif)
> **Protocol :** QDP v0.1
> **Parent :** I01 exploratoire CLOSE @ `116374b`
> **Draft v0.1 :** `0e893c2`
> **Calculs dans ce document :** aucun
> **Classe données I01 :** UNQUALIFIED (DR-007 / DR-008)

Ce fichier **ne signifie pas** que I02 est ouvert.
Aucun protocole, aucun run, aucun code expérimental I02 n'est autorisé.

$$
\text{observations I01} \neq \text{preuve de cette hypothèse candidate}
$$

E01–E04 ont **généré** la piste. Ils ne peuvent pas la valider.

Les propositions de ce texte (cible \(V_{t,h}\), CRPS, H1-v0.2) sont
**à évaluer**, pas des décisions finales. Rien n'est figé.

---

## 0. Ce que ce draft n'est pas

- pas un SCI-PASS, pas un SCI-FAIL ;
- pas une recommandation de confirmer I01 ;
- pas une ouverture de DR-003 / DR-005 ;
- pas E05 ;
- pas un contrat empirique pour un Market-State / Regime Engine ;
- pas un choix de seuil, de source, ni d'instrument ;
- pas une acceptation de CRPS, de \(h\), de \(S_t\) ou de \(C_t\).

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
- \(S_t\) — résumés simples du passé (**composition OPEN**) ;
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
Distance et composition de \(S\) : **OPEN**.

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
> pré-enregistrés de volatilité et d'énergie passées \(S_t\).

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

## 8. Concurrentes (inchangées dans l'esprit, recalées sur \(V\))

### H1 — Structure géométrique conditionnelle

Voir §7. Non établie.

### H2 — Amplitude / énergie

\(N_S\) (résumés simples) fournit une \(\widehat F_S\) **aussi
informative** que \(N_X\) au sens du score retenu. `rv_W` seul a déjà
été un contrôle insuffisant *pour `H_vol`* (E03) ; cela ne dit pas
qu'un \(S\) mieux conçu échoue pour \(\widehat F(V)\).

Hiérarchie conceptuelle :

```text
X bat B0 seulement                    → peu intéressant
X bat rv_W mais pas un meilleur S     → H2
spectacle seulement sur quelques queues → H3
rien hors information indépendante    → H4
X bat durablement les S sous C_t figé → H1 reste crédible
```

### H3 — Queue / métrique

Le gain de score (ou l'ancien `H_vol`) est porté par des épisodes
extrêmes / par le comportement de la métrique. Pas d'information
généralisable.

### H4 — Absence de structure reproductible

Pas de reproduction sur information indépendante. Issue normale.

---

## 9. Hiérarchie des comparateurs

```text
B0          témoin (hasard dans L_t)     — référence secondaire
   ↓
S           résumés simples (liste OPEN) — adversaire de H1
   ↓
X           structure multivariée        — candidat H1
```

H1 **ne** se soutient **pas** parce que \(X\) bat B0. La question
centrale : \(X\) apporte-t-il quelque chose au-delà d'explications
simples raisonnables ? C'est H2.

Composition exacte de \(S\) (p. ex. familles \(S_1\) vol passée,
\(S_2\) amplitude/énergie), métrique et normalisation de \(S\) :
**OPEN**. À construire **avant** tout run, et **avant** \(C_t\), pour
donner à H2 une vraie chance.

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

**A. Dimension.** \(X\in\mathbb{R}^{W}\) a plus de coordonnées que \(S\).
Un gain peut être « plus de dimensions », pas « géométrie ». D'où
l'exigence d'un \(S\) sérieux (H2), pas seulement `rv_W`.

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
2. \(N_S\) reproduit \(N_X\) au sens du score (H2).
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
- composition exacte de \(S_t\) ; métrique / normalisation de \(S_t\) ;
- définition finale de \(X_t\) ;
- valeur finale de \(h\) (héritage 10 = candidat argumenté, non décidé) ;
- valeur finale de \(k\) ;
- source de données ; instrument / univers de réplication ; holdout ;
- gates statistiques ; seuil de « stress » ;
- acceptation finale du CRPS (seulement `ACCEPTABLE CANDIDATE`) ;
- architecture Market-State Engine.

Éléments **documentés comme candidats**, non cochés comme décisions :

- observable \(V_{t,h}\) (RMS des \(h\) rendements futurs) ;
- information supplémentaire = meilleur score de \(\widehat F\) hors
  échantillon vs \(S\) (CRPS si retenu) ;
- H1-v0.2 ;
- rétrogradation de `H_vol` / `H_shape`.

---

## 17. Before I02 can open

Décisions **humaines**. Tant que la dernière case n'est pas cochée :

**I02 = NOT OPENED.**

- [ ] Hypothèse finale approuvée (H1-v0.2 reste une candidate)
- [ ] Condition de marché \(C_t\) définie ex ante (§14)
- [ ] Comparateur(s) simple(s) \(S_t\) définis ex ante (liste fermée)
- [ ] Observable futur **approuvé** (\(V_{t,h}\) est seulement candidat)
- [ ] Score probabiliste **approuvé** (CRPS = acceptable candidate)
- [ ] Rôle de `H_shape` défini (témoin / mesure / non-gate)
- [ ] Kill criteria approuvés
- [ ] Stratégie de données indépendantes / réplication définie
- [ ] Risque de data snooping documenté (héritage I01 + holdout + score)
- [ ] Protocole de gel avant premier résultat défini
- [ ] Décision explicite **OPEN I02**

Rien n'a été coché : les avancées de ce texte restent des propositions.

---

## 18. Revue de cohérence (auteur)

| Contrôle | Statut |
|----------|--------|
| Aucun chiffre nouveau calculé | oui |
| Aucune donnée nouvelle téléchargée | oui |
| CRPS non calculé ; aucune métrique testée sur données | oui |
| \(C_t\) / seuil de stress non définis | oui |
| \(S_t\) non choisi | oui |
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
