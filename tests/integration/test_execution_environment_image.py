"""Test the use of ``execution-environment-image`` through to runner."""
import os
import shlex

import pytest

from ansible_navigator import cli
from ..defaults import DEFAULT_CONTAINER_IMAGE
from ..defaults import FIXTURES_DIR
from ._cli2runner import Cli2Runner


test_data = [
    ("defaults", "", "ansible-navigator_empty.yml", {"container_image": DEFAULT_CONTAINER_IMAGE}),
    (
        "set at command line",
        "--execution-environment-image quay.io/ansible/python-base",
        "ansible-navigator_empty.yml",
        {"container_image": "quay.io/ansible/python-base:latest"},
    ),
    (
        "set in config file",
        "",
        "ansible-navigator_set_ee_image.yml",
        {"container_image": "quay.io/ansible/python-base:latest"},
    ),
    (
        "set command line and config file, command line wins",
        "--execution-environment True --execution-environment-image quay.io/ansible/python-base",
        "ansible-navigator_set_ee_image.yml",
        {"container_image": "quay.io/ansible/python-base:latest"},
    ),
]


@pytest.mark.parametrize(
    argnames=("comment", "cli_entry", "config_fixture", "expected"),
    argvalues=test_data,
    ids=[f"{idx}: {i[0]}" for idx, i in enumerate(test_data)],
)
class Test(Cli2Runner):
    """Test the use of ``execution-environment-image`` through to runner."""

    TEST_DIR_NAME = os.path.basename(__file__).replace("test_", "").replace(".py", "")
    TEST_FIXTURE_DIR = f"{FIXTURES_DIR}/integration/{TEST_DIR_NAME}"

    INTERACTIVE = {
        "config": "config",
        "inventory": f"inventory -i {TEST_FIXTURE_DIR}/inventory.yml",
        "run": f"run {TEST_FIXTURE_DIR}/site.yml",
    }

    STDOUT = {
        "config": "config dump",
        "inventory": "inventory -i bogus_inventory",
        "run": "run site.yaml",
    }

    def run_test(self, mocked_runner, mocker, tmpdir, cli_entry, config_fixture, expected):
        # pylint: disable=too-many-arguments
        """Mock the runner call so it raises an exception.

        :param mocked_runner: A patched instance of runner
        :param mocker: The pytest-mock fixture
        :param tmpdir: A fixture generating a unique temporary directory
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner.side_effect = Exception("called")
        cfg_path = f"{self.TEST_FIXTURE_DIR}/{config_fixture}"
        coll_cache_path = os.path.join(tmpdir, "collection_doc_cache.db")

        assert os.path.exists(cfg_path)

        params = shlex.split(cli_entry) + ["--pp", "never"]

        mocker.patch("sys.argv", params)
        mocker.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_CONFIG": cfg_path})
        mocker.patch.dict(
            os.environ,
            {"ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH": coll_cache_path},
        )
        with pytest.raises(Exception, match="called"):
            cli.main()

        _args, kwargs = mocked_runner.call_args

        for item in expected.items():
            assert item in kwargs.items()
