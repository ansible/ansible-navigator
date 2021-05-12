""" base class for config interactive tests
"""
import difflib
import json
import pytest

from typing import Optional
from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession


class BaseClass:
    """base class for interactive/stdout config tests"""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: Optional[str] = None


    @staticmethod
    @pytest.fixture(scope="module", name="tmux_config_session")
    def fixture_tmux_config_session(request):
        """tmux fixture for this module"""
        params = {
            "setup_commands": ["export ANSIBLE_CACHE_PLUGIN_TIMEOUT=42"],
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self, request, tmux_config_session, index, user_input, comment, testname, expected_in_output
    ):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive/stdout config"""

        if self.TEST_FOR_MODE == "interactive":
            search_within_response = ":help help"
        elif self.TEST_FOR_MODE == "stdout":
            search_within_response = tmux_config_session.cli_prompt
        else:
            raise ValueError(
                "Value of 'TEST_FOR_MODE' is not set."
                " Valid value is either 'interactive' or 'stdout'"
            )

        received_output = tmux_config_session.interaction(user_input, search_within_response)

        if expected_in_output:
            for out in expected_in_output:
                assert any(out in line for line in received_output), (out, received_output)
        else:
            # mask out some config that is subject to change each run
            for idx, line in enumerate(received_output):
                mask = "X" * 50
                if tmux_config_session.cli_prompt in line:
                    received_output[idx] = mask
                else:
                    if "13│BECOME_PLUGIN_PATH" in line:
                        received_output[idx] = mask
                    if "15│CACHE_PLUGIN_CONNECTION" in line:
                        received_output[idx] = mask

            if self.UPDATE_FIXTURES:
                update_fixtures(request, index, received_output, comment, testname=testname)
            dir_path, file_name = fixture_path_from_request(request, index, testname=testname)
            with open(f"{dir_path}/{file_name}") as infile:
                expected_output = json.load(infile)["output"]
            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received")
            )
