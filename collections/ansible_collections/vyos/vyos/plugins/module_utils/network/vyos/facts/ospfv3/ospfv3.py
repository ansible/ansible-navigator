#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The vyos ospfv3 fact class
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
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.ospfv3.ospfv3 import (
    Ospfv3Args,
)


class Ospfv3Facts(object):
    """The vyos ospfv3 fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospfv3Args.argument_spec
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
        """Populate the facts for ospfv3
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
        ospfv3 = findall(r"^set protocols ospfv3 (.+)", data, M)
        if ospfv3:
            objs = self.render_config(ospfv3)
        facts = {}
        params = utils.validate_config(self.argument_spec, {"config": objs})
        facts["ospfv3"] = utils.remove_empties(params["config"])
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def render_config(self, conf):
        """
        Render config as dictionary structure

        :param conf: The configuration
        :returns: The generated config
        """
        conf = "\n".join(filter(lambda x: x, conf))
        config = {}
        config["parameters"] = self.parse_attrib(
            conf, "parameters", "parameters"
        )
        config["areas"] = self.parse_attrib_list(conf, "area", "area_id")
        config["redistribute"] = self.parse_attrib_list(
            conf, "redistribute", "route_type"
        )
        return config

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
            items = findall(r"^" + attrib + " (?:'*)(\\S+)(?:'*)", conf, M)
        else:
            items = findall(r"" + attrib + " (?:'*)(\\S+)(?:'*)", conf, M)
        if items:
            a_lst = []
            for item in set(items):
                i_regex = r" %s .+$" % item
                cfg = "\n".join(findall(i_regex, conf, M))
                if attrib == "area":
                    obj = self.parse_area(cfg, item)
                else:
                    obj = self.parse_attrib(cfg, attrib)
                obj[param] = item.strip("'")
                if obj:
                    a_lst.append(obj)
            r_lst = sorted(a_lst, key=lambda i: i[param])
        return r_lst

    def parse_area(self, conf, area_id):
        """
        This function triggers the parsing of 'area' attributes.
        :param conf: configuration data
        :param area_id: area identity
        :return: generated rule configuration dictionary.
        """

        rule = self.parse_attrib(conf, "area_id", match=area_id)
        r_sub = {"range": self.parse_attrib_list(conf, "range", "address")}
        rule.update(r_sub)
        return rule

    def parse_attrib(self, conf, param, match=None):
        """
        This function triggers the parsing of 'ospf' attributes
        :param conf: configuration data
        :return: generated configuration dictionary
        """
        param_lst = {
            "area_id": ["export_list", "import_list"],
            "redistribute": ["route_map"],
            "range": ["advertise", "not_advertise"],
            "parameters": ["router_id"],
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
            else "enable"
            if attrib == "enabled"
            else attrib.replace("_", "-")
        )

    def is_bool(self, attrib):
        """
        This function looks for the attribute in predefined bool type set.
        :param attrib: attribute.
        :return: True/False
        """
        bool_set = ("enabled", "advertise", "not_advertise")
        return True if attrib in bool_set else False

    def is_num(self, attrib):
        """
        This function looks for the attribute in predefined integer type set.
        :param attrib: attribute.
        :return: True/false.
        """
        num_set = "ospf"
        return True if attrib in num_set else False
