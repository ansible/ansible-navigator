""" base class for run interactive tests
"""

import json
import os
import pytest

from typing import List
from typing import Optional

from ..._common import ActionRunTest
from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._common import TmuxSession


# Not yet used, but it will be
class BaseClass:
    """base class for interactive run tests"""

    UPDATE_FIXTURES = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_run_session")
    def fixture_tmux_run_session(request):
        """tmux fixture for this module"""
        params = {
            "window_name": request.node.name,
        }
        with TmuxSession(**params) as tmux_session:
            yield tmux_session

    def test(self, request, tmux_run_session, index, user_input, comment):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive run"""

        received_output = tmux_run_session.interaction(user_input)

        if self.UPDATE_FIXTURES:
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(os.path.join(dir_path, file_name)) as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output
