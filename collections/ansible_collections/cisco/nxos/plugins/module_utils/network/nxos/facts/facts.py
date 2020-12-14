#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
"""
The facts class for nxos
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.legacy.base import (
    Default,
    Legacy,
    Hardware,
    Config,
    Interfaces,
    Features,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.bfd_interfaces.bfd_interfaces import (
    Bfd_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.interfaces.interfaces import (
    InterfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces import (
    L2_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.lacp.lacp import (
    LacpFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l3_interfaces.l3_interfaces import (
    L3_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.lag_interfaces.lag_interfaces import (
    Lag_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.telemetry.telemetry import (
    TelemetryFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vlans.vlans import (
    VlansFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.lacp_interfaces.lacp_interfaces import (
    Lacp_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.lldp_global.lldp_global import (
    Lldp_globalFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.lldp_interfaces.lldp_interfaces import (
    Lldp_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.acl_interfaces.acl_interfaces import (
    Acl_interfacesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.acls.acls import (
    AclsFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.static_routes.static_routes import (
    Static_routesFacts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospfv2.ospfv2 import (
    Ospfv2Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospfv3.ospfv3 import (
    Ospfv3Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospf_interfaces.ospf_interfaces import (
    Ospf_interfacesFacts,
)


FACT_LEGACY_SUBSETS = dict(
    default=Default,
    legacy=Legacy,
    hardware=Hardware,
    interfaces=Interfaces,
    config=Config,
    features=Features,
)
FACT_RESOURCE_SUBSETS = dict(
    bfd_interfaces=Bfd_interfacesFacts,
    hsrp_interfaces=Hsrp_interfacesFacts,
    lag_interfaces=Lag_interfacesFacts,
    lldp_global=Lldp_globalFacts,
    telemetry=TelemetryFacts,
    vlans=VlansFacts,
    lacp=LacpFacts,
    lacp_interfaces=Lacp_interfacesFacts,
    interfaces=InterfacesFacts,
    l3_interfaces=L3_interfacesFacts,
    l2_interfaces=L2_interfacesFacts,
    lldp_interfaces=Lldp_interfacesFacts,
    acl_interfaces=Acl_interfacesFacts,
    acls=AclsFacts,
    static_routes=Static_routesFacts,
    ospfv2=Ospfv2Facts,
    ospfv3=Ospfv3Facts,
    ospf_interfaces=Ospf_interfacesFacts,
)


class Facts(FactsBase):
    """ The fact class for nxos
    """

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(
        self, legacy_facts_type=None, resource_facts_type=None, data=None
    ):
        """ Collect the facts for nxos
        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        if self.VALID_RESOURCE_SUBSETS:
            self.get_network_resources_facts(
                FACT_RESOURCE_SUBSETS, resource_facts_type, data
            )

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(
                FACT_LEGACY_SUBSETS, legacy_facts_type
            )

        return self.ansible_facts, self._warnings
