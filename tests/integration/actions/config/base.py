""" base class for config interactive tests
"""
import difflib
import json

import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._common import TmuxSession


class BaseClass:
    """base class for interactive config tests"""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_config_session")
    def fixture_tmux_config_session(request):
        """tmux fixture for this module"""
        params = {
            "window_name": request.node.name,
            "setup_commands": ["export ANSIBLE_CACHE_PLUGIN_TIMEOUT=42"],
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_config_session, index, user_input, comment):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive config"""
        received_output = tmux_config_session.interaction(user_input)
        # mask out some config that is subject to change each run
        for idx, line in enumerate(received_output):
            mask = "X" * 50
            if "13│BECOME_PLUGIN_PATH" in line:
                received_output[idx] = mask
            if "15│CACHE_PLUGIN_CONNECTION" in line:
                received_output[idx] = mask

        if self.UPDATE_FIXTURES:
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(f"{dir_path}/{file_name}") as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.ndiff(expected_output, received_output)
        )
