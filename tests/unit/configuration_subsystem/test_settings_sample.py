"""Tests for the transformation of settings to a json schema."""


from copy import deepcopy
from typing import Tuple

import pytest

from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import yaml


@pytest.fixture(name="settings_samples")
def _settings_samples() -> Tuple[str, str]:
    settings = deepcopy(NavigatorConfiguration)
    commented, uncommented = to_sample(settings=settings)
    return commented, uncommented


def test_valid_yaml(settings_samples: Tuple[str, str]):
    """Simple test to ensure the sample is valid yaml.

    :param settings_samples: The sample setting
    """
    commented, uncommented = settings_samples
    settings_contents = yaml.load(commented, Loader=Loader)
    assert settings_contents
    settings_contents = yaml.load(uncommented, Loader=Loader)
    assert settings_contents


def test_no_un_templated(settings_samples: Tuple[str, str]):
    """Simple test to ensure the sample is valid yaml.

    :param settings_samples: The sample settings
    """
    commented, uncommented = settings_samples
    assert "{{" not in commented
    assert "{{" not in uncommented
    assert "}}" not in commented
    assert "}}" not in uncommented
