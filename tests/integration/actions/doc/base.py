""" base class for config interactive tests
"""
import difflib
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
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "pane_height": "2000",
            "pane_width": "200",
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

            print(f"received_output is:\n{received_output}")
            print(f"expected_in_output is:\n{expected_in_output}")
            for out in expected_in_output:
                assert out in received_output
        else:
            updated_received_output = []
            for line in received_output:
                mask = "X" * 50
                if "filename" in line or "│warnings:" in line:
                    updated_received_output.append(mask)
                else:
                    for value in ["time=", "skipping entry", "failed:", "permission denied"]:
                        if value in line:
                            break
                    else:
                        updated_received_output.append(line)

            if self.UPDATE_FIXTURES:
                update_fixtures(request, index, updated_received_output, comment, testname=testname)
            dir_path, file_name = fixture_path_from_request(request, index, testname=testname)
            with open(f"{dir_path}/{file_name}", encoding="utf-8") as infile:
                expected_output = json.load(infile)["output"]

            assert expected_output == updated_received_output, "\n" + "\n".join(
                difflib.ndiff(expected_output, updated_received_output)
            )
