""" these test specificaly target variations of reapplying cli parameters
to subsequent configuration subsystem calls with the same config
grouped here because they are all similar
"""
import os

from copy import deepcopy
from unittest import mock

from ansible_navigator.configuration_subsystem.configurator import Configurator

from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.configuration_subsystem.definitions import CliParameters
from ansible_navigator.configuration_subsystem.definitions import Entry
from ansible_navigator.configuration_subsystem.definitions import EntrySource
from ansible_navigator.configuration_subsystem.definitions import EntryValue
from ansible_navigator.configuration_subsystem.definitions import SubCommand
from ansible_navigator.configuration_subsystem.definitions import Subset

from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration

from ansible_navigator.utils import Sentinel


def test_apply_previous_cli_all():
    """Ensure all previous cli parameter are applied when requested"""
    params = "doc shell --ee False --eei test_image --forks 15"
    expected = [
        ("app", "doc"),
        ("cmdline", ["--forks", "15"]),
        ("execution_environment", False),
        ("execution_environment_image", "test_image"),
        ("plugin_name", "shell"),
    ]

    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )
    configurator.configure()
    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is EntrySource.USER_CLI

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=Subset.ALL,
    )
    configurator.configure()

    expected = [
        ("app", "doc", EntrySource.USER_CLI),
        ("cmdline", ["--forks", "15"], EntrySource.PREVIOUS_CLI),
        ("execution_environment", False, EntrySource.PREVIOUS_CLI),
        ("execution_environment_image", "test_image", EntrySource.PREVIOUS_CLI),
        ("plugin_name", "shell", EntrySource.PREVIOUS_CLI),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_specified():
    """Ensure only some of the previous cli parameters are applied when requested"""
    params = "doc shell --ee False --eei test_image --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )

    configurator.configure()
    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "doc"),
        ("cmdline", ["--forks", "15"]),
        ("execution_environment", False),
        ("execution_environment_image", "test_image"),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is EntrySource.USER_CLI

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=["execution_environment", "execution_environment_image"],
    )
    configurator.configure()

    expected = [
        ("app", "doc", EntrySource.USER_CLI),
        ("cmdline", [], EntrySource.DEFAULT_CFG),
        ("execution_environment", False, EntrySource.PREVIOUS_CLI),
        ("execution_environment_image", "test_image", EntrySource.PREVIOUS_CLI),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_mixed():
    """Ensure a mixed config tests pass"""

    params = "doc shell --ee False --eei test_image --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)

    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )
    with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_PASS_ENVIRONMENT_VARIABLES": "ENV1,ENV2"}):
        configurator.configure()

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "doc", EntrySource.USER_CLI),
        ("cmdline", ["--forks", "15"], EntrySource.USER_CLI),
        ("execution_environment", False, EntrySource.USER_CLI),
        ("execution_environment_image", "test_image", EntrySource.USER_CLI),
        ("pass_environment_variable", ["ENV1", "ENV2"], EntrySource.ENVIRONMENT_VARIABLE),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]

    params = "doc --eei different_image"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=Subset.ALL,
    )
    with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_SET_ENVIRONMENT_VARIABLES": "ENV1=VAL1"}):
        configurator.configure()

    expected = [
        ("app", "doc", EntrySource.USER_CLI),
        ("cmdline", ["--forks", "15"], EntrySource.PREVIOUS_CLI),
        ("execution_environment", False, EntrySource.PREVIOUS_CLI),
        ("execution_environment_image", "different_image", EntrySource.USER_CLI),
        ("pass_environment_variable", [], EntrySource.DEFAULT_CFG),
        ("set_environment_variable", {"ENV1": "VAL1"}, EntrySource.ENVIRONMENT_VARIABLE),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_cmdline_not_applied():
    """Ensure cmdline is not carried forward"""
    params = "run /tmp/site.yml --ee False --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )

    configurator.configure()

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "run"),
        ("cmdline", ["--forks", "15"]),
        ("execution_environment", False),
        ("playbook", "/tmp/site.yml"),
    ]

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is EntrySource.USER_CLI

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=Subset.ALL,
    )
    configurator.configure()

    expected = [
        ("app", "doc", EntrySource.USER_CLI),
        ("cmdline", [], EntrySource.DEFAULT_CFG),
        ("execution_environment", False, EntrySource.PREVIOUS_CLI),
        ("playbook", "/tmp/site.yml", EntrySource.PREVIOUS_CLI),
    ]

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_previous_cli_none():
    """Ensure nothing is carried forward"""
    params = "run /tmp/site.yml --ee False --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )

    configurator.configure()

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    expected = [
        ("app", "run"),
        ("cmdline", ["--forks", "15"]),
        ("playbook", "/tmp/site.yml"),
        ("execution_environment", False),
    ]
    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is EntrySource.USER_CLI

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=Subset.NONE,
    )
    configurator.configure()

    expected = [
        ("app", "doc", EntrySource.USER_CLI),
        ("cmdline", [], EntrySource.DEFAULT_CFG),
        ("playbook", Sentinel, EntrySource.DEFAULT_CFG),
        ("execution_environment", True, EntrySource.DEFAULT_CFG),
    ]

    for expect in expected:
        assert application_configuration.entry(expect[0]).value.current == expect[1]
        assert application_configuration.entry(expect[0]).value.source is expect[2]


def test_apply_cli_subset_none():
    """Ensure subset none works for apply cli"""
    test_config = ApplicationConfiguration(
        application_name="test_application",
        post_processor=None,
        subcommands=[
            SubCommand(name="list", description="list"),
            SubCommand(name="run", description="run"),
        ],
        entries=[
            Entry(
                name="subcommand",
                short_description="Subcommands",
                subcommand_value=True,
                value=EntryValue(default="run"),
            ),
            Entry(
                name="z",
                apply_to_subsequent_cli=Subset.NONE,
                cli_parameters=CliParameters(short="-z"),
                short_description="the z paramter",
                value=EntryValue(),
            ),
        ],
    )
    configurator = Configurator(
        params=["list", "-z", "zebra"], application_configuration=test_config, save_as_intitial=True
    )
    configurator.configure()

    assert isinstance(test_config.initial, ApplicationConfiguration)

    expected = [
        ("subcommand", "list"),
        ("z", "zebra"),
    ]
    for expect in expected:
        assert test_config.entry(expect[0]).value.current == expect[1]
        assert test_config.entry(expect[0]).value.source is EntrySource.USER_CLI

    configurator = Configurator(
        params=["run"], application_configuration=test_config, apply_previous_cli_entries=Subset.ALL
    )
    configurator.configure()

    expected = [
        ("subcommand", "run", EntrySource.USER_CLI),
        ("z", Sentinel, EntrySource.DEFAULT_CFG),
    ]
    for expect in expected:
        assert test_config.entry(expect[0]).value.current == expect[1]
        assert test_config.entry(expect[0]).value.source is expect[2]
