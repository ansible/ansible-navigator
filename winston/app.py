""" simple base class for apps
"""
import logging

from typing import Tuple
from typing import Union

import winston.actions as actions

from .steps import Steps
from .ui import Action


class App:
    # pylint: disable=too-few-public-methods
    """simple base class for apps"""

    def __init__(self, args=None):
        self.actions: type.ModuleType = actions
        self.args = args
        self.name = "app_base_class"
        self.stdout = []
        self.steps = Steps()
        self._logger = logging.getLogger(__name__)

    def _action_match(self, entry: str) -> Union[Tuple[str, Action], Tuple[None, None]]:
        """attempt to match the user input against the regexes
        provided by each action

        :param entry: the user input
        :type entry: str
        :return: The name and matching action or not
        :rtype: str, Action or None, None
        """
        for kegex in self.actions.kegexes():
            if match := kegex.kegex.match(entry):
                return kegex.name, Action(match=match, value=entry)
        return None, None

    def update(self) -> None:
        """update, define in child if necessary"""

    def rerun(self) -> None:
        """per app rerun if needed"""

    def write_artifact(self, filename: str) -> None:
        """per app write_artifact
        likely player only"""
