""" some common funcs for the tests
"""
import os
import re
import sys
import tempfile
import time
import json

from argparse import Namespace
from distutils.spawn import find_executable
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional

import libtmux  # type: ignore
import pytest

from ansible_navigator.app_public import AppPublic
from ansible_navigator.ui_framework.ui import Action as Ui_action
from ansible_navigator.ui_framework.ui import Interaction
from ansible_navigator.ui_framework.ui import Ui
from ansible_navigator.steps import Steps

from .. import defaults


class ActionRunTest:
    def __init__(
        self,
        action_name,
        container_engine: Optional[str] = None,
        execution_environment: Optional[str] = None,
        execution_environment_image: Optional[str] = None,
        cwd: Optional[List] = None,
        set_environment_variable: Optional[Dict] = None,
        pass_environment_variable: Optional[List] = None,
    ) -> None:
        self._action_name = action_name
        self._container_engine = container_engine
        self._execution_environment = execution_environment
        self._execution_environment_image = execution_environment_image
        self._set_environment_variable = set_environment_variable
        self._pass_environment_variable = pass_environment_variable
        self._cwd = cwd
        self._app_args = {
            "container_engine": self._container_engine,
            "execution_environment": self._execution_environment,
            "execution_environment_image": self._execution_environment_image,
            "set_environment_variable": self._set_environment_variable,
            "pass_environment_variable": self._pass_environment_variable,
            "cwd": self._cwd,
        }
        self._app_action = __import__(
            f"ansible_navigator.actions.{self._action_name}", globals(), fromlist=["Action"]
        )

    def callable_pass_one_arg(self, value=0):
        """a do nothing callable"""

    def callable_pass(self, **kwargs):
        """a do nothing callable"""

    def run_action_interactive(self) -> Any:
        """run the action
        The return type is set to Any here since not all actions
        have the same signature, the cooresponding integration test
        will be using the action internals for asserts
        """
        self._app_args.update({"mode": "interactive"})
        args = Namespace(**self._app_args)
        action = self._app_action.Action(args=args)
        steps = Steps()
        app = AppPublic(
            args=args,
            name="test_app",
            rerun=self.callable_pass,
            stdout=[],
            steps=steps,
            update=self.callable_pass,
            write_artifact=self.callable_pass,
        )

        user_interface = Ui(
            clear=self.callable_pass,
            menu_filter=self.callable_pass_one_arg,
            scroll=self.callable_pass_one_arg,
            show=self.callable_pass,
            update_status=self.callable_pass,
            xform=self.callable_pass,
        )
        match = re.match(self._app_action.Action.KEGEX, self._action_name)
        if not match:
            raise ValueError

        ui_action = Ui_action(match=match, value=self._action_name)
        interaction = Interaction(name="test", ui=user_interface, action=ui_action)

        # run the action
        action.run(interaction=interaction, app=app)

        return action

    def run_action_stdout(self, cmdline: List) -> Tuple[str, str]:
        """run the action"""
        self._app_args.update({"mode": "stdout", "cmdline": cmdline})
        args = Namespace(**self._app_args)
        action = self._app_action.Action(args=args)

        # get a tty, runner/docker requires it
        _mtty, stty = os.openpty()

        # preserve current stdin, stdout, stderr
        __stdin__ = sys.stdin
        __stdout__ = sys.stdout
        __stderr__ = sys.stderr

        # pytest psuedo stdin doesn't fileno(), use original
        sys.stdin = stty  # type: ignore

        # set stderr and stdout to fds
        sys.stdout = tempfile.TemporaryFile()  # type: ignore
        sys.stderr = tempfile.TemporaryFile()  # type: ignore

        # run the action
        action.run_stdout()

        # restore stdin
        sys.stdin = __stdin__

        # read and restore stdout
        sys.stdout.seek(0)
        stdout = sys.stdout.read().decode()  # type: ignore
        sys.stdout = __stdout__

        # read and restore stderr
        sys.stderr.seek(0)
        stderr = sys.stderr.read().decode()  # type: ignore
        sys.stderr = __stderr__

        return stdout, stderr


def get_executable_path(name):
    if name == "python":
        exec_path = sys.executable
    else:
        exec_path = find_executable(name)
    if not exec_path:
        raise ValueError(f"{name} executable not found")
    return exec_path


class TmuxSession:
    def __init__(
        self,
        window_name,
        config_path=None,
        cwd=None,
        session_name="ansible-navigator-integration-test",
    ) -> None:
        self._window_name = window_name
        self._config_path = config_path
        self._session_name = session_name
        self._cwd = cwd

        if self._config_path is None:
            self._config_path = os.path.join(
                os.path.dirname(__file__), "..", "fixtures", "ansible-navigator.yml"
            )
        if self._cwd is None:
            # ensure CWD is top folder of library
            self._cwd = os.path.join(os.path.dirname(__file__), "..", "..")

    def __enter__(self):
        # pylint: disable=attribute-defined-outside-init
        self._server = libtmux.Server()
        self._session = self._server.new_session(
            session_name=self._session_name, start_directory=self._cwd, kill_session=True
        )
        self._window = self._session.new_window(self._window_name)
        self._pane = self._window.panes[0]
        self._pane.split_window(attach=False)
        # split vertical
        self._pane.split_window(vertical=False, attach=False)
        # attached to upper left
        self._pane.set_height(20)
        self._pane.set_width(132)
        # do this here so it goes away with the tmux shell session
        self._pane.send_keys(f"export ANSIBLE_NAVIGATOR_CONFIG={self._config_path}")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._server.has_session(self._session_name):
            self._session.kill_session()

    def interaction(self, value):
        """interact with the tmux session"""
        self._pane.send_keys(value, suppress_history=False)
        help_not_on_screen = True
        while help_not_on_screen:
            showing = []
            while not showing:
                time.sleep(0.1)
                showing = self._pane.capture_pane()
            help_not_on_screen = not any(":help help" in line for line in showing)
        return showing


def update_fixtures(request, index, received_output, comment):
    """Used by action plugins to generate the fixtures"""
    dir_path, file_name = fixture_path_from_request(request, index)
    os.makedirs(dir_path, exist_ok=True)
    fixture = {
        "name": request.node.name,
        "index": index,
        "comment": comment,
        "output": received_output,
    }
    with open(f"{dir_path}/{file_name}", "w", encoding="utf8") as outfile:
        json.dump(fixture, outfile, indent=4, ensure_ascii=False, sort_keys=False)


def fixture_path_from_request(request, index):
    """build a dir and file path for a test"""
    path_in_fixture_dir = request.node.nodeid.split("::")[0].lstrip("tests/")
    dir_path = f"{defaults.FIXTURES_DIR}/{path_in_fixture_dir}/{request.node.originalname}"
    file_name = f"{index}.json"
    return dir_path, file_name
