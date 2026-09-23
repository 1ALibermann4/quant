"""
C02 — conteneurs immuables pour l'état des objets C02 (C02-INV-05).

`frozen=True` n'interdit que la réaffectation des attributs d'un modèle ; il ne protège pas
les conteneurs qu'il porte. Tout conteneur atteignable depuis un objet C02 est donc gelé à
la validation : mappings → `FrozenMap`, listes → tuples, récursivement.

Sérialisation : `model_dump()` et `model_dump_json()` restituent des `dict` et des `list`,
identiques aux sorties produites avant le gel ; les représentations canoniques (QCJ-1) sont
inchangées.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Annotated, Any, TypeVar

from pydantic import AfterValidator, PlainSerializer, SerializationInfo, WrapSerializer

V = TypeVar("V")
T = TypeVar("T")


class FrozenMap(Mapping[str, Any]):
    """Mapping en lecture seule ; hachable si ses valeurs le sont."""

    __slots__ = ("_data",)

    def __init__(self, data: Mapping[str, Any] | None = None) -> None:
        object.__setattr__(self, "_data", dict(data or {}))

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("FrozenMap is immutable")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __hash__(self) -> int:
        return hash(frozenset(self._data.items()))

    def __repr__(self) -> str:
        return f"FrozenMap({self._data!r})"

    def __reduce__(self) -> tuple[Any, ...]:
        return (FrozenMap, (self._data,))


def deep_freeze(value: Any) -> Any:
    """Mappings → FrozenMap, listes/tuples → tuples, récursivement."""
    if isinstance(value, Mapping):
        return FrozenMap({key: deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list | tuple):
        return tuple(deep_freeze(item) for item in value)
    return value


def thaw(value: Any) -> Any:
    """Inverse de `deep_freeze` pour la sérialisation (dict / list)."""
    if isinstance(value, Mapping):
        return {key: thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw(item) for item in value]
    return value


def _dump_as_list(value: Any, handler: Any, info: SerializationInfo) -> Any:
    dumped = handler(value)
    return list(dumped) if info.mode == "python" else dumped


FrozenMapping = Annotated[
    Mapping[str, V],
    AfterValidator(deep_freeze),
    PlainSerializer(thaw, return_type=dict[str, Any]),
]
"""Mapping gelé en profondeur ; sérialisé en `dict` (valeurs tuple → list)."""

FrozenList = Annotated[tuple[T, ...], WrapSerializer(_dump_as_list)]
"""Séquence stockée en tuple ; `model_dump()` restitue une `list` (compatibilité v1.0)."""
