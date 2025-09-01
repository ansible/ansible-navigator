"""Object to hold basic UI settings."""

from dataclasses import dataclass

from ansible_navigator.utils.compatibility import Traversable


@dataclass
class UIConfig:
    """The UI configuration.

    Args:
        color: Enable the use of color for mode interactive and stdout
        colors_initialized: Whether colors have been initialized
        cursor_navigation: Enable arrow-key cursor navigation and Enter selection in menus
        grammar_dir: The path to the grammar directory
        osc4: Enable or disable terminal color changing support with OSC 4
        terminal_colors_path: The path to the terminal colors file
        theme_path: The path to the theme file
    """

    #: Enable the use of color for mode interactive and stdout
    color: bool
    #: Whether colors have been initialized
    colors_initialized: bool
    #: The path to the grammar directory
    grammar_dir: Traversable
    #: Enable or disable terminal color changing support with OSC 4
    osc4: bool
    #: The path to the terminal colors file
    terminal_colors_path: Traversable
    #: The path to the theme file
    theme_path: Traversable
    #: Enable arrow-key cursor navigation and Enter selection in menus
    cursor_navigation: bool = False
