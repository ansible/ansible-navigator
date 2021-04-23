""" base class for config interactive tests
"""
import json

import pytest

from typing import List

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._common import TmuxSession

from ....defaults import FIXTURES_COLLECTION_DIR


class BaseClass:
    """base class for interactive config tests"""

    UPDATE_FIXTURES = False

    def setup_class(self):
        self.expected_in_output: List = []
        self.assert_operator = "=="

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_config_session")
    def fixture_tmux_config_session(request):
        """tmux fixture for this module"""
        params = {
            "window_name": request.node.name,
            "setup_commands": [
                f"export ANSIBLE_COLLECTIONS_PATH={FIXTURES_COLLECTION_DIR}",
                "ANSIBLE_DEVEL_WARNING=False",
                "ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self, request, tmux_config_session, index, user_input, comment, testname, expected_in_output
    ):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive config"""
        received_output = tmux_config_session.interaction(user_input)

        # mask out some config that is subject to change each run
        if expected_in_output:
            received_output = "\n".join(received_output)
            for out in expected_in_output:
                assert out in received_output
        else:
            for idx, line in enumerate(received_output):
                mask = "X" * 50
                if "filename" in line:
                    received_output[idx] = mask

            if self.UPDATE_FIXTURES:
                update_fixtures(request, index, received_output, comment, testname=testname)
            dir_path, file_name = fixture_path_from_request(request, index, testname=testname)
            with open(f"{dir_path}/{file_name}") as infile:
                expected_output = json.load(infile)["output"]

            assert expected_output == received_output
