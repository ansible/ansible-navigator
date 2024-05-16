"""Some tests directly for ``Configurator``."""

import os


# pylint: disable=preferred-module  # FIXME: remove once migrated per GH-872
from collections.abc import Callable
from copy import deepcopy
from typing import Any
from unittest import mock
from unittest.mock import patch

import pytest

from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    generate_editor_command,
)


def test_mutual_exclusivity_for_configuration_init() -> None:
    """Ensure the configuration cannot be initiated with apply_previous_cli_entries and initial."""
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    with pytest.raises(ValueError, match="cannot be used while initializing"):
        Configurator(
            params=None,
            application_configuration=application_configuration,
            apply_previous_cli_entries=C.ALL,
        )


def test_apply_before_initial_saved() -> None:
    """Ensure the apply_previous_cli_entries can't be used before initial."""
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = False
    with pytest.raises(ValueError, match="enabled prior to"):
        Configurator(
            params=None,
            application_configuration=application_configuration,
            apply_previous_cli_entries=C.ALL,
        ).configure()


@patch("shutil.which", return_value="/path/to/container_engine")
def test_editor_command_from_editor(_mocked_func: Any, generate_config: Callable[..., Any]) -> None:
    """Ensure the editor_command defaults to EDITOR if set.

    :param generate_config: The configuration generator fixture
    """
    with mock.patch.dict(os.environ, {"EDITOR": "nano"}):
        # since this was already loaded, force it
        NavigatorConfiguration.entry("editor_command").value.default = generate_editor_command()
        response = generate_config()
        assert response.exit_messages == []
        assert response.application_configuration.editor_command == "nano {filename}"
