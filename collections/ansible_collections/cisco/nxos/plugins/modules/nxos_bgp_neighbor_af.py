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
module: nxos_bgp_neighbor_af
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Manages BGP address-family's neighbors configuration.
description:
- Manages BGP address-family's neighbors configurations on NX-OS switches.
version_added: 1.0.0
author: Gabriele Gerbino (@GGabriele)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- C(state=absent) removes the whole BGP address-family's neighbor configuration.
- Default, when supported, removes properties
- In order to default maximum-prefix configuration, only C(max_prefix_limit=default)
  is needed.
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
    default: default
    type: str
  neighbor:
    description:
    - Neighbor Identifier. Valid values are string. Neighbors may use IPv4 or IPv6
      notation, with or without prefix length.
    required: true
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
  additional_paths_receive:
    description:
    - Valid values are enable for basic command enablement; disable for disabling
      the command at the neighbor af level (it adds the disable keyword to the basic
      command); and inherit to remove the command at this level (the command value
      is inherited from a higher BGP layer).
    choices:
    - enable
    - disable
    - inherit
    type: str
  additional_paths_send:
    description:
    - Valid values are enable for basic command enablement; disable for disabling
      the command at the neighbor af level (it adds the disable keyword to the basic
      command); and inherit to remove the command at this level (the command value
      is inherited from a higher BGP layer).
    choices:
    - enable
    - disable
    - inherit
    type: str
  advertise_map_exist:
    description:
    - Conditional route advertisement. This property requires two route maps, an advertise-map
      and an exist-map. Valid values are an array specifying both the advertise-map
      name and the exist-map name, or simply 'default' e.g. ['my_advertise_map', 'my_exist_map'].
      This command is mutually exclusive with the advertise_map_non_exist property.
    type: list
    elements: str
  advertise_map_non_exist:
    description:
    - Conditional route advertisement. This property requires two route maps, an advertise-map
      and an exist-map. Valid values are an array specifying both the advertise-map
      name and the non-exist-map name, or simply 'default' e.g. ['my_advertise_map',
      'my_non_exist_map']. This command is mutually exclusive with the advertise_map_exist
      property.
    type: list
    elements: str
  allowas_in:
    description:
    - Activate allowas-in property
    type: bool
  allowas_in_max:
    description:
    - Max-occurrences value for allowas_in. Valid values are an integer value or 'default'.
      This is mutually exclusive with allowas_in.
    type: str
  as_override:
    description:
    - Activate the as-override feature.
    type: bool
  default_originate:
    description:
    - Activate the default-originate feature.
    type: bool
  default_originate_route_map:
    description:
    - Route-map for the default_originate property. Valid values are a string defining
      a route-map name, or 'default'. This is mutually exclusive with default_originate.
    type: str
  disable_peer_as_check:
    description:
    - Disable checking of peer AS-number while advertising
    type: bool
  filter_list_in:
    description:
    - Valid values are a string defining a filter-list name, or 'default'.
    type: str
  filter_list_out:
    description:
    - Valid values are a string defining a filter-list name, or 'default'.
    type: str
  max_prefix_limit:
    description:
    - maximum-prefix limit value. Valid values are an integer value or 'default'.
    type: str
  max_prefix_interval:
    description:
    - Optional restart interval. Valid values are an integer. Requires max_prefix_limit.
      May not be combined with max_prefix_warning.
    type: str
  max_prefix_threshold:
    description:
    - Optional threshold percentage at which to generate a warning. Valid values are
      an integer value. Requires max_prefix_limit.
    type: str
  max_prefix_warning:
    description:
    - Optional warning-only keyword. Requires max_prefix_limit. May not be combined
      with max_prefix_interval.
    type: bool
  next_hop_self:
    description:
    - Activate the next-hop-self feature.
    type: bool
  next_hop_third_party:
    description:
    - Activate the next-hop-third-party feature.
    type: bool
  prefix_list_in:
    description:
    - Valid values are a string defining a prefix-list name, or 'default'.
    type: str
  prefix_list_out:
    description:
    - Valid values are a string defining a prefix-list name, or 'default'.
    type: str
  route_map_in:
    description:
    - Valid values are a string defining a route-map name, or 'default'.
    type: str
  route_map_out:
    description:
    - Valid values are a string defining a route-map name, or 'default'.
    type: str
  route_reflector_client:
    description:
    - Router reflector client.
    type: bool
  send_community:
    description:
    - send-community attribute.
    choices:
    - none
    - both
    - extended
    - standard
    - default
    type: str
  soft_reconfiguration_in:
    description:
    - Valid values are 'enable' for basic command enablement; 'always' to add the
      always keyword to the basic command; and 'inherit' to remove the command at
      this level (the command value is inherited from a higher BGP layer).
    choices:
    - enable
    - always
    - inherit
    type: str
  soo:
    description:
    - Site-of-origin. Valid values are a string defining a VPN extcommunity or 'default'.
    type: str
  suppress_inactive:
    description:
    - suppress-inactive feature.
    type: bool
  unsuppress_map:
    description:
    - unsuppress-map. Valid values are a string defining a route-map name or 'default'.
    type: str
  weight:
    description:
    - Weight value. Valid values are an integer value or 'default'.
    type: str
  state:
    description:
    - Determines whether the config should be present or not on the device.
    default: present
    choices:
    - present
    - absent
    type: str
  rewrite_evpn_rt_asn:
    description:
    - Auto generate route targets for EBGP neighbor.
    type: bool
    version_added: 1.1.0
"""
EXAMPLES = """
- name: configure RR client
  cisco.nxos.nxos_bgp_neighbor_af:
    asn: 65535
    neighbor: 192.0.2.3
    afi: ipv4
    safi: unicast
    route_reflector_client: true
    state: present
    rewrite_evpn_rt_asn: true
"""

RETURN = """
commands:
  description: commands sent to the device
  returned: always
  type: list
  sample: ["router bgp 65535", "neighbor 192.0.2.3",
           "address-family ipv4 unicast", "route-reflector-client",
           "rewrite-evpn-rt-asn"]
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
    "allowas_in",
    "as_override",
    "default_originate",
    "disable_peer_as_check",
    "next_hop_self",
    "next_hop_third_party",
    "route_reflector_client",
    "suppress_inactive",
    "rewrite_evpn_rt_asn",
]
PARAM_TO_COMMAND_KEYMAP = {
    "afi": "address-family",
    "asn": "router bgp",
    "neighbor": "neighbor",
    "additional_paths_receive": "capability additional-paths receive",
    "additional_paths_send": "capability additional-paths send",
    "advertise_map_exist": "advertise-map exist-map",
    "advertise_map_non_exist": "advertise-map non-exist-map",
    "allowas_in": "allowas-in",
    "allowas_in_max": "allowas-in",
    "as_override": "as-override",
    "default_originate": "default-originate",
    "default_originate_route_map": "default-originate route-map",
    "disable_peer_as_check": "disable-peer-as-check",
    "filter_list_in": "filter-list in",
    "filter_list_out": "filter-list out",
    "max_prefix_limit": "maximum-prefix",
    "max_prefix_interval": "maximum-prefix interval",
    "max_prefix_threshold": "maximum-prefix threshold",
    "max_prefix_warning": "maximum-prefix warning",
    "next_hop_self": "next-hop-self",
    "next_hop_third_party": "next-hop-third-party",
    "prefix_list_in": "prefix-list in",
    "prefix_list_out": "prefix-list out",
    "route_map_in": "route-map in",
    "route_map_out": "route-map out",
    "route_reflector_client": "route-reflector-client",
    "safi": "address-family",
    "send_community": "send-community",
    "soft_reconfiguration_in": "soft-reconfiguration inbound",
    "soo": "soo",
    "suppress_inactive": "suppress-inactive",
    "unsuppress_map": "unsuppress-map",
    "weight": "weight",
    "vrf": "vrf",
    "rewrite_evpn_rt_asn": "rewrite-evpn-rt-asn",
}


def get_value(arg, config, module):
    custom = [
        "additional_paths_send",
        "additional_paths_receive",
        "max_prefix_limit",
        "max_prefix_interval",
        "max_prefix_threshold",
        "max_prefix_warning",
        "send_community",
        "soft_reconfiguration_in",
    ]
    command = PARAM_TO_COMMAND_KEYMAP[arg]
    has_command = re.search(r"^\s+{0}\s*".format(command), config, re.M)
    has_command_val = re.search(
        r"(?:{0}\s)(?P<value>.*)$".format(command), config, re.M
    )
    value = ""

    if arg in custom:
        value = get_custom_value(arg, config, module)

    elif arg == "next_hop_third_party":
        has_no_command = re.search(
            r"^\s+no\s+{0}\s*$".format(command), config, re.M
        )
        value = False
        if not has_no_command:
            value = True

    elif arg in BOOL_PARAMS:
        value = False
        if has_command:
            value = True

    elif command.startswith("advertise-map"):
        value = []
        has_adv_map = re.search(
            r"{0}\s(?P<value1>.*)\s{1}\s(?P<value2>.*)$".format(
                *command.split()
            ),
            config,
            re.M,
        )
        if has_adv_map:
            value = list(has_adv_map.groups())

    elif command.split()[0] in ["filter-list", "prefix-list", "route-map"]:
        has_cmd_direction_val = re.search(
            r"{0}\s(?P<value>.*)\s{1}$".format(*command.split()), config, re.M
        )
        if has_cmd_direction_val:
            value = has_cmd_direction_val.group("value")

    elif has_command_val:
        value = has_command_val.group("value")

    return value


def get_custom_value(arg, config, module):
    command = PARAM_TO_COMMAND_KEYMAP.get(arg)
    splitted_config = config.splitlines()
    value = ""

    if arg.startswith("additional_paths"):
        value = "inherit"
        for line in splitted_config:
            if command in line:
                if "disable" in line:
                    value = "disable"
                else:
                    value = "enable"
    elif arg.startswith("max_prefix"):
        for line in splitted_config:
            if "maximum-prefix" in line:
                splitted_line = line.split()
                if arg == "max_prefix_limit":
                    value = splitted_line[1]
                elif arg == "max_prefix_interval" and "restart" in line:
                    value = splitted_line[-1]
                elif arg == "max_prefix_threshold" and len(splitted_line) > 2:
                    try:
                        int(splitted_line[2])
                        value = splitted_line[2]
                    except ValueError:
                        value = ""
                elif arg == "max_prefix_warning":
                    value = "warning-only" in line
    elif arg == "soft_reconfiguration_in":
        value = "inherit"
        for line in splitted_config:
            if command in line:
                if "always" in line:
                    value = "always"
                else:
                    value = "enable"

    elif arg == "send_community":
        value = "none"
        for line in splitted_config:
            if command in line:
                if "extended" in line:
                    if value == "standard":
                        value = "both"
                    else:
                        value = "extended"
                elif "both" in line:
                    value = "both"
                else:
                    value = "standard"

    return value


def get_existing(module, args, warnings):
    existing = {}
    netcfg = CustomNetworkConfig(indent=2, contents=get_config(module))

    asn_regex = re.compile(
        r".*router\sbgp\s(?P<existing_asn>\d+(\.\d+)?).*", re.S
    )
    match_asn = asn_regex.match(str(netcfg))

    if match_asn:
        existing_asn = match_asn.group("existing_asn")
        parents = ["router bgp {0}".format(existing_asn)]

        if module.params["vrf"] != "default":
            parents.append("vrf {0}".format(module.params["vrf"]))

        parents.append("neighbor {0}".format(module.params["neighbor"]))
        parents.append(
            "address-family {0} {1}".format(
                module.params["afi"], module.params["safi"]
            )
        )
        config = netcfg.get_section(parents)

        if config:
            for arg in args:
                if arg not in ["asn", "vrf", "neighbor", "afi", "safi"]:
                    existing[arg] = get_value(arg, config, module)

            existing["asn"] = existing_asn
            existing["neighbor"] = module.params["neighbor"]
            existing["vrf"] = module.params["vrf"]
            existing["afi"] = module.params["afi"]
            existing["safi"] = module.params["safi"]
    else:
        warnings.append(
            "The BGP process didn't exist but the task just created it."
        )

    return existing


def apply_key_map(key_map, table):
    new_dict = {}
    for key in table:
        new_key = key_map.get(key)
        if new_key:
            new_dict[new_key] = table.get(key)

    return new_dict


def get_default_command(key, value, existing_commands):
    command = ""
    if existing_commands.get(key):
        existing_value = existing_commands.get(key)
        if value == "inherit":
            if existing_value != "inherit":
                command = "no {0}".format(key)
        else:
            if key == "advertise-map exist-map":
                command = "no advertise-map {0} exist-map {1}".format(
                    existing_value[0], existing_value[1]
                )
            elif key == "advertise-map non-exist-map":
                command = "no advertise-map {0} non-exist-map {1}".format(
                    existing_value[0], existing_value[1]
                )
            elif key == "filter-list in":
                command = "no filter-list {0} in".format(existing_value)
            elif key == "filter-list out":
                command = "no filter-list {0} out".format(existing_value)
            elif key == "prefix-list in":
                command = "no prefix-list {0} in".format(existing_value)
            elif key == "prefix-list out":
                command = "no prefix-list {0} out".format(existing_value)
            elif key == "route-map in":
                command = "no route-map {0} in".format(existing_value)
            elif key == "route-map out":
                command = "no route-map {0} out".format(existing_value)
            elif key.startswith("maximum-prefix"):
                command = "no maximum-prefix"
            elif key == "allowas-in max":
                command = ["no allowas-in {0}".format(existing_value)]
                command.append("allowas-in")
            else:
                command = "no {0} {1}".format(key, existing_value)
    else:
        if key.replace(" ", "_").replace("-", "_") in BOOL_PARAMS:
            command = "no {0}".format(key)
    return command


def fix_proposed(module, existing, proposed):
    allowas_in = proposed.get("allowas_in")
    allowas_in_max = proposed.get("allowas_in_max")

    if allowas_in_max and not allowas_in:
        proposed.pop("allowas_in_max")
    elif allowas_in and allowas_in_max:
        proposed.pop("allowas_in")

    if (
        existing.get("send_community") == "none"
        and proposed.get("send_community") == "default"
    ):
        proposed.pop("send_community")
    return proposed


def state_present(module, existing, proposed, candidate):
    commands = list()
    proposed = fix_proposed(module, existing, proposed)

    proposed_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, proposed)
    existing_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, existing)
    for key, value in proposed_commands.items():
        if value in ["inherit", "default"]:
            command = get_default_command(key, value, existing_commands)

            if isinstance(command, str):
                if command and command not in commands:
                    commands.append(command)
            elif isinstance(command, list):
                for cmd in command:
                    if cmd not in commands:
                        commands.append(cmd)

        elif key.startswith("maximum-prefix"):
            if module.params["max_prefix_limit"] != "default":
                command = "maximum-prefix {0}".format(
                    module.params["max_prefix_limit"]
                )
                if module.params["max_prefix_threshold"]:
                    command += " {0}".format(
                        module.params["max_prefix_threshold"]
                    )
                if module.params["max_prefix_interval"]:
                    command += " restart {0}".format(
                        module.params["max_prefix_interval"]
                    )
                elif module.params["max_prefix_warning"]:
                    command += " warning-only"
                commands.append(command)

        elif value is True:
            commands.append(key)
        elif value is False:
            commands.append("no {0}".format(key))
        elif key == "address-family":
            commands.append(
                "address-family {0} {1}".format(
                    module.params["afi"], module.params["safi"]
                )
            )
        elif key.startswith("capability additional-paths"):
            command = key
            if value == "disable":
                command += " disable"
            commands.append(command)
        elif key.startswith("advertise-map"):
            direction = key.split()[1]
            commands.append(
                "advertise-map {1} {0} {2}".format(direction, *value)
            )
        elif key.split()[0] in ["filter-list", "prefix-list", "route-map"]:
            commands.append("{1} {0} {2}".format(value, *key.split()))

        elif key == "soft-reconfiguration inbound":
            command = ""
            if value == "enable":
                command = key
            elif value == "always":
                command = "{0} {1}".format(key, value)
            commands.append(command)
        elif key == "send-community":
            command = key
            if value in ["standard", "extended"]:
                commands.append("no " + key + " both")
            command += " {0}".format(value)
            commands.append(command)
        else:
            command = "{0} {1}".format(key, value)
            commands.append(command)

    if commands:
        parents = ["router bgp {0}".format(module.params["asn"])]
        if module.params["vrf"] != "default":
            parents.append("vrf {0}".format(module.params["vrf"]))

        parents.append("neighbor {0}".format(module.params["neighbor"]))

        af_command = "address-family {0} {1}".format(
            module.params["afi"], module.params["safi"]
        )
        parents.append(af_command)
        if af_command in commands:
            commands.remove(af_command)
        candidate.add(commands, parents=parents)


def state_absent(module, existing, candidate):
    commands = []
    parents = ["router bgp {0}".format(module.params["asn"])]
    if module.params["vrf"] != "default":
        parents.append("vrf {0}".format(module.params["vrf"]))

    parents.append("neighbor {0}".format(module.params["neighbor"]))
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
        neighbor=dict(required=True, type="str"),
        afi=dict(
            required=True,
            type="str",
            choices=["ipv4", "ipv6", "vpnv4", "vpnv6", "l2vpn"],
        ),
        safi=dict(
            required=True, type="str", choices=["unicast", "multicast", "evpn"]
        ),
        additional_paths_receive=dict(
            required=False,
            type="str",
            choices=["enable", "disable", "inherit"],
        ),
        additional_paths_send=dict(
            required=False,
            type="str",
            choices=["enable", "disable", "inherit"],
        ),
        advertise_map_exist=dict(required=False, type="list", elements="str"),
        advertise_map_non_exist=dict(
            required=False, type="list", elements="str"
        ),
        allowas_in=dict(required=False, type="bool"),
        allowas_in_max=dict(required=False, type="str"),
        as_override=dict(required=False, type="bool"),
        default_originate=dict(required=False, type="bool"),
        default_originate_route_map=dict(required=False, type="str"),
        disable_peer_as_check=dict(required=False, type="bool"),
        filter_list_in=dict(required=False, type="str"),
        filter_list_out=dict(required=False, type="str"),
        max_prefix_limit=dict(required=False, type="str"),
        max_prefix_interval=dict(required=False, type="str"),
        max_prefix_threshold=dict(required=False, type="str"),
        max_prefix_warning=dict(required=False, type="bool"),
        next_hop_self=dict(required=False, type="bool"),
        next_hop_third_party=dict(required=False, type="bool"),
        prefix_list_in=dict(required=False, type="str"),
        prefix_list_out=dict(required=False, type="str"),
        route_map_in=dict(required=False, type="str"),
        route_map_out=dict(required=False, type="str"),
        route_reflector_client=dict(required=False, type="bool"),
        send_community=dict(
            required=False,
            choices=["none", "both", "extended", "standard", "default"],
        ),
        soft_reconfiguration_in=dict(
            required=False, type="str", choices=["enable", "always", "inherit"]
        ),
        soo=dict(required=False, type="str"),
        suppress_inactive=dict(required=False, type="bool"),
        unsuppress_map=dict(required=False, type="str"),
        weight=dict(required=False, type="str"),
        state=dict(
            choices=["present", "absent"], default="present", required=False
        ),
        rewrite_evpn_rt_asn=dict(required=False, type="bool"),
    )
    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ["advertise_map_exist", "advertise_map_non_exist"],
            ["max_prefix_interval", "max_prefix_warning"],
            ["default_originate", "default_originate_route_map"],
            ["allowas_in", "allowas_in_max"],
        ],
        supports_check_mode=True,
    )

    warnings = list()
    result = dict(changed=False, warnings=warnings)

    state = module.params["state"]
    for key in [
        "max_prefix_interval",
        "max_prefix_warning",
        "max_prefix_threshold",
    ]:
        if module.params[key] and not module.params["max_prefix_limit"]:
            module.fail_json(
                msg="max_prefix_limit is required when using %s" % key
            )
    if module.params["vrf"] == "default" and module.params["soo"]:
        module.fail_json(msg="SOO is only allowed in non-default VRF")

    args = PARAM_TO_COMMAND_KEYMAP.keys()
    existing = get_existing(module, args, warnings)

    if existing.get("asn") and state == "present":
        if existing.get("asn") != module.params["asn"]:
            module.fail_json(
                msg="Another BGP ASN already exists.",
                proposed_asn=module.params["asn"],
                existing_asn=existing.get("asn"),
            )

    for param in ["advertise_map_exist", "advertise_map_non_exist"]:
        if module.params[param] == ["default"]:
            module.params[param] = "default"

    proposed_args = dict(
        (k, v) for k, v in module.params.items() if v is not None and k in args
    )

    proposed = {}
    for key, value in proposed_args.items():
        if key not in ["asn", "vrf", "neighbor"]:
            if not isinstance(value, list):
                if str(value).lower() == "true":
                    value = True
                elif str(value).lower() == "false":
                    value = False
                elif str(value).lower() == "default":
                    if key in BOOL_PARAMS:
                        value = False
                    else:
                        value = "default"
                elif key == "send_community" and str(value).lower() == "none":
                    value = "default"
            if existing.get(key) != value:
                proposed[key] = value

    candidate = CustomNetworkConfig(indent=3)
    if state == "present":
        state_present(module, existing, proposed, candidate)
    elif state == "absent" and existing:
        state_absent(module, existing, candidate)

    if candidate:
        candidate = candidate.items_text()
        if not module.check_mode:
            responses = load_config(module, candidate)
            if responses:
                for resp in responses:
                    if resp:
                        if resp.endswith("is valid only for EBGP peers"):
                            module.fail_json(msg=resp)
        result["changed"] = True
        result["commands"] = candidate
    else:
        result["commands"] = []

    module.exit_json(**result)


if __name__ == "__main__":
    main()
