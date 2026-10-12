# I04-CAL HP-OPT — Rapport final (mandat)

## 1. État initial

- Branche de travail : `perf/I04-CAL-hp-opt` depuis `a268029`.
- CANONICAL-02 : **69 / 12096**, `config_hash=70e996a1…` (MATCH).
- PERF-02 déjà en place (cache, MP, self-term Soft-DTW) ; débit insuffisant.

## 2. Architecture

Pipeline `run_calibration` → workers spawn → `execute_cal_cell` → gates/géométries ; checkpoints atomiques ; allowlist bi-machine ; stop temporel opérationnel.

## 3. Profilage

Voir `HP-OPT-PROFILING.md`. Goulot historique : Soft-DTW G1. Post-Numba : G2/G5 pairwise (strides 8/4) redeviennent critiques.

## 4–5. Optimisations

| Essai | Retenu |
|-------|--------|
| Numba Soft-DTW + ref préservée | OUI |
| Cache PERF-02 | OUI |
| GPU Intel UHD | NON |
| Changement strides / oracles | NON (gelé) |

## 6. Mesures

Kernel Soft-DTW ~30–35× ; cellule G1 W20 ~1–9 s E2E. Artifacts JSON sous `research/I04/perf/`.

## 7. Qualification numérique

Tests `test_sdtw_numba` : égalité float64 (ε ≤ 3e-11). Suite runner PASS.

## 8. GPU

`HP-OPT-GPU.md` — REJECT.

## 9. Config CPU recommandée

`workers = n_logical - 1`, OMP/MKL/OPENBLAS=1, cache ON, Numba ON.

## 10–11. Projections

ASUS : 3 h pour l’univers restant **non garanti** (G2/G5). Bi-machine 16 h : maximiser cellules valides. OptiPlex : capacité inconnue → microbench au boot + `--capacity-optiplex`.

## 12–14. Runner / lancement / récupération

- ZIP : `dist/quant-I04-CAL-runner.zip` (+ `.sha256`)
- Lancement : `START_WINDOWS.cmd`
- Split : `config/allowlist_ASUS.txt` / `allowlist_OPTIPLEX.txt` (12027 restants, disjoint)
- Consolidation : `python -m quant.i04_cal.consolidate --out-dir … --source …`

## 15. Interruption / reprise

Smoke : resume 0.008 s sans recalcul ; `stopped_for_time=True` validé.

## 16. Fichiers principaux

- `src/quant/i04_cal/sdtw.py`, `geometries.py`, `pipeline.py`, `runtime.py`, `worker.py`
- `bimachine.py`, `consolidate.py`
- `scripts/pack_i04_cal_runner.py`, `profile_sdtw_hp.py`
- Rapports `research/I04/perf/HP-OPT-*.md`

## 17. Branche / commits

Branche `perf/I04-CAL-hp-opt`. Commits HP-OPT à suivre sur cette branche (ne pas écraser CANONICAL-02).

## 18. Limites

G2/G5 non encore accélérés au niveau Soft-DTW ; OptiPlex non qualifié ; contention CPU locale a biaisé certains benches familles.

## 19. Gouvernance

Aucune décision scientifique requise. Kaggle suspendu (décision déjà prise). Ne pas reprendre CANONICAL-02 sous un autre tip Git — merger via consolidate.

## 20. Verdict technique

**LIVRÉ pour usage bi-machine engineering** : moteur Numba qualifié, runner portable smoke-testé, split disjoint, consolidation fail-closed.  
**Non livré comme PASS scientifique I04-CAL** ni comme garantie « 3 heures ».
