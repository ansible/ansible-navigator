""" base class for inventory interactive tests
"""
import difflib
import json
import os

from typing import Optional

import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession
from ....defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "integration/actions/inventory")
ANSIBLE_INVENTORY_FIXTURE_DIR = os.path.join(TEST_FIXTURE_DIR, "ansible_inventory/inventory.yml")
TEST_CONFIG_FILE = os.path.join(TEST_FIXTURE_DIR, "ansible-navigator.yml")


class BaseClass:
    """base class for interactive inventory tests"""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: Optional[str] = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_inventory_session")
    def fixture_tmux_inventory_session(request):
        """tmux fixture for this module"""
        params = {"config_path": TEST_CONFIG_FILE, "unique_test_id": request.node.nodeid}
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_inventory_session, index, user_input, comment):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments

        """test interactive inventory"""
        assert os.path.exists(ANSIBLE_INVENTORY_FIXTURE_DIR)
        assert os.path.exists(TEST_CONFIG_FILE)

        if self.TEST_FOR_MODE == "interactive":
            search_within_response = ":help help"
        elif self.TEST_FOR_MODE == "stdout":
            search_within_response = tmux_inventory_session.cli_prompt
        else:
            raise ValueError(
                "Value of 'TEST_FOR_MODE' is not set."
                " Valid value is either 'interactive' or 'stdout'"
            )

        received_output = tmux_inventory_session.interaction(user_input, search_within_response)

        if (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        ):
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(f"{dir_path}/{file_name}") as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.unified_diff(expected_output, received_output, "expected", "received")
        )
