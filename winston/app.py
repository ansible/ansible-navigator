""" simple base class for apps
"""
import logging


class App:
    # pylint: disable=too-few-public-methods
    """simple base class for apps"""

    def __init__(self, args):
        self.args = args
        self.step = None
        self._logger = logging.getLogger(__name__)

    def update(self) -> None:
        """update, define in child if necessary"""

    def rerun(self) -> None:
        """per app rerun if needed"""
