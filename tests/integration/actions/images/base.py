"""Base class for images interactive tests."""
import difflib
import os
import re

import pytest

from ....conftest import default_ee_image_name
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._tmux_session import TmuxSession


# Note: This filters the list of images based on image version
# It is not bullet proof since 2 images could have the same version
IMAGE_VERSION = default_ee_image_name().split(":")[-1]


step_back = UiTestStep(user_input=":back", comment="goto info menu", present=["Everything"])

base_steps = (
    UiTestStep(
        user_input=f":f {IMAGE_VERSION}",
        comment=f"filter for {IMAGE_VERSION}",
        present=[IMAGE_VERSION],
    ),
    UiTestStep(user_input=":0", comment="goto info menu", present=["Everything"]),
    UiTestStep(user_input=":0", comment="goto Image information", present=["architecture:"]),
    step_back,
    UiTestStep(user_input=":1", comment="goto General information", present=["friendly:"]),
    step_back,
    UiTestStep(user_input=":2", comment="goto Ansible information", present=["collections:"]),
    step_back,
    UiTestStep(user_input=":3", comment="goto Python information", present=["ansible-runner"]),
    step_back,
    UiTestStep(user_input=":4", comment="goto System information", present=["basesystem"]),
    step_back,
    UiTestStep(user_input=":5", comment="goto Everything", present=["collections:"]),
)


def some_time_repl(match: re.Match) -> str:
    """Replace the match string with a string of the same length.

    :param match: The string matched
    :returns: A padded replacement string
    """
    match_len = len(match.group())
    return "some time ago".ljust(match_len)


class BaseClass:
    """Base class for interactive images tests."""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request):
        """Tmux fixture for this module.

        :param request: A fixture providing details about the test caller
        :yields: Tmux session
        """
        params = {
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        """Run the tests for images, mode and ``ee`` set in child class.

        :param request: A fixture providing details about the test caller
        :param tmux_session: The tmux session to use
        :param step: Step index to use
        :raises ValueError: When the test mode is not set
        """
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        elif step.search_within_response is SearchFor.WARNING:
            search_within_response = "Warning"
        else:
            raise ValueError("test mode not set")

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        # Replace images ages (e.g. 4 days ago)
        re_time_ago = re.compile(r"(About an|\d+)\s(minute|hour|day|month)s?\sago\s+")
        for idx, line in enumerate(received_output):
            new_line = re.sub(re_time_ago, some_time_repl, line)
            received_output[idx] = new_line

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
