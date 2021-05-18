""" directly run an action for testing """
import os
import re
import sys
import tempfile

from copy import deepcopy

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.ui_framework.ui import Action as Ui_action
from ansible_navigator.ui_framework.ui import Interaction
from ansible_navigator.ui_framework.ui import Ui
from ansible_navigator.steps import Steps


class ActionRunTest:
    """directly run an action"""

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

    def run_action_stdout(self, **kwargs) -> Tuple[int, str, str]:
        """run the action"""
        self._app_args.update({"mode": "stdout"})
        self._app_args.update(kwargs)
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
        return_code = action.run_stdout()

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

        return return_code, stdout, stderr
