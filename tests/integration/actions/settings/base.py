"""Base configuration for ``settings`` interactive/stdout tests."""

import difflib
import os

import pytest

from ....defaults import FIXTURES_DIR
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._tmux_session import TmuxSession


TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "integration/actions/settings")

base_steps = (
    UiTestStep(user_input=":f App", comment="filter for app settings"),
    UiTestStep(user_input=":0", comment="app settings details"),
    UiTestStep(user_input=":back", comment="return to filtered settings list"),
    UiTestStep(
        user_input=":f",
        comment="clear filter, full list",
        present=["Ansible runner artifact dir", "Help playbook"],
        mask=True,
    ),
    UiTestStep(user_input=":f Exec", comment="filter using a different index"),
    UiTestStep(user_input=":3", comment="execution_environment_image details"),
    UiTestStep(user_input=":back", comment="return to filtered list"),
    UiTestStep(
        user_input=":f",
        comment="clear filter, full list",
        present=["Ansible runner artifact dir", "Help playbook"],
        mask=True,
    ),
)


class BaseClass:
    """Base class for interactive/stdout ``settings`` tests."""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 25
    PANE_WIDTH = 300

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(self, request):
        """Tmux fixture for this module.

        :param request: Used for generating test id
        :yields: tmux_session object
        """
        params = {
            "setup_commands": [
                "export ANSIBLE_NAVIGATOR_ANSIBLE_RUNNER_TIMEOUT=42",
                "export PAGER=cat",
            ],
            "unique_test_id": request.node.nodeid,
            "pane_height": self.PANE_HEIGHT,
            "pane_width": self.PANE_WIDTH,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        # pylint: disable=too-many-locals
        """Run the tests for ``settings``, mode and ``ee`` set in child class.

        :param request: Used for generating test id
        :param tmux_session: tmux_session object
        :param step: UiTestStep object
        :raises ValueError: If HELP or PROMPT aren't found
        """
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        elif step.search_within_response is SearchFor.WARNING:
            search_within_response = "WARNING"
        else:
            raise ValueError("test mode not set")

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )
        if step.mask:
            # mask out some settings that is subject to change each run
            maskables = [
                "App",
                "Collection doc cache path",
                "Current settings file",
            ]
            # Determine if a menu is showing
            mask_column_name = "CURRENT"
            column_start = received_output[0].find(mask_column_name)
            column_exists = column_start != -1
            if column_exists:
                mask = len(mask_column_name) * "X"
                for idx, line in enumerate(received_output):
                    if any(f"│{m}" in line for m in maskables):
                        received_output[idx] = received_output[idx][0:column_start] + mask

        # Determine if fixtures need to be updated
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
