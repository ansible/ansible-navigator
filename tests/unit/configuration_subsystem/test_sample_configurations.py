"""  Some tests using a alternate test configurations
to prove code paths not covered by the ansible-navigator
configuration
"""
import pytest

from ansible_navigator.configuration_subsystem.configurator import Configurator

from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)

from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.configuration_subsystem.definitions import CliParameters
from ansible_navigator.configuration_subsystem.definitions import Entry
from ansible_navigator.configuration_subsystem.definitions import EntryValue
from ansible_navigator.configuration_subsystem.definitions import SubCommand

from ansible_navigator.configuration_subsystem.parser import Parser

# pylint: disable=protected-access


def test_cmdline_source_not_set():
    """Ensure a Config without a subparse entry fails"""
    test_config = ApplicationConfiguration(
        application_name="test_config1",
        post_processor=NavigatorPostProcessor(),
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
    configurator = Configurator(params=[], application_configuration=test_config)
    configurator._post_process()
    assert "Completed post processing for cmdline" in configurator._messages[0][1]
    assert configurator._errors == []


def test_no_subcommand():
    """Ensure a Config without a subparse entry fails"""
    test_config = ApplicationConfiguration(
        application_name="test_config1",
        post_processor=None,
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[],
    )
    with pytest.raises(ValueError, match="No entry with subparser value defined"):
        Configurator(params=[], application_configuration=test_config).configure()


def test_many_subcommand():
    """Ensure a Config without a subparse entry fails"""
    test_config = ApplicationConfiguration(
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
        Configurator(params=[], application_configuration=test_config).configure()


def test_invalid_choice_not_set():
    """Ensure an error is raised for no choice"""
    test_config = ApplicationConfiguration(
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
        test_config.entry("e1").invalid_choice  # pylint: disable=expression-not-assigned


def test_cutom_nargs_for_postional():
    """Ensure a nargs for a positional are carried forward"""
    test_config = ApplicationConfiguration(
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
                subcommands=["subcommand1"],
            ),
        ],
    )
    parser = Parser(test_config)
    assert parser.parser._actions[1].choices["subcommand1"]._actions[1].nargs == 3
