"""I01 mathematical core — vendor-agnostic geometric neighborhood.

This package must not import a market-data vendor or any confirmatory C02 loader.
A future C02 DATA-PASS adapter should feed :class:`ObservationSeries` into
:func:`run_geometry` without changing this package.
"""

from quant.i01.observations import ObservationSeries
from quant.i01.params import DEFAULT_PARAMS, I01Params
from quant.i01.pipeline import GeometryResult, run_geometry

__all__ = [
    "DEFAULT_PARAMS",
    "GeometryResult",
    "I01Params",
    "ObservationSeries",
    "run_geometry",
]
