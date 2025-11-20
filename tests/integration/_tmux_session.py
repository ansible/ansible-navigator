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

        captured = send_and_wait("clear")
        captured = send_and_wait("echo ready")
        if "ready" not in captured:
            msg = f"Failed to retrieve the 'echo ready' output: {captured}"
            raise ValueError(msg)

        captured = send_and_wait("clear")
        if len(captured) != 1 or self.cli_prompt not in captured[0]:
            msg = f"TMUX CLEAR Failure: {captured}."
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
        showing = None
        if self._fail_remaining:
            return self._fail_remaining
        start_time = timer()

        # before issuing commands, determine
        # if presently at command prompt or in TUI
        mode = None
        while True:
            showing = self._capture_pane()

            if showing:
                mode = "shell" if self.cli_prompt in showing[-1] else "app"

            if mode is not None:
                break

            elapsed = timer() - start_time
            if elapsed > timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX MODE TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                showing.insert(0, alert)
                return showing
            time.sleep(0.1)

        # capture the screen, send the value, ensure the screen has changed
        # if at the shell, the prompt should not longer be in the last line
        # for the TUI, ensure the screen has changed
        # this risk here is if the shell command is instant and returns to a prompt
        # before we get the screen this will result in a timeout
        pre_send = self._pane.capture_pane()
        self._pane.send_keys(value)
        command_executed = False
        while True:
            showing = self._capture_pane()

            if showing and showing != pre_send:
                if mode == "shell":
                    command_executed = value not in showing[-1]
                elif mode == "app":
                    command_executed = True

            if command_executed:
                break

            elapsed = timer() - start_time
            if elapsed > timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX EXEC TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                showing.insert(0, alert)
                return showing
            time.sleep(0.1)

        setup_capture_path = self._test_log_dir / "showing_setup.txt"
        timeout_capture_path = self._test_log_dir / "showing_timeout.txt"

        ok_to_return = False
        err_message = "RESPONSE"
        while True:
            showing = self._capture_pane()

            if showing:
                if isinstance(search_within_response, str):
                    for line in showing:
                        if search_within_response in line:
                            ok_to_return = True
                            break
                elif isinstance(search_within_response, list):
                    page = " ".join(showing)
                    ok_to_return = all(search in page for search in search_within_response)

                if ignore_within_response:
                    for line in showing:
                        if ignore_within_response in line:
                            ok_to_return = False
                            break

            if ok_to_return:
                screens = [showing]
                while True:
                    captured = self._capture_pane()

                    screens.append(captured)
                    if len(screens) >= 5 and all(elem == screens[-1] for elem in screens[-5:]):
                        showing = screens[-1]
                        break
                    elapsed = timer() - start_time
                    if elapsed > timeout:
                        err_message = "5 LIKE SCREENS"
                        break
                    time.sleep(0.1)
                break

            elapsed = timer() - start_time
            if elapsed > timeout:
                with setup_capture_path.open(mode="w", encoding="utf-8") as fh:
                    fh.writelines("\n".join(self._setup_capture))

                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                # taint the screen output w/ timestamp so it's never a valid fixture
                alerts = [
                    f"******** ERROR: TMUX '{err_message}'"
                    f" TIMEOUT @ {elapsed}s @ {time_stamp} ********",
                ]
                alerts.append(f"******** Captured to: {timeout_capture_path}")
                showing = alerts + showing
                with timeout_capture_path.open(mode="w", encoding="utf-8") as fh:
                    fh.writelines("\n".join(showing))
                self._fail_remaining = ["******** PREVIOUS TEST FAILURE ********"]
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
