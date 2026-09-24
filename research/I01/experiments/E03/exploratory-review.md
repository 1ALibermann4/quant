# I01-E03 — Revue exploratoire humaine

> **Status :** RECORDED
> **Authority :** décision humaine (pas un gate logiciel)
> **Parent result :** [I01-E03-run-report.md](I01-E03-run-report.md) @ `0c2d355`
> **Classe :** EXPLORATORY / UNQUALIFIED

## Branche retenue

**CONTINUE EXPLORATORY — mécanisme non expliqué.**

Pas d'arrêt d'I01. Pas d'ouverture de DR-003 / DR-005. Pas de SCI-PASS.
Pas « géométrie validée ». Pas assez pour payer / qualifier des données
confirmatoires.

## Lecture

La chaîne « L2 matche `rv_W` → la vol persiste → futurs de même vol » **ne
tient pas**. Les voisins L2 ont 95,7 % de l'écart `rv_W` d'un candidat
ordinaire ; le témoin tombe à 7,7 %. Le clustering existe (contrôle `H_vol`
−41,9 %) mais n'explique pas le `H_raw` L2 (−13,7 % vs −2,2 %).

On ne conclut pas non plus à une « nouvelle structure prédictive ». On ne
sait toujours pas ce que L2 sélectionne.

Le 42,8 % de dates où L2 bat le contrôle, malgré une meilleure moyenne
`H_vol`, est la piste suivante : l'avantage est probablement asymétrique.

## Suite autorisée

**I01-E04 — Conditional Effect Anatomy.**

Étudier \(D_t = H_{vol}^{rv}(t) - H_{vol}^{L2}(t)\) (et l'équivalent
`H_raw`) : distribution, temps, état courant déjà disponible, stabilité
sur blocs **préfixés**. Aucune recherche de seuil. Aucun retuning.
