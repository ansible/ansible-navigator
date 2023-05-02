"""The base class for exec interactive and stdout tests."""

from __future__ import annotations

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


TEST_FIXTURE_DIR = Path(FIXTURES_DIR, "integration", "actions", "exec")
TEST_CONFIG_FILE = Path(TEST_FIXTURE_DIR, "ansible-navigator.yaml")


class BaseClass:
    """The base class for interactive/stdout exec tests."""

    update_fixtures = False
    pane_height = 25
    pane_width = 300
    config_file: Path | None = None

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(
        self,
        request: pytest.FixtureRequest,
    ) -> Generator[TmuxSession, None, None]:
        """Tmux fixture for this module.

        :param request: The request for this fixture
        :yields: A tmux session
        """
        params: TmuxSessionKwargs = {
            "request": request,
            "pane_height": self.pane_height,
            "pane_width": self.pane_width,
        }
        if isinstance(self.config_file, Path):
            assert self.config_file.exists()
            params["config_path"] = self.config_file

        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request: pytest.FixtureRequest, tmux_session: TmuxSession, step: UiTestStep):
        """Test interactive/stdout exec.

        :param request: The test request
        :param tmux_session: The tmux session
        :param step: A step within a series of tests
        :raises ValueError: If test mode isn't set
        """
        if step.search_within_response is not SearchFor.PROMPT:
            raise ValueError("test mode not set")

        search_within_response = tmux_session.cli_prompt

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        # Mask out the container hostname
        for idx, line in enumerate(received_output):
            match = "HOSTNAME="
            if line.startswith(match):
                received_output[idx] = f"{match}{'X' * 8}"

        fixtures_update_requested = (
            self.update_fixtures
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

            diff = "\n".join(
                difflib.unified_diff(
                    expected_output,
                    received_output,
                    "expected",
                    "received",
                ),
            )
            assert expected_output == received_output, f"\n{diff}"
