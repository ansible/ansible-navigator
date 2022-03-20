"""base class for templar interactive tests
"""
import difflib
import os

from copy import copy
from typing import Optional

import pytest

from ....defaults import FIXTURES_DIR
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._tmux_session import TmuxSession


# run playbook
run_fixture_dir = os.path.join(FIXTURES_DIR, "integration", "actions", "run")
inventory_path = os.path.join(run_fixture_dir, "inventory")
playbook_path = os.path.join(run_fixture_dir, "site.yaml")

base_steps = (
    UiTestStep(user_input=":0", comment="play-1 details"),
    UiTestStep(user_input=":{{ this[0] }}", comment="render menu as content"),
    UiTestStep(user_input=":back", comment="show play-1 details"),
    UiTestStep(user_input=":0", comment="task-1 details"),
    UiTestStep(
        user_input=":doc",
        comment="doc for task",
        present=["module: debug"],
        search_within_response="module: debug",
    ),
    UiTestStep(
        user_input=":{{ examples }}",
        comment="dig examples",
        present=["ansible.builtin.debug:"],
    ),
    UiTestStep(
        user_input=":back",
        comment="show doc",
        present=["module: debug"],
        search_within_response="module: debug",
    ),
    UiTestStep(user_input=":back", comment="show task"),
    UiTestStep(
        user_input=":open {{ task_path }}",
        comment="goto vi",
        search_within_response="name: run integration test play-1",
        present=["name: run integration test play-1"],
    ),
    UiTestStep(user_input=":q!", comment="exit vi"),
)


class BaseClass:
    """base class for interactive templar tests"""

    UPDATE_FIXTURES = False
    TEST_FOR_MODE: Optional[str] = None

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request):
        """Return a new tmux session.

        The EDITOR is set here such that vim will not create swap files.
        """
        params = {
            "pane_height": "1000",
            "pane_width": "500",
            "setup_commands": [
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
                "export EDITOR='vim -n'",
            ],
            "unique_test_id": request.node.nodeid,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        # pylint: disable=too-many-branches
        """test interactive and ``stdout`` mode ``config``"""

        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        elif step.search_within_response is SearchFor.WARNING:
            search_within_response = "WARNING"
        else:
            search_within_response = step.search_within_response

        unmasked_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )
        received_output = copy(unmasked_output)

        if step.mask:
            # mask out some configuration that is subject to change each run
            mask = "X" * 50
            for idx, line in enumerate(received_output):
                if tmux_session.cli_prompt in line:
                    received_output[idx] = mask
                else:
                    for out in ["duration:", "playbook:", "start:", "end:", "task_path:"]:
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
