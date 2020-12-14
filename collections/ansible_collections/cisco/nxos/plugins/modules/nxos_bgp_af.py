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
module: nxos_bgp_af
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Manages BGP Address-family configuration.
description:
- Manages BGP Address-family configurations on NX-OS switches.
version_added: 1.0.0
author: Gabriele Gerbino (@GGabriele)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- C(state=absent) removes the whole BGP ASN configuration
- Default, where supported, restores params default value.
options:
  asn:
    description:
    - BGP autonomous system number. Valid values are String, Integer in ASPLAIN or
      ASDOT notation.
    required: true
    type: str
  vrf:
    description:
    - Name of the VRF. The name 'default' is a valid VRF representing the global bgp.
    default: 'default'
    type: str
  afi:
    description:
    - Address Family Identifier.
    required: true
    choices:
    - ipv4
    - ipv6
    - vpnv4
    - vpnv6
    - l2vpn
    type: str
  safi:
    description:
    - Sub Address Family Identifier.
    required: true
    choices:
    - unicast
    - multicast
    - evpn
    type: str
  additional_paths_install:
    description:
    - Install a backup path into the forwarding table and provide prefix independent
      convergence (PIC) in case of a PE-CE link failure.
    type: bool
  additional_paths_receive:
    description:
    - Enables the receive capability of additional paths for all of the neighbors
      under this address family for which the capability has not been disabled.
    type: bool
  additional_paths_selection:
    description:
    - Configures the capability of selecting additional paths for a prefix. Valid
      values are a string defining the name of the route-map.
    type: str
  additional_paths_send:
    description:
    - Enables the send capability of additional paths for all of the neighbors under
      this address family for which the capability has not been disabled.
    type: bool
  advertise_l2vpn_evpn:
    description:
    - Advertise evpn routes.
    type: bool
  client_to_client:
    description:
    - Configure client-to-client route reflection.
    type: bool
  dampen_igp_metric:
    description:
    - Specify dampen value for IGP metric-related changes, in seconds. Valid values
      are integer and keyword 'default'.
    type: str
  dampening_state:
    description:
    - Enable/disable route-flap dampening.
    type: bool
  dampening_half_time:
    description:
    - Specify decay half-life in minutes for route-flap dampening. Valid values are
      integer and keyword 'default'.
    type: str
  dampening_max_suppress_time:
    description:
    - Specify max suppress time for route-flap dampening stable route. Valid values
      are integer and keyword 'default'.
    type: str
  dampening_reuse_time:
    description:
    - Specify route reuse time for route-flap dampening. Valid values are integer
      and keyword 'default'.
    type: str
  dampening_routemap:
    description:
    - Specify route-map for route-flap dampening. Valid values are a string defining
      the name of the route-map.
    type: str
  dampening_suppress_time:
    description:
    - Specify route suppress time for route-flap dampening. Valid values are integer
      and keyword 'default'.
    type: str
  default_information_originate:
    description:
    - Default information originate.
    type: bool
  default_metric:
    description:
    - Sets default metrics for routes redistributed into BGP. Valid values are Integer
      or keyword 'default'
    type: str
  distance_ebgp:
    description:
    - Sets the administrative distance for eBGP routes. Valid values are Integer or
      keyword 'default'.
    type: str
  distance_ibgp:
    description:
    - Sets the administrative distance for iBGP routes. Valid values are Integer or
      keyword 'default'.
    type: str
  distance_local:
    description:
    - Sets the administrative distance for local BGP routes. Valid values are Integer
      or keyword 'default'.
    type: str
  inject_map:
    description:
    - An array of route-map names which will specify prefixes to inject. Each array
      entry must first specify the inject-map name, secondly an exist-map name, and
      optionally the copy-attributes keyword which indicates that attributes should
      be copied from the aggregate. For example [['lax_inject_map', 'lax_exist_map'],
      ['nyc_inject_map', 'nyc_exist_map', 'copy-attributes'], ['fsd_inject_map', 'fsd_exist_map']].
    type: list
    elements: list
  maximum_paths:
    description:
    - Configures the maximum number of equal-cost paths for load sharing. Valid value
      is an integer in the range 1-64.
    type: str
  maximum_paths_ibgp:
    description:
    - Configures the maximum number of ibgp equal-cost paths for load sharing. Valid
      value is an integer in the range 1-64.
    type: str
  networks:
    description:
    - Networks to configure. Valid value is a list of network prefixes to advertise.
      The list must be in the form of an array. Each entry in the array must include
      a prefix address and an optional route-map. For example [['10.0.0.0/16', 'routemap_LA'],
      ['192.168.1.1', 'Chicago'], ['192.168.2.0/24'], ['192.168.3.0/24', 'routemap_NYC']].
    type: list
    elements: list
  next_hop_route_map:
    description:
    - Configure a route-map for valid nexthops. Valid values are a string defining
      the name of the route-map.
    type: str
  redistribute:
    description:
    - A list of redistribute directives. Multiple redistribute entries are allowed.
      The list must be in the form of a nested array. the first entry of each array
      defines the source-protocol to redistribute from; the second entry defines a
      route-map name. A route-map is highly advised but may be optional on some platforms,
      in which case it may be omitted from the array list. For example [['direct',
      'rm_direct'], ['lisp', 'rm_lisp']].
    type: list
    elements: list
  suppress_inactive:
    description:
    - Advertises only active routes to peers.
    type: bool
  table_map:
    description:
    - Apply table-map to filter routes downloaded into URIB. Valid values are a string.
    type: str
  table_map_filter:
    description:
    - Filters routes rejected by the route-map and does not download them to the RIB.
    type: bool
  state:
    description:
    - Determines whether the config should be present or not on the device.
    default: present
    choices:
    - present
    - absent
    type: str
  retain_route_target:
    description:
    - Retains all of the routes or the routes which are part of configured route-map.
      Valid values are route-map names or keyword C(all) or keyword C(default).  C(all)
      retains all the routes regardless of Target-VPN community. C(default) will disable
      the retain route target option. If you are using route-map name please ensure
      that the name is not same as C(all) and C(default).
    type: str
    version_added: 1.1.0
"""
EXAMPLES = """
# configure a simple address-family
- cisco.nxos.nxos_bgp_af:
    asn: 65535
    vrf: TESTING
    afi: ipv4
    safi: unicast
    advertise_l2vpn_evpn: true
    state: present
    retain_route_target: all
"""

RETURN = """
commands:
    description: commands sent to the device
    returned: always
    type: list
    sample: ["router bgp 65535", "vrf TESTING",
            "address-family ipv4 unicast", "advertise l2vpn evpn",
            "retain route-target all"]
"""

import re

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    get_config,
    load_config,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    CustomNetworkConfig,
)


BOOL_PARAMS = [
    "additional_paths_install",
    "additional_paths_receive",
    "additional_paths_send",
    "advertise_l2vpn_evpn",
    "dampening_state",
    "default_information_originate",
    "suppress_inactive",
]
PARAM_TO_DEFAULT_KEYMAP = {
    "maximum_paths": "1",
    "maximum_paths_ibgp": "1",
    "client_to_client": True,
    "distance_ebgp": "20",
    "distance_ibgp": "200",
    "distance_local": "220",
    "dampen_igp_metric": "600",
}
PARAM_TO_COMMAND_KEYMAP = {
    "asn": "router bgp",
    "afi": "address-family",
    "safi": "address-family",
    "additional_paths_install": "additional-paths install backup",
    "additional_paths_receive": "additional-paths receive",
    "additional_paths_selection": "additional-paths selection route-map",
    "additional_paths_send": "additional-paths send",
    "advertise_l2vpn_evpn": "advertise l2vpn evpn",
    "client_to_client": "client-to-client reflection",
    "dampen_igp_metric": "dampen-igp-metric",
    "dampening_state": "dampening",
    "dampening_half_time": "dampening",
    "dampening_max_suppress_time": "dampening",
    "dampening_reuse_time": "dampening",
    "dampening_routemap": "dampening route-map",
    "dampening_suppress_time": "dampening",
    "default_information_originate": "default-information originate",
    "default_metric": "default-metric",
    "distance_ebgp": "distance",
    "distance_ibgp": "distance",
    "distance_local": "distance",
    "inject_map": "inject-map",
    "maximum_paths": "maximum-paths",
    "maximum_paths_ibgp": "maximum-paths ibgp",
    "networks": "network",
    "redistribute": "redistribute",
    "next_hop_route_map": "nexthop route-map",
    "suppress_inactive": "suppress-inactive",
    "table_map": "table-map",
    "table_map_filter": "table-map-filter",
    "vrf": "vrf",
    "retain_route_target": "retain route-target",
}
DAMPENING_PARAMS = [
    "dampening_half_time",
    "dampening_suppress_time",
    "dampening_reuse_time",
    "dampening_max_suppress_time",
]


def get_value(arg, config, module):
    command = PARAM_TO_COMMAND_KEYMAP[arg]
    command_val_re = re.compile(
        r"(?:{0}\s)(?P<value>.*)$".format(command), re.M
    )
    has_command_val = command_val_re.search(config)

    if arg in ["networks", "redistribute", "inject_map"]:
        value = []
        for ele in command_val_re.findall(config):
            tl = ele.split()
            if "exist-map" in tl:
                tl.remove("exist-map")
            elif "route-map" in tl:
                tl.remove("route-map")
            value.append(tl)

    elif command == "distance":
        distance_re = (
            r".*distance\s(?P<d_ebgp>\w+)\s(?P<d_ibgp>\w+)\s(?P<d_local>\w+)"
        )
        match_distance = re.match(distance_re, config, re.DOTALL)

        value = ""
        if match_distance:
            distance_group = match_distance.groupdict()

            if arg == "distance_ebgp":
                value = distance_group["d_ebgp"]
            elif arg == "distance_ibgp":
                value = distance_group["d_ibgp"]
            elif arg == "distance_local":
                value = distance_group["d_local"]

    elif command.split()[0] == "dampening":
        value = ""
        if arg == "dampen_igp_metric" or arg == "dampening_routemap":
            if command in config:
                value = has_command_val.group("value")
        else:
            dampening_re = r".*dampening\s(?P<half>\w+)\s(?P<reuse>\w+)\s(?P<suppress>\w+)\s(?P<max_suppress>\w+)"
            match_dampening = re.match(dampening_re, config, re.DOTALL)
            if match_dampening:
                dampening_group = match_dampening.groupdict()

                if arg == "dampening_half_time":
                    value = dampening_group["half"]
                elif arg == "dampening_reuse_time":
                    value = dampening_group["reuse"]
                elif arg == "dampening_suppress_time":
                    value = dampening_group["suppress"]
                elif arg == "dampening_max_suppress_time":
                    value = dampening_group["max_suppress"]
            else:
                if arg == "dampening_state":
                    value = True if "dampening" in config else False
    elif arg == "table_map_filter":
        tmf_regex = re.compile(r"\s+table-map.*filter$", re.M)
        value = False
        if tmf_regex.search(config):
            value = True

    elif arg == "table_map":
        tm_regex = re.compile(
            r"(?:table-map\s)(?P<value>\S+)(\sfilter)?$", re.M
        )
        has_tablemap = tm_regex.search(config)
        value = ""
        if has_tablemap:
            value = has_tablemap.group("value")

    elif arg == "client_to_client":
        no_command_re = re.compile(r"^\s+no\s{0}\s*$".format(command), re.M)
        value = True

        if no_command_re.search(config):
            value = False

    elif arg == "retain_route_target":
        value = ""
        if command in config:
            route_target = has_command_val.group("value")
            if route_target:
                if route_target == "all":
                    value = "all"
                elif "route-map" in route_target:
                    value = route_target.replace("route-map ", "")

    elif arg in BOOL_PARAMS:
        command_re = re.compile(r"^\s+{0}\s*$".format(command), re.M)
        value = False

        if command_re.search(config):
            value = True

    else:
        value = ""

        if has_command_val:
            value = has_command_val.group("value")

    return value


def get_existing(module, args, warnings):
    existing = {}
    netcfg = CustomNetworkConfig(indent=2, contents=get_config(module))

    asn_regex = re.compile(
        r".*router\sbgp\s(?P<existing_asn>\d+(\.\d+)?).*", re.DOTALL
    )
    match_asn = asn_regex.match(str(netcfg))

    if match_asn:
        existing_asn = match_asn.group("existing_asn")
        parents = ["router bgp {0}".format(existing_asn)]
        if module.params["vrf"] != "default":
            parents.append("vrf {0}".format(module.params["vrf"]))

        parents.append(
            "address-family {0} {1}".format(
                module.params["afi"], module.params["safi"]
            )
        )
        config = netcfg.get_section(parents)

        if config:
            for arg in args:
                if arg not in ["asn", "afi", "safi", "vrf"]:
                    gv = get_value(arg, config, module)
                    if gv:
                        existing[arg] = gv
                    else:
                        if (
                            arg != "client_to_client"
                            and arg in PARAM_TO_DEFAULT_KEYMAP.keys()
                        ):
                            existing[arg] = PARAM_TO_DEFAULT_KEYMAP.get(arg)
                        else:
                            existing[arg] = gv

            existing["asn"] = existing_asn
            existing["afi"] = module.params["afi"]
            existing["safi"] = module.params["safi"]
            existing["vrf"] = module.params["vrf"]
    else:
        warnings.append(
            "The BGP process {0} didn't exist but the task just created it.".format(
                module.params["asn"]
            )
        )

    return existing


def apply_key_map(key_map, table):
    new_dict = {}
    for key, value in table.items():
        new_key = key_map.get(key)
        if new_key:
            new_dict[new_key] = value

    return new_dict


def fix_proposed(module, proposed, existing):
    commands = list()
    command = ""
    fixed_proposed = {}
    for key, value in proposed.items():
        if key in DAMPENING_PARAMS:
            if value != "default":
                command = "dampening {0} {1} {2} {3}".format(
                    proposed.get("dampening_half_time"),
                    proposed.get("dampening_reuse_time"),
                    proposed.get("dampening_suppress_time"),
                    proposed.get("dampening_max_suppress_time"),
                )
            else:
                if existing.get(key):
                    command = "no dampening {0} {1} {2} {3}".format(
                        existing["dampening_half_time"],
                        existing["dampening_reuse_time"],
                        existing["dampening_suppress_time"],
                        existing["dampening_max_suppress_time"],
                    )
            if "default" in command:
                command = ""
        elif key.startswith("distance"):
            command = "distance {0} {1} {2}".format(
                proposed.get("distance_ebgp"),
                proposed.get("distance_ibgp"),
                proposed.get("distance_local"),
            )
        else:
            fixed_proposed[key] = value

        if command:
            if command not in commands:
                commands.append(command)

    return fixed_proposed, commands


def default_existing(existing_value, key, value):
    commands = []
    if key == "network":
        for network in existing_value:
            if len(network) == 2:
                commands.append(
                    "no network {0} route-map {1}".format(
                        network[0], network[1]
                    )
                )
            elif len(network) == 1:
                commands.append("no network {0}".format(network[0]))

    elif key == "inject-map":
        for maps in existing_value:
            if len(maps) == 2:
                commands.append(
                    "no inject-map {0} exist-map {1}".format(maps[0], maps[1])
                )
            elif len(maps) == 3:
                commands.append(
                    "no inject-map {0} exist-map {1} "
                    "copy-attributes".format(maps[0], maps[1])
                )

    elif key == "redistribute":
        for maps in existing_value:
            commands.append(
                "no redistribute {0} route-map {1}".format(maps[0], maps[1])
            )

    elif key == "retain route-target":
        if existing_value == "all":
            commands.append("no {0} {1}".format(key, existing_value))
        elif existing_value != "default":
            commands.append("no {0} route-map {1}".format(key, existing_value))

    else:
        commands.append("no {0} {1}".format(key, existing_value))
    return commands


def get_network_command(existing, key, value):
    commands = []
    existing_networks = existing.get("networks", [])
    for inet in value:
        if not isinstance(inet, list):
            inet = [inet]
        if inet not in existing_networks:
            if len(inet) == 1:
                command = "{0} {1}".format(key, inet[0])
            elif len(inet) == 2:
                command = "{0} {1} route-map {2}".format(key, inet[0], inet[1])
            if command:
                commands.append(command)
    for enet in existing_networks:
        if enet not in value:
            if len(enet) == 1:
                command = "no {0} {1}".format(key, enet[0])
            elif len(enet) == 2:
                command = "no {0} {1} route-map {2}".format(
                    key, enet[0], enet[1]
                )
            if command:
                commands.append(command)
    return commands


def get_inject_map_command(existing, key, value):
    commands = []
    existing_maps = existing.get("inject_map", [])
    for maps in value:
        if not isinstance(maps, list):
            maps = [maps]
        if maps not in existing_maps:
            if len(maps) == 2:
                command = "inject-map {0} exist-map {1}".format(
                    maps[0], maps[1]
                )
            elif len(maps) == 3:
                command = (
                    "inject-map {0} exist-map {1} "
                    "copy-attributes".format(maps[0], maps[1])
                )
            if command:
                commands.append(command)
    for emaps in existing_maps:
        if emaps not in value:
            if len(emaps) == 2:
                command = "no inject-map {0} exist-map {1}".format(
                    emaps[0], emaps[1]
                )
            elif len(emaps) == 3:
                command = (
                    "no inject-map {0} exist-map {1} "
                    "copy-attributes".format(emaps[0], emaps[1])
                )
            if command:
                commands.append(command)
    return commands


def get_redistribute_command(existing, key, value):
    commands = []
    existing_rules = existing.get("redistribute", [])
    for rule in value:
        if not isinstance(rule, list):
            rule = [rule]
        if rule not in existing_rules:
            command = "redistribute {0} route-map {1}".format(rule[0], rule[1])
            commands.append(command)
    for erule in existing_rules:
        if erule not in value:
            command = "no redistribute {0} route-map {1}".format(
                erule[0], erule[1]
            )
            commands.append(command)
    return commands


def get_table_map_command(module, existing, key, value):
    commands = []
    if key == "table-map":
        if value != "default":
            command = "{0} {1}".format(key, module.params["table_map"])
            if (
                module.params["table_map_filter"] is not None
                and module.params["table_map_filter"] != "default"
            ):
                command += " filter"
            commands.append(command)
        else:
            if existing.get("table_map"):
                command = "no {0} {1}".format(key, existing.get("table_map"))
                commands.append(command)
    return commands


def get_retain_route_target_command(existing, key, value):
    commands = []
    if key == "retain route-target":
        if value != "default":
            if value == "all":
                command = "{0} {1}".format(key, value)
            else:
                command = "{0} route-map {1}".format(key, value)
        else:
            existing_value = existing.get("retain_route_target")
            if existing_value == "all":
                command = "no {0} {1}".format(key, existing_value)
            else:
                command = "no {0} route-map {1}".format(key, existing_value)
        commands.append(command)
    return commands


def get_default_table_map_filter(existing):
    commands = []
    existing_table_map_filter = existing.get("table_map_filter")
    if existing_table_map_filter:
        existing_table_map = existing.get("table_map")
        if existing_table_map:
            command = "table-map {0}".format(existing_table_map)
            commands.append(command)
    return commands


def state_present(module, existing, proposed, candidate):
    fixed_proposed, commands = fix_proposed(module, proposed, existing)
    proposed_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, fixed_proposed)
    existing_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, existing)
    for key, value in proposed_commands.items():
        if key == "address-family":
            addr_family_command = "address-family {0} {1}".format(
                module.params["afi"], module.params["safi"]
            )
            if addr_family_command not in commands:
                commands.append(addr_family_command)

        elif key.startswith("table-map"):
            table_map_commands = get_table_map_command(
                module, existing, key, value
            )
            if table_map_commands:
                commands.extend(table_map_commands)

        elif value is True:
            commands.append(key)

        elif value is False:
            commands.append("no {0}".format(key))

        elif value == "default":
            if key in PARAM_TO_DEFAULT_KEYMAP:
                commands.append(
                    "{0} {1}".format(key, PARAM_TO_DEFAULT_KEYMAP[key])
                )

            elif existing_commands.get(key):
                if key == "table-map-filter":
                    default_tmf_command = get_default_table_map_filter(
                        existing
                    )

                    if default_tmf_command:
                        commands.extend(default_tmf_command)
                else:
                    existing_value = existing_commands.get(key)
                    default_command = default_existing(
                        existing_value, key, value
                    )
                    if default_command:
                        commands.extend(default_command)
        else:
            if key == "network":
                network_commands = get_network_command(existing, key, value)
                if network_commands:
                    commands.extend(network_commands)

            elif key == "inject-map":
                inject_map_commands = get_inject_map_command(
                    existing, key, value
                )
                if inject_map_commands:
                    commands.extend(inject_map_commands)

            elif key == "redistribute":
                redistribute_commands = get_redistribute_command(
                    existing, key, value
                )
                if redistribute_commands:
                    commands.extend(redistribute_commands)

            elif key == "retain route-target":
                retain_route_target_commands = get_retain_route_target_command(
                    existing, key, value
                )
                if retain_route_target_commands:
                    commands.extend(retain_route_target_commands)

            else:
                command = "{0} {1}".format(key, value)
                commands.append(command)

    if commands:
        parents = ["router bgp {0}".format(module.params["asn"])]
        if module.params["vrf"] != "default":
            parents.append("vrf {0}".format(module.params["vrf"]))

        addr_family_command = "address-family {0} {1}".format(
            module.params["afi"], module.params["safi"]
        )
        parents.append(addr_family_command)
        if addr_family_command in commands:
            commands.remove(addr_family_command)
        candidate.add(commands, parents=parents)


def state_absent(module, candidate):
    commands = []
    parents = ["router bgp {0}".format(module.params["asn"])]
    if module.params["vrf"] != "default":
        parents.append("vrf {0}".format(module.params["vrf"]))

    commands.append(
        "no address-family {0} {1}".format(
            module.params["afi"], module.params["safi"]
        )
    )
    candidate.add(commands, parents=parents)


def main():
    argument_spec = dict(
        asn=dict(required=True, type="str"),
        vrf=dict(required=False, type="str", default="default"),
        safi=dict(
            required=True, type="str", choices=["unicast", "multicast", "evpn"]
        ),
        afi=dict(
            required=True,
            type="str",
            choices=["ipv4", "ipv6", "vpnv4", "vpnv6", "l2vpn"],
        ),
        additional_paths_install=dict(required=False, type="bool"),
        additional_paths_receive=dict(required=False, type="bool"),
        additional_paths_selection=dict(required=False, type="str"),
        additional_paths_send=dict(required=False, type="bool"),
        advertise_l2vpn_evpn=dict(required=False, type="bool"),
        client_to_client=dict(required=False, type="bool"),
        dampen_igp_metric=dict(required=False, type="str"),
        dampening_state=dict(required=False, type="bool"),
        dampening_half_time=dict(required=False, type="str"),
        dampening_max_suppress_time=dict(required=False, type="str"),
        dampening_reuse_time=dict(required=False, type="str"),
        dampening_routemap=dict(required=False, type="str"),
        dampening_suppress_time=dict(required=False, type="str"),
        default_information_originate=dict(required=False, type="bool"),
        default_metric=dict(required=False, type="str"),
        distance_ebgp=dict(required=False, type="str"),
        distance_ibgp=dict(required=False, type="str"),
        distance_local=dict(required=False, type="str"),
        inject_map=dict(required=False, type="list", elements="list"),
        maximum_paths=dict(required=False, type="str"),
        maximum_paths_ibgp=dict(required=False, type="str"),
        networks=dict(required=False, type="list", elements="list"),
        next_hop_route_map=dict(required=False, type="str"),
        redistribute=dict(required=False, type="list", elements="list"),
        suppress_inactive=dict(required=False, type="bool"),
        table_map=dict(required=False, type="str"),
        table_map_filter=dict(required=False, type="bool"),
        state=dict(
            choices=["present", "absent"], default="present", required=False
        ),
        retain_route_target=dict(required=False, type="str"),
    )

    argument_spec.update(nxos_argument_spec)

    mutually_exclusive = [
        ("dampening_state", "dampening_routemap"),
        ("dampening_state", "dampening_half_time"),
        ("dampening_state", "dampening_suppress_time"),
        ("dampening_state", "dampening_reuse_time"),
        ("dampening_state", "dampening_max_suppress_time"),
        ("dampening_routemap", "dampening_half_time"),
        ("dampening_routemap", "dampening_suppress_time"),
        ("dampening_routemap", "dampening_reuse_time"),
        ("dampening_routemap", "dampening_max_suppress_time"),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        required_together=[
            DAMPENING_PARAMS,
            ["distance_ibgp", "distance_ebgp", "distance_local"],
        ],
        supports_check_mode=True,
    )

    warnings = list()
    result = dict(changed=False, warnings=warnings)

    state = module.params["state"]

    if module.params["advertise_l2vpn_evpn"]:
        if module.params["vrf"] == "default":
            module.fail_json(
                msg="It is not possible to advertise L2VPN "
                "EVPN in the default VRF. Please specify "
                "another one.",
                vrf=module.params["vrf"],
            )

    if module.params["table_map_filter"] and not module.params["table_map"]:
        module.fail_json(
            msg="table_map param is needed when using"
            " table_map_filter filter."
        )

    args = PARAM_TO_COMMAND_KEYMAP.keys()
    existing = get_existing(module, args, warnings)

    if existing.get("asn") and state == "present":
        if existing.get("asn") != module.params["asn"]:
            module.fail_json(
                msg="Another BGP ASN already exists.",
                proposed_asn=module.params["asn"],
                existing_asn=existing.get("asn"),
            )

    proposed_args = dict(
        (k, v) for k, v in module.params.items() if v is not None and k in args
    )

    for arg in ["networks", "inject_map", "redistribute"]:
        if proposed_args.get(arg):
            if proposed_args[arg][0] == "default":
                proposed_args[arg] = "default"

    proposed = {}
    for key, value in proposed_args.items():
        if key not in ["asn", "vrf"]:
            if str(value).lower() == "default":
                value = PARAM_TO_DEFAULT_KEYMAP.get(key, "default")
            if existing.get(key) != value:
                proposed[key] = value

    candidate = CustomNetworkConfig(indent=3)
    if state == "present":
        state_present(module, existing, proposed, candidate)
    elif state == "absent" and existing:
        state_absent(module, candidate)

    if candidate:
        candidate = candidate.items_text()
        if not module.check_mode:
            load_config(module, candidate)
        result["changed"] = True
        result["commands"] = candidate
    else:
        result["commands"] = []

    module.exit_json(**result)


if __name__ == "__main__":
    main()
