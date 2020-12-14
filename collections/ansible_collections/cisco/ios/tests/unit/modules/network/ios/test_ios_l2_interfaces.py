#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_l2_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosL2InterfacesModule(TestIosModule):
    module = ios_l2_interfaces

    def setUp(self):
        super(TestIosL2InterfacesModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2_interfaces.l2_interfaces."
            "L2_InterfacesFacts.get_l2_interfaces_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_l2_interfaces.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_l2_interfaces_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="GigabitEthernet0/1",
                        voice=dict(vlan=40),
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["60"],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["12-15", "20"],
                        ),
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "interface GigabitEthernet0/1",
            "switchport access vlan 20",
            "switchport voice vlan 40",
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan add 60",
            "switchport trunk pruning vlan add 12-15",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        mode="access",
                        name="GigabitEthernet0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="dot1q",
                            native_vlan=10,
                            pruning_vlans=["10", "20"],
                        ),
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_l2_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["20-25", "40"],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["10"],
                        ),
                    )
                ],
                state="replaced",
            )
        )
        commands = [
            "interface GigabitEthernet0/2",
            "no switchport mode",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan 20-25,40",
            "switchport trunk pruning vlan 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        mode="access",
                        name="GigabitEthernet0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="dot1q",
                            native_vlan=10,
                            pruning_vlans=["10", "20"],
                        ),
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_l2_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        voice=dict(vlan=20),
                        mode="access",
                        name="GigabitEthernet0/2",
                    )
                ],
                state="overridden",
            )
        )
        commands = [
            "interface GigabitEthernet0/1",
            "no switchport mode",
            "no switchport access vlan",
            "interface GigabitEthernet0/2",
            "no switchport trunk encapsulation",
            "no switchport trunk native vlan",
            "no switchport trunk allowed vlan",
            "no switchport trunk pruning vlan",
            "switchport access vlan 10",
            "switchport voice vlan 20",
            "switchport mode access",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=10),
                        mode="access",
                        name="GigabitEthernet0/1",
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="dot1q",
                            native_vlan=10,
                            pruning_vlans=["10", "20"],
                        ),
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_l2_interfaces_deleted_interface(self):
        set_module_args(
            dict(config=[dict(name="GigabitEthernet0/1")], state="deleted")
        )
        commands = [
            "interface GigabitEthernet0/1",
            "no switchport mode",
            "no switchport access vlan",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_ios_l2_interfaces_deleted_all(self):
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "interface GigabitEthernet0/1",
            "no switchport mode",
            "no switchport access vlan",
            "interface GigabitEthernet0/2",
            "no switchport mode",
            "no switchport trunk encapsulation",
            "no switchport trunk native vlan",
            "no switchport trunk allowed vlan",
            "no switchport trunk pruning vlan",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_ios_l2_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config="interface GigabitEthernet0/1\nswitchport mode trunk\nswitchport trunk native vlan 10\nswitchport trunk encapsulation dot1q\n",
                state="parsed",
            )
        )
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "mode": "trunk",
                "name": "GigabitEthernet0/1",
                "trunk": {"encapsulation": "dot1q", "native_vlan": 10},
            }
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_l2_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        access=dict(vlan=20),
                        mode="access",
                        name="GigabitEthernet0/1",
                        voice=dict(vlan=40),
                    ),
                    dict(
                        mode="trunk",
                        name="GigabitEthernet0/2",
                        trunk=dict(
                            allowed_vlans=["10-20", "40"],
                            encapsulation="isl",
                            native_vlan=20,
                            pruning_vlans=["12-15", "20"],
                        ),
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "interface GigabitEthernet0/1",
            "switchport access vlan 20",
            "switchport voice vlan 40",
            "switchport mode access",
            "interface GigabitEthernet0/2",
            "switchport trunk encapsulation isl",
            "switchport trunk native vlan 20",
            "switchport trunk allowed vlan 10-20,40",
            "switchport trunk pruning vlan 12-15,20",
            "switchport mode trunk",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)
