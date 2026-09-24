# I02 — Brouillon d'hypothèse (pré-investigation)

> **STATUS :** DRAFT / PRE-INVESTIGATION
> **I02 :** NOT OPENED
> **NO EXPERIMENT AUTHORIZED**
>
> **Authority class :** RESEARCH (brouillon, non normatif)
> **Protocol :** QDP v0.1
> **Parent :** I01 exploratoire CLOSE @ `116374b`
> **Calculs dans ce document :** aucun
> **Classe données I01 :** UNQUALIFIED (DR-007 / DR-008)

La création de ce fichier **ne signifie pas** que I02 est ouvert.
Aucun protocole, aucun run, aucun code expérimental I02 n'est autorisé
par ce texte.

$$
\text{observations I01} \neq \text{preuve de cette hypothèse candidate}
$$

E01–E04 ont **généré** la piste. Ils ne peuvent pas la valider.

---

## 0. Ce que ce draft n'est pas

- pas un SCI-PASS, pas un SCI-FAIL ;
- pas une recommandation de confirmer I01 ;
- pas une ouverture de DR-003 / DR-005 ;
- pas E05 ;
- pas un contrat empirique pour un Market-State / Regime Engine ;
- pas un choix de seuil, de source, ni d'instrument.

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

Formulations **interdites** comme faits :

- « L2 fonctionne en régime de stress » ;
- « un régime de crise a été identifié » ;
- « la géométrie prédit la volatilité en période de stress ».

Le mot **régime** est ici descriptif et provisoire. Il nomme une piste,
pas un objet mesuré.

---

## 2. Hypothèse candidate (à critiquer, pas acceptée)

Point de départ conceptuel, **pas** une hypothèse déjà figée :

> Sous une condition de marché définie causalement et indépendamment
> des épisodes ayant généré l'hypothèse, la structure multivariée de
> l'état passé \(X_t\) contient une information sur la distribution de
> volatilité future qui n'est pas expliquée par un résumé simple de
> volatilité / énergie passée.

Ceci **n'est plus I01**. I01 postulait une homogénéité future *générale*
des \(Y\) bruts vs B0. La candidate restreint l'univers (condition) et
change le concurrent (résumé simple ≠ B0 seul).

### Éléments à spécifier avant ouverture

| Élément | État | Commentaire |
|---------|------|-------------|
| Variable conditionnante \(C_t\) | **OPEN QUESTION** | Doit être causale, connue à \(t\), définie *avant* tout calcul I02. Ne peut pas être « 2008/2009/2020 » ni un seuil `rv_W` choisi pour coller à E04. Voir §8. |
| Information à \(t\) | Héritable en principe | Convention I01 / DEC-04 : observation **après clôture** de \(t\) ; \(\mathcal{O}_{\leq t}\) seulement. À reconfirmer, pas à « améliorer » après un premier chiffre. |
| Représentation \(X_t\) | **OPEN QUESTION** | I01 : fenêtre \(W=20\) standardisée par \(\hat\mu_t,\hat\sigma_t\) (\(M=252\)). La **réutiliser** parce qu'E01–E04 l'ont utilisée est un héritage générateur. La changer sans raison pré-enregistrée aussi. Décision humaine, pas un retuning. |
| Quantité future | **OPEN QUESTION** | Candidats déjà *vus* dans I01 : `H_vol` des voisins, `‖Y‖`, éventuellement `H_raw`. Choisir `H_vol` *parce que* E02 l'a montré dominant est contaminé. Il faut un observable annoncé, pas le plus flatteur. |
| Comparateur | **OPEN QUESTION** | E03 : `rv_W` ne suffit pas à expliquer L2. Un I02 sérieux exige **au moins un** résumé simple d'amplitude / énergie (et probablement plusieurs, figés). B0 aléatoire peut rester un témoin, pas le seul concurrent. Liste exacte : décision humaine. |
| Population / univers | **OPEN QUESTION** | SPY 1993–2026 a **généré** l'hypothèse. Voir §6. |
| Horizon \(h\) | **OPEN QUESTION** | I01 avait \(h=10\) figé. Le reprendre par commodité n'est pas anodin. |
| « Information supplémentaire » | **OPEN QUESTION** | Sens visé : sous \(\{t : C_t=1\}\), l'homogénéité (ou une loi de la vol future) après voisinage sur \(X\) est **meilleure** que celle obtenue par le(s) comparateur(s) simple(s) — à définir opérationnellement *avant* le run. Pas un alpha, pas un signe de rendement, pas une stratégie. |

Tant qu'une ligne est OPEN, I02 ne peut pas s'ouvrir honnêtement.

---

## 3. Hypothèses concurrentes (minimales)

Toutes sont des issues scientifiques **normales**. Aucune n'est écartée
par E01–E04.

### H1 — Structure géométrique conditionnelle

La structure **multivariée** de \(X_t\) contient, sous certaines
conditions définies **ex ante**, une information sur la volatilité
future que les résumés simples du passé ne capturent pas.

C'est la candidate à tester *si* I02 ouvre. Elle n'est pas établie.

### H2 — Amplitude / énergie

L'effet attribué à L2 peut être reproduit par une représentation
beaucoup plus simple de l'amplitude ou de l'énergie locale.
`rv_W` n'était simplement **pas** le contrôle suffisant (E03 le
suggère sans le prouver pour `‖X‖`, `σ̂_M`, amplitude brute, etc.).

### H3 — Queue / métrique

Le résultat provient principalement du comportement de `H_vol` ou de
la distribution de \(Y\) pendant des épisodes extrêmes. La géométrie
n'apporte pas d'information **généralisable**. Une moyenne tirée par
1 % des dates est compatible avec H3.

### H4 — Absence de structure reproductible

Le phénomène observé dans I01 ne se reproduit pas sur une information
**indépendante** (autre période réellement non vue, autre instrument,
autre univers — §6).

H4 n'est pas un échec de projet. C'est une clôture scientifique propre.

---

## 4. Témoin négatif `H_shape`

I01 n'a **pas** montré de similarité substantielle de forme des
trajectoires futures (`H_shape` ≈ plat vs B0 ; le contrôle `rv_W` non
plus).

Une éventuelle validation **future** portant sur la volatilité ne doit
**pas** être reformulée :

> « des passés géométriquement similaires produisent des trajectoires
> futures similaires ».

Rôle proposé (qualitatif, **pas un gate numérique** maintenant) :

- `H_shape` reste **mesuré** si un I02 compare des voisinages de \(Y\) ;
- il sert de **garde-fou sémantique** : un gain de `H_vol` ou `H_raw`
  n'autorise pas à parler de similarité de trajectoire ;
- un retournement *post hoc* de `H_shape` en critère de PASS serait
  une substitution interdite (héritage DEC-03 : `H_shape` n'était déjà
  pas substituable à SCI-001).

Seuil / rôle de gate : **OPEN QUESTION**, à trancher avant ouverture,
pas ici.

---

## 5. Holdout et réplication (conceptuel)

Le dataset SPY d'E01–E04 couvre **1993-01-29 → 2026-09-23**.

**Post-2022 n'est pas un holdout vierge** pour cette famille
d'hypothèses : 2022 apparaît dans E04 (`D_raw`) ; 2020 et 2025
apparaissent dans la queue de `D_vol` ; toute la série a été vue
pour générer la piste.

Catégories possibles de réplication — **aucune n'est sélectionnée** :

| Catégorie | Idée | Limite |
|-----------|------|--------|
| Futur réellement non observé | Barres **après** la dernière date consultée pour générer l'hypothèse | Indisponible aujourd'hui sans nouvelle acquisition ; calendrier / source = autre décision |
| Autre instrument | Non utilisé pour générer I01 | Corrélation forte avec SPY possible ; ne « lave » pas un seuil appris sur SPY si on le réutilise |
| Autre univers | Autre classe d'actifs, autre géographie | Change la population : succès ou échec n'est plus le même objet |
| Séparation pré-enregistrée | Coupure temporelle ou d'état **annoncée avant** le premier calcul I02, sur des données éventuellement déjà stockées mais **non ré-analysées** pour I02 | Défendable seulement si la coupure n'est pas choisie pour isoler 2008/2009/2020 ; le sandbox actuel reste UNQUALIFIED |

Ne pas : choisir une source ; rouvrir DR-003 / DR-005 ; contacter un
fournisseur ; requalifier le cache yfinance.

DR-007 reste : exploratoire ≠ confirmatoire. Un I02 *exploratoire* sur
UNQUALIFIED, s'il est un jour autorisé, ne produit toujours aucun
SCI-PASS / SCI-FAIL.

---

## 6. Falsification / kill criteria

Qualitatif. **Aucun seuil numérique optimisé.**

Poursuivre I02 deviendrait inutile si, *après* définition ex ante et
sur l'information de réplication retenue, on observait notamment :

1. **Disparition** de l'effet annoncé sur information indépendante (H4).
2. Un **contrôle simple** d'amplitude / énergie **reproduit** l'effet
   attribué à L2 / à la structure de \(X\) (H2).
3. L'effet reste **porté par quelques événements** sans reproductibilité
   sous la condition \(C_t\) pré-enregistrée (H3 / artefact).
4. Le résultat **dépend** d'une définition de « stress » choisie après
   avoir regardé 2008 / 2009 / 2020 ou après avoir maximisé \(D\).
5. Le résultat est **entièrement** explicable par le comportement de la
   métrique (`H_vol` et queues de `‖Y‖`) sans structure de voisinage.
6. **Instabilité forte** à des choix raisonnables **pré-enregistrés**
   (pas : chercher le \(W\) qui sauve le récit).

Un kill n'est pas un SCI-FAIL d'I01. I01 exploratoire est déjà clos.

---

## 7. Stress / market condition — définition non résolue

**OPEN QUESTION.** Section obligatoire précisément parce que le mot
est tentant et contaminé.

Utiliser directement comme condition :

- les années **2008**, **2009**, **2020** ;
- ou un **seuil `rv_W`** (ou `‖X‖`) choisi après E04, y compris le
  « tertile haut » relu comme règle `if rv_W > q` ;

serait **circulaire**. Ces coupes ont **généré** l'hypothèse. Les
réutiliser comme définition opérationnelle, c'est apprendre le
découpage sur le même échantillon.

Principes qu'une définition future **devrait** respecter (sans choisir
la définition) :

| Principe | Sens |
|----------|------|
| Causalité | \(C_t\) fonction de \(\mathcal{O}_{\leq t}\) seulement |
| Disponibilité à \(t\) | Calculable après clôture de \(t\), avant \(Y_t\) |
| Avant expérimentation | Texte gelé **avant** le premier chiffre I02 |
| Indépendance maximale | Ne pas encoder 2008/2009/2020 ni maximiser \(D_{vol}\) |
| Simplicité | Une règle courte plutôt qu'un score ajusté |
| Interprétabilité | On doit pouvoir dire ce que \(C_t=1\) *prétend* être |
| Pas d'optimisation sur \(D\) | Interdit : grille de seuils, recherche du quantile qui « marche » |

Exemples de *familles* (non retenues) : indicateur de vol long terme
causal distinct de la fenêtre \(W\) d'I01 ; règle calendaire externe
pré-annoncée ; condition définie sur un **autre** univers puis appliquée
à l'univers de test. Chaque famille a des défauts. **Aucune n'est
choisie ici.**

---

## 8. Market-State / Regime Engine

**Aucun contrat empirique n'est dérivé d'I01.**

L'idée architecturale existait avant E04. E04 lui donne au plus un
*candidat de question*, pas une spécification.

I02, **s'il** est ultérieurement autorisé, pourra fournir ou non des
éléments pour spécifier ce contrat. Cette décision n'est pas anticipée.
Aucune architecture n'est modifiée par ce draft.

---

## 9. Before I02 can open

Décisions **humaines**. Tant que la dernière case n'est pas cochée :

**I02 = NOT OPENED.**

- [ ] Hypothèse finale approuvée (plus un point de départ à critiquer)
- [ ] Condition de marché \(C_t\) définie ex ante (§7)
- [ ] Comparateur(s) simple(s) définis ex ante (liste fermée)
- [ ] Observable futur défini
- [ ] Rôle de `H_shape` défini (témoin / mesure / non-gate)
- [ ] Kill criteria approuvés
- [ ] Stratégie de données indépendantes / réplication définie
- [ ] Risque de data snooping documenté (héritage I01 + holdout)
- [ ] Protocole de gel avant premier résultat défini
- [ ] Décision explicite **OPEN I02**

---

## 10. Revue de cohérence (auteur)

| Contrôle | Statut |
|----------|--------|
| Aucun chiffre nouveau calculé | oui — reprise E01–E04 / synthèse |
| Aucune donnée nouvelle téléchargée | oui |
| Aucun seuil proposé à partir d'E04 | oui — §7 refuse 2008/2009/2020 et tout cutoff `rv_W` |
| Aucun code de recherche I02 | oui |
| Aucun test expérimental I02 | oui |
| DR-003 / DR-005 non modifiés | oui |
| Aucun fournisseur contacté | oui |
| I01 reste CLOSED | oui (`116374b`) |
| I02 reste NOT OPENED | oui |

---

## Références (lecture, pas autorité de validation)

- [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)
- E01–E04 run reports ; revue E04
- [hypothesis.md](../I01/hypothesis.md), [protocol.md](../I01/protocol.md)
- [DR-007](../../docs/adr/DR-007-exploratory-vs-confirmatory-data.md)
- [DR-008](../../docs/adr/DR-008-i01-e01-exploratory-source.md)
