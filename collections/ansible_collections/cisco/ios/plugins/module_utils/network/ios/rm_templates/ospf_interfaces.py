# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Ospf_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_ospf_interface(config_data):
    command = "interface {name}".format(**config_data)
    return command


def _tmplt_ospf_interface_process(config_data):
    if "process" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf {id} area {area_id}".format(
                **config_data["process"]
            )
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf {id} area {area_id}".format(
                **config_data["process"]
            )
        if "secondaries" in config_data["process"]:
            command += " secondaries"
    return command


def _tmplt_ip_ospf_authentication(config_data):
    if "authentication" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf authentication"
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf authentication"
        if "key_chain" in config_data["authentication"]:
            command += " key-chain {key_chain}".format(
                **config_data["authentication"]
            )
        elif "message_digest" in config_data["authentication"]:
            command += " message-digest"
        elif "null" in config_data["authentication"]:
            command += " null"
    return command


def _tmplt_ip_ospf_cost(config_data):
    if "cost" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf cost {interface_cost}".format(
                **config_data["cost"]
            )
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf cost"
            if "interface_cost" in config_data["cost"]:
                command = "ipv6 ospf cost {interface_cost}".format(
                    **config_data["cost"]
                )
            if "dynamic_cost" in config_data["cost"]:
                if "default" in config_data["cost"]["dynamic_cost"]:
                    command += " dynamic default {default}".format(
                        **config_data["cost"]["dynamic_cost"]
                    )
                elif "hysteresis" in config_data["cost"]["dynamic_cost"]:
                    command += " dynamic hysteresis"
                    if (
                        "percent"
                        in config_data["cost"]["dynamic_cost"]["hysteresis"]
                    ):
                        command += " percent {percent}".format(
                            **config_data["cost"]["dynamic_cost"]["hysteresis"]
                        )
                    elif (
                        "threshold"
                        in config_data["cost"]["dynamic_cost"]["hysteresis"]
                    ):
                        command += " threshold {threshold}".format(
                            **config_data["cost"]["dynamic_cost"]["hysteresis"]
                        )
                elif "weight" in config_data["cost"]["dynamic_cost"]:
                    command += " dynamic weight"
                    if (
                        "l2_factor"
                        in config_data["cost"]["dynamic_cost"]["weight"]
                    ):
                        command += " L2-factor {l2_factor}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
                    elif (
                        "latency"
                        in config_data["cost"]["dynamic_cost"]["weight"]
                    ):
                        command += " latency {latency}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
                    elif (
                        "oc" in config_data["cost"]["dynamic_cost"]["weight"]
                        and config_data["cost"]["dynamic_cost"]["weight"]["oc"]
                    ):
                        command += " oc cdr"
                    elif (
                        "resources"
                        in config_data["cost"]["dynamic_cost"]["weight"]
                    ):
                        command += " resources {resources}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
                    elif (
                        "throughput"
                        in config_data["cost"]["dynamic_cost"]["weight"]
                    ):
                        command += " throughput {throughput}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
    return command


def _tmplt_ip_ospf_dead_interval(config_data):
    if "dead_interval" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf dead-interval"
            if "time" in config_data["dead_interval"]:
                command += " {time}".format(**config_data["dead_interval"])
            elif "minimal" in config_data["dead_interval"]:
                command += " minimal hello-multiplier {minimal}".format(
                    **config_data["dead_interval"]
                )
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf dead-interval {time}".format(
                **config_data["dead_interval"]
            )
    return command


def _tmplt_ip_ospf_demand_circuit(config_data):
    if "demand_circuit" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf demand-circuit"
            if config_data["demand_circuit"]["ignore"]:
                command += " ignore"
            elif config_data["demand_circuit"]["enable"]:
                return command
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf demand-circuit"
            if config_data["demand_circuit"]["enable"]:
                return command
            elif config_data["demand_circuit"]["ignore"]:
                command += " ignore"
            elif config_data["demand_circuit"]["disable"]:
                command += " disable"
    return command


def _tmplt_ip_ospf_manet(config_data):
    if "manet" in config_data:
        command = "ipv6 ospf manet peering"
        if "cost" in config_data["manet"]:
            command += " cost"
            if "percent" in config_data["manet"]["cost"]:
                command += " percent {percent}".format(
                    **config_data["manet"]["cost"]
                )
            elif "threshold" in config_data["manet"]["cost"]:
                command += " threshold {threshold}".format(
                    **config_data["manet"]["cost"]
                )
        elif "link_metrics" in config_data["manet"]:
            command += " link-metrics"
            if "cost_threshold" in config_data["manet"]["link_metrics"]:
                command += " {cost_threshold}".format(
                    **config_data["manet"]["link_metrics"]
                )
    return command


def _tmplt_ip_ospf_multi_area(config_data):
    if "multi_area" in config_data:
        command = "ip ospf multi-area {id}".format(**config_data["multi_area"])
        if "cost" in config_data["multi_area"]:
            command += " cost {cost}".format(**config_data["multi_area"])
    return command


def _tmplt_ip_ospf_neighbor(config_data):
    if "neighbor" in config_data:
        command = "ipv6 ospf neighbor {address}".format(
            **config_data["neighbor"]
        )
    if "cost" in config_data["neighbor"]:
        command += " cost {cost}".format(**config_data["neighbor"])
    if (
        "database_filter" in config_data["neighbor"]
        and config_data["neighbor"]["database_filter"]
    ):
        command += " database-filter all out"
    if "poll_interval" in config_data["neighbor"]:
        command += " poll-interval {poll_interval}".format(
            **config_data["neighbor"]["poll_interval"]
        )
    if "priority" in config_data["neighbor"]:
        command += " priority {priority}".format(
            **config_data["neighbor"]["priority"]
        )
    return command


def _tmplt_ip_ospf_network(config_data):
    if "network" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf network"
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf network"
        if "broadcast" in config_data["network"]:
            command += " broadcast"
        if "manet" in config_data["network"]:
            command += " manet"
        if "non_broadcast" in config_data["network"]:
            command += " non-broadcast"
        if "point_to_multipoint" in config_data["network"]:
            command += " point-to-multipoint"
        if "point_to_point" in config_data["network"]:
            command += " point-to-point"
    return command


def _tmplt_ip_ospf_ttl_security(config_data):
    if "ttl_security" in config_data:
        command = "ip ospf ttl-security"
        if "hops" in config_data["ttl_security"]:
            command += " hops {hops}".format(**config_data["ttl_security"])
    return command


class Ospf_InterfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospf_InterfacesTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                  ^interface
                  \s(?P<name>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "interface {{ name }}",
            "result": {
                "{{ name }}": {"name": "{{ name }}", "address_family": {}}
            },
            "shared": True,
        },
        {
            "name": "process",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<id>\d+)*
                \s*(?P<area>area\s\d+)*
                \s*(?P<secondaries>secondaries)*

                \s*(?P<instance>instance*\s*\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_interface_process,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "process": {
                                "id": "{{ id }}",
                                "area_id": "{{ area.split(' ')[1] }}",
                                "secondaries": "{{ True if secondaries is defined }}",
                                "instance_id": "{{ instance.split(' ')[1]}}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "adjacency",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<adjacency>adjacency*\s*stagger)*
                \s*(?P<disable>disable)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} adjacency stagger disable",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "adjacency": "{{ True if adjacency is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*authentication*
                \s*(?P<key_chain>key-chain*\s*\S+)*
                \s*(?P<message_digest>message-digest)*
                \s*(?P<null>null)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_authentication,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "authentication": {
                                "key_chain": "{{ key_chain.split(' ')[1] }}",
                                "message_digest": "{{ True if message_digest is defined }}",
                                "null": "{{ True if null is defined }}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<bfd>bfd)*
                \s*(?P<disable>disable)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} bfd",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "bfd": "{{ True if bfd is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "cost_ip",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)*
                \s*ospf*
                \s*(?P<cost>cost*\s*\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_cost,
            "compval": "cost.interface_cost",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "cost": {
                                "interface_cost": "{{ cost.split(' ')[1] }}"
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "cost_ipv6_dynamic_cost",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ipv6)*
                \s*ospf*
                \s*cost*
                \s*(?P<interface_cost>\d+)*
                \s*dynamic*
                \s*(?P<default>default*\s*\d+)*
                \s*(?P<hysteresis>hysteresis*\s*)*
                \s*(?P<h_params>(percent|threshold)*\s*\d+)*
                \s*(?P<weight>weight)*
                \s*(?P<w_params>(L2-factor|latency|resources|throughput)*\s*\d+)*
                \s*(?P<weight_oc>oc)*
                $""",
                re.VERBOSE,
            ),
            "compval": "cost.dynamic_cost",
            "setval": _tmplt_ip_ospf_cost,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "cost": {
                                "interface_cost": "{{ interface_cost }}",
                                "dynamic_cost": {
                                    "default": "{{ default.split(' ')[1] }}",
                                    "hysteresis": {
                                        "percent": "{{ h_params.split(' ')[1] if h_params is defined and 'percent' in h_params }}",
                                        "threshold": "{{ h_params.split(' ')[1] if h_params is defined and 'threshold' in h_params  }}",
                                    },
                                    "weight": {
                                        "l2_factor": "{{ w_params.split(' ')[1] if w_params is defined and 'L2-factor' in w_params  }}",
                                        "latency": "{{ w_params.split(' ')[1] if w_params is defined and 'latency' in w_params  }}",
                                        "oc": "{{ True if weight_oc is defined}}",
                                        "resources": "{{ w_params.split(' ')[1] if w_params is defined and 'resources' in w_params  }}",
                                        "throughput": "{{ w_params.split(' ')[1] if w_params is defined and 'throughput' in w_params  }}",
                                    },
                                },
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "database_filter",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<database_filter>database-filter\sall\sout)*
                \s*(?P<disable>disable)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} database-filter all out",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "database_filter": "{{ True if database_filter is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "dead_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<dead_interval>dead-interval)*
                \s*(?P<seconds>\d+)*
                \s*(?P<minimal>minimal\shello-multiplier\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_dead_interval,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "dead_interval": {
                                "time": "{{ seconds }}",
                                "minimal": {
                                    "hello_multiplier": "{{ minimal.split(' ')[2] }}"
                                },
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "demand_circuit",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<demand_circuit>demand-circuit)*
                \s*(?P<ignore>ignore)*
                \s*(?P<disable>disable)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_demand_circuit,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "demand_circuit": {
                                "enable": "{{ True if demand_circuit is defined and ignore is not defined }}",
                                "ignore": "{{ True if ignore is defined }}",
                                "disable": "{{ True if disable is defined }}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "flood_reduction",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<flood_reduction>flood-reduction)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} flood-reduction",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "flood_reduction": "{{ True if flood_reduction is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "hello_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<hello_interval>hello-interval\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} hello-interval {{ hello_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "hello_interval": "{{ hello_interval.split(' ')[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "lls",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)*
                \s*ospf*
                \s*(?P<lls>lls)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} lls",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "lls": "{{ True if lls is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "manet",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ipv6)*
                \s*ospf*
                \s*(?P<manet>manet\speering)*
                \s*(?P<cost>(cost\spercent|cost\sthreshold)\s\d+)*
                \s*(?P<link_metrics>link-metrics\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_manet,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "manet": {
                                "cost": {
                                    "percent": "{{ cost.split(' ')[2] }}",
                                    "threshold": "{{ cost.split(' ')[2] }}",
                                },
                                "link_metrics": {
                                    "set": "{{ True if link_metrics is not defined and link_metrics is defined  }}",
                                    "cost_threshold": "{{ link_metrics.split(' ')[1] }}",
                                },
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "mtu_ignore",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<mtu_ignore>mtu-ignore)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} mtu-ignore",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "mtu_ignore": "{{ True if mtu_ignore is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "multi_area",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)*
                \s*ospf*
                \s*(?P<multi_area>multi-area\s\d+)*
                \s*(?P<cost>cost\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_multi_area,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "multi_area": {
                                "id": "{{ multi_area.split(' ')[1] }}",
                                "cost": "{{ cost.split(' ')[1] }}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ipv6)*
                \s*ospf*
                \s*neighbor*
                \s*(?P<address>(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+)*
                \s*(?P<cost>cost\s\d+)*
                \s*(?P<database_filter>database-filter\sall\sout)*
                \s*(?P<poll_interval>poll-interval\s\d+)*
                \s*(?P<priority>priority\s\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_neighbor,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "neighbor": {
                                "address": "{{ address }}",
                                "cost": "{{ cost.split(' ')[1] }}",
                                "database_filter": "{{ True if database_filter is defined }}",
                                "poll_interval": "{{ poll_interval.split(' ')[1] }}",
                                "priority": "{{ priority.split(' ')[1] }}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<network>network)*
                \s*(?P<broadcast>broadcast)*
                \s*(?P<manet>manet)*
                \s*(?P<non_broadcast>non-broadcast)*
                \s*(?P<point_to_multipoint>point-to-multipoint)*
                \s*(?P<point_to_point>point-to-point)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_network,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "network": {
                                "broadcast": "{{ True if broadcast is defined }}",
                                "manet": "{{ True if manet is defined }}",
                                "non_broadcast": "{{ True if non_broadcast is defined }}",
                                "point_to_multipoint": "{{ True if point_to_multipoint is defined }}",
                                "point_to_point": "{{ True if point_to_point is defined }}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "prefix_suppression",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<prefix_suppression>prefix-suppression)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} prefix-suppression",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "prefix_suppression": "{{ True if prefix_suppression is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<priority>priority*\s*\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} priority {{ priority }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "priority": "{{ priority.split(' ')[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "resync_timeout",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)*
                \s*ospf*
                \s*(?P<resync_timeout>resync-timeout*\s*\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "ip ospf resync-timeout {{ resync_timeout }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "resync_timeout": "{{ resync_timeout.split(' ')[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "retransmit_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<retransmit_interval>retransmit-interval*\s*\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} retransmit-interval {{ retransmit_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "retransmit_interval": "{{ retransmit_interval.split(' ')[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)*
                \s*ospf*
                \s*(?P<shutdown>shutdown)*
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} shutdown",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "shutdown": "{{ True if shutdown is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "transmit_delay",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ipv6)*
                \s*ospf*
                \s*(?P<transmit_delay>transmit-delay*\s*\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "ipv6 ospf transmit-delay {{ transmit_delay }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "transmit_delay": "{{ transmit_delay.split(' ')[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)*
                \s*ospf*
                \s*(?P<ttl_security>ttl-security)*
                \s*(?P<hops>hops\s\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_ttl_security,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "ttl_security": {
                                "set": "{{ True if hops is not defined and ttl_security is defined }}",
                                "hops": "{{ hops.split(' ')[1] }}",
                            },
                        }
                    }
                }
            },
        },
    ]
