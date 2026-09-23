# I01 — Hypothèses et objets mathématiques

> **Identifier :** I01-HYP-v0.1
> **Status :** OPEN
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1

---

## 1. Question scientifique

La première question quantitative du projet :

**La proximité géométrique entre deux états de marché apporte-t-elle de l'information
sur leurs comportements futurs — au-delà du hasard ?**

---

## 2. Hypothèses formelles

### H₀ (nulle)

La proximité géométrique n'apporte **aucune information supplémentaire** sur les futurs :

$$
\mathbb{E}\big[ \mathcal{H}(Y \mid N_k^{\text{geo}}(X_t)) \big]
=
\mathbb{E}\big[ \mathcal{H}(Y \mid N_k^{\text{B0}}(X_t)) \big]
$$

où $\mathcal{H}$ est une mesure d'hétérogénéité des futurs (§4) et $N_k^{\text{B0}}$ est
le voisinage contrôle aléatoire (baseline B0).

Équivalent opérationnel : la distribution des futurs conditionnée aux voisins géométriques
n'est **pas** significativement plus homogène que sous B0.

### H₁ (alternative)

Une distance faible implique des futurs plus homogènes :

$$
d(X_i, X_j) \text{ faible}
\quad \Rightarrow \quad
D(Y_i^{(h)}, Y_j^{(h)}) \text{ statistiquement plus faible}
$$

où $D$ mesure la dissimilarité entre trajectoires futures (§4).

**H₁ ne postule pas** un signe de rendement, un alpha tradable, ni une causalité —
seulement une **structure de similarité conditionnelle** dans les futurs.

---

## 3. Objets mathématiques

### 3.1 Temps et ensemble d'évaluation

- Calendrier de trading : $\mathcal{T} = \{t_1, \ldots, t_T\}$ (dates croissantes).
- Horizon futur : $h \in \mathbb{N}^+$ (jours de bourse).
- Chaque date $t \in \mathcal{T}_\text{eval}$ est un **point d'évaluation** (§5 du protocole).

### 3.2 État observable $X_t$

$$
X_t = \phi(\mathcal{O}_{\leq t})
$$

$X_t$ est la **représentation de l'information disponible au temps $t$**,
fonction des observations $\mathcal{O}_{\leq t}$ uniquement.

**Choix I01 v0.1 (minimal, classique) :**

Pour l'actif $a$ à la date $t$, soit $r_{t-w+1}, \ldots, r_t$ les rendements
logarithmiques quotidiens sur une fenêtre $W$ :

$$
r_\tau = \ln\frac{P_\tau}{P_{\tau-1}}
$$

où $P_\tau$ est le prix ajusté (splits/dividendes) connu à $t$.

Standardisation **causale** (paramètres estimés sur $\leq t$ uniquement) :

$$
\tilde{r}_\tau = \frac{r_\tau - \hat{\mu}_t}{\hat{\sigma}_t + \epsilon},
\quad \hat{\mu}_t, \hat{\sigma}_t \text{ calculés sur } [\max(t_0, t-M+1), t]
$$

Vecteur d'état :

$$
X_t^{(a)} = \big(\tilde{r}_{t-W+1}, \ldots, \tilde{r}_t\big) \in \mathbb{R}^W
$$

| Paramètre | Symbole | Valeur initiale | Rôle |
|-----------|---------|-----------------|------|
| Fenêtre d'état | $W$ | 20 | Forme récente de la trajectoire |
| Fenêtre standardisation | $M$ | 252 | Échelle locale comparable |
| Stabilisateur | $\epsilon$ | $10^{-8}$ | Éviter division par zéro |

**Justification du minimalisme :** I01 teste la **proximité géométrique**, pas la
richesse des features. Enrichir $X_t$ (volatilité, pente, etc.) = investigation I02+.

**Extension multi-actif (hors scope I01 v0.1) :** $X_t$ marché = concaténation ou
embedding cross-sectionnel — différé.

### 3.3 Futur observable $Y_t^{(h)}$

$$
Y_t^{(h)} = \psi\big(\mathcal{O}_{t+1:t+h}\big)
$$

**Choix I01 v0.1 :** vecteur des rendements log futurs :

$$
Y_t^{(h)} = (r_{t+1}, r_{t+2}, \ldots, r_{t+h}) \in \mathbb{R}^h
$$

**Scalarisation auxiliaire** (métrique secondaire) :

$$
y_t^{(h)} = \sum_{j=1}^{h} r_{t+j}
\quad \text{(rendement cumulé log sur l'horizon)}
$$

$Y_t^{(h)}$ n'est utilisé qu'**après** $t$ — jamais dans la construction de $X_t$.

### 3.4 Métrique $d$ sur l'espace des états

**Choix I01 v0.1 :** distance euclidienne :

$$
d(X_i, X_j) = \| X_i - X_j \|_2
$$

| Décision | Statut |
|----------|--------|
| Euclidean L2 | **Figé I01 v0.1** |
| Mahalanobis, cosinus, DTW | Différé I02+ |

La métrique est une **hypothèse scientifique**. Si I01 échoue sous L2, une investigation
ultérieure peut tester d'autres métriques — sans modifier rétroactivement I01.

### 3.5 Voisinage $N_k(X_t)$

$$
N_k^{\text{geo}}(X_t) = \arg\min_{S \subset \mathcal{L}_t,\ |S|=k} \sum_{j \in S} d(X_t, X_j)
$$

où $\mathcal{L}_t$ est la **bibliothèque historique admissible** au temps $t$ (§6 protocole).

En pratique : les $k$ états historiques $X_j$, $j \neq t$, minimisant $d(X_t, X_j)$.

| Paramètre | Symbole | Valeur initiale |
|-----------|---------|-----------------|
| Nombre de voisins | $k$ | 50 |

**Contraintes structurelles :**

- $j \notin \mathcal{E}_t$ (embargo temporel autour de $t$)
- $j < t$ strictement (pas de look-ahead)
- Un voisin = un instant historique distinct (pas de doublons de date)

### 3.6 Baseline B0 — $N_k^{\text{B0}}(X_t)$

$$
N_k^{\text{B0}}(X_t) \sim \text{Uniform}\big(\mathcal{L}_t,\ k\big)
$$

Tirage **uniforme sans remplacement** de $k$ dates dans $\mathcal{L}_t$,
**indépendamment** de $d(X_t, \cdot)$.

Même cardinalité $k$, même bibliothèque $\mathcal{L}_t$, mêmes contraintes d'embargo.
Seule la règle de sélection diffère.

**Nombre de répétitions Monte Carlo B0 :** $R = 200$ (moyenne des métriques sur R tirages).

---

## 4. Mesures de homogénéité / dissimilarité

### 4.1 Dissimilarité entre futurs $D(Y_i, Y_j)$

**Primaire (vectorielle) :**

$$
D(Y_i, Y_j) = \| Y_i^{(h)} - Y_j^{(h)} \|_2
$$

**Secondaire (scalaire, rendement cumulé) :**

$$
D_\text{sc}(y_i, y_j) = |y_i^{(h)} - y_j^{(h)}|
$$

### 4.2 Hétérogénéité d'un voisinage $\mathcal{H}$

Pour un voisinage $N$ de futurs $\{Y_j : j \in N\}$ :

**Métrique primaire SCI — variance mean pairwise distance :**

$$
\mathcal{H}_\text{mpd}(N) = \frac{2}{k(k-1)} \sum_{\substack{i,j \in N \\ i < j}} D(Y_i, Y_j)
$$

**Métrique auxiliaire — variance des rendements cumulés :**

$$
\mathcal{H}_\text{var}(N) = \mathrm{Var}_{j \in N}\big(y_j^{(h)}\big)
$$

**Métrique auxiliaire — IQR des rendements cumulés :**

$$
\mathcal{H}_\text{iqr}(N) = Q_{0.75} - Q_{0.25}
$$

### 4.3 Statistique de test par point d'évaluation

$$
\Delta_t = \mathcal{H}_\text{mpd}(N_k^{\text{B0}}(X_t)) - \mathcal{H}_\text{mpd}(N_k^{\text{geo}}(X_t))
$$

$\Delta_t > 0$ : les voisins géométriques produisent des futurs **plus homogènes**
(plus petit $\mathcal{H}$) que B0.

Agrégation sur $\mathcal{T}_\text{eval}$ : voir [protocol.md §7](protocol.md).

---

## 5. Ce que I01 ne teste pas

| Non-test | Raison |
|----------|--------|
| Signe ou magnitude du rendement | PRED / stratégie |
| Profit après coûts | ECON |
| Stabilité multi-régime | I02+ |
| Supériorité vs B2/B3 | Hors scope SCI initial |
| Optimalité de $(W, k, h)$ | Sensibilité documentée, pas optimisée pour PASS |

---

## 6. Succès / échec conceptuel

| Verdict SCI | Interprétation |
|-------------|----------------|
| **PASS** | H₀ rejetée avec contrôles satisfaits — information géométrique détectée |
| **FAIL** | Pas de gain significatif vs B0 — proximité L2 non informative (I01) |
| **INCONCLUSIVE** | Protocole ou données insuffisants — pas de conclusion |

Un **FAIL** est un **résultat scientifique valide** : il empêche de construire une
stratégie sur une proximité L2 naïve.

---

## Références

- [protocol.md](protocol.md) — protocole opérationnel
- [configuration.yaml](configuration.yaml) — valeurs numériques
