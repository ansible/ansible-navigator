""" test the use of execution-environment throguh to runner
"""
import os

from unittest import mock

import pytest


from .cli2runner import Cli2Runner
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
class Test(Cli2Runner):
    # pylint: disable=too-few-public-methods
    """base class for the parametrize"""

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
                print(os.environ)
                with pytest.raises(Exception, match="called"):
                    import ansible_navigator.cli as cli
                    cli.main()

        _args, kwargs = mocked_runner.call_args

        if expected is None:
            assert "process_isolation" not in kwargs
        else:
            for item in expected.items():
                assert item in kwargs.items()
