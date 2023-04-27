"""Tests for ``images`` from CLI, stdout."""
import pytest

from tests.defaults import id_func

from ....conftest import default_ee_image_name
from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import IMAGE_NO_VERSION
from .base import BaseClass


class StdoutCommand(Command):
    """Stdout command."""

    subcommand = "images"
    preclear = True


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="print image to stdout",
        user_input=StdoutCommand(
            cmdline="",
            mode="stdout",
            execution_environment=True,
            raw_append=" | grep creator",
        ).join(),
        present=[f"repository: {IMAGE_NO_VERSION}"],
    ),
    ShellCommand(
        comment="print all details to stdout",
        user_input=StdoutCommand(
            cmdline="--details --display-color false",
            mode="stdout",
            execution_environment=True,
            raw_append=" | grep '^[a-z]'",
        ).join(),
        present=[
            "ansible_collections",
            "ansible_version",
            f"image_name: {default_ee_image_name()}",
            "os_release",
            "python_packages",
            "python_version",
            "redhat_release",
            "system_packages",
        ],
    ),
    ShellCommand(
        comment="print all details to stdout",
        user_input=StdoutCommand(
            cmdline="-d ansible_collections -d ansible_version --display-color false",
            mode="stdout",
            execution_environment=True,
            raw_append=" | grep '^[a-z]'",
        ).join(),
        present=[
            "ansible_collections",
            "ansible_version",
            f"image_name: {default_ee_image_name()}",
        ],
        absent=[
            "os_release",
            "python_packages",
            "python_version",
            "redhat_release",
            "system_packages",
        ],
    ),
    ShellCommand(
        comment="print all details to stdout",
        user_input=StdoutCommand(
            cmdline="-d foo -d bar",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=[
            "must be one or more of",
        ],
    ),
    ShellCommand(
        comment="print image details as json output",
        user_input=StdoutCommand(
            cmdline="",
            mode="stdout",
            format="json",
            execution_environment=True,
            raw_append=" | grep creator",
        ).join(),
        present=['"name": "creator-ee"'],
    ),
)

steps = add_indices(stdout_tests)


@pytest.mark.parametrize("step", steps, ids=id_func)
class Test(BaseClass):
    """Run the tests for ``images`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
