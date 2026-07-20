"""The tmux session."""

from __future__ import annotations

import datetime
import os
import shlex
import time
import uuid
import warnings

from pathlib import Path
from timeit import default_timer as timer
from typing import TYPE_CHECKING
from typing import TypedDict

import libtmux
import libtmux.exc


if TYPE_CHECKING:
    import types

    import pytest

from ._common import generate_test_log_dir


class TmuxSessionKwargs(TypedDict, total=False):
    """Tmux session kwargs."""

    config_path: Path
    cwd: Path
    pane_height: int
    pane_width: int
    pull_policy: str
    request: pytest.FixtureRequest
    setup_commands: list[str]
    shell_prompt_timeout: int


class TmuxSession:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    """Tmux session."""

    def __init__(
        self,
        request: pytest.FixtureRequest,
        config_path: Path | None = None,
        cwd: Path | None = None,
        pane_height: int = 20,
        pane_width: int = 200,
        pull_policy: str = "never",
        setup_commands: list[str] | None = None,
        shell_prompt_timeout: int = 10,
    ) -> None:
        """Initialize a tmux session.

        Args:
            request: The request for this fixture
            config_path: The path to a settings file to use
            cwd: The current working directory to set when starting the
                tmux session
            pane_height: The height of the tmux session in lines
            pane_width: The width of the tmux session in characters
            pull_policy: The pull policy to set for the session
            setup_commands: Any commands needing to be run before
                starting the application in the tmux session
            shell_prompt_timeout: The amount of time to wait for a shell
                prompt in seconds after issuing commands in the tmux
                session
        """
        self.cli_prompt: str
        self._config_path = config_path
        self._cwd = cwd
        self._fail_remaining: list[str] = []
        self._pane_height = pane_height
        self._pane_width = pane_width
        self._pull_policy = pull_policy
        self._session: libtmux.session.Session
        self._session_name = str(uuid.uuid4())
        self._setup_capture: str | list[str]
        self._setup_commands = setup_commands or []
        self._shell_prompt_timeout = shell_prompt_timeout
        self._test_log_dir = generate_test_log_dir(request)

        if self._cwd is None:
            # ensure CWD is top folder of library
            self._cwd = Path(__file__).parent.parent.parent

    def _build_tmux_session(self) -> None:
        """Create a new tmux session.

        Retry here do to errors captured here:
        https://github.com/ansible/ansible-navigator/issues/812

        Raises:
            libtmux.exc.LibTmuxException: If tries are exceeded
        """
        count = 1
        tries = 3
        while count <= tries:
            try:
                self._session = self._server.new_session(
                    session_name=self._session_name,
                    start_directory=str(self._cwd),
                    kill_session=True,
                    attach=False,
                )
                break
            except libtmux.exc.LibTmuxException as exc:
                warnings.warn(
                    f"tmux session failure #{count}: {exc!s}",
                    RuntimeWarning,
                    stacklevel=2,
                )
                if count == tries:
                    raise
                count += 1

    def __enter__(self) -> TmuxSession:  # noqa: PYI034
        """Enter the tmux session.

        Returns:
            The tmux session

        Raises:
            ValueError: If the time is exceeded for finding the shell
                prompt
        """
        # pylint: disable=attribute-defined-outside-init

        self._server = libtmux.server.Server()
        self._build_tmux_session()
        self._window = self._session.windows[0]
        self._pane = self._window.panes[0]
        self._window.resize(height=self._pane_height, width=self._pane_width)

        # Figure out where the tox initiated venv is. In environments where a
        # venv is activated as part of bashrc, $VIRTUAL_ENV won't be what we
        # expect inside of tmux, so we can't depend on it. We *must* determine
        # it before we enter tmux. Do this before we switch to bash
        venv_path = os.environ.get("VIRTUAL_ENV")
        venv = "" if venv_path is None else shlex.quote(str(Path(venv_path) / "bin" / "activate"))

        # get the USER before we start a clean shell
        user = os.environ.get("USER")
        home = os.environ.get("HOME")

        # set a clean shell and predictable prompt
        self.cli_prompt = "bash$"
        self._pane.send_keys("bash")
        self._pane.send_keys("clear && env -i bash --noprofile --norc")
        self._pane.send_keys(f"export PS1={self.cli_prompt}")

        # set environment variables for this session
        tmux_common = []
        if venv:
            tmux_common.append(f". {venv}")
        tmux_common.append("export TERM=xterm")
        tmux_common.append("export LANG=en_US.UTF-8")
        tmux_common.append(f"export HOME='{home}'")
        tmux_common.append(f"export USER='{user}'")
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_CONFIG='{self._config_path}'")
        tmux_common.append("export ANSIBLE_NAVIGATOR_LOG_LEVEL=debug")

        log_file = self._test_log_dir / "ansible-navigator.log"
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_LOG_FILE='{log_file!s}'")
        playbook_artifact = self._test_log_dir / "playbook-artifact.log"
        tmux_common.append(
            f"export ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_SAVE_AS='{playbook_artifact!s}'",
        )
        collection_doc_cache = self._test_log_dir / "collection_doc_cache.db"
        tmux_common.append(
            f"export ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH='{collection_doc_cache!s}'",
        )
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_PULL_POLICY='{self._pull_policy}'")

        set_up_commands = tmux_common + self._setup_commands

        def send_and_wait(cmd: str) -> list[str]:
            """Send commands and waits for prompt to appear.

            Args:
                cmd: command to be executed.

            Returns:
                terminal captured lines

            Raises:
                ValueError: if prompt is not found after timeout
            """
            # We observed that on some platforms initialization can fail as
            # commands are sent too quickly.
            self._pane.send_keys(cmd)
            captured: str | list[str] = []
            timeout = time.time() + self._shell_prompt_timeout
            while not captured or not captured[-1].endswith(self.cli_prompt):
                time.sleep(0.05)
                captured = self._pane.capture_pane()
                if time.time() > timeout:
                    msg = f"Timeout waiting for prompt after running {cmd} under tmux."
                    raise ValueError(msg)
            if isinstance(captured, str):
                return [captured]
            return captured

        # send the setup commands
        for set_up_command in set_up_commands:
            send_and_wait(set_up_command)

        self._setup_capture = self._pane.capture_pane()

        send_and_wait("clear")
        captured = send_and_wait("echo ready")
        if "ready" not in captured:
            msg = f"Failed to retrieve the 'echo ready' output: {captured}"
            raise ValueError(msg)

        # The final clear needs special handling: send_and_wait returns as soon
        # as the prompt appears in the last line, but after 'echo ready' that
        # condition is already satisfied before 'clear' takes effect. So we
        # poll until the pane truly has only the prompt line.
        self._pane.send_keys("clear")
        clear_timeout = time.time() + self._shell_prompt_timeout
        cleared: list[str] = []
        while time.time() < clear_timeout:
            time.sleep(0.1)
            pane_content = self._pane.capture_pane()
            if isinstance(pane_content, str):
                pane_content = [pane_content]
            cleared = [line for line in pane_content if line != ""]
            if len(cleared) == 1 and self.cli_prompt in cleared[0]:
                break
        else:
            msg = f"TMUX CLEAR Failure: {cleared}."
            raise ValueError(msg)

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: types.TracebackType | None,
    ) -> None:
        """Exit the tmux session.

        Args:
            exc_type: exception type
            exc_value: exception value
            exc_traceback: exception traceback
        """
        if self._server.has_session(self._session_name):
            self._session.kill()

    def _capture_pane(self) -> list[str]:
        """Capture the pane.

        Returns:
            The captured pane

        Raises:
            RuntimeError: If there is a runtime error.
        """
        captured = self._pane.capture_pane()
        if isinstance(captured, str):
            return [captured]
        if isinstance(captured, list):
            return captured
        raise RuntimeError

    def _determine_mode(
        self,
        start_time: float,
        timeout: int,
    ) -> tuple[str | None, list[str]]:
        """Determine if the session is at a shell prompt or in a TUI app.

        Args:
            start_time: The timer start value
            timeout: Timeout in seconds

        Returns:
            A tuple of (mode, showing) where mode is 'shell', 'app', or None on timeout
        """
        while True:
            showing = self._capture_pane()

            if showing:
                mode = "shell" if self.cli_prompt in showing[-1] else "app"
                return mode, showing

            elapsed = timer() - start_time
            if elapsed > timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX MODE TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                showing.insert(0, alert)
                return None, showing
            time.sleep(0.1)

    def _wait_for_command_execution(
        self,
        value: str,
        mode: str,
        start_time: float,
        timeout: int,
    ) -> tuple[bool, list[str]]:
        """Send a value and wait for the command to execute.

        Args:
            value: The value to send
            mode: The current mode ('shell' or 'app')
            start_time: The timer start value
            timeout: Timeout in seconds

        Returns:
            A tuple of (success, showing)
        """
        pre_send = self._pane.capture_pane()
        self._pane.send_keys(value)
        while True:
            showing = self._capture_pane()

            if showing and showing != pre_send:
                if mode == "shell" and value not in showing[-1]:
                    return True, showing
                if mode == "app":
                    return True, showing

            elapsed = timer() - start_time
            if elapsed > timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX EXEC TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                showing.insert(0, alert)
                return False, showing
            time.sleep(0.1)

    def _check_response_match(
        self,
        showing: list[str],
        search_within_response: list[str] | str | None,
        ignore_within_response: str | None,
    ) -> bool:
        """Check if the screen content matches the search criteria.

        Args:
            showing: The current screen content
            search_within_response: Strings to find in the response
            ignore_within_response: String that invalidates the match

        Returns:
            True if the response matches
        """
        ok = False
        if isinstance(search_within_response, str):
            ok = any(search_within_response in line for line in showing)
        elif isinstance(search_within_response, list):
            page = " ".join(showing)
            ok = all(search in page for search in search_within_response)

        if (
            ok
            and ignore_within_response
            and any(ignore_within_response in line for line in showing)
        ):
            ok = False
        return ok

    def _wait_for_stable_screen(
        self,
        showing: list[str],
        start_time: float,
        timeout: int,
    ) -> tuple[list[str], bool]:
        """Wait for the screen to stabilize (5 identical captures in a row).

        Args:
            showing: The initial screen content
            start_time: The timer start value
            timeout: Timeout in seconds

        Returns:
            A tuple of (final_showing, timed_out)
        """
        screens = [showing]
        while True:
            captured = self._capture_pane()
            screens.append(captured)
            if len(screens) >= 5 and all(elem == screens[-1] for elem in screens[-5:]):
                return screens[-1], False
            elapsed = timer() - start_time
            if elapsed > timeout:
                return showing, True
            time.sleep(0.1)

    def _handle_response_timeout(
        self,
        showing: list[str],
        err_message: str,
    ) -> list[str]:
        """Handle a timeout while waiting for a response.

        Args:
            showing: The current screen content
            err_message: The error message category

        Returns:
            The annotated screen content
        """
        setup_capture_path = self._test_log_dir / "showing_setup.txt"
        timeout_capture_path = self._test_log_dir / "showing_timeout.txt"

        with setup_capture_path.open(mode="w", encoding="utf-8") as fh:
            fh.writelines("\n".join(self._setup_capture))

        datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        alerts = [
            f"******** ERROR: TMUX '{err_message}'"
            " TIMEOUT @ {elapsed}s @ {time_stamp} ********",
        ]
        alerts.append(f"******** Captured to: {timeout_capture_path}")
        showing = alerts + showing
        with timeout_capture_path.open(mode="w", encoding="utf-8") as fh:
            fh.writelines("\n".join(showing))
        self._fail_remaining = ["******** PREVIOUS TEST FAILURE ********"]
        return showing

    def _wait_for_response(
        self,
        search_within_response: list[str] | str | None,
        ignore_within_response: str | None,
        start_time: float,
        timeout: int,
    ) -> tuple[list[str], bool]:
        """Wait for the expected response to appear on screen.

        Args:
            search_within_response: Strings to find in the response
            ignore_within_response: String that invalidates the match
            start_time: The timer start value
            timeout: Timeout in seconds

        Returns:
            A tuple of (showing, timed_out)
        """
        while True:
            showing = self._capture_pane()

            if showing and self._check_response_match(
                showing,
                search_within_response,
                ignore_within_response,
            ):
                final_showing, stable_timeout = self._wait_for_stable_screen(
                    showing,
                    start_time,
                    timeout,
                )
                if stable_timeout:
                    return self._handle_response_timeout(final_showing, "5 LIKE SCREENS"), True
                return final_showing, False

            elapsed = timer() - start_time
            if elapsed > timeout:
                return self._handle_response_timeout(showing, "RESPONSE"), True
            time.sleep(0.1)

    def interaction(
        self,
        value: str,
        search_within_response: list[str] | str | None = None,
        ignore_within_response: str | None = None,
        timeout: int = 300,
        send_clear: bool = True,
    ) -> list[str]:
        """Interact with the tmux session.

        Args:
            value: Send to screen
            search_within_response: A list of strings or string to find
            ignore_within_response: Ignore screen if this there
            timeout: The amount of time is seconds to allow for
                completion
            send_clear: Send a clear command before sending the value

        Returns:
            The screen content
        """
        if self._fail_remaining:
            return self._fail_remaining
        start_time = timer()

        mode, showing = self._determine_mode(start_time, timeout)
        if mode is None:
            return showing

        success, showing = self._wait_for_command_execution(value, mode, start_time, timeout)
        if not success:
            return showing

        showing, timed_out = self._wait_for_response(
            search_within_response,
            ignore_within_response,
            start_time,
            timeout,
        )
        if timed_out:
            return showing

        # Clear the screen in case subsequent tests produce the same output
        # This ensures the pre_send capture will be different.
        if mode == "shell" and send_clear:
            self._pane.send_keys("clear")

        # Prior to libtmux v0.15, all empty lines were removed
        # from the captured pane. For fixture readability, remove them here
        # https://github.com/tmux-python/libtmux/pull/405/files
        showing = [line for line in showing if line != ""]

        return showing
