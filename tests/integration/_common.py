""" some common funcs for the tests
"""
import os
import re
import sys
import pexpect
import tempfile

from argparse import Namespace

from typing import Any
from typing import List
from typing import Tuple
from typing import Optional

from distutils.spawn import find_executable

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
        ee_image: Optional[str] = None,
        cwd: Optional[List] = None,
    ) -> None:
        self._action_name = action_name
        self._container_engine = container_engine
        self._execution_environment = execution_environment
        self._ee_image = ee_image
        self._cwd = cwd
        self._app_args = {
            "container_engine": self._container_engine,
            "execution_environment": self._execution_environment,
            "ee_image": self._ee_image,
            "cwd": self._cwd,
        }
        self._app_action = __import__(
            f"ansible_navigator.actions.{self._action_name}", globals(), fromlist=["Action"]
        )

    def callable_pass_one_arg(self, value=0):
        """a do nothing callable"""
        pass

    def callable_pass(self, **kwargs):
        """a do nothing callable"""
        pass

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
    if name is None:
        name = "python"
    exec_path = find_executable(name)
    if not exec_path:
        raise ValueError(f"{name} executable not found")
    return exec_path


def _run_command(
    command: List,
    user_interactions: List,
    expected_patterns: List,
    config_path: Optional[str] = None,
):
    env = os.environ.copy()
    if len(user_interactions) != len(expected_patterns):
        raise ValueError("length of 'user_interactions' and 'expected_patterns' should be same")
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "ansible-navigator.yaml"
        )
    env.update({"ANSIBLE_NAVIGATOR_CONFIG": config_path})

    stdout_handle = tempfile.TemporaryFile(mode="w+")

    try:
        child = pexpect.spawn(
            command[0],
            command[1:],
            cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
            env=env,
            encoding="utf-8",
            codec_errors="replace",
            echo=False,
            use_poll=defaults.pexpect_use_poll,
        )
        child.logfile_read = stdout_handle
        while child.isalive():
            result_id = child.expect(expected_patterns, timeout=defaults.pexpect_timeout)
            interaction = user_interactions[result_id]
            expected_patterns.pop(result_id)
            user_interactions.pop(result_id)
            child.sendline(interaction)
    except pexpect.exceptions.EOF:
        pass

    stdout_handle.seek(0)
    out = stdout_handle.read()
    stdout_handle.flush()
    stdout_handle.close()
    child.close()

    return out


def _sanitize_response(data):
    ansi_escape = re.compile("\x1B(?:[@-Z\\-_]|\\[[0-?]*[ -/]*[@-~])|\\(B")
    return ansi_escape.sub("", data)


def execute_command(
    cmdline_args, user_interactions, expected_patterns, exe_name=None, sanitize=True
):
    py_exec = get_executable_path(exe_name)
    cmd = [py_exec] + cmdline_args
    out = _run_command(cmd, user_interactions, expected_patterns)
    if sanitize:
        out = _sanitize_response(out)
    return out
