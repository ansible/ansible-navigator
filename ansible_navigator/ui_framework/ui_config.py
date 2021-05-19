from typing import NamedTuple


class UIConfig(NamedTuple):
    """
    Used to determine properties about rendering things. An instance of this
    class gets threaded throughout most of the UI system, so it can be used for
    fairly global things, such as "should we render color, ever?"
    """

    color: bool = True
    osc4: bool = True
