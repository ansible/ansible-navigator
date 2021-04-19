""" test the use of execution-environment throguh to runner
"""
import os

from unittest import mock

import pytest

import ansible_navigator.cli as cli

from ..defaults import FIXTURES_DIR

test_data = [
    ("defaults", "", "ansible-navigator_empty.yml", {"process_isolation": True}),
    ("set at command line", "--execution-environment false", "ansible-navigator_empty.yml", None),
    ("set in config file", "", "ansible-navigator_disable_ee.yml", None),
    (
        "set command line and config file, command line wins",
        "--execution-environment y",
        "ansible-navigator_disable_ee.yml",
        {"process_isolation": True},
    ),
]


@pytest.mark.parametrize(
    argnames=("comment", "cli_entry", "config_fixture", "expected"),
    argvalues=test_data,
    ids=[f"{idx}: {i[0]}" for idx, i in enumerate(test_data)],
)
class Test:
    # pylint: disable=too-few-public-methods
    # pylint: disable=unused-argument
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=redefined-outer-name
    # pylint: disable=too-many-arguments
    """test execution-environment"""

    __test__ = True

    TEST_FIXTURE_DIR = f"{FIXTURES_DIR}/integration/execution_environment_image"

    STDOUT = {
        "config": "config dump",
        "inventory": "inventory -i bogus_inventory",
        "run": "run site.yaml",
    }

    INTERACTIVE = {
        "config": "config",
        "inventory": f"inventory -i {TEST_FIXTURE_DIR}/inventory.yml",
        "run": f"run {TEST_FIXTURE_DIR}/site.yml",
    }

    def run_test(self, mocked_runner, cli_entry, config_fixture, expected):
        """mock the runner call so it raises an exception
        mock the command line with sys.argv
        set the ANSIBLE_NAVIGATOR_CONFIG envvar
        call cli.main(), check the kwargs passed to the runner func
        """
        mocked_runner.side_effect = Exception("called")
        with mock.patch("sys.argv", cli_entry.split()):
            cfg_path = f"{self.TEST_FIXTURE_DIR}/{config_fixture}"
            with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_CONFIG": cfg_path}):
                with pytest.raises(Exception, match="called"):
                    cli.main()

        _args, kwargs = mocked_runner.call_args

        if expected is None:
            assert "process_isolation" not in kwargs
        else:
            for item in expected.items():
                assert item in kwargs.items()

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.cli_entry = "ansible-navigator {0} {1} -m {2}"

    @mock.patch("ansible_navigator.runner.api.get_ansible_config")
    def test_config_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["config"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command")
    def test_config_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["config"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.get_inventory")
    def test_inventory_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["inventory"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command")
    def test_inventory_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["inventory"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command_async")
    def test_run_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["run"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command_async")
    def test_run_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["run"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)
