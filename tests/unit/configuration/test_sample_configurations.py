"""  Some tests using a alternate test configurations
to prove code paths not covered by the ansible-navigator
configuration
"""
import pytest

from ansible_navigator.configuration import Configuration

from ansible_navigator.configuration.application_post_processor import ApplicationPostProcessor

from ansible_navigator.configuration.definitions import CliParameters
from ansible_navigator.configuration.definitions import Config
from ansible_navigator.configuration.definitions import Entry
from ansible_navigator.configuration.definitions import EntryValue
from ansible_navigator.configuration.definitions import SubCommand

from ansible_navigator.configuration.parser import Parser


def test_cmdline_source_not_set():
    """Ensure a Config without a subparse entry fails"""
    TestConfig = Config(
        application_name="test_config1",
        post_processor=ApplicationPostProcessor(),
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[
            Entry(
                name="cmdline",
                short_description="cmdline",
                value=EntryValue(),
            ),
        ],
    )
    cfg = Configuration(params=[], application_configuration=TestConfig)
    cfg._post_process()
    assert "Completed post processing for cmdline" in cfg._messages[0][1]
    assert cfg._errors == []


def test_no_subcommand():
    """Ensure a Config without a subparse entry fails"""
    TestConfig = Config(
        application_name="test_config1",
        post_processor=None,
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[],
    )
    with pytest.raises(ValueError, match="No entry with subparser value defined"):
        Configuration(params=[], application_configuration=TestConfig).configure()


def test_many_subcommand():
    """Ensure a Config without a subparse entry fails"""
    TestConfig = Config(
        application_name="test_config1",
        post_processor=None,
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[
            Entry(
                name="sb1",
                short_description="Subcommands",
                subcommand_value=True,
                value=EntryValue(default="welcome"),
            ),
            Entry(
                name="sb2",
                short_description="Subcommands",
                subcommand_value=True,
                value=EntryValue(default="welcome"),
            ),
        ],
    )
    with pytest.raises(ValueError, match="Multiple entries with subparser value defined"):
        Configuration(params=[], application_configuration=TestConfig).configure()


def test_invalid_choice_not_set():
    """Ensure a Config without a subparse entry fails"""
    TestConfig = Config(
        application_name="test_config1",
        post_processor=None,
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[
            Entry(
                name="sb1",
                short_description="Subcommands",
                subcommand_value=True,
                value=EntryValue(default="welcome"),
            ),
            Entry(
                name="e1",
                short_description="ex1",
                value=EntryValue(),
            ),
        ],
    )
    with pytest.raises(ValueError, match="Current source not set for e1"):
        TestConfig.entry("e1").invalid_choice


def test_cutom_nargs_for_postional():
    """Ensure a Config without a subparse entry fails"""
    TestConfig = Config(
        application_name="test_config1",
        post_processor=None,
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[
            Entry(
                name="sb1",
                short_description="Subcommands",
                subcommand_value=True,
                value=EntryValue(default="welcome"),
            ),
            Entry(
                name="e1",
                cli_parameters=CliParameters(positional=True, nargs=3),
                short_description="ex1",
                value=EntryValue(),
            ),
        ],
    )
    parser = Parser(TestConfig)
    entry = [action for action in parser.parser._actions if action.dest == "e1"]
    assert entry[0].nargs == 3


def test_apply_cli_source_not_set():
    """Ensure a Config without a subparse entry fails"""
    TestConfig = Config(
        application_name="test_config1",
        post_processor=ApplicationPostProcessor(),
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[
            Entry(
                name="e1",
                short_description="e1",
                value=EntryValue(),
            ),
            Entry(
                name="e2",
                short_description="e2",
                value=EntryValue(),
            ),
        ],
        initial=True,
    )

    cfg = Configuration(
        params=[], application_configuration=TestConfig, apply_previous_cli_entries=["all"]
    )
    cfg._apply_previous_cli_to_current()
    assert cfg._messages == []
    assert cfg._errors == []
