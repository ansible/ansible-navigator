"""Tests for the transformation of settings to a json schema."""


from copy import deepcopy
from pathlib import Path
from typing import Any
from typing import Dict

import pytest

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.configuration_subsystem import to_schema
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import yaml
from .defaults import TEST_FIXTURE_DIR


@pytest.fixture(name="schema_dict")
def _schema_dict():
    settings = deepcopy(NavigatorConfiguration)
    settings.application_version = "test"
    schema = to_schema(settings)
    return schema


def test_basic(schema_dict: Dict[str, Any]):
    """Simple test to ensure an exception isn't raised.

    :param schema_dict: The json schema as a dictionary
    """
    assert schema_dict["$schema"] == "http://json-schema.org/draft-07/schema"
    assert isinstance(schema_dict["properties"]["ansible-navigator"]["properties"], dict)
    # This checks for a number of root keys in the settings file
    assert len(schema_dict["properties"]["ansible-navigator"]["properties"]) >= 15


def test_additional_properties(schema_dict: Dict[str, Any]):
    """Ensure additional properties are forbidden throughout the schema.

    :param schema_dict: The json schema as a dictionary
    """

    def property_dive(subschema: Dict[str, Any]):
        if "properties" in subschema:
            assert subschema["additionalProperties"] is False
            for value in subschema["properties"].values():
                property_dive(subschema=value)

    property_dive(schema_dict)


def test_no_extras(schema_dict: Dict[str, Any]):
    """Ensure no extras exist in either settings or schema.

    :param schema_dict: The json schema as a dictionary
    """
    settings = deepcopy(NavigatorConfiguration)
    all_paths = [
        setting.settings_file_path(prefix=settings.application_name_dashed)
        for setting in settings.entries
    ]

    json_paths = []

    def dive(subschema, path=""):
        if "properties" in subschema:
            for name, prop in subschema["properties"].items():
                if path:
                    dive(prop, f"{path}.{name}")
                else:
                    dive(prop, name)
        else:
            json_paths.append(path)

    dive(schema_dict)

    # The difference below are because we do not have settings entries for the individual
    # keys but instead the full dict
    only_in_json = [p for p in json_paths if p not in all_paths]
    assert only_in_json == [
        "ansible-navigator.execution-environment.volume-mounts.dest",
        "ansible-navigator.execution-environment.volume-mounts.label",
        "ansible-navigator.execution-environment.volume-mounts.options",
    ]
    only_in_settings = [p for p in all_paths if p not in json_paths]
    assert only_in_settings == ["ansible-navigator.execution-environment.volume-mounts"]


def test_schema_sample_full_tests(schema_dict: Dict[str, Any]):
    """Check the full settings file against the schema.

    :param schema_dict: The json schema as a dictionary
    """
    settings_file = Path(TEST_FIXTURE_DIR, "ansible-navigator.yml")
    with settings_file.open(encoding="utf-8") as fh:
        settings_contents = yaml.load(fh, Loader=Loader)
    validate(instance=settings_contents, schema=schema_dict)


def test_schema_sample_full_package_data(schema_dict: Dict[str, Any]):
    """Check the settings file used as a sample against the schema.

    :param schema_dict: The json schema as a dictionary
    """
    settings = deepcopy(NavigatorConfiguration)
    commented, uncommented = to_sample(settings=settings)
    settings_dict = yaml.load(commented, Loader=Loader)
    validate(instance=settings_dict, schema=schema_dict)
    settings_dict = yaml.load(uncommented, Loader=Loader)
    validate(instance=settings_dict, schema=schema_dict)


def test_schema_sample_wrong(schema_dict: Dict[str, Any]):
    """Check the broken settings file against the schema.

    :param schema_dict: The json schema as a dictionary
    """
    settings_file = Path(TEST_FIXTURE_DIR, "ansible-navigator_no_app.yml")
    with settings_file.open(encoding="utf-8") as fh:
        settings_contents = yaml.load(fh, Loader=Loader)
    with pytest.raises(ValidationError) as exc:
        validate(instance=settings_contents, schema=schema_dict)
    assert "'non_app' is not one of ['builder'" in str(exc)
