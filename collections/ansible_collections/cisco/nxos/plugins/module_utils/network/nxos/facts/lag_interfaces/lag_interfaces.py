#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)#!/usr/bin/python
"""
The nxos lag_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.lag_interfaces.lag_interfaces import (
    Lag_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    get_interface_type,
    normalize_interface,
)


class Lag_interfacesFacts(object):
    """ The nxos lag_interfaces fact class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Lag_interfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for lag_interfaces
        :param connection: the device connection
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        objs = []
        if not data:
            data = connection.get("show running-config | section ^interface")

        objs = self.render_config(self.generated_spec, data, connection)

        ansible_facts["ansible_network_resources"].pop("lag_interfaces", None)
        facts = {}
        if objs:
            facts["lag_interfaces"] = []
            params = utils.validate_config(
                self.argument_spec, {"config": objs}
            )
            for cfg in params["config"]:
                facts["lag_interfaces"].append(utils.remove_empties(cfg))

        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def render_config(self, spec, conf, connection):
        """
        Render config as dictionary structure and delete keys
          from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        result = []
        match = re.findall(r"interface (port-channel\d+)", conf)

        for item in match:
            result.append({"name": item, "members": []})

        for intf in conf.split("interface "):
            member = {}
            match_intf = re.search(r"(port-channel|Ethernet)(\S+)", intf)
            if match_intf:
                member["member"] = match_intf.group(0)

            match_line = re.search(
                r"channel-group\s(?P<port_channel>\d+)(\smode\s(?P<mode>on|active|passive))?",
                intf,
            )
            if match_line:
                member.update(match_line.groupdict())

            if member and member.get("port_channel", None):
                port_channel = "port-channel{0}".format(
                    member.pop("port_channel")
                )
                for x in result:
                    if x["name"] == port_channel:
                        x["members"].append(utils.remove_empties(member))

        return result
