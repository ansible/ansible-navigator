"""tests for colorize
"""
import os

from typing import Dict
from typing import NamedTuple
from unittest.mock import patch  # pylint: disable=preferred-module  # FIXME: GH-872

from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentView
from ansible_navigator.ui_framework.colorize import Colorize
from ansible_navigator.ui_framework.curses_defs import SimpleLinePart
from ansible_navigator.utils.serialize import SerializationFormat
from ansible_navigator.utils.serialize import serialize


SHARE_DIR = os.path.abspath(
    os.path.join(os.path.basename(__file__), "..", "share", "ansible_navigator"),
)
THEME_PATH = os.path.join(SHARE_DIR, "themes", "dark_vs.json")
GRAMMAR_DIR = os.path.join(SHARE_DIR, "grammar")


class Sample(NamedTuple):
    """Sample data for colorize tests."""

    serialization_format: SerializationFormat
    content: Dict[str, str] = {"test": "data"}
    content_view: ContentView = ContentView.NORMAL


SAMPLE_JSON = Sample(serialization_format=SerializationFormat.JSON)._asdict()
SAMPLE_YAML = Sample(serialization_format=SerializationFormat.YAML)._asdict()


def test_basic_success_json():
    """Ensure the json string is returned as 1 lines, 5 parts and can be reassembled
    to the json string"""
    sample = serialize(**SAMPLE_JSON) + "\n"
    colorized = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="source.json",
    )
    assert len(colorized) == 3
    serialized_lines = sample.splitlines(keepends=True)
    colorized_lines = ["".join(part.chars for part in line) for line in colorized]
    assert serialized_lines == colorized_lines
    assert "".join(serialized_lines) == sample


def test_basic_success_yaml():
    """Ensure the yaml string is returned as 2 lines, with 1 and 3 parts
    respectively, ensure the parts of the second line can be reassembled to
    the second line of the yaml string
    """
    sample = serialize(**SAMPLE_YAML)
    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="source.yaml",
    )
    assert len(result) == 2
    assert len(result[0]) == 1
    assert result[0][0].chars == sample.splitlines(keepends=True)[0]
    assert len(result[1]) == 4
    assert (
        "".join(line_part.chars for line_part in result[1]) == sample.splitlines(keepends=True)[1]
    )


def test_basic_success_log():
    """Ensure the log string is returned as 1 line, with 5 parts.

    Also ensure the parts can be reassembled to match the string.
    """
    sample = "1 ERROR text 42\n"

    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="text.log",
    )
    assert len(result) == 1
    first_line = result[0]
    line_parts = tuple(p.chars for p in first_line)
    assert line_parts == ("1", " ", "ERROR", " text ", "42", "\n")
    assert "".join(line_parts) == sample


def test_basic_success_no_color():
    """Ensure scope ``no_color`` return just lines."""
    sample = serialize(**SAMPLE_JSON)
    colorized = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="no_color",
    )
    assert not any(part.color for line in colorized for part in line)


@patch("ansible_navigator.ui_framework.colorize.tokenize")
def test_graceful_failure(mocked_func, caplog):
    """Ensure a tokenization error returns the original one line json string
    w/o color and the log reflects the critical error
    """
    mocked_func.side_effect = ValueError()
    sample = serialize(**SAMPLE_JSON)

    _result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="source.json",
    )
    assert "rendered without color" in caplog.text


YAML_TXT = """
- ansible.builtin.debug:
    var: before

# this is a comment

- ansible.builtin.debug:
    var: after
"""

YAML_TXT_EXPECTED = [
    [SimpleLinePart(chars="\n", column=0, color=None)],
    [
        SimpleLinePart(chars="- ", column=0, color=None),
        SimpleLinePart(chars="ansible.builtin.debug", column=2, color=(86, 156, 214)),
        SimpleLinePart(chars=":\n", column=23, color=None),
    ],
    [
        SimpleLinePart(chars="    ", column=0, color=None),
        SimpleLinePart(chars="var", column=4, color=(86, 156, 214)),
        SimpleLinePart(chars=": ", column=7, color=None),
        SimpleLinePart(chars="before", column=9, color=(206, 145, 120)),
        SimpleLinePart(chars="\n", column=15, color=None),
    ],
    [SimpleLinePart(chars="\n", column=0, color=None)],
    [SimpleLinePart(chars="# this is a comment\n", column=0, color=(106, 153, 85))],
    [SimpleLinePart(chars="\n", column=0, color=None)],
    [
        SimpleLinePart(chars="- ", column=0, color=None),
        SimpleLinePart(chars="ansible.builtin.debug", column=2, color=(86, 156, 214)),
        SimpleLinePart(chars=":\n", column=23, color=None),
    ],
    [
        SimpleLinePart(chars="    ", column=0, color=None),
        SimpleLinePart(chars="var", column=4, color=(86, 156, 214)),
        SimpleLinePart(chars=": ", column=7, color=None),
        SimpleLinePart(chars="after", column=9, color=(206, 145, 120)),
        SimpleLinePart(chars="\n", column=14, color=None),
    ],
]


def test_basic_success_yaml_text():
    """Ensure the yaml string is returned matche the expected tokens."""
    content_format = ContentFormat.YAML_TXT

    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=YAML_TXT,
        scope=content_format.value.scope,
    )
    assert result == YAML_TXT_EXPECTED
