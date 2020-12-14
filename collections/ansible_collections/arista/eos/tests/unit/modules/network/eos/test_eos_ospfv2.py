#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_ospfv2
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosOspfv2Module(TestEosModule):
    module = eos_ospfv2

    def setUp(self):
        super(TestEosOspfv2Module, self).setUp()

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
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.ospfv2.ospfv2.Ospfv2Facts.get_device_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosOspfv2Module, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        if filename is None:
            filename = "eos_ospfv2_config.cfg"

        def load_from_file(*args, **kwargs):
            output = load_fixture(filename)
            return output

        self.execute_show_command.side_effect = load_from_file

    def test_eos_ospfv2_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            adjacency=dict(
                                exchange_start=dict(threshold=20045623)
                            ),
                            areas=[
                                dict(
                                    filter=dict(address="10.1.1.0/24"),
                                    area_id="0.0.0.2",
                                ),
                                dict(
                                    area_id="0.0.0.50",
                                    range=dict(
                                        address="172.20.0.0/16", cost=34
                                    ),
                                ),
                            ],
                            default_information=dict(
                                metric=100, metric_type=1, originate=True
                            ),
                            distance=dict(intra_area=85),
                            max_lsa=dict(
                                count=80000,
                                threshold=40,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                            ),
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.2.0/24"),
                                dict(area="0.0.0.0", prefix="10.10.3.0/24"),
                            ],
                            redistribute=[dict(routes="static")],
                            router_id="170.21.0.4",
                        ),
                        dict(
                            process_id=2,
                            vrf="vrf01",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            max_lsa=dict(
                                count=80000,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                                threshold=40,
                            ),
                        ),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            redistribute=[dict(routes="static")],
                        ),
                    ]
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv2_merged_partly_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            adjacency=dict(
                                exchange_start=dict(threshold=20045623)
                            ),
                            areas=[
                                dict(
                                    filter=dict(address="10.1.1.0/24"),
                                    area_id="0.0.0.2",
                                )
                            ],
                            distance=dict(intra_area=85),
                            max_lsa=dict(
                                count=80000,
                                threshold=40,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                            ),
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.3.0/24")
                            ],
                            redistribute=[dict(routes="static")],
                            router_id="170.21.0.4",
                        ),
                        dict(
                            process_id=2,
                            vrf="vrf01",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                        ),
                    ]
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv2_merged(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            areas=[
                                dict(
                                    filter=dict(address="10.2.1.0/24"),
                                    area_id="0.0.0.12",
                                )
                            ],
                            redistribute=[
                                dict(routes="isis", isis_level="level-1")
                            ],
                        ),
                        dict(
                            process_id=4,
                            vrf="vrftest",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.3.0/24")
                            ],
                        ),
                    ]
                ),
                state="merged",
            )
        )
        commands = [
            "router ospf 1",
            "area 0.0.0.12 filter 10.2.1.0/24",
            "redistribute isis level-1",
            "exit",
            "router ospf 4 vrf vrftest",
            "area 0.0.0.9 default-cost 20",
            "network 10.10.3.0/24 area 0.0.0.0",
            "exit",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv2_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            areas=[
                                dict(
                                    filter=dict(address="10.2.1.0/24"),
                                    area_id="0.0.0.12",
                                )
                            ],
                            redistribute=[
                                dict(routes="isis", isis_level="level-1")
                            ],
                        ),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.3.0/24")
                            ],
                        ),
                    ]
                ),
                state="replaced",
            )
        )
        commands = [
            "router ospf 1",
            "no adjacency exchange-start threshold 20045623",
            "no area 0.0.0.2 filter 10.1.1.0/24",
            "no area 0.0.0.50  range 172.20.0.0/16 cost 34",
            "no default-information originate metric 100 metric-type 1",
            "no distance ospf intra-area 85",
            "no max-lsa  80000 40 ignore-count 3  ignore-time 6  reset-time 20",
            "no network 10.10.2.0/24 area 0.0.0.0",
            "no network 10.10.3.0/24 area 0.0.0.0",
            "no redistribute static",
            "no router-id 170.21.0.4",
            "area 0.0.0.12 filter 10.2.1.0/24",
            "redistribute isis level-1",
            "exit",
            "router ospf 3 vrf vrf02",
            "no redistribute static",
            "area 0.0.0.9 default-cost 20",
            "network 10.10.3.0/24 area 0.0.0.0",
            "exit",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv2_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            adjacency=dict(
                                exchange_start=dict(threshold=20045623)
                            ),
                            areas=[
                                dict(
                                    filter=dict(address="10.1.1.0/24"),
                                    area_id="0.0.0.2",
                                ),
                                dict(
                                    area_id="0.0.0.50",
                                    range=dict(
                                        address="172.20.0.0/16", cost=34
                                    ),
                                ),
                            ],
                            default_information=dict(
                                metric=100, metric_type=1, originate=True
                            ),
                            distance=dict(intra_area=85),
                            max_lsa=dict(
                                count=80000,
                                threshold=40,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                            ),
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.2.0/24"),
                                dict(area="0.0.0.0", prefix="10.10.3.0/24"),
                            ],
                            redistribute=[dict(routes="static")],
                            router_id="170.21.0.4",
                        ),
                        dict(
                            process_id=2,
                            vrf="vrf01",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            max_lsa=dict(
                                count=80000,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                                threshold=40,
                            ),
                        ),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            redistribute=[dict(routes="static")],
                        ),
                    ]
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv2_overridden(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            areas=[
                                dict(
                                    filter=dict(address="10.2.1.0/24"),
                                    area_id="0.0.0.12",
                                )
                            ],
                            redistribute=[
                                dict(routes="isis", isis_level="level-1")
                            ],
                        ),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.3.0/24")
                            ],
                        ),
                    ]
                ),
                state="overridden",
            )
        )
        commands = [
            "router ospf 1",
            "no adjacency exchange-start threshold 20045623",
            "no area 0.0.0.2 filter 10.1.1.0/24",
            "no area 0.0.0.50  range 172.20.0.0/16 cost 34",
            "no default-information originate metric 100 metric-type 1",
            "no distance ospf intra-area 85",
            "no max-lsa  80000 40 ignore-count 3  ignore-time 6  reset-time 20",
            "no network 10.10.2.0/24 area 0.0.0.0",
            "no network 10.10.3.0/24 area 0.0.0.0",
            "no redistribute static",
            "no router-id 170.21.0.4",
            "area 0.0.0.12 filter 10.2.1.0/24",
            "redistribute isis level-1",
            "exit",
            "no router ospf 2",
            "router ospf 3 vrf vrf02",
            "no redistribute static",
            "area 0.0.0.9 default-cost 20",
            "network 10.10.3.0/24 area 0.0.0.0",
            "exit",
        ]

        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv2_overridden_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            adjacency=dict(
                                exchange_start=dict(threshold=20045623)
                            ),
                            areas=[
                                dict(
                                    filter=dict(address="10.1.1.0/24"),
                                    area_id="0.0.0.2",
                                ),
                                dict(
                                    area_id="0.0.0.50",
                                    range=dict(
                                        address="172.20.0.0/16", cost=34
                                    ),
                                ),
                            ],
                            default_information=dict(
                                metric=100, metric_type=1, originate=True
                            ),
                            distance=dict(intra_area=85),
                            max_lsa=dict(
                                count=80000,
                                threshold=40,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                            ),
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.2.0/24"),
                                dict(area="0.0.0.0", prefix="10.10.3.0/24"),
                            ],
                            redistribute=[dict(routes="static")],
                            router_id="170.21.0.4",
                        ),
                        dict(
                            process_id=2,
                            vrf="vrf01",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            max_lsa=dict(
                                count=80000,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                                threshold=40,
                            ),
                        ),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            redistribute=[dict(routes="static")],
                        ),
                    ]
                ),
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv2_error1(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            areas=[
                                dict(
                                    filter=dict(address="10.2.1.0/24"),
                                    area_id="0.0.0.12",
                                )
                            ],
                            redistribute=[
                                dict(routes="isis", isis_level="level-1")
                            ],
                        ),
                        dict(
                            process_id=5,
                            vrf="vrf02",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.3.0/24")
                            ],
                        ),
                    ]
                )
            )
        )
        result = self.execute_module(failed=True)
        self.assertIn(
            "Value of vrf and process_id does not match the config present in the device",
            result["msg"],
        )

    def test_eos_ospfv2_error2(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            areas=[
                                dict(
                                    filter=dict(address="10.2.1.0/24"),
                                    area_id="0.0.0.12",
                                )
                            ],
                            redistribute=[
                                dict(routes="isis", isis_level="level-1")
                            ],
                        ),
                        dict(
                            process_id=2,
                            vrf="vrf02",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.3.0/24")
                            ],
                        ),
                    ]
                ),
                state="overridden",
            )
        )
        result = self.execute_module(failed=True)
        self.assertIn(
            "Value of vrf and process_id does not match the config present in the device",
            result["msg"],
        )

    def test_eos_ospfv2_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="1",
                            adjacency=dict(
                                exchange_start=dict(threshold=20045623)
                            ),
                            areas=[
                                dict(
                                    filter=dict(address="10.1.1.0/24"),
                                    area_id="0.0.0.2",
                                ),
                                dict(
                                    area_id="0.0.0.50",
                                    range=dict(
                                        address="172.20.0.0/16", cost=34
                                    ),
                                ),
                            ],
                            default_information=dict(
                                metric=100, metric_type=1, originate=True
                            ),
                            distance=dict(intra_area=85),
                            max_lsa=dict(
                                count=80000,
                                threshold=40,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                            ),
                            networks=[
                                dict(area="0.0.0.0", prefix="10.10.2.0/24"),
                                dict(area="0.0.0.0", prefix="10.10.3.0/24"),
                            ],
                            redistribute=[dict(routes="static")],
                            router_id="170.21.0.4",
                        ),
                        dict(
                            process_id=2,
                            vrf="vrf01",
                            areas=[dict(default_cost=20, area_id="0.0.0.9")],
                            max_lsa=dict(
                                count=80000,
                                ignore_count=3,
                                ignore_time=6,
                                reset_time=20,
                                threshold=40,
                            ),
                        ),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            redistribute=[dict(routes="static")],
                        ),
                    ]
                ),
                state="rendered",
            )
        )
        commands = [
            "router ospf 1",
            "adjacency exchange-start threshold 20045623",
            "area 0.0.0.2 filter 10.1.1.0/24",
            "area 0.0.0.50  range 172.20.0.0/16 cost 34",
            "default-information originate metric 100 metric-type 1",
            "distance ospf intra-area 85",
            "max-lsa  80000 40 ignore-count 3  ignore-time 6  reset-time 20",
            "network 10.10.2.0/24 area 0.0.0.0",
            "network 10.10.3.0/24 area 0.0.0.0",
            "redistribute static",
            "router-id 170.21.0.4",
            "exit",
            "router ospf 2 vrf vrf01",
            "area 0.0.0.9 default-cost 20",
            "max-lsa  80000 40 ignore-count 3  ignore-time 6  reset-time 20",
            "exit",
            "router ospf 3 vrf vrf02",
            "redistribute static",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_eos_ospfv2_parsed(self):
        commands = [
            "router ospf 1",
            "adjacency exchange-start threshold 20045623",
            "area 0.0.0.2 filter 10.1.1.0/24",
            "area 0.0.0.50  range 172.20.0.0/16 cost 34",
            "default-information originate metric 100 metric-type 1",
            "distance ospf intra-area 85",
            "max-lsa  80000 40 ignore-count 3  ignore-time 6  reset-time 20",
            "network 10.10.2.0/24 area 0.0.0.0",
            "network 10.10.3.0/24 area 0.0.0.0",
            "redistribute static",
            "router-id 170.21.0.4",
            "exit",
            "router ospf 3 vrf vrf02",
            "redistribute static",
            "exit",
        ]
        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = {
            "processes": [
                {
                    "adjacency": {"exchange_start": {"threshold": 20045623}},
                    "areas": [
                        {
                            "filter": {"address": "10.1.1.0/24"},
                            "area_id": "0.0.0.2",
                        },
                        {
                            "area_id": "0.0.0.50",
                            "range": {"address": "172.20.0.0/16", "cost": 34},
                        },
                    ],
                    "default_information": {
                        "metric": 100,
                        "metric_type": 1,
                        "originate": True,
                    },
                    "distance": {"intra_area": 85},
                    "max_lsa": {
                        "count": 80000,
                        "ignore_count": 3,
                        "ignore_time": 6,
                        "reset_time": 20,
                        "threshold": 40,
                    },
                    "networks": [
                        {"area": "0.0.0.0", "prefix": "10.10.2.0/24"},
                        {"area": "0.0.0.0", "prefix": "10.10.3.0/24"},
                    ],
                    "process_id": 1,
                    "redistribute": [{"routes": "static"}],
                    "router_id": "170.21.0.4",
                },
                {
                    "process_id": 3,
                    "redistribute": [{"routes": "static"}],
                    "vrf": "vrf02",
                },
            ]
        }
        self.assertEqual(sorted(parsed_list), sorted(result["parsed"]))

    def test_eos_ospfv2_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(
            changed=False, filename="eos_ospfv2_config_gather.cfg"
        )
        gather_list = {
            "processes": [
                {
                    "adjacency": {"exchange_start": {"threshold": 20045623}},
                    "areas": [
                        {
                            "filter": {"address": "10.1.1.0/24"},
                            "area_id": "0.0.0.2",
                        },
                        {
                            "area_id": "0.0.0.50",
                            "range": {"address": "172.20.0.0/16", "cost": 34},
                        },
                    ],
                    "default_information": {
                        "metric": 100,
                        "metric_type": 1,
                        "originate": True,
                    },
                    "distance": {"intra_area": 85},
                    "max_lsa": {
                        "count": 80000,
                        "ignore_count": 3,
                        "ignore_time": 6,
                        "reset_time": 20,
                        "threshold": 40,
                    },
                    "networks": [
                        {"area": "0.0.0.0", "prefix": "10.10.2.0/24"},
                        {"area": "0.0.0.0", "prefix": "10.10.3.0/24"},
                    ],
                    "process_id": 1,
                    "redistribute": [{"routes": "static"}],
                    "router_id": "170.21.0.4",
                },
                {
                    "process_id": 3,
                    "redistribute": [{"routes": "static"}],
                    "vrf": "vrf02",
                },
            ]
        }
        self.assertEqual(sorted(gather_list), sorted(result["gathered"]))

    def test_eos_ospfv2_deleted(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(process_id="1"),
                        dict(
                            process_id=3,
                            vrf="vrf02",
                            redistribute=[dict(routes="static")],
                        ),
                    ]
                ),
                state="deleted",
            )
        )
        commands = [
            "no router ospf 1",
            "router ospf 3 vrf vrf02",
            "no redistribute static",
            "exit",
        ]
        self.execute_module(changed=True, commands=commands)
