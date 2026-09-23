"""
Profil C02-I01 v1.0 — exigences DATA-REQ-I01 v0.1 sur un DatasetSnapshot C02 v1.1.

Le contrat générique C02 accepte tout objet v1.0/v1.1 valide ; ce profil exprime les
exigences supplémentaires d'I01. Trois catégories de constats :

- `errors` : représentation absente, incohérente ou exigence violée avec certitude ;
- `blocking_unknowns` : métadonnée REQUIRED représentée honnêtement comme non connue —
  l'objet est conforme mais DATA-PASS est impossible tant qu'elle n'est pas résolue ;
- `warnings` : exigences RECOMMENDED non satisfaites ou non vérifiables.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import date, timedelta

from pydantic import BaseModel, ConfigDict

from quant.contracts.data_assessment import DataGateAssessment, DataVerdict
from quant.contracts.dataset_snapshot import DatasetSnapshot
from quant.contracts.knowledge import Knowable, KnowledgeStatus
from quant.contracts.lineage import ProviderArtifact
from quant.contracts.market_calendar import MarketCalendarSnapshot

I01_PROFILE_ID = "C02-I01"
I01_PROFILE_VERSION = "1.0"
I01_AUTHORITY = "research/I01/DATA-REQ-I01.md v0.1"

CANONICAL_TIMEZONE = "America/New_York"
INTENDED_USES = frozenset({"technical", "confirmatory"})
QUALITY_CHECK_IDS = tuple(f"Q-{i:02d}" for i in range(1, 15))
ALLOWED_COLUMNS = {
    "session_date": {"date"},
    "adjusted_close": {"decimal"},
    "close": {"decimal"},
    "volume": {"integer", "decimal"},
}

TIER_BELOW_TECHNICAL = "BELOW_TECHNICAL"
TIER_TECHNICAL = "TECHNICAL"
TIER_CONFIRMATORY = "CONFIRMATORY"
TIER_PREFERRED = "PREFERRED"


class ProfileReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    profile_id: str = I01_PROFILE_ID
    profile_version: str = I01_PROFILE_VERSION
    authority: str = I01_AUTHORITY
    errors: tuple[str, ...] = ()
    blocking_unknowns: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    depth_tier: str | None = None

    @property
    def conforms(self) -> bool:
        return not self.errors

    @property
    def data_pass_eligible(self) -> bool:
        return self.conforms and not self.blocking_unknowns


def _add_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return date(d.year + years, 2, 28)


def i01_depth_tier(valid_sessions: int, first_session: date, last_session: date) -> str:
    """Palier de profondeur DATA-REQ §4.1 (séances valides et durée calendaire)."""
    if valid_sessions >= 3780 and last_session >= _add_years(first_session, 15):
        return TIER_PREFERRED
    if valid_sessions >= 2520 and last_session >= _add_years(first_session, 10):
        return TIER_CONFIRMATORY
    if valid_sessions >= 1500:
        return TIER_TECHNICAL
    return TIER_BELOW_TECHNICAL


class _Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.blocking: list[str] = []
        self.warnings: list[str] = []

    def required(self, value: Knowable | None, label: str) -> None:
        """Métadonnée REQUIRED : absente/N-A → erreur ; UNKNOWN → bloquant."""
        if value is None:
            self.errors.append(f"{label}: missing")
        elif value.status is KnowledgeStatus.UNKNOWN:
            self.blocking.append(f"{label}: UNKNOWN")
        elif value.status is KnowledgeStatus.NOT_APPLICABLE:
            self.errors.append(f"{label}: NOT_APPLICABLE is not admissible for I01")

    def recommended(self, value: Knowable | None, label: str) -> None:
        if value is None or not value.is_known:
            self.warnings.append(f"{label}: not known (RECOMMENDED)")

    def guard(self, label: str, check: Callable[[], None]) -> bool:
        try:
            check()
        except ValueError as exc:
            self.errors.append(f"{label}: {exc}")
            return False
        return True


def _check_schema(snapshot: DatasetSnapshot, f: _Findings) -> None:
    schema = snapshot.table_schema
    if schema is None:
        f.errors.append("table_schema: missing")
        return
    if schema.primary_key != ("session_date",):
        f.errors.append("table_schema: primary key must be ('session_date',) (TS-01)")
    for column in schema.columns:
        allowed = ALLOWED_COLUMNS.get(column.name)
        if allowed is None:
            f.errors.append(f"table_schema: column {column.name!r} is out of I01 scope (§3.1)")
        elif column.type not in allowed:
            f.errors.append(f"table_schema: column {column.name!r} has type {column.type}")
    for name in ("session_date", "adjusted_close"):
        column = schema.column(name)
        if column is None:
            f.errors.append(f"table_schema: required column {name!r} missing (§3.1)")
        elif column.nullable:
            f.errors.append(f"table_schema: column {name!r} must not be nullable")


def _canonical_order(artifacts: list[ProviderArtifact]) -> list[ProviderArtifact]:
    """Ordre de parcours indépendant de l'ordre fourni (identifiants uniques après P-03)."""
    return sorted(artifacts, key=lambda a: a.artifact_id)


def _check_artifacts(
    snapshot: DatasetSnapshot, artifacts: list[ProviderArtifact], f: _Findings
) -> list[ProviderArtifact] | None:
    """P-03 puis exigences par artefact ; artefacts revalidés, ou None s'ils ne sont pas vérifiés."""
    if not snapshot.source_artifacts:
        f.errors.append("source_artifacts: missing (§7.1 raw fingerprint)")
        return None
    if not f.guard("source_artifacts", lambda: snapshot.verify_artifacts(artifacts)):
        return None
    artifacts = _canonical_order([ProviderArtifact.model_validate(a) for a in artifacts])
    for artifact in artifacts:
        label = f"artifact {artifact.artifact_id}"
        f.required(artifact.provider_interface_version, f"{label}.provider_interface_version")
        f.required(artifact.license.usage_basis_ref, f"{label}.license.usage_basis_ref")
        retention = artifact.license.raw_retention_permitted
        if retention.is_known and retention.value is False:
            f.errors.append(f"{label}.license: raw retention not permitted (REP-05)")
        else:
            f.required(retention, f"{label}.license.raw_retention_permitted")
        if snapshot.instrument is not None and artifact.instrument.ticker != snapshot.instrument.ticker:
            f.errors.append(f"{label}: instrument ticker differs from snapshot instrument")
    return artifacts


def _check_instrument(snapshot: DatasetSnapshot, f: _Findings) -> None:
    if snapshot.instrument is None:
        f.errors.append("instrument: missing (INS-05)")
        return
    if len(snapshot.instruments) > 1:
        f.errors.append("instruments: I01 is univariate (INS-01)")
    f.required(snapshot.instrument.venue, "instrument.venue")
    ids = (snapshot.instrument.isin, snapshot.instrument.cusip, snapshot.instrument.figi)
    if not any(i.is_known for i in ids):
        f.blocking.append("instrument: no ISIN/CUSIP/FIGI known (INS-05)")


def _check_temporal(snapshot: DatasetSnapshot, f: _Findings) -> None:
    tc = snapshot.temporal_convention
    if tc is None:
        f.errors.append("temporal_convention: missing (TS-03)")
        return
    if tc.canonical_timezone != CANONICAL_TIMEZONE:
        f.errors.append(f"temporal_convention: canonical timezone must be {CANONICAL_TIMEZONE}")
    if tc.source_timezone.status is KnowledgeStatus.UNKNOWN:
        f.blocking.append("temporal_convention.source_timezone: UNKNOWN (TS-03)")
    if not tc.session_date_rule.strip():
        f.errors.append("temporal_convention.session_date_rule: empty (TS-02)")


def _check_calendar(
    snapshot: DatasetSnapshot, calendar: MarketCalendarSnapshot, f: _Findings
) -> MarketCalendarSnapshot | None:
    """C02-INV-14 via `verify_calendar` ; calendrier revalidé, ou None s'il n'est pas vérifié."""
    if snapshot.market_calendar is None:
        f.errors.append("market_calendar: missing (CAL-01)")
        return None
    if not f.guard("market_calendar", lambda: snapshot.verify_calendar(calendar)):
        return None
    calendar = MarketCalendarSnapshot.model_validate(calendar)
    f.required(calendar.source, "calendar.source (CAL-01)")
    f.required(calendar.source_version, "calendar.source_version (CAL-01)")
    return calendar


def _check_ranges_and_counts(snapshot: DatasetSnapshot, f: _Findings) -> None:
    f.required(snapshot.requested_range, "requested_range")
    if snapshot.returned_range is None:
        f.errors.append("returned_range: missing")
    if snapshot.canonical_range is None:
        f.errors.append("canonical_range: missing")
    counts = snapshot.counts
    if counts is None:
        f.errors.append("counts: missing")
        return
    for value, label in (
        (counts.expected_sessions, "counts.expected_sessions"),
        (counts.missing_sessions, "counts.missing_sessions"),
    ):
        if not value.is_known:
            f.errors.append(f"{label}: must be KNOWN (derivable from the calendar)")
    f.required(counts.invalidated_sessions, "counts.invalidated_sessions")


def _check_adjustment(snapshot: DatasetSnapshot, f: _Findings) -> None:
    adj = snapshot.adjustment_methodology
    if adj is None:
        f.errors.append("adjustment_methodology: missing (§3.3)")
        return
    f.required(adj.events_covered, "adjustment.events_covered")
    f.required(adj.method, "adjustment.method")
    f.required(adj.reference_date, "adjustment.reference_date")
    f.required(adj.numeric_precision, "adjustment.numeric_precision")
    f.required(adj.currency, "adjustment.currency")
    f.required(adj.methodology_ref, "adjustment.methodology_ref (ADJ-01)")
    f.recommended(adj.dividend_factor_formula, "adjustment.dividend_factor_formula")
    f.recommended(adj.methodology_version, "adjustment.methodology_version")


def _check_temporal_bounds(
    snapshot: DatasetSnapshot,
    calendar: MarketCalendarSnapshot,
    artifacts: list[ProviderArtifact],
    f: _Findings,
) -> None:
    rng = snapshot.canonical_range
    if rng is None:
        return
    last_close = calendar.close_instant(rng.last_session)
    first_close = calendar.close_instant(rng.first_session)
    if snapshot.availability_cutoff != last_close:
        f.errors.append(
            "availability_cutoff must equal the close of the last canonical session (§7.1)"
        )
    if snapshot.provenance.time_range_end != last_close:
        f.errors.append("provenance.time_range_end must equal the last session close")
    if snapshot.provenance.time_range_start != first_close:
        f.errors.append("provenance.time_range_start must equal the first session close")
    for artifact in _canonical_order(artifacts):
        acquired_local = artifact.acquired_at.astimezone(last_close.tzinfo).date()
        gap = calendar.sessions_between(rng.last_session + timedelta(days=1), acquired_local)
        if gap < 5:
            f.warnings.append(
                f"REV-D-04: only {gap} calendar sessions between last session and acquisition "
                f"of {artifact.artifact_id} (>= 5 recommended; calendar coverage may limit count)"
            )


def _check_assessment(
    snapshot: DatasetSnapshot,
    assessment: DataGateAssessment,
    tier: str | None,
    f: _Findings,
) -> None:
    ref = assessment.snapshot_ref
    if ref.snapshot_id != snapshot.snapshot_id or ref.fingerprint != snapshot.fingerprint:
        f.errors.append("assessment: snapshot_ref does not match the snapshot")
    ids = {c.check_id for c in assessment.checks}
    if ids != set(QUALITY_CHECK_IDS):
        missing = sorted(set(QUALITY_CHECK_IDS) - ids)
        extra = sorted(ids - set(QUALITY_CHECK_IDS))
        f.errors.append(f"assessment: checks must be exactly Q-01..Q-14 (missing {missing}, extra {extra})")
    if assessment.intended_use != snapshot.intended_use:
        f.errors.append("assessment: intended_use differs from the snapshot declaration (§4.3)")
    if tier is not None and assessment.coverage_tier != tier:
        f.errors.append(f"assessment: coverage_tier {assessment.coverage_tier} != derived {tier}")
    must_fail = tier == TIER_BELOW_TECHNICAL or (
        snapshot.intended_use == "confirmatory" and tier == TIER_TECHNICAL
    )
    if must_fail and assessment.verdict is not DataVerdict.FAIL:
        f.errors.append("assessment: depth tier insufficient for intended use requires FAIL (§4.3)")
    if assessment.verdict is DataVerdict.PASS and (f.errors or f.blocking):
        f.errors.append("assessment: DATA-PASS with profile errors or blocking unknowns")


def validate_i01_snapshot(
    snapshot: DatasetSnapshot,
    *,
    calendar: MarketCalendarSnapshot,
    artifacts: Iterable[ProviderArtifact],
    assessment: DataGateAssessment | None = None,
) -> ProfileReport:
    """
    Évalue la conformité d'un snapshot au profil C02-I01 v1.0.

    Frontière validante : snapshot et évaluation sont revalidés (ValidationError si l'objet
    n'est pas conforme à C02) ; calendrier et artefacts le sont par `verify_calendar` et
    `verify_artifacts`, un échec devenant une erreur du rapport.
    """
    snapshot = DatasetSnapshot.model_validate(snapshot)
    if assessment is not None:
        assessment = DataGateAssessment.model_validate(assessment)
    artifacts = list(artifacts)
    f = _Findings()
    if snapshot.contract_version != "1.1":
        f.errors.append("contract_version: I01 requires C02 v1.1")
    _check_schema(snapshot, f)
    verified_artifacts = _check_artifacts(snapshot, artifacts, f)
    _check_instrument(snapshot, f)
    _check_temporal(snapshot, f)
    verified_calendar = _check_calendar(snapshot, calendar, f)
    _check_ranges_and_counts(snapshot, f)
    _check_adjustment(snapshot, f)
    if not snapshot.lineage:
        f.errors.append("lineage: missing (§7.1 transformation provenance)")
    if snapshot.intended_use not in INTENDED_USES:
        f.errors.append(f"intended_use: must be one of {sorted(INTENDED_USES)} (§4.3)")
    if verified_calendar is not None:
        _check_temporal_bounds(snapshot, verified_calendar, verified_artifacts or [], f)

    tier = None
    if snapshot.counts is not None and snapshot.canonical_range is not None:
        tier = i01_depth_tier(
            snapshot.counts.canonical_observations,
            snapshot.canonical_range.first_session,
            snapshot.canonical_range.last_session,
        )
    if assessment is not None:
        _check_assessment(snapshot, assessment, tier, f)

    return ProfileReport(
        errors=tuple(f.errors),
        blocking_unknowns=tuple(f.blocking),
        warnings=tuple(f.warnings),
        depth_tier=tier,
    )
