#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_ospf_interfaces
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosOspfInterfacesModule(TestIosModule):
    module = ios_ospf_interfaces

    def setUp(self):
        super(TestIosOspfInterfacesModule, self).setUp()

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
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module."
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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospf_interfaces.ospf_interfaces."
            "Ospf_InterfacesFacts.get_ospf_interfaces_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosOspfInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_ospf_interfaces.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_ospf_interfaces_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=30),
                                network=dict(broadcast=True),
                                priority=60,
                                resync_timeout=90,
                                ttl_security=dict(hops=120),
                                authentication=dict(key_chain="test_key"),
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                dead_interval=dict(time=100),
                                network=dict(manet=True),
                                priority=50,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=50),
                                priority=50,
                                ttl_security=dict(hops=150),
                            )
                        ],
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "interface GigabitEthernet0/3",
            "ip ospf bfd",
            "ip ospf cost 50",
            "ip ospf priority 50",
            "ip ospf ttl-security hops 150",
            "interface GigabitEthernet0/2",
            "ip ospf authentication key-chain test_key",
            "ip ospf bfd",
            "ip ospf cost 30",
            "ip ospf network broadcast",
            "ip ospf priority 60",
            "ip ospf resync-timeout 90",
            "ip ospf ttl-security hops 120",
            "ipv6 ospf bfd",
            "ipv6 ospf dead-interval 100",
            "ipv6 ospf network manet",
            "ipv6 ospf priority 50",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv4",
                                adjacency=True,
                                cost=dict(interface_cost=30),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                ttl_security=dict(hops=50),
                            )
                        ],
                        name="GigabitEthernet0/2",
                    ),
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                adjacency=True,
                                priority=20,
                                process=dict(id=55, area_id="105"),
                                transmit_delay=30,
                            )
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospf_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=50),
                                priority=50,
                                ttl_security=dict(hops=150),
                            )
                        ],
                    )
                ],
                state="replaced",
            )
        )
        commands = [
            "interface GigabitEthernet0/3",
            "ip ospf bfd",
            "ip ospf cost 50",
            "ip ospf priority 50",
            "ip ospf ttl-security hops 150",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv4",
                                adjacency=True,
                                cost=dict(interface_cost=30),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                ttl_security=dict(hops=50),
                            )
                        ],
                        name="GigabitEthernet0/2",
                    ),
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                adjacency=True,
                                priority=20,
                                process=dict(id=55, area_id="105"),
                                transmit_delay=30,
                            )
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospf_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                manet=dict(cost=dict(percent=10)),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                transmit_delay=50,
                            )
                        ],
                        name="GigabitEthernet0/3",
                    )
                ],
                state="overridden",
            )
        )
        commands = [
            "interface GigabitEthernet0/2",
            "no ip ospf 10 area 20",
            "no ip ospf adjacency stagger disable",
            "no ip ospf cost 30",
            "no ip ospf priority 40",
            "no ip ospf ttl-security hops 50",
            "interface GigabitEthernet0/3",
            "ipv6 ospf 10 area 20",
            "no ipv6 ospf adjacency stagger disable",
            "ipv6 ospf manet peering cost percent 10",
            "ipv6 ospf priority 40",
            "ipv6 ospf transmit-delay 50" "",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_family=[
                            dict(
                                afi="ipv4",
                                adjacency=True,
                                cost=dict(interface_cost=30),
                                priority=40,
                                process=dict(id=10, area_id="20"),
                                ttl_security=dict(hops=50),
                            )
                        ],
                        name="GigabitEthernet0/2",
                    ),
                    dict(
                        address_family=[
                            dict(
                                afi="ipv6",
                                adjacency=True,
                                priority=20,
                                process=dict(id=55, area_id="105"),
                                transmit_delay=30,
                            )
                        ],
                        name="GigabitEthernet0/3",
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospf_interfaces_deleted_interface(self):
        set_module_args(
            dict(config=[dict(name="GigabitEthernet0/2")], state="deleted")
        )
        commands = [
            "interface GigabitEthernet0/2",
            "no ip ospf priority 40",
            "no ip ospf adjacency stagger disable",
            "no ip ospf ttl-security hops 50",
            "no ip ospf 10 area 20",
            "no ip ospf cost 30",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_deleted_all(self):
        set_module_args(dict(config=[], state="deleted"))
        commands = [
            "interface GigabitEthernet0/3",
            "no ipv6 ospf 55 area 105",
            "no ipv6 ospf adjacency stagger disable",
            "no ipv6 ospf priority 20",
            "no ipv6 ospf transmit-delay 30",
            "interface GigabitEthernet0/2",
            "no ip ospf 10 area 20",
            "no ip ospf adjacency stagger disable",
            "no ip ospf cost 30",
            "no ip ospf priority 40",
            "no ip ospf ttl-security hops 50",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospf_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="GigabitEthernet0/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=30),
                                network=dict(broadcast=True),
                                priority=60,
                                resync_timeout=90,
                                ttl_security=dict(hops=120),
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                dead_interval=dict(time=100),
                                network=dict(manet=True),
                                priority=50,
                            ),
                        ],
                    ),
                    dict(
                        name="GigabitEthernet0/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                bfd=True,
                                cost=dict(interface_cost=50),
                                priority=50,
                                ttl_security=dict(hops=150),
                            )
                        ],
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "interface GigabitEthernet0/3",
            "ip ospf bfd",
            "ip ospf cost 50",
            "ip ospf priority 50",
            "ip ospf ttl-security hops 150",
            "interface GigabitEthernet0/2",
            "ip ospf bfd",
            "ip ospf cost 30",
            "ip ospf network broadcast",
            "ip ospf priority 60",
            "ip ospf resync-timeout 90",
            "ip ospf ttl-security hops 120",
            "ipv6 ospf bfd",
            "ipv6 ospf dead-interval 100",
            "ipv6 ospf network manet",
            "ipv6 ospf priority 50",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
