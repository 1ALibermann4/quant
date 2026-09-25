"""Unit smoke for HAT fixture identity (no full HAT execution)."""

from __future__ import annotations

from quant.i02.fixture_hat import FIXTURE_N, fixture_sha256, generate_hat_returns


def test_hat_fixture_deterministic_hash():
    a = generate_hat_returns()
    b = generate_hat_returns()
    assert a.shape == (FIXTURE_N,)
    assert fixture_sha256(a) == fixture_sha256(b)
    assert fixture_sha256(a) == (
        "sha256:196f9c82a878521edb5db02416a6874f526020b989904152157d202accdbd2b5"
    )


def test_runtime_parser_has_no_scientific_knobs():
    from quant.i02.runtime import build_parser

    help_text = build_parser().format_help()
    for forbidden in (
        "--W_X",
        "--k",
        "--B",
        "--b-star",
        "--alpha",
        "--M_Z",
        "--s3-primary",
    ):
        assert forbidden not in help_text
