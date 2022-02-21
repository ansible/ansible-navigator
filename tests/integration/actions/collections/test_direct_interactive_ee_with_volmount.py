"""Tests for collections from CLI, interactive, with an EE and volume mount."""
import pytest

from .base import BaseClass


CLI = (
    "cd /tmp && "  # Get out of collection root, ensure test is independent of CWD
    "ansible-navigator collections --execution-environment true "
    "--eev $ANSIBLE_COLLECTIONS_PATH/collections:/tmp/collections_to_volmount:Z "
    "--senv ANSIBLE_COLLECTIONS_PATH=/tmp/collections_to_volmount"
)

testdata = [
    (0, CLI, "ansible-navigator collections browse window"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """Run the tests for collections from CLI, interactive, with an EE."""

    TEST_FOR_MODE = "interactive"
    EXECUTION_ENVIRONMENT_TEST = True
    UPDATE_FIXTURES = False
