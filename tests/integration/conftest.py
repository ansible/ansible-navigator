"""Integration test fixtures."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.configuration_subsystem.definitions import CliParameters
from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration
from ansible_navigator.utils.functions import shlex_join
from tests.conftest import _cmd_in_tty as cmd_in_tty

from ._action_run_test import ActionRunTest
from ._common import Parameter
from ._common import generate_test_log_dir


if TYPE_CHECKING:
    from collections.abc import Generator


EXECUTION_MODES = ["interactive", "stdout"]


@pytest.fixture
def action_run_stdout() -> Generator[type[ActionRunTest]]:
    """Create a fixture for ActionRunTest.

    :yield: The ActionRunTest class.
    """
    yield ActionRunTest


@pytest.fixture(scope="session")
def test_fixtures_dir() -> Path:
    """Return the test fixture directory.

    Returns:
        The test fixture directory.
    """
    return Path(__file__).parent / ".." / "fixtures"


@pytest.fixture(scope="session")
def os_independent_tmp() -> str:
    """Return an os independent tmp directory.

    This attempts to ensure the length of the ``/tmp``
    is the same between MacOS and Linux
    otherwise ansible-navigator column widths can vary

    Returns:
        The os independent tmp directory.
    """
    tmp_real = Path("/tmp").resolve()
    an_tmp = tmp_real / "an" if tmp_real == "/private/tmp" else Path("/tmp") / "private" / "an"
    an_tmp.mkdir(parents=True, exist_ok=True)
    return str(an_tmp)


@pytest.mark.usefixtures("cmd_in_tty")
class CliRunner:
    """A class to run ansible-navigator in a tty."""

    def __init__(
        self,
        request: pytest.FixtureRequest,
    ) -> None:
        """Initialize the class.

        Args:
            request: The current test request.
        """
        self.cwd: Path | None
        self.parameters: tuple[Parameter, ...]
        self.request: pytest.FixtureRequest = request
        self.settings: ApplicationConfiguration = deepcopy(NavigatorConfiguration)

    def _apply_parameters(self) -> None:
        """Apply the parameters to the settings."""
        default_parameters = (
            Parameter(name="display_color", value=False),
            Parameter(name="log_level", value="debug"),
            Parameter(name="log_append", value=False),
            Parameter(name="log_file", value=generate_test_log_dir(self.request)),
            Parameter(name="mode", value="stdout"),
            Parameter(name="pull_policy", value="never"),
        )
        for parameter in default_parameters:
            self._apply_parameter(parameter)

        for parameter in self.parameters:
            self._apply_parameter(parameter)

    def _apply_parameter(self, parameter: Parameter) -> None:
        """Apply a parameter to the settings.

        Args:
            parameter: The parameter to apply.
        """
        entry = self.settings.entry(parameter.name)
        entry.value.current = str(parameter.value)
        entry.value.source = Constants.TEST

    def to_cmdline(self) -> str:
        """Return the command line to run.

        Returns:
            The command line.
        """
        self._apply_parameters()
        cli_parts = ["ansible-navigator"]
        for entry in self.settings.entries:
            if entry.value.source != Constants.TEST:
                continue
            if entry.name == "app":
                cli_parts.insert(1, entry.value.current)
                continue
            if (
                hasattr(entry, "cli_parameters")
                and isinstance(entry.cli_parameters, CliParameters)
                and isinstance(entry.cli_parameters.short, str)
            ):
                cli_parts.append(entry.cli_parameters.short)
            else:
                pytest.exit(f"Missing cli_parameters for {entry.name} or short isn't a string")
            cli_parts.append(entry.value.current)
        return shlex_join(cli_parts)

    def run(self) -> tuple[str, str, int]:
        """Run ansible-navigator.

        Returns:
            The stdout, stderr, and exit code.
        """
        return cmd_in_tty(self.to_cmdline(), cwd=self.cwd)


@pytest.fixture
def cli_runner(request: pytest.FixtureRequest) -> CliRunner:
    """Create a fixture for the cli runner.

    Args:
        request: The current test request.

    Returns:
        The CliRunner class.
    """
    return CliRunner(request=request)
