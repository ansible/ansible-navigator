#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The eos ospfv2 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
import re
from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.argspec.ospfv2.ospfv2 import (
    Ospfv2Args,
)


class Ospfv2Facts(object):
    """ The eos ospfv2 fact class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospfv2Args.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_device_data(self, connection):
        return connection.get("show running-config | section ospf")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for ospfv2
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = self.get_device_data(connection)

        # split the config into instances of the resource
        resource_delim = "router ospf"
        find_pattern = r"(?:^|\n)%s.*?(?=(?:^|\n)%s|$)" % (
            resource_delim,
            resource_delim,
        )
        resources = [
            p.strip() for p in re.findall(find_pattern, data, re.DOTALL)
        ]
        objs_list = []
        objs = {}
        for resource in resources:
            if resource and "router ospfv3" not in resource:
                obj = self.render_config(self.generated_spec, resource)
                if obj:
                    objs_list.append(obj)
        objs = {"processes": objs_list}
        ansible_facts["ansible_network_resources"].pop("ospfv2", None)

        facts = {}
        if objs:
            facts["ospfv2"] = {}
            params = utils.validate_config(
                self.argument_spec, {"config": objs}
            )
            facts["ospfv2"].update(utils.remove_empties(params["config"]))

        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def render_config(self, spec, conf):
        """
        Render config as dictionary structure and delete keys
          from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        instance_list = []
        ospf_params_dict = {}
        areas_list = []
        distance_dict = {}
        network_list = []
        redistribute_list = []
        timers_list = []
        areas_list = []
        for dev_config in conf.split("\n"):
            if not dev_config:
                continue
            network_dict = {}
            redistribute_dict = {}
            dev_config = dev_config.strip()
            dev_config = re.sub(r"-", "_", dev_config).strip()
            matches = re.findall(r"router (ospf) (.*)", dev_config)
            if matches:
                if ospf_params_dict:
                    instance_list.append(ospf_params_dict)
                    ospf_params_dict = {}
                instance = matches[0][1].split()
                ospf_params_dict.update({"process_id": str(instance[0])})
                if "vrf" in dev_config:
                    vrf_name = instance[-1]
                else:
                    vrf_name = None
                ospf_params_dict.update({"vrf": vrf_name})
            if "traffic_engineering" in dev_config:
                ospf_params_dict.update({"traffic_engineering": True})
            config_params = dev_config.split()
            if config_params[0] == "adjacency":
                threshold = config_params[-1]
                adjacency_dict = {"exchange_start": {"threshold": threshold}}
                ospf_params_dict.update({"adjacency": adjacency_dict})
            elif "auto_cost" in dev_config:
                bw = config_params[-1]
                ospf_params_dict.update(
                    {"auto_cost": {"reference_bandwidth": bw}}
                )
            elif "bfd" in dev_config:
                ospf_params_dict.update({"bfd": {"all_interfaces": True}})
            elif config_params[0] == "default_information":
                def_dict = {"originate": True}
                for i, val in enumerate(config_params[2::]):
                    if val == "always":
                        def_dict.update({"always": True})
                    elif val in ["route_map", "metric", "metric_type"]:
                        def_dict.update({val: config_params[i + 3]})
                ospf_params_dict.update({"default_information": def_dict})
            elif "default_metric" in dev_config:
                ospf_params_dict.update({"default_metric": config_params[-1]})
            elif "distance" in dev_config:
                distance_dict.update({config_params[-2]: config_params[-1]})
                ospf_params_dict.update({"distance": distance_dict})
            elif "distribute_list" in dev_config:
                ospf_params_dict.update(
                    {"distribute_list": {config_params[1]: config_params[2]}}
                )
            elif "dn_bit_ignore" in dev_config:
                ospf_params_dict.update({"dn_bit_ignore": True})
            elif "fips_restrictions" in dev_config:
                ospf_params_dict.update({"fips_restrictions": True})
            elif "graceful_restart" in dev_config:
                if "grace_period" in dev_config:
                    ospf_params_dict.update(
                        {
                            "graceful_restart": {
                                "grace_period": config_params[-1]
                            }
                        }
                    )
                else:
                    ospf_params_dict.update(
                        {"graceful_restart": {"set": True}}
                    )
            elif "graceful_restart_helper" in dev_config:
                ospf_params_dict.update({"graceful_restart_helper": True})
            elif "log_adjacency_changes" in dev_config:
                detail = True if "detail" in dev_config else False
                ospf_params_dict.update(
                    {"log_adjacency_changes": {"detail": detail}}
                )
            elif "max_lsa" in dev_config:
                max_lsa_dict = {}
                config_params.pop(0)
                max_lsa_dict.update({"count": config_params.pop(0)})
                if config_params:
                    if config_params[0].isdigit():
                        max_lsa_dict.update(
                            {"threshold": config_params.pop(0)}
                        )
                    for i, el in enumerate(config_params):
                        if el == "warning_only":
                            max_lsa_dict.update({"warning": True})
                        if el in ["ignore_count", "ignore_time", "reset_time"]:
                            max_lsa_dict.update({el: config_params[i + 1]})
                ospf_params_dict.update({"max_lsa": max_lsa_dict})
            elif "maximum_paths" in dev_config:
                ospf_params_dict.update({"maximum_paths": config_params[1]})
            elif "mpls ldp sync default" in dev_config:
                ospf_params_dict.update({"mpls_ldp": True})
            elif config_params[0] == "network":
                config_params.pop(0)
                prefix = re.search(r"\/", config_params[0])
                if prefix:
                    network_dict.update({"prefix": config_params.pop(0)})
                else:
                    network_dict.update(
                        {"network_address": config_params.pop(0)}
                    )
                    network_dict.update({"mask": config_params.pop(0)})
                network_dict.update({"area": config_params[-1]})
                network_list.append(network_dict)
                ospf_params_dict.update({"networks": network_list})
            elif "passive_interface" in dev_config:
                if config_params[1] == "default":
                    ospf_params_dict.update(
                        {"passive_interface": {"default": True}}
                    )
                else:
                    ospf_params_dict.update(
                        {
                            "passive_interface": {
                                "interface_list": config_params[1]
                            }
                        }
                    )
            elif "point_to_point" in dev_config:
                ospf_params_dict.update({"point_to_point": True})
            elif "redistribute" in dev_config:
                redistribute_dict.update({"routes": config_params[1]})
                if config_params[1] == "isis":
                    if "level" in config_params[2]:
                        k = re.sub(r"_", "-", config_params[2])
                        redistribute_dict.update({"isis_level": k})
                if "route_map" in dev_config:
                    redistribute_dict.update({"route_map": config_params[-1]})
                redistribute_list.append(redistribute_dict)
                ospf_params_dict.update({"redistribute": redistribute_list})
            elif "router_id" in dev_config:
                ospf_params_dict.update({"router_id": config_params[-1]})
            elif "retransmission_threshold" in dev_config:
                ospf_params_dict.update(
                    {"retransmission_threshold": config_params[-1]}
                )
            elif config_params[0] == "compatible":
                ospf_params_dict.update({"rfc1583compatibility": True})
            elif "shutdown" in dev_config:
                ospf_params_dict.update({"shutdown": True})
            elif "summary_address" in dev_config:
                summary_address_dict = {}
                config_params.pop(0)
                prefix = re.search(r"\/", config_params[0])
                if prefix:
                    summary_address_dict.update(
                        {"prefix": config_params.pop(0)}
                    )
                else:
                    summary_address_dict.update(
                        {"address": config_params.pop(0)}
                    )
                    summary_address_dict.update({"mask": config_params.pop(0)})
                if "not_advertise" in dev_config:
                    summary_address_dict.update({"not_advertise": True})
                    config_params.pop(0)
                else:
                    if config_params:
                        summary_address_dict.update(
                            {config_params[0]: config_params[1]}
                        )
                ospf_params_dict.update(
                    {"summary_address": summary_address_dict}
                )
            elif "timers" in dev_config:
                timers_dict = {}
                if config_params[1] == "lsa":
                    if config_params[2] == "rx":
                        timers_dict.update(
                            {
                                "lsa": {
                                    "rx": {"min_interval": config_params[-1]}
                                }
                            }
                        )
                    else:
                        timers_dict.update(
                            {
                                "lsa": {
                                    "tx": {
                                        "delay": {
                                            "initial": config_params[-3],
                                            "min": config_params[-2],
                                            "max": config_params[-1],
                                        }
                                    }
                                }
                            }
                        )
                elif config_params[1] == "out_delay":
                    timers_dict.update({"out_delay": config_params[-1]})
                elif config_params[1] == "pacing":
                    timers_dict.update({"pacing": config_params[-1]})
                elif config_params[1] == "spf":
                    if config_params[2] == "delay":
                        timers_dict.update(
                            {
                                "spf": {
                                    "tx": {
                                        "delay": {
                                            "initial": config_params[-3],
                                            "min": config_params[-2],
                                            "max": config_params[-1],
                                        }
                                    }
                                }
                            }
                        )
                    else:
                        timers_dict.update(
                            {"spf": {"seconds": config_params[-1]}}
                        )
                timers_list.append(timers_dict)
                ospf_params_dict.update({"timers": timers_list})
            elif config_params[0] == "area":
                areas_dict = {}
                areas_dict.update({"area_id": config_params[1]})
                if config_params[2] == "default_cost":
                    areas_dict.update({"default_cost": config_params[-1]})
                elif config_params[2] == "filter":
                    prefix = re.search(r"\/", config_params[3])
                    if prefix:
                        areas_dict.update(
                            {"filter": {"address": config_params[3]}}
                        )
                    elif config_params[3] == "prefix_list":
                        areas_dict.update(
                            {"filter": {"prefix_list": config_params[-1]}}
                        )
                    else:
                        areas_dict.update(
                            {"filter": {"subnet_address": config_params[3]}}
                        )
                        areas_dict.update(
                            {"filter": {"subnet_mask": config_params[4]}}
                        )
                elif config_params[2] == "not_so_stubby":
                    if len(config_params) == 3:
                        areas_dict.update({"not_so_stubby": {"set": True}})
                        continue
                    if config_params[3] == "lsa":
                        areas_dict.update({"not_so_stubby": {"lsa": True}})
                    elif config_params[3] == "default_information_originate":
                        default_dict = {}
                        for i, val in enumerate(config_params):
                            if val == "nssa_only":
                                default_dict.update({"nssa_only": True})
                            if val == "metric_type":
                                default_dict.update(
                                    {"metric_type": config_params[i + 1]}
                                )
                            if val == "metric":
                                default_dict.update(
                                    {"metric": config_params[i + 1]}
                                )
                        areas_dict.update(
                            {
                                "not_so_stubby": {
                                    "default_information_originate": default_dict
                                }
                            }
                        )
                    elif config_params[3] == "no_summary":
                        areas_dict.update(
                            {"not_so_stubby": {"no_summary": True}}
                        )
                    elif config_params[3] == "nssa_only":
                        areas_dict.update(
                            {"not_so_stubby": {"nssa_only": True}}
                        )
                elif config_params[2] == "nssa":
                    if len(config_params) == 3:
                        areas_dict.update({"nssa": {"set": True}})
                        continue
                    if config_params[3] == "default_information_originate":
                        default_dict = {}
                        for i, val in enumerate(config_params):
                            if val == "nssa_only":
                                default_dict.update({"nssa_only": True})
                            if val == "metric_type":
                                default_dict.update(
                                    {"metric_type": config_params[i + 1]}
                                )
                            if val == "metric":
                                default_dict.update(
                                    {"metric": config_params[i + 1]}
                                )
                        areas_dict.update(
                            {
                                "nssa": {
                                    "default_information_originate": default_dict
                                }
                            }
                        )
                    elif config_params[3] == "no_summary":
                        areas_dict.update({"nssa": {"no_summary": True}})
                    elif config_params[3] == "nssa_only":
                        areas_dict.update({"nssa": {"nssa_only": True}})
                elif config_params[2] == "range":
                    prefix = re.search(r"\/", config_params[3])
                    range_dict = {}
                    if prefix:
                        range_dict.update({"address": config_params[3]})
                    else:
                        range_dict.update({"subnet_address": config_params[3]})
                        range_dict.update({"subnet_mask": config_params[4]})
                    if "advertise" in dev_config:
                        range_dict.update({"advertise": True})
                    if "not_advertise" in dev_config:
                        range_dict.update({"advertise": False})
                    if "cost" in dev_config:
                        range_dict.update({"cost": config_params[-1]})
                    areas_dict.update({"range": range_dict})
                elif config_params[2] == "stub":
                    if "no_summary" in dev_config:
                        areas_dict.update({"stub": {"no_summary": True}})
                    else:
                        areas_dict.update({"stub": {"set": True}})
                areas_list.append(areas_dict)
                ospf_params_dict.update({"areas": areas_list})
            elif config_params[0] == "max_metric":
                config_params.pop(0)
                router_lsa_dict = {}
                config_params.pop(0)
                if not config_params:
                    ospf_params_dict.update(
                        {"max_metric": {"router_lsa": {"set": True}}}
                    )
                else:
                    for i, val in enumerate(config_params):
                        if val == "include_stub":
                            router_lsa_dict.update({"include_stub": True})
                        elif val == "on_startup":
                            if config_params[i + 1] == "wait_for_bgp":
                                router_lsa_dict.update(
                                    {"on_startup": {"wait_for_bgp": True}}
                                )
                            else:
                                router_lsa_dict.update(
                                    {
                                        "on_startup": {
                                            "time": config_params[i + 1]
                                        }
                                    }
                                )
                        elif val == "external_lsa":
                            if (
                                i < len(config_params)
                                and config_params[i + 1].isdigit()
                            ):
                                router_lsa_dict.update(
                                    {
                                        "external_lsa": {
                                            "max_metric_value": config_params[
                                                i + 1
                                            ]
                                        }
                                    }
                                )
                            else:
                                router_lsa_dict.update(
                                    {"external_lsa": {"set": True}}
                                )
                        elif val == "summary_lsa":
                            if (
                                i < len(config_params) - 1
                                and config_params[i + 1].isdigit()
                            ):
                                router_lsa_dict.update(
                                    {
                                        "summary_lsa": {
                                            "max_metric_value": config_params[
                                                i + 1
                                            ]
                                        }
                                    }
                                )
                            else:
                                router_lsa_dict.update(
                                    {"summary_lsa": {"set": True}}
                                )
                    ospf_params_dict.update(
                        {"max_metric": {"router_lsa": router_lsa_dict}}
                    )
        # instance_list.append(ospf_params_dict)
        # config.update({"ospf_version": "v2", "ospf_processes": instance_list})
        return utils.remove_empties(ospf_params_dict)
