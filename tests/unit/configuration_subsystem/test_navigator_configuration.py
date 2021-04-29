""" tests for configuration subsystem
"""
import os
from collections import Counter
from copy import deepcopy
from unittest import mock

import pytest

from ansible_navigator.configuration_subsystem.configurator import Configurator
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration

from ansible_navigator.configuration_subsystem.navigator_configuration import (
    generate_editor_command,
)
from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration


from .data import BASE_EXPECTED
from .data import BASE_LONG_CLI
from .data import BASE_SHORT_CLI
from .data import CLI_DATA
from .data import ENVVAR_DATA
from .data import SETTINGS

from .utils import fixture_generate_config
from .utils import id_for_base
from .utils import id_for_cli
from .utils import id_for_name
from .utils import id_for_settings

from ...defaults import FIXTURES_DIR


def test_no_duplicate_names():
    """Ensure no name is duplicated"""
    values = Counter([entry.name for entry in NavigatorConfiguration.entries])
    assert not any(k for (k, v) in values.items() if v > 1)


def test_no_duplicate_shorts():
    """Ensure no short is duplicated"""
    values = Counter(
        [
            entry.cli_parameters.short
            for entry in NavigatorConfiguration.entries
            if entry.cli_parameters is not None
        ]
    )
    assert not any(k for (k, v) in values.items() if v > 1)


def test_no_missing_envvar_data():
    """Ensure the ENVVAR_DATA covers all entries"""
    entry_names = [entry.name for entry in NavigatorConfiguration.entries]
    data_names = [entry[0] for entry in ENVVAR_DATA]
    assert entry_names == data_names


def test_entries_are_alphbetical():
    """Ensure entries are alphabetical"""
    values = [entry.name for entry in NavigatorConfiguration.entries]
    assert values == sorted(values)


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_no_dash_in_name(entry):
    """Ensure no names contain a -"""
    assert "-" not in entry.name


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_no_dash_in_environment_variable(entry):
    """Ensure no environment variable has a dash"""
    assert "-" not in entry.environment_variable("ansible_navigator")


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_no_short_long_if_postional(entry):
    """Ensure no postional argument has a short or long set"""
    if hasattr(entry, "cli_arguments") and entry.cli_parameters.positional:
        assert entry.short is None
        assert entry.long_override is None


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_no_underscore_in_path(entry):
    """Ensure no long override has an _"""
    if entry.settings_file_path_override is not None:
        assert "_" not in entry.settings_file_path_override


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_default(generate_config, entry):
    """Ensure all entries are set to a default value"""
    response = generate_config()
    configured_entry = response.application_configuration.entry(entry.name)
    assert configured_entry.value.source.name == "DEFAULT_CFG", entry

    if entry.name in ["inventory", "inventory_column", "pass_environment_variable"]:
        assert configured_entry.value.current == [], entry
    elif entry.name in ["set_environment_variable"]:
        assert configured_entry.value.current == {}, entry
    else:
        assert configured_entry.value.current == entry.value.default, entry


@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_envvars(generate_config, base, cli_entry, expected):
    """Ensure all entries are set by the cli even with envvars set"""
    if base is None:
        params = cli_entry.split()
        expected = dict(expected)
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    envvars = {}
    for entry in NavigatorConfiguration.entries:
        envvar_name = entry.environment_variable("ansible_navigator")
        envvar_value = [value[1] for value in ENVVAR_DATA if value[0] == entry.name]
        assert len(envvar_value) == 1, entry.name
        envvars[envvar_name] = envvar_value[0]

    with mock.patch.dict(os.environ, envvars):
        response = generate_config(params=params)
        for key, value in expected.items():
            assert response.application_configuration.entry(key).value.current == value
            assert response.application_configuration.entry(key).value.source.name == "USER_CLI"
        for entry in response.application_configuration.entries:
            if entry.name not in expected:
                assert entry.value.source.name == "ENVIRONMENT_VARIABLE", entry


@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_settings(
    generate_config, settings, source_other, base, cli_entry, expected
):
    """Ensure all entries are set by the cli
    based on the settings file, the non cli parametes will be
    either DEFAULT_CFG or USER_CFG
    """
    if base is None:
        params = cli_entry.split()
        expected = dict(expected)
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    response = generate_config(params=params, setting_file_name=settings)
    for key, value in expected.items():
        configured_entry = response.application_configuration.entry(key)
        assert configured_entry.value.current == value, configured_entry
        assert configured_entry.value.source.name == "USER_CLI", configured_entry
    for entry in response.application_configuration.entries:
        if entry.name not in expected:
            assert entry.value.source.name == source_other, entry


@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_settings_and_envars(
    generate_config, settings, source_other, base, cli_entry, expected
):
    """Ensure all entries are set by the cli
    the non cli parametes will be all be ENVIRONMENT_VARIABLE
    even though an empty or full settings file was provided
    """
    if base is None:
        params = cli_entry.split()
        expected = dict(expected)
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    envvars = {}
    for entry in NavigatorConfiguration.entries:
        envvar_name = entry.environment_variable("ansible_navigator")
        envvar_value = [value[1] for value in ENVVAR_DATA if value[0] == entry.name]
        assert len(envvar_value) == 1, entry.name
        envvars[envvar_name] = envvar_value[0]

    with mock.patch.dict(os.environ, envvars):
        response = generate_config(params=params, setting_file_name=settings)
        for key, value in expected.items():
            configured_entry = response.application_configuration.entry(key)
            assert configured_entry.value.current == value, configured_entry
            assert configured_entry.value.source.name == "USER_CLI", configured_entry
        for entry in response.application_configuration.entries:
            if entry.name not in expected:
                assert entry.value.source.name == "ENVIRONMENT_VARIABLE", entry


@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("entry, value, expected", ENVVAR_DATA)
def test_all_entries_reflect_envvar_given_settings(
    generate_config, settings, source_other, entry, value, expected
):
    # pylint: disable=unused-argument
    """Ensure each entry is are set by an environment variables
    even though settings file has been provided, the others
    should by default or user cfg
    """
    environment_variable = NavigatorConfiguration.entry(entry).environment_variable(
        "ansible_navigator"
    )
    with mock.patch.dict(os.environ, {environment_variable: str(value)}):
        response = generate_config(setting_file_name=settings)
        configured_entry = response.application_configuration.entry(entry)
        assert configured_entry.value.source.name == "ENVIRONMENT_VARIABLE"
        assert configured_entry.value.current == expected
    for other_entry in response.application_configuration.entries:
        if other_entry.name != entry:
            assert other_entry.value.source.name == source_other, other_entry


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_settings_given_settings(generate_config, entry):
    """Ensure all entries are set to an entry in a settings file"""
    response = generate_config(setting_file_name="ansible-navigator.yml")
    configured_entry = response.application_configuration.entry(entry.name)
    if entry.cli_parameters is not None:
        assert configured_entry.value.source.name == "USER_CFG", entry
        path = entry.settings_file_path("ansible-navigator")
        expected = response.settings_contents
        for key in path.split("."):
            expected = expected[key]
        assert configured_entry.value.current == expected, entry


def test_apply_previous_cli_all():
    params = "doc shell --ee False --eei test_image --forks 15"
    expected = {
        "app": "doc",
        "cmdline": ["--forks", "15"],
        "execution_environment": False,
        "execution_environment_image": "test_image",
    }

    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )
    configurator.configure()
    for key, value in expected.items():
        assert application_configuration.entry(key).value.current == value
        assert application_configuration.entry(key).value.source.name == "USER_CLI"

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=["all"],
    )
    configurator.configure()
    for key, value in expected.items():
        if key != "app":
            assert application_configuration.entry(key).value.current == value
            assert application_configuration.entry(key).value.source.name == "PREVIOUS_CLI"


def test_apply_previous_cli_some():
    params = "doc shell --ee False --eei test_image --forks 15"
    application_configuration = deepcopy(NavigatorConfiguration)
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )

    configurator.configure()

    expected = {
        "app": "doc",
        "cmdline": ["--forks", "15"],
        "execution_environment": False,
        "execution_environment_image": "test_image",
    }
    for key, value in expected.items():
        assert application_configuration.entry(key).value.current == value
        assert application_configuration.entry(key).value.source.name == "USER_CLI"

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    params = "doc"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=["execution_environment", "execution_environment_image"],
    )
    configurator.configure()

    expected = {
        "app": "doc",
        "execution_environment": False,
        "execution_environment_image": "test_image",
    }
    for key, value in expected.items():
        if key != "app":
            assert application_configuration.entry(key).value.current == value
            assert application_configuration.entry(key).value.source.name == "PREVIOUS_CLI"
    assert application_configuration.cmdline == []
    assert application_configuration.entry("cmdline").value.source.name == "DEFAULT_CFG"


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

    expected = {
        "app": "doc",
        "cmdline": ["--forks", "15"],
        "execution_environment": False,
        "execution_environment_image": "test_image",
    }
    # all expected set at command line
    for key, value in expected.items():
        assert application_configuration.entry(key).value.current == value
        assert application_configuration.entry(key).value.source.name == "USER_CLI"

    # penv set as environment variable
    assert application_configuration.pass_environment_variable == ["ENV1", "ENV2"]
    assert (
        application_configuration.entry("pass_environment_variable").value.source.name
        == "ENVIRONMENT_VARIABLE"
    )

    assert isinstance(application_configuration.initial, ApplicationConfiguration)

    params = "doc --eei different_image"
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli_entries=["all"],
    )
    with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_SET_ENVIRONMENT_VARIABLES": "ENV1=VAL1"}):
        configurator.configure()

    # ee is carried forward because it was not in the command
    assert application_configuration.execution_environment is False
    assert (
        application_configuration.entry("execution_environment").value.source.name == "PREVIOUS_CLI"
    )

    # eei is pulled from the current command
    assert application_configuration.execution_environment_image == "different_image"
    assert (
        application_configuration.entry("execution_environment_image").value.source.name
        == "USER_CLI"
    )

    # penv is default because it is no longer set
    assert application_configuration.pass_environment_variable == []
    assert (
        application_configuration.entry("pass_environment_variable").value.source.name
        == "DEFAULT_CFG"
    )

    # senv is set because it is a new envvar
    assert application_configuration.set_environment_variable == {"ENV1": "VAL1"}
    assert (
        application_configuration.entry("set_environment_variable").value.source.name
        == "ENVIRONMENT_VARIABLE"
    )


def test_editor_command_from_editor(generate_config):
    """Ensure the editor_command defaults to EDITOR if set"""
    with mock.patch.dict(os.environ, {"EDITOR": "nano"}):
        # since this was already loaded, force it
        NavigatorConfiguration.entry("editor_command").value.default = generate_editor_command()
        response = generate_config()
        assert response.application_configuration.editor_command == "nano {filename}"


def test_not_a_bool(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for wrong type of value"""
    import ansible_navigator.configuration_subsystem.configurator

    response = generate_config(setting_file_name="ansible-navigator_not_bool.yml")
    errors = [
        (
            "execution-environment must be one of 'True' or 'False',"
            " but set as '5' in user provided configuration file"
        )
    ]
    assert response.errors == errors


def test_badly_formatted_envar(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for badly formatted set env var"""
    params = "run site.yml --senv TK1:TV1"
    response = generate_config(params=params.split())
    errors = ["The following set-environment-variable entry could not be parsed: TK1:TV1"]
    assert response.errors == errors


def test_broken_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for broken settings file"""
    response = generate_config(setting_file_name="ansible-navigator_broken.yml")
    assert len(response.errors) == 1
    error = "/ansible-navigator_broken.yml empty"
    assert response.errors[0].endswith(error)


def test_garbage_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for garbage settings file"""
    response = generate_config(setting_file_name=os.path.abspath(__file__))
    assert len(response.errors) == 1
    error = "but failed to load it."
    assert response.errors[0].endswith(error)


def test_inventory_no_inventory(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for wrong type of value"""
    response = generate_config(params=["inventory"])
    errors = ["An inventory is required when using the inventory subcommand"]
    assert response.errors == errors


def test_mutual_exclusivity_for_configuration_init(generate_config):
    """Ensure the configuration cannot be intited with both
    apply_previous_cli_entries and save_as_intitial"""
    with pytest.raises(ValueError, match="cannot be used with"):
        Configurator(
            params=None,
            application_configuration=None,
            save_as_intitial=True,
            apply_previous_cli_entries=["all"],
        )


def test_apply_before_initial_saved(generate_config):
    """Ensure the apply_previous_cli_entries cant' be used before save_as_intitial"""
    with pytest.raises(ValueError, match="enabled prior to"):
        Configurator(
            params=None,
            application_configuration=NavigatorConfiguration,
            apply_previous_cli_entries=["all"],
        ).configure()


@pytest.mark.parametrize(
    "entry", [entry for entry in NavigatorConfiguration.entries if entry.choices], ids=id_for_name
)
def test_poor_choices(generate_config, entry):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for poor choices"""
    import ansible_navigator.configuration_subsystem.configurator

    def test(param):
        response = generate_config(params=[param, "Sentinel"])
        assert len(response.errors) == 1
        error = "must be one of"
        assert error in response.errors[0]

    test(entry.cli_parameters.short)
    test(entry.cli_parameters.long_override or f"--{entry.name_dashed}")


def test_generate_argparse_error(generate_config):
    """Ensure errors generated for badly formatted set env var"""
    params = "Sentinel"
    response = generate_config(params=params.split())
    assert len(response.errors) == 1
    error = "invalid choice: 'Sentinel'"
    assert error in response.errors[0]
