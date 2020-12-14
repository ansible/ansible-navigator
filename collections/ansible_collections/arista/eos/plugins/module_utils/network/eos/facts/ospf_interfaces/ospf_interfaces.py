# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The eos ospf_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.rm_templates.ospf_interfaces import (
    Ospf_interfacesTemplate,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.argspec.ospf_interfaces.ospf_interfaces import (
    Ospf_interfacesArgs,
)


class Ospf_interfacesFacts(object):
    """ The eos ospf_interfaces facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospf_interfacesArgs.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section interface ")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Ospf_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        resource_delim = "interface"
        find_pattern = r"(?:^|\n)%s.*?(?=(?:^|\n)%s|$)" % (
            resource_delim,
            resource_delim,
        )
        resources = [
            p.strip() for p in re.findall(find_pattern, data, re.DOTALL)
        ]
        # parse native config using the Ospf_interfaces template
        ospf_interfaces_facts = []
        for resource in resources:
            ospf_interfaces_parser = Ospf_interfacesTemplate(
                lines=resource.splitlines()
            )
            entry = ospf_interfaces_parser.parse()
            if entry:
                if "address_family" in entry and entry["address_family"]:
                    entry["address_family"] = sorted(
                        list(entry["address_family"].values()),
                        key=lambda k, sk="afi": k[sk],
                    )
            if entry:
                if entry.get("address_family"):
                    for addr in entry["address_family"]:
                        if "ip_params" in addr:
                            addr["ip_params"] = sorted(
                                list(addr["ip_params"].values()),
                                key=lambda k, sk="afi": k[sk],
                            )
            ospf_interfaces_facts.append(entry)

        ansible_facts["ansible_network_resources"].pop("ospf_interfaces", None)
        facts = {"ospf_interfaces": []}
        params = utils.remove_empties(
            utils.validate_config(
                self.argument_spec, {"config": ospf_interfaces_facts}
            )
        )

        if params.get("config"):
            for cfg in params["config"]:
                facts["ospf_interfaces"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
