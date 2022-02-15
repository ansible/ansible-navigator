"""Object to hold basic UI settings."""

from dataclasses import dataclass


@dataclass
class UIConfig:
    """Object to hold basic UI settings.

    Used to determine properties about rendering things. An instance of this
    class gets threaded throughout most of the UI system, so it can be used for
    fairly global things, such as "should we render color, ever?"
    """

    #: Indicates coloring is enabled or disabled
    color: bool
    #: Indicates if the curses colors have been initialized
    colors_initialized: bool
    #: The path to the grammar directory
    grammar_dir: str
    #: Indicates if terminal support for OSC4 is enabled
    osc4: bool
    #: The path to the 16 terminal color map
    terminal_colors_path: str
    #: The path to the theme file
    theme_path: str
