""" :write """
import json
import logging
import os
import re

from . import _actions as actions
from ..app_public import AppPublic
from ..ui_framework import Interaction

from ..utils import remove_dbl_un

from ..yaml import human_dump


@actions.register
class Action:
    """:write"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^w(?:rite)?(?P<force>!)?\s+(?P<append>>>)?\s*(?P<filename>.+)$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :write

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        # pylint: disable=too-many-branches
        self._logger.debug("write requested as %s", interaction.action.value)
        match = interaction.action.match.groupdict()
        filename = os.path.abspath(match["filename"])
        if match["append"]:
            if not os.path.exists(filename) and not match["force"]:
                self._logger.warning(
                    "Append operation failed because %s does not exist, force with !", filename
                )
                return None
            fmode = "a"
        else:
            if os.path.exists(filename) and not match["force"]:
                self._logger.warning(
                    "Write operation failed because %s exists, force with !", filename
                )
                return None
            fmode = "w"

        if interaction.content:
            obj = interaction.content.showing
        elif interaction.menu:
            obj = [
                {remove_dbl_un(k): v for k, v in c.items() if k in interaction.menu.columns}
                for c in interaction.menu.current
            ]
            if interaction.ui.menu_filter():
                obj = [
                    e
                    for e in obj
                    if interaction.ui.menu_filter().search(" ".join(str(v) for v in e.values()))
                ]

        if isinstance(obj, str):
            write_as = "text"
        else:
            if re.match(r"^.*\.y(?:a)?ml$", filename):
                write_as = "yaml"
            elif filename.endswith(".json"):
                write_as = "json"
            else:
                write_as = interaction.ui.xform()

        if write_as == "text":
            with open(os.path.abspath(filename), fmode) as outfile:
                outfile.write(obj)
        elif write_as == "yaml":
            human_dump(obj=obj, filename=filename, fmode=fmode)
        elif write_as == "json":
            with open(os.path.abspath(filename), fmode) as outfile:
                json.dump(obj, outfile, indent=4, sort_keys=True)

        self._logger.info("Wrote to '%s' with mode '%s' as '%s'", filename, fmode, write_as)
        return None
