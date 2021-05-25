""" base class for config interactive tests
"""
import difflib
import json
import os

import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession
from ..._interactions import SearchFor
from ..._interactions import Step
from ....defaults import FIXTURES_DIR

CONFIG_FIXTURE = os.path.join(FIXTURES_DIR, "integration", "actions", "config", "ansible.cfg")


base_steps = (
    Step(user_input=":f CACHE_PLUGIN_TIMEOUT", comment="filter for cache plugin timeout"),
    Step(user_input=":0", comment="cache plugin details"),
    Step(user_input=":back", comment="return to filtered list"),
    Step(user_input=":f", comment="clear filter, full list"),
    Step(user_input=":f yaml", comment="filter off screen value"),
    Step(user_input=":3", comment="YAML_FILENAME_EXTENSIONS details"),
    Step(user_input=":back", comment="return to filtered list"),
    Step(user_input=":f", comment="clear filter, full list"),
)


class BaseClass:
    """base class for interactive/stdout config tests"""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 20
    PANE_WIDTH = 300

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(self, request):
        """tmux fixture for this module"""
        params = {
            "setup_commands": ["export ANSIBLE_CACHE_PLUGIN_TIMEOUT=42", "export PAGER=cat"],
            "unique_test_id": request.node.nodeid,
            "pane_height": self.PANE_HEIGHT,
            "pane_width": self.PANE_WIDTH,

        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive/stdout config"""

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

        if step.mask:
            # mask out some config that is subject to change each run
            mask = "X" * 50
            for idx, line in enumerate(received_output):
                if "13│BECOME_PLUGIN_PATH" in line:
                    received_output[idx] = mask
                if "15│CACHE_PLUGIN_CONNECTION" in line:
                    received_output[idx] = mask

        if (
            self.UPDATE_FIXTURES
            or os.environ.get("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES") == "true"
        ):
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
            with open(f"{dir_path}/{file_name}") as infile:
                expected_output = json.load(infile)["output"]

            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received")
            )
