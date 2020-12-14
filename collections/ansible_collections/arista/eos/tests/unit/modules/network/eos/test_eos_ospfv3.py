#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_ospfv3
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosOspfv3Module(TestEosModule):
    module = eos_ospfv3

    def setUp(self):
        super(TestEosOspfv3Module, self).setUp()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_execute_show_command = patch(
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.ospfv3.ospfv3.Ospfv3Facts.get_config"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosOspfv3Module, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        if filename is None:
            filename = "eos_ospfv3_config.cfg"

        def load_from_file(*args, **kwargs):
            output = load_fixture(filename)
            return output

        self.execute_show_command.side_effect = load_from_file

    def test_eos_ospfv3_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="default",
                            adjacency=dict(exchange_start=dict(threshold=11)),
                            areas=[
                                dict(stub=dict(set=True), area_id="0.0.0.20"),
                                dict(
                                    area_id="0.0.0.40",
                                    stub=dict(set=True),
                                    default_cost=45,
                                ),
                            ],
                            timers=dict(pacing=7),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    fips_restrictions=True,
                                    redistribute=[dict(routes="connected")],
                                ),
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    router_id="10.1.1.1",
                                ),
                            ],
                        ),
                        dict(
                            vrf="vrf01",
                            bfd=dict(all_interfaces=True),
                            log_adjacency_changes=dict(detail=True),
                            areas=[
                                dict(
                                    area_id="0.0.0.0",
                                    encryption=dict(
                                        algorithm="sha1",
                                        hidden_key=True,
                                        passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                        encryption="null",
                                        spi=44,
                                    ),
                                )
                            ],
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    fips_restrictions=True,
                                    redistribute=[
                                        dict(
                                            routes="connected",
                                            route_map="MAP01",
                                        )
                                    ],
                                    passive_interface=True,
                                    maximum_paths=100,
                                ),
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    areas=[
                                        dict(
                                            area_id="0.0.0.10",
                                            nssa=dict(no_summary=True),
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    max_metric=dict(
                                        router_lsa=dict(
                                            external_lsa=dict(
                                                max_metric_value=25
                                            ),
                                            summary_lsa=dict(set=True),
                                        )
                                    ),
                                ),
                            ],
                        ),
                        dict(
                            vrf="vrf02",
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    areas=[
                                        dict(
                                            area_id="0.0.0.1",
                                            stub=dict(set=True),
                                        )
                                    ],
                                    distance=200,
                                    router_id="10.17.0.3",
                                    timers=dict(
                                        out_delay=10,
                                        throttle=dict(
                                            initial=56,
                                            max=56,
                                            min=56,
                                            spf=True,
                                        ),
                                    ),
                                )
                            ],
                        ),
                    ]
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv3_merged(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="default",
                            areas=[
                                dict(
                                    area_id="0.0.0.20",
                                    authentication=dict(
                                        algorithm="sha1",
                                        spi="33",
                                        hidden_key=True,
                                        passphrase="4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
                                    ),
                                )
                            ],
                            timers=dict(pacing=7),
                        ),
                        dict(
                            vrf="vrf03",
                            log_adjacency_changes=dict(detail=True),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv6",
                                    areas=[
                                        dict(
                                            area_id="0.0.0.43",
                                            nssa=dict(no_summary=True),
                                            ranges=[
                                                dict(
                                                    address="20.1.1.0/24",
                                                    advertise=False,
                                                )
                                            ],
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    graceful_restart=dict(set=True),
                                )
                            ],
                        ),
                    ]
                ),
                state="merged",
            )
        )
        commands = [
            "router ospfv3",
            "area 0.0.0.20 authentication ipsec spi 33 sha1 passphrase 7 4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
            "exit",
            "router ospfv3 vrf vrf03",
            "fips restrictions",
            "log-adjacency-changes detail",
            "address-family ipv6",
            "area 0.0.0.43 nssa no-summary",
            "area 0.0.0.43 range 20.1.1.0/24 not-advertise",
            "default-information originate route-map DefaultRouteFilter",
            "graceful-restart",
            "exit",
            "exit",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv3_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="vrf02",
                            areas=[
                                dict(
                                    area_id="0.0.0.20",
                                    authentication=dict(
                                        algorithm="sha1",
                                        spi="33",
                                        hidden_key=True,
                                        passphrase="4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
                                    ),
                                )
                            ],
                            log_adjacency_changes=dict(detail=True),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv6",
                                    areas=[
                                        dict(
                                            area_id="0.0.0.43",
                                            nssa=dict(no_summary=True),
                                            ranges=[
                                                dict(
                                                    address="20.1.1.0/24",
                                                    advertise=False,
                                                )
                                            ],
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    graceful_restart=dict(set=True),
                                )
                            ],
                        )
                    ]
                ),
                state="replaced",
            )
        )
        commands = [
            "router ospfv3 vrf vrf02",
            "address-family ipv6",
            "no area 0.0.0.1 stub",
            "no distance ospf intra-area 200",
            "no fips restrictions",
            "no router-id",
            "no timers out-delay 10",
            "no timers throttle spf 56 56 56",
            "area 0.0.0.43 nssa no-summary",
            "area 0.0.0.43 range 20.1.1.0/24 not-advertise",
            "default-information originate route-map DefaultRouteFilter",
            "graceful-restart",
            "exit",
            "area 0.0.0.20 authentication ipsec spi 33 sha1 passphrase 7 4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
            "log-adjacency-changes detail",
            "exit",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv3_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="vrf01",
                            bfd=dict(all_interfaces=True),
                            log_adjacency_changes=dict(detail=True),
                            areas=[
                                dict(
                                    area_id="0.0.0.0",
                                    encryption=dict(
                                        algorithm="sha1",
                                        hidden_key=True,
                                        passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                        encryption="null",
                                        spi=44,
                                    ),
                                )
                            ],
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    fips_restrictions=True,
                                    redistribute=[
                                        dict(
                                            routes="connected",
                                            route_map="MAP01",
                                        )
                                    ],
                                    passive_interface=True,
                                    maximum_paths=100,
                                ),
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    areas=[
                                        dict(
                                            area_id="0.0.0.10",
                                            nssa=dict(no_summary=True),
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    max_metric=dict(
                                        router_lsa=dict(
                                            external_lsa=dict(
                                                max_metric_value=25
                                            ),
                                            summary_lsa=dict(set=True),
                                        )
                                    ),
                                ),
                            ],
                        )
                    ]
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv3_overridden_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="default",
                            adjacency=dict(exchange_start=dict(threshold=11)),
                            areas=[
                                dict(stub=dict(set=True), area_id="0.0.0.20"),
                                dict(
                                    area_id="0.0.0.40",
                                    stub=dict(set=True),
                                    default_cost=45,
                                ),
                            ],
                            timers=dict(pacing=7),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    fips_restrictions=True,
                                    redistribute=[dict(routes="connected")],
                                ),
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    router_id="10.1.1.1",
                                ),
                            ],
                        ),
                        dict(
                            vrf="vrf01",
                            bfd=dict(all_interfaces=True),
                            log_adjacency_changes=dict(detail=True),
                            areas=[
                                dict(
                                    area_id="0.0.0.0",
                                    encryption=dict(
                                        algorithm="sha1",
                                        hidden_key=True,
                                        passphrase="7hl8FV3lZ6H1mAKpjL47hQ==",
                                        encryption="null",
                                        spi=44,
                                    ),
                                )
                            ],
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    fips_restrictions=True,
                                    redistribute=[
                                        dict(
                                            routes="connected",
                                            route_map="MAP01",
                                        )
                                    ],
                                    passive_interface=True,
                                    maximum_paths=100,
                                ),
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    areas=[
                                        dict(
                                            area_id="0.0.0.10",
                                            nssa=dict(no_summary=True),
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    max_metric=dict(
                                        router_lsa=dict(
                                            external_lsa=dict(
                                                max_metric_value=25
                                            ),
                                            summary_lsa=dict(set=True),
                                        )
                                    ),
                                ),
                            ],
                        ),
                        dict(
                            vrf="vrf02",
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    areas=[
                                        dict(
                                            area_id="0.0.0.1",
                                            stub=dict(set=True),
                                        )
                                    ],
                                    distance=200,
                                    router_id="10.17.0.3",
                                    timers=dict(
                                        out_delay=10,
                                        throttle=dict(
                                            initial=56,
                                            max=56,
                                            min=56,
                                            spf=True,
                                        ),
                                    ),
                                )
                            ],
                        ),
                    ]
                ),
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_ospfv3_overridden(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="default",
                            adjacency=dict(exchange_start=dict(threshold=11)),
                            areas=[
                                dict(stub=dict(set=True), area_id="0.0.0.20"),
                                dict(
                                    area_id="0.0.0.40",
                                    stub=dict(set=True),
                                    default_cost=45,
                                ),
                            ],
                            timers=dict(pacing=7),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    fips_restrictions=True,
                                    redistribute=[dict(routes="connected")],
                                ),
                                dict(
                                    afi="ipv6",
                                    fips_restrictions=True,
                                    router_id="10.1.1.1",
                                ),
                            ],
                        ),
                        dict(
                            vrf="vrf02",
                            areas=[
                                dict(
                                    area_id="0.0.0.20",
                                    authentication=dict(
                                        algorithm="sha1",
                                        spi="33",
                                        hidden_key=True,
                                        passphrase="4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
                                    ),
                                )
                            ],
                            log_adjacency_changes=dict(detail=True),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv6",
                                    areas=[
                                        dict(
                                            area_id="0.0.0.43",
                                            nssa=dict(no_summary=True),
                                            ranges=[
                                                dict(
                                                    address="20.1.1.0/24",
                                                    advertise=False,
                                                )
                                            ],
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    graceful_restart=dict(set=True),
                                )
                            ],
                        ),
                    ]
                ),
                state="overridden",
            )
        )
        commands = [
            "router ospfv3 vrf vrf02",
            "address-family ipv6",
            "no area 0.0.0.1 stub",
            "no distance ospf intra-area 200",
            "no fips restrictions",
            "no router-id",
            "no timers out-delay 10",
            "no timers throttle spf 56 56 56",
            "area 0.0.0.43 nssa no-summary",
            "area 0.0.0.43 range 20.1.1.0/24 not-advertise",
            "default-information originate route-map DefaultRouteFilter",
            "graceful-restart",
            "exit",
            "area 0.0.0.20 authentication ipsec spi 33 sha1 passphrase 7 4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
            "log-adjacency-changes detail",
            "exit",
            "no router ospfv3 vrf vrf01",
        ]

        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv3_deleted(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[dict(vrf="default"), dict(vrf="vrf02")]
                ),
                state="deleted",
            )
        )
        commands = ["no router ospfv3 vrf vrf02", "no router ospfv3"]

        self.execute_module(changed=True, commands=commands)

    def test_eos_ospfv3_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            vrf="default",
                            areas=[
                                dict(
                                    area_id="0.0.0.20",
                                    authentication=dict(
                                        algorithm="sha1",
                                        spi="33",
                                        hidden_key=True,
                                        passphrase="4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
                                    ),
                                )
                            ],
                            timers=dict(pacing=7),
                        ),
                        dict(
                            vrf="vrf03",
                            log_adjacency_changes=dict(detail=True),
                            fips_restrictions=True,
                            address_family=[
                                dict(
                                    afi="ipv6",
                                    areas=[
                                        dict(
                                            area_id="0.0.0.43",
                                            nssa=dict(no_summary=True),
                                            ranges=[
                                                dict(
                                                    address="20.1.1.0/24",
                                                    advertise=False,
                                                )
                                            ],
                                        )
                                    ],
                                    default_information=dict(
                                        originate=True,
                                        route_map="DefaultRouteFilter",
                                    ),
                                    graceful_restart=dict(set=True),
                                )
                            ],
                        ),
                    ]
                ),
                state="rendered",
            )
        )
        commands = [
            "router ospfv3",
            "area 0.0.0.20 authentication ipsec spi 33 sha1 passphrase 7 4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
            "timers pacing flood 7",
            "exit",
            "router ospfv3 vrf vrf03",
            "fips restrictions",
            "log-adjacency-changes detail",
            "address-family ipv6",
            "area 0.0.0.43 nssa no-summary",
            "area 0.0.0.43 range 20.1.1.0/24 not-advertise",
            "default-information originate route-map DefaultRouteFilter",
            "graceful-restart",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_eos_ospfv3_parsed(self):
        commands = [
            "router ospfv3",
            "area 0.0.0.20 authentication ipsec spi 33 sha1 passphrase 7 4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
            "timers pacing flood 7",
            "exit",
            "router ospfv3 vrf vrf03",
            "fips restrictions",
            "log-adjacency-changes detail",
            "address-family ipv6",
            "area 0.0.0.43 nssa no-summary",
            "area 0.0.0.43 range 20.1.1.0/24 not-advertise",
            "default-information originate route-map DefaultRouteFilter",
            "graceful-restart",
            "exit",
            "exit",
        ]

        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = {
            "processes": [
                {
                    "vrf": "default",
                    "areas": [
                        {
                            "area_id": "0.0.0.20",
                            "authentication": {
                                "algorithm": "sha1",
                                "spi": 33,
                                "hidden_key": True,
                                "passphrase": "4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
                            },
                        }
                    ],
                    "timers": {"pacing": 7},
                },
                {
                    "vrf": "vrf03",
                    "log_adjacency_changes": {"detail": True},
                    "fips_restrictions": True,
                    "address_family": [
                        {
                            "afi": "ipv6",
                            "areas": [
                                {
                                    "area_id": "0.0.0.43",
                                    "nssa": {"no_summary": True},
                                    "ranges": [
                                        {
                                            "address": "20.1.1.0/24",
                                            "advertise": False,
                                        }
                                    ],
                                }
                            ],
                            "default_information": {
                                "originate": True,
                                "route_map": "DefaultRouteFilter",
                            },
                            "graceful_restart": {"set": True},
                        }
                    ],
                },
            ]
        }
        self.assertEqual(sorted(parsed_list), sorted(result["parsed"]))

    def test_eos_ospfv3_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(
            changed=False, filename="eos_ospfv3_config_gather.cfg"
        )
        gather_list = {
            "processes": [
                {
                    "vrf": "default",
                    "areas": [
                        {
                            "area_id": "0.0.0.20",
                            "authentication": {
                                "algorithm": "sha1",
                                "spi": 33,
                                "hidden_key": True,
                                "passphrase": "4O8T3zo4xBdRWXBnsnK934o9SEb+jEhHUN6+xzZgCo2j9EnQBUvtwNxxLEmYmm6w",
                            },
                        }
                    ],
                    "timers": {"pacing": 7},
                },
                {
                    "vrf": "vrf03",
                    "log_adjacency_changes": {"detail": True},
                    "fips_restrictions": True,
                    "address_family": [
                        {
                            "afi": "ipv6",
                            "areas": [
                                {
                                    "area_id": "0.0.0.43",
                                    "nssa": {"no_summary": True},
                                    "ranges": [
                                        {
                                            "address": "20.1.1.0/24",
                                            "advertise": False,
                                        }
                                    ],
                                }
                            ],
                            "default_information": {
                                "originate": True,
                                "route_map": "DefaultRouteFilter",
                            },
                            "graceful_restart": {"set": True},
                        }
                    ],
                },
            ]
        }
        self.assertEqual(sorted(gather_list), sorted(result["gathered"]))
