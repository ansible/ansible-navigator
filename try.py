import curses

from ansible_navigator.ui_framework import CursesLinePart

string = "string"
color = 5

one = tuple(
            [
                CursesLinePart(
                    column=0,
                    string=string,
                    color=color,
                    decoration=curses.A_UNDERLINE,
                ),
            ],
        )

two = (
            CursesLinePart(
                column=0,
                string=string,
                color=color,
                decoration=curses.A_UNDERLINE,
            ),
        )

pass