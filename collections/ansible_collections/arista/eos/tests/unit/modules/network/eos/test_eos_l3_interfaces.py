#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_l3_interfaces
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosL3InterfacesModule(TestEosModule):
    module = eos_l3_interfaces

    def setUp(self):
        super(TestEosL3InterfacesModule, self).setUp()

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
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.l3_interfaces.l3_interfaces.L3_interfacesFacts.get_device_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosL3InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli"):
        def load_from_file(*args, **kwargs):
            return load_fixture("eos_l3_interfaces_config.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_eos_l3_interfaces_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1",
                        ipv4=[dict(address="198.51.100.14/24")],
                    ),
                    dict(
                        name="Ethernet2",
                        ipv4=[dict(address="203.0.113.27/24")],
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "interface Ethernet1",
            "ip address 198.51.100.14/24",
            "interface Ethernet2",
            "ip address 203.0.113.27/24",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l3_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1", ipv4=[dict(address="192.0.2.12/24")]
                    ),
                    dict(
                        name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_l3_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        ipv4=[dict(address="203.0.113.27/24")],
                    ),
                    dict(
                        name="Management1",
                        ipv4=[dict(address="dhcp")],
                        ipv6=[dict(address="auto-config")],
                    ),
                ],
                state="overridden",
            )
        )
        commands = [
            "interface Ethernet2",
            "no ipv6 address 2001:db8::1/64",
            "ip address 203.0.113.27/24",
            "interface Ethernet1",
            "no ip address",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l3_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
                    ),
                    dict(
                        name="Ethernet1", ipv4=[dict(address="192.0.2.12/24")]
                    ),
                    dict(
                        name="Management1",
                        ipv4=[dict(address="dhcp")],
                        ipv6=[dict(address="auto-config")],
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_l3_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        ipv4=[dict(address="203.0.113.27/24")],
                    )
                ],
                state="replaced",
            )
        )
        commands = [
            "interface Ethernet2",
            "ip address 203.0.113.27/24",
            "no ipv6 address 2001:db8::1/64",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l3_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
                    ),
                    dict(
                        name="Ethernet1", ipv4=[dict(address="192.0.2.12/24")]
                    ),
                    dict(
                        name="Management1",
                        ipv4=[dict(address="dhcp")],
                        ipv6=[dict(address="auto-config")],
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_l3_interfaces_deleted(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
                    )
                ],
                state="deleted",
            )
        )
        commands = ["interface Ethernet2", "no ipv6 address 2001:db8::1/64"]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l3_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1",
                        ipv4=[dict(address="198.51.100.14/24")],
                    ),
                    dict(
                        name="Ethernet2",
                        ipv4=[dict(address="203.0.113.27/24")],
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "interface Ethernet1",
            "ip address 198.51.100.14/24",
            "interface Ethernet2",
            "ip address 203.0.113.27/24",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_eos_l3_interfaces_parsed(self):
        commands = [
            "interface Ethernet1",
            "ip address 198.51.100.14/24",
            "interface Ethernet2",
            "ip address 203.0.113.27/24",
        ]
        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = [
            {"name": "Ethernet1", "ipv4": [{"address": "198.51.100.14/24"}]},
            {"name": "Ethernet2", "ipv4": [{"address": "203.0.113.27/24"}]},
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_eos_l3_interfaces_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        gather_list = [
            {"name": "Ethernet1", "ipv4": [{"address": "192.0.2.12/24"}]},
            {"name": "Ethernet2", "ipv6": [{"address": "2001:db8::1/64"}]},
            {
                "name": "Management1",
                "ipv4": [{"address": "dhcp"}],
                "ipv6": [{"address": "auto-config"}],
            },
        ]
        self.assertEqual(gather_list, result["gathered"])
