"""Base class for collections interactive tests.
"""
import difflib
import os

from typing import Optional

import pytest

from ....defaults import FIXTURES_COLLECTION_DIR
from ..._common import copytree
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession


class BaseClass:
    # pylint: disable=too-few-public-methods
    """Base class for interactive collections tests."""

    UPDATE_FIXTURES = False
    EXECUTION_ENVIRONMENT_TEST = False
    TEST_FOR_MODE: Optional[str] = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_collections_session")
    def _fixture_tmux_config_session(request, os_independent_tmp):
        """Tmux fixture for this module."""

        tmp_coll_dir = os.path.join(os_independent_tmp, request.node.name, "")
        os.makedirs(tmp_coll_dir, exist_ok=True)
        copytree(
            FIXTURES_COLLECTION_DIR,
            os.path.join(tmp_coll_dir, "collections"),
            dirs_exist_ok=True,
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
        os_independent_tmp,
        tmux_collections_session,
        index,
        user_input,
        comment,
    ):
        # pylint: disable=too-many-arguments
        """Run the tests for collections, mode and ``ee`` set in child class.

        wait on help here to ensure we get the welcome screen and subsequent screens
        after entering a : command
        """

        ignore_within_response = "Collecting collection content"
        if self.TEST_FOR_MODE == "interactive":
            search_within_response = ":help help"
        else:
            raise ValueError(
                "Value of 'TEST_FOR_MODE' is not set."
                " Valid value is either 'interactive' or 'stdout'",
            )

        received_output = tmux_collections_session.interaction(
            user_input,
            search_within_response,
            ignore_within_response=ignore_within_response,
        )

        received_output = [
            line.replace(os_independent_tmp, "FIXTURES_COLLECTION_DIR") for line in received_output
        ]

        fixtures_update_requested = (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        )
        if fixtures_update_requested:
            update_fixtures(request, index, received_output, comment)

        expected_output = retrieve_fixture_for_step(request, index)
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.unified_diff(expected_output, received_output, "expected", "received"),
        )
