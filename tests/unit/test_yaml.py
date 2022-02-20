"""Tests related to the yaml abstraction layer.
"""

import pytest

from yaml import Dumper

import ansible_navigator._yaml as yaml_import


def test_check_yaml_imports():
    """Ensure yaml, Dumper, and Loader are imported without error."""
    assert yaml_import.yaml is not None
    assert yaml_import.Dumper is not None
    assert yaml_import.Loader is not None


@pytest.fixture(name="aliases_allowed")
def _aliases_allowed(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest):
    """Patch the human dumper if requested.

    :param monkeypatch: Fixture for patching
    :param request: The request for this fixture from a test
    :returns: The original request parameter
    """
    if request.param:  # type: ignore[attr-defined] # github.com/pytest-dev/pytest/issues/8073
        monkeypatch.setattr(
            "ansible_navigator._yaml.HumanDumper.ignore_aliases",
            Dumper.ignore_aliases,
        )
    return request.param  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "aliases_allowed",
    [True, False],
    ids=["pyyaml original", "no aliases or anchors"],
    indirect=("aliases_allowed",),
)
def test_anchor_alias(aliases_allowed: bool):
    """Test for anchors and aliases in yaml output.

    :param aliases_allowed: Indicates if aliases and anchors should be found
    """
    data = {"integer": 42}
    many_data = [data, data, data]
    yaml_string = yaml_import.human_dump(many_data)
    assert isinstance(yaml_string, str), "Unexpected value from human_dump"
    found_alias = "&id" in yaml_string
    assert found_alias is aliases_allowed
    found_anchor = "*id" in yaml_string
    assert found_anchor is aliases_allowed
