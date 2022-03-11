"""test the mode post processor
using invalid package and subcommand names
"""
from ansible_navigator.configuration_subsystem.configurator import Configurator
from ansible_navigator.configuration_subsystem.definitions import (
    ApplicationConfiguration,
)
from ansible_navigator.configuration_subsystem.definitions import SettingsEntry
from ansible_navigator.configuration_subsystem.definitions import SettingsEntryValue
from ansible_navigator.configuration_subsystem.definitions import SubCommand
from ansible_navigator.configuration_subsystem.navigator_configuration import Internals
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)


# pylint: disable=protected-access


def test_import_error():
    """Ensure an error for invalid action_package"""
    test_config = ApplicationConfiguration(
        application_name="test_config1",
        application_version="1.0",
        internals=Internals(action_packages=["__ansible_navigator.__actions"]),
        post_processor=NavigatorPostProcessor(),
        subcommands=[
            SubCommand(name="subcommand1", description="subcommand1"),
        ],
        entries=[
            SettingsEntry(
                name="app",
                short_description="test_app",
                value=SettingsEntryValue(current="subcommand1"),
            ),
            SettingsEntry(
                name="mode",
                short_description="mode",
                value=SettingsEntryValue(),
            ),
        ],
    )
    test_config.internals.initializing = True
    configurator = Configurator(params=[], application_configuration=test_config)
    configurator._post_process()
    message = "Unable to load action package: '__ansible_navigator.__actions':"
    message += " No module named '__ansible_navigator'"
    assert message in (entry.message for entry in configurator._messages)
    exit_msg = "Unable to find an action for 'subcommand1', tried: '__ansible_navigator.__actions'"
    assert exit_msg in [exit_msg.message for exit_msg in configurator._exit_messages]


def test_subcommand_not_found():
    """Ensure an error for invalid subcommand/action"""
    test_config = ApplicationConfiguration(
        application_name="test_config1",
        application_version="1.0",
        internals=Internals(action_packages=["ansible_navigator.actions"]),
        post_processor=NavigatorPostProcessor(),
        subcommands=[
            SubCommand(name="__test_action", description="test_action"),
        ],
        entries=[
            SettingsEntry(
                name="app",
                short_description="test_app",
                value=SettingsEntryValue(current="__test_action"),
            ),
            SettingsEntry(
                name="mode",
                short_description="mode",
                value=SettingsEntryValue(),
            ),
        ],
    )
    test_config.internals.initializing = True
    configurator = Configurator(params=[], application_configuration=test_config)
    configurator._post_process()
    exit_msg = "Unable to find an action for '__test_action', tried: 'ansible_navigator.actions'"
    assert exit_msg in [exit_msg.message for exit_msg in configurator._exit_messages]
