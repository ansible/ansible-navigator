"""Base class for serialization interactive tests."""
import difflib
import os

from typing import Generator

import pytest

from ....defaults import FIXTURES_COLLECTION_DIR
from ..._common import copytree
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._tmux_session import TmuxSession


class SerUiTestStep(UiTestStep):
    """Custom test step for capturing with escape codes."""

    search_within_response: str = ":help"


# Note the order here: yaml, markdown, json, markdown, yaml
# This was done to ensure there was a screen change for each step
# json and yaml will render a string the same, markdown with provide some
# highlighting

base_steps = (
    SerUiTestStep(user_input=":0", comment="coll_1 content, menu"),
    SerUiTestStep(user_input=":1", comment="mod_1 full, yaml"),
    SerUiTestStep(user_input=":json", comment="mod_1 full, json"),
    SerUiTestStep(user_input=":markdown", comment="mod_1 full, markdown"),
    SerUiTestStep(user_input=":yaml", comment="mod_1 full, yaml"),
    SerUiTestStep(user_input=":{{ examples }}", comment="mod_1 examples, yaml"),
    SerUiTestStep(user_input=":markdown", comment="mod_1 examples, markdown"),
    SerUiTestStep(user_input=":json", comment="mod_1 examples, json"),
    SerUiTestStep(user_input=":markdown", comment="mod_1 examples, markdown"),
    SerUiTestStep(user_input=":yaml", comment="mod_1 examples, yaml"),
    SerUiTestStep(user_input=":back", comment="mod_1 full, yaml"),
    SerUiTestStep(user_input=":back", comment="coll_1 content, menu"),
    SerUiTestStep(user_input=":2", comment="role_full details, yaml"),
    SerUiTestStep(user_input=":markdown", comment="role_full details, markdown"),
    SerUiTestStep(user_input=":json", comment="role_full details, json"),
    SerUiTestStep(user_input=":yaml", comment="role_full details, yaml"),
    SerUiTestStep(user_input=":{{ readme }}", comment="role_full readme, yaml"),
    SerUiTestStep(user_input=":markdown", comment="role_full readme, markdown"),
    SerUiTestStep(user_input=":json", comment="role_full readme, json"),
    SerUiTestStep(user_input=":markdown", comment="role_full readme, markdown"),
    SerUiTestStep(user_input=":yaml", comment="role_full readme, yaml"),
    SerUiTestStep(user_input=":back", comment="role_full , yaml"),
    SerUiTestStep(user_input=":back", comment="coll_1 content, menu"),
)


class BaseClass:
    """Base class for interactive serialization tests."""

    update_fixtures = False
    pane_height = 2000
    pane_width = 200

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(
        self,
        request: pytest.FixtureRequest,
        os_independent_tmp: str,
    ) -> Generator[TmuxSession, None, None]:
        """Tmux fixture for this module.

        :param request: The request for this fixture
        :param os_independent_tmp: An OS independent tmp directory
        :yields: A tmux session
        """
        tmp_coll_dir = os.path.join(os_independent_tmp, request.node.name, "")
        os.makedirs(tmp_coll_dir, exist_ok=True)
        copytree(
            FIXTURES_COLLECTION_DIR,
            os.path.join(tmp_coll_dir, "collections"),
            dirs_exist_ok=True,
        )
        params = {
            "capture_escape": True,
            "setup_commands": [
                f"cd {tmp_coll_dir}",
                f"export ANSIBLE_COLLECTIONS_PATH={tmp_coll_dir}",
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "pane_height": self.pane_height,
            "pane_width": self.pane_width,
            "unique_test_id": request.node.nodeid,
        }

        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(
        self,
        os_independent_tmp: str,
        request: pytest.FixtureRequest,
        step: SerUiTestStep,
        tmux_session: TmuxSession,
    ):
        """Run the tests for serialization, mode and ``ee`` set in child class.

        :param os_independent_tmp: An OS independent tmp directory
        :param request: The request for this fixture
        :param step: The UI test step
        :param tmux_session: A tmux session
        """
        if step.search_within_response is SearchFor.HELP:
            search_within_response = ":help help"
        elif step.search_within_response is SearchFor.PROMPT:
            search_within_response = tmux_session.cli_prompt
        else:
            search_within_response = step.search_within_response

        received_output = tmux_session.interaction(
            value=step.user_input,
            search_within_response=search_within_response,
        )

        received_output = [
            line.replace(os_independent_tmp, "FIXTURES_COLLECTION_DIR") for line in received_output
        ]

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
                ansi_sidecar=True,
            )

        page = " ".join(received_output)

        if step.present:
            assert all(present in page for present in step.present)

        if step.absent:
            assert not any(look_not in page for look_not in step.absent)

        if not any((step.present, step.absent)):
            expected_output = retrieve_fixture_for_step(request, step.step_index)
            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received"),
            )
