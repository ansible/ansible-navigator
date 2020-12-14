#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_l2_interfaces
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosL2InterfacesModule(TestEosModule):
    module = eos_l2_interfaces

    def setUp(self):
        super(TestEosL2InterfacesModule, self).setUp()

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
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.l2_interfaces.l2_interfaces.L2_interfacesFacts.get_device_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli"):
        def load_from_file(*args, **kwargs):
            return load_fixture("eos_l2_interfaces_config.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_eos_l2_interfaces_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1",
                        trunk=dict(
                            native_vlan=10, trunk_allowed_vlans=["20-25"]
                        ),
                    ),
                    dict(name="Ethernet2", access=dict(vlan=30)),
                ],
                state="merged",
            )
        )
        commands = [
            "interface Ethernet1",
            "switchport trunk native vlan 10",
            "switchport trunk allowed vlan add 20,21,22,23,24,25",
            "interface Ethernet2",
            "switchport access vlan 30",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l2_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(name="Ethernet2", trunk=dict(native_vlan=20)),
                    dict(
                        name="Ethernet1",
                        access=dict(vlan=20),
                        trunk=dict(trunk_allowed_vlans=["7-10"]),
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_l2_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        mode="trunk",
                        trunk=dict(
                            native_vlan=50, trunk_allowed_vlans=[3, "5"]
                        ),
                    ),
                    dict(name="Ethernet3", access=dict(vlan=30)),
                ],
                state="replaced",
            )
        )
        commands = [
            "interface Ethernet2",
            "switchport trunk native vlan 50",
            "switchport trunk allowed vlan 3,5",
            "interface Ethernet3",
            "switchport access vlan 30",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l2_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        mode="trunk",
                        trunk=dict(native_vlan=20),
                    ),
                    dict(
                        name="Ethernet1",
                        access=dict(vlan=20),
                        trunk=dict(trunk_allowed_vlans=["7-10"]),
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_l2_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        mode="trunk",
                        trunk=dict(native_vlan=50),
                    )
                ],
                state="overridden",
            )
        )
        commands = [
            "interface Ethernet2",
            "switchport trunk native vlan 50",
            "interface Ethernet1",
            "no switchport access vlan",
            "no switchport trunk allowed vlan",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_l2_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        mode="trunk",
                        trunk=dict(native_vlan=20),
                    ),
                    dict(
                        name="Ethernet1",
                        access=dict(vlan=20),
                        trunk=dict(trunk_allowed_vlans=["7-10"]),
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_l2_interfaces_deleted(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet2",
                        mode="trunk",
                        trunk=dict(native_vlan=20),
                    ),
                    dict(name="Ethernet1", access=dict(vlan=20)),
                ],
                state="deleted",
            )
        )
        commands = [
            "interface Ethernet2",
            "no switchport mode",
            "no switchport trunk native vlan",
            "interface Ethernet1",
            "no switchport access vlan",
            "no switchport trunk allowed vlan",
        ]
        self.execute_module(changed=True, commands=commands)
