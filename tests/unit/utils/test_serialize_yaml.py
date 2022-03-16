"""Tests related to the yaml abstraction layer."""

import pytest

from yaml import Dumper

from ansible_navigator.content_defs import ContentView
from ansible_navigator.utils import serialize


def test_check_yaml_imports():
    """Ensure yaml, Dumper, and Loader are imported without error."""
    assert serialize.yaml is not None
    assert serialize.SafeDumper is not None
    assert serialize.Loader is not None


@pytest.fixture(name="aliases_allowed")
def _aliases_allowed(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest):
    """Patch the human dumper if requested.

    :param monkeypatch: Fixture for patching
    :param request: The request for this fixture from a test
    :returns: The original request parameter
    """
    if request.param:  # type: ignore[attr-defined] # github.com/pytest-dev/pytest/issues/8073
        monkeypatch.setattr(
            "ansible_navigator.utils.serialize.HumanDumper.ignore_aliases",
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
    yaml_string = serialize.serialize(
        content=many_data,
        content_view=ContentView.NORMAL,
        serialization_format=serialize.SerializationFormat.YAML,
    )
    assert isinstance(yaml_string, str), "Unexpected value from human_dump"
    found_alias = "&id" in yaml_string
    assert found_alias is aliases_allowed
    found_anchor = "*id" in yaml_string
    assert found_anchor is aliases_allowed
