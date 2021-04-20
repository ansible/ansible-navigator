""" base class for inventory interactive tests
"""
import json
import os

import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._common import TmuxSession
from ....defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "integration/actions/inventory")
ANSIBLE_INVENTORY_FIXTURE_DIR = os.path.join(TEST_FIXTURE_DIR, "ansible_inventory/inventory.yml")
TEST_CONFIG_FILE = os.path.join(TEST_FIXTURE_DIR, "ansible-navigator.yml")


class BaseClass:
    """base class for interactive inventory tests"""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_inventory_session")
    def fixture_tmux_inventory_session(request):
        """tmux fixture for this module"""
        params = {"window_name": request.node.name, "config_path": TEST_CONFIG_FILE}
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_inventory_session, index, user_input, comment):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments

        """test interactive inventory"""
        assert os.path.exists(ANSIBLE_INVENTORY_FIXTURE_DIR)
        assert os.path.exists(TEST_CONFIG_FILE)

        received_output = tmux_inventory_session.interaction(user_input)
        if self.UPDATE_FIXTURES:
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(f"{dir_path}/{file_name}") as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output
