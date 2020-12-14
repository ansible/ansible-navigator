# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios ospfv3 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from copy import deepcopy
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ospfv3.ospfv3 import (
    Ospfv3Args,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospfv3 import (
    Ospfv3Template,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


class Ospfv3Facts(object):
    """ The ios ospfv3 fact class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospfv3Args.argument_spec

    def get_ospfv3_data(self, connection):
        return connection.get("sh running-config | section ^router ospfv3")

    def parse(self, net_template_obj):
        """ Overrided network template parse
        """
        result = {}
        shared = {}
        temp_pid = None
        for line in net_template_obj._lines:
            for parser in net_template_obj._tmplt.PARSERS:
                cap = re.match(parser["getval"], line)
                if cap:
                    capdict = cap.groupdict()

                    capdict = {
                        k: v for k, v in iteritems(capdict) if v is not None
                    }
                    if "address-family" in line:
                        capdict.update({"id": temp_pid})
                    if (
                        "manet" in line
                        and "pid" not in shared
                        and shared.get("unicast")
                    ):
                        del shared["unicast"]

                    if "router ospfv3" in line:
                        temp_pid = None
                    if parser.get("shared"):
                        shared = capdict
                    if not temp_pid and (
                        shared.get("pid") or shared.get("id")
                    ):
                        temp_pid = shared.get("pid") or shared.get("id")
                    vals = utils.dict_merge(capdict, shared)
                    try:
                        res = net_template_obj._deepformat(
                            deepcopy(parser["result"]), vals
                        )
                    except Exception:
                        continue
                    result = utils.dict_merge(result, res)
                    break
        return result

    def parse_for_address_family(self, current):
        """ Parsing and Fishing out address family contents
        """
        pid_addr_family_dict = {}
        temp_dict = {}
        temp_pid = None
        temp = []
        if current.get("address_family"):
            for each in current.pop("address_family"):
                each = utils.remove_empties(each)
                if each.get("exit"):
                    if temp_pid == each.get("exit")["pid"]:
                        temp.append(temp_dict)
                        pid_addr_family_dict[temp_pid] = temp
                        temp_dict = dict()
                    else:
                        temp_pid = each.get("exit")["pid"]
                        pid_addr_family_dict[temp_pid] = [temp_dict]
                        temp = []
                        temp.append(temp_dict)
                        temp_dict = dict()
                elif each.get("manet") and temp_dict.get("manet"):
                    for k, v in iteritems(each.get("manet")):
                        if k in temp_dict.get("manet"):
                            temp_dict.get("manet")[k].update(v)
                        else:
                            temp_dict["manet"].update(each.get("manet"))
                elif each.get("manet") and not temp_dict.get("manet"):
                    temp_dict["manet"] = each.get("manet")
                else:
                    temp_dict.update(each)
        return pid_addr_family_dict

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for ospfv3
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_ospfv3_data(connection)

        ipv4 = {"processes": []}
        rmmod = NetworkTemplate(
            lines=data.splitlines(), tmplt=Ospfv3Template()
        )
        current = self.parse(rmmod)
        address_family = self.parse_for_address_family(current)
        if address_family:
            for k, v in iteritems(current["processes"]):
                temp = address_family.pop(k)
                v.update({"address_family": temp})
        # convert some of the dicts to lists
        for key, sortv in [("processes", "process_id")]:
            if key in current and current[key]:
                current[key] = current[key].values()
                current[key] = sorted(
                    current[key], key=lambda k, sk=sortv: k[sk]
                )

        for process in current.get("processes", []):
            if "areas" in process:
                process["areas"] = list(process["areas"].values())
                process["areas"] = sorted(
                    process["areas"], key=lambda k, sk="area_id": k[sk]
                )
                for area in process["areas"]:
                    if "filters" in area:
                        area["filters"].sort()
            if "address_family" in process:
                for each in process["address_family"]:
                    if "areas" in each:
                        each["areas"] = list(each["areas"].values())
                        each["areas"] = sorted(
                            each["areas"], key=lambda k, sk="area_id": k[sk]
                        )
                        for area in each["areas"]:
                            if "filters" in area:
                                area["filters"].sort()
            ipv4["processes"].append(process)

        ansible_facts["ansible_network_resources"].pop("ospfv3", None)
        facts = {}
        if current:
            params = utils.validate_config(
                self.argument_spec, {"config": ipv4}
            )
            params = utils.remove_empties(params)

            facts["ospfv3"] = params["config"]

            ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
