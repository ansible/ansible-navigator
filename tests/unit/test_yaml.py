"""Tests related to the yaml abstraction layer.
"""

from typing import Any
from unittest.mock import patch

from yaml import Dumper
import ansible_navigator._yaml as yaml_import


def test_check_yaml_imports():
    """Ensure yaml, Dumper, and Loader are imported without error."""
    assert yaml_import.yaml is not None
    assert yaml_import.Dumper is not None
    assert yaml_import.Loader is not None


def test_no_anchor_alias():
    """Ensure anchors and aliases are not present with ingore_aliases present."""
    data = {"integer": 42}
    many_data = [data, data, data]
    result = yaml_import.human_dump(many_data)
    assert "&id" not in result
    assert "*id" not in result


@patch("ansible_navigator._yaml.HumanDumper.ignore_aliases", Dumper.ignore_aliases)
def test_anchor_alias():
    """Ensure anchors and aliases are present with ignore_aliases restored."""
    data = {"integer": 42}
    many_data = [data, data, data]
    result = yaml_import.human_dump(many_data)
    assert "&id" in result
    assert "*id" in result
