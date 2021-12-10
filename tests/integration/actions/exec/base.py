"""The base class for exec interactive and stdout tests."""

import difflib
import json
import os

from pathlib import Path
from typing import Generator
from typing import Union

import pytest

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._tmux_session import TmuxSession
from ..._interactions import SearchFor
from ..._interactions import Step
from ....defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = Path(FIXTURES_DIR, "integration", "actions", "exec")
TEST_CONFIG_FILE = Path(TEST_FIXTURE_DIR, "ansible-navigator.yaml")


class BaseClass:
    """The base class for interactive/stdout exec tests."""

    UPDATE_FIXTURES = False
    PANE_HEIGHT = 25
    PANE_WIDTH = 300
    CONFIG_FILE: Union[Path, None] = None

    @pytest.fixture(scope="module", name="tmux_session")
    def fixture_tmux_session(
        self, request: pytest.FixtureRequest
    ) -> Generator[TmuxSession, None, None]:
        """Tmux fixture for this module.

        :param request: The request for this fixture
        :yields: A tmux session
        """
        params = {
            "unique_test_id": request.node.nodeid,
            "pane_height": self.PANE_HEIGHT,
            "pane_width": self.PANE_WIDTH,
        }
        if isinstance(self.CONFIG_FILE, Path):
            assert self.CONFIG_FILE.exists()
            params["config_path"] = self.CONFIG_FILE

        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request: pytest.FixtureRequest, tmux_session: TmuxSession, step: Step):
        # pylint: disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """Test interactive/stdout exec.

        :param request: The test request
        :param tmux_session: The tmux session
        :param step: A step within a series of tests
        :raises ValueError: If test mode isn't set
        """
        if step.search_within_response is SearchFor.PROMPT:
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
            with open(f"{dir_path}/{file_name}") as infile:
                expected_output = json.load(infile)["output"]

            assert expected_output == received_output, "\n" + "\n".join(
                difflib.unified_diff(expected_output, received_output, "expected", "received")
            )
