#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: eos_static_route
author: Trishna Guha (@trishnaguha)
short_description: (deprecated, removed after 2022-06-01) Manage static IP
  routes on Arista EOS network devices
description:
- This module provides declarative management of static IP routes on Arista EOS network
  devices.
version_added: 1.0.0
deprecated:
  alternative: eos_static_routes
  why: Updated modules with more functionality
  removed_at_date: '2022-06-01'
notes:
- Tested against EOS 4.15
options:
  address:
    description:
    - Network address with prefix of the static route.
    aliases:
    - prefix
    type: str
  next_hop:
    description:
    - Next hop IP of the static route.
    type: str
  vrf:
    description:
    - VRF for static route.
    default: default
    type: str
  admin_distance:
    description:
    - Admin distance of the static route.
    default: 1
    type: int
  aggregate:
    description: List of static route definitions
    type: list
    elements: dict
    suboptions:
      address:
        description:
        - Network address with prefix of the static route.
        aliases:
        - prefix
        type: str
        required: True
      next_hop:
        description:
        - Next hop IP of the static route.
        type: str
      vrf:
        description:
        - VRF for static route.
        default: default
        type: str
      admin_distance:
        description:
        - Admin distance of the static route.
        type: int
      state:
        description:
        - State of the static route configuration.
        choices:
        - present
        - absent
        type: str
  state:
    description:
    - State of the static route configuration.
    default: present
    choices:
    - present
    - absent
    type: str
extends_documentation_fragment:
- arista.eos.eos

"""

EXAMPLES = """
- name: configure static route
  arista.eos.eos_static_route:
    address: 10.0.2.0/24
    next_hop: 10.8.38.1
    admin_distance: 2
- name: delete static route
  arista.eos.eos_static_route:
    address: 10.0.2.0/24
    next_hop: 10.8.38.1
    state: absent
- name: configure static routes using aggregate
  arista.eos.eos_static_route:
    aggregate:
    - {address: 10.0.1.0/24, next_hop: 10.8.38.1}
    - {address: 10.0.3.0/24, next_hop: 10.8.38.1}
- name: Delete static route using aggregate
  arista.eos.eos_static_route:
    aggregate:
    - {address: 10.0.1.0/24, next_hop: 10.8.38.1}
    - {address: 10.0.3.0/24, next_hop: 10.8.38.1}
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - ip route 10.0.2.0/24 10.8.38.1 3
    - no ip route 10.0.2.0/24 10.8.38.1
"""

import re

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    is_masklen,
    validate_ip_address,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_default_spec,
    validate_prefix,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.eos import (
    get_config,
    load_config,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.eos import (
    eos_argument_spec,
)


def is_address(value):
    if value:
        address = value.split("/")
        if is_masklen(address[1]) and validate_ip_address(address[0]):
            return True
    return False


def is_hop(value):
    if value:
        if validate_ip_address(value):
            return True
    return False


def map_obj_to_commands(updates, module):
    commands = list()
    want, have = updates

    for w in want:
        address = w["address"]
        next_hop = w["next_hop"]
        admin_distance = w["admin_distance"]
        vrf = w["vrf"]
        state = w["state"]
        del w["state"]

        if state == "absent" and w in have:
            if vrf == "default":
                commands.append("no ip route %s %s" % (address, next_hop))
            else:
                commands.append(
                    "no ip route vrf %s %s %s" % (vrf, address, next_hop)
                )
        elif state == "present" and w not in have:
            if vrf == "default":
                commands.append(
                    "ip route %s %s %d" % (address, next_hop, admin_distance)
                )
            else:
                commands.append(
                    "ip route vrf %s %s %s %d"
                    % (vrf, address, next_hop, admin_distance)
                )

    return commands


def map_params_to_obj(module, required_together=None):
    obj = []

    aggregate = module.params.get("aggregate")
    if aggregate:
        for item in aggregate:
            for key in item:
                if item.get(key) is None:
                    item[key] = module.params[key]

            module._check_required_together(required_together, item)
            d = item.copy()

            obj.append(d)
    else:
        obj.append(
            {
                "address": module.params["address"].strip(),
                "next_hop": module.params["next_hop"].strip(),
                "admin_distance": module.params["admin_distance"],
                "state": module.params["state"],
                "vrf": module.params["vrf"],
            }
        )

    return obj


def map_config_to_obj(module):
    objs = []

    try:
        out = get_config(module, flags=["| include ip.route"])
    except IndexError:
        out = ""
    if out:
        lines = out.splitlines()
        for line in lines:
            obj = {}
            add_match = re.search(r"ip route ([\d\./]+)", line, re.M)
            if add_match:
                obj["vrf"] = "default"
                address = add_match.group(1)
                if is_address(address):
                    obj["address"] = address
                hop_match = re.search(
                    r"ip route {0} ([\d\./]+)".format(address), line, re.M
                )
                if hop_match:
                    hop = hop_match.group(1)
                    if is_hop(hop):
                        obj["next_hop"] = hop
                    dist_match = re.search(
                        r"ip route {0} {1} (\d+)".format(address, hop),
                        line,
                        re.M,
                    )
                    if dist_match:
                        distance = dist_match.group(1)
                        obj["admin_distance"] = int(distance)
                    else:
                        obj["admin_distance"] = 1

            vrf_match = re.search(
                r"ip route vrf ([\w]+) ([\d\./]+)", line, re.M
            )
            if vrf_match:
                vrf = vrf_match.group(1)
                obj["vrf"] = vrf
                address = vrf_match.group(2)
                if is_address(address):
                    obj["address"] = address
                hop_vrf_match = re.search(
                    r"ip route vrf {0} {1} ([\d\./]+)".format(vrf, address),
                    line,
                    re.M,
                )
                if hop_vrf_match:
                    hop = hop_vrf_match.group(1)
                    if is_hop(hop):
                        obj["next_hop"] = hop
                    dist_vrf_match = re.search(
                        r"ip route vrf {0} {1} {2} (\d+)".format(
                            vrf, address, hop
                        ),
                        line,
                        re.M,
                    )
                    if dist_vrf_match:
                        distance = dist_vrf_match.group(1)
                        obj["admin_distance"] = int(distance)
                    else:
                        obj["admin_distance"] = 1

            objs.append(obj)

    return objs


def main():
    """ main entry point for module execution
    """
    element_spec = dict(
        address=dict(type="str", aliases=["prefix"]),
        next_hop=dict(type="str"),
        vrf=dict(type="str", default="default"),
        admin_distance=dict(default=1, type="int"),
        state=dict(default="present", choices=["present", "absent"]),
    )

    aggregate_spec = deepcopy(element_spec)
    aggregate_spec["address"] = dict(required=True, aliases=["prefix"])

    # remove default in aggregate spec, to handle common arguments
    remove_default_spec(aggregate_spec)

    aggregate_spec["vrf"].update(default="default")
    argument_spec = dict(
        aggregate=dict(type="list", elements="dict", options=aggregate_spec)
    )

    argument_spec.update(element_spec)
    argument_spec.update(eos_argument_spec)

    required_one_of = [["aggregate", "address"]]
    required_together = [["address", "next_hop"]]
    mutually_exclusive = [["aggregate", "address"]]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=required_one_of,
        required_together=required_together,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    address = module.params["address"]
    if address is not None:
        prefix = address.split("/")[-1]

    if address and prefix:
        if "/" not in address or not validate_ip_address(
            address.split("/")[0]
        ):
            module.fail_json(
                msg="{0} is not a valid IP address".format(address)
            )

        if not validate_prefix(prefix):
            module.fail_json(
                msg="Length of prefix should be between 0 and 32 bits"
            )

    warnings = list()
    result = {"changed": False}
    if warnings:
        result["warnings"] = warnings

    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands((want, have), module)
    result["commands"] = commands

    if commands:
        commit = not module.check_mode
        response = load_config(module, commands, commit=commit)
        if response.get("diff") and module._diff:
            result["diff"] = {"prepared": response.get("diff")}
        result["session_name"] = response.get("session")
        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
