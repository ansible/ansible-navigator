"""Tests related to the yaml abstraction layer.
"""

import ansible_navigator._yaml as yaml_import


def test_check_yaml_imports():
    """Ensure yaml, Dumper, and Loader are imported without error."""
    assert yaml_import.yaml is not None
    assert yaml_import.Dumper is not None
    assert yaml_import.Loader is not None
