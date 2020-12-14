from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_ospfv3_cmd(process):

    command = "router ospfv3 {process_id}".format(**process)
    if "vrf" in process:
        command += " vrf {vrf}".format(**process)
    return command


def _tmplt_ospf_adjacency_cmd(config_data):
    if "adjacency" in config_data:
        command = "adjacency stagger"
        if "none" in config_data["adjacency"]:
            command += " none"
        else:
            command += " {min_adjacency}".format(**config_data["adjacency"])
        if "max_adjacency" in config_data["adjacency"]:
            command += " {min_adjacency}".format(**config_data["adjacency"])
        return command


def _tmplt_ospf_address_family_cmd(config_data):
    if "address_family" in config_data:
        command = []
        # for config_data in config_data["address_family"]:
        cmd = "address-family {afi}".format(**config_data["address_family"])
        if config_data["address_family"].get("unicast"):
            cmd += " unicast"
        if config_data["address_family"].get("vrf"):
            cmd += " vrf {vrf}".format(**config_data["address_family"])
        command.append(cmd)
        if command:
            command.insert(len(command), "exit-address-family")
        return command


def _tmplt_address_family_graceful_restart(config_data):
    if "graceful_restart" in config_data:
        command = "graceful_restart {enable}".format(
            **config_data["graceful_restart"]
        )
        if "disable" in config_data["graceful_restart"]:
            command += " disable"
        elif "strict_lsa_checking" in config_data["graceful_restart"]:
            command += " strict-lsa-checking"
        return command


def _tmplt_ospf_area_authentication(config_data):
    if "authentication" in config_data:
        command = "area {area_id} authentication".format(**config_data)
        if config_data["authentication"].get("message_digest"):
            command += " message-digest"
        return command


def _tmplt_ospf_area_filter(config_data):
    if "filter_list" in config_data:
        command = []
        for key, value in iteritems(config_data.get("filter_list")):
            cmd = "area {area_id}".format(**config_data)
            if value.get("name") and value.get("direction"):
                cmd += " filter-list prefix {name} {direction}".format(**value)
            command.append(cmd)
        return command


def _tmplt_ospf_area_nssa(config_data):
    if "nssa" in config_data:
        command = "area {area_id} nssa".format(**config_data)
        if "default_information_originate" in config_data["nssa"]:
            command += " default-information-originate"
            if (
                "metric"
                in config_data["nssa"]["default_information_originate"]
            ):
                command += " metric {metric}".format(
                    **config_data["nssa"]["default_information_originate"]
                )
            if (
                "metric_type"
                in config_data["nssa"]["default_information_originate"]
            ):
                command += " metric-type {metric_type}".format(
                    **config_data["nssa"]["default_information_originate"]
                )
            if (
                "nssa_only"
                in config_data["nssa"]["default_information_originate"]
            ):
                command += " nssa-only"
        if config_data["nssa"].get("no_ext_capability"):
            command += " no-ext-capability"
        if config_data["nssa"].get("no_redistribution"):
            command += " no-redistribution"
        if config_data["nssa"].get("no_summary"):
            command += " no-summary"
        return command


def _tmplt_ospf_area_nssa_translate(config_data):
    if "nssa" in config_data and "translate" in config_data["nssa"]:
        command = "area {area_id} nssa".format(**config_data)
        if "translate" in config_data["nssa"]:
            command += " translate type7 {translate}".format(
                **config_data["nssa"]
            )
        return command


def _tmplt_ospf_area_ranges(config_data):
    if "ranges" in config_data:
        commands = []
        for k, v in iteritems(config_data["ranges"]):
            cmd = "area {area_id} range".format(**config_data)
            temp_cmd = " {address} {netmask}".format(**v)
            if "advertise" in v:
                temp_cmd += " advertise"
            elif "not_advertise" in v:
                temp_cmd += " not-advertise"
            if "cost" in v:
                temp_cmd += " cost {cost}".format(**v)
            cmd += temp_cmd
            commands.append(cmd)
        return commands


def _tmplt_ospf_area_sham_link(config_data):
    if "sham_link" in config_data:
        command = "area {area_id} sham-link".format(**config_data)
        if "source" in config_data["sham_link"]:
            command += " {source} {destination}".format(
                **config_data["sham_link"]
            )
        if "cost" in config_data["sham_link"]:
            command += " cost {cost}".format(**config_data["sham_link"])
        if "ttl_security" in config_data["sham_link"]:
            command += " ttl-security hops {ttl_security}".format(
                **config_data["sham_link"]
            )
        return command


def _tmplt_ospf_area_stub_link(config_data):
    if "stub" in config_data:
        command = "area {area_id} stub".format(**config_data)
        if "no_ext_capability" in config_data["stub"]:
            command += " no-ext-capability"
        if "no_summary" in config_data["stub"]:
            command += " no-summary"
        return command


def _tmplt_ospf_auto_cost(config_data):
    if "auto_cost" in config_data:
        command = "auto-cost"
        if "reference_bandwidth" in config_data["auto_cost"]:
            command += " reference-bandwidth {reference_bandwidth}".format(
                **config_data["auto_cost"]
            )
        return command


def _tmplt_ospf_capability(config_data):
    if "capability" in config_data:
        if "lls" in config_data["capability"]:
            command = "capability lls"
        elif "opaque" in config_data["capability"]:
            command = "capability opaque"
        elif "transit" in config_data["capability"]:
            command = "capability transit"
        elif "vrf_lite" in config_data["capability"]:
            command = "capability vrf_lite"
        return command


def _tmplt_ospf_compatible(config_data):
    if "compatible" in config_data:
        if "rfc1583" in config_data["compatible"]:
            command = "compatible rfc1583"
        elif "rfc1587" in config_data["compatible"]:
            command = "compatible rfc1587"
        elif "rfc5243" in config_data["compatible"]:
            command = "compatible rfc5243"
        return command


def _tmplt_ospf_default_information(config_data):
    if "default_information" in config_data:
        command = "default-information"
        if "originate" in config_data["default_information"]:
            command += " originate"
        if "always" in config_data["default_information"]:
            command += " always"
        if "metric" in config_data["default_information"]:
            command += " metric {metric}".format(
                **config_data["default_information"]
            )
        if "metric_type" in config_data["default_information"]:
            command += " metric-type {metric_type}".format(
                **config_data["default_information"]
            )
        if "metric" in config_data["default_information"]:
            command += " route-map {route_map}".format(
                **config_data["default_information"]
            )
        return command


def _tmplt_ospf_discard_route(config_data):
    if "discard_route" in config_data:
        command = "discard-route"
        if "external" in config_data["discard_route"]:
            command += " external {external}".format(
                **config_data["discard_route"]
            )
        if "internal" in config_data["discard_route"]:
            command += " internal {internal}".format(
                **config_data["discard_route"]
            )
        return command


def _tmplt_ospf_distance_admin_distance(config_data):
    if "admin_distance" in config_data["distance"]:
        command = "distance {distance}".format(
            **config_data["distance"]["admin_distance"]
        )
        if "address" in config_data["distance"]["admin_distance"]:
            command += " {address} {wildcard_bits}".format(
                **config_data["distance"]["admin_distance"]
            )
        if "acl" in config_data["distance"]["admin_distance"]:
            command += " {acl}".format(
                **config_data["distance"]["admin_distance"]
            )
        return command


def _tmplt_ospf_distance_ospf(config_data):
    if "ospf" in config_data["distance"]:
        command = "distance ospf"
        if "inter_area" in config_data["distance"]["ospf"]:
            command += " inter-area {inter_area}".format(
                **config_data["distance"]["ospf"]
            )
        if config_data["distance"].get("ospf").get("intra_area"):
            command += " intra-area {intra_area}".format(
                **config_data["distance"]["ospf"]
            )
        if config_data["distance"].get("ospf").get("external"):
            command += " external {external}".format(
                **config_data["distance"]["ospf"]
            )
        return command


def _tmplt_ospf_distribute_list_acls(config_data):
    if "acls" in config_data.get("distribute_list"):
        command = []
        for k, v in iteritems(config_data["distribute_list"]["acls"]):
            cmd = "distribute-list {name} {direction}".format(**v)
            if "interface" in v:
                cmd += " {interface}".format(**v)
            if "protocol" in v:
                cmd += " {protocol}".format(**v)
            command.append(cmd)
        return command


def _tmplt_ospf_distribute_list_prefix(config_data):
    if "prefix" in config_data.get("distribute_list"):
        command = "distribute-list prefix {name}".format(
            **config_data["distribute_list"]["prefix"]
        )
        if "gateway_name" in config_data["distribute_list"]["prefix"]:
            command += " gateway {gateway_name}".format(
                **config_data["distribute_list"]["prefix"]
            )
        if "direction" in config_data["distribute_list"]["prefix"]:
            command += " {direction}".format(
                **config_data["distribute_list"]["prefix"]
            )
        if "interface" in config_data["distribute_list"]["prefix"]:
            command += " {interface}".format(
                **config_data["distribute_list"]["prefix"]
            )
        if "protocol" in config_data["distribute_list"]["prefix"]:
            command += " {protocol}".format(
                **config_data["distribute_list"]["prefix"]
            )
        return command


def _tmplt_ospf_domain_id(config_data):
    if "domain_id" in config_data:
        command = "domain-id"
        if "ip_address" in config_data["domain_id"]:
            if "address" in config_data["domain_id"]["ip_address"]:
                command += " {address}".format(
                    **config_data["domain_id"]["ip_address"]
                )
                if "secondary" in config_data["domain_id"]["ip_address"]:
                    command += " {secondary}".format(
                        **config_data["domain_id"]["ip_address"]
                    )
        elif "null" in config_data["domain_id"]:
            command += " null"
        return command


def _tmplt_ospf_event_log(config_data):
    if "event_log" in config_data:
        command = "event-log"
        if "one_shot" in config_data["event_log"]:
            command += " one-shot"
        if "pause" in config_data["event_log"]:
            command += " pause"
        if "size" in config_data["event_log"]:
            command += " size {size}".format(**config_data["event_log"])
        return command


def _tmplt_ospf_manet(config_data):
    if "manet" in config_data:
        command = []
        if "cache" in config_data["manet"]:
            cmd = "manet cache"
            if "acknowledgement" in config_data["manet"]["cache"]:
                cmd += " acknowledgement {acknowledgement}".format(
                    **config_data["manet"]["cache"]
                )
            elif "redundancy" in config_data["manet"]["cache"]:
                cmd += " redundancy {redundancy}".format(
                    **config_data["manet"]["cache"]
                )
            command.append(cmd)
        if "hello" in config_data["manet"] and config_data["manet"]["hello"]:
            command.append("manet hello")
        if "peering" in config_data["manet"]:
            cmd = "manet peering selective"
            if "per_interface" in config_data["manet"]["peering"]:
                cmd += " per-interface"
            if "redundancy" in config_data["manet"]["peering"]:
                cmd += " redundancy {redundancy}".format(
                    **config_data["manet"]["peering"]
                )
            command.append(cmd)
        if "willingness" in config_data["manet"]:
            command.append(
                "manet willingness".format(
                    **config_data["manet"]["willingness"]
                )
            )
    return command


def _tmplt_ospf_limit(config_data):
    if "limit" in config_data:
        command = "limit retransmissions"
        if "dc" in config_data["limit"]:
            if "number" in config_data["limit"]["dc"]:
                command += " dc {number}".format(**config_data["limit"]["dc"])
            if "disable" in config_data["limit"]["dc"]:
                command += " dc disable"
        if "non_dc" in config_data["limit"]:
            if "number" in config_data["limit"]["non_dc"]:
                command += " non-dc {number}".format(
                    **config_data["limit"]["non_dc"]
                )
            if "disable" in config_data["limit"]["dc"]:
                command += " non-dc disable"
        return command


def _tmplt_ospf_vrf_local_rib_criteria(config_data):
    if "local_rib_criteria" in config_data:
        command = "local-rib-criteria"
        if "forwarding_address" in config_data["local_rib_criteria"]:
            command += " forwarding-address"
        if "inter_area_summary" in config_data["local_rib_criteria"]:
            command += " inter-area-summary"
        if "nssa_translation" in config_data["local_rib_criteria"]:
            command += " nssa-translation"
        return command


def _tmplt_ospf_log_adjacency_changes(config_data):
    if "log_adjacency_changes" in config_data:
        command = "log-adjacency-changes"
        if "detail" in config_data["log_adjacency_changes"]:
            command += " detail"
        return command


def _tmplt_ospf_max_lsa(config_data):
    if "max_lsa" in config_data:
        command = "max-lsa {number}".format(**config_data["max_lsa"])
        if "threshold_value" in config_data["max_lsa"]:
            command += " {threshold_value}".format(**config_data["max_lsa"])
        if "ignore_count" in config_data["max_lsa"]:
            command += " ignore-count {ignore_count}".format(
                **config_data["max_lsa"]
            )
        if "ignore_time" in config_data["max_lsa"]:
            command += " ignore-time {ignore_time}".format(
                **config_data["max_lsa"]
            )
        if "reset_time" in config_data["max_lsa"]:
            command += " reset-time {reset_time}".format(
                **config_data["max_lsa"]
            )
        if "warning_only" in config_data["max_lsa"]:
            command += " warning-only"
        return command


def _tmplt_ospf_max_metric(config_data):
    if "max_metric" in config_data:
        command = "max-metric"
        if "router_lsa" in config_data["max_metric"]:
            command += " router-lsa"
        if "external_lsa" in config_data["max_metric"]:
            command += " external-lsa {external_lsa}".format(
                **config_data["max_metric"]
            )
        if "include_stub" in config_data["max_metric"]:
            command += " include-stub"
        if "on_startup" in config_data["max_metric"]:
            if "time" in config_data["max_metric"]["on_startup"]:
                command += " on-startup {time}".format(
                    **config_data["max_metric"]["on_startup"]
                )
            elif "wait_for_bgp" in config_data["max_metric"]["on_startup"]:
                command += " on-startup wait-for-bgp"
        if "summary_lsa" in config_data["max_metric"]:
            command += " summary-lsa {summary_lsa}".format(
                **config_data["max_metric"]
            )
        return command


def _tmplt_ospf_mpls_ldp(config_data):
    if "ldp" in config_data["mpls"]:
        command = "mpls ldp"
        if "autoconfig" in config_data["mpls"]["ldp"]:
            command += " autoconfig"
            if "area" in config_data["mpls"]["ldp"]["autoconfig"]:
                command += " area {area}".format(
                    **config_data["mpls"]["ldp"]["autoconfig"]
                )
        elif "sync" in config_data["mpls"]["ldp"]:
            command += " sync"
    return command


def _tmplt_ospf_mpls_traffic_eng(config_data):
    if "traffic_eng" in config_data["mpls"]:
        command = "mpls traffic-eng"
        if "area" in config_data["mpls"]["traffic_eng"]:
            command += " area {area}".format(
                **config_data["mpls"]["traffic_eng"]
            )
        elif "autoroute_exclude" in config_data["mpls"]["traffic_eng"]:
            command += " autoroute-exclude prefix-list {autoroute_exclude}".format(
                **config_data["mpls"]["traffic_eng"]
            )
        elif "interface" in config_data["mpls"]["traffic_eng"]:
            command += " interface {int_type}".format(
                **config_data["mpls"]["traffic_eng"]["interface"]
            )
            if "area" in config_data["mpls"]["traffic_eng"]["interface"]:
                command += " area {area}".format(
                    **config_data["mpls"]["traffic_eng"]["interface"]
                )
        elif "mesh_group" in config_data["mpls"]["traffic_eng"]:
            command += " mesh-group {id} {interface}".format(
                **config_data["mpls"]["traffic_eng"]["mesh_group"]
            )
            if "area" in config_data["mpls"]["traffic_eng"]["mesh_group"]:
                command += " area {area}".format(
                    **config_data["mpls"]["traffic_eng"]["mesh_group"]
                )
        elif "multicast_intact" in config_data["mpls"]["traffic_eng"]:
            command += " multicast-intact"
        elif "router_id_interface" in config_data["mpls"]["traffic_eng"]:
            command += " router-id {router_id_interface}".format(
                **config_data["mpls"]["traffic_eng"]
            )
        return command


def _tmplt_ospf_neighbor(config_data):
    if "neighbor" in config_data:
        command = "neighbor"
        if "address" in config_data["neighbor"]:
            command += " {address}".format(**config_data["neighbor"])
        if "cost" in config_data["neighbor"]:
            command += " cost {cost}".format(**config_data["neighbor"])
        if "database_filter" in config_data["neighbor"]:
            command += " database-filter all out"
        if "poll_interval" in config_data["neighbor"]:
            command += " poll-interval {poll_interval}".format(
                **config_data["neighbor"]
            )
        if "priority" in config_data["neighbor"]:
            command += " priority {priority}".format(**config_data["neighbor"])
        return command


def _tmplt_ospf_network(config_data):
    if "network" in config_data:
        command = "network"
        if "address" in config_data["network"]:
            command += " {address} {wildcard_bits}".format(
                **config_data["network"]
            )
        if "area" in config_data["network"]:
            command += " area {area}".format(**config_data["network"])
        return command


def _tmplt_ospf_nsf_cisco(config_data):
    if "cisco" in config_data["nsf"]:
        command = "nsf cisco helper"
        if "disable" in config_data["nsf"]["cisco"]:
            command += " disable"
        return command


def _tmplt_ospf_nsf_ietf(config_data):
    if "ietf" in config_data["nsf"]:
        command = "nsf ietf helper"
        if "disable" in config_data["nsf"]["ietf"]:
            command += " disable"
        elif "strict_lsa_checking" in config_data["nsf"]["ietf"]:
            command += " strict-lsa-checking"
        return command


def _tmplt_ospf_queue_depth_hello(config_data):
    if "hello" in config_data["queue_depth"]:
        command = "queue-depth hello"
        if "max_packets" in config_data["queue_depth"]["hello"]:
            command += " {max_packets}".format(
                **config_data["queue_depth"]["hello"]
            )
        elif "unlimited" in config_data["queue_depth"]["hello"]:
            command += " unlimited"
        return command


def _tmplt_ospf_queue_depth_update(config_data):
    if "update" in config_data["queue_depth"]:
        command = "queue-depth update"
        if "max_packets" in config_data["queue_depth"]["update"]:
            command += " {max_packets}".format(
                **config_data["queue_depth"]["update"]
            )
        elif "unlimited" in config_data["queue_depth"]["update"]:
            command += " unlimited"
        return command


def _tmplt_ospf_summary_prefix(config_data):
    if "summary_prefix" in config_data:
        command = "summary-prefix {address} {mask}".format(
            **config_data["summary_prefix"]
        )
        if "not_advertise" in config_data["summary_prefix"]:
            command += " not-advertise"
        elif "nssa_only" in config_data["summary_prefix"]:
            command += " nssa-only"
            if "tag" in config_data["summary_prefix"]:
                command += " tag {tag}".format(**config_data["summary_prefix"])
        return command


def _tmplt_ospf_timers_pacing(config_data):
    if "pacing" in config_data["timers"]:
        command = "timers pacing"
        if "flood" in config_data["timers"]["pacing"]:
            command += " flood {flood}".format(
                **config_data["timers"]["pacing"]
            )
        elif "lsa_group" in config_data["timers"]["pacing"]:
            command += " lsa-group {lsa_group}".format(
                **config_data["timers"]["pacing"]
            )
        elif "retransmission" in config_data["timers"]["pacing"]:
            command += " retransmission {retransmission}".format(
                **config_data["timers"]["pacing"]
            )
        return command


def _tmplt_ospf_ttl_security(config_data):
    if "ttl_security" in config_data:
        command = "ttl-security all-interfaces"
        if "hops" in config_data["ttl_security"]:
            command += " hops {hops}".format(**config_data["ttl_security"])
        return command


class Ospfv3Template(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospfv3Template, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "pid",
            "getval": re.compile(
                r"""
                        ^router\s
                        ospfv3*
                        \s(?P<pid>\S+)
                        $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospfv3_cmd,
            "result": {
                "processes": {"{{ pid }}": {"process_id": "{{ pid|int }}"}}
            },
            "shared": True,
        },
        {
            "name": "adjacency",
            "getval": re.compile(
                r"""\s+adjacency
                    \sstagger*
                    \s*((?P<min>\d+)|(?P<none_adj>none))*
                    \s*(?P<max>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_adjacency_cmd,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "adjacency": {
                            "min_adjacency": "{{ min|int }}",
                            "max_adjacency": "{{ max|int }}",
                            "none": "{{ True if none_adj is defined else None }}",
                        }
                    }
                }
            },
        },
        {
            "name": "area.authentication",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \s*(?P<auth>authentication)*
                    \s*(?P<md>message-digest)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_authentication,
            "compval": "authentication",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "authentication": {
                                    "enable": "{{ True if auth is defined and md is undefined }}",
                                    "message_digest": "{{ not not md }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.capability",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \s*(?P<capability>capability)*
                    \s*(?P<df>default-exclusion)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} capability default-exclusion",
            "compval": "capability",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "capability": "{{ not not capability }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.default_cost",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \sdefault-cost*
                    \s*(?P<default_cost>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} default-cost {{ default_cost }}",
            "compval": "default_cost",
            "result": {
                "processes": {
                    "{{ pid }}": {
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
            "name": "area.filter_list",
            "getval": re.compile(
                r"""\s+area
                    \s*(?P<area_id>\S+)*
                    \s*filter-list\sprefix*
                    \s*(?P<name>\S+)*
                    \s*(?P<dir>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_filter,
            "compval": "filter_list",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "filter_list": [
                                    {
                                        "name": "{{ name }}",
                                        "direction": "{{ dir }}",
                                    }
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.nssa",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \s(?P<nssa>nssa)*
                    \s*(?P<no_redis>no-redistribution)*
                    \s*(?P<def_origin>default-information-originate)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<no_summary>no-summary)*
                    \s*(?P<no_ext>no-ext-capability)*$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_nssa,
            "compval": "nssa",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "set": "{{ True if nssa is defined and def_origin is undefined and "
                                    "no_ext is undefined and no_redis is undefined and nssa_only is undefined }}",
                                    "default_information_originate": {
                                        "set": "{{ True if def_origin is defined and metric is undefined and "
                                        "metric_type is undefined and nssa_only is undefined }}",
                                        "metric": "{{ metric.split("
                                        ")[1]|int }}",
                                        "metric_type": "{{ metric_type.split("
                                        ")[1]|int }}",
                                        "nssa_only": "{{ True if nssa_only is defined }}",
                                    },
                                    "no_ext_capability": "{{ True if no_ext is defined }}",
                                    "no_redistribution": "{{ True if no_redis is defined }}",
                                    "no_summary": "{{ True if no_summary is defined }}",
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
                r"""\s+area*
                    \s*(?P<area_id>\S+)*
                    \s*(?P<nssa>nssa)*
                    \stranslate\stype7*
                    \s(?P<translate_always>always)*
                    \s* (?P<translate_supress>suppress-fa)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_nssa_translate,
            "compval": "nssa.translate",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "translate": "{{ translate_always if translate_always is defined else translate_supress if translate_supress is defined }}"
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
                r"""\s+area\s(?P<area_id>\S+)
                    \srange
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    \s(?P<netmask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*((?P<advertise>advertise)|(?P<not_advertise>not-advertise))*
                    \s*(?P<cost>cost\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_ranges,
            "compval": "ranges",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "ranges": [
                                    {
                                        "address": "{{ address }}",
                                        "netmask": "{{ netmask }}",
                                        "advertise": "{{ True if advertise is defined }}",
                                        "cost": "{{ cost.split(" ")[1]|int }}",
                                        "not_advertise": "{{ True if not_advertise is defined }}",
                                    }
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.sham_link",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \ssham-link
                    \s(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    \s(?P<destination>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<cost>cost\s\d+)*
                    \s*(?P<ttl_security>ttl-security\shops\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_sham_link,
            "compval": "sham_link",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "sham_link": {
                                    "source": "{{ source }}",
                                    "destination": "{{ destination }}",
                                    "cost": "{{ cost.split(" ")[1]|int }}",
                                    "ttl_security": '{{ ttl_security.split("hops ")[1] }}',
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.stub",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \s(?P<stub>stub)*
                    \s*(?P<no_ext>no-ext-capability)*
                    \s*(?P<no_sum>no-summary)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_stub_link,
            "compval": "stub",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "stub": {
                                    "set": "{{ True if stub is defined and no_ext is undefined and no_sum is undefined }}",
                                    "no_ext_capability": "{{ True if no_ext is defined }}",
                                    "no_summary": "{{ True if no_sum is defined }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "auto_cost",
            "getval": re.compile(
                r"""\s+(?P<auto_cost>auto-cost)*
                    \s*(?P<ref_band>reference-bandwidth\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_auto_cost,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "auto_cost": {
                            "set": "{{ True if auto_cost is defined and ref_band is undefined }}",
                            "reference_bandwidth": '{{ ref_band.split(" ")[1] }}',
                        }
                    }
                }
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""\s+bfd*
                    \s*(?P<bfd>all-interfaces)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "bfd all-interfaces",
            "result": {
                "processes": {
                    "{{ pid }}": {"bfd": "{{ True if bfd is defined }}"}
                }
            },
        },
        {
            "name": "capability",
            "getval": re.compile(
                r"""\s+capability*
                    \s*((?P<lls>lls)|(?P<opaque>opaque)|(?P<transit>transit)|(?P<vrf_lite>vrf-lite))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_capability,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "capability": {
                            "lls": "{{ True if lls is defined }}",
                            "opaque": "{{ True if opaque is defined }}",
                            "transit": "{{ True if transit is defined }}",
                            "vrf_lite": "{{ True if vrf_lite is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "compatible",
            "getval": re.compile(
                r"""\s+compatible*
                    \s*((?P<rfc1583>rfc1583)|(?P<rfc1587>rfc1587)|(?P<rfc5243>rfc5243))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_compatible,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "compatible": {
                            "rfc1583": "{{ True if rfc1583 is defined }}",
                            "rfc1587": "{{ True if rfc1587 is defined }}",
                            "rfc5243": "{{ True if rfc5243 is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "default_information",
            "getval": re.compile(
                r"""\s+default-information*
                    \s*(?P<originate>originate)*
                    \s*(?P<always>always)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<route_map>route-map\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_default_information,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "default_information": {
                            "originate": "{{ True if originate is defined }}",
                            "always": "{{ True if always is defined }}",
                            "metric": "{{ metric.split(" ")[1]|int }}",
                            "metric_type": "{{ metric_type.split("
                            ")[1]|int }}",
                            "route_map": "{{ route_map.split(" ")[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""\s+default-metric(?P<default_metric>\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric }}",
            "result": {
                "processes": {
                    "{{ pid }}": {"default_metric": "{{ default_metric| int}}"}
                }
            },
        },
        {
            "name": "discard_route",
            "getval": re.compile(
                r"""\s+(?P<discard_route>discard-route)*
                    \s*(?P<external>external\s\d+)*
                    \s*(?P<internal>internal\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_discard_route,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "discard_route": {
                            "set": "{{ True if discard_route is defined and external is undefined and internal is undefined }}",
                            "external": "{{ external.split(" ")[1]|int }}",
                            "internal": "{{ internal.split(" ")[1]|int }}",
                        }
                    }
                }
            },
        },
        {
            "name": "distance.admin_distance",
            "getval": re.compile(
                r"""\s+distance
                    \s(?P<admin_dist>\S+)*
                    \s*(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<wildcard>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<acl>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distance_admin_distance,
            "compval": "admin_distance",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distance": {
                            "admin_distance": {
                                "distance": "{{ admin_dist }}",
                                "address": "{{ source }}",
                                "wildcard_bits": "{{ wildcard }}",
                                "acl": "{{ acl }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "distance.ospf",
            "getval": re.compile(
                r"""\s+distance
                    \sospf*
                    \s*(?P<intra>intra-area\s\d+)*
                    \s*(?P<inter>inter-area\s\d+)*
                    \s*(?P<external>external\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distance_ospf,
            "compval": "ospf",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distance": {
                            "ospf": {
                                "inter_area": "{{ inter.split(" ")[1]|int }}",
                                "intra_area": "{{ intra.split(" ")[1]|int }}",
                                "external": "{{ external.split(" ")[1]|int }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "distribute_list.acls",
            "getval": re.compile(
                r"""\s+distribute-list
                    \s(?P<name>\S+)*
                    \s*(?P<dir>\S+)*
                    \s*(?P<int_pro>\S+\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distribute_list_acls,
            "compval": "distribute_list.acls",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distribute_list": {
                            "acls": [
                                {
                                    "name": "{{ name }}",
                                    "direction": "{{ dir }}",
                                    "interface": '{{ int_pro if dir == "in" }}',
                                    "protocol": '{{ int_pro if dir == "out" }}',
                                }
                            ]
                        }
                    }
                }
            },
        },
        {
            "name": "distribute_list.prefix",
            "getval": re.compile(
                r"""\s+distribute-list
                    \s(?P<prefix>prefix\s\S+)*
                    \s*(?P<gateway>gateway\s\S+)*
                    \s*(?P<dir>\S+)*
                    \s*(?P<int_pro>\S+\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distribute_list_prefix,
            "compval": "distribute_list.prefix",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distribute_list": {
                            "prefix": {
                                "name": "{{ prefix.split(" ")[1] }}",
                                "gateway_name": "{{ gateway.split("
                                ")[1] if prefix is defined }}",
                                "direction": "{{ dir if gateway is undefined }}",
                                "interface": '{{ int_pro if dir == "in" }}',
                                "protocol": '{{ int_pro if dir == "out" }}',
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "distribute_list.route_map",
            "getval": re.compile(
                r"""\s+distribute-list
                    \s(?P<route_map>route-map\s\S+)*
                    \s*(?P<dir>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "distribute-list route-map {{ distribute_list.route_map.name }} in",
            "compval": "distribute_list.route_map",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "distribute_list": {
                            "route_map": {
                                "name": "{{ route_map.split(" ")[1] }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "domain_id",
            "getval": re.compile(
                r"""\s+domain-id
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<secondary>secondary)*
                    \s*(?P<null>null)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_domain_id,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "domain_id": {
                            "ip_address": {
                                "address": "{{ address }}",
                                "secondary": "{{ True if secondary is defined }}",
                            },
                            "null": "{{ True if null is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "domain_tag",
            "getval": re.compile(
                r"""\s+domain-tag
                    \s(?P<tag>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "domain-tag {{ domain_tag }}",
            "result": {
                "processes": {"{{ pid }}": {"domain_tag": "{{ tag|int }}"}}
            },
        },
        {
            "name": "event_log",
            "getval": re.compile(
                r"""\s+(?P<event_log>event-log)*
                    \s*(?P<one_shot>one-shot)*
                    \s*(?P<pause>pause)*
                    \s*(?P<size>size\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_event_log,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "event_log": {
                            "enable": "{{ True if event_log is defined and one_shot is undefined and pause is undefined and size is undefined }}",
                            "one_shot": "{{ True if one_shot is defined }}",
                            "pause": "{{ True if pause is defined }}",
                            "size": "{{ size.split(" ")[1]|int }}",
                        }
                    }
                }
            },
        },
        {
            "name": "help",
            "getval": re.compile(
                r"""\s+(?P<help>help)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "help",
            "result": {
                "processes": {
                    "{{ pid }}": {"help": "{{ True if help is defined }}"}
                }
            },
        },
        {
            "name": "ignore",
            "getval": re.compile(
                r"""\s+(?P<ignore>ignore)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "ignore lsa mospf",
            "result": {
                "processes": {
                    "{{ pid }}": {"ignore": "{{ True if ignore is defined }}"}
                }
            },
        },
        {
            "name": "interface_id",
            "getval": re.compile(
                r"""\s+(?P<interface_id>interface-id\ssnmp-if-index)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "interface-id snmp-if-index",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "interface_id": "{{ True if interface_id is defined }}"
                    }
                }
            },
        },
        {
            "name": "ispf",
            "getval": re.compile(
                r"""\s+(?P<ispf>ispf)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "ispf",
            "result": {
                "processes": {
                    "{{ pid }}": {"ispf": "{{ True if ispf is defined }}"}
                }
            },
        },
        {
            "name": "limit",
            "getval": re.compile(
                r"""\s+limit\sretransmissions
                    \s((?P<dc_num>dc\s\d+)|(?P<dc_disable>dc\sdisable))*
                    \s*((?P<non_dc_num>non-dc\s\d+)|(?P<non_dc_disable>non-dc\sdisable))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_limit,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "limit": {
                            "dc": {
                                "number": "{{ dc_num.split(" ")[1]|int }}",
                                "disable": "{{ True if dc_disable is defined }}",
                            },
                            "non_dc": {
                                "number": "{{ non_dc_num.split(" ")[1]|int }}",
                                "disable": "{{ True if dc_disable is defined }}",
                            },
                        }
                    }
                }
            },
        },
        {
            "name": "local_rib_criteria",
            "getval": re.compile(
                r"""\s+(?P<local>local-rib-criteria)*
                    \s*(?P<forward>forwarding-address)*
                    \s*(?P<inter>inter-area-summary)*
                    \s*(?P<nssa>nssa-translation)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_vrf_local_rib_criteria,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "local_rib_criteria": {
                            "enable": "{{ True if local is defined and forward is undefined and inter is undefined and nssa is undefined }}",
                            "forwarding_address": "{{ True if forward is defined }}",
                            "inter_area_summary": "{{ True if inter is defined }}",
                            "nssa_translation": "{{ True if nssa is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "log_adjacency_changes",
            "getval": re.compile(
                r"""\s+(?P<log>log-adjacency-changes)*
                    \s*(?P<detail>detail)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_log_adjacency_changes,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "log_adjacency_changes": {
                            "set": "{{ True if log is defined and detail is undefined }}",
                            "detail": "{{ True if detail is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "manet",
            "getval": re.compile(
                r"""\s+manet*
                    \s*(?P<cache>cache)*
                    \s*(?P<acknowledgement>acknowledgement\s\d+)*
                    \s*(?P<update>update\s\d+)*
                    \s*(?P<hello>hello)*
                    \s*(?P<unicast>unicast)*
                    \s*(?P<multicast>multicast)*
                    \s*(?P<peering>peering\sselective)*
                    \s*(?P<disable>disable)*
                    \s*(?P<per_interface>per-interface)*
                    \s*(?P<redundancy>redundancy\s\d+)*
                    \s*(?P<willingness>willingness\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_manet,
            "compval": "manet",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "manet": {
                            "cache": {
                                "acknowledgement": "{{ acknowledgement.split("
                                ")[1] }}",
                                "update": "{{ update.split(" ")[1] }}",
                            },
                            "hello": {
                                "unicast": "{{ True if unicast is defined }}",
                                "multicast": "{{ True if multicast is defined }}",
                            },
                            "peering": {
                                "set": "{{ True if peering is defined  }}",
                                "disable": "{{ True if disable is defined }}",
                                "per_interface": "{{ True if per_interface is defined }}",
                                "redundancy": "{{ redundancy.split(" ")[1] }}",
                            },
                            "willingness": "{{ willingness.split(" ")[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "max_lsa",
            "getval": re.compile(
                r"""\s+max-lsa
                    \s(?P<number>\d+)*
                    \s*(?P<threshold>\d+)*
                    \s*(?P<ignore_count>ignore-count\s\d+)*
                    \s*(?P<ignore_time>ignore-time\s\d+)*
                    \s*(?P<reset_time>reset-time\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_lsa,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "max_lsa": {
                            "number": "{{ number }}",
                            "threshold_value": "{{ threshold }}",
                            "ignore_count": "{{ ignore_count.split(" ")[1] }}",
                            "ignore_time": "{{ ignore_time.split(" ")[1] }}",
                            "reset_time": "{{ reset_time.split(" ")[1] }}",
                            "warning_only": "{{ True if warning is defined }}",
                        }
                    }
                }
            },
        },
        {
            "name": "max_metric",
            "getval": re.compile(
                r"""\s+max-metric*
                    \s*(?P<router_lsa>router-lsa)*
                    \s*(?P<include_stub>include-stub)*
                    \s*(?P<external_lsa>external-lsa\s\d+)*
                    \s*(?P<startup_time>on-startup\s\d+)*
                    \s*(?P<startup_wait>on-startup\s\S+)*
                    \s*(?P<summary_lsa>summary-lsa\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_metric,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "max_metric": {
                            "router_lsa": "{{ True if router_lsa is defined }}",
                            "external_lsa": "{{ external_lsa.split(" ")[1] }}",
                            "include_stub": "{{ ignore_count.split(" ")[1] }}",
                            "on_startup": {
                                "time": "{{ startup_time.split(" ")[1] }}",
                                "wait_for_bgp": "{{ True if startup_wait is defined }}",
                            },
                            "summary_lsa": "{{ summary_lsa.split(" ")[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "maximum_paths",
            "getval": re.compile(
                r"""\s+maximum-paths*
                    \s+(?P<paths>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths {{ maximum_paths }}",
            "result": {
                "processes": {"{{ pid }}": {"maximum_paths": "{{ paths }}"}}
            },
        },
        {
            "name": "mpls.ldp",
            "getval": re.compile(
                r"""\s+mpls
                    \sldp*
                    \s*(?P<autoconfig>autoconfig*\s*(?P<area>area\s\S+))*
                    \s*(?P<sync>sync)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_mpls_ldp,
            "compval": "ldp",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "mpls": {
                            "ldp": {
                                "autoconfig": {
                                    "set": "{{ True if autoconfig is defined and area is undefined }}",
                                    "area": "{{ area.split(" ")[1] }}",
                                },
                                "sync": "{{ True if sync is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "mpls.traffic_eng",
            "getval": re.compile(
                r"""\s+mpls
                    \straffic-eng*
                    \s*(?P<area>area\s\S+)*
                    \s*(?P<autoroute>autoroute-exclude\s\S+\s\S+)*
                    \s*(?P<interface>interface\s(?P<int_type>\S+\s\S+)\s(?P<int_area>area\s\S+))*
                    \s*(?P<mesh>mesh-group\s\d+\s(?P<mesh_int>\S+\s\S+)\s(?P<mesh_area>area\s\d+))*
                    \s*(?P<multicast>multicast-intact)*
                    \s*(?P<router>router-id\s(?P<router_int>\S+\s\S+))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_mpls_traffic_eng,
            "compval": "traffic_eng",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "mpls": {
                            "traffic_eng": {
                                "area": "{{ area.split(" ")[1] }}",
                                "autoroute_exclude": "{{ autoroute.split("
                                ")[2] }}",
                                "interface": {
                                    "interface_type": "{{ int_type }}",
                                    "area": "{{ int_area.split(" ")[1] }}",
                                },
                                "mesh_group": {
                                    "id": "{{ mesh.split(" ")[1] }}",
                                    "interface": "{{ mest_int }}",
                                    "area": "{{ mesh_area.split(" ")[1] }}",
                                },
                                "multicast_intact": "{{ True if multicast is defined }}",
                                "router_id_interface": "{{ router_int }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""\s+neighbor
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<cost>cost\s\d+)*
                    \s*(?P<db_filter>database-filter\sall\sout)*
                    \s*(?P<poll>poll-interval\s\d+)*
                    \s*(?P<priority>priority\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_neighbor,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "neighbor": {
                            "address": "{{ address }}",
                            "cost": "{{ cost.split(" ")[1] }}",
                            "database_filter": "{{ True if db_filter is defined }}",
                            "poll_interval": "{{ poll.split(" ")[1] }}",
                            "priority": "{{ priority.split(" ")[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""\s+network
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<wildcard>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<area>area\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_network,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "network": {
                            "address": "{{ address }}",
                            "wildcard_bits": "{{ wildcard }}",
                            "area": "{{ area.split(" ")[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "nsf.cisco",
            "getval": re.compile(
                r"""\s+nsf
                    \s(?P<cisco>cisco)*
                    \s*(?P<helper>helper)*
                    \s*(?P<disable>disable)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_nsf_cisco,
            "compval": "cisco",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "nsf": {
                            "cisco": {
                                "helper": "{{ True if helper is defined }}",
                                "disable": "{{ True if disable is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "nsf.ietf",
            "getval": re.compile(
                r"""\s+nsf
                    \s(?P<ietf>ietf)*
                    \s*(?P<helper>helper)*
                    \s*(?P<disable>disable)*
                    \s*(?P<strict>strict-lsa-checking)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_nsf_ietf,
            "compval": "ietf",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "nsf": {
                            "ietf": {
                                "helper": "{{ True if helper is defined }}",
                                "disable": "{{ True if disable is defined }}",
                                "strict_lsa_checking": "{{ True if strict is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "passive_interface",
            "getval": re.compile(
                r"""\s+passive-interface
                    \s(?P<interface>\S+\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "passive-interface {{ passive_interface }}",
            "result": {
                "processes": {
                    "{{ pid }}": {"passive_interface": "{{ interface }}"}
                }
            },
        },
        {
            "name": "prefix_suppression",
            "getval": re.compile(
                r"""\s+(?P<prefix_sup>prefix-suppression)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "prefix-suppression",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "prefix_suppression": "{{ True if prefix_sup is defined }}"
                    }
                }
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""\s+priority
                    \s(?P<priority>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "priority {{ priority }}",
            "result": {
                "processes": {"{{ pid }}": {"priority": "{{ priority }}"}}
            },
        },
        {
            "name": "queue_depth.hello",
            "getval": re.compile(
                r"""\s+queue-depth
                    \shello*
                    \s*(?P<max_packets>\d+)*
                    \s*(?P<unlimited>unlimited)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_queue_depth_hello,
            "compval": "hello",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "queue_depth": {
                            "hello": {
                                "max_packets": "{{ max_packets }}",
                                "unlimited": "{{ True if unlimited is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "queue_depth.update",
            "getval": re.compile(
                r"""\s+queue-depth
                    \supdate*
                    \s*(?P<max_packets>\d+)*
                    \s*(?P<unlimited>unlimited)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_queue_depth_update,
            "compval": "update",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "queue_depth": {
                            "update": {
                                "max_packets": "{{ max_packets }}",
                                "unlimited": "{{ True if unlimited is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "router_id",
            "getval": re.compile(
                r"""\s+router-id
                    \s(?P<id>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    *$""",
                re.VERBOSE,
            ),
            "setval": "router-id {{ router_id }}",
            "result": {"processes": {"{{ pid }}": {"router_id": "{{ id }}"}}},
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""\s+(?P<shutdown>shutdown)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "shutdown": "{{ True if shutdown is defined }}"
                    }
                }
            },
        },
        {
            "name": "timers.lsa",
            "getval": re.compile(
                r"""\s+timers
                    \slsa
                    \sarrival
                    \s(?P<lsa>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers lsa arrival {{ timers.lsa }}",
            "compval": "lsa",
            "result": {
                "processes": {"{{ pid }}": {"timers": {"lsa": "{{ lsa }}"}}}
            },
        },
        {
            "name": "timers.pacing",
            "getval": re.compile(
                r"""\s+timers
                    \spacing
                    \s(?P<flood>flood\s\d+)*
                    \s*(?P<lsa_group>lsa-group\s\d+)*
                    \s*(?P<retransmission>retransmission\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_timers_pacing,
            "compval": "pacing",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "timers": {
                            "pacing": {
                                "flood": "{{ flood.split(" ")[1] }}",
                                "lsa_group": "{{ lsa_group.split(" ")[1] }}",
                                "retransmission": "{{ retransmission.split("
                                ")[1] }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "timers.throttle.lsa",
            "getval": re.compile(
                r"""\s+timers
                    \sthrottle
                    \s*(?P<lsa>lsa)*
                    \s*(?P<first_delay>\d+)*
                    \s*(?P<min_delay>\d+)*
                    \s*(?P<max_delay>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers throttle lsa {{ throttle.lsa.first_delay }} {{ throttle.lsa.min_delay }} {{ throttle.lsa.max_delay }}",
            "compval": "throttle.lsa",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "timers": {
                            "throttle": {
                                "lsa": {
                                    "first_delay": "{{ first_delay }}",
                                    "min_delay": "{{ min_delay }}",
                                    "max_delay": "{{ max_delay }}",
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
                r"""\s+timers
                    \sthrottle
                    \s*(?P<spf>spf)*
                    \s*(?P<first_delay>\d+)*
                    \s*(?P<min_delay>\d+)*
                    \s*(?P<max_delay>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers throttle spf {{ throttle.spf.receive_delay }} {{ throttle.spf.between_delay }} {{ throttle.spf.max_delay }}",
            "compval": "throttle.spf",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "timers": {
                            "throttle": {
                                "spf": {
                                    "receive_delay": "{{ first_delay }}",
                                    "between_delay": "{{ min_delay }}",
                                    "max_delay": "{{ max_delay }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "traffic_share",
            "getval": re.compile(
                r"""\s+(?P<traffic>traffic-share\smin\sacross-interfaces)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "traffic-share min across-interfaces",
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "traffic_share": "{{ True if traffic is defined }}"
                    }
                }
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""\s+ttl-security
                    \s(?P<interfaces>all-interfaces)*
                    \s*(?P<hops>hops\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_ttl_security,
            "result": {
                "processes": {
                    "{{ pid }}": {
                        "ttl_security": {
                            "set": "{{ True if interfaces is defined and hops is undefined }}",
                            "hops": "{{ hops.split(" ")[1] }}",
                        }
                    }
                }
            },
        },
        {
            "name": "address_family",
            "getval": re.compile(
                r"""\s+address-family*
                    \s*(?P<afi>\S+)*
                    \s*(?P<unicast>unicast)*
                    \s*(?P<vrf>vrf\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_address_family_cmd,
            # "compval": "afi",
            "result": {
                "address_family": [
                    {
                        "afi": "{{ afi }}",
                        "unicast": "{{ True if unicast is defined }}",
                        "vrf": "{{ vrf.split(" ")[1] }}",
                    }
                ]
            },
            "shared": True,
        },
        {
            "name": "address_family.exit",
            "getval": re.compile(
                r"""\s+exit-address-family
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_address_family_cmd,
            "result": {
                "address_family": [
                    {
                        "exit": {
                            "pid": "{{ id }}",
                            "afi": "{{ afi }}",
                            "unicast": "{{ True if unicast is defined }}",
                            "vrf": "{{ vrf.split(" ")[1] }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.adjacency",
            "getval": re.compile(
                r"""\s+adjacency
                    \sstagger*
                    \s*((?P<min>\d+)|(?P<none_adj>none))*
                    \s*(?P<max>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_adjacency_cmd,
            "compval": "adjacency",
            "result": {
                "address_family": [
                    {
                        "adjacency": {
                            "min_adjacency": "{{ min|int }}",
                            "max_adjacency": "{{ max|int }}",
                            "none": "{{ True if none_adj is defined else None }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.authentication",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \s*(?P<auth>authentication)*
                    \s*(?P<md>message-digest)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_authentication,
            "compval": "authentication",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "authentication": {
                                    "enable": "{{ True if auth is defined and md is undefined }}",
                                    "message_digest": "{{ not not md }}",
                                },
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.capability",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \s*(?P<capability>capability)*
                    \s*(?P<df>default-exclusion)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} capability default-exclusion",
            "compval": "capability",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "capability": "{{ not not capability }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.default_cost",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \sdefault-cost*
                    \s*(?P<default_cost>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} default-cost {{ default_cost }}",
            "compval": "default_cost",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "default_cost": "{{ default_cost|int }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.filter_list",
            "getval": re.compile(
                r"""\s+area
                    \s*(?P<area_id>\S+)*
                    \s*filter-list\sprefix*
                    \s*(?P<name>\S+)*
                    \s*(?P<dir>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_filter,
            "compval": "filter_list",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "filter_list": [
                                    {
                                        "name": "{{ name }}",
                                        "direction": "{{ dir }}",
                                    }
                                ],
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.nssa",
            "getval": re.compile(
                r"""\s+area*
                    \s*(?P<area_id>\S+)*
                    \s*(?P<nssa>nssa)*
                    \s*(?P<no_redis>no-redistribution)*
                    \s*(?P<def_origin>default-information-originate)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<nssa_only>nssa-only)*
                    \s*(?P<no_summary>no-summary)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_nssa,
            "compval": "nssa",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "set": "{{ True if nssa is defined and def_origin is undefined and "
                                    "no_ext is undefined and no_redis is undefined and nssa_only is undefined }}",
                                    "default_information_originate": {
                                        "set": "{{ True if def_origin is defined and metric is undefined and "
                                        "metric_type is undefined and nssa_only is undefined }}",
                                        "metric": "{{ metric.split("
                                        ")[1]|int }}",
                                        "metric_type": "{{ metric_type.split("
                                        ")[1]|int }}",
                                        "nssa_only": "{{ True if nssa_only is defined }}",
                                    },
                                    "no_ext_capability": "{{ True if no_ext is defined }}",
                                    "no_redistribution": "{{ True if no_redis is defined }}",
                                    "no_summary": "{{ True if no_summary is defined }}",
                                },
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.nssa.translate",
            "getval": re.compile(
                r"""\s+area*
                    \s*(?P<area_id>\S+)*
                    \s*(?P<nssa>nssa)*
                    \stranslate\stype7*
                    \s(?P<translate_always>always)*
                    \s* (?P<translate_supress>suppress-fa)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_nssa_translate,
            "compval": "nssa.translate",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "nssa": {
                                    "translate": "{{ translate_always if translate_always is defined else translate_supress if translate_supress is defined }}"
                                },
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.ranges",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \srange
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    \s(?P<netmask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*((?P<advertise>advertise)|(?P<not_advertise>not-advertise))*
                    \s*(?P<cost>cost\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_ranges,
            "compval": "ranges",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "ranges": [
                                    {
                                        "address": "{{ address }}",
                                        "netmask": "{{ netmask }}",
                                        "advertise": "{{ True if advertise is defined }}",
                                        "cost": "{{ cost.split(" ")[1]|int }}",
                                        "not_advertise": "{{ True if not_advertise is defined }}",
                                    }
                                ],
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.sham_link",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \ssham-link
                    \s(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    \s(?P<destination>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<cost>cost\s\d+)*
                    \s*(?P<ttl_security>ttl-security\shops\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_sham_link,
            "compval": "sham_link",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "sham_link": {
                                    "source": "{{ source }}",
                                    "destination": "{{ destination }}",
                                    "cost": "{{ cost.split(" ")[1]|int }}",
                                    "ttl_security": '{{ ttl_security.split("hops ")[1] }}',
                                },
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.area.stub",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \s(?P<stub>stub)*
                    \s*(?P<no_ext>no-ext-capability)*
                    \s*(?P<no_sum>no-summary)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_stub_link,
            "compval": "stub",
            "result": {
                "address_family": [
                    {
                        "areas": {
                            "{{ area_id }}": {
                                "area_id": "{{ area_id }}",
                                "stub": {
                                    "set": "{{ True if stub is defined and no_ext is undefined and no_sum is undefined }}",
                                    "no_ext_capability": "{{ True if no_ext is defined }}",
                                    "no_summary": "{{ True if no_sum is defined }}",
                                },
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.auto_cost",
            "getval": re.compile(
                r"""\s+(?P<auto_cost>auto-cost)*
                    \s*(?P<ref_band>reference-bandwidth\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_auto_cost,
            "compval": "auto_cost",
            "result": {
                "address_family": [
                    {
                        "auto_cost": {
                            "set": "{{ True if auto_cost is defined and ref_band is undefined }}",
                            "reference_bandwidth": '{{ ref_band.split(" ")[1] }}',
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.bfd",
            "getval": re.compile(
                r"""\s+bfd*
                    \s*(?P<bfd>all-interfaces)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "bfd all-interfaces",
            "compval": "bfd",
            "result": {
                "address_family": [{"bfd": "{{ True if bfd is defined }}"}]
            },
        },
        {
            "name": "address_family.capability",
            "getval": re.compile(
                r"""\s+capability*
                    \s*((?P<lls>lls)|(?P<opaque>opaque)|(?P<transit>transit)|(?P<vrf_lite>vrf-lite))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_capability,
            "compval": "capability",
            "result": {
                "address_family": [
                    {
                        "capability": {
                            "lls": "{{ True if lls is defined }}",
                            "opaque": "{{ True if opaque is defined }}",
                            "transit": "{{ True if transit is defined }}",
                            "vrf_lite": "{{ True if vrf_lite is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.compatible",
            "getval": re.compile(
                r"""\s+compatible*
                    \s*((?P<rfc1583>rfc1583)|(?P<rfc1587>rfc1587)|(?P<rfc5243>rfc5243))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_compatible,
            "compval": "compatible",
            "result": {
                "address_family": [
                    {
                        "compatible": {
                            "rfc1583": "{{ True if rfc1583 is defined }}",
                            "rfc1587": "{{ True if rfc1587 is defined }}",
                            "rfc5243": "{{ True if rfc5243 is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.default_information",
            "getval": re.compile(
                r"""\s+default-information*
                    \s*(?P<originate>originate)*
                    \s*(?P<always>always)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<route_map>route-map\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_default_information,
            "compval": "default_information",
            "result": {
                "address_family": [
                    {
                        "default_information": {
                            "originate": "{{ True if originate is defined }}",
                            "always": "{{ True if always is defined }}",
                            "metric": "{{ metric.split(" ")[1]|int }}",
                            "metric_type": "{{ metric_type.split("
                            ")[1]|int }}",
                            "route_map": "{{ route_map.split(" ")[1] }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.default_metric",
            "getval": re.compile(
                r"""\s+default-metric(?P<default_metric>\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric }}",
            "compval": "default_metric",
            "result": {
                "address_family": [
                    {"default_metric": "{{ default_metric| int}}"}
                ]
            },
        },
        {
            "name": "address_family.discard_route",
            "getval": re.compile(
                r"""\s+(?P<discard_route>discard-route)*
                    \s*(?P<external>external\s\d+)*
                    \s*(?P<internal>internal\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_discard_route,
            "compval": "discard_route",
            "result": {
                "address_family": [
                    {
                        "discard_route": {
                            "set": "{{ True if discard_route is defined and external is undefined and internal is undefined }}",
                            "external": "{{ external.split(" ")[1]|int }}",
                            "internal": "{{ internal.split(" ")[1]|int }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.distance.admin_distance",
            "getval": re.compile(
                r"""\s+distance
                    \s(?P<admin_dist>\S+)*
                    \s*(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<wildcard>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<acl>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distance_admin_distance,
            "compval": "admin_distance",
            "result": {
                "address_family": [
                    {
                        "distance": {
                            "admin_distance": {
                                "distance": "{{ admin_dist }}",
                                "address": "{{ source }}",
                                "wildcard_bits": "{{ wildcard }}",
                                "acl": "{{ acl }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.distance.ospf",
            "getval": re.compile(
                r"""\s+distance
                    \sospf*
                    \s*(?P<intra>intra-area\s\d+)*
                    \s*(?P<inter>inter-area\s\d+)*
                    \s*(?P<external>external\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distance_ospf,
            "compval": "ospf",
            "result": {
                "address_family": [
                    {
                        "distance": {
                            "ospf": {
                                "inter_area": "{{ inter.split(" ")[1]|int }}",
                                "intra_area": "{{ intra.split(" ")[1]|int }}",
                                "external": "{{ external.split(" ")[1]|int }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.distribute_list.acls",
            "getval": re.compile(
                r"""\s+distribute-list
                    \s(?P<name>\S+)*
                    \s*(?P<dir>\S+)*
                    \s*(?P<int_pro>\S+\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distribute_list_acls,
            "compval": "distribute_list.acls",
            "result": {
                "address_family": [
                    {
                        "distribute_list": {
                            "acls": [
                                {
                                    "name": "{{ name }}",
                                    "direction": "{{ dir }}",
                                    "interface": '{{ int_pro if dir == "in" }}',
                                    "protocol": '{{ int_pro if dir == "out" }}',
                                }
                            ]
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.distribute_list.prefix",
            "getval": re.compile(
                r"""\s+distribute-list
                    \s(?P<prefix>prefix\s\S+)*
                    \s*(?P<gateway>gateway\s\S+)*
                    \s*(?P<dir>\S+)*
                    \s*(?P<int_pro>\S+\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_distribute_list_prefix,
            "compval": "distribute_list.prefix",
            "result": {
                "address_family": [
                    {
                        "distribute_list": {
                            "prefix": {
                                "name": "{{ prefix.split(" ")[1] }}",
                                "gateway_name": "{{ gateway.split("
                                ")[1] if prefix is defined }}",
                                "direction": "{{ dir if gateway is undefined }}",
                                "interface": '{{ int_pro if dir == "in" }}',
                                "protocol": '{{ int_pro if dir == "out" }}',
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.distribute_list.route_map",
            "getval": re.compile(
                r"""\s+distribute-list
                    \s(?P<route_map>route-map\s\S+)*
                    \s*(?P<dir>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "distribute-list route-map {{ distribute_list.route_map.name }} in",
            "compval": "distribute_list.route_map",
            "result": {
                "address_family": [
                    {
                        "distribute_list": {
                            "route_map": {
                                "name": "{{ route_map.split(" ")[1] }}"
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.domain_id",
            "getval": re.compile(
                r"""\s+domain-id
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<secondary>secondary)*
                    \s*(?P<null>null)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_domain_id,
            "compval": "domain_id",
            "result": {
                "address_family": [
                    {
                        "domain_id": {
                            "ip_address": {
                                "address": "{{ address }}",
                                "secondary": "{{ True if secondary is defined }}",
                            },
                            "null": "{{ True if null is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.domain_tag",
            "getval": re.compile(
                r"""\s+domain-tag
                    \s(?P<tag>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "domain-tag {{ domain_tag }}",
            "compval": "domain_tag",
            "result": {"address_family": [{"domain_tag": "{{ tag|int }}"}]},
        },
        {
            "name": "address_family.graceful_restart",
            "getval": re.compile(
                r"""\s+graceful-restart*
                    \s*(?P<enable>helper)*
                    \s*(?P<disable>disable)*
                    \s*(?P<lsa>strict-lsa-checking)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_address_family_graceful_restart,
            "compval": "graceful_restart",
            "result": {
                "address_family": [
                    {
                        "event_log": {
                            "enable": "{{ True if is enable defined }}",
                            "disable": "{{ True if disable is defined }}",
                            "strict_lsa_checking": "{{ True if lsa is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.event_log",
            "getval": re.compile(
                r"""\s+(?P<event_log>event-log)*
                    \s*(?P<one_shot>one-shot)*
                    \s*(?P<pause>pause)*
                    \s*(?P<size>size\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_event_log,
            "compval": "event_log",
            "result": {
                "address_family": [
                    {
                        "event_log": {
                            "enable": "{{ True if event_log is defined and one_shot is undefined and pause is undefined and size is undefined }}",
                            "one_shot": "{{ True if one_shot is defined }}",
                            "pause": "{{ True if pause is defined }}",
                            "size": "{{ size.split(" ")[1]|int }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.help",
            "getval": re.compile(
                r"""\s+(?P<help>help)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "help",
            "compval": "help",
            "result": {
                "address_family": [{"help": "{{ True if help is defined }}"}]
            },
        },
        {
            "name": "address_family.interface_id",
            "getval": re.compile(
                r"""\s+(?P<interface_id>interface-id\ssnmp-if-index)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "interface-id snmp-if-index",
            "compval": "interface_id",
            "result": {
                "address_family": [
                    {"interface_id": "{{ True if interface_id is defined }}"}
                ]
            },
        },
        {
            "name": "address_family.limit",
            "getval": re.compile(
                r"""\s+limit\sretransmissions
                    \s((?P<dc_num>dc\s\d+)|(?P<dc_disable>dc\sdisable))*
                    \s*((?P<non_dc_num>non-dc\s\d+)|(?P<non_dc_disable>non-dc\sdisable))
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_limit,
            "compval": "limit",
            "result": {
                "address_family": [
                    {
                        "limit": {
                            "dc": {
                                "number": "{{ dc_num.split(" ")[1]|int }}",
                                "disable": "{{ True if dc_disable is defined }}",
                            },
                            "non_dc": {
                                "number": "{{ non_dc_num.split(" ")[1]|int }}",
                                "disable": "{{ True if dc_disable is defined }}",
                            },
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.local_rib_criteria",
            "getval": re.compile(
                r"""\s+(?P<local>local-rib-criteria)*
                    \s*(?P<forward>forwarding-address)*
                    \s*(?P<inter>inter-area-summary)*
                    \s*(?P<nssa>nssa-translation)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_vrf_local_rib_criteria,
            "compval": "local_rib_criteria",
            "result": {
                "address_family": [
                    {
                        "local_rib_criteria": {
                            "enable": "{{ True if local is defined and forward is undefined and inter is undefined and nssa is undefined }}",
                            "forwarding_address": "{{ True if forward is defined }}",
                            "inter_area_summary": "{{ True if inter is defined }}",
                            "nssa_translation": "{{ True if nssa is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.log_adjacency_changes",
            "getval": re.compile(
                r"""\s+(?P<log>log-adjacency-changes)*
                    \s*(?P<detail>detail)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_log_adjacency_changes,
            "compval": "log_adjacency_changes",
            "result": {
                "address_family": [
                    {
                        "log_adjacency_changes": {
                            "set": "{{ True if log is defined and detail is undefined }}",
                            "detail": "{{ True if detail is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.manet",
            "getval": re.compile(
                r"""\s+manet*
                    \s*(?P<cache>cache)*
                    \s*(?P<acknowledgement>acknowledgement\s\d+)*
                    \s*(?P<update>update\s\d+)*
                    \s*(?P<hello>hello)*
                    \s*(?P<unicast>unicast)*
                    \s*(?P<multicast>multicast)*
                    \s*(?P<peering>peering\sselective)*
                    \s*(?P<disable>disable)*
                    \s*(?P<per_interface>per-interface)*
                    \s*(?P<redundancy>redundancy\s\d+)*
                    \s*(?P<willingness>willingness\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_lsa,
            "compval": "manet",
            "result": {
                "address_family": [
                    {
                        "manet": {
                            "cache": {
                                "acknowledgement": "{{ acknowledgement.split("
                                ")[1] }}",
                                "update": "{{ update.split(" ")[1] }}",
                            },
                            "hello": {
                                "unicast": "{{ True if unicast is defined }}",
                                "multicast": "{{ True if multicast is defined }}",
                            },
                            "peering": {
                                "set": "{{ True if peering is defined  }}",
                                "disable": "{{ True if disable is defined }}",
                                "per_interface": "{{ True if per_interface is defined }}",
                                "redundancy": "{{ redundancy.split(" ")[1] }}",
                            },
                            "willingness": "{{ willingness.split(" ")[1] }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.max_lsa",
            "getval": re.compile(
                r"""\s+max-lsa
                    \s(?P<number>\d+)*
                    \s*(?P<threshold>\d+)*
                    \s*(?P<ignore_count>ignore-count\s\d+)*
                    \s*(?P<ignore_time>ignore-time\s\d+)*
                    \s*(?P<reset_time>reset-time\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_lsa,
            "compval": "max_lsa",
            "result": {
                "address_family": [
                    {
                        "max_lsa": {
                            "number": "{{ number }}",
                            "threshold_value": "{{ threshold }}",
                            "ignore_count": "{{ ignore_count.split(" ")[1] }}",
                            "ignore_time": "{{ ignore_time.split(" ")[1] }}",
                            "reset_time": "{{ reset_time.split(" ")[1] }}",
                            "warning_only": "{{ True if warning is defined }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.max_metric",
            "getval": re.compile(
                r"""\s+max-metric*
                    \s*(?P<router_lsa>router-lsa)*
                    \s*(?P<include_stub>include-stub)*
                    \s*(?P<external_lsa>external-lsa\s\d+)*
                    \s*(?P<startup_time>on-startup\s\d+)*
                    \s*(?P<startup_wait>on-startup\s\S+)*
                    \s*(?P<summary_lsa>summary-lsa\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_metric,
            "compval": "max_metric",
            "result": {
                "address_family": [
                    {
                        "max_metric": {
                            "router_lsa": "{{ True if router_lsa is defined }}",
                            "external_lsa": "{{ external_lsa.split(" ")[1] }}",
                            "include_stub": "{{ ignore_count.split(" ")[1] }}",
                            "on_startup": {
                                "time": "{{ startup_time.split(" ")[1] }}",
                                "wait_for_bgp": "{{ True if startup_wait is defined }}",
                            },
                            "summary_lsa": "{{ summary_lsa.split(" ")[1] }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.maximum_paths",
            "getval": re.compile(
                r"""\s+maximum-paths*
                    \s+(?P<paths>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths {{ maximum_paths }}",
            "compval": "maximum_paths",
            "result": {"address_family": [{"maximum_paths": "{{ paths }}"}]},
        },
        {
            "name": "address_family.passive_interface",
            "getval": re.compile(
                r"""\s+passive-interface
                    \s(?P<interface>\S+\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "passive-interface {{ passive_interface }}",
            "compval": "passive_interface",
            "result": {
                "address_family": [{"passive_interface": "{{ interface }}"}]
            },
        },
        {
            "name": "address_family.prefix_suppression",
            "getval": re.compile(
                r"""\s+(?P<prefix_sup>prefix-suppression)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "prefix-suppression",
            "compval": "prefix_suppression",
            "result": {
                "address_family": [
                    {
                        "prefix_suppression": "{{ True if prefix_sup is defined }}"
                    }
                ]
            },
        },
        {
            "name": "address_family.queue_depth.hello",
            "getval": re.compile(
                r"""\s+queue-depth
                    \shello*
                    \s*(?P<max_packets>\d+)*
                    \s*(?P<unlimited>unlimited)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_queue_depth_hello,
            "compval": "hello",
            "result": {
                "address_family": [
                    {
                        "queue_depth": {
                            "hello": {
                                "max_packets": "{{ max_packets }}",
                                "unlimited": "{{ True if unlimited is defined }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.queue_depth.update",
            "getval": re.compile(
                r"""\s+queue-depth
                    \supdate*
                    \s*(?P<max_packets>\d+)*
                    \s*(?P<unlimited>unlimited)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_queue_depth_update,
            "compval": "update",
            "result": {
                "address_family": [
                    {
                        "queue_depth": {
                            "update": {
                                "max_packets": "{{ max_packets }}",
                                "unlimited": "{{ True if unlimited is defined }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.router_id",
            "getval": re.compile(
                r"""\s+router-id
                    \s(?P<id>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
                    *$""",
                re.VERBOSE,
            ),
            "setval": "router-id {{ router_id }}",
            "compval": "router_id",
            "result": {"address_family": [{"router_id": "{{ id }}"}]},
        },
        {
            "name": "address_family.summary_prefix",
            "getval": re.compile(
                r"""\s+summary-address
                    \s(?P<address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                    \s*(?P<not_adv>not-advertise)*
                    \s*(?P<nssa>nssa-only)*
                    \s*(?P<tag>tag\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_summary_prefix,
            "compval": "summary_prefix",
            "result": {
                "address_family": [
                    {
                        "summary_prefix": {
                            "address": "{{ address }}",
                            "mask": "{{ mask }}",
                            "not_advertise": "{{ True if not_adv is defined }}",
                            "nssa_only": "{{ True if nssa is defined }}",
                            "tag": "{{ tag.split(" ")[1] }}",
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.shutdown",
            "getval": re.compile(
                r"""\s+(?P<shutdown>shutdown)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "shutdown",
            "compval": "shutdown",
            "result": {
                "address_family": [
                    {"shutdown": "{{ True if shutdown is defined }}"}
                ]
            },
        },
        {
            "name": "address_family.timers.lsa",
            "getval": re.compile(
                r"""\s+timers
                    \slsa
                    \sarrival
                    \s(?P<lsa>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers lsa arrival {{ timers.lsa }}",
            "compval": "lsa",
            "result": {"address_family": [{"timers": {"lsa": "{{ lsa }}"}}]},
        },
        {
            "name": "address_family.timers.pacing",
            "getval": re.compile(
                r"""\s+timers
                    \spacing
                    \s(?P<flood>flood\s\d+)*
                    \s*(?P<lsa_group>lsa-group\s\d+)*
                    \s*(?P<retransmission>retransmission\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_timers_pacing,
            "compval": "pacing",
            "result": {
                "address_family": [
                    {
                        "timers": {
                            "pacing": {
                                "flood": "{{ flood.split(" ")[1] }}",
                                "lsa_group": "{{ lsa_group.split(" ")[1] }}",
                                "retransmission": "{{ retransmission.split("
                                ")[1] }}",
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.timers.throttle.lsa",
            "getval": re.compile(
                r"""\s+timers
                    \sthrottle
                    \s*(?P<lsa>lsa)*
                    \s*(?P<first_delay>\d+)*
                    \s*(?P<min_delay>\d+)*
                    \s*(?P<max_delay>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers throttle lsa {{ throttle.lsa.first_delay }} {{ throttle.lsa.min_delay }} {{ throttle.lsa.max_delay }}",
            "compval": "throttle.lsa",
            "result": {
                "address_family": [
                    {
                        "timers": {
                            "throttle": {
                                "lsa": {
                                    "first_delay": "{{ first_delay }}",
                                    "min_delay": "{{ min_delay }}",
                                    "max_delay": "{{ max_delay }}",
                                }
                            }
                        }
                    }
                ]
            },
        },
        {
            "name": "address_family.timers.throttle.spf",
            "getval": re.compile(
                r"""\s+timers
                    \sthrottle
                    \s*(?P<spf>spf)*
                    \s*(?P<first_delay>\d+)*
                    \s*(?P<min_delay>\d+)*
                    \s*(?P<max_delay>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers throttle spf {{ throttle.spf.receive_delay }} {{ throttle.spf.between_delay }} {{ throttle.spf.max_delay }}",
            "compval": "throttle.spf",
            "result": {
                "address_family": [
                    {
                        "timers": {
                            "throttle": {
                                "spf": {
                                    "receive_delay": "{{ first_delay }}",
                                    "between_delay": "{{ min_delay }}",
                                    "max_delay": "{{ max_delay }}",
                                }
                            }
                        }
                    }
                ]
            },
        },
    ]
