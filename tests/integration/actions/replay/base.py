"""Base class for replay interactive tests.
"""
import difflib
import json
import os

import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession
from ....defaults import FIXTURES_DIR


TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "integration/actions/replay")
PLAYBOOK_ARTIFACT = os.path.join(TEST_FIXTURE_DIR, "playbook-artifact.json")
TEST_CONFIG_FILE = os.path.join(TEST_FIXTURE_DIR, "ansible-navigator.yml")


class BaseClass:
    """Base class for replay interactive tests."""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request):
        """tmux fixture for this module"""
        params = {
            "config_path": TEST_CONFIG_FILE,
            "pane_height": "100",
            "setup_commands": [
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, index, user_input, comment, search_within_response):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-locals
        """Run the tests for replay, mode and ``ee`` set in child class."""
        assert os.path.exists(PLAYBOOK_ARTIFACT)
        assert os.path.exists(TEST_CONFIG_FILE)

        received_output = tmux_session.interaction(user_input, search_within_response)

        fixtures_update_requested = (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        )
        if fixtures_update_requested:
            update_fixtures(request, index, received_output, comment)

        dir_path, file_name = fixture_path_from_request(request, index)
        with open(file=f"{dir_path}/{file_name}", encoding="utf-8") as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.unified_diff(expected_output, received_output, "expected", "received")
        )
