""" simple base class for apps
"""
import logging

from copy import deepcopy
from typing import List
from typing import Pattern
from typing import Tuple
from typing import Union

from ansible_navigator.actions import kegexes

from .app_public import AppPublic

from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import Constants as C
from .configuration_subsystem import Entry

from .initialization import parse_and_update

from .steps import Steps

from .ui_framework.ui import Action
from .ui_framework import Interaction

from .utils import LogMessage
from .utils import ExitMessage


class App:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """simple base class for apps"""

    def __init__(self, args: ApplicationConfiguration, name, logger_name=__name__):

        # allow args to be set after __init__
        self._args: ApplicationConfiguration = args
        self._calling_app: AppPublic
        self._interaction: Interaction
        self._logger = logging.getLogger(logger_name)
        self._parser_error: str = ""
        self._previous_configuration_entries: List[Entry] = deepcopy(self._args.entries)
        self._previous_scroll: int
        self._previous_filter: Union[Pattern, None]
        self._name = name
        self.stdout: List = []
        self.steps = Steps()

    @staticmethod
    def _action_match(entry: str) -> Union[Tuple[str, Action], Tuple[None, None]]:
        """attempt to match the user input against the regexes
        provided by each action

        :param entry: the user input
        :type entry: str
        :return: The name and matching action or not
        :rtype: str, Action or None, None
        """
        for kegex in kegexes():
            match = kegex.kegex.match(entry)
            if match:
                return kegex.name, Action(match=match, value=entry)
        return None, None

    @property
    def app(self) -> AppPublic:
        """this will be passed to other actions to limit the scope of
        what can be mutated internally
        """
        if self._args:
            return AppPublic(
                args=self._args,
                name=self._name,
                rerun=self.rerun,
                stdout=self.stdout,
                steps=self.steps,
                update=self.update,
                write_artifact=self.write_artifact,
            )
        raise AttributeError("app passed without args initialized")

    def _prepare_to_run(self, app: AppPublic, interaction: Interaction) -> None:
        self._calling_app = app
        self._interaction = interaction
        self._interaction.ui.scroll(0)
        self._previous_scroll = interaction.ui.scroll()
        self._previous_filter = interaction.ui.menu_filter()

    def _prepare_to_exit(self, interaction) -> None:
        """Prior to exiting an app can call this to clean up"""
        interaction.ui.scroll(self._previous_scroll)
        interaction.ui.menu_filter(self._previous_filter)
        interaction.ui.scroll(0)
        self._args.entries = self._previous_configuration_entries

    def parser_error(self, message: str) -> Tuple[None, None]:
        """callback for parser error

        :param message: A message from the parser
        :type message: str
        """
        self._parser_error = message
        return None, None

    def rerun(self) -> None:
        """per app rerun if needed"""

    def update(self) -> None:
        """update, define in child if necessary"""

    def _update_args(self, params: List, apply_previous_cli_entries: C = C.ALL) -> None:
        """pass the params through the configuration subsystem
        log messages and exit_messages as warnings since most will result in a form
        while the exit_messages would have cause a sys.exit(1) from the CLI
        each action should handle them in a manner that does not exit the TUI
        """
        messages: List[LogMessage]
        exit_messages: List[ExitMessage]

        messages, exit_messages = parse_and_update(
            params=params, args=self._args, apply_previous_cli_entries=apply_previous_cli_entries
        )

        for message in messages:
            self._logger.log(level=message.level, msg=message.message)

        for exit_msg in exit_messages:
            if exit_msg.level == logging.ERROR:
                self._logger.warning(msg=exit_msg.message)
            else:
                self._logger.log(level=exit_msg.level, msg=exit_msg.message)

    def write_artifact(self, filename: str) -> None:
        """per app write_artifact
        likely player only"""
