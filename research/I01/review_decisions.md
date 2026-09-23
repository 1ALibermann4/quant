# I01 — Décisions de revue (post REV v0.1)

> **Identifier :** I01-DECISIONS-v0.1
> **Status :** ACCEPTED
> **Authority class :** RESEARCH
> **Protocol :** QDP v0.1
> **Source review :** `evaluation_protocol_review.md` @ `d9481b5`

Décisions humaines enregistrées **avant** modification normative du protocole.

---

## Décisions P0 (tranchées)

| ID | Sujet | Décision retenue | REV résolu |
|----|-------|------------------|------------|
| **DEC-01** | Inférence SCI-001 | **Block bootstrap temporel** comme méthode confirmatoire principale. T-test iid **interdit** comme gate. $L_\min \geq \max(W,h)$ ; sensibilité de $L$ pré-enregistrée ; jamais choisir $L$ selon p-value ; verdict instable → INCONCLUSIVE | REV-08, REV-09 |
| **DEC-02** | Ensemble admissible | **Hard constraint** $s + h \leq t$ dans $\mathcal{L}_t$, indépendamment de l'embargo. Invariant impl : `candidate.future_end <= query.information_cutoff` | REV-07 |
| **DEC-03** | Homogénéité | **$H_\text{raw}$** (L2 brute) = endpoint confirmatoire SCI-001 v0.1. **$H_\text{vol}$** et **$H_\text{shape}$** = diagnostics obligatoires pré-enregistrés, **non substituables** pour PASS | REV-11 |
| **DEC-04** | Standardisation $X_t$ | Observation **après clôture** de $t$. $\hat{\mu}_t, \hat{\sigma}_t$ sur $[t-M+1, t]$ **inclusif** ($r_t$ inclus). $Y_t$ commence à $t+1$ | REV-01, REV-02 |
| **DEC-05** | Profondeur historique | ~1 500 séances = **minimum technique** ; **≥ 10 ans** = exigence cible inférence confirmatoire ; 15–20 ans si disponible sans changer méthodologie | REV-15 |

---

## Décisions P1 (tranchées avec le protocole révisé)

| ID | Sujet | Décision retenue | REV résolu |
|----|-------|------------------|------------|
| **DEC-06** | Chevauchement $Y$ inter-voisins | **Diagnostic obligatoire** : distribution $|i-j|$ dans $N^\text{geo}$ vs $N^\text{B0}$ ; pas de contrainte $|i-j| \geq h$ en v0.1 | REV-06 |
| **DEC-07** | Taille bibliothèque | $|\mathcal{L}_t| \geq L_\min$ avec $L_\min = 3k = 150$ pour $t \in \mathcal{T}_\text{eval}$ | REV-10 |
| **DEC-08** | Usage split train | Train **descriptif uniquement** ; interdiction modifier gates/seuils/métriques après observation test | REV-13 |
| **DEC-09** | Rôles des gates | Primaire : SCI-001 ; Confirmatoire : SCI-002, SCI-004 ; Diagnostique : SCI-003, SCI-DIAG-*, SCI-AUX-* | REV-14 |
| **DEC-10** | Embargo justification | Corriger texte : $t-s \geq \tau+1 \geq W+1$ ⇒ **zéro** rendement commun entre fenêtres $X$ | REV-05 |
| **DEC-11** | Sélection voisins | Invariant AF-08 : sélection = fonction de $X$ uniquement | REV-04 |
| **DEC-12** | Portée SCI PASS | Texte normatif strict (voir protocol.md §8) | REV-20 |
| **DEC-13** | Falsifiabilité | Protocole versionné avant snapshot ; interdiction post-hoc metric/param/date subset | REV-18 |
| **DEC-14** | Reproductibilité | Tri dates stable ; seeds figées ; tolérance float $10^{-10}$ ; versions deps dans artefacts | REV-19 |
| **DEC-15** | adjusted_close | Exigences C02 documentées dans protocol §9 ; détail fournisseur → DATA-REQ | REV-17 |
| **DEC-16** | Non-stationnarité | Limitation assumée ; SCI PASS ne prouve pas stationnarité | REV-16 |

---

## Non modifié en v0.1

| Sujet | Report |
|-------|--------|
| B0 stratifié par vol | I01-bis si nécessaire |
| Contrainte $|i-j| \geq h$ sur voisins | Diagnostic seulement |
| Point-in-time prices | DATA-REQ / ADR data |
