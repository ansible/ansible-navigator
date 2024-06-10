"""Base class for replay interactive tests."""

import difflib
import os

from collections.abc import Generator
from pathlib import Path

import pytest

from tests.defaults import FIXTURES_DIR
from tests.integration._common import retrieve_fixture_for_step
from tests.integration._common import update_fixtures
from tests.integration._tmux_session import TmuxSession


TEST_FIXTURE_DIR = FIXTURES_DIR / "integration/actions/replay"
PLAYBOOK_ARTIFACT = TEST_FIXTURE_DIR / "playbook-artifact.json"
TEST_CONFIG_FILE = TEST_FIXTURE_DIR / "ansible-navigator.yml"


class BaseClass:
    """Base class for replay interactive tests."""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request: pytest.FixtureRequest) -> Generator[TmuxSession, None, None]:
        """Tmux fixture for this module.

        :param request: A fixture providing details about the test caller
        :yields: Tmux session
        """
        with TmuxSession(
            config_path=Path(TEST_CONFIG_FILE),
            pane_height=100,
            setup_commands=[
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            request=request,
        ) as tmux_session:
            yield tmux_session

    def test(
        self,
        request: pytest.FixtureRequest,
        tmux_session: TmuxSession,
        index: int,
        user_input: str,
        comment: str,
        search_within_response: str,
    ) -> None:
        # pylint: disable=too-many-arguments
        """Run the tests for replay, mode and ``ee`` set in child class.

        :param request: A fixture providing details about the test caller
        :param tmux_session: The tmux session to use
        :param index: Step index
        :param user_input: Value to send to the tmux session
        :param comment: Comment to add to the fixture
        :param search_within_response: A list of strings or string to find
        """
        assert PLAYBOOK_ARTIFACT.exists()
        assert TEST_CONFIG_FILE.exists()

        received_output = tmux_session.interaction(user_input, search_within_response)

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
