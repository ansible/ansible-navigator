# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.vyos.vyos.tests.unit.compat.mock import patch
from ansible_collections.vyos.vyos.plugins.modules import vyos_ospf_interfaces
from ansible_collections.vyos.vyos.tests.unit.modules.utils import (
    set_module_args,
)
from .vyos_module import TestVyosModule, load_fixture


class TestVyosOspfInterfacesModule(TestVyosModule):

    module = vyos_ospf_interfaces

    def setUp(self):
        super(TestVyosOspfInterfacesModule, self).setUp()
        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_execute_show_command = patch(
            "ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.facts.ospf_interfaces.ospf_interfaces.Ospf_interfacesFacts.get_device_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestVyosOspfInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        if filename is None:
            filename = "vyos_ospf_interfaces_config.cfg"

        def load_from_file(*args, **kwargs):
            output = load_fixture(filename)
            return output

        self.execute_show_command.side_effect = load_from_file

    def sort_address_family(self, entry_list):
        for entry in entry_list:
            if entry.get("address_family"):
                entry["address_family"].sort(key=lambda i: i.get("afi"))

    def test_vyos_ospf_interfaces_merged_new_config(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                                authentication=dict(
                                    plaintext_password="abcdefg!"
                                ),
                                priority=55,
                            ),
                            dict(afi="ipv6", mtu_ignore=True, instance=20),
                        ],
                    ),
                    dict(
                        name="bond2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                transmit_delay=9,
                            ),
                            dict(afi="ipv6", passive=True),
                        ],
                    ),
                ],
                state="merged",
            )
        )
        commands = [
            "set interfaces bonding bond2 ip ospf transmit-delay 9",
            "set interfaces bonding bond2 ipv6 ospfv3 passive",
            "set interfaces ethernet eth0 ip ospf cost 100",
            "set interfaces ethernet eth0 ip ospf priority 55",
            "set interfaces ethernet eth0 ip ospf authentication plaintext-password abcdefg!",
            "set interfaces ethernet eth0 ipv6 ospfv3 instance-id 20",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospf_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(afi="ipv6", mtu_ignore=True, instance=33),
                        ],
                    ),
                    dict(
                        name="eth1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                            ),
                            dict(afi="ipv6", ifmtu=33),
                        ],
                    ),
                ],
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospf_interfaces_existing_config_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(afi="ipv6", cost=500),
                        ],
                    ),
                    dict(
                        name="eth1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                priority=100,
                            ),
                            dict(afi="ipv6", ifmtu=25),
                        ],
                    ),
                ],
            )
        )
        commands = [
            "set interfaces ethernet eth0 ipv6 ospfv3 cost 500",
            "set interfaces ethernet eth1 ip ospf priority 100",
            "set interfaces ethernet eth1 ipv6 ospfv3 ifmtu 25",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospf_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                                authentication=dict(
                                    plaintext_password="abcdefg!"
                                ),
                                priority=55,
                            ),
                        ],
                    ),
                    dict(
                        name="bond2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                transmit_delay=9,
                            ),
                            dict(afi="ipv6", passive=True),
                        ],
                    ),
                ],
                state="replaced",
            )
        )
        commands = [
            "set interfaces bonding bond2 ip ospf transmit-delay 9",
            "set interfaces bonding bond2 ipv6 ospfv3 passive",
            "set interfaces ethernet eth0 ip ospf cost 100",
            "set interfaces ethernet eth0 ip ospf priority 55",
            "set interfaces ethernet eth0 ip ospf authentication plaintext-password abcdefg!",
            "delete interfaces ethernet eth0 ipv6 ospfv3 instance-id 33",
            "delete interfaces ethernet eth0 ipv6 ospfv3 mtu-ignore",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospf_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(afi="ipv6", mtu_ignore=True, instance=33),
                        ],
                    ),
                    dict(
                        name="eth1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                            ),
                            dict(afi="ipv6", ifmtu=33),
                        ],
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospf_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                                authentication=dict(
                                    plaintext_password="abcdefg!"
                                ),
                                priority=55,
                            ),
                        ],
                    ),
                    dict(
                        name="bond2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                transmit_delay=9,
                            ),
                            dict(afi="ipv6", passive=True),
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        commands = [
            "set interfaces bonding bond2 ip ospf transmit-delay 9",
            "set interfaces bonding bond2 ipv6 ospfv3 passive",
            "set interfaces ethernet eth0 ip ospf cost 100",
            "set interfaces ethernet eth0 ip ospf priority 55",
            "set interfaces ethernet eth0 ip ospf authentication plaintext-password abcdefg!",
            "delete interfaces ethernet eth1 ip ospf",
            "delete interfaces ethernet eth1 ipv6 ospfv3",
            "delete interfaces ethernet eth0 ipv6 ospfv3 mtu-ignore",
            "delete interfaces ethernet eth0 ipv6 ospfv3 instance-id 33",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospf_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(afi="ipv6", mtu_ignore=True, instance=33),
                        ],
                    ),
                    dict(
                        name="eth1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                            ),
                            dict(afi="ipv6", ifmtu=33),
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospf_interfaces_deleted(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                    ),
                ],
                state="deleted",
            )
        )
        commands = ["delete interfaces ethernet eth0 ipv6 ospfv3"]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospf_interfaces_notpresent_deleted(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth3",
                    ),
                ],
                state="deleted",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospf_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="eth0",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=100,
                                authentication=dict(
                                    plaintext_password="abcdefg!"
                                ),
                                priority=55,
                            ),
                            dict(afi="ipv6", mtu_ignore=True, instance=20),
                        ],
                    ),
                    dict(
                        name="bond2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                transmit_delay=9,
                            ),
                            dict(afi="ipv6", passive=True),
                        ],
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "set interfaces ethernet eth0 ip ospf cost 100",
            "set interfaces ethernet eth0 ip ospf authentication plaintext-password abcdefg!",
            "set interfaces ethernet eth0 ip ospf priority 55",
            "set interfaces ethernet eth0 ipv6 ospfv3 mtu-ignore",
            "set interfaces ethernet eth0 ipv6 ospfv3 instance-id 20",
            "set interfaces bonding bond2 ip ospf transmit-delay 9",
            "set interfaces bonding bond2 ipv6 ospfv3 passive",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_vyos_ospf_interfaces_parsed(self):
        commands = [
            "set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'",
            "set interfaces bonding bond2 ip ospf bandwidth '70'",
            "set interfaces bonding bond2 ip ospf transmit-delay '45'",
            "set interfaces bonding bond2 ipv6 ospfv3 'passive'",
            "set interfaces ethernet eth0 ip ospf cost '50'",
            "set interfaces ethernet eth0 ip ospf priority '26'",
            "set interfaces ethernet eth0 ipv6 ospfv3 instance-id '33'",
            "set interfaces ethernet eth0 ipv6 ospfv3 'mtu-ignore'",
            "set interfaces ethernet eth1 ip ospf network 'point-to-point'",
            "set interfaces ethernet eth1 ip ospf priority '26'",
            "set interfaces ethernet eth1 ip ospf transmit-delay '50'",
            "set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'",
        ]

        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "address_family": [
                    {
                        "afi": "ipv4",
                        "authentication": {
                            "md5_key": {
                                "key": "1111111111232345",
                                "key_id": 10,
                            }
                        },
                        "bandwidth": 70,
                        "transmit_delay": 45,
                    },
                    {"afi": "ipv6", "passive": True},
                ],
                "name": "bond2",
            },
            {
                "address_family": [
                    {"afi": "ipv4", "cost": 50, "priority": 26},
                    {"afi": "ipv6", "instance": "33", "mtu_ignore": True},
                ],
                "name": "eth0",
            },
            {
                "address_family": [
                    {
                        "afi": "ipv4",
                        "network": "point-to-point",
                        "priority": 26,
                        "transmit_delay": 50,
                    },
                    {"afi": "ipv6", "dead_interval": 39},
                ],
                "name": "eth1",
            },
        ]
        result_list = self.sort_address_family(result["parsed"])
        given_list = self.sort_address_family(parsed_list)
        self.assertEqual(result_list, given_list)

    def test_vyos_ospf_interfaces_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(
            changed=False, filename="vyos_ospf_interfaces_config.cfg"
        )
        gathered_list = [
            {
                "address_family": [
                    {"afi": "ipv6", "instance": "33", "mtu_ignore": True}
                ],
                "name": "eth0",
            },
            {
                "address_family": [
                    {"afi": "ipv4", "cost": 100},
                    {"afi": "ipv6", "ifmtu": 33},
                ],
                "name": "eth1",
            },
        ]

        result_list = self.sort_address_family(result["gathered"])
        given_list = self.sort_address_family(gathered_list)
        self.assertEqual(result_list, given_list)
