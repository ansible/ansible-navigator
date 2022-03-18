"""Tests for the transformation of settings to a json schema."""

import json

from pathlib import Path
from typing import Any
from typing import Dict

import pytest

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import yaml
from .defaults import TEST_FIXTURE_DIR


@pytest.fixture(name="settings_sample")
def _settings_sample():
    settings = NavigatorConfiguration
    settings_file = to_sample(settings=settings)
    return settings_file


def test_valid_yaml(settings_sample: str):
    """Simple test to ensure the sample is valid yaml.

    :param settings_sample: The sample settings file
    """
    settings_contents = yaml.load(settings_sample, Loader=Loader)
    assert settings_contents
