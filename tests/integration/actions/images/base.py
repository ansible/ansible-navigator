"""Base class for images interactive tests.
"""
import difflib
import json
import os

import pytest

from ....defaults import DEFAULT_CONTAINER_IMAGE
from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._tmux_session import TmuxSession


IMAGE_SHORT = DEFAULT_CONTAINER_IMAGE.rsplit("/", maxsplit=1)[-1].split(":")[0]


step_back = Step(user_input=":back", comment="goto info menu", look_fors=["Everything"])

base_steps = (
    Step(
        user_input=f":f {IMAGE_SHORT}",
        comment=f"filter for {IMAGE_SHORT}",
        look_fors=[IMAGE_SHORT],
    ),
    Step(user_input=":0", comment="goto info menu", look_fors=["Everything"]),
    Step(user_input=":0", comment="goto Image information", look_fors=["architecture:"]),
    step_back,
    Step(user_input=":1", comment="goto General information", look_fors=["friendly:"]),
    step_back,
    Step(user_input=":2", comment="goto Ansible information", look_fors=["collections:"]),
    step_back,
    Step(user_input=":3", comment="goto Python information", look_fors=["ansible-runner"]),
    step_back,
    Step(user_input=":4", comment="goto System information", look_fors=["basesystem"]),
    step_back,
    Step(user_input=":5", comment="goto Everything", look_fors=["collections:"]),
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
                    "look_fors": step.look_fors,
                    "look_nots": step.look_nots,
                    "compared_fixture": not any((step.look_fors, step.look_nots)),
                },
            )

        page = " ".join(received_output)

        if step.look_fors:
            assert all(look_for in page for look_for in step.look_fors)

        if step.look_nots:
            assert not any(look_not in page for look_not in step.look_nots)

        if not any((step.look_fors, step.look_nots)):
            dir_path, file_name = fixture_path_from_request(request, step.step_index)
            with open(file=f"{dir_path}/{file_name}", encoding="utf-8") as fh:
                expected_output = json.load(fh)["output"]

            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received"),
            )
