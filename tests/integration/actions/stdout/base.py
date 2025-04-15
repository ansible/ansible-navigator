"""Base class for stdout interactive tests."""

import difflib
import os

from collections.abc import Generator
from pathlib import Path

import pytest

from tests.defaults import FIXTURES_DIR
from tests.integration._common import retrieve_fixture_for_step
from tests.integration._common import update_fixtures
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._tmux_session import TmuxSession
from tests.integration._tmux_session import TmuxSessionKwargs


TEST_FIXTURE_DIR = FIXTURES_DIR / "integration/actions/stdout"
ANSIBLE_PLAYBOOK = TEST_FIXTURE_DIR / "site.yml"
TEST_CONFIG_FILE = TEST_FIXTURE_DIR / "ansible-navigator.yml"

base_steps = UiTestStep(user_input=":0", comment="play-1 details")


class BaseClass:
    """Base class for stdout interactive stdout."""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request: pytest.FixtureRequest) -> Generator[TmuxSession, None, None]:
        """Tmux fixture for this module.

        Args:
            request: A fixture providing details about the test caller

        Yields:
            Tmux session
        """
        params: TmuxSessionKwargs = {
            "config_path": Path(TEST_CONFIG_FILE),
            "pane_height": 100,
            "setup_commands": [
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "request": request,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self,
        request: pytest.FixtureRequest,
        tmux_session: TmuxSession,
        step: UiTestStep,
        skip_if_already_failed: None,
    ) -> None:
        """Run the tests for stdout, mode and EE set in child class.

        Args:
            request: A fixture providing details about the test caller
            tmux_session: The tmux session to use
            step: The commands to issue and content to look for
            skip_if_already_failed: Fixture that stops parametrized tests running on first failure.
        """
        assert ANSIBLE_PLAYBOOK.exists()
        assert TEST_CONFIG_FILE.exists()

        search_within_response: str | list[str]
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        elif step.search_within_response is SearchFor.WARNING:
            search_within_response = "Warning"
        else:
            search_within_response = step.search_within_response
        received_output = tmux_session.interaction(step.user_input, search_within_response)

        index = step.step_index

        fixtures_update_requested = (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        )
        if fixtures_update_requested:
            update_fixtures(request, index, received_output, step.comment)

        expected_output = retrieve_fixture_for_step(request, index)

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
