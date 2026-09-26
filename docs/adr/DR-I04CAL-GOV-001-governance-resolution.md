# Decision Record: I04-CAL Governance Resolution (GOV-I04CAL-001)

**Status**: ACCEPTED
**Date**: 2026-09-26
**Context**: I04-CAL synthetic structural calibration
**Decision**: Restore scientific contract after implementation drift

---

## Context

### Background
I04-CAL is a synthetic structural calibration bench designed to qualify measurement machinery before any I04 market screening. The implementation was interrupted by an external quota limit, requiring a takeover audit.

### Takeover Audit Findings
The forensic audit identified two critical scientific contract drifts introduced during Cursor implementation:

1. **Stride Contract Drift (GOV-01)**:
   - Original frozen contract: QUERY_STRIDE=8, CANDIDATE_STRIDE=4
   - Implementation drift: Changed to 16/16 for performance
   - Retroactive spec update to document 16/16 as "preregistered"
   - Scientific impact: Alters query density, candidate pool, estimator variance/bias, cross-geometry comparability

2. **Numerical Calibration Threshold Drift (GOV-02)**:
   - Original contract: C1–C10 referenced but not numerically operationalized
   - Implementation drift: Arbitrary thresholds (0.4, 0.25, 0.2, 0.25 observability) introduced
   - These thresholds controlled CAL-PASS/CAL-FAIL decisions
   - Violated INV-07 (calibration should establish thresholds, not pre-invent them)

### Governance Authority
The human authority (GOV-I04CAL-001) reviewed the takeover audit and provided explicit resolutions for each identified drift.

---

## Decision

### GOV-01: Stride Contract Resolution

**Decision**: RESTORE the original frozen contract.

**Authorized Configuration**:
- Core geometries: QUERY_STRIDE=8, CANDIDATE_STRIDE=4
- G1 Soft-DTW: QUERY_STRIDE=32, CANDIDATE_STRIDE=32

**Rationale**:
- The 16/16 change was introduced for performance after the scientific freeze
- It changes query density, candidate pool, estimator variance/bias, neighborhood composition
- G1 32/32 remains authorized because it was part of the original frozen contract

**Implementation**:
- Revert `src/quant/i04_cal/params.py` to original stride values
- Revert retroactive spec update in `I04-CAL-SPEC-v0.2.md`
- Document history transparently in spec governance section
- Document G1's different sampling density as a limitation

**Constraint**: Do not solve runtime problems by further changing scientific sampling. Use exact semantics-preserving optimizations instead.

---

### GOV-02: Numerical Calibration Threshold Resolution

**Decision**: REMOVE all unpreregistered numerical thresholds from scientific qualification logic.

**Affected Thresholds**:
- Contrast < 0.4
- Fraction < 0.25
- Nuisance threshold > 0.2
- Observability Spearman >= 0.25

**Rationale**:
- I04-CAL exists to measure/calibrate these distributions
- Pre-inventing thresholds contradicts the calibration purpose
- INV-07 explicitly rejected arbitrary pre-CAL thresholds

**Implementation**:
- Rewrite `assess.py` to report raw/distributional statistics only
- Remove threshold-based CAL-PASS/CAL-FAIL logic
- Remove automatic VALID/INVALID based on observability threshold
- Report: values, distributions, quantiles, W sensitivity, parameter sensitivity, null behavior, nuisance associations, observability diagnostics, CAL-6 diagnostics
- Status: "CALIBRATION DATA COMPLETE, SCIENTIFIC QUALIFICATION PENDING GOVERNANCE"

**Constraint**: Thresholds may remain only if clearly renamed as LEGACY_DIAGNOSTIC_ONLY with zero effect on scientific status. Prefer complete removal.

---

### GOV-03: Execution Tier Resolution

**Decision**: AUTHORIZED as a performance mechanism only.

**Authorized Partition**:
- Tier A: G0, G3, G4, G7, GORD
- Tier B: G1, G2, G5

**Rationale**:
- Tiers exist for compute tractability and scheduling
- No scientific hierarchy between tiers
- The frozen benchmark remains the UNION of all authorized families

**Implementation**:
- Clarify in `CalConfig` docstring that tiers are performance-only
- Document that completed Tier A does not imply complete scientific benchmark
- Tiers may be run separately as independent artifacts

**Constraint**: Do not define Tier A as "scientifically required" or Tier B as "optional science."

---

### RUN1 Resolution

**Decision**: Preserve as INCOMPLETE operational history.

**Rationale**:
- RUN1 used unauthorized 16/16 contract
- Contains only one completed cell
- Must not be interpreted scientifically

**Implementation**:
- Do not resume RUN1 as canonical CAL run
- Create new canonical run identity after restoring authorized contract
- Preserve RUN1 as historical/operational evidence only

---

## Consequences

### Positive
- Scientific contract restored to original frozen state
- Calibration outputs are now raw/distributional as intended
- Execution tiers clearly documented as performance-only
- Audit trail preserved transparently

### Negative
- Runtime will be higher with restored 8/4 strides
- Scientific qualification now requires governance evaluation of distributions
- Cannot force binary CAL-PASS/CAL-FAIL without governance

### Mitigation
- Use exact semantics-preserving optimizations for performance
- Implement comprehensive distributional reporting for governance
- Benchmark per-family runtime to identify bottlenecks

---

## Alternatives Considered

### Stride Contract
1. **Authorize 16/16**: Rejected — changes scientific sampling contract
2. **Geometry-unified 16/16**: Rejected — would require governance authorization
3. **Await CAL benchmarking**: Rejected — should not change contract mid-experiment

### Calibration Thresholds
1. **Keep thresholds as diagnostic-only**: Partially accepted — but prefer complete removal
2. **Governance-authorized thresholds**: Deferred to post-CAL evaluation
3. **CAL-based threshold derivation**: Deferred to post-CAL analysis

---

## References

- Original freeze commit: `ef8f30a`
- Implementation commit: `0b13114`
- Drift commit: `4667adf`
- Retroactive spec update: `b55cb18`
- Takeover audit: Devin forensic audit (2026-09-26)
- Governance authority: GOV-I04CAL-001 (2026-09-26)
- Mandate: QUANT / I04-CAL Devin Mandate

---

## Implementation Commits

1. `audit(I04): restore stride contract to original 8/4 (GOV-01)`
2. `fix(I04): remove numerical thresholds from qualification logic (GOV-02)`
3. `docs(I04): clarify execution tiers as performance-only (GOV-03)`
4. `docs(I04): record governance history in specification`

---

## Outstanding Governance Decisions

None after implementing GOV-01, GOV-02, GOV-03.

Post-CAL evaluation may require additional governance decisions to:
- Interpret calibration distributions
- Establish numerical qualification thresholds if desired
- Evaluate observability diagnostics
- Determine final CAL-PASS/CAL-FAIL status
