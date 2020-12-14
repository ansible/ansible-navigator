#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_bgp
author: Nilashish Chakraborty (@NilashishC)
short_description: Configure global BGP protocol settings on Cisco IOS.
description:
- This module provides configuration management of global BGP parameters on devices
  running Cisco IOS
version_added: 1.0.0
notes:
- Tested against Cisco IOS Version 15.6(3)M2
options:
  config:
    description:
    - Specifies the BGP related configuration.
    type: dict
    suboptions:
      bgp_as:
        description:
        - Specifies the BGP Autonomous System (AS) number to configure on the device.
        type: int
        required: true
      router_id:
        description:
        - Configures the BGP routing process router-id value.
        type: str
        default:
      log_neighbor_changes:
        description:
        - Enable/disable logging neighbor up/down and reset reason.
        type: bool
      neighbors:
        description:
        - Specifies BGP neighbor related configurations.
        type: list
        elements: dict
        suboptions:
          neighbor:
            description:
            - Neighbor router address.
            required: true
            type: str
          remote_as:
            description:
            - Remote AS of the BGP neighbor to configure.
            type: int
            required: true
          update_source:
            description:
            - Source of the routing updates.
            type: str
          password:
            description:
            - Password to authenticate the BGP peer connection.
            type: str
          enabled:
            description:
            - Administratively shutdown or enable a neighbor.
            type: bool
          description:
            description:
            - Neighbor specific description.
            type: str
          ebgp_multihop:
            description:
            - Specifies the maximum hop count for EBGP neighbors not on directly connected
              networks.
            - The range is from 1 to 255.
            type: int
          peer_group:
            description:
            - Name of the peer group that the neighbor is a member of.
            type: str
          timers:
            description:
            - Specifies BGP neighbor timer related configurations.
            type: dict
            suboptions:
              keepalive:
                description:
                - Frequency (in seconds) with which the device sends keepalive messages
                  to its peer.
                - The range is from 0 to 65535.
                type: int
                required: true
              holdtime:
                description:
                - Interval (in seconds) after not receiving a keepalive message that
                  IOS declares a peer dead.
                - The range is from 0 to 65535.
                type: int
                required: true
              min_neighbor_holdtime:
                description:
                - Interval (in seconds) specifying the minimum acceptable hold-time
                  from a BGP neighbor.
                - The minimum acceptable hold-time must be less than, or equal to,
                  the interval specified in the holdtime argument.
                - The range is from 0 to 65535.
                type: int
          local_as:
            description:
            - The local AS number for the neighbor.
            type: int
      networks:
        description:
        - Specify Networks to announce via BGP.
        - For operation replace, this option is mutually exclusive with networks option
          under address_family.
        - For operation replace, if the device already has an address family activated,
          this option is not allowed.
        type: list
        elements: dict
        suboptions:
          prefix:
            description:
            - Network ID to announce via BGP.
            required: true
            type: str
          masklen:
            description:
            - Subnet mask length for the Network to announce(e.g, 8, 16, 24, etc.).
            type: int
          route_map:
            description:
            - Route map to modify the attributes.
            type: str
      address_family:
        description:
        - Specifies BGP address family related configurations.
        type: list
        elements: dict
        suboptions:
          afi:
            description:
            - Type of address family to configure.
            choices:
            - ipv4
            - ipv6
            required: true
            type: str
          safi:
            description:
            - Specifies the type of cast for the address family.
            choices:
            - flowspec
            - unicast
            - multicast
            - labeled-unicast
            default: unicast
            type: str
          synchronization:
            description:
            - Enable/disable IGP synchronization.
            type: bool
          auto_summary:
            description:
            - Enable/disable automatic network number summarization.
            type: bool
          redistribute:
            description:
            - Specifies the redistribute information from another routing protocol.
            type: list
            elements: dict
            suboptions:
              protocol:
                description:
                - Specifies the protocol for configuring redistribute information.
                choices:
                - ospf
                - ospfv3
                - eigrp
                - isis
                - static
                - connected
                - odr
                - lisp
                - mobile
                - rip
                required: true
                type: str
              id:
                description:
                - Identifier for the routing protocol for configuring redistribute
                  information.
                - Valid for protocols 'ospf', 'ospfv3' and 'eigrp'.
                type: str
              metric:
                description:
                - Specifies the metric for redistributed routes.
                type: int
              route_map:
                description:
                - Specifies the route map reference.
                type: str
          networks:
            description:
            - Specify Networks to announce via BGP.
            - For operation replace, this option is mutually exclusive with root level
              networks option.
            type: list
            elements: dict
            suboptions:
              prefix:
                description:
                - Network ID to announce via BGP.
                required: true
                type: str
              masklen:
                description:
                - Subnet mask length for the Network to announce(e.g, 8, 16, 24, etc.).
                type: int
              route_map:
                description:
                - Route map to modify the attributes.
                type: str
          neighbors:
            description:
            - Specifies BGP neighbor related configurations in Address Family configuration
              mode.
            type: list
            elements: dict
            suboptions:
              neighbor:
                description:
                - Neighbor router address.
                required: true
                type: str
              advertisement_interval:
                description:
                - Minimum interval between sending BGP routing updates for this neighbor.
                type: int
              route_reflector_client:
                description:
                - Specify a neighbor as a route reflector client.
                type: bool
              route_server_client:
                description:
                - Specify a neighbor as a route server client.
                type: bool
              activate:
                description:
                - Enable the Address Family for this Neighbor.
                type: bool
              remove_private_as:
                description:
                - Remove the private AS number from outbound updates.
                type: bool
              next_hop_self:
                description:
                - Enable/disable the next hop calculation for this neighbor.
                type: bool
              next_hop_unchanged:
                description:
                - Propagate next hop unchanged for iBGP paths to this neighbor.
                type: bool
              maximum_prefix:
                description:
                - Maximum number of prefixes to accept from this peer.
                - The range is from 1 to 2147483647.
                type: int
              prefix_list_in:
                description:
                - Name of ip prefix-list to apply to incoming prefixes.
                type: str
              prefix_list_out:
                description:
                - Name of ip prefix-list to apply to outgoing prefixes.
                type: str
  operation:
    description:
    - Specifies the operation to be performed on the BGP process configured on the
      device.
    - In case of merge, the input configuration will be merged with the existing BGP
      configuration on the device.
    - In case of replace, if there is a diff between the existing configuration and
      the input configuration, the existing configuration will be replaced by the
      input configuration for every option that has the diff.
    - In case of override, all the existing BGP configuration will be removed from
      the device and replaced with the input configuration.
    - In case of delete the existing BGP configuration will be removed from the device.
    default: merge
    type: str
    choices:
    - merge
    - replace
    - override
    - delete
"""
EXAMPLES = """
- name: configure global bgp as 64496
  cisco.ios.ios_bgp:
    config:
      bgp_as: 64496
      router_id: 192.0.2.1
      log_neighbor_changes: true
      neighbors:
      - neighbor: 203.0.113.5
        remote_as: 64511
        timers:
          keepalive: 300
          holdtime: 360
          min_neighbor_holdtime: 360
      - neighbor: 198.51.100.2
        remote_as: 64498
      networks:
      - prefix: 198.51.100.0
        route_map: RMAP_1
      - prefix: 192.0.2.0
        masklen: 23
      address_family:
      - afi: ipv4
        safi: unicast
        redistribute:
        - protocol: ospf
          id: 223
          metric: 10
    operation: merge

- name: Configure BGP neighbors
  cisco.ios.ios_bgp:
    config:
      bgp_as: 64496
      neighbors:
      - neighbor: 192.0.2.10
        remote_as: 64496
        password: ansible
        description: IBGP_NBR_1
        ebgp_multihop: 100
        timers:
          keepalive: 300
          holdtime: 360
          min_neighbor_holdtime: 360
      - neighbor: 192.0.2.15
        remote_as: 64496
        description: IBGP_NBR_2
        ebgp_multihop: 150
    operation: merge

- name: Configure root-level networks for BGP
  cisco.ios.ios_bgp:
    config:
      bgp_as: 64496
      networks:
      - prefix: 203.0.113.0
        masklen: 27
        route_map: RMAP_1
      - prefix: 203.0.113.32
        masklen: 27
        route_map: RMAP_2
    operation: merge

- name: Configure BGP neighbors under address family mode
  cisco.ios.ios_bgp:
    config:
      bgp_as: 64496
      address_family:
      - afi: ipv4
        safi: unicast
        neighbors:
        - neighbor: 203.0.113.10
          activate: yes
          maximum_prefix: 250
          advertisement_interval: 120
        - neighbor: 192.0.2.15
          activate: yes
          route_reflector_client: true
    operation: merge

- name: remove bgp as 64496 from config
  cisco.ios.ios_bgp:
    config:
      bgp_as: 64496
    operation: delete
"""
RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - router bgp 64496
    - bgp router-id 192.0.2.1
    - bgp log-neighbor-changes
    - neighbor 203.0.113.5 remote-as 64511
    - neighbor 203.0.113.5 timers 300 360 360
    - neighbor 198.51.100.2 remote-as 64498
    - network 198.51.100.0 route-map RMAP_1
    - network 192.0.2.0 mask 255.255.254.0
    - address-family ipv4
    - redistribute ospf 223 metric 70
    - exit-address-family
"""
from ansible.module_utils._text import to_text
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.module import (
    NetworkModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.cli.config.bgp.process import (
    REDISTRIBUTE_PROTOCOLS,
)


def main():
    """ main entry point for module execution
    """
    network_spec = {
        "prefix": dict(required=True),
        "masklen": dict(type="int"),
        "route_map": dict(),
    }
    redistribute_spec = {
        "protocol": dict(choices=REDISTRIBUTE_PROTOCOLS, required=True),
        "id": dict(),
        "metric": dict(type="int"),
        "route_map": dict(),
    }
    timer_spec = {
        "keepalive": dict(type="int", required=True),
        "holdtime": dict(type="int", required=True),
        "min_neighbor_holdtime": dict(type="int"),
    }
    neighbor_spec = {
        "neighbor": dict(required=True),
        "remote_as": dict(type="int", required=True),
        "local_as": dict(type="int"),
        "update_source": dict(),
        "password": dict(no_log=True),
        "enabled": dict(type="bool"),
        "description": dict(),
        "ebgp_multihop": dict(type="int"),
        "timers": dict(type="dict", options=timer_spec),
        "peer_group": dict(),
    }
    af_neighbor_spec = {
        "neighbor": dict(required=True),
        "activate": dict(type="bool"),
        "advertisement_interval": dict(type="int"),
        "remove_private_as": dict(type="bool"),
        "next_hop_self": dict(type="bool"),
        "next_hop_unchanged": dict(type="bool"),
        "route_reflector_client": dict(type="bool"),
        "route_server_client": dict(type="bool"),
        "maximum_prefix": dict(type="int"),
        "prefix_list_in": dict(),
        "prefix_list_out": dict(),
    }
    address_family_spec = {
        "afi": dict(choices=["ipv4", "ipv6"], required=True),
        "safi": dict(
            choices=["flowspec", "labeled-unicast", "multicast", "unicast"],
            default="unicast",
        ),
        "auto_summary": dict(type="bool"),
        "synchronization": dict(type="bool"),
        "networks": dict(type="list", elements="dict", options=network_spec),
        "redistribute": dict(
            type="list", elements="dict", options=redistribute_spec
        ),
        "neighbors": dict(
            type="list", elements="dict", options=af_neighbor_spec
        ),
    }
    config_spec = {
        "bgp_as": dict(type="int", required=True),
        "router_id": dict(),
        "log_neighbor_changes": dict(type="bool"),
        "neighbors": dict(type="list", elements="dict", options=neighbor_spec),
        "address_family": dict(
            type="list", elements="dict", options=address_family_spec
        ),
        "networks": dict(type="list", elements="dict", options=network_spec),
    }
    argument_spec = {
        "config": dict(type="dict", options=config_spec),
        "operation": dict(
            default="merge", choices=["merge", "replace", "override", "delete"]
        ),
    }
    module = NetworkModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    try:
        result = module.edit_config(config_filter="| section ^router bgp")
    except Exception as exc:
        module.fail_json(msg=to_text(exc))
    module.exit_json(**result)


if __name__ == "__main__":
    main()
