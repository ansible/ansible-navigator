"""Test the use of execution-environment-image through to runner.
"""
import os
import shlex

from unittest import mock

import pytest

from ansible_navigator import cli
from ._cli2runner import Cli2Runner
from ..defaults import DEFAULT_CONTAINER_IMAGE
from ..defaults import FIXTURES_DIR


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
    """test the use of execution-environment-image through to runner"""

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

    def run_test(self, mocked_runner, tmpdir, cli_entry, config_fixture, expected):
        # pylint: disable=too-many-arguments
        """mock the runner call so it raises an exception
        mock the command line with ``sys.argv``
        set the ANSIBLE_NAVIGATOR_CONFIG environment variable
        set the expected environment variables
        call ``cli.main()``, check the arguments passed to the runner function
        """
        mocked_runner.side_effect = Exception("called")
        cfg_path = f"{self.TEST_FIXTURE_DIR}/{config_fixture}"
        coll_cache_path = os.path.join(tmpdir, "collection_doc_cache.db")

        assert os.path.exists(cfg_path)

        params = shlex.split(cli_entry) + ["--pp", "never"]

        with mock.patch("sys.argv", params):
            with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_CONFIG": cfg_path}):
                with mock.patch.dict(
                    os.environ,
                    {"ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH": coll_cache_path},
                ):
                    with pytest.raises(Exception, match="called"):
                        cli.main()

        _args, kwargs = mocked_runner.call_args

        for item in expected.items():
            assert item in kwargs.items()
