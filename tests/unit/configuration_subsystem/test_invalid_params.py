"""Some test using invalid parameters
"""
import tempfile

from unittest.mock import patch

import pytest

from ansible_navigator.configuration_subsystem import NavigatorConfiguration

from .utils import id_for_name


def test_generate_argparse_error(generate_config):
    """Ensure errors generated by argparse are caught"""
    params = "Sentinel"
    response = generate_config(params=params.split())
    assert len(response.errors) == 1
    error = "invalid choice: 'Sentinel'"
    assert error in response.errors[0]


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_inventory_no_inventory(_mocked_func, generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for an inventory without an inventory specified"""
    response = generate_config(params=["inventory"])
    errors = ["An inventory is required when using the inventory subcommand"]
    assert errors == response.errors


@patch(
    "ansible_navigator.configuration_subsystem.navigator_post_processor.check_for_ansible",
    return_value=(False, "no_ansible"),
)
def test_ee_false_no_ansible(_mocked_func, generate_config):
    """Ensure an error is created if EE is false and ansible not present"""
    response = generate_config(params=["--ee", "false"])
    assert response.errors == ["no_ansible"]


@patch("distutils.spawn.find_executable", return_value=None)
def test_no_container_engine(_mocked_func, generate_config):
    """Ensure an error is created if EE is false and ansible not present"""
    response = generate_config()
    error = (
        "The specified container engine could not be found:'podman',"
        " set by 'default configuration value'"
    )
    assert response.errors == [error]


@patch("os.makedirs", side_effect=OSError)
@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_fail_log_file_dir(_mf1, _mf2, generate_config):
    """Ensure an error is created if log file cannot be created"""
    response = generate_config()
    error = "Failed to create log file"
    assert response.errors[0].startswith(error)


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_doc_no_plugin_name(_mocked_func, generate_config):
    """Ensure an error is created doc is used without plugin_name"""
    response = generate_config(params=["doc"])
    errors = ["An plugin name is required when using the doc subcommand"]
    assert response.errors == errors


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_load_no_artifact(_mocked_func, generate_config):
    """Ensure an error is created load is used without playbook artifact"""
    response = generate_config(params=["load"])
    errors = ["An playbook artifact file is required when using the load subcommand"]
    assert response.errors == errors


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_load_missing_artifact(_mocked_func, generate_config):
    """Ensure an error is created load is used with a missing playbook artifact"""
    response = generate_config(params=["load", tempfile.NamedTemporaryFile().name])
    error = "The specified playbook artifact could not be found:"
    assert response.errors[0].startswith(error)


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_badly_formatted_envar(_mocked_func, generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for badly formatted set env var"""
    params = "run site.yml --senv TK1:TV1"
    response = generate_config(params=params.split())
    errors = ["The following set-environment-variable entry could not be parsed: TK1:TV1"]
    assert errors == response.errors


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_not_a_bool(_mocked_func, generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for wrong type of value"""

    response = generate_config(setting_file_name="ansible-navigator_not_bool.yml")
    error = "execution_environment could not be converted to a boolean value, value was '5' (int)"
    assert response.errors[0] == error


choices = [entry for entry in NavigatorConfiguration.entries if entry.choices]


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
@pytest.mark.parametrize("entry", choices, ids=id_for_name)
def test_poor_choices(_mocked_func, generate_config, entry):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for poor choices"""

    def test(subcommand, param):
        if subcommand is None:
            response = generate_config(params=[param, "Sentinel"])
        else:
            response = generate_config(params=[subcommand, param, "Sentinel"])
        assert any("must be one of" in err for err in response.errors)

    if isinstance(entry.subcommands, list):
        subcommand = entry.subcommands[0]
    else:
        subcommand = None

    test(subcommand, entry.cli_parameters.short)
    test(subcommand, entry.cli_parameters.long_override or f"--{entry.name_dashed}")


@pytest.mark.parametrize("subcommand", ["load", "collections"])
@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_interactive_only_subcommand(_mocked_func, generate_config, subcommand):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for badly formatted set env var"""
    params = f"{subcommand} -m stdout"
    response = generate_config(params=params.split())
    error = (
        f"Subcommand '{subcommand}' does not support mode 'stdout'. Supported modes: 'interactive'."
    )
    assert error in response.errors
