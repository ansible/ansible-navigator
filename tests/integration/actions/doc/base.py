"""Base class for doc interactive/stdout tests.
"""
import difflib
import os

from typing import Optional

import pytest

from ....defaults import FIXTURES_COLLECTION_DIR
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession


class BaseClass:
    """Base class for interactive/stdout doc tests."""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: Optional[str] = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_doc_session")
    def fixture_tmux_doc_session(request):
        """Tmux fixture for this module."""
        params = {
            "pane_height": "2000",
            "pane_width": "200",
            "setup_commands": [
                f"export ANSIBLE_COLLECTIONS_PATH={FIXTURES_COLLECTION_DIR}",
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self,
        request,
        tmux_doc_session,
        index,
        user_input,
        comment,
        testname,
        expected_in_output,
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        """Run the tests for collections, mode and ``ee`` set in child class."""
        if self.TEST_FOR_MODE == "interactive":
            search_within_response = ":help help"
        elif self.TEST_FOR_MODE == "stdout":
            search_within_response = tmux_doc_session.cli_prompt
            # clear the screen so it starts with stdout
            user_input = f"clear && {user_input}"
        else:
            raise ValueError(
                "Value of 'TEST_FOR_MODE' is not set."
                " Valid value is either 'interactive' or 'stdout'",
            )

        received_output = tmux_doc_session.interaction(user_input, search_within_response)
        updated_received_output = []
        mask = "X" * 50
        for line in received_output:
            if tmux_doc_session.cli_prompt in line:
                updated_received_output.append(mask)
            elif "filename" in line or "│warnings:" in line:
                updated_received_output.append(mask)
            else:
                for value in ["time=", "skipping entry", "failed:", "permission denied"]:
                    if value in line:
                        break
                else:
                    updated_received_output.append(line)

        if expected_in_output:
            for out in expected_in_output:
                assert any(out in line for line in received_output), (out, received_output)
        else:
            fixtures_update_requested = (
                self.UPDATE_FIXTURES
                or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
            )
            if fixtures_update_requested:
                update_fixtures(request, index, updated_received_output, comment, testname=testname)

            expected_output = retrieve_fixture_for_step(request, index, testname)
            assert expected_output == updated_received_output, "\n" + "\n".join(
                difflib.unified_diff(
                    expected_output,
                    updated_received_output,
                    "expected",
                    "received",
                ),
            )
