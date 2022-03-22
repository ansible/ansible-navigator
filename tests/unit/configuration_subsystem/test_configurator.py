"""Some tests directly for ``Configurator``
"""
import os

from copy import deepcopy

# pylint: disable=preferred-module  # FIXME: remove once migrated per GH-872
from unittest import mock
from unittest.mock import patch

import pytest

from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    generate_editor_command,
)


def test_mutual_exclusivity_for_configuration_init():
    """Ensure the configuration cannot be initiated with both
    apply_previous_cli_entries and initial"""
    with pytest.raises(ValueError, match="cannot be used while initializing"):
        application_configuration = deepcopy(NavigatorConfiguration)
        application_configuration.internals.initializing = True
        Configurator(
            params=None,
            application_configuration=application_configuration,
            apply_previous_cli_entries=C.ALL,
        )


def test_apply_before_initial_saved():
    """Ensure the apply_previous_cli_entries can't be used before initial"""
    with pytest.raises(ValueError, match="enabled prior to"):
        application_configuration = deepcopy(NavigatorConfiguration)
        application_configuration.internals.initializing = False
        Configurator(
            params=None,
            application_configuration=application_configuration,
            apply_previous_cli_entries=C.ALL,
        ).configure()


@patch("shutil.which", return_value="/path/to/container_engine")
def test_editor_command_from_editor(_mocked_func, generate_config):
    """Ensure the editor_command defaults to EDITOR if set"""
    with mock.patch.dict(os.environ, {"EDITOR": "nano"}):
        # since this was already loaded, force it
        NavigatorConfiguration.entry("editor_command").value.default = generate_editor_command()
        response = generate_config()
        assert response.exit_messages == []
        assert response.application_configuration.editor_command == "nano {filename}"
