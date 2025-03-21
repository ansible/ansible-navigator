"""Directly run an action for testing."""

from __future__ import annotations

import os
import re
import sys
import tempfile

from copy import deepcopy
from typing import TYPE_CHECKING
from typing import Any

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentType
from ansible_navigator.steps import Steps
from ansible_navigator.ui_framework.ui import Action as Ui_action
from ansible_navigator.ui_framework.ui import Interaction
from ansible_navigator.ui_framework.ui import Ui


if TYPE_CHECKING:
    from collections.abc import Callable

    from ansible_navigator.action_defs import RunStdoutReturn
    from ansible_navigator.ui_framework.form import Form


class ActionRunTest:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    """Directly run an action."""

    def __init__(
        self,
        action_name: str,
        container_engine: str | None = None,
        container_options: list[str] | None = None,
        execution_environment: str | None = None,
        execution_environment_image: str | None = None,
        host_cwd: list[str] | None = None,
        set_environment_variable: dict[str, str] | None = None,
        pass_environment_variable: list[str] | None = None,
        private_data_dir: str | None = None,
        rotate_artifacts: int | None = None,
        timeout: int | None = None,
    ) -> None:
        """Initialize the test runner for an action.

        Args:
            action_name: The name of the action tests will be run
                against
            container_engine: The name of the container engine
            container_options: Any options being passed directly to the
                container engine
            execution_environment: A boolean indicating if an execution
                environment should be used
            execution_environment_image: The name of the execution
                environment image to be used
            host_cwd: The current working directory for the host
            set_environment_variable: Any environment variable to set in
                the execution environment
            pass_environment_variable: Any environment variables to pass
                into the execution environment
            private_data_dir: The artifact directory for ansible runner
            rotate_artifacts: The number of artifacts ansible runner
                should maintain
            timeout: The ansible runner timeout value
        """
        self._action_name = action_name
        self._container_engine = container_engine
        self._container_options = container_options
        self._execution_environment = execution_environment
        self._execution_environment_image = execution_environment_image
        self._set_environment_variable = set_environment_variable
        self._pass_environment_variable = pass_environment_variable
        self._host_cwd = host_cwd
        self._private_data_dir = private_data_dir
        self._rotate_artifacts = rotate_artifacts
        self._timeout = timeout
        self._app_args = {
            "container_engine": self._container_engine,
            "container_options": self._container_options,
            "execution_environment": self._execution_environment,
            "execution_environment_image": self._execution_environment_image,
            "set_environment_variable": self._set_environment_variable,
            "pass_environment_variable": self._pass_environment_variable,
            "ansible_runner_artifact_dir": self._private_data_dir,
            "ansible_runner_rotate_artifacts_count": self._rotate_artifacts,
            "ansible_runner_timeout": self._timeout,
        }
        self._app_action = __import__(
            f"ansible_navigator.actions.{self._action_name}",
            globals(),
            fromlist=["Action"],
        )

    def callable_pass_one_arg(self, value: int = 0) -> None:
        """Do nothing callable.

        Args:
            value: The value to return
        """

    def callable_pass(self, **kwargs: Any) -> None:
        """Do nothing callable.

        Args:
            **kwargs: The call values
        """

    def content_format(
        self,
        value: ContentFormat | None = None,
        default: bool = False,
    ) -> ContentFormat:
        """Do nothing content format callable.

        Args:
            value: The content format value
            default: A boolean indicating if the default value should be
                used

        Returns:
            The content format value
        """
        return value if value else ContentFormat.YAML

    def show(
        self,
        obj: ContentType,
        content_format: ContentFormat | None = None,
        index: int | None = None,
        columns: list[str] | None = None,
        await_input: bool = True,
        filter_content_keys: Callable[..., Any] = lambda x: x,
        color_menu_item: Callable[..., Any] = lambda *args, **kwargs: (0, 0),
        content_heading: Callable[..., Any] = lambda *args, **kwargs: None,
    ) -> None:
        """Show a content object, but don't really.

        Args:
            obj: The content object to show
            content_format: The content format to use
            index: The index of the content object
            columns: The columns to display
            await_input: A boolean indicating if input should be awaited
            filter_content_keys: A callable to filter content keys
            color_menu_item: A callable to color menu items
            content_heading: A callable to display content headings
        """

    def show_form(self, form: Form) -> Form:
        """Do nothing show form callable.

        Args:
            form: The form to show

        Returns:
            The form to show
        """
        return form

    def run_action_interactive(self) -> Any:
        """Run the action.

        The return type is set to Any here since not all actions
        have the same signature, the corresponding integration test
        will be using the action internals for asserts

        Returns:
            The action return value

        Raises:
            ValueError: If no action name match
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
            # Ignored here because it doesn't make sens to mock up a full
            # Interaction for the above show function, this returns
            # None and the ShowCallable protocol returns an Interaction
            show=self.show,  # type: ignore[arg-type]
            show_form=self.show_form,
            update_status=self.callable_pass,
            content_format=self.content_format,
        )
        match = re.match(self._app_action.Action.KEGEX, self._action_name)
        if not match:
            raise ValueError

        ui_action = Ui_action(match=match, value=self._action_name)
        interaction = Interaction(name="test", ui=user_interface, action=ui_action)

        # run the action
        action.run(interaction=interaction, app=app)

        return action

    def run_action_stdout(self, **kwargs: Any) -> tuple[RunStdoutReturn, str, str]:
        # pylint: disable=too-many-locals
        """Run the action, stdout.

        Args:
            **kwargs: The action arguments

        Returns:
            The result, stdout and stderr
        """
        self._app_args.update({"mode": "stdout"})
        self._app_args.update(kwargs)
        args = deepcopy(NavigatorConfiguration)
        for argument, value in self._app_args.items():
            args.entry(argument).value.current = value
            args.entry(argument).value.source = C.USER_CFG

        action = self._app_action.Action(args=args)

        # get a TTY, runner/docker requires it
        _parent_tty, child_tty = os.openpty()

        # preserve current ``stdin``, ``stdout``, ``stderr``
        __stdin__ = sys.stdin
        __stdout__ = sys.stdout
        __stderr__ = sys.stderr

        # ``pytest`` pseudo ``stdin`` doesn't ``fileno()``, use original
        sys.stdin = child_tty  # type: ignore[assignment]

        # set ``stderr`` and ``stdout`` to file descriptors
        with tempfile.TemporaryFile() as sys_stdout, tempfile.TemporaryFile() as sys_stderr:
            sys.stdout = sys_stdout  # type: ignore[assignment]
            sys.stderr = sys_stderr  # type: ignore[assignment]

            # run the action
            result = action.run_stdout()

            # restore ``stdin``
            sys.stdin = __stdin__

            # read and restore ``stdout``
            sys.stdout.seek(0)
            stdout = sys.stdout.read().decode()  # type: ignore[attr-defined]
            sys.stdout = __stdout__

            # read and restore ``stderr``
            sys.stderr.seek(0)
            stderr = sys.stderr.read().decode()  # type: ignore[attr-defined]
            sys.stderr = __stderr__

        return result, stdout, stderr
