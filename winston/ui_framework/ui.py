""" the main ui renderer
"""

# pylint: disable=too-many-lines
import curses
import json
import logging

import os
import re

from curses import ascii as curses_ascii

from functools import lru_cache
from math import ceil, floor
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Match
from typing import NamedTuple
from typing import Pattern
from typing import Tuple
from typing import Union
from winston.ui_framework.field_text import FieldText

from .colorize import Colorize
from .colorize import rgb_to_ansi  # , hex_to_rgb_curses


from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines

from .curses_window import CursesWindow
from .curses_window import Window

from .form import Form

from .field_text import FieldText
from .form_handler_text import FormHandlerText

from ..utils import convert_percentages, distribute
from ..yaml import yaml, Dumper


STND_KEYS = {
    "^f/PgUp": "page up",
    "^b/PgDn": "page down",
    "\u2191\u2193": "scroll",
    "esc": "back",
}
END_KEYS = {
    ":help": "help",
}


class Action(NamedTuple):
    """the user's input"""

    value: Union[str, int]
    match: Match


class Content(NamedTuple):
    """what's on the screen, when showing content"""

    showing: Any


class Menu(NamedTuple):
    """details about the currently showing menu"""

    current: List
    columns: List


class Ui(NamedTuple):
    """select functions that can be called from an action"""

    menu_filter: Callable
    scroll: Callable
    show: Callable
    update_status: Callable
    xform: Callable


class Interaction(NamedTuple):
    """wrapper for what is sent bak to the calling app"""

    name: str
    action: Action
    ui: Ui
    content: Union[Content, None] = None
    menu: Union[Menu, None] = None


class MenuItem(NamedTuple):
    """One menu item"""

    obj: Dict
    line: CursesLine


MenuItems = Tuple[MenuItem, ...]


class UserInterface(CursesWindow):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    """The main UI class"""

    def __init__(
        self,
        screen_miny: int,
        no_osc4: bool,
        kegexes: Callable[..., Any],
        refresh: int,
        share_dir: str,
        pbar_width: int = 11,
    ) -> None:
        """init

        :param screen_miny: The minimum screen height
        :type screen_miny: int
        :param pbar_width: The width of the progress bar
        :type pbar_width: int
        :param words_to_color: Words that get colored (regex, color_int)
        :type words_to_color: list
        :param no_osc4: enable/disable osc4 terminal color change support
        :type no_osc4: str (enabled/disabled)
        """
        super().__init__()
        self._color_menu_item: Callable[[int, str, Dict[str, Any]], int]
        self._colorizer = Colorize(share_dir=share_dir)
        self._content_heading: Callable[[Any, int], Union[CursesLines, None]]
        self._default_colors = None
        self._default_pairs = None
        self._default_obj_serialization = "source.yaml"
        self._filter_content_keys: Callable[[Dict[Any, Any]], Dict[Any, Any]]
        self._hide_keys = True
        self._kegexes = kegexes
        self._logger = logging.getLogger(__name__)
        self._menu_filter: Union[Pattern, None] = None
        self._menu_indicies: Tuple[int, ...] = tuple()
        self._no_osc4 = no_osc4

        self._pbar_width = pbar_width
        self._prefix_color = 8
        self._refresh = [refresh]
        self._rgb_to_curses_color_idx: Dict[str, int] = {}
        self._screen_miny = screen_miny
        self._scroll = 0
        self._theme_dir = os.path.join(share_dir, "themes")
        self._xform = self._default_obj_serialization
        self._status = ""
        self._status_color = 0

        curses.curs_set(0)
        self._set_colors()
        self._screen: Window = curses.initscr()
        self._screen.timeout(refresh)
        self._one_line_input = FormHandlerText(screen=self._screen)

    def disable_refresh(self) -> None:
        """Disable the screen refresh"""
        self._refresh.append(self._refresh[-1])
        self._refresh.append(-1)
        self._screen.timeout(-1)

    def restore_refresh(self) -> None:
        """Restore the screen refresh
        to the previous value
        """
        self._refresh.pop()
        self._screen.timeout(self._refresh.pop())

    def update_status(self, status: str = "", status_color: int = 0) -> None:
        """update the status"""
        self._status = status
        self._status_color = status_color

    def menu_filter(self, value: Union[str, None] = "") -> object:
        """Set or return the menu filter

        :param args[0]: None or the menu_filter to set
        :type args[0]: None or str(regex)
        :return: the current menu filter
        :rtype: None or Pattern
        """
        if value != "":
            if value is None:
                self._menu_filter = None
            else:
                try:
                    self._menu_filter = re.compile(value)
                except re.error as exc:
                    self._menu_filter = None
                    self._logger.error("Regex for menu filter was invalid: %s", value)
                    self._logger.exception(exc)
        return self._menu_filter

    def scroll(self, value: Union[int, None] = None) -> int:
        """Set or return the current scroll

        :param value: the value to set the scroll to
        :type value: int
        :return: the current scroll
        :rtype: int
        """
        if value is not None:
            if not isinstance(value, int):
                raise TypeError
            self._scroll = value
        return self._scroll

    def xform(self, value: Union[str, None] = None, default: bool = False) -> str:
        """Set or return the current xform

        :param value: the value to set the xform to
        :type value: str or None
        :return: the current xform
        :rtype: str
        """
        if value is not None:
            self._xform = value
            if default:
                self._default_obj_serialization = value
        return self._xform

    @property
    def _ui(self) -> Ui:
        """Limit the callables the actions can access

        :return: A tuple of avialble functions
        :rtype: Ui
        """
        res = Ui(
            menu_filter=self.menu_filter,
            scroll=self.scroll,
            show=self.show,
            update_status=self.update_status,
            xform=self.xform,
        )
        return res

    def _footer(self, key_dict: dict) -> CursesLine:
        """build a footer from the key dict
        spread the columns out evenly

        :param key_dict: the keys and their description
        :type key_dict: dict
        :return: The footer line
        :rtype: CursesLine
        """
        colws = [len("{k}: {v}".format(k=str(k), v=str(v))) for k, v in key_dict.items()]
        if self._status:
            status_width = self._pbar_width
        else:
            status_width = 0
        gap = floor((self._screen_w - status_width - sum(colws)) / len(key_dict))
        adj_colws = [c + gap for c in colws]
        col_starts = [0]
        for idx, colw in enumerate(adj_colws):
            col_starts.append(colw + col_starts[idx])
        footer = []
        for idx, key in enumerate(key_dict):
            left = key[0 : adj_colws[idx]]
            right = " {v}".format(v=key_dict[key])
            right = right[0 : adj_colws[idx] - len(key)]
            footer.append(
                CursesLinePart(
                    column=col_starts[idx],
                    string=left,
                    color=curses.color_pair(0),
                    decoration=curses.A_REVERSE,
                )
            )
            footer.append(
                CursesLinePart(
                    column=col_starts[idx] + len(left),
                    string=right,
                    color=curses.color_pair(0),
                    decoration=0,
                )
            )
        if self._status:
            footer.append(
                CursesLinePart(
                    column=self._screen_w - self._pbar_width,
                    string=self._status[0 : self._pbar_width + 1].upper().center(self._pbar_width),
                    color=curses.color_pair(self._status_color % self._number_colors),
                    decoration=curses.A_REVERSE,
                )
            )
        return tuple(footer)

    def _scroll_bar(
        self, max_lines: int, len_heading: int, len_lines: int, body_start: int, body_stop: int
    ) -> None:
        """Add a scroll bar if the lines > viewport

        :param footer_height: The height of the footer
        :type footer_height: int
        :param_len_heading: the height of the heading
        :type len_heading: int
        :param len_lines: the number of lines in the content
        :type len_lines: int
        :param body_start: where we are in the body
        :type body_start: int
        :param body_stop: the end of the body
        :type body_stop: int
        """
        if len_lines:
            if len_lines > max_lines:
                start_scroll_bar = body_start / len_lines * max_lines
                stop_scroll_bar = body_stop / len_lines * max_lines
                len_scroll_bar = ceil(stop_scroll_bar - start_scroll_bar)
                color = curses.color_pair(self._prefix_color % self._number_colors)
                for idx in range(int(start_scroll_bar), int(start_scroll_bar + len_scroll_bar)):
                    lineno = idx + len_heading
                    line_part = CursesLinePart(
                        column=self._screen_w - 1,
                        string="\u2592",
                        color=color,
                        decoration=0,
                    )
                    self._add_line(
                        window=self._screen,
                        lineno=min(lineno, max_lines + len_heading),
                        line=tuple([line_part]),
                    )

    def _get_input_line(self) -> str:
        """get one line of input from the user

        :return: the lines
        :rtype: str
        """
        self.disable_refresh()
        form_field = FieldText(name="one_line", prompt="")
        clp = CursesLinePart(column=0, string=":", color=curses.color_pair(0), decoration=0)
        self._add_line(window=self._screen, lineno=self._screen_h, line=tuple([clp]))
        self._screen.refresh()
        self._one_line_input.win = curses.newwin(1, self._screen_w, self._screen_h, 1)
        self._one_line_input.win.keypad(True)
        while True:
            user_input, char = self._one_line_input.handle(0, [form_field])
            if char == curses_ascii.ESC:
                break
            if char in (curses.KEY_ENTER, 10, 13):
                break
            if char == curses.KEY_RESIZE:
                break
        self.restore_refresh()
        curses.curs_set(0)
        return user_input

    def _display(
        self,
        lines: CursesLines,
        heading: Union[CursesLines, None],
        indent_heading: int,
        key_dict: dict,
        await_input: bool,
    ) -> str:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        """show something on the screen

        :param lines: The lines to show
        :type lines: CursesLines
        :param heading: the headers to show
        :type heading: CursesLines or None
        :param key_dict: any suplimental key to show
        :type key_dict: dict
        :param await_input: Should we wait for a key
        :type await_input: bool
        :return: the key pressed
        :rtype: str
        """
        display_heading = heading or ()
        footer = self._footer(dict(**STND_KEYS, **key_dict, **END_KEYS))

        max_lines = self._screen_h - len(display_heading)
        self.scroll(max(self.scroll(), max_lines))

        index_width = len(str(len(lines)))
        keypad = set(str(x) for x in range(0, 10))
        other_valid_keys = ["+", "-", "_", "KEY_F(5)", "^[", "\x1b"]
        while True:
            self._screen.erase()
            prefix = " " * (index_width + len("|")) if indent_heading else None
            for idx, line in enumerate(display_heading):
                self._add_line(window=self._screen, lineno=idx, line=line, prefix=prefix)
            self._add_line(window=self._screen, lineno=self._screen_h, line=footer)

            body_start = self.scroll() - max_lines
            body_stop = self.scroll()
            for idx, line in enumerate(lines[body_start:body_stop]):
                line_index = body_start + idx
                prefix = "{idx}\u2502".format(idx=str(line_index).rjust(index_width))
                self._add_line(
                    window=self._screen, lineno=idx + len(display_heading), line=line, prefix=prefix
                )

            self._scroll_bar(
                max_lines=max_lines,
                len_heading=len(display_heading),
                len_lines=len(lines),
                body_start=body_start,
                body_stop=body_stop,
            )

            self._screen.refresh()

            if await_input:
                char = self._screen.getch()
                key = "KEY_F(5)" if char == -1 else curses.keyname(char).decode()
            else:
                key = "KEY_F(5)"

            if key == "KEY_RESIZE":
                self.scroll(min(body_start + self._screen_h - len(display_heading), len(lines)))
                return key

            if key in keypad or key in other_valid_keys:
                return key

            if key == ":":
                colon_entry = self._get_input_line()
                if colon_entry is None:
                    continue
                return colon_entry

            if key == "KEY_DOWN":
                self.scroll(max(min(self.scroll() + 1, len(lines)), max_lines))
            elif key == "KEY_UP":
                self.scroll(max(self.scroll() - 1, max_lines))
            elif key in ["^F", "KEY_NPAGE"]:
                self.scroll(max(min(self.scroll() + max_lines, len(lines)), max_lines))
            elif key in ["^B", "KEY_PPAGE"]:
                self.scroll(max(self.scroll() - max_lines, max_lines))

    def _menu(self, dicts: List, cols: List) -> Tuple[CursesLines, CursesLines]:
        """Build a text menu from a list of dicts given columns(root keys)

        :param dicts: A list of dicts
        :type dicts: list
        :param cols: The columns (keys) to use in the dicts
        :type cols: list of strings
        :return: the heading and body of the menu
        :rtype: (CursesLines, CursesLines)
        """
        line_prefix_w = len(str(len(dicts))) + len("|")
        dicts = convert_percentages(dicts, cols, self._pbar_width)
        lines = [[str(d.get(c)) for c in cols] for d in dicts]
        colws = [
            max([len(str(v)) for v in c])
            for c in zip(*lines + [[re.sub("^__", "", col) for col in cols]])
        ]
        # add a space
        colws = [c + 1 for c in colws]

        available = self._screen_w - line_prefix_w - 1  # scrollbar width
        adj_colws = distribute(available, colws)

        col_starts = [0]
        for idx, colw in enumerate(adj_colws):
            col_starts.append(colw + col_starts[idx])

        menu_layout = tuple([col_starts, cols, adj_colws])
        header = self._menu_header_line(menu_layout)

        menu_layout = tuple([col_starts, cols, adj_colws, header])
        curses_lines = self._menu_lines(dicts, menu_layout)

        return tuple([header]), curses_lines

    def _menu_header_line(self, menu_layout: Tuple[List, ...]) -> CursesLine:
        """Generate the menu header line

        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :return: the menu head line
        :type: CursesLine
        """
        _col_starts, cols, _adj_colws = menu_layout
        return tuple(self._menu_header_line_part(colno, menu_layout) for colno in range(len(cols)))

    @staticmethod
    def _menu_header_line_part(colno: int, menu_layout: Tuple[List, ...]) -> CursesLinePart:
        """Generate one part of the menu header line

        :param colno: The column number
        :type colno: int
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :return: the menu head line
        :type: CursesLinePart
        """
        col_starts, cols, adj_colws = menu_layout
        coltext = re.sub("^__", "", cols[colno])
        coltext = re.sub("_", " ", coltext)
        adj_entry = coltext[0 : adj_colws[colno]].upper()
        # right justifyheader if %
        if coltext.startswith("% "):
            return CursesLinePart(
                column=col_starts[colno] + adj_colws[colno] - len(adj_entry),
                string=adj_entry,
                color=curses.color_pair(0),
                decoration=curses.A_UNDERLINE,
            )
        return CursesLinePart(
            column=col_starts[colno], string=adj_entry, color=0, decoration=curses.A_UNDERLINE
        )

    def _menu_lines(self, dicts: List[Dict], menu_layout: Tuple[List, ...]) -> CursesLines:
        """Generate all the menu lines

        :params dicts: A list of dicts from which the menu will be generated
        :type dicts: List of Dicts
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :param menu_layout[3]: the menu header, used to determine justification
        :type memu_layout[3]: CursesLine
        :return: the menu lines
        :type: CursesLines
        """
        return tuple(self._menu_line(dyct, menu_layout) for dyct in dicts)

    def _menu_line(self, dyct: dict, menu_layout: Tuple[List, ...]) -> CursesLine:
        """Generate one the menu line

        :param dyct: One dict from which the menu line will be generated
        :type dyct: dict
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :param menu_layout[3]: the menu header, used to determine justification
        :type memu_layout[3]: CursesLine
        :return: a menu line
        :type: CursesLine
        """
        _col_starts, cols, _adj_colws, _header = menu_layout
        menu_line = (dyct.get(c) for c in cols)
        return tuple(
            self._menu_line_part(colno, coltext, dyct, menu_layout)
            for colno, coltext in enumerate(menu_line)
        )

    def _menu_line_part(
        self,
        colno: int,
        coltext: Any,
        dyct: dict,
        menu_layout: Tuple[List, ...],
    ) -> CursesLinePart:
        """Generate one menu line part

        :param colno: The column number of the line part
        :type colno: int
        :param coltext: The text to be placed at the given column
        :type: coltext: str
        :param dyct: the dict from which the menu line will be generated
        :type dyct: dict
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :param menu_layout[3]: the menu header, used to determine justification
        :type memu_layout[3]: CursesLine
        :return: a menu line part
        :type: CursesLinePart
        """
        col_starts, cols, adj_colws, header = menu_layout

        color = self._color_menu_item(colno, cols[colno], dyct)
        color = curses.color_pair(color % self._number_colors)

        text = str(coltext)[0 : adj_colws[colno]]
        if isinstance(coltext, (int, bool, float)) or cols[colno].lower() == "__duration":
            # right jusitfy on header if int, bool, float or "duration"
            print_at = col_starts[colno] + len(header[colno][1]) - len(text)
        elif re.match(r"^[\s0-9]{3}%\s[\u2587|\s]", str(coltext)):
            # right justify in column if %
            print_at = col_starts[colno] + adj_colws[colno] - len(text)
        else:
            # left justify
            print_at = col_starts[colno]
        return CursesLinePart(column=print_at, string=str(text), color=color, decoration=0)

    def _action_match(self, entry: str) -> Union[Tuple[str, Action], Tuple[None, None]]:
        """attempt to match the user input against the regexes
        provided by each action

        :param entry: the user input
        :type entry: str
        :return: The name and matching action or not
        :rtype: str, Action or None, None
        """
        for kegex in self._kegexes():
            if match := kegex.kegex.match(entry):
                return kegex.name, Action(match=match, value=entry)
        return None, None

    def _serialize_color(self, obj: Any) -> CursesLines:
        """Serialize, if neccesary and color an obj

        :param obj: the object to color
        :type obj: Any
        :return: The generated lines
        :rtype: CursesLines
        """
        if self.xform() == "source.ansi":
            return self._colorizer.render(doc=obj, scope=self.xform())
        if self.xform() == "source.yaml":
            string = yaml.dump(
                obj, default_flow_style=False, Dumper=Dumper, explicit_start=True, sort_keys=True
            )
        elif self.xform() == "source.json":
            string = json.dumps(obj, indent=4, sort_keys=True)
        else:
            string = obj
        colorized = self._colorizer.render(doc=string, scope=self.xform())
        lines = self._color_lines_for_term(colorized)
        return lines

    def _color_lines_for_term(self, lines: List) -> CursesLines:
        """Give a list of dicts from tokenized lines
        transform them into lines for curses
        add colors as needed, maintain a mapping of rgb colors
        to curses colors in self._rgb_to_curses_color_idx

        :params lines: the lines to transform
        :type lines: list of lists of dicts
            Lines[LinePart[{"color": rgb, "chars": text, "column": n},...]]
        :return: the lines ready for curses
        :type: CursesLines
        """
        if self._custom_colors_enabled:
            unique_colors = list(
                set(chars["color"] for line in lines for chars in line if chars["color"])
            )
            # start custom colors at 16
            for color in unique_colors:
                scale = 1000 / 255
                red, green, blue = color
                if color not in self._rgb_to_curses_color_idx:
                    if not self._rgb_to_curses_color_idx:
                        curses_colors_idx = 16
                    else:
                        curses_colors_idx = max(self._rgb_to_curses_color_idx.values()) + 1

                    self._rgb_to_curses_color_idx[color] = curses_colors_idx
                    curses.init_color(
                        curses_colors_idx, int(red * scale), int(green * scale), int(blue * scale)
                    )
                    self._logger.debug(
                        "Added color: %s:%s",
                        curses_colors_idx,
                        curses.color_content(curses_colors_idx),
                    )
                    curses.init_pair(curses_colors_idx, curses_colors_idx, -1)
        colored_lines = self._colored_lines(lines)
        return colored_lines

    def _colored_lines(self, lines: List[List[Dict]]) -> CursesLines:
        """color each of the lines

        :params lines: the lines to transform
        :type lines: list of lists of dicts
            Lines[LinePart[{"color": rgb, "chars": text, "column": n},...]]
        :return: all the lines
        :rtype: CursesLines
        """
        return tuple(self._colored_line(line) for line in lines)

    def _colored_line(self, line: List[Dict]) -> CursesLine:
        """color one line

        :param line: the line to transform
        :type line: lists of dicts
            LinePart[{"color": rgb, "chars": text, "column": n},...]
        :return one colored line:
        :rtype: CursesLine
        """
        return tuple(self._colored_line_part(line_part) for line_part in line)

    def _colored_line_part(self, lp_dict: Dict) -> CursesLinePart:
        """color one linepart

        :param lp_dict: a dict describing the line part
        :type lp_dict: dict {"color": rgb, "chars": text, "column": n}
        :return: the colored line part
        :rtype: CursesLinePart
        """
        if lp_dict["color"]:
            if self._custom_colors_enabled:
                color = self._rgb_to_curses_color_idx[lp_dict["color"]]
            else:
                red, green, blue = lp_dict["color"]
                color = rgb_to_ansi(red, green, blue, self._number_colors)
        else:
            color = 0
        return CursesLinePart(
            column=lp_dict["column"],
            string=lp_dict["chars"],
            color=curses.color_pair(color),
            decoration=0,
        )

    def _filter_and_serialize(self, obj: Any) -> Tuple[Union[CursesLines, None], CursesLines]:
        """filter an obj and serialize

        :param obj: the obj to serialize
        :type obj: Any
        :return: the serialize lines ready for display
        :rtype: CursesLines
        """
        heading = self._content_heading(obj, self._screen_w)
        filtered_obj = (
            self._filter_content_keys(obj) if self._hide_keys and isinstance(obj, dict) else obj
        )
        lines = self._serialize_color(filtered_obj)
        return heading, lines

    def _show_form(self, obj: Form) -> Form:
        res = obj.present(screen=self._screen)
        return res

    def _show_obj_from_list(self, objs: List[Any], index: int, await_input: bool) -> Interaction:
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        """Show an object on the display

        :param objs: A list of one or more object
        :type objs: A list of Any
        :param await_input: Should we wait for user input before returning
        :type await_input: bool
        :return: interaction with the user
        :rtype: Interaction
        """
        heading, lines = self._filter_and_serialize(objs[index])
        while True:

            if len(objs) > 1:
                key_dict = {
                    "+": "previous",
                    "-": "next",
                    "[0-9]": "goto",
                }
            else:
                key_dict = {}

            entry = self._display(
                lines=lines,
                heading=heading,
                indent_heading=False,
                key_dict=key_dict,
                await_input=await_input,
            )
            if entry == "KEY_RESIZE":
                # only the heading knows about the screen_w and screen_h
                heading = self._content_heading(objs[index], self._screen_w)

            if entry == "_":
                self._hide_keys = not self._hide_keys
                heading, lines = self._filter_and_serialize(objs[index])

            # get the less or more, wrap, incase we jumped out of the menu indices
            elif entry == "-":
                less = list(reversed([i for i in self._menu_indicies if i - index < 0]))
                more = list(reversed([i for i in self._menu_indicies if i - index > 0]))
                if ordered_indicies := less + more:
                    index = ordered_indicies[0]
                    self.scroll(0)
                    entry = "KEY_F(5)"

            elif entry == "+":
                more = [i for i in self._menu_indicies if i - index > 0]
                less = [i for i in self._menu_indicies if i - index < 0]
                if ordered_indicies := more + less:
                    index = ordered_indicies[0]
                    self.scroll(0)
                    entry = "KEY_F(5)"

            elif entry.isnumeric():
                index = int(entry) % len(objs)
                self.scroll(0)
                entry = "KEY_F(5)"

            name, action = self._action_match(entry)
            if name and action:
                if name == "refresh":
                    action = action._replace(value=index)

                current = objs[index % len(objs)]
                filtered = (
                    self._filter_content_keys(current)
                    if self._hide_keys and isinstance(current, dict)
                    else current
                )

                content = Content(showing=filtered)
                return Interaction(name=name, action=action, content=content, ui=self._ui)

    def _obj_match_filter(self, obj: Dict, columns: List) -> bool:
        """Check a dict's columns against a regex

        :param obj: The dict to check
        :type obj: dict
        :param columns: The dicts keys to check
        :type columns: list
        :return: True if a mtch else False
        :rtype: bool
        """
        return any(
            self._search_value(self.menu_filter(), str(val))
            for key, val in obj.items()
            if key in columns
        )

    @staticmethod
    @lru_cache(maxsize=None)
    def _search_value(regex: Pattern, value: str) -> Union[Match, None]:
        """check a str against a regex
        lru_cache enabled because this is hit during resize

        :param regex: the compiled regex
        :type regex: Pattern
        :param value: the string to check
        :type value: str
        :return: the match if made
        :rtype: Match or None
        """
        return regex.search(str(value))

    def _get_heading_menu_items(
        self, current: List, columns: List
    ) -> Tuple[CursesLines, MenuItems]:
        """build the menu

        :param current: A dict
        :type current: dict
        :param columns: The keys from the dic to use as columns
        :type columns: list
        :return: The heading and menu items
        :rtype: CursesLines, MenuItems
        """
        menu_heading, lines = self._menu(current, columns)
        menu_items = tuple(MenuItem(obj=z[0], line=z[1]) for z in zip(current, lines))
        return menu_heading, menu_items

    def _show_menu(self, current: List, columns: List, await_input: bool) -> Interaction:
        """Show a menu on the screen

        :param current: A dict
        :type current: dict
        :param columns: The keys from the dic to use as columns
        :type columns: list
        :param await_input: Should we wait for user input?
        :type await_input: bool
        :return: interaction with the user
        :rtype: Interaction
        """
        menu_heading, menu_items = self._get_heading_menu_items(current, columns)
        while True:
            if self.menu_filter():
                self._menu_indicies = tuple(
                    idx
                    for idx, mi in enumerate(menu_items)
                    if self._obj_match_filter(mi.obj, columns)
                )
            else:
                self._menu_indicies = tuple(range(len(menu_items)))

            entry = self._display(
                lines=tuple(menu_items[idx].line for idx in self._menu_indicies),
                heading=menu_heading,
                indent_heading=True,
                key_dict={"[0-9]": "goto"},
                await_input=await_input,
            )

            if entry == "KEY_RESIZE":
                menu_heading, menu_items = self._get_heading_menu_items(current, columns)
                continue

            name, action = self._action_match(entry)
            if name and action:
                if name == "select":
                    if menu_items:
                        index = self._menu_indicies[int(entry) % len(self._menu_indicies)]
                        action = action._replace(value=index)
                    else:
                        continue
                clean_columns = [re.sub("^__", "", col) for col in columns]
                clean_current = [{re.sub("^__", "", k): v for k, v in me.items()} for me in current]
                menu = Menu(current=clean_current, columns=clean_columns)
                return Interaction(name=name, action=action, menu=menu, ui=self._ui)

    def show(
        self,
        obj: Union[List, Dict, str, bool, int, float],
        xform: str = "",
        index: int = None,
        columns: List = None,
        await_input: bool = True,
        filter_content_keys: Callable = lambda x: x,
        color_menu_item: Callable = lambda *args, **kwargs: 0,
        content_heading: Callable = lambda *args, **kwargs: None,
    ) -> Union[Interaction, Form]:
        """Show something on the screen

        :param obj: The inbound object
        :type obj: anything
        :param xform: Set the xform
        :type xform: str
        :param index: When obj is a list, show this entry
        :type index: int
        :param columns: When obj is a list of dicts, use these keys for menu columns
        :type columns: list
        :param wait_input: Should we wait for user input?
        :type wait_input: bool
        :return: interaction with the user
        :rtype: Interaction
        """
        self._color_menu_item = color_menu_item
        self._content_heading = content_heading
        self._filter_content_keys = filter_content_keys
        columns = columns or []
        self.xform(xform or self._default_obj_serialization)

        if isinstance(obj, Form):
            form_result = self._show_form(obj)
            return form_result

        if index is not None and isinstance(obj, list):
            result = self._show_obj_from_list(obj, index, await_input)
        elif columns and isinstance(obj, list):
            result = self._show_menu(obj, columns, await_input)
        else:
            result = self._show_obj_from_list([obj], 0, await_input)
        return result
