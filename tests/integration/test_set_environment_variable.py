""" test the use of set_environment_variable throguh to runner
"""
import os
import shlex

from unittest import mock

import pytest

from ansible_navigator import cli

from ._cli2runner import Cli2Runner
from ..defaults import FIXTURES_DIR

test_data = [
    ("not set", "", "ansible-navigator_empty.yml", {}),
    (
        "set 1 at command line",
        "--senv TEST_ENV=nav",
        "ansible-navigator_empty.yml",
        {"TEST_ENV": "nav"},
    ),
    (
        "set 2 at command line",
        "--senv TEST_ENV=nav --senv TEST_ENV2=nav2",
        "ansible-navigator_empty.yml",
        {"TEST_ENV": "nav", "TEST_ENV2": "nav2"},
    ),
    (
        "set 3 in config file",
        "",
        "ansible-navigator.yml",
        {"TEST_STR": "navigator", "TEST_BOOL": "true", "TEST_INT": "42"},
    ),
    (
        "set command line and config file, command line wins",
        "--senv TEST_ENV=nav --senv TEST_ENV2=nav2",
        "ansible-navigator.yml",
        {"TEST_ENV": "nav", "TEST_ENV2": "nav2"},
    ),
]


@pytest.mark.parametrize(
    argnames=("comment", "cli_entry", "config_fixture", "expected"),
    argvalues=test_data,
    ids=[f"{idx}: {i[0]}" for idx, i in enumerate(test_data)],
)
class Test(Cli2Runner):
    """test the use of set_environment_variable throguh to runner"""

    TEST_DIR_NAME = os.path.basename(__file__).replace("test_", "").replace(".py", "")
    TEST_FIXTURE_DIR = f"{FIXTURES_DIR}/integration/{TEST_DIR_NAME}"

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

    def run_test(self, mocked_runner, tmpdir, cli_entry, config_fixture, expected):
        # pylint: disable=too-many-arguments
        """Mock the runner call so it raises an exception.

        mock the command line with sys.argv
        set the ANSIBLE_NAVIGATOR_CONFIG envvar
        call cli.main(), check the kwarg envvars passed to the runner func
        """
        mocked_runner.side_effect = Exception("called")
        cfg_path = f"{self.TEST_FIXTURE_DIR}/{config_fixture}"
        coll_cache_path = os.path.join(tmpdir, "collection_doc_cache.db")

        assert os.path.exists(cfg_path)

        params = shlex.split(cli_entry) + ["--pp", "never"]

        with mock.patch("sys.argv", params):
            with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_CONFIG": cfg_path}):
                with mock.patch.dict(
                    os.environ, {"ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH": coll_cache_path}
                ):
                    with pytest.raises(Exception, match="called"):
                        cli.main()

        _args, kwargs = mocked_runner.call_args

        for item in expected.items():
            assert item in kwargs["envvars"].items()
