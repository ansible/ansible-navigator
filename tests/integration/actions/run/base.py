""" base class for run interactive tests
"""
import difflib
import json
import os
import pytest

from typing import Optional
from ....defaults import FIXTURES_DIR
from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession


# run playbook
run_fixture_dir = os.path.join(FIXTURES_DIR, "integration", "actions", "run")
inventory_path = os.path.join(run_fixture_dir, "inventory")
playbook_path = os.path.join(run_fixture_dir, "site.yaml")


class BaseClass:
    """base class for interactive/stdout run tests"""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: Optional[str] = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_run_session")
    def fixture_tmux_run_session(request):
        """tmux fixture for this module"""
        params = {
            "pane_height": "1000",
            "pane_width": "500",
            "setup_commands": [
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_run_session, index, user_input, comment, search_within_response):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive/stdout config"""

        if self.TEST_FOR_MODE == "stdout":
            search_within_response = tmux_run_session.cli_prompt
            # clear the screen so it starts with stdout
            user_input = f"clear && {user_input}"

        received_output = tmux_run_session.interaction(user_input, search_within_response)

        # mask out some lines that is subject to change each run
        mask = "X" * 50
        for idx, line in enumerate(received_output):
            if tmux_run_session.cli_prompt in line:
                received_output[idx] = mask
            else:
                for out in ["duration:", "playbook:", "start:", "end:", "task_path:"]:
                    if out in line:
                        received_output[idx] = mask

        if True: #self.UPDATE_FIXTURES:
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(os.path.join(dir_path, file_name)) as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.unified_diff(expected_output, received_output, "expected", "received")
        )
