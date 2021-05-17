""" base class for config interactive tests
"""
import difflib
import json
import os

from typing import Optional

import pytest

from ..._common import copytree
from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession

from ....defaults import FIXTURES_COLLECTION_DIR


class BaseClass:
    # pylint: disable=attribute-defined-outside-init
    """base class for interactive collections tests"""

    UPDATE_FIXTURES = False
    EXECUTION_ENVIRONMENT_TEST = False
    TEST_FOR_MODE: Optional[str] = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_collections_session")
    def _fixture_tmux_config_session(request, os_indendent_tmp):
        """tmux fixture for this module"""

        tmp_coll_dir = os.path.join(os_indendent_tmp, request.node.name, "")
        os.makedirs(tmp_coll_dir, exist_ok=True)
        copytree(
            FIXTURES_COLLECTION_DIR, os.path.join(tmp_coll_dir, "collections"), dirs_exist_ok=True
        )
        params = {
            "setup_commands": [
                f"cd {tmp_coll_dir}",
                f"export ANSIBLE_COLLECTIONS_PATH={tmp_coll_dir}",
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "pane_height": "2000",
            "pane_width": "200",
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self,
        request,
        os_indendent_tmp,
        tmux_collections_session,
        index,
        user_input,
        comment,
    ):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive config"""

        # wait on help here to ensure we get the welcome screen and subsequent screens
        # after entering a : command

        ignore_within_response = "Collecting collection content"
        if self.TEST_FOR_MODE == "interactive":
            search_within_response = ":help help"
        else:
            raise ValueError(
                "Value of 'TEST_FOR_MODE' is not set."
                " Valid value is either 'interactive' or 'stdout'"
            )

        received_output = tmux_collections_session.interaction(
            user_input, search_within_response, ignore_within_response=ignore_within_response
        )

        received_output = [
            line.replace(os_indendent_tmp, "FIXTURES_COLLECTION_DIR") for line in received_output
        ]

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
