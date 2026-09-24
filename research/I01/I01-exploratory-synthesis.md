# I01 — Synthèse exploratoire

> **Identifier :** I01-EXPLORATORY-SYNTHESIS
> **Status :** EXPLORATORY COMPLETE
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Classe données :** UNQUALIFIED (DR-007 / DR-008)
> **Calculs :** aucun — ce document relit E01–E04
> **Baseline résultats :** E04 @ `4a920c3`

## Verdict humain

```text
EXPLORATORY COMPLETE
ORIGINAL HYPOTHESIS NOT RECOMMENDED FOR CONFIRMATION
REGIME-CONDITIONAL PHENOMENON IDENTIFIED
```

Ce n'est **pas** un SCI-PASS. Ce n'est **pas** un SCI-FAIL (DR-007).
Ce n'est **pas** un DATA-PASS. Aucune promotion PRED / ECON / OPS.

**Pas de DR-003 / DR-005 pour confirmer I01 maintenant.**
**Pas d'E05.** Pas de retuning. Pas d'acquisition payante.

$$
\text{observations I01} \neq \text{preuve de la nouvelle hypothèse}
$$

E01–E04 ont **généré** une hypothèse candidate. Ils ne peuvent pas aussi
la valider.

---

## Chaîne, sans enjoliver

```text
E01  effet global observé vs B0
 ↓
E02  dominé par la volatilité future, pas la forme
 ↓
E03  pas expliqué par un matching simple de rv_W
 ↓
E04  fortement conditionnel au stress / régime
 ↓
────────────────────────────
EXPLORATORY COMPLETE
```

### E01 — un effet moyen existe

Sur le sandbox SPY / yfinance 1.6.0 / daily (UNQUALIFIED), les voisins L2
ont en moyenne des futurs plus homogènes que B0 :

| | L2 vs B0 |
|--|--|
| `H_raw` | −13,7 % |
| `H_vol` | −54,0 % |
| `H_shape` | −0,21 % |

`Δ > 0` n'était pas une preuve. C'était une raison de diagnostiquer.

### E02 — pas « mêmes trajectoires »

L'effet concerne surtout l'amplitude / volatilité future. `H_shape` est
plat. `Δ_raw` suit `Δ_vol` (corr. 0,762), pas `Δ_shape` (0,009). L'intuition
« même passé → formes futures similaires » était déjà trop générale.

L'effet raw n'était pas un artefact de deux crises isolées *contre B0*
(32/33 années `Δ_raw > 0`). E04 montrera que **contre le contrôle `rv_W`**,
l'histoire est autre.

### E03 — pas du clustering déguisé en L2

Les voisins L2 ont **95,7 %** de l'écart `rv_W` d'un candidat ordinaire.
Le témoin qui matche `rv_W` tombe à **7,7 %**. Le contrôle fonctionne.

La persistance existe (`rv_W ↔ ‖Y‖` : 0,671 ; contrôle `H_vol` −41,9 %).
Elle n'explique pas le `H_raw` L2 (−13,7 % vs −2,2 % pour le contrôle).
L2 atteint −54 % sur `H_vol` **sans** matcher `rv_W`.

On ne pouvait pas conclure à une « nouvelle structure prédictive ». On ne
savait pas ce que L2 sélectionnait.

### E04 — où se cache l'avantage vs `rv_W`

\(D_t = H^{rv}(t) - H^{L2}(t)\).

| | `D_vol` | `D_raw` |
|--|---------|---------|
| moyenne | +4.09e-5 | +0.00524 |
| médiane | **−1.52e-5** | +0.00226 |
| asymétrie | **+7,44** | +2,78 |
| part `D>0` | **42,8 %** | 56,0 % |
| top 1 % des dates / `∑D` | **77 %** | 22 % |
| plus grosse année | **2008 (37 %)** | 2008 (18 %) |

La moyenne `H_vol` vs contrôle racontait une histoire incomplète. La date
typique, L2 n'est **pas** meilleur que `rv_W` sur cette métrique. Une queue
droite — 2008, 2009, 2020, tertile descriptif `rv_W` haut — fait basculer
la moyenne. La décennie préfixée **2010–2019** a une moyenne `D_vol` et
`D_raw` **négative**.

Ce n'est pas :

```text
1995 + petit effet … 2025 + petit effet
```

C'est plus proche de :

```text
marché ordinaire  →  rv_W souvent aussi bon / meilleur sur H_vol
stress important  →  parfois énorme avantage L2 (2008, 2009, 2020)
```

Les tertiles à effectif égal (non optimisés) montrent un gradient d'état.
**Ce n'est pas** `if rv_W > threshold: use L2`. Ce seuil serait appris sur
les mêmes données.

---

## Ce qui est tranché / ce qui ne l'est pas

### Hypothèse originale — non recommandée à la confirmation

Forme essentielle :

$$
X_s \approx X_t \Rightarrow Y \text{ plus homogènes}
$$

L'exploration ne la soutient pas assez pour justifier le coût d'une
réplication confirmatoire **telle quelle**. L'effet vs B0 est réel sur ce
sandbox ; l'effet vs un contrôle de vol est conditionnel, à queue lourde,
et absent en moyenne sur une décennie préfixée. `H_shape` n'a presque pas
bougé.

Le protocole I01 v0.2 (voisinage, B0, gates SCI) **reste** le protocole
pré-enregistré. On ne le « corrige » pas après coup. On **ne l'exécute
pas** en confirmatoire maintenant.

### Résultat négatif important

Pas de similarité notable de **forme** future (`H_shape`).

### Résultat mécanistique

Un matching simple de volatilité passée (`rv_W`) est insuffisant pour
expliquer L2. L2 n'est pas ce contrôle.

### Résultat conditionnel

L'avantage moyen `H_vol` face au contrôle est fortement concentré dans une
queue et dans des épisodes de stress. La médiane est négative.

### Hypothèse candidate — non testée

$$
\text{état de stress} + \text{structure de } X_t
\Rightarrow
\text{information potentielle sur le régime de volatilité futur}
$$

Ce n'est plus I01. Si on la poursuit, ce sera une **nouvelle investigation**
(probablement I02), question définie **avant** tout nouveau calcul.

I02 n'est **pas** ouvert par ce document.

---

## Ce que cette séquence a réussi méthodologiquement

Un backtest moins discipliné aurait vu `H_vol −54 %` et conclu que « la
géométrie prédit très bien la volatilité ». E04 montre que, face au
contrôle `rv_W`, la **médiane est négative**. Quelques épisodes produisent
des gains qui font basculer la moyenne. C'est le rôle des diagnostics
prébornés : empêcher la moyenne globale de raconter seule l'histoire.

On arrête d'interroger E01 jusqu'à obtenir l'histoire souhaitée. On prend
ce qu'il a appris. On formule éventuellement une autre question.

## Interdictions qui restent

- SCI-PASS / SCI-FAIL / PRED / ECON à partir d'E01–E04
- confirmer I01 sans nouveau protocole et sans données qualifiées
- rouvrir DR-003 / DR-005 « pour I01 »
- E05, E06, E07 sur le même run
- chercher un seuil de `rv_W` sur ces dates
- qualifier yfinance (DR-003 L-13)
- trading, broker, capital

## Suite (hors de ce document)

Toute poursuite = nouvelle investigation, hypothèse pré-enregistrée.
Choix data (même sandbox + holdout, ou C02 qualifié) = décision **de
cette** investigation, pas d'E05.

Rapports : [E01](experiments/E01/I01-E01-run-report.md),
[E02](experiments/E02/I01-E02-run-report.md),
[E03](experiments/E03/I01-E03-run-report.md),
[E04](experiments/E04/I01-E04-run-report.md).
