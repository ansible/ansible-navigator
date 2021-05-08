""" base class for config interactive tests
"""
import difflib
import json
import os
import pytest
import shutil

from ..._common import fixture_path_from_request
from ..._common import update_fixtures
from ..._common import TmuxSession

from ....defaults import FIXTURES_COLLECTION_DIR


class BaseClass:
    # pylint: disable=attribute-defined-outside-init
    """base class for interactive collections tests"""

    UPDATE_FIXTURES = False
    EXECUTION_ENVIRONMENT_TEST = False

    @staticmethod
    @pytest.fixture(scope="module", name="tmux_collections_session")
    def _fixture_tmux_config_session(request):
        """tmux fixture for this module"""

        # this ensure the length of the colelction path
        # is the same between MacOS and Linux
        # otherwise ansible-navigator column widths can vary
        tmp_real = os.path.realpath("/tmp")
        if tmp_real != "/private/tmp":
            tmp_real = "/tmp/private"

        tmp_coll_dir = os.path.join(tmp_real, request.node.name, "")
        try:
            shutil.rmtree(tmp_coll_dir)
        except FileNotFoundError:
            pass
        os.makedirs(tmp_coll_dir)
        shutil.copytree(FIXTURES_COLLECTION_DIR, os.path.join(tmp_coll_dir, "collections"))
        params = {
            "window_name": request.node.name,
            "setup_commands": [
                f"cd {tmp_coll_dir}",
                f"export ANSIBLE_COLLECTIONS_PATH={tmp_coll_dir}",
                "export ANSIBLE_DEVEL_WARNING=False",
                "export ANSIBLE_DEPRECATION_WARNINGS=False",
            ],
            "pane_height": "2000",
            "pane_width": "200",
        }
        try:
            with TmuxSession(**params) as tmux_session:
                yield tmux_session
        finally:
            shutil.rmtree(tmp_coll_dir)

    def test(
        self, request, tmux_collections_session, index, user_input, comment, collection_fetch_prompt
    ):
        # pylint:disable=unused-argument
        # pylint: disable=too-few-public-methods
        # pylint: disable=too-many-arguments
        """test interactive config"""
        received_output = tmux_collections_session.interaction(
            user_input, wait_on_collection_fetch_prompt=collection_fetch_prompt
        )

        # mask out collection tmp directory
        tmp_real = os.path.realpath("/tmp")
        if tmp_real != "/private/tmp":
            tmp_real = "/tmp/private"

        received_output = [
            line.replace(tmp_real, "FIXTURES_COLLECTION_DIR") for line in received_output
        ]

        if self.UPDATE_FIXTURES:
            update_fixtures(request, index, received_output, comment)
        dir_path, file_name = fixture_path_from_request(request, index)
        with open(f"{dir_path}/{file_name}") as infile:
            expected_output = json.load(infile)["output"]
        assert expected_output == received_output, "\n" + "\n".join(
            difflib.unified_diff(expected_output, received_output, "expected", "received")
        )
