# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The eos ospfv3 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re
from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.rm_templates.ospfv3 import (
    Ospfv3Template,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.argspec.ospfv3.ospfv3 import (
    Ospfv3Args,
)


class Ospfv3Facts(object):
    """ The eos ospfv3 facts class
    """

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

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section ospfv3")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Ospfv3 network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_config(connection)

        # split the config into instances of the resource
        resource_delim = "router ospfv3"
        find_pattern = r"(?:^|\n)%s.*?(?=(?:^|\n)%s|$)" % (
            resource_delim,
            resource_delim,
        )
        resources = [
            p.strip() for p in re.findall(find_pattern, data, re.DOTALL)
        ]

        # parse native config using the Ospfv3 template
        ospfv3_facts = {"processes": []}

        for resource in resources:
            ospfv3_parser = Ospfv3Template(lines=resource.splitlines())
            objs = ospfv3_parser.parse()

            for key, sortv in [("address_family", "afi")]:
                if key in objs["processes"] and objs["processes"][key]:
                    objs["processes"][key] = list(
                        objs["processes"][key].values()
                    )

            for addr_family in objs["processes"]["address_family"]:
                if "areas" in addr_family:
                    addr_family["areas"] = list(addr_family["areas"].values())

            for addr_family in objs["processes"]["address_family"]:
                if not addr_family.get("afi"):
                    # global vars
                    objs["processes"].update(addr_family)
                    objs["processes"]["address_family"].remove(addr_family)

            ospfv3_facts["processes"].append(objs["processes"])

        ansible_facts["ansible_network_resources"].pop("ospfv3", None)
        params = utils.validate_config(
            self.argument_spec, {"config": ospfv3_facts}
        )
        params = utils.remove_empties(params)

        facts["ospfv3"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
