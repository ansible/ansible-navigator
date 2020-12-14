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
from ansible_collections.cisco.nxos.plugins.modules import nxos_ospfv3

from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosOspfv3Module(TestNxosModule):

    # Testing strategy
    # ------------------
    # (a) The unit tests cover `merged` and `replaced` for every attribute.
    #     Since `overridden` is essentially `replaced` but at a larger
    #     scale, these indirectly cover `overridden` as well.
    # (b) For linear attributes replaced is not valid and hence, those tests
    #     delete the attributes from the config subsection.
    # (c) The argspec for VRFs is same as the top-level spec and the config logic
    #     is re-used. Hence, those attributes are not explictly covered. However, a
    #     combination of VRF + top-level spec + AF is tested.

    module = nxos_ospfv3

    def setUp(self):
        super(TestNxosOspfv3Module, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospfv3.ospfv3.Ospfv3Facts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosOspfv3Module, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_ospfv3_af_areas_filter_list_merged(self):
        # test merged for config->processes->af->areas->filter_list
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 default-cost 100
                area 1.1.1.1 filter-list route-map test-11 in
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.1",
                                        filter_list=[
                                            dict(
                                                route_map="test-1",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-2",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                    dict(
                                        area_id="1.1.1.2",
                                        filter_list=[
                                            dict(
                                                route_map="test-3",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-4",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "area 1.1.1.1 filter-list route-map test-1 in",
            "area 1.1.1.1 filter-list route-map test-2 out",
            "area 1.1.1.2 filter-list route-map test-3 in",
            "area 1.1.1.2 filter-list route-map test-4 out",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_filter_list_replaced(self):
        # test replaced for config->processes->af->areas->filter_list
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.4 filter-list route-map test-11 out
                area 1.1.1.4 filter-list route-map test-12 in
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.1",
                                        filter_list=[
                                            dict(
                                                route_map="test-1",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-2",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                    dict(
                                        area_id="1.1.1.2",
                                        filter_list=[
                                            dict(
                                                route_map="test-3",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-4",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no area 1.1.1.4 filter-list route-map test-11 out",
            "no area 1.1.1.4 filter-list route-map test-12 in",
            "area 1.1.1.1 filter-list route-map test-1 in",
            "area 1.1.1.1 filter-list route-map test-2 out",
            "area 1.1.1.2 filter-list route-map test-3 in",
            "area 1.1.1.2 filter-list route-map test-4 out",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_ranges_merged(self):
        # test merged for config->processes->af->areas->rang
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 range 2001:db2::/32
                area 1.1.1.1 range 2001:db3::/32 cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.1",
                                        ranges=[
                                            dict(
                                                prefix="2001:db3::/32",
                                                cost="20",
                                            )
                                        ],
                                    ),
                                    dict(
                                        area_id="1.1.1.2",
                                        ranges=[
                                            dict(
                                                prefix="2001:db4::/32", cost=11
                                            ),
                                            dict(
                                                prefix="2001:db5::/32",
                                                not_advertise=True,
                                            ),
                                            dict(
                                                prefix="2001:db7::/32",
                                                not_advertise=True,
                                                cost=18,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "area 1.1.1.1 range 2001:db3::/32 cost 20",
            "area 1.1.1.2 range 2001:db4::/32 cost 11",
            "area 1.1.1.2 range 2001:db5::/32 not-advertise",
            "area 1.1.1.2 range 2001:db7::/32 not-advertise cost 18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_ranges_replaced(self):
        # test replaced for config->processes->af->areas->ranges
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 range 2001:db2::/32
                area 1.1.1.1 range 2001:db3::/32 cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.2",
                                        ranges=[
                                            dict(
                                                prefix="2001:db4::/32", cost=11
                                            ),
                                            dict(
                                                prefix="2001:db5::/32",
                                                not_advertise=True,
                                            ),
                                            dict(
                                                prefix="2001:db7::/32",
                                                not_advertise=True,
                                                cost=18,
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no area 1.1.1.1 range 2001:db2::/32",
            "no area 1.1.1.1 range 2001:db3::/32",
            "area 1.1.1.2 range 2001:db4::/32 cost 11",
            "area 1.1.1.2 range 2001:db5::/32 not-advertise",
            "area 1.1.1.2 range 2001:db7::/32 not-advertise cost 18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_default_cost_merged(self):
        # test merged for config->processes->af->areas->default_cost
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 default-cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(area_id="1.1.1.1", default_cost=12),
                                    dict(area_id="1.1.1.2", default_cost=200),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "area 1.1.1.1 default-cost 12",
            "area 1.1.1.2 default-cost 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_default_cost_replaced(self):
        # test merged for config->processes->af->areas->default_cost
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 default-cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(area_id="1.1.1.2", default_cost=200)
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no area 1.1.1.1 default-cost 10",
            "area 1.1.1.2 default-cost 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_default_information_merged(self):
        # test merged for config->processes->af->default_information
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                default-information originate
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                default_information=dict(
                                    originate=dict(
                                        always=True, route_map="test-2"
                                    )
                                ),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "default-information originate always route-map test-2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_default_information_merged_2(self):
        # test merged for config->processes->af->default_information->set
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                default-information originate always route-map test-2
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                default_information=dict(
                                    originate=dict(set=False)
                                ),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no default-information originate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_default_information_replaced(self):
        # test replaced for config->processes->af->default_information
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                default-information originate always test-2
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                default_information=dict(
                                    originate=dict(set=True)
                                ),
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "default-information originate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_distance_merged(self):
        # test merged for config->processes->af->distance
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                distance 20
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6", safi="unicast", distance=35
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "distance 35",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_distance_replaced(self):
        # test replaced for config->processes->af->distance
        # `distance` is a linear attribute so replaced test
        # can only be removal of this attribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                distance 20
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(afi="ipv6", safi="unicast"),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no distance 20",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_maximum_paths_merged(self):
        # test merged for config->processes->af->maximum_paths
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                maximum-paths 18
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6", safi="unicast", maximum_paths=27
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "maximum-paths 27",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_maximum_paths_replaced(self):
        # test replaced for config->processes->af->maximum_paths
        # `maximum_paths` is a linear attribute so replaced test
        # can only be removal of this attribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                maximum-paths 18
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(afi="ipv6", safi="unicast"),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no maximum-paths 18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_redistribute_merged(self):
        # test merged for config->processes->af->redistribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                redistribute eigrp 100 route-map test-17
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                redistribute=[
                                    dict(
                                        protocol="eigrp",
                                        id="100",
                                        route_map="test-1",
                                    ),
                                    dict(
                                        protocol="eigrp",
                                        id="101",
                                        route_map="test-2",
                                    ),
                                    dict(
                                        protocol="bgp",
                                        id="65563",
                                        route_map="test-3",
                                    ),
                                    dict(
                                        protocol="static", route_map="test-4"
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "redistribute eigrp 100 route-map test-1",
            "redistribute eigrp 101 route-map test-2",
            "redistribute bgp 65563 route-map test-3",
            "redistribute static route-map test-4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_redistribute_replaced(self):
        # test replaced for config->processes->af->redistribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                redistribute eigrp 100 route-map test-1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                redistribute=[
                                    dict(
                                        protocol="eigrp",
                                        id="101",
                                        route_map="test-2",
                                    ),
                                    dict(
                                        protocol="bgp",
                                        id="65563",
                                        route_map="test-3",
                                    ),
                                    dict(
                                        protocol="static", route_map="test-4"
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no redistribute eigrp 100 route-map test-1",
            "redistribute eigrp 101 route-map test-2",
            "redistribute bgp 65563 route-map test-3",
            "redistribute static route-map test-4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_summary_address_merged(self):
        # test merged for config->processes->af->summary_address
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                summary-address 2001:db2::/32
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                summary_address=[
                                    dict(prefix="2001:db2::/32", tag=19),
                                    dict(
                                        prefix="2001:db3::/32",
                                        not_advertise=True,
                                    ),
                                    dict(prefix="2001:db4::/32"),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "summary-address 2001:db2::/32 tag 19",
            "summary-address 2001:db3::/32 not-advertise",
            "summary-address 2001:db4::/32",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_summary_address_replaced(self):
        # test replaced for config->processes->af->summary_address
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                summary-address 2001:db2::/32 tag 19
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                summary_address=[
                                    dict(
                                        prefix="2001:db3::/32",
                                        not_advertise=True,
                                    )
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no summary-address 2001:db2::/32 tag 19",
            "summary-address 2001:db3::/32 not-advertise",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_table_map_merged(self):
        # test merged for config->processes->af->table_map
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                summary-address 2001:db2::/32 tag 19
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                table_map=dict(name="test-1", filter=True),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "table-map test-1 filter",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_table_map_replaced(self):
        # test replaced for config->processes->af->table_map
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map test-1 filter
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                table_map=dict(name="test-2"),
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "table-map test-2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_timers_merged(self):
        # test merged for config->processes->af->timers
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                timers throttle spf 1000 20 2800
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                timers=dict(
                                    throttle=dict(
                                        spf=dict(
                                            initial_spf_delay=1100,
                                            max_wait_time=2805,
                                        )
                                    )
                                ),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "timers throttle spf 1100 20 2805",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_timers_replaced(self):
        # test replaced for config->processes->af->timers
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                timers throttle spf 1000 20 2800
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(afi="ipv6", safi="unicast"),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no timers throttle spf 1000 20 2800",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_areas_nssa_merged(self):
        # test merged for config->processes->areas->nssa
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              area 1.1.1.1 nssa no-redistribution default-information-originate
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            areas=[
                                dict(
                                    area_id="1.1.1.1",
                                    nssa=dict(no_summary=True),
                                ),
                                dict(area_id="1.1.1.2", nssa=dict(set=True)),
                                dict(
                                    area_id="1.1.1.3",
                                    nssa=dict(
                                        default_information_originate=True,
                                        no_summary=True,
                                        no_redistribution=True,
                                        route_map="test-1",
                                        translate=dict(
                                            type7=dict(
                                                always=True, supress_fa=True
                                            )
                                        ),
                                    ),
                                ),
                            ],
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "area 1.1.1.1 nssa no-summary no-redistribution default-information-originate",
            "area 1.1.1.2 nssa",
            "area 1.1.1.3 nssa translate type7 always supress-fa",
            "area 1.1.1.3 nssa no-summary no-redistribution default-information-originate route-map test-1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_areas_nssa_merged_2(self):
        # test merged for config->processes->areas->nssa->set
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              area 1.1.1.1 nssa no-summary
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            areas=[
                                dict(area_id="1.1.1.1", nssa=dict(set=False))
                            ],
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = ["router ospfv3 100", "no area 1.1.1.1 nssa"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_areas_nssa_replaced(self):
        # test replaced for config->processes->areas->nssa
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              area 1.1.1.1 nssa no-summary no-redistribution default-information-originate
              area 1.1.1.3 nssa translate type7 always supress-fa
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            areas=[
                                dict(
                                    area_id="1.1.1.3",
                                    nssa=dict(
                                        default_information_originate=True,
                                        no_summary=True,
                                        no_redistribution=True,
                                        route_map="test-1",
                                    ),
                                )
                            ],
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "no area 1.1.1.1 nssa",
            "no area 1.1.1.3 nssa translate type7 always supress-fa",
            "area 1.1.1.3 nssa no-summary no-redistribution default-information-originate route-map test-1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_areas_stub_merged(self):
        # test merged for config->processes->areas->stub
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              area 1.1.1.3 stub
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            areas=[
                                dict(
                                    area_id="1.1.1.3",
                                    stub=dict(no_summary=True),
                                )
                            ],
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = ["router ospfv3 100", "area 1.1.1.3 stub no-summary"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_areas_stub_merged_2(self):
        # test merged for config->processes->areas->stub->set
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              area 1.1.1.3 stub
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            areas=[
                                dict(area_id="1.1.1.3", stub=dict(set=False)),
                                dict(
                                    area_id="1.1.1.4",
                                    stub=dict(no_summary=True),
                                ),
                            ],
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "no area 1.1.1.3 stub",
            "area 1.1.1.4 stub no-summary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_areas_stub_replaced(self):
        # test replaced for config->processes->areas->stub
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              area 1.1.1.3 stub no-summary
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(process_id="100", areas=[dict(area_id="1.1.1.3")])
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = ["router ospfv3 100", "no area 1.1.1.3 stub"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_autocost_flush_route_isolate_merged(self):
        # test merged for config->processes->autocost,flush_routes, isolate
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              auto-cost reference-bandwidth 300 Mbps
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            auto_cost=dict(
                                reference_bandwidth=100, unit="Gbps"
                            ),
                            flush_routes=True,
                            isolate=True,
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "auto-cost reference-bandwidth 100 Gbps",
            "flush-routes",
            "isolate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_autocost_flush_route_isolate_replaced(self):
        # test merged for config->processes->autocost,flush_routes, isolate
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              auto-cost reference-bandwidth 300 Mbps
              flush-routes
            """
        )
        set_module_args(
            dict(
                config=dict(processes=[dict(process_id="100", isolate=True)]),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "no auto-cost reference-bandwidth 300 Mbps",
            "no flush-routes",
            "isolate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_log_adjacency_changes_name_lookup_passive_interface_merged(
        self
    ):
        # test merged for config->processes->log_adjacency_changes, name_lookup, passive_interface
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              log-adjacency-changes
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            log_adjacency_changes=dict(detail=True),
                            name_lookup=True,
                            passive_interface=dict(default=True),
                        ),
                        dict(
                            process_id="102",
                            log_adjacency_changes=dict(log=True),
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "log-adjacency-changes detail",
            "name-lookup",
            "passive-interface default",
            "router ospfv3 102",
            "log-adjacency-changes",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_log_adjacency_changes_name_lookup_passive_interface_replaced(
        self
    ):
        # test replaced for config->processes->log_adjacency_changes, name_lookup, passive_interface
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              log-adjacency-changes detail
              name-lookup
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            passive_interface=dict(default=True),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "no log-adjacency-changes detail",
            "no name-lookup",
            "passive-interface default",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_max_lsa_router_id_merged(self):
        # test merged for config->processes->max_lsa, router_id
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              router-id 192.168.1.100
              max-lsa 4200 85 ignore-count 10 reset-time 120
            router ospfv3 102
              max-lsa 4200 85 ignore-time 120 ignore-count 12 reset-time 300
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="192.168.1.100",
                            max_lsa=dict(
                                max_non_self_generated_lsa=4200,
                                threshold=85,
                                ignore_count=100,
                                reset_time=138,
                            ),
                        ),
                        dict(
                            process_id="102",
                            router_id="192.168.2.102",
                            max_lsa=dict(
                                max_non_self_generated_lsa=4200,
                                threshold=85,
                                ignore_time=200,
                                ignore_count=20,
                                reset_time=120,
                            ),
                        ),
                        dict(
                            process_id="103",
                            max_lsa=dict(
                                max_non_self_generated_lsa=4200,
                                warning_only=True,
                            ),
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "max-lsa 4200 85 ignore-count 100 reset-time 138",
            "router ospfv3 102",
            "router-id 192.168.2.102",
            "max-lsa 4200 85 ignore-time 200 ignore-count 20 reset-time 120",
            "router ospfv3 103",
            "max-lsa 4200 warning-only",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_max_lsa_router_id_replaced(self):
        # test replaced for config->processes->max_lsa, router_id
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              router-id 192.168.1.100
              max-lsa 4200 85 ignore-count 10 reset-time 120
            router ospfv3 102
              max-lsa 4200 85 ignore-time 120 ignore-count 12 reset-time 300
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            max_lsa=dict(
                                max_non_self_generated_lsa=4200,
                                threshold=85,
                                warning_only=True,
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "no router-id 192.168.1.100",
            "max-lsa 4200 85 warning-only",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_graceful_restart_merged(self):
        # test merged for config->processes->graceful_restart
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              no graceful-restart
            router ospfv3 102
              no graceful-restart planned-only
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            graceful_restart=dict(
                                grace_period=50, helper_disable=True
                            ),
                        ),
                        dict(
                            process_id="102",
                            graceful_restart=dict(planned_only=True),
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "graceful-restart grace-period 50",
            "graceful-restart helper-disable",
            "router ospfv3 102",
            "graceful-restart planned-only",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_graceful_restart_replaced(self):
        # test replaced for config->processes->graceful_restart
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              graceful-restart grace-period 50
              graceful-restart helper-disable
            router ospfv3 102
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            graceful_restart=dict(grace_period=10),
                        ),
                        dict(
                            process_id="102",
                            graceful_restart=dict(helper_disable=True),
                        ),
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "graceful-restart grace-period 10",
            "no graceful-restart helper-disable",
            "router ospfv3 102",
            "graceful-restart helper-disable",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_max_metric_merged(self):
        # test merged for config->processes->max_metric
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              max-metric router-lsa external-lsa 1900
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            max_metric=dict(
                                router_lsa=dict(
                                    external_lsa=dict(max_metric_value=2000),
                                    stub_prefix_lsa=True,
                                    on_startup=dict(set=True),
                                )
                            ),
                        ),
                        dict(
                            process_id="102",
                            max_metric=dict(
                                router_lsa=dict(
                                    inter_area_prefix_lsa=dict(
                                        max_metric_value=1800
                                    )
                                )
                            ),
                        ),
                        dict(
                            process_id="103",
                            max_metric=dict(
                                router_lsa=dict(
                                    on_startup=dict(
                                        wait_period=1200,
                                        wait_for_bgp_asn=65563,
                                    ),
                                    inter_area_prefix_lsa=dict(set=True),
                                )
                            ),
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "max-metric router-lsa external-lsa 2000 stub-prefix-lsa on-startup",
            "router ospfv3 102",
            "max-metric router-lsa inter-area-prefix-lsa 1800",
            "router ospfv3 103",
            "max-metric router-lsa on-startup 1200 wait-for bgp 65563 inter-area-prefix-lsa",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_max_metric_merged_2(self):
        # test merged for config->processes->max_metric->set
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              max-metric router-lsa inter-area-prefix-lsa 1800
            router ospfv3 103
              max-metric router-lsa on-startup 1200 wait-for bgp 65563 inter-area-prefix-lsa
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            max_metric=dict(router_lsa=dict(set=False)),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = ["router ospfv3 100", "no max-metric router-lsa"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_max_metric_replaced(self):
        # test replaced for config->processes->max_metric
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
            router ospfv3 102
              max-metric router-lsa inter-area-prefix-lsa 1800
            router ospfv3 103
              max-metric router-lsa on-startup 1200 wait-for bgp 65563 inter-area-prefix-lsa
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            max_metric=dict(
                                router_lsa=dict(
                                    external_lsa=dict(max_metric_value=2000),
                                    stub_prefix_lsa=True,
                                    on_startup=dict(set=True),
                                )
                            ),
                        ),
                        dict(process_id="102"),
                        dict(process_id="103"),
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "max-metric router-lsa external-lsa 2000 stub-prefix-lsa on-startup",
            "router ospfv3 102",
            "no max-metric router-lsa",
            "router ospfv3 103",
            "no max-metric router-lsa",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_timers_shutdown_merged(self):
        # test merged for config->processes->timers, shutdown
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              timers lsa-group-pacing 190
              shutdown
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            timers=dict(
                                lsa_arrival=1200,
                                lsa_group_pacing=210,
                                throttle=dict(
                                    lsa=dict(
                                        start_interval=100,
                                        hold_interval=70,
                                        max_interval=1500,
                                    )
                                ),
                            ),
                            shutdown=False,
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "timers lsa-arrival 1200",
            "timers lsa-group-pacing 210",
            "timers throttle lsa 100 70 1500",
            "no shutdown",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_timers_shutdown_replaced(self):
        # test replaced for config->processes->timers, shutdown
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              timers lsa-arrival 800
              timers lsa-group-pacing 210
              timers throttle lsa 100 70 1500
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            timers=dict(lsa_arrival=1200),
                            shutdown=True,
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "timers lsa-arrival 1200",
            "no timers lsa-group-pacing 210",
            "no timers throttle lsa 100 70 1500",
            "shutdown",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_vrf_merged(self):
        # test merged for config->processes->vrf
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              vrf blue
                area 1.1.1.1 nssa
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            vrfs=[
                                dict(
                                    vrf="blue",
                                    areas=[
                                        dict(
                                            area_id="1.1.1.1",
                                            nssa=dict(no_summary=True),
                                        ),
                                        dict(
                                            area_id="1.1.1.2",
                                            nssa=dict(set=True),
                                        ),
                                    ],
                                ),
                                dict(
                                    vrf="red",
                                    areas=[
                                        dict(
                                            area_id="1.1.1.3",
                                            nssa=dict(
                                                default_information_originate=True,
                                                no_summary=True,
                                                no_redistribution=True,
                                                route_map="test-1",
                                                translate=dict(
                                                    type7=dict(
                                                        always=True,
                                                        supress_fa=True,
                                                    )
                                                ),
                                            ),
                                        )
                                    ],
                                ),
                            ],
                        ),
                        dict(
                            process_id="103",
                            vrfs=[
                                dict(
                                    vrf="red",
                                    max_metric=dict(
                                        router_lsa=dict(
                                            on_startup=dict(
                                                wait_period=1200,
                                                wait_for_bgp_asn=65563,
                                            ),
                                            inter_area_prefix_lsa=dict(
                                                set=True
                                            ),
                                        )
                                    ),
                                )
                            ],
                        ),
                        dict(
                            process_id="104",
                            vrfs=[
                                dict(
                                    vrf="red",
                                    timers=dict(
                                        lsa_arrival=1200,
                                        lsa_group_pacing=210,
                                        throttle=dict(
                                            lsa=dict(
                                                start_interval=100,
                                                hold_interval=70,
                                                max_interval=1500,
                                            )
                                        ),
                                    ),
                                    shutdown=True,
                                )
                            ],
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "vrf blue",
            "area 1.1.1.1 nssa no-summary",
            "area 1.1.1.2 nssa",
            "vrf red",
            "area 1.1.1.3 nssa translate type7 always supress-fa",
            "area 1.1.1.3 nssa no-summary no-redistribution default-information-originate route-map test-1",
            "router ospfv3 103",
            "vrf red",
            "max-metric router-lsa on-startup 1200 wait-for bgp 65563 inter-area-prefix-lsa",
            "router ospfv3 104",
            "vrf red",
            "timers lsa-arrival 1200",
            "timers lsa-group-pacing 210",
            "timers throttle lsa 100 70 1500",
            "shutdown",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_vrf_replaced(self):
        # test replaced for config->processes->vrf
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              vrf blue
                area 1.1.1.1 nssa no-summary
                area 1.1.1.2 nssa
              vrf red
                area 1.1.1.3 nssa translate type7 always supress-fa
                area 1.1.1.3 nssa no-summary no-redistribution default-information-originate route-map test-1
            router ospfv3 103
              vrf red
                max-metric router-lsa on-startup 1200 wait-for bgp 65563 inter-area-prefix-lsa
            router ospfv3 104
              vrf red
                timers lsa-arrival 1200
                timers lsa-group-pacing 210
                timers throttle lsa 100 70 1500
                shutdown
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            vrfs=[
                                dict(
                                    vrf="blue",
                                    areas=[
                                        dict(
                                            area_id="1.1.1.1",
                                            nssa=dict(
                                                no_summary=True,
                                                translate=dict(
                                                    type7=dict(
                                                        always=True,
                                                        supress_fa=True,
                                                    )
                                                ),
                                            ),
                                        )
                                    ],
                                )
                            ],
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "vrf blue",
            "area 1.1.1.1 nssa no-summary",
            "no area 1.1.1.2 nssa",
            "area 1.1.1.1 nssa translate type7 always supress-fa",
            "no vrf red",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_top_spec_af_vrf_merged(self):
        # test merged for every nested level
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map map1 filter
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                redistribute=[
                                    dict(
                                        protocol="eigrp",
                                        id="100",
                                        route_map="rmap1",
                                    )
                                ],
                            ),
                            vrfs=[
                                dict(vrf="blue", router_id="10.0.0.2"),
                                dict(
                                    vrf="red",
                                    areas=[
                                        dict(
                                            area_id="1.1.1.1",
                                            nssa=dict(set=True),
                                        )
                                    ],
                                ),
                            ],
                        ),
                        dict(
                            process_id="103",
                            vrfs=[dict(vrf="red", shutdown=True)],
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "redistribute eigrp 100 route-map rmap1",
            "vrf blue",
            "router-id 10.0.0.2",
            "vrf red",
            "area 1.1.1.1 nssa",
            "router ospfv3 103",
            "vrf red",
            "shutdown",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_top_spec_af_vrf_replaced(self):
        # test replaced for every nested level
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map map1 filter
                redistribute eigrp 100 route-map rmap1
              vrf blue
                router-id 10.0.0.2
              vrf red
                area 1.1.1.1 nssa
            router ospfv3 103
              vrf red
              shutdown
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                redistribute=[
                                    dict(
                                        protocol="eigrp",
                                        id="100",
                                        route_map="rmap1",
                                    )
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no table-map map1 filter",
            "no vrf blue",
            "no vrf red",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_top_spec_af_vrf_overridden(self):
        # test overridden for every nested level
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map map1 filter
                redistribute eigrp 100 route-map rmap1
              vrf blue
                router-id 10.0.0.2
              vrf red
                area 1.1.1.1 nssa
            router ospfv3 103
              vrf red
              shutdown
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                redistribute=[
                                    dict(
                                        protocol="eigrp",
                                        id="100",
                                        route_map="rmap2",
                                    )
                                ],
                            ),
                        )
                    ]
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no table-map map1 filter",
            "redistribute eigrp 100 route-map rmap2",
            "no vrf blue",
            "no vrf red",
            "no router ospfv3 103",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_top_spec_af_vrf_deleted(self):
        # test overridden for every nested level
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map map1 filter
                redistribute eigrp 100 route-map rmap1
              vrf blue
                router-id 10.0.0.2
              vrf red
                area 1.1.1.1 nssa
            router ospfv3 103
              vrf red
              shutdown
            """
        )
        set_module_args(
            dict(
                config=dict(processes=[dict(process_id="100")]),
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = ["no router ospfv3 100"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_top_spec_af_vrf_deleted_all(self):
        # test overridden for every nested level
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map map1 filter
                redistribute eigrp 100 route-map rmap1
              vrf blue
                router-id 10.0.0.2
              vrf red
                area 1.1.1.1 nssa
            router ospfv3 103
              vrf red
              shutdown
            """
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = ["no router ospfv3 100", "no router ospfv3 103"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_parsed(self):
        # test parsed
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router ospfv3 100
                      address-family ipv6 unicast
                        table-map map1 filter
                        redistribute eigrp 100 route-map rmap1
                      vrf blue
                        router-id 10.0.0.2
                      vrf red
                        area 1.1.1.1 nssa
                    router ospfv3 103
                      vrf red
                        shutdown
                    """
                ),
                state="parsed",
            ),
            ignore_provider_arg,
        )
        parsed = {
            "processes": [
                {
                    "process_id": "100",
                    "address_family": {
                        "table_map": {"name": "map1", "filter": True},
                        "redistribute": [
                            {
                                "protocol": "eigrp",
                                "id": "100",
                                "route_map": "rmap1",
                            }
                        ],
                        "afi": "ipv6",
                        "safi": "unicast",
                    },
                    "vrfs": [
                        {"vrf": "blue", "router_id": "10.0.0.2"},
                        {
                            "vrf": "red",
                            "areas": [
                                {"area_id": "1.1.1.1", "nssa": {"set": True}}
                            ],
                        },
                    ],
                },
                {
                    "process_id": "103",
                    "vrfs": [{"vrf": "red", "shutdown": True}],
                },
            ]
        }
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["parsed"]), set(parsed))

    def test_nxos_ospfv3_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map map1 filter
                redistribute eigrp 100 route-map rmap1
              vrf blue
                router-id 10.0.0.2
              vrf red
                area 1.1.1.1 nssa
            router ospfv3 103
              vrf red
              shutdown
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = {
            "processes": [
                {
                    "process_id": "100",
                    "address_family": {
                        "table_map": {"name": "map1", "filter": True},
                        "redistribute": [
                            {
                                "protocol": "eigrp",
                                "id": "100",
                                "route_map": "rmap1",
                            }
                        ],
                        "afi": "ipv6",
                        "safi": "unicast",
                    },
                    "vrfs": [
                        {"vrf": "blue", "router_id": "10.0.0.2"},
                        {
                            "vrf": "red",
                            "areas": [
                                {"area_id": "1.1.1.1", "nssa": {"set": True}}
                            ],
                        },
                    ],
                },
                {
                    "process_id": "103",
                    "vrfs": [{"vrf": "red", "shutdown": True}],
                },
            ]
        }
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["gathered"]), set(gathered))

    def test_nxos_ospfv3_process_id_word(self):
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              router-id 203.0.113.20
            router ospfv3 TEST-1
              router-id 198.51.100.1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(process_id="100", router_id="203.0.113.20"),
                        dict(process_id="TEST-1", router_id="198.51.100.1"),
                        dict(process_id="TEST-2", router_id="198.52.200.1"),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )

        commands = ["router ospfv3 TEST-2", "router-id 198.52.200.1"]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
