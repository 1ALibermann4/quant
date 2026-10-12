# I04-CAL HP-OPT — GPU Feasibility (L3)

**Date**: 2026-10-12  
**Host**: ASUS VivoBook (dev machine)

## Detected hardware

| Item | Value |
|------|-------|
| GPU | Intel(R) UHD Graphics |
| AdapterRAM (reported) | ~1 GiB |
| Driver | 30.0.100.9864 |
| CUDA | **Not available** (integrated Intel) |
| CPU | i5-1035G1 4C/8L |

## Evaluation

- Soft-DTW is a **banded DP** with sequential dependences along the anti-diagonal; GPU payoff requires large batched pairs + significant transfer amortization.
- No CUDA stack on this host; OpenCL/oneAPI would add large dependency and determinism risk.
- End-to-end G1 cell already drops to **seconds** on CPU+Numba for W=20 (see cell bench), so transfer+kernel init would likely dominate short cells.

## Decision

**REJECT GPU acceleration for I04-CAL production path on this class of hardware.**

Retain CPU Numba Soft-DTW + existing caches + ProcessPool workers.

OptiPlex: runner will snapshot GPU at first boot (`reports/hardware.json`). If discrete CUDA GPU appears, re-open GPU study; do not assume parity with ASUS.
