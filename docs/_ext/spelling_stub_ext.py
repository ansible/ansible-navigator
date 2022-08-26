# fmt: off
"""Sphinx extension for making the spelling directive noop."""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Union

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nodes


class SpellingNoOpDirective(SphinxDirective):
    """Definition of the stub spelling directive."""

    has_content = True

    def run(self) -> list[nodes.Node]:
        """Generate nothing in place of the directive.

        :returns: An empty list rather than a typical list of Docutils/Sphinx nodes
        """
        return []


def setup(app: Sphinx) -> dict[str, bool | str]:
    """Initialize the extension.

    :param app: An instance of sphinx
    :return: The extension metadata
    """
    app.add_directive("spelling", SpellingNoOpDirective)

    return {
        "parallel_read_safe": True,
        "version": "builtin",
    }
