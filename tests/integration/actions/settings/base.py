"""Base configuration for ``settings`` interactive/stdout tests."""

import difflib
import os

from collections.abc import Generator

import pytest

from tests.defaults import FIXTURES_DIR
from tests.integration._common import retrieve_fixture_for_step
from tests.integration._common import update_fixtures
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._tmux_session import TmuxSession


TEST_FIXTURE_DIR = FIXTURES_DIR / "integration/actions/settings"

base_steps = (
    UiTestStep(user_input=":f App", comment="filter for app settings"),
    UiTestStep(user_input=":0", comment="app settings details"),
    UiTestStep(user_input=":back", comment="return to filtered settings list"),
    UiTestStep(
        user_input=":f",
        comment="clear filter, full list",
        present=["Ansible runner artifact dir", "Help config"],
        mask=True,
    ),
    UiTestStep(user_input=":f Exec", comment="filter using a different index"),
    UiTestStep(user_input=":3", comment="execution_environment_image details"),
    UiTestStep(user_input=":back", comment="return to filtered list"),
    UiTestStep(
        user_input=":f",
        comment="clear filter, full list",
        present=["Ansible runner artifact dir", "Help config"],
        mask=True,
    ),
)


def _resolve_search_for(
    step: UiTestStep,
    cli_prompt: str,
) -> str:
    """Resolve the search_within_response from a UiTestStep.

    Args:
        step: The test step
        cli_prompt: The CLI prompt string

    Returns:
        The resolved search string

    Raises:
        ValueError: When the test mode is not set
    """
    if step.search_within_response is SearchFor.HELP:
        return ":help help"
    if step.search_within_response is SearchFor.PROMPT:
        return cli_prompt
    if step.search_within_response is SearchFor.WARNING:
        return "Warning"
    msg = "test mode not set"
    raise ValueError(msg)


def _mask_settings_output(
    received_output: list[str],
    maskables: list[str],
) -> None:
    """Mask columns in output lines that match maskable prefixes.

    Args:
        received_output: The output lines to mask in place
        maskables: List of prefixes to match for masking
    """
    mask_column_name = "Current"
    column_start = received_output[0].find(mask_column_name)
    if column_start == -1:
        return
    mask = len(mask_column_name) * "X"
    for idx, line in enumerate(received_output):
        if any(f"│{m}" in line for m in maskables):
            received_output[idx] = received_output[idx][0:column_start] + mask


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
    """Base class for interactive/stdout ``settings`` tests."""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 25
    PANE_WIDTH = 300

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(
        self,
        request: pytest.FixtureRequest,
    ) -> Generator[TmuxSession, None, None]:
        """Tmux fixture for this module.

        Args:
            request: Used for generating test id

        Yields:
            tmux_session object
        """
        with TmuxSession(
            setup_commands=[
                "export ANSIBLE_NAVIGATOR_ANSIBLE_RUNNER_TIMEOUT=42",
                "export PAGER=cat",
            ],
            request=request,
            pane_height=self.PANE_HEIGHT,
            pane_width=self.PANE_WIDTH,
        ) as tmux_session:
            yield tmux_session

    def test(
        self,
        request: pytest.FixtureRequest,
        tmux_session: TmuxSession,
        step: UiTestStep,
        skip_if_already_failed: None,
    ) -> None:
        """Run the tests for ``settings``, mode and ``ee`` set in child class.

        Args:
            request: Used for generating test id
            tmux_session: tmux_session object
            step: UiTestStep object
            skip_if_already_failed: Fixture that stops parametrized tests running on first failure.
        """
        search_within_response = _resolve_search_for(step, tmux_session.cli_prompt)

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )
        if step.mask:
            maskables = [
                "App",
                "Collection doc cache path",
                "Current settings file",
            ]
            _mask_settings_output(received_output, maskables)

        fixtures_update_requested = (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        )
        _check_fixtures(request, step, received_output, fixtures_update_requested)
