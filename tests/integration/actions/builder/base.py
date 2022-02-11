"""Base class for ``builder`` stdout tests."""
import difflib
import os

import pytest

from ....defaults import FIXTURES_DIR
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._tmux_session import TmuxSession


BUILDER_FIXTURE = os.path.join(FIXTURES_DIR, "common", "builder", "test_ee")


class BaseClass:
    """Base class for stdout ``builder`` tests."""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 300
    PANE_WIDTH = 300

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(self, request):
        """Generate a tmux fixture for this module.

        :param request: A fixture providing details about the test caller
        :yields: A tmux session
        """
        params = {
            "setup_commands": ["export ANSIBLE_CACHE_PLUGIN_TIMEOUT=42", "export PAGER=cat"],
            "unique_test_id": request.node.nodeid,
            "pane_height": self.PANE_HEIGHT,
            "pane_width": self.PANE_WIDTH,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        """Run the tests for ``builder``, mode and ``ee`` set in child class.

        :param request: A fixture providing details about the test caller
        :param tmux_session: The tmux session to use
        :param step: The commands to issue and content to look for
        :raises ValueError: When the test mode is not set
        """
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        else:
            raise ValueError("test mode not set")

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
            timeout=600,
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
                    "present": step.present,
                    "absent": step.absent,
                    "compared_fixture": not any((step.present, step.absent)),
                },
            )

        page = " ".join(received_output)

        if step.present:
            assert all(present in page for present in step.present)

        if step.absent:
            assert not any(absent in page for absent in step.absent)

        if not any((step.present, step.absent)):
            expected_output = retrieve_fixture_for_step(request, step.step_index)
            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received"),
            )
