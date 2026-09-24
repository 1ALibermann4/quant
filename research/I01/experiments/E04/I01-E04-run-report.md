# I01-E04 — Anatomie conditionnelle de \(D_t\)

> **EXPLORATORY / UNQUALIFIED / NOT SCIENTIFICALLY PROMOTABLE**
>
> \(D_t = H^{rv}(t) - H^{L2}(t)\) (positif ⇒ L2 plus homogène que le contrôle).
> Paramètres **figés**. Blocs **préfixés**. Aucun seuil recherché.
> Ce n'est pas un classifieur de régimes.

| Champ | Valeur |
|-------|--------|
| Parent | I01-E03 (revue : CONTINUE — mécanisme non expliqué) |
| Cache | même téléchargement UNQUALIFIED (2026-09-24T12:00:16Z) |
| `T_eval` | 8038 |
| Blocs temps | tertiles chrono de `T_eval` ; décennies 1994–1999 / 2000–2009 / 2010–2019 / 2020–2026 |
| État | tertiles à effectif égal de `rv_W`, `‖X‖`, somme de la fenêtre `W` |

Les moyennes `D` reproduisent E03 (`H_vol` contrôle − L2 = +4.09e-5 ; `H_raw` +0.00524).

## 1. Distribution — le paradoxe 42,8 %

| | `D_vol` | `D_raw` |
|--|---------|---------|
| moyenne | **+4.09e-5** | **+0.00524** |
| médiane | **−1.52e-5** | +0.00226 |
| moyenne − médiane | +5.61e-5 | +0.00297 |
| asymétrie | **+7,44** | +2,78 |
| part `D>0` | **42,8 %** | 56,0 % |
| q10 / q90 | −1.35e-4 / +1.77e-4 | −0.012 / +0.025 |
| min / max | −8.15e-4 / +4.28e-3 | −0.025 / +0.146 |

**Observation `D_vol` :** la date typique a `D_vol < 0` (L2 *moins* homogène
que le contrôle). La moyenne positive vient d'une queue droite. C'est
exactement le schéma « beaucoup de dates L2 ≈ ou > contrôle, quelques dates
L2 ≪≪≪ contrôle ».

**Observation `D_raw` :** moyenne et médiane sont du même signe. L'avantage
brut est plus « typique » que l'avantage `H_vol`, avec une queue plus
modérée.

## 2. Temps — pas un brouillard de trente ans

Part de `sum(D)` :

| | `D_vol` | `D_raw` |
|--|---------|---------|
| top 1 % des dates | **76,9 %** | 21,8 % |
| top 5 % des dates | **136 %** | 55,3 % |
| plus grosse année | **2008 (37,2 %)** | 2008 (18,3 %) |

(Une part > 100 % est possible : des années négatives compensent.)

Années qui portent le plus `D_vol` : **2008 (37 %)** , **2020 (28 %)** ,
**2009 (21 %)**. Trois années de stress portent l'essentiel de la somme.

Décennies préfixées, `D_vol` :

| bloc | moyenne | médiane | part `D>0` |
|------|---------|---------|------------|
| 1994–1999 | +1.7e-5 | +1.6e-6 | 53 % |
| 2000–2009 | +7.1e-5 | −1.5e-5 | 45 % |
| 2010–2019 | **−1.8e-5** | −3.4e-5 | 33 % |
| 2020–2026 | +1.0e-4 | −8.9e-6 | 47 % |

Tertiles chrono : moyenne toujours positive ; médiane positive seulement
dans le premier tiers. Le phénomène **n'est pas** stable date par date sur
les trois blocs.

`D_raw` : positif et fréquent en 1994–2009 ; **négatif en moyenne** sur
2010–2019 ; de nouveau positif en 2020–2026 (porté par 2020 et 2022).

## 3. État courant — tertiles à effectif égal (pas un seuil optimal)

Ce sont des rangs en trois, fixés *a priori*. On n'a **pas** cherché le
seuil de `rv_W` qui maximise `D`.

`D_vol` selon `rv_W` :

| tertile | moyenne | médiane | part `D>0` |
|---------|---------|---------|------------|
| bas | −4.6e-5 | −4.4e-5 | 23 % |
| milieu | ≈ 0 | −7.6e-6 | 46 % |
| haut | **+1.7e-4** | +2.9e-5 | 59 % |

Même gradient, plus net, sur `D_raw` : tertile `rv_W` haut +0.022 (98 %
positifs) ; tertile bas −0.0077 (14 % positifs). `‖X‖` haut va dans le
même sens. La somme de fenêtre est plus faible et non monotone.

**Observation :** l'écart L2 − contrôle se manifeste surtout lorsque la
volatilité *courante* de la fenêtre `W` est déjà élevée. Ce n'est pas une
règle de trading. Ce n'est pas un régime classifié.

## 4. Lecture pour la décision humaine

E04 répond à « où et quand » sans dire *pourquoi* L2 gagne ces jours-là.

Faits durs, non tranchés :

1. L'avantage moyen `H_vol` vs `rv_W` n'est **pas** un gain diffus : médiane
   négative, 1 % des dates portent 77 % de la somme.
2. Il se concentre sur des années de stress (2008, 2009, 2020) et, dans
   une coupe descriptive, sur les tertiles `rv_W` / `‖X‖` hauts.
3. `D_raw` est plus souvent positif (56 %, médiane > 0) mais suit les
   mêmes années et le même gradient d'état ; il disparaît en moyenne dans
   les années 2010.
4. 2010–2019 est un contre-exemple temporel préfixé : moyenne `D_vol` et
   `D_raw` négatives.

## Ce que E04 n'autorise pas

- chercher un seuil de `rv_W` qui « marche mieux » ;
- inventer I02, changer `W`, `k`, `h`, L2, B0 ;
- un SCI-PASS / SCI-FAIL ;
- E05 automatique ;
- rouvrir DR-003 / DR-005 par automatisme ;
- du trading.

## Décision (humaine, pas ce rapport)

```text
E04
 ├── écart diffus et récurrent     → geler l'exploratoire I01 ;
 │                                   décider ensuite si le coût
 │                                   confirmatoire se justifie
 ├── écart porté par peu d'épisodes → artefact conditionnel probable ;
 │                                   confirmation coûteuse peu justifiée
 └── autre lecture                 → investigation documentée
                                     (pas un retuning silencieux)
```

Ce rapport **ne choisit pas** la branche.

Figure hors git : `data/exploratory/UNQUALIFIED_e04_d_by_year.png`.
