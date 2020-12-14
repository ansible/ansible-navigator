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
module: ios_l3_interface
author: Ganesh Nalawade (@ganeshrn)
short_description: (deprecated, removed after 2022-06-01) Manage Layer-3 interfaces
  on Cisco IOS network devices.
description:
- This module provides declarative management of Layer-3 interfaces on IOS network
  devices.
version_added: 1.0.0
deprecated:
  alternative: ios_l3_interfaces
  why: Newer and updated modules released with more functionality in Ansible 2.9
  removed_at_date: '2022-06-01'
notes:
- Tested against IOS 15.2
options:
  name:
    description:
    - Name of the Layer-3 interface to be configured eg. GigabitEthernet0/2
    type: str
  ipv4:
    description:
    - IPv4 address to be set for the Layer-3 interface mentioned in I(name) option.
      The address format is <ipv4 address>/<mask>, the mask is number in range 0-32
      eg. 192.168.0.1/24
    type: str
  ipv6:
    description:
    - IPv6 address to be set for the Layer-3 interface mentioned in I(name) option.
      The address format is <ipv6 address>/<mask>, the mask is number in range 0-128
      eg. fd5d:12c9:2201:1::1/64
    type: str
  aggregate:
    description:
    - List of Layer-3 interfaces definitions. Each of the entry in aggregate list
      should define name of interface C(name) and a optional C(ipv4) or C(ipv6) address.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name of the Layer-3 interface to be configured eg. GigabitEthernet0/2
        type: str
        required: true
      ipv4:
        description:
        - IPv4 address to be set for the Layer-3 interface mentioned in I(name) option.
          The address format is <ipv4 address>/<mask>, the mask is number in range 0-32
          eg. 192.168.0.1/24
        type: str
      ipv6:
        description:
        - IPv6 address to be set for the Layer-3 interface mentioned in I(name) option.
          The address format is <ipv6 address>/<mask>, the mask is number in range 0-128
          eg. fd5d:12c9:2201:1::1/64
        type: str
      state:
        description:
        - State of the Layer-3 interface configuration. It indicates if the configuration
          should be present or absent on remote device.
        type: str
        choices:
        - present
        - absent
  state:
    description:
    - State of the Layer-3 interface configuration. It indicates if the configuration
      should be present or absent on remote device.
    default: present
    choices:
    - present
    - absent
    type: str
extends_documentation_fragment:
- cisco.ios.ios


"""
EXAMPLES = """
- name: Remove GigabitEthernet0/3 IPv4 and IPv6 address
  cisco.ios.ios_l3_interface:
    name: GigabitEthernet0/3
    state: absent
- name: Set GigabitEthernet0/3 IPv4 address
  cisco.ios.ios_l3_interface:
    name: GigabitEthernet0/3
    ipv4: 192.168.0.1/24
- name: Set GigabitEthernet0/3 IPv6 address
  cisco.ios.ios_l3_interface:
    name: GigabitEthernet0/3
    ipv6: fd5d:12c9:2201:1::1/64
- name: Set GigabitEthernet0/3 in dhcp
  cisco.ios.ios_l3_interface:
    name: GigabitEthernet0/3
    ipv4: dhcp
    ipv6: dhcp
- name: Set interface Vlan1 (SVI) IPv4 address
  cisco.ios.ios_l3_interface:
    name: Vlan1
    ipv4: 192.168.0.5/24
- name: Set IP addresses on aggregate
  cisco.ios.ios_l3_interface:
    aggregate:
    - {name: GigabitEthernet0/3, ipv4: 192.168.2.10/24}
    - {name: GigabitEthernet0/3, ipv4: 192.168.3.10/24, ipv6: fd5d:12c9:2201:1::1/64}
- name: Remove IP addresses on aggregate
  cisco.ios.ios_l3_interface:
    aggregate:
    - {name: GigabitEthernet0/3, ipv4: 192.168.2.10/24}
    - {name: GigabitEthernet0/3, ipv4: 192.168.3.10/24, ipv6: fd5d:12c9:2201:1::1/64}
    state: absent
"""
RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - interface GigabitEthernet0/2
    - ip address 192.168.0.1 255.255.255.0
    - ipv6 address fd5d:12c9:2201:1::1/64
"""
import re
from copy import deepcopy
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    get_config,
    load_config,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    ios_argument_spec,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_default_spec,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    is_netmask,
    is_masklen,
    to_netmask,
    to_masklen,
)


def validate_ipv4(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv4 address>/<mask>, got invalid format %s"
                % value
            )
        if not is_masklen(address[1]):
            module.fail_json(
                msg="invalid value for mask: %s, mask should be in range 0-32"
                % address[1]
            )


def validate_ipv6(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv6 address>/<mask>, got invalid format %s"
                % value
            )
        elif not 0 <= int(address[1]) <= 128:
            module.fail_json(
                msg="invalid value for mask: %s, mask should be in range 0-128"
                % address[1]
            )


def validate_param_values(module, obj, param=None):
    if param is None:
        param = module.params
    for key in obj:
        # validate the param value (if validator func exists)
        validator = globals().get("validate_%s" % key)
        if callable(validator):
            validator(param.get(key), module)


def parse_config_argument(configobj, name, arg=None):
    cfg = configobj["interface %s" % name]
    cfg = "\n".join(cfg.children)
    values = []
    matches = re.finditer("%s (.+)$" % arg, cfg, re.M)
    for match in matches:
        match_str = match.group(1).strip()
        if arg == "ipv6 address":
            values.append(match_str)
        else:
            values = match_str
            break
    return values or None


def search_obj_in_list(name, lst):
    for o in lst:
        if o["name"] == name:
            return o
    return None


def map_obj_to_commands(updates, module):
    commands = list()
    want, have = updates
    for w in want:
        name = w["name"]
        ipv4 = w["ipv4"]
        ipv6 = w["ipv6"]
        state = w["state"]
        interface = "interface " + name
        commands.append(interface)
        obj_in_have = search_obj_in_list(name, have)
        if state == "absent" and obj_in_have:
            if obj_in_have["ipv4"]:
                if ipv4:
                    address = ipv4.split("/")
                    if len(address) == 2:
                        ipv4 = "{0} {1}".format(
                            address[0], to_netmask(address[1])
                        )
                    commands.append("no ip address {0}".format(ipv4))
                else:
                    commands.append("no ip address")
            if obj_in_have["ipv6"]:
                if ipv6:
                    commands.append("no ipv6 address {0}".format(ipv6))
                else:
                    commands.append("no ipv6 address")
                    if "dhcp" in obj_in_have["ipv6"]:
                        commands.append("no ipv6 address dhcp")
        elif state == "present":
            if ipv4:
                if (
                    obj_in_have is None
                    or obj_in_have.get("ipv4") is None
                    or ipv4 != obj_in_have["ipv4"]
                ):
                    address = ipv4.split("/")
                    if len(address) == 2:
                        ipv4 = "{0} {1}".format(
                            address[0], to_netmask(address[1])
                        )
                    commands.append("ip address {0}".format(ipv4))
            if ipv6:
                if (
                    obj_in_have is None
                    or obj_in_have.get("ipv6") is None
                    or ipv6.lower()
                    not in [addr.lower() for addr in obj_in_have["ipv6"]]
                ):
                    commands.append("ipv6 address {0}".format(ipv6))
        if commands[-1] == interface:
            commands.pop(-1)
    return commands


def map_config_to_obj(module):
    config = get_config(module)
    configobj = NetworkConfig(indent=1, contents=config)
    match = re.findall("^interface (\\S+)", config, re.M)
    if not match:
        return list()
    instances = list()
    for item in set(match):
        ipv4 = parse_config_argument(configobj, item, "ip address")
        if ipv4:
            address = ipv4.strip().split(" ")
            if len(address) == 2 and is_netmask(address[1]):
                ipv4 = "{0}/{1}".format(
                    address[0], to_text(to_masklen(address[1]))
                )
        obj = {
            "name": item,
            "ipv4": ipv4,
            "ipv6": parse_config_argument(configobj, item, "ipv6 address"),
            "state": "present",
        }
        instances.append(obj)
    return instances


def map_params_to_obj(module):
    obj = []
    aggregate = module.params.get("aggregate")
    if aggregate:
        for item in aggregate:
            for key in item:
                if item.get(key) is None:
                    item[key] = module.params[key]
            validate_param_values(module, item, item)
            obj.append(item.copy())
    else:
        obj.append(
            {
                "name": module.params["name"],
                "ipv4": module.params["ipv4"],
                "ipv6": module.params["ipv6"],
                "state": module.params["state"],
            }
        )
        validate_param_values(module, obj)
    return obj


def main():
    """ main entry point for module execution
    """
    element_spec = dict(
        name=dict(),
        ipv4=dict(),
        ipv6=dict(),
        state=dict(default="present", choices=["present", "absent"]),
    )
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec["name"] = dict(required=True)
    # remove default in aggregate spec, to handle common arguments
    remove_default_spec(aggregate_spec)
    argument_spec = dict(
        aggregate=dict(type="list", elements="dict", options=aggregate_spec)
    )
    argument_spec.update(element_spec)
    argument_spec.update(ios_argument_spec)
    required_one_of = [["name", "aggregate"]]
    mutually_exclusive = [["name", "aggregate"]]
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    warnings = list()
    result = {"changed": False}
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands((want, have), module)
    result["commands"] = commands
    if commands:
        if not module.check_mode:
            resp = load_config(module, commands)
            warnings.extend(out for out in resp if out)
        result["changed"] = True
    if warnings:
        result["warnings"] = warnings
    module.exit_json(**result)


if __name__ == "__main__":
    main()
