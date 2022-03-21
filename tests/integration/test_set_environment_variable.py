"""Test the use of ``set-environment-variable`` through to runner."""
import os
import shlex

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Dict

import pytest

from ansible_navigator import cli
from ..defaults import FIXTURES_DIR
from ._cli2runner import Cli2Runner
from ._cli2runner import RunnerTestException


if TYPE_CHECKING:
    from unittest.mock import MagicMock  # pylint: disable=preferred-module

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
    """Test the use of ``set-environment-variable`` through to runner."""

    TEST_DIR_NAME = os.path.basename(__file__).replace("test_", "").replace(".py", "")
    TEST_FIXTURE_DIR = Path(FIXTURES_DIR) / "integration" / TEST_DIR_NAME

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

    def run_test(
        self,
        mocked_runner: "MagicMock",
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        """Confirm execution of ``cli.main()`` produces the desired results.

        :param mocked_runner: A patched instance of runner
        :param monkeypatch: The monkey patch fixture
        :param tmp_path: A test specific temporary path
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        cfg_path = f"{self.TEST_FIXTURE_DIR}/{config_fixture}"
        coll_cache_path = tmp_path / "collection_doc_cache.db"

        assert os.path.exists(cfg_path)

        params = shlex.split(cli_entry) + ["--pp", "never"]

        monkeypatch.setattr("sys.argv", params)
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", cfg_path)
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH", str(coll_cache_path))
        monkeypatch.chdir(tmp_path)

        with pytest.raises(RunnerTestException):
            cli.main()

        _args, kwargs = mocked_runner.call_args

        for item in expected.items():
            assert item in kwargs["envvars"].items()  # cspell:ignore envvars
