# I01 — Hypothèses et objets mathématiques

> **Identifier :** I01-HYP-v0.2
> **Status :** ACCEPTED
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Decisions :** [review_decisions.md](review_decisions.md)

---

## 1. Question scientifique

La première question quantitative du projet :

**La proximité géométrique entre deux états de marché apporte-t-elle de l'information
sur leurs comportements futurs — au-delà du hasard ?**

---

## 2. Hypothèses formelles

### H₀ (nulle)

La proximité géométrique n'apporte **aucune information supplémentaire** sur l'homogénéité
L2 brute des futurs :

$$
\mathbb{E}\big[ \mathcal{H}_\text{raw}(Y \mid N_k^{\text{geo}}(X_t)) \big]
=
\mathbb{E}\big[ \mathcal{H}_\text{raw}(Y \mid N_k^{\text{B0}}(X_t)) \big]
$$

où $\mathcal{H}_\text{raw}$ est la mean pairwise L2 (§4.2) et $N_k^{\text{B0}}$ la baseline B0.

### H₁ (alternative)

Une distance faible implique des futurs plus homogènes (L2 brute) :

$$
d(X_i, X_j) \text{ faible}
\quad \Rightarrow \quad
D(Y_i^{(h)}, Y_j^{(h)}) \text{ statistiquement plus faible}
$$

où $D(Y_i,Y_j) = \|Y_i^{(h)} - Y_j^{(h)}\|_2$.

**H₁ ne postule pas** un signe de rendement, un alpha tradable, ni une causalité —
seulement une **structure de similarité conditionnelle** dans les futurs bruts.

---

## 3. Convention temporelle (DEC-04)

> **I01 observe le marché après la clôture de la séance $t$.**

- $P_t$ et $r_t = \ln(P_t/P_{t-1})$ sont **connus** et appartiennent à $\mathcal{O}_{\leq t}$.
- $X_t$ est construit avec cette information.
- $Y_t^{(h)}$ commence **strictement** à $t+1$ : $(r_{t+1}, \ldots, r_{t+h})$.

Cette convention est normative pour I01 v0.1 (daily). Toute extension intraday
requerra un nouveau protocole.

---

## 4. Objets mathématiques

### 4.1 Temps et ensemble d'évaluation

- Calendrier : $\mathcal{T} = \{t_1, \ldots, t_T\}$ (dates croissantes).
- Horizon : $h = 10$ jours de bourse (figé v0.1).
- Points d'évaluation :

$$
\mathcal{T}_\text{eval} = \left\{ t \in \mathcal{T} :
  X_t \text{ valide},\ Y_t^{(h)} \text{ complet},\ |\mathcal{L}_t| \geq L_\min \right\}
$$

avec $L_\min = 3k$ (DEC-07).

### 4.2 État observable $X_t$

$$
X_t = \phi(\mathcal{O}_{\leq t})
$$

Rendements log :

$$
r_\tau = \ln\frac{P_\tau}{P_{\tau-1}}, \quad P_\tau \text{ adjusted close connu à } t
$$

Standardisation causale **inclusive de $r_t$** (DEC-04) :

$$
\hat{\mu}_t = \frac{1}{M}\sum_{u=t-M+1}^{t} r_u,
\quad
\hat{\sigma}_t = \sqrt{\frac{1}{M-1}\sum_{u=t-M+1}^{t}(r_u - \hat{\mu}_t)^2}
$$

$$
\tilde{r}_u = \frac{r_u - \hat{\mu}_t}{\hat{\sigma}_t + \epsilon},
\quad u \in [t-W+1, t]
$$

$$
X_t = (\tilde{r}_{t-W+1}, \ldots, \tilde{r}_t) \in \mathbb{R}^W, \quad W=20,\ M=252,\ \epsilon=10^{-8}
$$

### 4.3 Futur observable $Y_t^{(h)}$

$$
Y_t^{(h)} = (r_{t+1}, r_{t+2}, \ldots, r_{t+h}) \in \mathbb{R}^h
$$

Scalarisation auxiliaire :

$$
y_t^{(h)} = \sum_{j=1}^{h} r_{t+j}
$$

$Y_t^{(h)}$ n'intervient **jamais** dans la sélection des voisins (AF-08).

### 4.4 Métrique $d$

$$
d(X_i, X_j) = \| X_i - X_j \|_2 \quad \text{(L2, figé v0.1)}
$$

### 4.5 Bibliothèque admissible $\mathcal{L}_t$ (DEC-02)

$$
\mathcal{L}_t = \left\{ s \in \mathcal{T} :
  s < t,\quad
  s \notin \mathcal{E}_t,\quad
  s + h \leq t,\quad
  X_s \text{ valide},\ Y_s^{(h)} \text{ valide}
\right\}
$$

Embargo :

$$
\mathcal{E}_t = \{ s : |s - t| \leq \tau \}, \quad \tau = W = 20
$$

**Invariant anti-look-ahead (impl)** :

```text
candidate.future_end <= query.information_cutoff
```

où `candidate.future_end = s + h` et `query.information_cutoff = t`.

Avec $\tau=W$ : $t-s \geq 21 > W-1$ ⇒ **zéro** rendement commun entre fenêtres $X_t$ et $X_s$.

### 4.6 Voisinage $N_k^{\text{geo}}(X_t)$

Les $k=50$ dates $s \in \mathcal{L}_t$ minimisant $d(X_t, X_s)$ (ties : date la plus ancienne).

### 4.7 Baseline B0

$k$ dates tirées uniformément sans remplacement dans $\mathcal{L}_t$, indépendamment de $d$.
Moyenne Monte Carlo sur $R=200$ tirages (seed figée).

---

## 5. Mesures d'homogénéité (DEC-03)

Pour un voisinage $N$ de cardinalité $k$, futurs $\{Y_j : j \in N\}$ :

### 5.1 $\mathcal{H}_\text{raw}$ — endpoint confirmatoire SCI-001

$$
D_\text{raw}(Y_i,Y_j) = \| Y_i^{(h)} - Y_j^{(h)} \|_2
$$

$$
\mathcal{H}_\text{raw}(N) = \frac{2}{k(k-1)} \sum_{i<j} D_\text{raw}(Y_i, Y_j)
$$

(Anciennement $\mathcal{H}_\text{mpd}$ — alias conservé dans artefacts.)

### 5.2 $\mathcal{H}_\text{vol}$ — diagnostic obligatoire (non gate)

Amplitude future par voisin : $v_j = \|Y_j^{(h)}\|_2$.

$$
\mathcal{H}_\text{vol}(N) = \mathrm{Var}_{j \in N}(v_j)
$$

Interprétation : homogénéité de **volatilité/amplitude** future dans le voisinage.

### 5.3 $\mathcal{H}_\text{shape}$ — diagnostic obligatoire (non gate)

Trajectoire normalisée : $\hat{Y}_j = Y_j / (\|Y_j\|_2 + \epsilon)$.

$$
D_\text{shape}(\hat{Y}_i,\hat{Y}_j) = \| \hat{Y}_i - \hat{Y}_j \|_2
$$

$$
\mathcal{H}_\text{shape}(N) = \frac{2}{k(k-1)} \sum_{i<j} D_\text{shape}(\hat{Y}_i, \hat{Y}_j)
$$

Interprétation : homogénéité de **forme** indépendamment de l'échelle.

### 5.4 Statistique $\Delta_t$ (endpoint SCI-001)

$$
\bar{\mathcal{H}}_\text{B0,raw}(t) = \frac{1}{R}\sum_{r=1}^{R} \mathcal{H}_\text{raw}(N_{k,r}^{\text{B0}})
$$

$$
\Delta_t^\text{raw} = \bar{\mathcal{H}}_\text{B0,raw}(t) - \mathcal{H}_\text{raw}(N_k^{\text{geo}})
$$

$\Delta_t^\text{raw} > 0$ ⇔ voisins géométriques **plus homogènes** (L2 brute) que B0.

Diagnostics analogues : $\Delta_t^\text{vol}$, $\Delta_t^\text{shape}$ — **jamais** utilisés pour PASS/FAIL SCI-001.

### 5.5 Lecture croisée (interprétation, pas gate)

| Pattern | Lecture scientifique |
|---------|---------------------|
| raw ✓, vol ✓, shape ✗ | Info sur **régime d'amplitude** futur, pas forme |
| raw ✓, vol faible, shape ✓ | Suspicion d'info **structurelle** sur trajectoires |
| raw ✗ | Proximité L2 non informative (endpoint) |

---

## 6. Inférence (DEC-01)

Série $\{\Delta_t^\text{raw}\}$ sur split **test** — **dépendance temporelle assumée**.

Gate SCI-001 : **block bootstrap temporel** (pas t-test iid).

- Longueur bloc $L \geq L_\min = \max(W,h) = 20$
- Sensibilité pré-enregistrée sur $L$ ; **jamais** choisir $L$ selon p-value
- Instabilité du verdict → **INCONCLUSIVE**

Détail : [protocol.md §7](protocol.md).

---

## 7. Ce que I01 ne teste pas

| Non-test | Raison |
|----------|--------|
| Signe / alpha | PRED |
| Profit | ECON |
| Stationnarité globale | NOTE — limitation assumée |
| Optimalité $(W,k,h,L)$ | Sensibilité diagnostic |

---

## 8. Portée d'un SCI PASS (DEC-12)

Un **SCI PASS** autorise **uniquement** :

> Pour l'instrument et la période testées, avec $X_t$ défini §4.2, $d$ L2, $h=10$,
> la règle k-NN produit un voisinage dont $\mathcal{H}_\text{raw}$ est significativement
> inférieure à B0 sous block bootstrap, anti-fuite validée.

**N'autorise pas** : similarité de forme (sauf diagnostic shape), PRED, ECON, trading.

---

## Références

- [protocol.md](protocol.md)
- [configuration.yaml](configuration.yaml)
- [review_decisions.md](review_decisions.md)
