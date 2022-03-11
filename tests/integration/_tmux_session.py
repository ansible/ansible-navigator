"""the tmux session"""
import datetime
import os
import shlex
import time
import warnings

from timeit import default_timer as timer
from typing import List
from typing import Optional
from typing import Union

import libtmux

from ._common import generate_test_log_dir


class TmuxSession:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    """tmux session"""

    def __init__(
        self,
        unique_test_id,
        config_path=None,
        cwd=None,
        pane_height=20,
        pane_width=200,
        pull_policy: str = "never",
        setup_commands=None,
        shell_prompt_timeout=10,
    ) -> None:
        """Initialize a tmux session.

        :param unique_test_id: The unique id for this tmux session, the session name
        :param config_path: The path to a settings file to use
        :param cwd: The current working directory to set when starting the tmux session
        :param pane_height: The height of the tmux session in lines
        :param pane_width: The width of the tmux session in characters
        :param pull_policy: The pull policy to set for the session
        :param setup_commands: Any commands needing to be run before starting the application
            in the tmux session
        :param shell_prompt_timeout: The amount of time to wait for a shell prompt in seconds after
            issuing commands in the tmux session
        """
        self.cli_prompt: str
        self._config_path = config_path
        self._cwd = cwd
        self._fail_remaining: List = []
        self._pane_height = pane_height
        self._pane_width = pane_width
        self._pull_policy = pull_policy
        self._session: libtmux.Session
        self._session_name = os.path.splitext(unique_test_id)[0]
        self._setup_capture: List
        self._setup_commands = setup_commands or []
        self._shell_prompt_timeout = shell_prompt_timeout
        self._test_log_dir = generate_test_log_dir(unique_test_id)

        if self._cwd is None:
            # ensure CWD is top folder of library
            self._cwd = os.path.join(os.path.dirname(__file__), "..", "..")

    def _build_tmux_session(self):
        """Create a new tmux session.

        Retry here do to errors captured here:
        https://github.com/ansible/ansible-navigator/issues/812
        """
        count = 1
        tries = 3
        while count <= tries:
            try:
                self._session = self._server.new_session(
                    session_name=self._session_name,
                    start_directory=self._cwd,
                    kill_session=True,
                )
                break
            except libtmux.exc.LibTmuxException as exc:
                warnings.warn(f"tmux session failure #{count}: {str(exc)}", RuntimeWarning)
                if count == tries:
                    raise
                count += 1

    def __enter__(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        self._server = libtmux.Server()
        self._build_tmux_session()
        self._window = self._session.new_window(self._session_name)
        self._pane = self._window.panes[0]
        self._pane.split_window(attach=False)
        # split vertical
        self._pane.split_window(vertical=False, attach=False)
        # attached to upper left
        self._pane.set_height(self._pane_height)
        self._pane.set_width(self._pane_width)

        # Figure out where the tox initiated venv is. In environments where a
        # venv is activated as part of bashrc, $VIRTUAL_ENV won't be what we
        # expect inside of tmux, so we can't depend on it. We *must* determine
        # it before we enter tmux. Do this before we switch to bash
        venv_path = os.environ.get("VIRTUAL_ENV")
        if venv_path is None:
            raise AssertionError(
                "VIRTUAL_ENV environment variable was not set but tox should have set it.",
            )
        venv = os.path.join(shlex.quote(venv_path), "bin", "activate")

        # get the USER before we start a clean shell
        user = os.environ.get("USER")
        home = os.environ.get("HOME")

        # get a clean shell and predictable prompt
        self.cli_prompt = self._get_cli_prompt()

        # set environment variables for this session
        tmux_common = [f". {venv}"]
        tmux_common.append("export TERM=xterm")
        tmux_common.append("export LANG=en_US.UTF-8")
        tmux_common.append(f"export HOME='{home}'")
        tmux_common.append(f"export USER='{user}'")
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_CONFIG='{self._config_path}'")
        tmux_common.append("export ANSIBLE_NAVIGATOR_LOG_LEVEL=debug")

        log_file = os.path.join(self._test_log_dir, "ansible-navigator.log")
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_LOG_FILE='{log_file}'")
        playbook_artifact = os.path.join(self._test_log_dir, "playbook-artifact.log")
        tmux_common.append(
            f"export ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_SAVE_AS='{playbook_artifact}'",
        )
        collection_doc_cache = os.path.join(self._test_log_dir, "collection_doc_cache.db")
        tmux_common.append(
            f"export ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH='{collection_doc_cache}'",
        )
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_PULL_POLICY='{self._pull_policy}'")
        tmux_common.append("env")

        set_up_commands = tmux_common + self._setup_commands
        set_up_command = " && ".join(set_up_commands)

        # send setup, wait for the prompt in last line
        start_time = timer()
        self._pane.send_keys(set_up_command)
        prompt_showing = False
        while True:
            showing = self._pane.capture_pane()
            # find the prompt in the last line of a full screen
            # or at least a screen as big as the list of environment variables
            # because the environment variables were dumped
            if showing:
                prompt_showing = self.cli_prompt in showing[-1] and len(showing) > min(
                    len(tmux_common),
                    int(self._pane_height) - 1,
                )
            if prompt_showing:
                break
            elapsed = timer() - start_time
            if elapsed > self._shell_prompt_timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX SETUP TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                raise ValueError(alert)

            time.sleep(0.1)

        # capture the setup screen
        self._setup_capture = self._pane.capture_pane()

        # clear the screen, wait for prompt in line 0
        start_time = timer()
        self._pane.send_keys("clear")
        prompt_showing = False
        while True:
            showing = self._pane.capture_pane()
            # the screen has been cleared, wait for prompt in first line
            if showing:
                prompt_showing = self.cli_prompt in showing[0]
            if prompt_showing:
                break
            elapsed = timer() - start_time
            if elapsed > self._shell_prompt_timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX CLEAR TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                raise ValueError(alert)
            time.sleep(0.1)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._server.has_session(self._session_name):
            self._session.kill_session()

    def interaction(
        self,
        value,
        search_within_response: Optional[Union[List, str]] = None,
        ignore_within_response=None,
        timeout=300,
    ):
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        """Interact with the tmux session.

        :param value: send to screen
        :param search_within_response: a list of strings or string to find
        :param ignore_within_response: ignore screen if this there
        :param timeout: the amount of time is seconds to allow for completion
        """
        showing = None
        if self._fail_remaining:
            return self._fail_remaining
        start_time = timer()

        # before issuing commands, determine
        # if presently at command prompt or in TUI
        mode = None
        while True:
            showing = self._pane.capture_pane()
            if showing:
                if self.cli_prompt in showing[-1]:
                    mode = "shell"
                else:
                    mode = "app"

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
            showing = self._pane.capture_pane()
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

        setup_capture_path = os.path.join(self._test_log_dir, "showing_setup.txt")
        timeout_capture_path = os.path.join(self._test_log_dir, "showing_timeout.txt")

        ok_to_return = False
        err_message = "RESPONSE"
        while True:

            showing = self._pane.capture_pane()

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
                    screens.append(self._pane.capture_pane())
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
                with open(file=setup_capture_path, mode="w", encoding="utf-8") as fh:
                    fh.writelines("\n".join(self._setup_capture))

                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                # taint the screen output w/ timestamp so it's never a valid fixture
                alerts = [
                    f"******** ERROR: TMUX '{err_message}'"
                    " TIMEOUT @ {elapsed}s @ {time_stamp} ********",
                ]
                alerts.append(f"******** Captured to: {timeout_capture_path}")
                showing = alerts + showing
                with open(file=timeout_capture_path, mode="w", encoding="utf-8") as fh:
                    fh.writelines("\n".join(showing))
                self._fail_remaining = ["******** PREVIOUS TEST FAILURE ********"]
                return showing

        # Clear the screen in case subsequent tests produce the same output
        # This ensures the pre_send capture will be different.
        if mode == "shell":
            self._pane.send_keys("clear")

        return showing

    def _get_cli_prompt(self):
        """get CLI prompt"""
        # start a fresh clean shell, set TERM
        start_time = timer()
        self._pane.send_keys("clear && env -i bash --noprofile --norc")
        bash_prompt_visible = False
        while True:
            showing = self._pane.capture_pane()
            if showing:
                bash_prompt_visible = showing[-1].startswith("bash")
            if bash_prompt_visible:
                break

            elapsed = timer() - start_time
            if elapsed > self._shell_prompt_timeout:
                time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
                alert = f"******** ERROR: TMUX BASH TIMEOUT  @ {elapsed}s @ {time_stamp} ********"
                raise ValueError(alert)
            time.sleep(0.1)
        return showing[-1]
