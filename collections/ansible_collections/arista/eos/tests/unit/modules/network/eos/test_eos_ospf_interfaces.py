#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_ospf_interfaces
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosOspf_InterfacesModule(TestEosModule):
    module = eos_ospf_interfaces

    def setUp(self):
        super(TestEosOspf_InterfacesModule, self).setUp()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_execute_show_command = patch(
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.ospf_interfaces.ospf_interfaces.Ospf_interfacesFacts.get_config"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosOspf_InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        if filename is None:
            filename = "eos_ospf_interfaces_config.cfg"

        def load_from_file(*args, **kwargs):
            output = load_fixture(filename)
            return output

        self.execute_show_command.side_effect = load_from_file

    def test_eos_ospf_interfaces_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                area=dict(area_id="0.0.0.10"),
                                cost=100,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                dead_interval=44,
                                ip_params=[
                                    dict(
                                        afi="ipv6",
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    )
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan2",
                        address_family=[
                            dict(
                                afi="ipv6",
                                retransmit_interval=144,
                                authentication_v3=dict(
                                    spi=30,
                                    algorithm="md5",
                                    keytype=7,
                                    passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                ),
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=9,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ]
            )
        )
        commands = [
            "interface Vlan1",
            "ip ospf cost 100",
            "ip ospf area 0.0.0.10",
            "ospfv3 dead-interval 44",
            "interface Vlan2",
            "ospfv3 retransmit-interval 144",
            "ospfv3 authentication ipsec spi 30 md5 passphrase 7 7hl8FV3lZ6H1mAKpjL47hQ==",
            "ospfv3 ipv4 priority 9",
            "ospfv3 ipv4 area 0.0.0.6",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospf_interfaces_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                dead_interval=29,
                                hello_interval=66,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                cost=106,
                                hello_interval=77,
                                transmit_delay=100,
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=45,
                                        area=dict(area_id="0.0.0.5"),
                                    ),
                                    dict(
                                        afi="ipv6",
                                        passive_interface=True,
                                        dead_interval=56,
                                        retransmit_interval=115,
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan3",
                        address_family=[
                            dict(
                                afi="ipv6",
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        hello_interval=45,
                                        retransmit_interval=100,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ]
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospf_interfaces_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                area=dict(area_id="0.0.0.10"),
                                cost=100,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                dead_interval=44,
                                ip_params=[
                                    dict(
                                        afi="ipv6",
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    )
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan2",
                        address_family=[
                            dict(
                                afi="ipv6",
                                retransmit_interval=144,
                                authentication_v3=dict(
                                    spi=30,
                                    algorithm="md5",
                                    keytype=7,
                                    passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                ),
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=9,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="replaced",
            )
        )
        commands = [
            "interface Vlan1",
            "ip ospf cost 100",
            "ip ospf area 0.0.0.10",
            "ospfv3 dead-interval 44",
            "no ospfv3 ipv4 priority 45",
            "no ospfv3 ipv4 area 0.0.0.5",
            "no ospfv3 ipv6 passive-interface",
            "no ospfv3 ipv6 dead-interval 56",
            "no ospfv3 ipv6 retransmit-interval 115",
            "no ospfv3 bfd",
            "no ospfv3 cost 106",
            "no ospfv3 hello-interval 77",
            "no ospfv3 transmit-delay 100",
            "no ip ospf dead-interval 29",
            "no ip ospf hello-interval 66",
            "interface Vlan2",
            "ospfv3 retransmit-interval 144",
            "ospfv3 authentication ipsec spi 30 md5 passphrase 7 7hl8FV3lZ6H1mAKpjL47hQ==",
            "ospfv3 ipv4 priority 9",
            "ospfv3 ipv4 area 0.0.0.6",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospf_interfaces_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                dead_interval=29,
                                hello_interval=66,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                cost=106,
                                hello_interval=77,
                                transmit_delay=100,
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=45,
                                        area=dict(area_id="0.0.0.5"),
                                    ),
                                    dict(
                                        afi="ipv6",
                                        passive_interface=True,
                                        dead_interval=56,
                                        retransmit_interval=115,
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan3",
                        address_family=[
                            dict(
                                afi="ipv6",
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        hello_interval=45,
                                        retransmit_interval=100,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospf_interfaces_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                area=dict(area_id="0.0.0.10"),
                                cost=100,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                dead_interval=44,
                                ip_params=[
                                    dict(
                                        afi="ipv6",
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    )
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan2",
                        address_family=[
                            dict(
                                afi="ipv6",
                                retransmit_interval=144,
                                authentication_v3=dict(
                                    spi=30,
                                    algorithm="md5",
                                    keytype=7,
                                    passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                ),
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=9,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        commands = [
            "interface Vlan3",
            "no ospfv3 ipv4 hello-interval 45",
            "no ospfv3 ipv4 retransmit-interval 100",
            "no ospfv3 ipv4 area 0.0.0.6",
            "interface Vlan1",
            "ip ospf area 0.0.0.10",
            "ip ospf cost 100",
            "no ip ospf dead-interval 29",
            "no ip ospf hello-interval 66",
            "ospfv3 dead-interval 44",
            "no ospfv3 ipv4 priority 45",
            "no ospfv3 ipv4 area 0.0.0.5",
            "no ospfv3 ipv6 passive-interface",
            "no ospfv3 ipv6 dead-interval 56",
            "no ospfv3 ipv6 retransmit-interval 115",
            "no ospfv3 bfd",
            "no ospfv3 cost 106",
            "no ospfv3 hello-interval 77",
            "no ospfv3 transmit-delay 100",
            "interface Vlan2",
            "ospfv3 retransmit-interval 144",
            "ospfv3 authentication ipsec spi 30 md5 passphrase 7 7hl8FV3lZ6H1mAKpjL47hQ==",
            "ospfv3 ipv4 priority 9",
            "ospfv3 ipv4 area 0.0.0.6",
        ]

        self.execute_module(changed=True, commands=commands)

    def test_eos_ospf_interfaces_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                dead_interval=29,
                                hello_interval=66,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                bfd=True,
                                cost=106,
                                hello_interval=77,
                                transmit_delay=100,
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=45,
                                        area=dict(area_id="0.0.0.5"),
                                    ),
                                    dict(
                                        afi="ipv6",
                                        passive_interface=True,
                                        dead_interval=56,
                                        retransmit_interval=115,
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan3",
                        address_family=[
                            dict(
                                afi="ipv6",
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        hello_interval=45,
                                        retransmit_interval=100,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospf_interfaces_deleted(self):
        set_module_args(dict(config=[dict(name="Vlan1")], state="deleted"))
        commands = [
            "interface Vlan1",
            "no ospfv3 bfd",
            "no ip ospf dead-interval 29",
            "no ip ospf hello-interval 66",
            "no ip ospf mtu-ignore",
            "no ospfv3 cost 106",
            "no ospfv3 hello-interval 77",
            "no ospfv3 transmit-delay 100",
            "no ospfv3 ipv4 priority 45",
            "no ospfv3 ipv4 area 0.0.0.5",
            "no ospfv3 ipv6 dead-interval 56",
            "no ospfv3 ipv6 mtu-ignore",
            "no ospfv3 ipv6 network point-to-point",
            "no ospfv3 ipv6 passive-interface",
            "no ospfv3 ipv6 retransmit-interval 115",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospf_interfaces_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Vlan1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                area=dict(area_id="0.0.0.10"),
                                cost=100,
                                mtu_ignore=True,
                            ),
                            dict(
                                afi="ipv6",
                                dead_interval=44,
                                ip_params=[
                                    dict(
                                        afi="ipv6",
                                        mtu_ignore=True,
                                        network="point-to-point",
                                    )
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Vlan2",
                        address_family=[
                            dict(
                                afi="ipv6",
                                retransmit_interval=144,
                                authentication_v3=dict(
                                    spi=30,
                                    algorithm="md5",
                                    keytype=7,
                                    passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                ),
                                ip_params=[
                                    dict(
                                        afi="ipv4",
                                        priority=9,
                                        area=dict(area_id="0.0.0.6"),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="rendered",
            )
        )
        commands = [
            "interface Vlan1",
            "ip ospf cost 100",
            "ip ospf area 0.0.0.10",
            "ospfv3 dead-interval 44",
            "ip ospf mtu-ignore",
            "ospfv3 ipv6 mtu-ignore",
            "ospfv3 ipv6 network point-to-point",
            "interface Vlan2",
            "ospfv3 retransmit-interval 144",
            "ospfv3 authentication ipsec spi 30 md5 passphrase 7 7hl8FV3lZ6H1mAKpjL47hQ==",
            "ospfv3 ipv4 priority 9",
            "ospfv3 ipv4 area 0.0.0.6",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_vyos_ospf_interfaces_parsed(self):
        commands = [
            "interface Vlan1",
            "ip ospf cost 500",
            "ip ospf mtu-ignore",
            "ip ospf area 0.0.0.10",
            "ospfv3 dead-interval 44",
            "ospfv3 ipv6 mtu-ignore",
            "ospfv3 ipv6 network point-to-point",
        ]
        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = [
            {
                "address_family": [
                    {
                        "afi": "ipv4",
                        "area": {"area_id": "0.0.0.10"},
                        "mtu_ignore": True,
                    },
                    {
                        "afi": "ipv6",
                        "ip_params": [
                            {
                                "afi": "ipv6",
                                "mtu_ignore": True,
                                "network": "point-to-point",
                            }
                        ],
                    },
                ],
                "name": "Vlan1",
            }
        ]

        self.assertEqual(parsed_list, result["parsed"])

    def test_vyos_ospf_interfaces_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(
            changed=False, filename="eos_ospf_interfaces_config.cfg"
        )
        gathered_list = {
            "Vlan1": [
                {
                    "afi": "ipv4",
                    "dead_interval": 29,
                    "hello_interval": 66,
                    "mtu_ignore": True,
                },
                {
                    "afi": "ipv6",
                    "bfd": True,
                    "cost": 106,
                    "hello_interval": 77,
                    "ip_params": [
                        {
                            "afi": "ipv4",
                            "area": {"area_id": "0.0.0.5"},
                            "priority": 45,
                        },
                        {
                            "afi": "ipv6",
                            "dead_interval": 56,
                            "mtu_ignore": True,
                            "network": "point-to-point",
                            "passive_interface": True,
                            "retransmit_interval": 115,
                        },
                    ],
                    "transmit_delay": 100,
                },
            ],
            "Vlan3": [
                {
                    "afi": "ipv6",
                    "ip_params": [
                        {
                            "afi": "ipv4",
                            "area": {"area_id": "0.0.0.6"},
                            "hello_interval": 45,
                            "retransmit_interval": 100,
                        }
                    ],
                }
            ],
        }
        for entry in result["gathered"]:
            if entry.get("name") in ["Vlan1", "Vlan3"]:
                self.assertEqual(
                    gathered_list[entry["name"]], entry["address_family"]
                )
