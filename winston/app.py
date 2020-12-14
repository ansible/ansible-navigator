""" simple base class for apps
"""
import logging

import winston.actions as actions

from .steps import Steps


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

    def update(self) -> None:
        """update, define in child if necessary"""

    def rerun(self) -> None:
        """per app rerun if needed"""

    def write_artifact(self, filename: str) -> None:
        """per app write_artifact
        likely player only"""
