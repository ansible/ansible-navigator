# (c) 2019 Red Hat Inc.
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
from ansible_collections.cisco.nxos.plugins.modules import nxos_ospfv2

from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosOspfv2Module(TestNxosModule):

    module = nxos_ospfv2

    def setUp(self):
        super(TestNxosOspfv2Module, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospfv2.ospfv2.Ospfv2Facts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosOspfv2Module, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_ospfv2_merged(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="203.0.113.20",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="rmap_1",
                                ),
                                dict(
                                    protocol="direct",
                                    route_map="direct-connect",
                                ),
                            ],
                            log_adjacency_changes=dict(detail=True),
                        ),
                        dict(
                            process_id="200",
                            router_id="198.51.100.1",
                            areas=[
                                dict(
                                    area_id="0.0.0.100",
                                    filter_list=[
                                        dict(
                                            route_map="rmap_1", direction="in"
                                        ),
                                        dict(
                                            route_map="rmap_2", direction="out"
                                        ),
                                    ],
                                    ranges=[
                                        dict(prefix="198.51.100.64/27"),
                                        dict(prefix="198.51.100.96/27"),
                                    ],
                                ),
                                dict(
                                    area_id="0.0.0.101",
                                    authentication=dict(message_digest=True),
                                ),
                            ],
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospf 100",
            "router-id 203.0.113.20",
            "redistribute eigrp 100 route-map rmap_1",
            "redistribute direct route-map direct-connect",
            "log-adjacency-changes detail",
            "router ospf 200",
            "router-id 198.51.100.1",
            "area 0.0.0.100 filter-list route-map rmap_1 in",
            "area 0.0.0.100 filter-list route-map rmap_2 out",
            "area 0.0.0.100 range 198.51.100.64/27",
            "area 0.0.0.100 range 198.51.100.96/27",
            "area 0.0.0.101 authentication message-digest",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv2_merged_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="203.0.113.20",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="rmap_1",
                                ),
                                dict(
                                    protocol="direct",
                                    route_map="direct-connect",
                                ),
                            ],
                        ),
                        dict(
                            process_id="200",
                            router_id="198.51.100.1",
                            areas=[
                                dict(
                                    area_id="0.0.0.100",
                                    filter_list=[
                                        dict(
                                            route_map="rmap_1", direction="in"
                                        ),
                                        dict(
                                            route_map="rmap_2", direction="out"
                                        ),
                                    ],
                                    ranges=[
                                        dict(prefix="198.51.100.64/27"),
                                        dict(prefix="198.51.100.96/27"),
                                    ],
                                ),
                                dict(
                                    area_id="0.0.0.101",
                                    authentication=dict(message_digest=True),
                                ),
                            ],
                        ),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ospfv2_merged_update(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="203.0.113.20",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="rmap_2",
                                )
                            ],
                            areas=[
                                dict(
                                    area_id="0.0.0.101",
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

        commands = [
            "router ospf 100",
            "redistribute eigrp 100 route-map rmap_2",
            "area 0.0.0.101 stub no-summary",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv2_replaced(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="203.0.113.20",
                            areas=[
                                dict(
                                    area_id="0.0.0.101",
                                    stub=dict(no_summary=True),
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
            "router ospf 100",
            "no redistribute eigrp 100 route-map rmap_1",
            "no redistribute direct route-map direct-connect",
            "area 0.0.0.101 stub no-summary",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv2_replaced_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="203.0.113.20",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="rmap_1",
                                ),
                                dict(
                                    protocol="direct",
                                    route_map="direct-connect",
                                ),
                            ],
                        ),
                        dict(
                            process_id="200",
                            router_id="198.51.100.1",
                            areas=[
                                dict(
                                    area_id="0.0.0.100",
                                    filter_list=[
                                        dict(
                                            route_map="rmap_1", direction="in"
                                        ),
                                        dict(
                                            route_map="rmap_2", direction="out"
                                        ),
                                    ],
                                    ranges=[
                                        dict(prefix="198.51.100.64/27"),
                                        dict(prefix="198.51.100.96/27"),
                                    ],
                                ),
                                dict(
                                    area_id="0.0.0.101",
                                    authentication=dict(message_digest=True),
                                ),
                            ],
                        ),
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ospfv2_overridden(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(process_id="300", router_id="203.0.113.20")
                    ]
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no router ospf 100",
            "no router ospf 200",
            "router ospf 300",
            "router-id 203.0.113.20",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv2_overridden_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            router_id="203.0.113.20",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="rmap_1",
                                ),
                                dict(
                                    protocol="direct",
                                    route_map="direct-connect",
                                ),
                            ],
                        ),
                        dict(
                            process_id="200",
                            router_id="198.51.100.1",
                            areas=[
                                dict(
                                    area_id="0.0.0.100",
                                    filter_list=[
                                        dict(
                                            route_map="rmap_1", direction="in"
                                        ),
                                        dict(
                                            route_map="rmap_2", direction="out"
                                        ),
                                    ],
                                    ranges=[
                                        dict(prefix="198.51.100.64/27"),
                                        dict(prefix="198.51.100.96/27"),
                                    ],
                                ),
                                dict(
                                    area_id="0.0.0.101",
                                    authentication=dict(message_digest=True),
                                ),
                            ],
                        ),
                    ]
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ospfv2_deleted(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            router ospf 300
              router-id 192.0.168.102
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[dict(process_id="100"), dict(process_id="300")]
                ),
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = ["no router ospf 100", "no router ospf 300"]

        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_ospfv2_deleted_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            router ospf 300
              router-id 192.0.168.102
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[dict(process_id="400"), dict(process_id="500")]
                ),
                state="deleted",
            ),
            ignore_provider_arg,
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ospfv2_deleted_all(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
              redistribute eigrp 100 route-map rmap_1
              redistribute direct route-map direct-connect
            router ospf 200
              router-id 198.51.100.1
              area 0.0.0.100 filter-list route-map rmap_1 in
              area 0.0.0.100 filter-list route-map rmap_2 out
              area 0.0.0.100 range 198.51.100.64/27
              area 0.0.0.100 range 198.51.100.96/27
              area 0.0.0.101 authentication message-digest
            router ospf 300
              router-id 192.0.168.102
            """
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)

        commands = [
            "no router ospf 100",
            "no router ospf 200",
            "no router ospf 300",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv2_process_id_word(self):
        self.get_config.return_value = dedent(
            """\
            router ospf 100
              router-id 203.0.113.20
            router ospf TEST-1
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

        commands = ["router ospf TEST-2", "router-id 198.52.200.1"]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
