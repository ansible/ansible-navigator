# (c) 2020 Red Hat Inc.
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

from textwrap import dedent
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_ospf_interfaces

from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosOspfInterfacesModule(TestNxosModule):

    # Testing strategy
    # ------------------
    # (a) The unit tests cover `merged` and `replaced` for every attribute.
    #     Since `overridden` is essentially `replaced` but at a larger
    #     scale, these indirectly cover `overridden` as well.
    # (b) For linear attributes replaced is not valid and hence, those tests
    #     delete the attributes from the config subsection.

    module = nxos_ospf_interfaces

    def setUp(self):
        super(TestNxosOspfInterfacesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospf_interfaces.ospf_interfaces.Ospf_interfacesFacts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosOspfInterfacesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_ospf_interfaces_af_process_area_merged(self):
        # test merged for config->af->processes->area
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip router ospf 100 area 1.1.1.1 secondaries none
            interface Ethernet1/2
              no switchport
              ip router ospf 101 area 2.2.2.2
              ipv6 router ospfv3 100 area 4.4.4.4
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                processes=[
                                    dict(
                                        process_id="102",
                                        area=dict(area_id="1.1.1.2"),
                                    )
                                ],
                            ),
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="200",
                                        area=dict(area_id="2.2.2.8"),
                                    )
                                ],
                            ),
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                processes=[
                                    dict(
                                        process_id="101",
                                        area=dict(area_id="2.2.2.3"),
                                    )
                                ],
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="300",
                                        area=dict(
                                            area_id="2.2.2.3",
                                            secondaries="False",
                                        ),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip router ospf 102 area 1.1.1.2",
            "ipv6 router ospfv3 200 area 2.2.2.8",
            "interface Ethernet1/2",
            "ip router ospf 101 area 2.2.2.3",
            "interface Ethernet1/3",
            "ipv6 router ospfv3 300 area 2.2.2.3 secondaries none",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_af_process_area_replaced(self):
        # test replaced for config->af->processes->area
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip router ospf 100 area 1.1.1.1 secondaries none
            interface Ethernet1/2
              no switchport
              ip router ospf 101 area 2.2.2.2
              ipv6 router ospfv3 100 area 4.4.4.4
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="200",
                                        area=dict(area_id="2.2.2.8"),
                                    )
                                ],
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                processes=[
                                    dict(
                                        process_id="102",
                                        area=dict(area_id="1.1.1.2"),
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip router ospf 100 area 1.1.1.1 secondaries none",
            "ipv6 router ospfv3 200 area 2.2.2.8",
            "interface Ethernet1/2",
            "no ip router ospf 101 area 2.2.2.2",
            "ip router ospf 102 area 1.1.1.2",
            "no ipv6 router ospfv3 100 area 4.4.4.4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_af_process_multiareas_merged(self):
        # test merged for config->af->processes->multiareas
        # processes->multiareas is only valid for IPv6
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ipv6 router ospfv3 100 multi-area 1.1.1.1
              ipv6 router ospfv3 100 multi-area 1.1.1.2
              ipv6 router ospfv3 102 multi-area 2.2.2.1
              ipv6 router ospfv3 102 multi-area 2.2.2.2
            interface Ethernet1/2
              no switchport
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="100",
                                        multi_areas=["1.1.1.3"],
                                    ),
                                    dict(
                                        process_id="200",
                                        multi_areas=["3.3.3.3", "4.4.4.4"],
                                    ),
                                ],
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="109",
                                        multi_areas=["5.5.5.5", "5.5.5.6"],
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ipv6 router ospfv3 100 multi-area 1.1.1.3",
            "ipv6 router ospfv3 200 multi-area 3.3.3.3",
            "ipv6 router ospfv3 200 multi-area 4.4.4.4",
            "interface Ethernet1/2",
            "ipv6 router ospfv3 109 multi-area 5.5.5.5",
            "ipv6 router ospfv3 109 multi-area 5.5.5.6",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_af_process_multiareas_replaced(self):
        # test replaced for config->af->processes->multiareas
        # processes->multiareas is only valid for IPv6
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ipv6 router ospfv3 100 multi-area 1.1.1.1
              ipv6 router ospfv3 100 multi-area 1.1.1.2
              ipv6 router ospfv3 102 multi-area 2.2.2.1
              ipv6 router ospfv3 102 multi-area 2.2.2.2
            interface Ethernet1/2
              no switchport
              ipv6 router ospfv3 109 multi-area 5.5.5.5
              ipv6 router ospfv3 200 multi-area 4.2.2.1
              ipv6 router ospfv3 200 multi-area 4.2.2.2
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="100",
                                        multi_areas=["1.1.1.3"],
                                    ),
                                    dict(
                                        process_id="102",
                                        multi_areas=["2.2.2.2"],
                                    ),
                                    dict(
                                        process_id="200",
                                        multi_areas=["3.3.3.3", "4.4.4.4"],
                                    ),
                                ],
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv6",
                                processes=[
                                    dict(
                                        process_id="109",
                                        multi_areas=["5.5.5.6"],
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ipv6 router ospfv3 100 multi-area 1.1.1.1",
            "no ipv6 router ospfv3 100 multi-area 1.1.1.2",
            "no ipv6 router ospfv3 102 multi-area 2.2.2.1",
            "ipv6 router ospfv3 100 multi-area 1.1.1.3",
            "ipv6 router ospfv3 200 multi-area 3.3.3.3",
            "ipv6 router ospfv3 200 multi-area 4.4.4.4",
            "interface Ethernet1/2",
            "no ipv6 router ospfv3 109 multi-area 5.5.5.5",
            "no ipv6 router ospfv3 200 multi-area 4.2.2.1",
            "no ipv6 router ospfv3 200 multi-area 4.2.2.2",
            "ipv6 router ospfv3 109 multi-area 5.5.5.6",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_af_multiareas_merged(self):
        # test merged for config->af->multiareas
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip router ospf multi-area 1.1.1.1
              ip router ospf multi-area 1.1.1.2
              ipv6 router ospfv3 multi-area 2.2.2.1
              ipv6 router ospfv3 multi-area 2.2.2.2
            interface Ethernet1/2
              no switchport
              ipv6 router ospfv3 multi-area 5.5.5.5
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4", multi_areas=["1.1.1.1", "1.1.1.3"]
                            ),
                            dict(
                                afi="ipv6", multi_areas=["3.3.3.3", "4.4.4.4"]
                            ),
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(afi="ipv6", multi_areas=["5.5.5.6"])
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip router ospf multi-area 1.1.1.3",
            "ipv6 router ospfv3 multi-area 3.3.3.3",
            "ipv6 router ospfv3 multi-area 4.4.4.4",
            "interface Ethernet1/2",
            "ipv6 router ospfv3 multi-area 5.5.5.6",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_af_multiareas_replaced(self):
        # test replaced for config->af->multiareas
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip router ospf multi-area 1.1.1.1
              ip router ospf multi-area 1.1.1.2
              ipv6 router ospfv3 multi-area 2.2.2.1
              ipv6 router ospfv3 multi-area 2.2.2.2
            interface Ethernet1/2
              no switchport
              ipv6 router ospfv3 multi-area 5.5.5.5
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4", multi_areas=["1.1.1.1", "1.1.1.3"]
                            ),
                            dict(
                                afi="ipv6", multi_areas=["3.3.3.3", "4.4.4.4"]
                            ),
                        ],
                    ),
                    dict(name="Ethernet1/2"),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip router ospf multi-area 1.1.1.2",
            "no ipv6 router ospfv3 multi-area 2.2.2.1",
            "no ipv6 router ospfv3 multi-area 2.2.2.2",
            "ip router ospf multi-area 1.1.1.3",
            "ipv6 router ospfv3 multi-area 3.3.3.3",
            "ipv6 router ospfv3 multi-area 4.4.4.4",
            "interface Ethernet1/2",
            "no ipv6 router ospfv3 multi-area 5.5.5.5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_authentication_merged(self):
        # test merged for config->af->authentication
        # only valid for IPv4
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf authentication
            interface Ethernet1/2
              no switchport
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
              ip ospf authentication
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                authentication=dict(
                                    key_chain="test-1", message_digest=True
                                ),
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4", authentication=dict(null_auth=True)
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(afi="ipv4", authentication=dict(enable=True))
                        ],
                    ),
                    dict(
                        name="Ethernet1/4",
                        address_family=[
                            dict(afi="ipv4", authentication=dict(enable=False))
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf authentication message-digest",
            "ip ospf authentication key-chain test-1",
            "interface Ethernet1/2",
            "ip ospf authentication null",
            "interface Ethernet1/3",
            "ip ospf authentication",
            "interface Ethernet1/4",
            "no ip ospf authentication",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_authentication_replaced(self):
        # test merged for config->af->authentication
        # only valid for IPv4
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf authentication message-digest
              ip ospf authentication key-chain test-1
            interface Ethernet1/2
              no switchport
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(name="Ethernet1/1"),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4", authentication=dict(null_auth=True)
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(afi="ipv4", authentication=dict(enable=True))
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf authentication message-digest",
            "no ip ospf authentication key-chain test-1",
            "interface Ethernet1/2",
            "ip ospf authentication null",
            "interface Ethernet1/3",
            "ip ospf authentication",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_authentication_key_merged(self):
        # test merged for config->af->authentication_key
        # only valid for IPv4
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf authentication-key 3 abc01d272be25d29
            interface Ethernet1/2
              no switchport
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                authentication_key=dict(
                                    encryption=3, key="77840f9d4d882176"
                                ),
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                authentication_key=dict(
                                    encryption=0, key="password"
                                ),
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                authentication_key=dict(
                                    encryption=7, key="712090404011C031628"
                                ),
                            )
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf authentication-key 3 77840f9d4d882176",
            "interface Ethernet1/2",
            "ip ospf authentication-key 0 password",
            "interface Ethernet1/3",
            "ip ospf authentication-key 7 712090404011C031628",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_authentication_key_replaced(self):
        # test replaced for config->af->authentication_key
        # only valid for IPv4
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf authentication-key 3 abc01d272be25d29
            interface Ethernet1/2
              no switchport
            interface Ethernet1/3
              no switchport
              ip ospf authentication-key 7 712090404011C031628
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(name="Ethernet1/1"),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                authentication_key=dict(
                                    encryption=0, key="password"
                                ),
                            )
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf authentication-key 3 abc01d272be25d29",
            "interface Ethernet1/2",
            "ip ospf authentication-key 0 password",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_message_digest_key_merged(self):
        # test merged for config->af->message_digest_key
        # only valid for IPv4
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d
            interface Ethernet1/2
              no switchport
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                message_digest_key=dict(
                                    key_id=101,
                                    encryption=3,
                                    key="abc01d272be25d29",
                                ),
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                message_digest_key=dict(
                                    key_id=1, encryption=0, key="password"
                                ),
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                message_digest_key=dict(
                                    key_id=2,
                                    encryption=7,
                                    key="712090404011C031628",
                                ),
                            )
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf message-digest-key 101 md5 3 abc01d272be25d29",
            "interface Ethernet1/2",
            "ip ospf message-digest-key 1 md5 0 password",
            "interface Ethernet1/3",
            "ip ospf message-digest-key 2 md5 7 712090404011C031628",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_message_digest_key_replaced(self):
        # test replaced for config->af->message_digest_key
        # only valid for IPv4
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d
            interface Ethernet1/2
              no switchport
              ip ospf message-digest-key 1 md5 0 password
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(name="Ethernet1/1"),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                message_digest_key=dict(
                                    key_id=1, encryption=0, key="password1"
                                ),
                            )
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d",
            "interface Ethernet1/2",
            "ip ospf message-digest-key 1 md5 0 password1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_1_merged(self):
        # test merged for config->af->cost, dead_interval, hello_interval
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf cost 100
              ospfv3 cost 120
              ip ospf dead-interval 2400
              ospfv3 dead-interval 1200
              ip ospf hello-interval 9000
            interface Ethernet1/2
              no switchport
              ip ospf cost 110
              ip ospf dead-interval 3000
              ospfv3 hello-interval 8000
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(afi="ipv4", cost=200),
                            dict(
                                afi="ipv6",
                                dead_interval=5000,
                                hello_interval=9000,
                            ),
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                cost=120,
                                dead_interval=3400,
                                hello_interval=8100,
                            ),
                            dict(afi="ipv6", cost=180, dead_interval=3000),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf cost 200",
            "ospfv3 dead-interval 5000",
            "ospfv3 hello-interval 9000",
            "interface Ethernet1/2",
            "ip ospf cost 120",
            "ip ospf dead-interval 3400",
            "ospfv3 cost 180",
            "ospfv3 dead-interval 3000",
            "ip ospf hello-interval 8100",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_1_replaced(self):
        # test replaced for config->af->cost, dead_interval, hello_interval
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf cost 100
              ospfv3 cost 120
              ip ospf dead-interval 2400
              ospfv3 dead-interval 1200
              ip ospf hello-interval 9000
            interface Ethernet1/2
              no switchport
              ip ospf cost 110
              ip ospf dead-interval 3000
              ospfv3 hello-interval 8000
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(afi="ipv4", cost=200, hello_interval=9000)
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(afi="ipv6", cost=180, dead_interval=3000)
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf cost 200",
            "no ospfv3 cost 120",
            "no ip ospf dead-interval 2400",
            "no ospfv3 dead-interval 1200",
            "interface Ethernet1/2",
            "no ip ospf cost 110",
            "no ip ospf dead-interval 3000",
            "no ospfv3 hello-interval 8000",
            "ospfv3 cost 180",
            "ospfv3 dead-interval 3000",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_2_merged(self):
        # test merged for config->af->instance, mtu_ignore, network
        # `instance` is only valid for IPv6
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ospfv3 instance 200
            interface Ethernet1/2
              no switchport
              ip ospf mtu-ignore
              ip ospf network broadcast
              ospfv3 network point-to-point
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                mtu_ignore=True,
                                network="point-to-point",
                            ),
                            dict(afi="ipv6", instance=210),
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(afi="ipv4", mtu_ignore=False),
                            dict(afi="ipv6", network="broadcast"),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf mtu-ignore",
            "ip ospf network point-to-point",
            "ospfv3 instance 210",
            "interface Ethernet1/2",
            "no ip ospf mtu-ignore",
            "ospfv3 network broadcast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_2_replaced(self):
        # test replaced for config->af->instance, mtu_ignore, network
        # `instance` is only valid for IPv6
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf mtu-ignore
              ospfv3 instance 200
            interface Ethernet1/2
              no switchport
              ip ospf mtu-ignore
              ip ospf network broadcast
              ospfv3 network point-to-point
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                mtu_ignore=False,
                                network="point-to-point",
                            ),
                            dict(afi="ipv6", instance=200),
                        ],
                    ),
                    dict(name="Ethernet1/2"),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf mtu-ignore",
            "ip ospf network point-to-point",
            "interface Ethernet1/2",
            "no ip ospf mtu-ignore",
            "no ip ospf network broadcast",
            "no ospfv3 network point-to-point",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_3_merged(self):
        # test merged for config->af->passive_interface, priority, retransmit_interval
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf passive-interface
              ip ospf priority 120
              ospfv3 retransmit-interval 4800
            interface Ethernet1/2
              no switchport
              ip ospf retransmit-interval 5000
              ospfv3 passive-interface
              ospfv3 priority 140
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4",
                                passive_interface=False,
                                retransmit_interval=8000,
                            ),
                            dict(afi="ipv6", passive_interface=True),
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(
                                afi="ipv4",
                                passive_interface=True,
                                retransmit_interval=5000,
                            )
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(
                                afi="ipv4",
                                passive_interface=True,
                                priority=200,
                            ),
                            dict(afi="ipv6", retransmit_interval=5100),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf passive-interface",
            "ospfv3 passive-interface",
            "ip ospf retransmit-interval 8000",
            "interface Ethernet1/2",
            "ip ospf passive-interface",
            "interface Ethernet1/3",
            "ip ospf passive-interface",
            "ip ospf priority 200",
            "ospfv3 retransmit-interval 5100",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_3_replaced(self):
        # test merged for config->af->passive_interface, priority, retransmit_interval
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf passive-interface
              ip ospf priority 120
              ospfv3 retransmit-interval 4800
            interface Ethernet1/2
              no switchport
              ip ospf retransmit-interval 5000
              ospfv3 passive-interface
              ospfv3 priority 140
            interface Ethernet1/3
              no switchport
              ip ospf passive-interface
              ip ospf priority 200
              ospfv3 retransmit-interval 5100
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(name="Ethernet1/1"),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(afi="ipv4", retransmit_interval=5100),
                            dict(
                                afi="ipv6",
                                passive_interface=True,
                                priority=140,
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf passive-interface",
            "no ip ospf priority 120",
            "no ospfv3 retransmit-interval 4800",
            "interface Ethernet1/2",
            "ip ospf retransmit-interval 5100",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_4_merged(self):
        # test merged for config->af->shutdown, transmit_delay
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf shutdown
              ospfv3 transmit-delay 200
            interface Ethernet1/2
              no switchport
              ip ospf transmit-delay 210
              ospfv3 shutdown
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4", shutdown=False, transmit_delay=210
                            ),
                            dict(afi="ipv6", shutdown=True),
                        ],
                    ),
                    dict(
                        name="Ethernet1/2",
                        address_family=[
                            dict(afi="ipv4", shutdown=True),
                            dict(afi="ipv6", transmit_delay=300),
                        ],
                    ),
                    dict(
                        name="Ethernet1/3",
                        address_family=[
                            dict(
                                afi="ipv4", shutdown=True, transmit_delay=430
                            ),
                            dict(
                                afi="ipv6", shutdown=True, transmit_delay=120
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf shutdown",
            "ip ospf transmit-delay 210",
            "ospfv3 shutdown",
            "interface Ethernet1/2",
            "ip ospf shutdown",
            "ospfv3 transmit-delay 300",
            "interface Ethernet1/3",
            "ip ospf shutdown",
            "ip ospf transmit-delay 430",
            "ospfv3 shutdown",
            "ospfv3 transmit-delay 120",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_linear_args_4_replaced(self):
        # test replaced for config->af->shutdown, transmit_delay
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf shutdown
              ospfv3 transmit-delay 200
            interface Ethernet1/2
              no switchport
              ip ospf transmit-delay 210
              ospfv3 shutdown
            interface Ethernet1/3
              no switchport
              ip ospf shutdown
              ip ospf transmit-delay 430
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(name="Ethernet1/1"),
                    dict(
                        name="Ethernet1/2",
                        address_family=[dict(afi="ipv6", transmit_delay=300)],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf shutdown",
            "no ospfv3 transmit-delay 200",
            "interface Ethernet1/2",
            "no ospfv3 shutdown",
            "no ip ospf transmit-delay 210",
            "ospfv3 transmit-delay 300",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_parsed(self):
        # test parsed
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface Ethernet1/1
                      no switchport
                      ip router ospf 102 area 1.1.1.2 secondaries none
                      ipv6 router ospfv3 200 area 2.2.2.8
                    interface Ethernet1/2
                      no switchport
                      ipv6 router ospfv3 210 multi-area 3.3.3.3
                    interface Ethernet1/3
                      no switchport
                    interface Ethernet1/4
                      no switchport
                    """
                ),
                state="parsed",
            ),
            ignore_provider_arg,
        )
        parsed = [
            {
                "name": "Ethernet1/1",
                "address_family": [
                    {
                        "afi": "ipv4",
                        "processes": [
                            {
                                "process_id": "102",
                                "area": {
                                    "area_id": "1.1.1.2",
                                    "secondaries": False,
                                },
                            }
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "processes": [
                            {
                                "process_id": "200",
                                "area": {"area_id": "2.2.2.8"},
                            }
                        ],
                    },
                ],
            },
            {
                "name": "Ethernet1/2",
                "address_family": [
                    {
                        "afi": "ipv6",
                        "processes": [
                            {"process_id": "210", "multi_areas": ["3.3.3.3"]}
                        ],
                    }
                ],
            },
            {"name": "Ethernet1/3"},
            {"name": "Ethernet1/4"},
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_ospf_interfaces_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip router ospf 102 area 1.1.1.2 secondaries none
              ipv6 router ospfv3 200 area 2.2.2.8
            interface Ethernet1/2
              no switchport
              ipv6 router ospfv3 210 multi-area 3.3.3.3
            interface Ethernet1/3
              no switchport
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = [
            {
                "name": "Ethernet1/1",
                "address_family": [
                    {
                        "afi": "ipv4",
                        "processes": [
                            {
                                "process_id": "102",
                                "area": {
                                    "area_id": "1.1.1.2",
                                    "secondaries": False,
                                },
                            }
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "processes": [
                            {
                                "process_id": "200",
                                "area": {"area_id": "2.2.2.8"},
                            }
                        ],
                    },
                ],
            },
            {
                "name": "Ethernet1/2",
                "address_family": [
                    {
                        "afi": "ipv6",
                        "processes": [
                            {"process_id": "210", "multi_areas": ["3.3.3.3"]}
                        ],
                    }
                ],
            },
            {"name": "Ethernet1/3"},
            {"name": "Ethernet1/4"},
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_ospf_interfaces_sanity(self):
        # test gathered
        self.get_config.return_value = dedent(
            """
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = []
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_ospf_interfaces_overridden(self):
        # test overriden
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf shutdown
              ospfv3 transmit-delay 200
            interface Ethernet1/2
              no switchport
              ip ospf transmit-delay 210
              ospfv3 shutdown
            interface Ethernet1/3
              no switchport
              ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        address_family=[
                            dict(
                                afi="ipv4", shutdown=False, transmit_delay=300
                            ),
                            dict(afi="ipv6", shutdown=True),
                        ],
                    )
                ],
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "ip ospf transmit-delay 300",
            "no ip ospf shutdown",
            "no ospfv3 transmit-delay 200",
            "ospfv3 shutdown",
            "interface Ethernet1/2",
            "no ip ospf transmit-delay 210",
            "no ospfv3 shutdown",
            "interface Ethernet1/3",
            "no ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_deleted(self):
        # test deleted
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf shutdown
              ospfv3 transmit-delay 200
            interface Ethernet1/2
              no switchport
              ip ospf transmit-delay 210
              ospfv3 shutdown
            interface Ethernet1/3
              no switchport
              ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(
            dict(config=[dict(name="Ethernet1/1")], state="deleted"),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "no ip ospf shutdown",
            "no ospfv3 transmit-delay 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospf_interfaces_deleted_all(self):
        # test deleted
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/1
              no switchport
              ip ospf shutdown
              ospfv3 transmit-delay 200
            interface Ethernet1/2
              no switchport
              ip ospf transmit-delay 210
              ospfv3 shutdown
            interface Ethernet1/3
              no switchport
              ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d
            interface Ethernet1/4
              no switchport
            """
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "interface Ethernet1/1",
            "no ip ospf shutdown",
            "no ospfv3 transmit-delay 200",
            "interface Ethernet1/2",
            "no ip ospf transmit-delay 210",
            "no ospfv3 shutdown",
            "interface Ethernet1/3",
            "no ip ospf message-digest-key 101 md5 3 109a86e9d947cc5d",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
