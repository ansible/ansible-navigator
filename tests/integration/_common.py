""" some common funcs for the tests
"""
import os
import re
import shlex
import sys
import tempfile
import time
import json

from copy import deepcopy
from timeit import default_timer as timer
from distutils.spawn import find_executable
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
from typing import Optional
from unittest import mock


import libtmux  # type: ignore
import pytest

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
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
        args = deepcopy(NavigatorConfiguration)
        for argument, value in self._app_args.items():
            args.entry(argument).value.current = value
            args.entry(argument).value.source = C.USER_CFG

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
        args = deepcopy(NavigatorConfiguration)
        for argument, value in self._app_args.items():
            args.entry(argument).value.current = value
            args.entry(argument).value.source = C.USER_CFG

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
        test_path,
        config_path=None,
        cwd=None,
        setup_commands=None,
        pane_height=20,
        pane_width=200,
    ) -> None:
        self._test_path = test_path
        self._config_path = config_path
        self._setup_commands = setup_commands or []
        self._cwd = cwd
        self._pane_height = pane_height
        self._pane_width = pane_width
        self._test_log_dir: Union[None, str]
        self._session_name = os.path.splitext(self._test_path)[0]

        if self._cwd is None:
            # ensure CWD is top folder of library
            self._cwd = os.path.join(os.path.dirname(__file__), "..", "..")

    def __enter__(self):
        # pylint: disable=attribute-defined-outside-init
        self._server = libtmux.Server()
        self._session = self._server.new_session(
            session_name=self._session_name, start_directory=self._cwd, kill_session=True
        )
        self._window = self._session.new_window(self._session_name)
        self._pane = self._window.panes[0]
        self._pane.split_window(attach=False)
        # split vertical
        self._pane.split_window(vertical=False, attach=False)
        # attached to upper left
        self._pane.set_height(self._pane_height)
        self._pane.set_width(self._pane_width)

        # get the cli prompt from pane
        self._cli_prompt = self._get_cli_prompt()

        # Figure out where the tox-initiated venv is. In environments where a
        # venv is activated as part of bashrc, $VIRTUAL_ENV won't be what we
        # expect inside of tmux, so we can't depend on it. We *must* determine
        # it before we enter tmux.
        venv_path = os.environ.get("VIRTUAL_ENV")
        if venv_path is None or ".tox" not in venv_path:
            raise AssertionError(
                "VIRTUAL_ENV environment variable was not set but tox should have set it."
            )
        venv = os.path.join(shlex.quote(venv_path), "bin", "activate")

        # send the config envvar + other set up commands
        tmux_common = [f"source {venv}"]
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_CONFIG={self._config_path}")
        tmux_common.append("export ANSIBLE_NAVIGATOR_LOG_LEVEL=debug")

        ci_running = os.environ.get("USER") == "zuul"
        self._test_log_dir = None
        if ci_running:
            self._test_log_dir = os.path.join(
                "/home/zuul", "zuul-output", "anible-navigator", self._test_path
            )
        else:
            self._test_log_dir = os.path.join("./", ".test_logs", self._test_path)
            os.makedirs(self._test_log_dir, exist_ok=True)

        log_file = os.path.join(self._test_log_dir, "ansible-navigator.log")
        tmux_common.append(f"export ANSIBLE_NAVIGATOR_LOG_FILE={log_file}")
        playbook_artifact = os.path.join(self._test_log_dir, "playbook-artifact.log")
        tmux_common.append(
            f"export ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_SAVE_AS={playbook_artifact}"
        )

        set_up_commands = tmux_common + self._setup_commands
        set_up_command = " && ".join(set_up_commands)
        self._pane.send_keys(set_up_command)
        time.sleep(1)

        setup_capture_path = os.path.join(self._test_log_dir, "showing_setup.txt")
        with open(setup_capture_path, "w") as filehandle:
            filehandle.writelines("\n".join(self._pane.capture_pane()))

        # wait for the prompt
        prompt_showing = True
        while not prompt_showing:
            prompt_showing = self._pane.capture_pane()[0] == self._cli_prompt

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._server.has_session(self._session_name):
            self._session.kill_session()

    def interaction(
        self,
        value,
        wait_on_help=True,
        wait_on_playbook_status=False,
        wait_on_collection_fetch_prompt=None,
        wait_on_cli_prompt=False,
        timeout=60,
    ):
        """interact with the tmux session"""
        start_time = timer()
        self._pane.send_keys(value, suppress_history=False)
        ok_to_return = [False]
        while not all(ok_to_return):
            ok_to_return = []
            showing = []
            while not showing:
                time.sleep(0.1)
                showing = self._pane.capture_pane()
                elapsed = timer() - start_time
                if elapsed > timeout:
                    timeout_capture_path = os.path.join(self._test_log_dir, "showing_timeout.txt")
                    with open(timeout_capture_path, "w") as filehandle:
                        filehandle.writelines("\n".join(showing))
                    return showing
            if wait_on_cli_prompt:
                # handle command sent but pane not updated
                if len(showing) > 1:
                    ok_to_return.append(self._cli_prompt in showing[-1])
                else:
                    ok_to_return.append(False)
            else:
                if wait_on_help:
                    ok_to_return.append(any(":help help" in line for line in showing))
                if wait_on_playbook_status:
                    ok_to_return.append(showing[-1].endswith(wait_on_playbook_status))
                if wait_on_collection_fetch_prompt:
                    ok_to_return.append(wait_on_collection_fetch_prompt not in showing[0])
        return showing

    def _get_cli_prompt(self):
        """get cli prompt"""
        self._pane.send_keys("clear")
        showing = []
        while len(showing) != 1:
            showing = self._pane.capture_pane()
            time.sleep(0.1)

        return showing[0]


def update_fixtures(request, index, received_output, comment, testname=None):
    """Used by action plugins to generate the fixtures"""
    dir_path, file_name = fixture_path_from_request(request, index, testname=testname)
    os.makedirs(dir_path, exist_ok=True)
    fixture = {
        "name": request.node.name,
        "index": index,
        "comment": comment,
        "output": received_output,
    }
    with open(f"{dir_path}/{file_name}", "w", encoding="utf8") as outfile:
        json.dump(fixture, outfile, indent=4, ensure_ascii=False, sort_keys=False)


def fixture_path_from_request(request, index, testname=None):
    """build a dir and file path for a test"""
    path_in_fixture_dir = request.node.nodeid.split("::")[0].lstrip("tests/")
    dir_path = os.path.join(defaults.FIXTURES_DIR, path_in_fixture_dir, request.node.originalname)
    if testname:
        dir_path = os.path.join(dir_path, testname)

    file_name = f"{index}.json"
    return dir_path, file_name


def container_runtime_or_fail():
    """find a container runtime, prefer podman
    fail if neither available"""
    # pylint: disable=import-outside-toplevel
    import subprocess

    for runtime in ("podman", "docker"):
        try:
            subprocess.run([runtime, "-v"], check=False)
            return runtime
        except FileNotFoundError:
            pass
    raise Exception("container runtime required")


class Cli2Runner:
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=too-many-arguments
    # pylint: disable=unused-argument
    """A base class which mocks the runner calls"""

    INTERACTIVE = {
        "config": "override in subclass",
        "inventory": "override in subclass",
        "run": "override in subclass",
    }

    STDOUT = {
        "config": "override in subclass",
        "inventory": "override in subclass",
        "run": "override in subclass",
    }

    def run_test(self, mocked_runner, cli_entry, config_fixture, expected):
        # pylint: disable=no-self-use
        """the func to run the test and assert"""
        raise Exception("Override in subclass")

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.cli_entry = "ansible-navigator {0} {1} -m {2} --ce " + container_runtime_or_fail()

    @mock.patch("ansible_navigator.runner.api.get_ansible_config")
    def test_config_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["config"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command")
    def test_config_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["config"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.get_inventory")
    def test_inventory_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["inventory"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command")
    def test_inventory_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["inventory"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command_async")
    def test_run_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["run"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command_async")
    def test_run_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["run"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)
