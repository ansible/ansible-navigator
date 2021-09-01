""" obj to hold basic ui settings """
from types import SimpleNamespace


class UIConfig(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """
    Used to determine properties about rendering things. An instance of this
    class gets threaded throughout most of the UI system, so it can be used for
    fairly global things, such as "should we render color, ever?"

    :param color: Is coloring enabled?
    :param colors_initialized: Have curses colors been initialized?
    :param grammars_dir: The path to the grammar directory
    :param osc4: Terminal support for OSC4
    :param terminal_color_path: Path to the 16 color map
    :param theme_path: Path to the theme colors
    """

    color: bool
    colors_initialized: bool
    grammars_dir: str
    osc4: bool
    terminal_colors_path: str
    theme_path: str
