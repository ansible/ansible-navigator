"""these test specifically target variations of reapplying CLI parameters
to subsequent configuration subsystem calls with the same configuration
grouped here because they are all similar
"""
import os

from copy import deepcopy

# pylint: disable=preferred-module  # FIXME: remove once migrated per GH-872
from unittest import mock
from unittest.mock import patch

from ansible_navigator.configuration_subsystem.configurator import Configurator
from ansible_navigator.configuration_subsystem.definitions import (
    ApplicationConfiguration,
)
from ansible_navigator.configuration_subsystem.definitions import CliParameters
from ansible_navigator.configuration_subsystem.definitions import Constants as C
from ansible_navigator.configuration_subsystem.definitions import SettingsEntry
from ansible_navigator.configuration_subsystem.definitions import SettingsEntryValue
from ansible_navigator.configuration_subsystem.definitions import SubCommand
from ansible_navigator.configuration_subsystem.navigator_configuration import Internals
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    NavigatorConfiguration,
)


def test_apply_previous_cli_all():
    """Ensure all previous CLI parameters are applied when requested"""
    params = "doc shell --ee False --eei test_image:latest --forks 15"
    expected = [
        ("app", "doc"),
        ("cmdline", ["--forks", "15"]),
        ("execution_environment", False),
        ("execution_environment_image", "test_image:latest"),
        ("plugin_name", "shell"),
    ]

    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
    )
    _messages, exit_messages = configurator.configure()
    assert exit_messages == []
    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is C.USER_CLI

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=C.ALL,
    )
    _messages, exit_messages = configurator.configure()
    assert exit_messages == []

    expected = [
        ("app", "doc", C.USER_CLI),
        ("cmdline", ["--forks", "15"], C.PREVIOUS_CLI),
        ("execution_environment", False, C.PREVIOUS_CLI),
        ("execution_environment_image", "test_image:latest", C.PREVIOUS_CLI),
        ("plugin_name", "shell", C.PREVIOUS_CLI),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_specified():
    """Ensure only some of the previous CLI parameters are applied when requested"""
    params = "doc shell --ee False --eei test_image:latest --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
    )

    _messages, exit_messages = configurator.configure()
    assert not exit_messages
    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "doc"),
        ("cmdline", ["--forks", "15"]),
        ("execution_environment", False),
        ("execution_environment_image", "test_image:latest"),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is C.USER_CLI

    params = "doc shell"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=["execution_environment", "execution_environment_image"],
    )
    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    expected = [
        ("app", "doc", C.USER_CLI),
        ("cmdline", C.NOT_SET, C.NOT_SET),
        ("execution_environment", False, C.PREVIOUS_CLI),
        ("execution_environment_image", "test_image:latest", C.PREVIOUS_CLI),
        ("plugin_name", "shell", C.USER_CLI),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_mixed():
    """Ensure a mixed configuration passes"""

    params = "doc shell --ee False --eei test_image:latest --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
    )
    with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_PASS_ENVIRONMENT_VARIABLES": "ENV1,ENV2"}):
        _messages, exit_messages = configurator.configure()
        assert not exit_messages

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "doc", C.USER_CLI),
        ("cmdline", ["--forks", "15"], C.USER_CLI),
        ("execution_environment", False, C.USER_CLI),
        ("execution_environment_image", "test_image:latest", C.USER_CLI),
        ("pass_environment_variable", ["ENV1", "ENV2"], C.ENVIRONMENT_VARIABLE),
        ("plugin_name", "shell", C.USER_CLI),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]

    params = "doc shell --eei different_image:latest"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=C.ALL,
    )
    with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_SET_ENVIRONMENT_VARIABLES": "ENV1=VAL1"}):
        _messages, exit_messages = configurator.configure()
        assert not exit_messages

    expected = [
        ("app", "doc", C.USER_CLI),
        ("cmdline", ["--forks", "15"], C.PREVIOUS_CLI),
        ("execution_environment", False, C.PREVIOUS_CLI),
        ("execution_environment_image", "different_image:latest", C.USER_CLI),
        ("pass_environment_variable", C.NOT_SET, C.NOT_SET),
        ("plugin_name", "shell", C.USER_CLI),
        ("set_environment_variable", {"ENV1": "VAL1"}, C.ENVIRONMENT_VARIABLE),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_cmdline_not_applied():
    """Ensure the command line parameters are not carried forward"""
    params = "run /tmp/site.yml --ee False --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
    )

    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "run"),
        ("cmdline", ["--forks", "15"]),
        ("execution_environment", False),
        ("playbook", "/tmp/site.yml"),
    ]

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is C.USER_CLI

    params = "doc shell"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=C.ALL,
    )
    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    expected = [
        ("app", "doc", C.USER_CLI),
        ("cmdline", C.NOT_SET, C.NOT_SET),
        ("execution_environment", False, C.PREVIOUS_CLI),
        ("playbook", "/tmp/site.yml", C.PREVIOUS_CLI),
        ("plugin_name", "shell", C.USER_CLI),
    ]

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


@patch("shutil.which", return_value="/path/to/container_engine")
def test_apply_previous_cli_none(_mf1):
    """Ensure nothing is carried forward"""
    params = "run /tmp/site.yml --ee False --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
    )

    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "run"),
        ("cmdline", ["--forks", "15"]),
        ("playbook", "/tmp/site.yml"),
        ("execution_environment", False),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is C.USER_CLI

    params = "doc shell"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=C.NONE,
    )
    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    expected = [
        ("app", "doc", C.USER_CLI),
        ("cmdline", C.NOT_SET, C.NOT_SET),
        ("playbook", C.NOT_SET, C.NOT_SET),
        ("execution_environment", True, C.DEFAULT_CFG),
        ("plugin_name", "shell", C.USER_CLI),
    ]

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_cli_subset_none():
    """Ensure subset none works for apply CLI"""
    test_config = ApplicationConfiguration(
        application_name="test_application",
        application_version="1.0",
        internals=Internals(initializing=True),
        post_processor=None,
        subcommands=[
            SubCommand(name="list", description="list"),
            SubCommand(name="run", description="run"),
        ],
        entries=[
            SettingsEntry(
                name="subcommand",
                short_description="Subcommands",
                subcommand_value=True,
                value=SettingsEntryValue(default="run"),
            ),
            SettingsEntry(
                name="z",
                apply_to_subsequent_cli=C.NONE,
                cli_parameters=CliParameters(short="-z"),
                short_description="the z parameter",
                value=SettingsEntryValue(),
            ),
            SettingsEntry(
                name="execution_environment",
                apply_to_subsequent_cli=C.NONE,
                cli_parameters=CliParameters(short="-e"),
                short_description="the e parameter",
                value=SettingsEntryValue(),
            ),
        ],
    )
    configurator = Configurator(
        params=["list", "-z", "zebra"],
        application_configuration=test_config,
    )
    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    assert isinstance(test_config.initial, ApplicationConfiguration)

    expected = [
        ("subcommand", "list"),
        ("z", "zebra"),
    ]
    for expect in expected:
        assert test_config.entry(expect[0]).value.current == expect[1]
        assert test_config.entry(expect[0]).value.source is C.USER_CLI

    configurator = Configurator(
        params=["run"],
        application_configuration=test_config,
        apply_previous_cli_entries=C.ALL,
    )
    _messages, exit_messages = configurator.configure()
    assert not exit_messages

    expected = [
        ("subcommand", "run", C.USER_CLI),
        ("z", C.NOT_SET, C.NOT_SET),
    ]
    for expect in expected:
        assert test_config.entry(expect[0]).value.current == expect[1]
        assert test_config.entry(expect[0]).value.source is expect[2]
