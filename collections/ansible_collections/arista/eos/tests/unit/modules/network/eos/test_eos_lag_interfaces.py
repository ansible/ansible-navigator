# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_lag_interfaces
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosLagInterfacesModule(TestEosModule):
    module = eos_lag_interfaces

    def setUp(self):
        super(TestEosLagInterfacesModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.lag_interfaces.lag_interfaces.Lag_interfacesFacts.get_device_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosLagInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli"):
        def load_from_file(*args, **kwargs):
            return load_fixture("eos_lag_interfaces_config.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_eos_lag_interfaces_digit_name_only(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="1",
                        members=[
                            dict(member="Ethernet1", mode="on"),
                            dict(member="Ethernet2", mode="on"),
                        ],
                    )
                ],
                state="merged",
            )
        )
        commands = [
            "interface Ethernet1",
            "channel-group 1 mode on",
            "interface Ethernet2",
            "channel-group 1 mode on",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_lag_interfaces_portchannel_and_digit_name(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel1",
                        members=[
                            dict(member="Ethernet1", mode="on"),
                            dict(member="Ethernet2", mode="on"),
                        ],
                    )
                ],
                state="merged",
            )
        )
        commands = [
            "interface Ethernet1",
            "channel-group 1 mode on",
            "interface Ethernet2",
            "channel-group 1 mode on",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_lag_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel5",
                        members=[dict(member="Ethernet3", mode="passive")],
                    )
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False)

    def test_eos_lag_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel1",
                        members=[dict(member="Ethernet3", mode="on")],
                    )
                ],
                state="replaced",
            )
        )
        commands = ["interface Ethernet3", "channel-group 1 mode on"]

        self.execute_module(changed=True, commands=commands)

    def test_eos_lag_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel5",
                        members=[dict(member="Ethernet3", mode="passive")],
                    )
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False)

    def test_eos_lag_interfaces_overridden_newchannel(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel1",
                        members=[dict(member="Ethernet2", mode="on")],
                    )
                ],
                state="overridden",
            )
        )
        commands = [
            "interface Ethernet2",
            "channel-group 1 mode on",
            "no interface Port-Channel5",
        ]

        self.execute_module(changed=True, commands=commands)

    def test_eos_lag_interfaces_overridden_samechannel(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel5",
                        members=[dict(member="Ethernet2", mode="on")],
                    )
                ],
                state="overridden",
            )
        )
        commands = [
            "interface Ethernet2",
            "channel-group 5 mode on",
            "interface Ethernet3",
            "no channel-group",
        ]

        self.execute_module(changed=True, commands=commands)

    def test_eos_lag_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel5",
                        members=[dict(member="Ethernet3", mode="passive")],
                    )
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False)

    def test_eos_lag_interfaces_deleted(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel5",
                        members=[dict(member="Ethernet3", mode="passive")],
                    )
                ],
                state="deleted",
            )
        )
        commands = ["no interface Port-Channel5"]

        self.execute_module(changed=True, commands=commands)

    def test_eos_lag_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Port-Channel1",
                        members=[
                            dict(member="Ethernet1", mode="on"),
                            dict(member="Ethernet2", mode="on"),
                        ],
                    )
                ],
                state="rendered",
            )
        )
        commands = [
            "interface Ethernet1",
            "channel-group 1 mode on",
            "interface Ethernet2",
            "channel-group 1 mode on",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_eos_lag_interfaces_parsed(self):
        commands = [
            "interface Ethernet1",
            "channel-group 1 mode on",
            "interface Ethernet2",
            "channel-group 1 mode on",
        ]
        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "name": "Port-Channel1",
                "members": [
                    {"member": "Ethernet1", "mode": "on"},
                    {"member": "Ethernet2", "mode": "on"},
                ],
            }
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_eos_lag_interfaces_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        gather_list = [
            {
                "name": "Port-Channel5",
                "members": [{"member": "Ethernet3", "mode": "passive"}],
            }
        ]
        self.assertEqual(gather_list, result["gathered"])
