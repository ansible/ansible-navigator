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
from ansible_collections.vyos.vyos.plugins.modules import vyos_ospfv2
from ansible_collections.vyos.vyos.tests.unit.modules.utils import (
    set_module_args,
)
from .vyos_module import TestVyosModule, load_fixture


class TestVyosOspfv2Module(TestVyosModule):

    module = vyos_ospfv2

    def setUp(self):
        super(TestVyosOspfv2Module, self).setUp()
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

        self.mock_execute_show_command = patch(
            "ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.facts.ospfv2.ospfv2.Ospfv2Facts.get_device_data"
        )

        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestVyosOspfv2Module, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        if filename is None:
            filename = "vyos_ospfv2_config.cfg"

        def load_from_file(*args, **kwargs):
            output = load_fixture(filename)
            return output

        self.execute_show_command.side_effect = load_from_file

    def test_vyos_ospfv2_merged_new_config(self):
        set_module_args(
            dict(
                config=dict(
                    log_adjacency_changes="detail",
                    mpls_te=dict(enabled=True, router_address="192.0.11.11"),
                    auto_cost=dict(reference_bandwidth=2),
                    areas=[
                        dict(
                            area_id="2",
                            area_type=dict(normal=True),
                            authentication="plaintext-password",
                            shortcut="enable",
                        ),
                        dict(
                            area_id="4",
                            area_type=dict(stub=dict(default_cost=10)),
                            network=[dict(address="192.0.2.0/24")],
                            range=[
                                dict(address="192.0.3.0/24", cost=10),
                                dict(address="192.0.4.0/24", cost=12),
                            ],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        commands = [
            "set protocols ospf mpls-te enable",
            "set protocols ospf mpls-te router-address '192.0.11.11'",
            "set protocols ospf auto-cost reference-bandwidth '2'",
            "set protocols ospf log-adjacency-changes 'detail'",
            "set protocols ospf area '2'",
            "set protocols ospf area 2 authentication plaintext-password",
            "set protocols ospf area 2 shortcut enable",
            "set protocols ospf area 2 area-type normal",
            "set protocols ospf area 4 range 192.0.3.0/24 cost 10",
            "set protocols ospf area 4 range 192.0.3.0/24",
            "set protocols ospf area 4 range 192.0.4.0/24 cost 12",
            "set protocols ospf area 4 range 192.0.4.0/24",
            "set protocols ospf area 4 area-type stub default-cost 10",
            "set protocols ospf area '4'",
            "set protocols ospf area 4 network 192.0.2.0/24",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv2_merged_idem(self):
        set_module_args(
            dict(
                config=dict(
                    areas=[
                        dict(
                            area_id="12",
                            area_type=dict(normal=True),
                            authentication="plaintext-password",
                            shortcut="enable",
                        ),
                        dict(
                            area_id="14",
                            area_type=dict(stub=dict(default_cost=20)),
                            network=[dict(address="192.0.12.0/24")],
                            range=[
                                dict(address="192.0.13.0/24", cost=10),
                                dict(address="192.0.14.0/24", cost=12),
                            ],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospfv2_merged_update_existing(self):
        set_module_args(
            dict(
                config=dict(
                    areas=[
                        dict(
                            area_id="12",
                            area_type=dict(normal=True),
                            authentication="plaintext-password",
                            shortcut="enable",
                        ),
                        dict(
                            area_id="14",
                            area_type=dict(stub=dict(set=False)),
                            network=[
                                dict(address="192.0.12.0/24"),
                                dict(address="192.0.22.0/24"),
                            ],
                            range=[
                                dict(address="192.0.13.0/24", cost=10),
                                dict(address="192.0.14.0/24", cost=12),
                            ],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        commands = [
            "delete protocols ospf area 14 area-type stub",
            "set protocols ospf area 14 network 192.0.22.0/24",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv2_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    log_adjacency_changes="detail",
                    mpls_te=dict(enabled=True, router_address="192.0.11.11"),
                    auto_cost=dict(reference_bandwidth=2),
                    areas=[
                        dict(
                            area_id="12",
                            area_type=dict(normal=True),
                            authentication="plaintext-password",
                            shortcut="enable",
                        ),
                        dict(
                            area_id="15",
                            area_type=dict(stub=dict(default_cost=10)),
                            network=[dict(address="192.0.12.0/24")],
                            range=[
                                dict(address="192.0.13.0/24", cost=10),
                                dict(address="192.0.14.0/24", cost=12),
                                dict(address="192.0.15.0/24", cost=14),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            )
        )
        commands = [
            "set protocols ospf mpls-te enable",
            "set protocols ospf mpls-te router-address '192.0.11.11'",
            "set protocols ospf auto-cost reference-bandwidth '2'",
            "set protocols ospf log-adjacency-changes 'detail'",
            "delete protocols ospf area 14",
            "set protocols ospf area 15 range 192.0.13.0/24 cost 10",
            "set protocols ospf area 15 range 192.0.13.0/24",
            "set protocols ospf area 15 range 192.0.14.0/24 cost 12",
            "set protocols ospf area 15 range 192.0.14.0/24",
            "set protocols ospf area 15 range 192.0.15.0/24 cost 14",
            "set protocols ospf area 15 range 192.0.15.0/24",
            "set protocols ospf area 15 area-type stub default-cost 10",
            "set protocols ospf area '15'",
            "set protocols ospf area 15 network 192.0.12.0/24",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv2_replaced_idem(self):
        set_module_args(
            dict(
                config=dict(
                    areas=[
                        dict(
                            area_id="12",
                            area_type=dict(normal=True),
                            authentication="plaintext-password",
                            shortcut="enable",
                        ),
                        dict(
                            area_id="14",
                            area_type=dict(stub=dict(default_cost=20)),
                            network=[dict(address="192.0.12.0/24")],
                            range=[
                                dict(address="192.0.13.0/24", cost=10),
                                dict(address="192.0.14.0/24", cost=12),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospfv2_deleted_no_config(self):
        set_module_args(dict(config=None, state="deleted"))
        commands = ["delete protocols ospf"]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv2_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(
            changed=False, filename="vyos_ospfv2_config.cfg"
        )
        gather_dict = {
            "areas": [
                {
                    "area_id": "2",
                    "area_type": {"normal": True},
                    "authentication": "plaintext-password",
                    "shortcut": "enable",
                },
                {
                    "area_id": "14",
                    "area_type": {"stub": {"default_cost": 20, "set": True}},
                    "network": [{"address": "192.0.12.0/24"}],
                    "range": [
                        {"address": "192.0.13.0/24", "cost": 10},
                        {"address": "192.0.14.0/24", "cost": 12},
                    ],
                },
            ],
        }
        self.assertEqual(sorted(gather_dict), sorted(result["gathered"]))

    def test_vyos_ospfv2_parsed(self):
        parsed_str = """set protocols ospf area 2 area-type 'normal'
        set protocols ospf area 2 authentication 'plaintext-password'
        set protocols ospf area 2 shortcut 'enable'
        set protocols ospf area 3 area-type 'nssa'
        set protocols ospf area 4 area-type stub default-cost '20'
        set protocols ospf area 4 network '192.0.2.0/24'
        set protocols ospf area 4 range 192.0.3.0/24 cost '10'
        set protocols ospf area 4 range 192.0.4.0/24 cost '12'
        set protocols ospf default-information originate 'always'
        set protocols ospf default-information originate metric '10'
        set protocols ospf default-information originate metric-type '2'
set protocols ospf auto-cost reference-bandwidth '2'
set protocols ospf default-information originate route-map 'ingress'
set protocols ospf log-adjacency-changes 'detail'
set protocols ospf max-metric router-lsa 'administrative'
set protocols ospf max-metric router-lsa on-shutdown '10'
set protocols ospf max-metric router-lsa on-startup '10'
set protocols ospf mpls-te 'enable'
set protocols ospf mpls-te router-address '192.0.11.11'
set protocols ospf neighbor 192.0.11.12 poll-interval '10'
set protocols ospf neighbor 192.0.11.12 priority '2'
set protocols ospf parameters abr-type 'cisco'
set protocols ospf parameters 'opaque-lsa'
set protocols ospf parameters 'rfc1583-compatibility'
set protocols ospf parameters router-id '192.0.1.1'
set protocols ospf passive-interface 'eth1'
set protocols ospf passive-interface 'eth2'
set protocols ospf redistribute bgp metric '10'
set protocols ospf redistribute bgp metric-type '2'"""
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = {
            "areas": [
                {
                    "area_id": "2",
                    "area_type": {"normal": True},
                    "authentication": "plaintext-password",
                    "shortcut": "enable",
                },
                {"area_id": "3", "area_type": {"nssa": {"set": True}}},
                {
                    "area_id": "4",
                    "area_type": {"stub": {"default_cost": 20, "set": True}},
                    "network": [{"address": "192.0.2.0/24"}],
                    "range": [
                        {"address": "192.0.3.0/24", "cost": 10},
                        {"address": "192.0.4.0/24", "cost": 12},
                    ],
                },
            ],
            "auto_cost": {"reference_bandwidth": 2},
            "default_information": {
                "originate": {
                    "always": True,
                    "metric": 10,
                    "metric_type": 2,
                    "route_map": "ingress",
                }
            },
            "log_adjacency_changes": "detail",
            "max_metric": {
                "router_lsa": {
                    "administrative": True,
                    "on_shutdown": 10,
                    "on_startup": 10,
                }
            },
            "mpls_te": {"enabled": True, "router_address": "192.0.11.11"},
            "neighbor": [
                {
                    "neighbor_id": "192.0.11.12",
                    "poll_interval": 10,
                    "priority": 2,
                }
            ],
            "parameters": {
                "abr_type": "cisco",
                "opaque_lsa": True,
                "rfc1583_compatibility": True,
                "router_id": "192.0.1.1",
            },
            "passive_interface": ["eth2", "eth1"],
            "redistribute": [
                {"metric": 10, "metric_type": 2, "route_type": "bgp"}
            ],
        }
        self.assertEqual(sorted(parsed_list), sorted(result["parsed"]))

    def test_vyos_ospfv2_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    log_adjacency_changes="detail",
                    mpls_te=dict(enabled=True, router_address="192.0.11.11"),
                    auto_cost=dict(reference_bandwidth=2),
                    areas=[
                        dict(
                            area_id="2",
                            area_type=dict(normal=True),
                            authentication="plaintext-password",
                            shortcut="enable",
                        ),
                        dict(
                            area_id="4",
                            area_type=dict(stub=dict(default_cost=10)),
                            network=[dict(address="192.0.2.0/24")],
                            range=[
                                dict(address="192.0.3.0/24", cost=10),
                                dict(address="192.0.4.0/24", cost=12),
                            ],
                        ),
                    ],
                ),
                state="rendered",
            )
        )
        commands = [
            "set protocols ospf mpls-te enable",
            "set protocols ospf mpls-te router-address '192.0.11.11'",
            "set protocols ospf auto-cost reference-bandwidth '2'",
            "set protocols ospf log-adjacency-changes 'detail'",
            "set protocols ospf area '2'",
            "set protocols ospf area 2 authentication plaintext-password",
            "set protocols ospf area 2 shortcut enable",
            "set protocols ospf area 2 area-type normal",
            "set protocols ospf area 4 range 192.0.3.0/24 cost 10",
            "set protocols ospf area 4 range 192.0.3.0/24",
            "set protocols ospf area 4 range 192.0.4.0/24 cost 12",
            "set protocols ospf area 4 range 192.0.4.0/24",
            "set protocols ospf area 4 area-type stub default-cost 10",
            "set protocols ospf area '4'",
            "set protocols ospf area 4 network 192.0.2.0/24",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )
