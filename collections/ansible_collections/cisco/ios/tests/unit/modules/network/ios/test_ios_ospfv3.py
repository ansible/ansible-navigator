#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_ospfv3
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosOspfV3Module(TestIosModule):
    module = ios_ospfv3

    def setUp(self):
        super(TestIosOspfV3Module, self).setUp()

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
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.ospfv3.ospfv3."
            "Ospfv3Facts.get_ospfv3_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosOspfV3Module, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_ospfv3.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_ospfv3_merged(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            auto_cost=dict(reference_bandwidth="4"),
                            areas=[dict(area_id=10, default_cost=10)],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=100, max_adjacency=100
                                    ),
                                )
                            ],
                        )
                    ]
                ),
                state="merged",
            )
        )
        commands = [
            "router ospfv3 1",
            "auto-cost reference-bandwidth 4",
            "area 10 default-cost 10",
            "address-family ipv4 unicast vrf blue",
            "adjacency stagger 100 100",
            "exit-address-family",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_ospfv3_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(
                                router_lsa=True, on_startup=dict(time=110)
                            ),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(
                                            metric=10
                                        )
                                    ),
                                )
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=50, max_adjacency=50
                                    ),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25, nssa_only=True
                                                )
                                            ),
                                        )
                                    ],
                                )
                            ],
                        )
                    ]
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv3_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(
                                router_lsa=True, on_startup=dict(time=100)
                            ),
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=100, max_adjacency=100
                                    ),
                                )
                            ],
                        )
                    ]
                ),
                state="replaced",
            )
        )
        commands = [
            "router ospfv3 1",
            "max-metric router-lsa on-startup 100",
            "no area 10 nssa default-information-originate metric 10",
            "address-family ipv4 unicast vrf blue",
            "adjacency stagger 100 100",
            "exit-address-family",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    #
    def test_ios_ospfv3_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(
                                router_lsa=True, on_startup=dict(time=110)
                            ),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(
                                            metric=10
                                        )
                                    ),
                                )
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=50, max_adjacency=50
                                    ),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25, nssa_only=True
                                                )
                                            ),
                                        )
                                    ],
                                )
                            ],
                        )
                    ]
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv3_overridden(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="200",
                            max_metric=dict(
                                router_lsa=True, on_startup=dict(time=200)
                            ),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(
                                            metric=10
                                        )
                                    ),
                                )
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    adjacency=dict(
                                        min_adjacency=50, max_adjacency=50
                                    ),
                                    areas=[
                                        dict(
                                            area_id=200,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=200, nssa_only=True
                                                )
                                            ),
                                        )
                                    ],
                                )
                            ],
                        )
                    ]
                ),
                state="overridden",
            )
        )

        commands = [
            "no router ospfv3 1",
            "router ospfv3 200",
            "max-metric router-lsa on-startup 200",
            "area 10 nssa default-information-originate metric 10",
            "address-family ipv4 unicast",
            "adjacency stagger 50 50",
            "area 200 nssa default-information-originate metric 200 nssa-only",
            "exit-address-family",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_ios_ospfv3_overridden_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(
                                router_lsa=True, on_startup=dict(time=110)
                            ),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(
                                            metric=10
                                        )
                                    ),
                                )
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=50, max_adjacency=50
                                    ),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25, nssa_only=True
                                                )
                                            ),
                                        )
                                    ],
                                )
                            ],
                        )
                    ]
                ),
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_ios_ospfv3_deleted(self):
        set_module_args(
            dict(
                config=dict(processes=[dict(process_id="1")]), state="deleted"
            )
        )
        commands = ["no router ospfv3 1"]
        self.execute_module(changed=True, commands=commands)

    def test_ios_ospfv3_parsed(self):
        set_module_args(
            dict(running_config="router ospfv3 1\n area 5", state="parsed")
        )
        result = self.execute_module(changed=False)
        parsed_list = {
            "processes": [{"areas": [{"area_id": "5"}], "process_id": 1}]
        }
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_ospfv3_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            max_metric=dict(
                                router_lsa=True, on_startup=dict(time=110)
                            ),
                            areas=[
                                dict(
                                    area_id=10,
                                    nssa=dict(
                                        default_information_originate=dict(
                                            metric=10
                                        )
                                    ),
                                )
                            ],
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    unicast=True,
                                    vrf="blue",
                                    adjacency=dict(
                                        min_adjacency=50, max_adjacency=50
                                    ),
                                    areas=[
                                        dict(
                                            area_id=25,
                                            nssa=dict(
                                                default_information_originate=dict(
                                                    metric=25, nssa_only=True
                                                )
                                            ),
                                        )
                                    ],
                                )
                            ],
                        )
                    ]
                ),
                state="rendered",
            )
        )
        commands = [
            "address-family ipv4 unicast vrf blue",
            "adjacency stagger 50 50",
            "area 10 nssa default-information-originate metric 10",
            "area 25 nssa default-information-originate metric 25 nssa-only",
            "exit-address-family",
            "max-metric router-lsa on-startup 110",
            "router ospfv3 1",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), commands)
