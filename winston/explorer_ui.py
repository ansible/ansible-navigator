""" the explorer ui class
"""
import curses
import re
from typing import Any
from typing import Union
from .ui import UserInterface
from .ui import CursesLines
from .ui import CursesLinePart

RESULT_TO_COLOR = [
    ("(?i)^failed$", 9),
    ("(?i)^ok$", 10),
    ("(?i)^ignored$", 13),
    ("(?i)^skipped$", 14),
    ("(?i)^in progress$", 8),
    ("(?i)^title$", 9),
    ("(?i)^date$", 11),
    ("(?i)^category$", 14),
]

get_color = lambda word: next((x[1] for x in RESULT_TO_COLOR if re.match(x[0], word)), None)


class ExplorerUi(UserInterface):
    # pylint: disable=too-few-public-methods
    """wrap the ui and set app specific keys"""

    @staticmethod
    def _filter_keys(obj):
        return {k: v for k, v in obj.items() if not (k.startswith("_") or k.endswith("uuid"))}

    @staticmethod
    def _custom_color(colname, entry):
        # pylint: disable=too-many-branches
        """Find matching color for word

        :param word: A word to match
        :type word: str(able)
        """

        colval = entry[colname]
        color = None
        if "play name" in entry:
            if not colval:
                color = 8
            elif colname in ["% completed", "task count", "play name"]:
                failures = entry["failed"] + entry["unreachable"]
                if failures:
                    color = 9
                elif entry["ok"]:
                    color = 10
                else:
                    color = 8
            elif colname == "changed":
                color = 11
            else:
                color = get_color(colname)

        elif "task" in entry:
            if entry["result"].lower() == "in progress":
                color = get_color(entry["result"])
            elif colname in ["result", "host", "number", "task", "task action"]:
                color = get_color(entry["result"])
            elif colname == "changed":
                if colval:
                    color = 11
                else:
                    color = 8
            elif colname == "duration":
                color = 12

        # blog page
        elif set((k.lower() for k in entry.keys())) == set(("title", "date", "category", "link")):
            color = get_color(colname)

        return color

    def _custom_heading(self, obj: Any) -> Union[CursesLines, None]:
        if isinstance(obj, dict) and "task" in obj:
            heading = []
            detail = "PLAY [{play}:{tnum}] ".format(play=obj["play"], tnum=obj["number"])
            stars = "*" * (self._screen_w - len(detail))
            heading.append(
                tuple(
                    [
                        CursesLinePart(
                            column=0,
                            string=detail + stars,
                            color=curses.color_pair(0),
                            decoration=0,
                        )
                    ]
                )
            )

            detail = "TASK [{task}] ".format(task=obj["task"])
            stars = "*" * (self._screen_w - len(detail))
            heading.append(
                tuple(
                    [
                        CursesLinePart(
                            column=0,
                            string=detail + stars,
                            color=curses.color_pair(0),
                            decoration=0,
                        )
                    ]
                )
            )

            if obj["changed"] is True:
                color = 11
                res = "CHANGED"
            else:
                color = next((x[1] for x in RESULT_TO_COLOR if re.match(x[0], obj["result"])), 0)
                res = obj["result"]

            if "res" in obj and "msg" in obj["res"]:
                msg = str(obj["res"]["msg"]).replace("\n", " ").replace("\r", "")
            else:
                msg = ""

            string = "{res}: [{host}] {msg}".format(res=res, host=obj["host"], msg=msg)
            string = string + (" " * (self._screen_w - len(string) + 1))
            heading.append(
                tuple(
                    [
                        CursesLinePart(
                            column=0,
                            string=string,
                            color=curses.color_pair(color),
                            decoration=curses.A_UNDERLINE,
                        )
                    ]
                )
            )
            return tuple(heading)
        return None
