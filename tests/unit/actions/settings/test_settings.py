"""Unit tests for the ``settings`` action."""

from dataclasses import asdict
from dataclasses import dataclass

import pytest

from ansible_navigator.actions.settings import CONTENT_HEADING_DEFAULT
from ansible_navigator.actions.settings import CONTENT_HEADING_NOT_DEFAULT
from ansible_navigator.actions.settings import color_menu
from ansible_navigator.actions.settings import content_heading
from ansible_navigator.configuration_subsystem import PresentableSettingsEntry
from ansible_navigator.configuration_subsystem.defs_presentable import PresentableCliParameters
from ansible_navigator.ui_framework import Color
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import Decoration
from tests.defaults import BaseScenario
from tests.defaults import id_func


@dataclass
class ColorMenuTestEntry(BaseScenario):
    """A test for menu coloring."""

    color: int
    """The color for menu entry"""
    comment: str
    """Describe the test"""
    decoration: int
    """The test decoration"""
    default: bool
    """Is the current value equal to the default"""

    def __str__(self) -> str:
        """Provide a string representation.

        Returns:
            The string representation of self
        """
        return self.comment


ColorMenuTestEntries = (
    pytest.param(
        ColorMenuTestEntry(
            comment="default/green",
            color=Color.GREEN,
            decoration=Decoration.NORMAL,
            default=True,
        ),
        id="0",
    ),
    pytest.param(
        ColorMenuTestEntry(
            comment="not default/yellow",
            color=Color.YELLOW,
            decoration=Decoration.NORMAL,
            default=False,
        ),
        id="1",
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=ColorMenuTestEntries)
def test_color_menu(data: ColorMenuTestEntry) -> None:
    """Test color menu for a val set to the default.

    Args:
        data: A test entry
    """
    entry = PresentableSettingsEntry(
        choices=[],
        current_settings_file="",
        current_value="",
        default=data.default,
        default_value="",
        description="",
        env_var="",
        name="",
        settings_file_sample="",
        source="",
        subcommands=[],
        cli_parameters=PresentableCliParameters(long="", short=""),
        version_added="v0.0",
    )
    assert color_menu(0, "", entry) == (data.color, data.decoration)


@dataclass
class ContentHeadingEntry(BaseScenario):
    """A test for content headings."""

    color: int
    """The color for menu entry"""
    comment: str
    """Describes the test"""
    content: PresentableSettingsEntry
    """The content"""

    @property
    def heading(self) -> str:
        """Create the expected heading for this content.

        Returns:
            The expected heading
        """
        heading = CONTENT_HEADING_DEFAULT if self.content.default else CONTENT_HEADING_NOT_DEFAULT
        return heading.format(**asdict(self.content))

    def __str__(self) -> str:
        """Provide a string representation.

        Returns:
            The string representation of self
        """
        return self.comment


ContentHeadingEntries = (
    ContentHeadingEntry(
        color=Color.GREEN,
        comment="same",
        content=PresentableSettingsEntry(
            choices=[],
            current_settings_file="",
            current_value="navigator",
            default=True,
            default_value="navigator",
            description="",
            env_var="",
            name="TEST",
            settings_file_sample="",
            source="",
            subcommands=[],
            cli_parameters=PresentableCliParameters(long="", short=""),
            version_added="v0.0",
        ),
    ),
    ContentHeadingEntry(
        color=Color.YELLOW,
        comment="different",
        content=PresentableSettingsEntry(
            choices=[],
            current_settings_file="",
            current_value="ansible",
            default=False,
            default_value="navigator",
            description="",
            env_var="",
            name="TEST",
            settings_file_sample="",
            source="",
            subcommands=[],
            cli_parameters=PresentableCliParameters(long="", short=""),
            version_added="v0.0",
        ),
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=ContentHeadingEntries, ids=id_func)
def test_content_heading(data: ContentHeadingEntry) -> None:
    """Test menu generation.

    Args:
        data: The test data
    """
    width = 100
    heading = content_heading(obj=data.content, screen_w=width)
    heading_lines = 1
    line_parts = 1

    assert len(heading) == heading_lines

    first_line = heading[0]
    assert len(first_line) == line_parts

    first_line_part = heading[0][0]
    assert isinstance(first_line_part, CursesLinePart)
    assert len(first_line_part.string) == width + 1
    assert first_line_part.color == data.color
    assert first_line_part.column == 0
    assert data.heading in first_line_part.string
