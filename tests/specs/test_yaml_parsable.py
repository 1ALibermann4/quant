"""Parsabilité des fichiers YAML normatifs (DR-006).

Contrôle de développement/CI uniquement : PyYAML appartient au groupe ``dev``
et n'est jamais importé par ``src/quant``. Aucun modèle n'est chargé depuis
le YAML ; seul le document est analysé syntaxiquement.
"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
NORMATIVE_DIRS = ("specs", "research", "docs")


class _UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader refusant les clés dupliquées (PyYAML garde sinon la dernière)."""


def _construct_mapping(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        seen.add(key)
    return loader.construct_mapping(node, deep=deep)


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def _normative_yaml_files() -> list[Path]:
    files = []
    for directory in NORMATIVE_DIRS:
        base = ROOT / directory
        files += [*base.rglob("*.yaml"), *base.rglob("*.yml")]
    return sorted(files)


YAML_FILES = _normative_yaml_files()


def test_normative_yaml_files_are_discovered():
    names = {p.relative_to(ROOT).as_posix() for p in YAML_FILES}
    assert "specs/contracts/C02/C02_v1.1.yaml" in names
    assert "specs/contracts/C02/profiles/C02-I01_v1.0.yaml" in names


@pytest.mark.parametrize(
    "path", YAML_FILES, ids=[p.relative_to(ROOT).as_posix() for p in YAML_FILES]
)
def test_normative_yaml_is_parsable(path: Path):
    document = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    assert isinstance(document, dict), f"{path}: top-level document must be a mapping"


@pytest.mark.parametrize(
    "text",
    [
        "a: 1\na: 2\n",
        "outer:\n  k: 1\n  k: 2\n",
        "items:\n  - checks: {measurement?, detail?}}\n",
        "key: value: other\n",
    ],
)
def test_loader_rejects_invalid_or_ambiguous_yaml(text: str):
    with pytest.raises(yaml.YAMLError):
        yaml.load(text, Loader=_UniqueKeyLoader)


def test_runtime_does_not_import_yaml():
    offenders = [
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "src").rglob("*.py")
        if any(
            line.strip().startswith(("import yaml", "from yaml"))
            for line in p.read_text(encoding="utf-8").splitlines()
        )
    ]
    assert offenders == []
