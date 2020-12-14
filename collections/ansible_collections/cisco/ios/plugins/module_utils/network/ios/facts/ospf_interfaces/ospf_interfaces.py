# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios ospf_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospf_interfaces import (
    Ospf_InterfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ospf_interfaces.ospf_interfaces import (
    Ospf_InterfacesArgs,
)


class Ospf_InterfacesFacts(object):
    """ The cisco.ios ospf_interfaces facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospf_InterfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_ospf_interfaces_data(self, connection):
        return connection.get("sh running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Ospf_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_ospf_interfaces_data(connection)

        # parse native config using the Ospf_interfaces template
        ospf_interfaces_parser = Ospf_InterfacesTemplate(
            lines=data.splitlines()
        )

        objs = ospf_interfaces_parser.parse()
        final_objs = []
        for key, value in iteritems(objs):
            temp_af = []
            if value["address_family"].get("ip"):
                temp_af.append(value["address_family"].get("ip"))
            if value["address_family"].get("ipv6"):
                temp_af.append(value["address_family"].get("ipv6"))
            if temp_af:
                value["address_family"] = temp_af
            if value:
                value = utils.remove_empties(value)
                final_objs.append(value)
        ansible_facts["ansible_network_resources"].pop("ospf_interfaces", None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": final_objs})
        )

        facts["ospf_interfaces"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
