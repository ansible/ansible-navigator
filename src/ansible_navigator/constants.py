"""Constants for ansible-navigator."""

from .utils.compatibility import Traversable
from .utils.compatibility import importlib_resources


PKG_NAME: str = "ansible_navigator"
DATA_DIR: Traversable = importlib_resources.files(PKG_NAME).joinpath("data")

THEME_DIR: Traversable = DATA_DIR.joinpath("themes")
THEME_NAME: str = "dark_vs.json"
THEME_PATH: Traversable = THEME_DIR.joinpath(THEME_NAME)

TERMINAL_COLORS: str = "terminal_colors.json"
TERMINAL_COLORS_PATH: Traversable = THEME_DIR.joinpath(TERMINAL_COLORS)

GRAMMAR_DIR: Traversable = DATA_DIR.joinpath("grammar")
