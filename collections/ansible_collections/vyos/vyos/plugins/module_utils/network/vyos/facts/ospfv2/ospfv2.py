#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The vyos ospfv2 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from re import findall, search, M
from copy import deepcopy
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.ospfv2.ospfv2 import (
    Ospfv2Args,
)


class Ospfv2Facts(object):

    """The vyos ospfv2 fact class"""

    def __init__(
        self,
        module,
        subspec="config",
        options="options",
    ):

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
        return connection.get_config()

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for ospfv2
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = self.get_device_data(connection)

            # typically data is populated from the current device configuration
            # data = connection.get('show running-config | section ^interface')
            # using mock data instead

        objs = {}
        ospfv2 = findall(r"^set protocols ospf (.+)", data, M)
        if ospfv2:
            objs = self.render_config(ospfv2)
        facts = {}
        params = utils.validate_config(self.argument_spec, {"config": objs})
        facts["ospfv2"] = utils.remove_empties(params["config"])
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def render_config(self, conf):
        """
        Render config as dictionary structure

        :param conf: The configuration
        :returns: The generated config
        """

        conf = "\n".join(filter(lambda x: x, conf))
        a_lst = ["default_metric", "log_adjacency_changes"]
        config = self.parse_attr(conf, a_lst)

        if not config:
            config = {}
        config["timers"] = self.parse_timers(conf)
        config["auto_cost"] = self.parse_auto_cost(conf)
        config["distance"] = self.parse_distance(conf)
        config["max_metric"] = self.parse_max_metric(conf)
        config["default_information"] = self.parse_def_info(conf)
        config["route_map"] = self.parse_leaf_list(conf, "route-map")
        config["mpls_te"] = self.parse_attrib(conf, "mpls_te", "mpls-te")
        config["areas"] = self.parse_attrib_list(conf, "area", "area_id")
        config["parameters"] = self.parse_attrib(
            conf, "parameters", "parameters"
        )
        config["neighbor"] = self.parse_attrib_list(
            conf, "neighbor", "neighbor_id"
        )
        config["passive_interface"] = self.parse_leaf_list(
            conf, "passive-interface"
        )
        config["redistribute"] = self.parse_attrib_list(
            conf, "redistribute", "route_type"
        )
        config["passive_interface_exclude"] = self.parse_leaf_list(
            conf, "passive-interface-exclude"
        )
        return config

    def parse_timers(self, conf):
        """
        This function triggers the parsing of 'timers' attributes
        :param conf: configuration
        :return: generated config dictionary
        """

        cfg_dict = {}
        cfg_dict["refresh"] = self.parse_refresh(conf, "refresh")
        cfg_dict["throttle"] = self.parse_throttle(conf, "spf")
        return cfg_dict

    def parse_throttle(self, conf, attrib=None):
        """
        This function triggers the parsing of 'throttle' attributes
        :param conf: configuration
        :param attrib: 'spf'
        :return: generated config dictionary
        """

        cfg_dict = {}
        cfg_dict[attrib] = self.parse_attrib(conf, attrib, match=attrib)
        return cfg_dict

    def parse_refresh(self, conf, attrib=None):
        """
        This function triggers the parsing of 'refresh' attributes
        :param conf: configuration
        :param attrib: 'refresh'
        :return: generated config dictionary
        """

        cfg_dict = self.parse_attr(conf, ["timers"], match=attrib)
        return cfg_dict

    def parse_leaf_list(self, conf, attrib):
        """
        This function forms the regex to fetch the listed attributes
        from the configuration data
        :param conf: configuration data
        :param attrib: attribute name
        :return: generated rule list configuration
        """

        lst = []
        items = findall(r"^" + attrib + " (?:'*)(\\S+)(?:'*)", conf, M)
        if items:
            for i in set(items):
                lst.append(i.strip("'"))
                lst.sort()
        return lst

    def parse_distance(self, conf, attrib=None):
        """
        This function triggers the parsing of 'distance' attributes
        :param conf: configuration
        :param attrib: attribute name
        :return: generated config dictionary
        """

        cfg_dict = self.parse_attr(conf, ["global"], match=attrib)
        cfg_dict["ospf"] = self.parse_ospf(conf, "ospf")
        return cfg_dict

    def parse_ospf(self, conf, attrib=None):
        """
        This function triggers the parsing of 'distance ospf' attributes
        :param conf: configuration
        :param attrib: 'ospf'
        :return: generated config dictionary
        """

        cfg_dict = self.parse_attrib(conf, "ospf", match=attrib)
        return cfg_dict

    def parse_max_metric(self, conf):
        """
        This function triggers the parsing of 'max_metric' attributes
        :param conf: configuration
        :return: generated config dictionary
        """

        cfg_dict = {}
        cfg_dict["router_lsa"] = self.parse_attrib(
            conf, "router_lsa", match="router-lsa"
        )
        return cfg_dict

    def parse_auto_cost(self, conf, attrib=None):
        """
        This function triggers the parsing of 'auto_cost' attributes
        :param conf: configuration
        :param attrib: attribute name
        :return: generated config dictionary
        """

        cfg_dict = self.parse_attr(conf, ["reference_bandwidth"], match=attrib)
        return cfg_dict

    def parse_def_info(self, conf):
        """
        This function triggers the parsing of 'default_information' attributes
        :param conf: configuration
        :return: generated config dictionary
        """

        cfg_dict = {}
        cfg_dict["originate"] = self.parse_attrib(
            conf, "originate", "originate"
        )
        return cfg_dict

    def parse_area(self, conf, area_id):
        """
        This function triggers the parsing of 'area' attributes.
        :param conf: configuration data
        :param area_id: area identity
        :return: generated rule configuration dictionary.
        """

        rule = self.parse_attrib(conf, "area_id", match=area_id)
        r_sub = {
            "area_type": self.parse_area_type(conf, "area-type"),
            "network": self.parse_network(conf),
            "range": self.parse_attrib_list(conf, "range", "address"),
            "virtual_link": self.parse_attrib_list(
                conf, "virtual-link", "address"
            ),
        }
        rule.update(r_sub)
        return rule

    def parse_key(self, conf, key_id):
        """
        This function triggers the parsing of 'area' attributes.
        :param conf: configuration data
        :param area_id: area identity
        :return: generated rule configuration dictionary.
        """

        rule = self.parse_attrib(conf, "key_id", match=key_id)
        return rule

    def parse_area_type(self, conf, attrib=None):
        """
        This function triggers the parsing of 'area_type' attributes
        :param conf: configuration
        :param attrib: 'area-type'
        :return: generated config dictionary
        """

        cfg_dict = self.parse_attr(conf, ["normal"], match=attrib)
        cfg_dict["nssa"] = self.parse_attrib(conf, "nssa", match="nssa")
        cfg_dict["stub"] = self.parse_attrib(conf, "stub", match="stub")
        return cfg_dict

    def parse_network(self, conf):
        """
        This function forms the regex to fetch the 'network'
        :param conf: configuration data
        :return: generated rule list configuration
        """

        a_lst = []
        applications = findall(r"network (.+)", conf, M)
        if applications:
            app_lst = []
            for r in set(applications):
                obj = {"address": r.strip("'")}
                app_lst.append(obj)
            a_lst = sorted(app_lst, key=lambda i: i["address"])
        return a_lst

    def parse_vlink(self, conf):
        """
        This function triggers the parsing of 'virtual_link' attributes
        :param conf: configuration data
        :return: generated rule configuration dictionary
        """

        rule = self.parse_attrib(conf, "vlink")
        r_sub = {
            "authentication": self.parse_authentication(conf, "authentication")
        }
        rule.update(r_sub)
        return rule

    def parse_authentication(self, conf, attrib=None):
        """
        This function triggers the parsing of 'authentication' attributes.
        :param conf: configuration
        :param attrib: 'authentication'
        :return: generated config dictionary
        """

        cfg_dict = self.parse_attr(conf, ["plaintext_password"], match=attrib)
        cfg_dict["md5"] = self.parse_attrib_list(conf, "key-id", "key_id")
        return cfg_dict

    def parse_attrib_list(self, conf, attrib, param):
        """
        This function forms the regex to fetch the listed attributes
        from config
        :param conf: configuration data
        :param attrib: attribute name
        :param param: parameter data
        :return: generated rule list configuration
        """

        r_lst = []
        if attrib == "area":
            items = findall(
                r"^" + attrib.replace("_", "-") + " (?:'*)(\\S+)(?:'*)",
                conf,
                M,
            )
        elif attrib == "key-id":
            items = findall(
                r"^.*" + attrib.replace("_", "-") + " (?:'*)(\\S+)(?:'*)",
                conf,
                M,
            )
        else:
            items = findall(r"" + attrib + " (?:'*)(\\S+)(?:'*)", conf, M)
        if items:
            a_lst = []
            for item in set(items):
                i_regex = r" %s .+$" % item
                cfg = "\n".join(findall(i_regex, conf, M))
                if attrib == "area":
                    obj = self.parse_area(cfg, item)
                elif attrib == "virtual-link":
                    obj = self.parse_vlink(cfg)
                elif attrib == "key-id":
                    obj = self.parse_key(cfg, item)
                else:
                    obj = self.parse_attrib(cfg, attrib)
                obj[param] = item.strip("'")
                if obj:
                    a_lst.append(obj)
            r_lst = sorted(a_lst, key=lambda i: i[param])
        return r_lst

    def parse_attrib(self, conf, param, match=None):
        """
        This function triggers the parsing of 'ospf' attributes
        :param conf: configuration data
        :return: generated configuration dictionary
        """

        param_lst = {
            "key_id": ["md5_key"],
            "mpls_te": ["enabled", "router_address"],
            "area_id": ["shortcut", "authentication"],
            "neighbor": ["priority", "poll_interval"],
            "stub": ["set", "default_cost", "no_summary"],
            "range": ["cost", "substitute", "not_advertise"],
            "ospf": ["external", "inter_area", "intra_area"],
            "spf": ["delay", "max_holdtime", "initial_holdtime"],
            "redistribute": ["metric", "metric_type", "route_map"],
            "nssa": ["set", "translate", "default_cost", "no_summary"],
            "config_routes": ["default_metric", "log_adjacency_changes"],
            "originate": ["always", "metric", "metric_type", "route_map"],
            "router_lsa": ["administrative", "on_shutdown", "on_startup"],
            "parameters": [
                "abr_type",
                "opaque_lsa",
                "router_id",
                "rfc1583_compatibility",
            ],
            "vlink": [
                "dead_interval",
                "hello_interval",
                "transmit_delay",
                "retransmit_interval",
            ],
        }
        cfg_dict = self.parse_attr(conf, param_lst[param], match)
        return cfg_dict

    def parse_attr(self, conf, attr_list, match=None):
        """
        This function peforms the following:
        - Form the regex to fetch the required attribute config.
        - Type cast the output in desired format.
        :param conf: configuration.
        :param attr_list: list of attributes.
        :param match: parent node/attribute name.
        :return: generated config dictionary.
        """

        config = {}
        for attrib in attr_list:
            regex = self.map_regex(attrib)

            if match:
                regex = match.replace("_", "-") + " " + regex
            if conf:
                if self.is_bool(attrib):
                    out = conf.find(attrib.replace("_", "-"))
                    dis = conf.find(attrib.replace("_", "-") + " 'disable'")
                    if match:
                        if attrib == "set" and conf.find(match) >= 1:
                            config[attrib] = True
                        en = conf.find(match + " 'enable'")
                    if out >= 1:
                        if dis >= 1:
                            config[attrib] = False
                        else:
                            config[attrib] = True
                    elif match and en >= 1:
                        config[attrib] = True
                else:
                    out = search(r"^.*" + regex + " (.+)", conf, M)
                    if out:
                        val = out.group(1).strip("'")
                        if self.is_num(attrib):
                            val = int(val)
                        config[attrib] = val
        return config

    def map_regex(self, attrib):
        """
        - This function construct the regex string.
        - replace the underscore with hyphen.
        :param attrib: attribute
        :return: regex string
        """

        return (
            "disable"
            if attrib == "disabled"
            else (
                "enable"
                if attrib == "enabled"
                else (
                    "area" if attrib == "area_id" else attrib.replace("_", "-")
                )
            )
        )

    def is_bool(self, attrib):
        """
        This function looks for the attribute in predefined bool type set.
        :param attrib: attribute.
        :return: True/False
        """

        bool_set = (
            "set",
            "always",
            "normal",
            "enabled",
            "opaque_lsa",
            "not_advertise",
            "administrative",
            "rfc1583_compatibility",
        )
        return True if attrib in bool_set else False

    def is_num(self, attrib):
        """
        This function looks for the attribute in predefined integer type set.
        :param attrib: attribute.
        :return: True/false.
        """

        num_set = (
            "ospf",
            "delay",
            "metric",
            "inter_area",
            "intra_area",
            "on_startup",
            "metric_type",
            "on_shutdown",
            "max_holdtime",
            "poll_interval",
            "default_metric",
            "initial_holdtime",
            "key_id",
        )
        return True if attrib in num_set else False
