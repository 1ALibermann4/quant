"""
Propriétés génératives CA-03 (Hypothesis, dépendance `dev` uniquement).

Chaque test formalise une propriété mathématique du contrat, pas une énumération
de cas : instants équivalents, permutations, Unicode canonisable, ordre QCT-1.
"""

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from quant.contracts.canonical import (
    canonical_json_bytes,
    canonical_table_bytes,
    to_canonical_utc,
)
from quant.contracts.credentials import credential_indicator

UTC = timezone.utc
NY = ZoneInfo("America/New_York")


@settings(max_examples=80, deadline=None)
@given(hours=st.integers(min_value=-14, max_value=14), minutes=st.sampled_from((0, 30)))
def test_equivalent_offsets_collapse_to_the_same_utc(hours, minutes):
    instant = datetime(2020, 6, 15, 12, 0, tzinfo=UTC)
    offset = timezone(timedelta(hours=hours, minutes=minutes if hours >= 0 else -minutes))
    local = instant.astimezone(offset)
    assert to_canonical_utc(local) == instant
    assert to_canonical_utc(local).tzinfo is timezone.utc


@settings(max_examples=40, deadline=None)
@given(fold=st.sampled_from((0, 1)))
def test_dst_fallback_instants_are_converted_not_compared_as_wall_clock(fold):
    wall = datetime(2020, 11, 1, 1, 30, fold=fold, tzinfo=NY)
    utc = to_canonical_utc(wall)
    assert utc.tzinfo is timezone.utc
    cols = [{"name": "t", "type": "datetime"}]
    assert canonical_table_bytes(cols, ["t"], [{"t": wall}]) == (
        f"t\n{utc.strftime('%Y-%m-%dT%H:%M:%S')}.{utc.microsecond:06d}Z\n".encode()
    )


@settings(max_examples=40, deadline=None)
@given(st.permutations(["basic", "token", "Bearer"]))
def test_v2_repeated_schemes_before_a_real_token_are_still_detected(schemes):
    value = " ".join(schemes) + " abc123def456"
    assert credential_indicator(value) == "V2 authentication scheme value"


@settings(max_examples=60, deadline=None)
@given(st.text(alphabet=st.characters(blacklist_categories=("Cs",)), min_size=1, max_size=20))
def test_valid_unicode_is_qcj_encodable(text):
    assert canonical_json_bytes({"s": text}).decode("utf-8")


def test_lone_surrogate_is_never_qcj_encodable():
    with pytest.raises(ValueError, match="UTF-8"):
        canonical_json_bytes({"s": "\ud800"})


@settings(max_examples=40, deadline=None)
@given(
    a=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2020, 12, 31)).map(
        lambda d: d.replace(tzinfo=UTC)
    ),
    b=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2020, 12, 31)).map(
        lambda d: d.replace(tzinfo=NY)
    ),
)
def test_qct_datetime_pk_order_matches_utc_order(a, b):
    if to_canonical_utc(a) == to_canonical_utc(b):
        return
    cols = [{"name": "t", "type": "datetime"}]
    ny_first = canonical_table_bytes(cols, ["t"], [{"t": a}, {"t": b}])
    utc_first = canonical_table_bytes(
        cols, ["t"], [{"t": to_canonical_utc(a)}, {"t": to_canonical_utc(b)}]
    )
    assert ny_first == utc_first


@settings(max_examples=60, deadline=None)
@given(
    raw=st.one_of(
        st.booleans(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(max_size=8),
        st.lists(st.integers(), max_size=3),
        st.dictionaries(st.text(min_size=1, max_size=4), st.integers(), max_size=2),
    )
)
def test_knowable_int_rejects_anything_that_is_not_an_exact_int(raw):
    from pydantic import ValidationError

    from quant.contracts.knowledge import Knowable

    if type(raw) is int:
        return
    with pytest.raises(ValidationError, match="exact int"):
        Knowable[int].known(raw)


@settings(max_examples=40, deadline=None)
@given(n=st.integers(min_value=-10_000, max_value=10_000))
def test_knowable_int_json_roundtrip_preserves_exact_int(n):
    from quant.contracts.knowledge import Knowable

    known = Knowable[int].known(n)
    assert type(known.value) is int
    assert known.value == n
    restored = Knowable[int].model_validate_json(known.model_dump_json())
    assert restored == known
    assert type(restored.value) is int


@settings(max_examples=60, deadline=None)
@given(
    raw=st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(max_size=8),
        st.just("yes"),
        st.just("true"),
        st.just("false"),
    )
)
def test_knowable_bool_rejects_anything_that_is_not_an_exact_bool(raw):
    from pydantic import ValidationError

    from quant.contracts.knowledge import Knowable

    if type(raw) is bool:
        return
    with pytest.raises(ValidationError, match="exact bool"):
        Knowable[bool].known(raw)


@settings(max_examples=20, deadline=None)
@given(flag=st.booleans())
def test_knowable_bool_json_roundtrip_preserves_exact_bool(flag):
    from quant.contracts.knowledge import Knowable

    known = Knowable[bool].known(flag)
    assert known.value is flag
    restored = Knowable[bool].model_validate_json(known.model_dump_json())
    assert restored == known
    assert restored.value is flag


_ascii = st.characters(min_codepoint=32, max_codepoint=126)
_qcj_scalars = st.one_of(st.none(), st.booleans(), st.integers(), st.text(max_size=8, alphabet=_ascii))


@settings(max_examples=30, deadline=None)
@given(
    mapping=st.dictionaries(
        st.text(min_size=1, max_size=6, alphabet=st.characters(min_codepoint=97, max_codepoint=122)),
        st.recursive(
            _qcj_scalars,
            lambda children: st.one_of(
                st.lists(children, max_size=3),
                st.dictionaries(
                    st.text(
                        min_size=1,
                        max_size=6,
                        alphabet=st.characters(min_codepoint=97, max_codepoint=122),
                    ),
                    children,
                    max_size=3,
                ),
            ),
            max_leaves=8,
        ),
        min_size=1,
        max_size=3,
    )
)
def test_knowable_mapping_freeze_json_roundtrip_preserves_sense(mapping):
    from quant.contracts.canonical import canonical_json_bytes
    from quant.contracts.knowledge import Knowable

    known = Knowable.known(mapping)
    dumped = known.model_dump(mode="json")
    restored = Knowable.model_validate_json(known.model_dump_json())
    assert restored == known
    assert restored.model_dump(mode="json") == dumped
    assert canonical_json_bytes(restored.value) == canonical_json_bytes(mapping)
