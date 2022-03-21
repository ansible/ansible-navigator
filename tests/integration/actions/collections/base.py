"""Base class for collections interactive tests.
"""
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


EXPECTED_COLLECTIONS = ["ansible.builtin", "company_name.coll_1", "company_name.coll_2"]

base_steps = (
    UiTestStep(user_input=":1", comment="Browse company_name.coll_1 plugins window"),
    UiTestStep(user_input=":0", comment="lookup_1 plugin docs window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_1 plugins window"),
    UiTestStep(user_input=":1", comment="mod_1 plugin docs window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_1 plugins window"),
    UiTestStep(user_input=":2", comment="role_full details window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_1 plugins window"),
    UiTestStep(user_input=":3", comment="role_minimal details window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_1 plugins window"),
    UiTestStep(
        user_input=":back",
        comment="Back to ansible-navigator collections browse window",
        present=EXPECTED_COLLECTIONS,
    ),
    UiTestStep(user_input=":2", comment="Browse company_name.coll_2 plugins window"),
    UiTestStep(user_input=":0", comment="lookup_2 plugin docs window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_2 plugins window"),
    UiTestStep(user_input=":1", comment="mod_2 plugin docs window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_2 plugins window"),
    UiTestStep(
        user_input=":back",
        comment="Back to ansible-navigator collections browse window",
        present=EXPECTED_COLLECTIONS,
    ),
    # Try some things that should not work but not fail (#1061 and #1062)
    UiTestStep(
        user_input=":collections --ee FFFFF",
        comment="Provide an invalid ee value",
        present=["Errors were encountered while parsing the last command"],
        search_within_response=SearchFor.WARNING,
    ),
    # Dismiss the warning
    UiTestStep(
        user_input="Enter",
        comment="ansible-navigator collections browse window",
        present=EXPECTED_COLLECTIONS,
    ),
    # and repeat some basic browsing
    UiTestStep(user_input=":1", comment="Browse company_name.coll_1 plugins window"),
    UiTestStep(user_input=":0", comment="lookup_1 plugin docs window"),
    UiTestStep(user_input=":back", comment="Back to browse company_name.coll_1 plugins window"),
    UiTestStep(
        user_input=":back",
        comment="Back to ansible-navigator collections browse window",
        present=EXPECTED_COLLECTIONS,
    ),
    UiTestStep(
        user_input=":0",
        comment="Browse ansible.builtin plugins window",
        present=["yum_repository"],
    ),
    UiTestStep(
        user_input=":0",
        comment="Browse ansible.builtin.add_host module",
        present=["ANSIBLE.BUILTIN.ADD_HOST"],
    ),
)


class BaseClass:
    """Base class for interactive ``collections`` tests."""

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
        step: UiTestStep,
        tmux_session: TmuxSession,
    ):
        """Run the tests for ``collections``, mode and ``ee`` set in child class.

        :param os_independent_tmp: An OS independent tmp directory
        :param request: The request for this fixture
        :param step: The UI test step
        :param tmux_session: A tmux session
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
