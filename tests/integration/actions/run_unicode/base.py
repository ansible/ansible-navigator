"""Base class for run interactive/stdout tests, with unicode."""

from __future__ import annotations

import difflib
import os

from typing import TYPE_CHECKING

import pytest

from tests.defaults import FIXTURES_DIR
from tests.integration._common import retrieve_fixture_for_step
from tests.integration._common import update_fixtures
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._tmux_session import TmuxSession
from tests.integration._tmux_session import TmuxSessionKwargs


if TYPE_CHECKING:
    from collections.abc import Generator


# run playbook
run_fixture_dir = FIXTURES_DIR / "integration" / "actions" / "run_unicode"
inventory_path = run_fixture_dir / "inventory"
playbook_path = run_fixture_dir / "site.yaml"

base_steps = (
    UiTestStep(user_input=":0", comment="play-1 details"),
    UiTestStep(user_input=":0", comment="task-1 yaml", present=["航海家"]),
    UiTestStep(user_input=":json", comment="task-1 json", present=["航海家"]),
    UiTestStep(user_input=":back", comment="play-1 details"),
    UiTestStep(user_input=":1", comment="task-2 json", present=["航海家"]),
    UiTestStep(user_input=":yaml", comment="task-2 yaml", present=["航海家"]),
    UiTestStep(user_input=":back", comment="play-1 details"),
    UiTestStep(user_input=":back", comment="all play details"),
    UiTestStep(user_input=":st", comment="display stream"),
)


class BaseClass:
    """Base class for run interactive/stdout tests, with unicode."""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: str | None = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request: pytest.FixtureRequest) -> Generator[TmuxSession]:
        """Tmux fixture for this module.

        Args:
            request: The request for this fixture from a test

        Yields:
            A tmux session
        """
        params: TmuxSessionKwargs = {
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
        """Run the tests for run, mode and ``ee`` set in child class.

        Args:
            request: The request for a test
            tmux_session: The tmux session
            step: A step within a series of tests
            skip_if_already_failed: Fixture that stops parametrized tests running on first failure.
        """
        search_within_response: str | list[str]
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        elif step.search_within_response is SearchFor.WARNING:
            search_within_response = "Warning"
        else:
            search_within_response = step.search_within_response

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        if step.mask:
            # mask out some configuration that is subject to change each run
            mask = "X" * 50
            for idx, line in enumerate(received_output):
                if tmux_session.cli_prompt in line:
                    received_output[idx] = mask
                else:
                    for out in ["duration", "playbook", "start", "end", "task_path"]:
                        if out in line:
                            received_output[idx] = mask

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
