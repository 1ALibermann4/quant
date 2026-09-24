# I01-E02 — Revue exploratoire humaine

> **Status :** RECORDED
> **Authority :** décision humaine (pas un gate logiciel)
> **Parent result :** [I01-E02-run-report.md](I01-E02-run-report.md) @ `8ebe32d`
> **Classe :** EXPLORATORY / UNQUALIFIED

## Branche retenue

**Phénomène suffisamment intéressant pour poursuivre l'investigation**, mais
**pas encore prêt pour une réplication confirmatoire**.

Pas d'ouverture de DR-003 / DR-005. Pas d'achat. Pas de retuning `W/k/h/L2/B0`.
Pas de SCI-PASS / SCI-FAIL.

## Lecture

E01 pouvait suggérer une similarité générale des futurs. E02 précise :

```text
proximité des passés  →  forte homogénéité de volatilité future
proximité des passés  →  similarité de forme future   (quasi-nul)
```

`H_raw` (+13,7 % vs B0) est potentiellement trompeur lu seul : il suit `H_vol`
(corr. 0,762) et non `H_shape` (0,009).

Ce n'est pas un résultat vide. Caractériser la volatilité future à partir de
la géométrie des états serait déjà une propriété structurelle. Ce n'est
peut-être pas le phénomène initialement attendu.

## Suite autorisée

**I01-E03 — Volatility Mechanism Diagnostic.**

Question : la distance L2 sur les 20 rendements standardisés sélectionne-t-elle
des futurs de volatilité similaire *au-delà* d'une information de volatilité
déjà présente dans `X_t` / la fenêtre passée ?

Un contrôle diagnostique fondé sur la volatilité passée compare
descriptivement l'homogénéité future à celle des voisins L2. Ce contrôle
**n'est pas** un nouveau B0 et ne remplace pas B0.
