"""tests for colorize
"""
import json
import os

from unittest.mock import patch

from ansible_navigator._yaml import human_dump
from ansible_navigator.ui_framework.colorize import Colorize


SHARE_DIR = os.path.abspath(
    os.path.join(os.path.basename(__file__), "..", "share", "ansible_navigator"),
)
THEME_PATH = os.path.join(SHARE_DIR, "themes", "dark_vs.json")
GRAMMAR_DIR = os.path.join(SHARE_DIR, "grammar")


def test_basic_success_json():
    """Ensure the json string is returned as 1 lines, 5 parts and can be reassembled
    to the json string"""
    sample = json.dumps({"test": "data"})
    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="source.json",
    )
    assert len(result) == 1
    assert len(result[0]) == 5
    assert "".join(line_part.chars for line_part in result[0]) == sample


def test_basic_success_yaml():
    """Ensure the yaml string is returned as 2 lines, with 1 and 3 parts
    respectively, ensure the parts of the second line can be reassembled to
    the second line of the yaml string
    """
    sample = human_dump({"test": "data"})
    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="source.yaml",
    )
    assert len(result) == 2
    assert len(result[0]) == 1
    assert result[0][0].chars == sample.splitlines()[0]
    assert len(result[1]) == 3
    assert "".join(line_part.chars for line_part in result[1]) == sample.splitlines()[1]


def test_basic_success_no_color():
    """Ensure scope ``no_color`` return just lines."""
    sample = json.dumps({"test": "data"})
    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="no_color",
    )
    assert len(result) == 1
    assert len(result[0]) == 1
    assert result[0][0].chars == sample
    assert result[0][0].color is None
    assert result[0][0].column == 0


@patch("ansible_navigator.ui_framework.colorize.tokenize")
def test_graceful_failure(mocked_func, caplog):
    """Ensure a tokenization error returns the original one line json string
    w/o color and the log reflects the critical error
    """
    mocked_func.side_effect = ValueError()
    sample = json.dumps({"test": "data"})
    result = Colorize(grammar_dir=GRAMMAR_DIR, theme_path=THEME_PATH).render(
        doc=sample,
        scope="source.json",
    )
    assert len(result) == 1
    assert len(result[0]) == 1
    assert result[0][0].chars == sample
    assert result[0][0].color is None
    assert result[0][0].column == 0
    assert "rendered without color" in caplog.text
