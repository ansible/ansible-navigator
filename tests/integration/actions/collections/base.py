""" base class for config interactive tests
"""
import difflib
import json
import os
import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._common import TmuxSession

from ....defaults import FIXTURES_COLLECTION_DIR


class BaseClass:
    """base class for interactive collections tests"""

    UPDATE_FIXTURES = False
    EXECUTION_ENVIRONMENT_TEST = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_collections_session")
    def fixture_tmux_config_session(request):
        """tmux fixture for this module"""
        params = {
            "window_name": request.node.name,
            "setup_commands": [
                "cd tests/fixtures/common",
                f"export ANSIBLE_COLLECTIONS_PATH={FIXTURES_COLLECTION_DIR}",
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "pane_height": "2000",
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self, request, tmux_collections_session, index, user_input, comment, collection_fetch_prompt
    ):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive config"""
        received_output = tmux_collections_session.interaction(
            user_input, wait_on_collection_fetch_prompt=collection_fetch_prompt
        )
        mask = "X" * 5
        # mask out some config that is subject to change each run
        for idx, line in enumerate(received_output):
            if "path:" in line:
                received_output[idx] = mask

            contents = line.split()
            # mask path in the first collection window
            if self.EXECUTION_ENVIRONMENT_TEST:
                path_index = 4
            else:
                path_index = 3
            if len(contents) == (path_index + 1) and os.path.isdir(contents[-1].strip()):
                received_output[idx] = line.replace(contents[-1], mask)

        if self.UPDATE_FIXTURES:
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(f"{dir_path}/{file_name}") as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.ndiff(expected_output, received_output)
        )
