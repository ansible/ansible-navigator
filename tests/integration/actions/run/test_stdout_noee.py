""" run direct from cli stdout tests
"""
from typing import List

import pytest

from .base import BaseClass
from .base import inventory_path
from .base import playbook_path


# run without EE
CLI_RUN = f"ansible-navigator run {playbook_path} -i {inventory_path} -m stdout --ee false"

testdata_run: List = [
    (0, CLI_RUN, "ansible-navigator run playbook", None),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata_run)
class TestStdoutNoee(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False
