"""Base class for inventory interactive/stdout tests.
"""
import difflib
import os

import pytest

from ....defaults import FIXTURES_DIR
from ..._common import retrieve_fixture_for_step
from ..._common import update_fixtures
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._tmux_session import TmuxSession


TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "integration", "actions", "inventory")
ANSIBLE_INVENTORY_FIXTURE_DIR = os.path.join(TEST_FIXTURE_DIR, "ansible_inventory", "inventory.yml")
TEST_CONFIG_FILE = os.path.join(TEST_FIXTURE_DIR, "ansible-navigator.yml")


base_steps = (
    UiTestStep(user_input=":0", comment="Browse hosts/ungrouped window"),
    UiTestStep(user_input=":0", comment="Group list window"),
    UiTestStep(user_input=":0", comment="group01 hosts detail window"),
    UiTestStep(user_input=":0", comment="host0101 detail window"),
    UiTestStep(user_input=":back", comment="Previous window (group01 hosts detail window)"),
    UiTestStep(user_input=":back", comment="Previous window (Group list window)"),
    UiTestStep(user_input=":1", comment="group02 hosts detail window"),
    UiTestStep(user_input=":0", comment="host0201 detail window"),
    UiTestStep(user_input=":back", comment="Previous window (group02 hosts detail window)"),
    UiTestStep(user_input=":back", comment="Previous window (Group list window)"),
    UiTestStep(user_input=":2", comment="group03 hosts detail window"),
    UiTestStep(user_input=":0", comment="host0301 detail window"),
    UiTestStep(user_input=":back", comment="Previous window (group03 hosts detail window)"),
    UiTestStep(user_input=":back", comment="Previous window (Group list window)"),
    UiTestStep(user_input=":back", comment="Previous window (Browse hosts/ungrouped window)"),
    UiTestStep(user_input=":back", comment="Previous window (top window)"),
    UiTestStep(user_input=":1", comment="Inventory hostname window"),
    UiTestStep(user_input=":0", comment="host0101 detail window"),
    UiTestStep(
        user_input=":back",
        comment="Previous window after host0101 (Inventory hostname window)",
    ),
    UiTestStep(user_input=":1", comment="host0201 detail window"),
    UiTestStep(
        user_input=":back",
        comment="Previous window after host0201 (Inventory hostname window)",
    ),
    UiTestStep(user_input=":2", comment="host0301 detail window"),
)


class BaseClass:
    """base class for inventory interactive/stdout tests"""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(request):
        """tmux fixture for this module"""
        params = {
            "setup_commands": [
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "pane_height": "2000",
            "pane_width": "500",
            "config_path": TEST_CONFIG_FILE,
            "unique_test_id": request.node.nodeid,
        }

        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_session, step):
        """Run the tests for inventory, mode and ``ee`` set in child class."""
        assert os.path.exists(ANSIBLE_INVENTORY_FIXTURE_DIR)
        assert os.path.exists(TEST_CONFIG_FILE)

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
            # mask out some configuration that is subject to change each run
            mask = "X" * 50
            for idx, line in enumerate(received_output):
                if tmux_session.cli_prompt in line:
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
