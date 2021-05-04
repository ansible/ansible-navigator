""" fixtures for configuration subsystem tests
"""
import os
from copy import deepcopy

from typing import Dict
from typing import List
from typing import NamedTuple

import pytest

from ansible_navigator.configuration_subsystem.configurator import Configurator

from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration

from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration

from ansible_navigator.utils import LogMessage

from ansible_navigator.yaml import yaml
from ansible_navigator.yaml import Loader

from ...defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "unit", "configuration_subsystem")


class GenerateConfigResponse(NamedTuple):
    """obj for generate_config_response"""

    messages: List[LogMessage]
    errors: List[str]
    application_configuration: ApplicationConfiguration
    settings_contents: Dict


def _generate_config(params=None, setting_file_name=None) -> GenerateConfigResponse:
    """Generate a configuration given a settings file"""
    if params is None:
        params = []

    if setting_file_name:
        settings_file_path = os.path.join(TEST_FIXTURE_DIR, setting_file_name)
        with open(settings_file_path) as file:
            try:
                settings_contents = yaml.load(file, Loader=Loader)
            except yaml.parser.ParserError:
                # let the config subsystem catch the invalid yaml file
                settings_contents = {}
    else:
        settings_file_path = ""
        settings_contents = {}

    # deepcopy here to ensure we do not modify the original
    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params,
        settings_file_path=settings_file_path or None,
    )
    messages, errors = configurator.configure()
    return GenerateConfigResponse(
        messages=messages,
        errors=errors,
        application_configuration=application_configuration,
        settings_contents=settings_contents,
    )


@pytest.fixture(name="generate_config")
def fixture_generate_config():
    """generate a config"""
    return _generate_config
