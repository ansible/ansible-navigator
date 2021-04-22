""" simple base class for apps
"""
import logging
from argparse import Namespace
from typing import List
from typing import Tuple
from typing import Union

from ansible_navigator.actions import kegexes

from .app_public import AppPublic

from .steps import Steps

from .utils import check_for_ansible
from .utils import set_ansible_envar

from .ui_framework.ui import Action


class App:
    # pylint: disable=too-few-public-methods
    """simple base class for apps"""

    def __init__(self, args: Namespace):

        # allow args to be set after __init__
        self.args: Namespace = args
        self._calling_app: AppPublic
        self.name = "app_base_class"
        self._parser_error: str = ""
        self.stdout: List = []
        self.steps = Steps()
        self._logger = logging.getLogger(__name__)

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
        if self.args:
            return AppPublic(
                args=self.args,
                name=self.name,
                rerun=self.rerun,
                stdout=self.stdout,
                steps=self.steps,
                update=self.update,
                write_artifact=self.write_artifact,
            )
        raise AttributeError("app passed without args initialized")

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

    def _update_args(self, params: List) -> Union[Namespace, None]:
        """pass the params through the original cli parser
        as if run was invoked from the command line
        provide an error callback so the app doesn't sys.exit if the parsing fails
        """

        try:
            msgs, new_args = self._calling_app.args.parse_and_update(
                params=params, error_cb=self.parser_error
            )
        except TypeError:
            self._logger.error("While attempting to parse %s:", " ".join(params))
            self._logger.error(self._parser_error)
            return None

        for msg in msgs:
            self._logger.debug(msg)

        if not hasattr(new_args, "requires_ansible") or new_args.requires_ansible:
            if not new_args.execution_environment:
                success, msg = check_for_ansible()
                if success:
                    self._logger.debug(msg)
                else:
                    self._logger.critical(msg)
                    return None
            set_ansible_envar()
        return new_args

    def write_artifact(self, filename: str) -> None:
        """per app write_artifact
        likely player only"""
