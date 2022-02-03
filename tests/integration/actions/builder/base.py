"""Base class for ``builder`` stdout tests.
"""
import difflib
import json
import os

import pytest

from ....defaults import FIXTURES_DIR
from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._tmux_session import TmuxSession


BUIDLER_FIXTURE = os.path.join(FIXTURES_DIR, "common", "builder", "test_ee")


class BaseClass:
    """Base class for stdout ``builder`` tests."""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 300
    PANE_WIDTH = 300

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(self, request):
        """tmux fixture for this module"""
        params = {
            "setup_commands": ["export ANSIBLE_CACHE_PLUGIN_TIMEOUT=42", "export PAGER=cat"],
            "unique_test_id": request.node.nodeid,
            "pane_height": self.PANE_HEIGHT,
            "pane_width": self.PANE_WIDTH,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        """Run the tests for ``builder``, mode and ``ee`` set in child class."""

        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        else:
            raise ValueError("test mode not set")

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        fixtures_update_requested = (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        )
        if fixtures_update_requested:
            update_fixtures(
                request,
                step.step_index,
                received_output,
                step.comment,
                additional_information={
                    "look_fors": step.look_fors,
                    "look_nots": step.look_nots,
                    "compared_fixture": not any((step.look_fors, step.look_nots)),
                },
            )

        page = " ".join(received_output)

        if step.look_fors:
            assert all(look_for in page for look_for in step.look_fors)

        if step.look_nots:
            assert not any(look_not in page for look_not in step.look_nots)

        if not any((step.look_fors, step.look_nots)):
            dir_path, file_name = fixture_path_from_request(request, step.step_index)
            with open(file=f"{dir_path}/{file_name}", encoding="utf-8") as infile:
                expected_output = json.load(infile)["output"]

            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received"),
            )
