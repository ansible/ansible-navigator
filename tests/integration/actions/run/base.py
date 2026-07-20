"""Base class for run interactive/stdout tests."""

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
run_fixture_dir = FIXTURES_DIR / "integration" / "actions" / "run"
inventory_path = run_fixture_dir / "inventory"
playbook_path = run_fixture_dir / "site.yaml"

common_fixture_dir = FIXTURES_DIR / "common" / "collections"
PLAYBOOK_COLLECTION = "company_name.coll_1.playbook_1"

base_steps = (
    UiTestStep(user_input=":0", comment="play-1 details"),
    UiTestStep(user_input=":0", comment="task-1 details"),
    UiTestStep(user_input=":back", comment="play-1 details"),
    UiTestStep(user_input=":1", comment="play-1 task-2 details"),
    UiTestStep(user_input=":back", comment="play-1 details"),
    UiTestStep(user_input=":back", comment="all play details"),
    UiTestStep(user_input=":1", comment="play-2 details"),
    UiTestStep(user_input=":0", comment="play-2 task-1 details"),
    UiTestStep(user_input=":back", comment="play-2 details"),
    UiTestStep(user_input=":1", comment="play-2 task-2 details"),
    UiTestStep(user_input=":back", comment="play-2 details"),
    UiTestStep(user_input=":back", comment="all play details"),
    UiTestStep(user_input=":st", comment="display stream"),
)


RUN_MASK_PATTERNS = ("duration:", "playbook:", "start:", "end:", "task_path:")


def _resolve_search_for(
    step: UiTestStep,
    cli_prompt: str,
) -> str | list[str]:
    """Resolve the search_within_response from a UiTestStep.

    Args:
        step: The test step
        cli_prompt: The CLI prompt string

    Returns:
        The resolved search value
    """
    if step.search_within_response is SearchFor.HELP:
        return ":help help"
    if step.search_within_response is SearchFor.PROMPT:
        return cli_prompt
    if step.search_within_response is SearchFor.WARNING:
        return "Warning"
    return step.search_within_response


def _mask_run_output(
    received_output: list[str],
    cli_prompt: str,
    mask_patterns: tuple[str, ...] = RUN_MASK_PATTERNS,
) -> None:
    """Mask lines containing prompts or variable run data in place.

    Args:
        received_output: The output lines to mask in place
        cli_prompt: The CLI prompt string
        mask_patterns: Patterns that trigger masking
    """
    mask = "X" * 50
    for idx, line in enumerate(received_output):
        if cli_prompt in line or any(out in line for out in mask_patterns):
            received_output[idx] = mask


def _check_fixtures(
    request: pytest.FixtureRequest,
    step: UiTestStep,
    received_output: list[str],
    update_requested: bool,
) -> None:
    """Update fixtures if requested and assert expected output.

    Args:
        request: A fixture providing details about the test caller
        step: The test step
        received_output: The output received from the session
        update_requested: Whether fixture updates are requested
    """
    if update_requested:
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


class BaseClass:
    """Base class for run interactive/stdout tests."""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: str | None = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request: pytest.FixtureRequest) -> Generator[TmuxSession]:
        """Generate a tmux fixture for this module.

        Args:
            request: A fixture providing details about the test caller

        Yields:
            A tmux session
        """
        params: TmuxSessionKwargs = {
            "pane_height": 1000,
            "pane_width": 500,
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
            request: A fixture providing details about the test caller
            tmux_session: The tmux session to use
            step: The commands to issue and content to look for
            skip_if_already_failed: Fixture that stops parametrized tests running on first failure.
        """
        search_within_response = _resolve_search_for(step, tmux_session.cli_prompt)

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        if step.mask:
            _mask_run_output(received_output, tmux_session.cli_prompt)

        fixtures_update_requested = self.UPDATE_FIXTURES or (
            os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
            and not any((step.present, step.absent))
        )
        _check_fixtures(request, step, received_output, fixtures_update_requested)
