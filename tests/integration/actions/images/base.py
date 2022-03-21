"""Base class for images interactive tests.
"""
import difflib
import os

import pytest

from ....defaults import DEFAULT_CONTAINER_IMAGE
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._tmux_session import TmuxSession


IMAGE_SHORT = DEFAULT_CONTAINER_IMAGE.rsplit("/", maxsplit=1)[-1].split(":")[0]


step_back = UiTestStep(user_input=":back", comment="goto info menu", present=["Everything"])

base_steps = (
    UiTestStep(
        user_input=f":f {IMAGE_SHORT}",
        comment=f"filter for {IMAGE_SHORT}",
        present=[IMAGE_SHORT],
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


class BaseClass:
    """Base class for interactive images tests."""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request):
        """tmux fixture for this module"""
        params = {
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        """Run the tests for images, mode and ``ee`` set in child class."""

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
