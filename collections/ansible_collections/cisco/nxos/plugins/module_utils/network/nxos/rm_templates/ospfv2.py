from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_area_range(arange):
    command = "area {area} range {range}".format(**arange)
    if arange.get("not_advertise") is True:
        command += " not-advertise"
    if "cost" in arange:
        command += " cost {cost}".format(**arange)
    return command


def _tmplt_default_information(proc):
    command = "default-information originate"
    if (
        "always" in proc["default_information"]
        and proc["default_information"]["always"]
    ):
        command += " always"
    if "route_map" in proc["default_information"]:
        command += " route-map"
        command += " {default_information[route_map]}".format(**proc)
    return command


def _tmplt_log_adjacency_changes(proc):
    command = "log-adjacency-changes"
    if proc.get("log_adjacency_changes").get("detail", False) is True:
        command += " detail"
    return command


def _tmplt_area_authentication(area):
    command = "area {area_id} authentication".format(**area)
    if area.get("authentication", {}).get("message_digest"):
        command += " message-digest"
    return command


def _tmplt_max_lsa(proc):
    max_lsa = proc["max_lsa"]
    command = "max-lsa {max_non_self_generated_lsa}".format(**max_lsa)
    if max_lsa.get("threshold"):
        command += " {threshold}".format(**max_lsa)
    if max_lsa.get("warning_only"):
        command += " warning-only"
    if max_lsa.get("ignore_time"):
        command += " ignore-time {ignore_time}".format(**max_lsa)
    if max_lsa.get("ignore_count"):
        command += " ignore-count {ignore_count}".format(**max_lsa)
    if max_lsa.get("reset_time"):
        command += " reset-time {reset_time}".format(**max_lsa)
    return command


def _tmplt_default_information(proc):
    default_information = proc["default_information"]["originate"]
    command = "default-information originate"

    if default_information.get("set") is False:
        command = "no {0}".format(command)
    else:
        if default_information.get("always"):
            command += " always"
        if default_information.get("route_map"):
            command += " route-map {route_map}".format(**default_information)

    return command


def _tmplt_table_map(proc):
    table_map = proc["table_map"]
    command = "table-map"

    if table_map.get("name"):
        command += " {name}".format(**table_map)
    if table_map.get("filter"):
        command += " filter"

    return command


def _tmplt_max_metric(proc):
    max_metric = proc["max_metric"]
    command = "max-metric router-lsa"

    if max_metric.get("router_lsa", {}).get("set") is False:
        command = "no {0}".format(command)
    else:
        external_lsa = max_metric.get("router_lsa", {}).get("external_lsa", {})
        include_stub = max_metric.get("router_lsa", {}).get("include_stub", {})
        on_startup = max_metric.get("router_lsa", {}).get("on_startup", {})
        summary_lsa = max_metric.get("router_lsa", {}).get("summary_lsa", {})
        if external_lsa:
            command += " external-lsa"
            if external_lsa.get("max_metric_value"):
                command += " {max_metric_value}".format(**external_lsa)
        if include_stub:
            command += " include-stub"
        if on_startup:
            command += " on-startup"
            if on_startup.get("wait_period"):
                command += " {wait_period}".format(**on_startup)
            if on_startup.get("wait_for_bgp_asn"):
                command += " wait-for bgp {wait_for_bgp_asn}".format(
                    **on_startup
                )
        if summary_lsa:
            command += " summary-lsa"
            if summary_lsa.get("max_metric_value"):
                command += " {max_metric_value}".format(**summary_lsa)

    return command


def _tmplt_area_nssa(area):
    nssa = area["nssa"]
    command = "area {area_id} nssa".format(**area)
    if nssa.get("set") is False:
        command = "no {0}".format(command)
    else:
        for attrib in [
            "no_summary",
            "no_redistribution",
            "default_information_originate",
        ]:
            if nssa.get(attrib):
                command += " {0}".format(attrib.replace("_", "-"))
    return command


def _tmplt_area_nssa_translate(area):
    translate = area["nssa"]["translate"]["type7"]
    command = "area {area_id} nssa translate type7".format(**area)
    for attrib in ["always", "never", "supress_fa"]:
        if translate.get(attrib):
            command += " {0}".format(attrib.replace("_", "-"))
    return command


def _tmplt_area_ranges(arange):
    command = "area {area_id} range {prefix}".format(**arange)
    if arange.get("not_advertise") is True:
        command += " not-advertise"
    if "cost" in arange:
        command += " cost {cost}".format(**arange)
    return command


def _tmplt_area_ranges(arange):
    command = "area {area_id} range {prefix}".format(**arange)
    if arange.get("not_advertise") is True:
        command += " not-advertise"
    if "cost" in arange:
        command += " cost {cost}".format(**arange)
    return command


def _tmplt_summary_address(proc):
    command = "summary-address {prefix}".format(**proc)
    if proc.get("tag"):
        command += " tag {tag}".format(**proc)
    elif proc.get("not_advertise"):
        command += " not-advertise"
    return command


def _tmplt_area_stub(area):
    stub = area["stub"]
    command = "area {area_id} stub".format(**area)
    if stub.get("set") is False:
        command = "no {0}".format(command)
    elif stub.get("no_summary"):
        command += " no-summary"
    return command


def _tmplt_redistribute(redis):
    command = "redistribute {protocol}".format(**redis)
    if redis.get("id"):
        command += " {id}".format(**redis)
    if redis.get("route_map"):
        command += " route-map {route_map}".format(**redis)
    return command


def _tmplt_capability_vrf_lite(proc):
    command = "capability vrf-lite"
    vrf_lite = proc["capability"]["vrf_lite"]
    if vrf_lite.get("set") is False:
        command = "no {0}".format(command)
    else:
        if vrf_lite.get("evpn"):
            command += " evpn"
    return command


class Ospfv2Template(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospfv2Template, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            "name": "vrf",
            "getval": re.compile(
                r"""
                \s+vrf
                \s(?P<vrf>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "vrf {{ vrf }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "vrf": "{{ vrf }}"
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \s+(?P<bfd>bfd)$""",
                re.VERBOSE,
            ),
            "setval": "bfd",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "bfd": "{{ not not bfd }}"
                    }
                }
            },
        },
        {
            "name": "process_id",
            "getval": re.compile(
                r"""
                ospf(?:v3)*\s
                (?P<process_id>\S+)""",
                re.VERBOSE,
            ),
            "setval": "router ospf {{ process_id }}",
            "result": {
                "process_id": "{{ process_id }}",
            },
            "shared": True,
        },
        {
            "name": "down_bit_ignore",
            "getval": re.compile(
                r"""
                \s+(?P<down_bit_ignore>down-bit-ignore)$""",
                re.VERBOSE,
            ),
            "setval": "down-bit-ignore",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "down_bit_ignore": "{{ not not down_bit_ignore }}",
                    }
                }
            },
        },
        {
            "name": "capability.vrf_lite",
            "getval": re.compile(
                r"""
                \s+capability
                \s(?P<vrf_lite>vrf-lite)
                \s*(?P<evpn>evpn)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_capability_vrf_lite,
            "remval": "capability vrf-lite",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "capability": {
                            "vrf_lite": {
                                "set": "{{ True if vrf_lite is defined and evpn is undefined else None }}",
                                "evpn": "{{ not not evpn }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "auto_cost",
            "getval": re.compile(
                r"""
                \s+auto-cost\sreference-bandwidth\s
                (?P<acrb>\d+)\s(?P<unit>\S+)$""",
                re.VERBOSE,
            ),
            "setval": (
                "auto-cost reference-bandwidth"
                " {{ auto_cost.reference_bandwidth }}"
                " {{ auto_cost.unit }}"
            ),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "auto_cost": {
                            "reference_bandwidth": "{{ acrb }}",
                            "unit": "{{ unit }}",
                        }
                    }
                }
            },
        },
        {
            "name": "flush_routes",
            "getval": re.compile(
                r"""
                \s+(?P<flush_routes>flush-routes)$""",
                re.VERBOSE,
            ),
            "setval": "flush-routes",
            "result": {
                "flush_routes": "{{ not not flush_routes }}"
            },
        },
        {
            "name": "graceful_restart.set",
            "getval": re.compile(
                r"""
                \s+(?P<graceful_restart>no\sgraceful-restart)
                $""",
                re.VERBOSE,
            ),
            "setval": "graceful-restart",
            "remval": "no graceful-restart",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "graceful_restart": {
                            "set": "{{ not graceful_restart }}"
                        }
                    }
                }
            },
        },
        {
            "name": "graceful_restart.helper_disable",
            "getval": re.compile(
                r"""
                \s+graceful-restart
                \s+(?P<helper_disable>helper-disable)
                $""",
                re.VERBOSE,
            ),
            "setval": "graceful-restart helper-disable",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "graceful_restart": {
                            "helper_disable": "{{ not not helper_disable }}",
                        }
                    }
                }
            },
        },
        {
            "name": "graceful_restart.grace_period",
            "getval": re.compile(
                r"""
                \s+graceful-restart
                \s+grace-period
                \s+(?P<grace_period>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "graceful-restart helper-disable",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "graceful_restart": {
                            "grace_period": "{{ grace_period }}",
                        }
                    }
                }
            },
        },
        {
            "name": "isolate",
            "getval": re.compile(
                r"""
                \s+(?P<isolate>isolate)$""",
                re.VERBOSE,
            ),
            "setval": "isolate",
            "result": {"isolate": "{{ not not isolate }}"},
        },
        {
            "name": "log_adjacency_changes",
            "getval": re.compile(
                r"""
                \s+(?P<log>log-adjacency-changes)
                \s*(?P<detail>detail)*$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_log_adjacency_changes,
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "log_adjacency_changes": {
                            "log": "{{ True if log is defined and detail is undefined else None }}",
                            "detail": "{{ True if detail is defined else None }}",
                        }
                    }
                }
            },
        },
        {
            "name": "max_lsa",
            "getval": re.compile(
                r"""
                \s+max-lsa
                \s(?P<max_gen_lsa>\d+)
                \s*(?P<threshold>\d*)
                \s*(?P<warning_only>warning-only)*
                \s*(ignore-time)*\s*(?P<ig_time>\d*)
                \s*(ignore-count)*\s*(?P<ig_count>\d*)
                \s*(reset-time)*\s*(?P<rst_time>\d*)
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_max_lsa,
            "remval": "max-lsa {{ max_lsa.max_non_self_generated_lsa }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "max_lsa": {
                            "max_non_self_generated_lsa": "{{ max_gen_lsa }}",
                            "threshold": "{{ threshold }}",
                            "ignore_time": "{{ ig_time }}",
                            "ignore_count": "{{ ig_count }}",
                            "reset_time": "{{ rst_time }}",
                            "warning_only": "{{ not not warning_only }}",
                        }
                    }
                }
            },
        },
        {
            "name": "mpls.traffic_eng.areas",
            "getval": re.compile(
                r"""
                \s+mpls\straffic-eng\sarea
                \s(?P<area_id>\S+)$""",
                re.VERBOSE,
            ),
            "setval": ("mpls traffic-eng area {{ area_id }}"),
            "result": {
                "mpls": {
                    "traffic_eng": {
                        "areas": [
                            {
                                "area_id": "{{ area_id }}",
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "mpls.traffic_eng.router_id",
            "getval": re.compile(
                r"""
                \s+mpls\straffic-eng\srouter-id
                \s(?P<router_id>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": (
                "mpls traffic-eng router-id" " {{ mpls.traffic_eng.router_id }}"
            ),
            "result": {"mpls": {"traffic_eng": {"router_id": "{{ router_id }}"}}},
        },
        {
            "name": "mpls.traffic_eng.multicast_intact",
            "getval": re.compile(
                r"""
                \s+mpls\straffic-eng
                \s(?P<multicast_intact>multicast-intact)
                $""",
                re.VERBOSE,
            ),
            "setval": ("mpls traffic-eng multicast-intact"),
            "result": {
                "mpls": {
                    "traffic_eng": {
                        "multicast_intact": "{{ not not multicast_intact }}"
                    }
                }
            },
        },
        {
            "name": "name_lookup",
            "getval": re.compile(
                r"""
                \s+(?P<name_lookup>name-lookup)
                $""",
                re.VERBOSE,
            ),
            "setval": ("name-lookup"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "name_lookup": "{{ not not name_lookup }}"
                    }
                }
            },
        },
        {
            "name": "passive_interface.default",
            "getval": re.compile(
                r"""
                \s+passive-interface
                \s+(?P<default>default)
                $""",
                re.VERBOSE,
            ),
            "setval": ("passive-interface default"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "passive_interface": {"default": "{{ not not default }}"}
                    }
                }
            },
        },
        {
            "name": "rfc1583compatibility",
            "getval": re.compile(
                r"""
                \s+(?P<rfc>rfc1583compatibility)$""",
                re.VERBOSE,
            ),
            "setval": ("rfc1583compatibility"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "rfc1583compatibility": "{{ not not rfc }}"
                    }
                }
            },
        },
        {
            "name": "router_id",
            "getval": re.compile(
                r"""
                \s+router-id
                \s(?P<router_id>\S+)$""",
                re.VERBOSE,
            ),
            "setval": ("router-id" " {{ router_id }}"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "router_id": "{{ router_id }}"
                    }
                }
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s+(?P<shutdown>shutdown)$""",
                re.VERBOSE,
            ),
            "setval": ("shutdown"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "shutdown": "{{ not not shutdown }}"
                    }
                }
            },
        },
        {
            "name": "default_information.originate",
            "getval": re.compile(
                r"""
                \s+default-information
                \s(?P<originate>originate)
                \s*(?P<always>always)*
                \s*(route-map)*
                \s*(?P<route_map>\S+)*$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_default_information,
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "default_information": {
                            "originate": {
                                "set": "{{ True if originate is defined and always is undefined and route_map is undefined else None }}",
                                "always": "{{ not not always }}",
                                "route_map": "{{ route_map }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""
                \s+default-metric
                \s(?P<default_metric>\d+)$""",
                re.VERBOSE,
            ),
            "setval": ("default-metric {{ default_metric }}"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "default_metric": "{{ default_metric }}"
                    }
                }
            },
        },
        {
            "name": "distance",
            "getval": re.compile(
                r"""
                \s+distance
                \s(?P<distance>\d+)$""",
                re.VERBOSE,
            ),
            "setval": ("distance {{ distance }}"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "distance": "{{ distance }}"
                    }
                }
            },
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""
                \s+table-map
                \s(?P<rmap>\S+)
                \s*(?P<filter>filter)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_table_map,
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "table_map": {
                            "name": "{{ rmap }}",
                            "filter": "{{ not not filter }}",
                        }
                    }
                }
            },
        },
        {
            "name": "timers.lsa_arrival",
            "getval": re.compile(
                r"""
                \s+timers
                \slsa-arrival
                \s(?P<lsa_arrival_val>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": ("timers lsa-arrival {{ timers.lsa_arrival }}"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "timers": {
                            "lsa_arrival": "{{ lsa_arrival_val }}"
                        }
                    }
                }
            },
        },
        {
            "name": "timers.lsa_group_pacing",
            "getval": re.compile(
                r"""
                \s+timers
                \slsa-group-pacing
                \s(?P<lsa_group_pacing>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "timers lsa-group-pacing {{ timers.lsa_group_pacing }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "timers": {
                            "lsa_group_pacing": "{{ lsa_group_pacing }}"
                        }
                    }
                }
            },
        },
        {
            "name": "timers.throttle.lsa",
            "getval": re.compile(
                r"""
                \s+timers\sthrottle\slsa
                \s(?P<start>\d+)
                \s(?P<hold>\d+)
                \s(?P<max>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "timers throttle lsa {{ timers.throttle.lsa.start_interval }}"
            " {{ timers.throttle.lsa.hold_interval }}"
            " {{ timers.throttle.lsa.max_interval }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "timers": {
                            "throttle": {
                                "lsa": {
                                    "start_interval": "{{ start }}",
                                    "hold_interval": "{{ hold }}",
                                    "max_interval": "{{ max }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "timers.throttle.spf",
            "getval": re.compile(
                r"""
                \s+timers\sthrottle\sspf
                \s(?P<initial>\d+)
                \s(?P<min>\d+)
                \s(?P<max>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "timers throttle spf {{ timers.throttle.spf.initial_spf_delay }}"
            " {{ timers.throttle.spf.min_hold_time }}"
            " {{ timers.throttle.spf.max_wait_time }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "timers": {
                            "throttle": {
                                "spf": {
                                    "initial_spf_delay": "{{ initial }}",
                                    "min_hold_time": "{{ min }}",
                                    "max_wait_time": "{{ max }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.default_cost",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)\s
                default-cost\s(?P<default_cost>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} default-cost {{ default_cost }}",
            "compval": "default_cost",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "default_cost": "{{ default_cost|int }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.authentication",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)
                \s(?P<auth>authentication)
                \s*(?P<md>message-digest)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_area_authentication,
            "remval": "area {{ area_id }} authentication",
            "compval": "authentication",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "authentication": {
                                    "set": "{{ True if auth is defined and md is undefined }}",
                                    "message_digest": "{{ True if md is defined else False }}"
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.filter_list",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)
                \sfilter-list
                \sroute-map\s(?P<rmap>\S+)
                \s(?P<dir>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} filter-list route-map {{ route_map }} {{ direction }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "filter_list": [
                                    {
                                        "route_map": "{{ rmap }}",
                                        "direction": "{{ dir }}",
                                    },
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "redistribute",
            "getval": re.compile(
                r"""
                \s+redistribute
                \s(?P<protocol>\S+)
                \s*(?P<id>\S+)*
                \sroute-map\s(?P<rmap>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_redistribute,
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "redistribute": [
                            {
                                "protocol": "{{ protocol }}",
                                "id": "{{ id }}",
                                "route_map": "{{ rmap }}",
                            },
                        ]
                    }
                }
            },
        },
        {
            "name": "area.nssa",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)
                \s(?P<nssa>nssa)
                \s*(?P<no_sum>no-summary)*
                \s*(?P<no_redis>no-redistribution)*
                \s*(?P<def_info>default-information-originate)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_area_nssa,
            "remval": "area {{ area_id }} nssa",
            "compval": "nssa",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "set": "{{ True if nssa is defined and no_sum is undefined and no_redis is undefined and def_info is undefined }}",
                                    "no_summary": "{{ not not no_sum }}",
                                    "no_redistribution": "{{ not not no_redis }}",
                                    "default_information_originate": "{{ not not def_info }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.nssa.translate",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)\snssa
                \stranslate
                \stype7
                \s(?P<choice>always|never)
                \s*(?P<supress_fa>supress-fa)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_area_nssa_translate,
            "compval": "nssa.translate",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "translate": {
                                        "type7": {
                                            "always": '{{ True if choice == "always" else None }}',
                                            "never": '{{ True if choice == "never" else None }}',
                                            "supress_fa": "{{ not not supress_fa }}",
                                        }
                                    }
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.ranges",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)
                \srange\s(?P<prefix>\S+)
                \s*(cost)*\s*(?P<cost>\d+)*
                \s*(?P<not_adver>not-advertise)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_area_ranges,
            "remval": "area {{ area_id }} range {{ prefix }}",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "ranges": [
                                    {
                                        "prefix": "{{ prefix }}",
                                        "cost": "{{ cost }}",
                                        "not_advertise": "{{ not not not_adver }}",
                                    },
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "summary_address",
            "getval": re.compile(
                r"""
                \s+summary-address
                \s(?P<prefix>\S+)
                \s*(?P<not_adver>not-advertise)*
                \s*(tag)*\s*(?P<tag>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_summary_address,
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "summary_address": [
                            {
                                "prefix": "{{ prefix }}",
                                "not_advertise": "{{ not not not_adver }}",
                                "tag": "{{ tag }}",
                            },
                        ]
                    }
                }
            },
        },
        {
            "name": "area.stub",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)
                \s(?P<stub>stub)
                \s*(?P<no_summary>no-summary)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_area_stub,
            "remval": "area {{ area_id }} stub",
            "compval": "stub",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "stub": {
                                    "set": "{{ True if stub is defined and no_summary is undefined else None }}",
                                    "no_summary": "{{ not not no_summary }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "maximum_paths",
            "getval": re.compile(
                r"""
                \s+maximum-paths
                \s(?P<maximum_paths>\d+)$""",
                re.VERBOSE,
            ),
            "setval": ("maximum-paths {{ maximum_paths }}"),
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {"maximum_paths": "{{ maximum_paths }}"}
                }
            },
        },
        {
            "name": "max_metric",
            "getval": re.compile(
                r"""
                \s+max-metric
                \s+(?P<router_lsa>router-lsa)
                \s*(?P<external_lsa>external-lsa)*
                \s*(?P<max_metric_value>\d+)*
                \s*(?P<include_stub>include-stub)*
                \s*(?P<on_startup>on-startup)*
                \s*(?P<wait_period>\d+)*
                \s*(wait-for\sbgp)*
                \s*(?P<bgp_asn>\d+)*
                \s*(?P<summary_lsa>summary-lsa)*
                \s*(?P<sum_lsa_max_metric_value>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_max_metric,
            "remval": "max-metric router-lsa",
            "result": {
                "vrfs": {
                    '{{ "vrf_" + vrf|d() }}': {
                        "max_metric": {
                            "router_lsa": {
                                "set": "{{ True if router_lsa is defined and external_lsa is undefined else None }}",
                                "external_lsa": {
                                    "set": "{{ True if external_lsa is defined and max_metric_value is undefined else None }}",
                                    "max_metric_value": "{{ max_metric_value }}",
                                },
                                "include_stub": "{{ not not include_stub }}",
                                "on_startup": {
                                    "set": "{{ True if on_startup is defined and (wait_period and bgp_asn) is undefined else None }}",
                                    "wait_period": "{{ wait_period }}",
                                    "wait_for_bgp_asn": "{{ bgp_asn }}",
                                },
                                "summary_lsa": {
                                    "set": "{{ True if summary_lsa is defined and sum_lsa_max_metric_value is undefined else None }}",
                                    "max_metric_value": "{{ sum_lsa_max_metric_value }}",
                                },
                            }
                        }
                    }
                }
            },
        },
    ]
    # fmt: on
