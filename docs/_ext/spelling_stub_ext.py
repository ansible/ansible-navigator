"""Sphinx extension for making the spelling directive noop."""

from typing import List

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nodes


class SpellingNoOpDirective(SphinxDirective):
    """Definition of the stub spelling directive."""

    has_content = True

    def run(self) -> List[nodes.Node]:
        """Generate nothing in place of the directive."""
        return []


def setup(app: Sphinx) -> None:
    """Initialize the extension."""
    app.add_directive("spelling", SpellingNoOpDirective)

    return {
        "parallel_read_safe": True,
        "version": "builtin",
    }
