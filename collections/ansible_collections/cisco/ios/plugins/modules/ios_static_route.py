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
module: ios_static_route
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage static IP routes
  on Cisco IOS network devices
description:
- This module provides declarative management of static IP routes on Cisco IOS network
  devices.
version_added: 1.0.0
deprecated:
  alternative: ios_static_routes
  why: Newer and updated modules released with more functionality.
  removed_at_date: '2022-06-01'
notes:
- Tested against IOS 15.6
options:
  prefix:
    description:
    - Network prefix of the static route.
    type: str
  mask:
    description:
    - Network prefix mask of the static route.
    type: str
  next_hop:
    description:
    - Next hop IP of the static route.
    type: str
  vrf:
    description:
    - VRF of the static route.
    type: str
  interface:
    description:
    - Interface of the static route.
    type: str
  name:
    description:
    - Name of the static route
    type: str
    aliases:
    - description
  admin_distance:
    description:
    - Admin distance of the static route.
    type: str
  tag:
    description:
    - Set tag of the static route.
    type: str
  track:
    description:
    - Tracked item to depend on for the static route.
    type: str
  aggregate:
    description: List of static route definitions.
    type: list
    elements: dict
    suboptions:
      prefix:
        description:
        - Network prefix of the static route.
        type: str
        required: true
      mask:
        description:
        - Network prefix mask of the static route.
        type: str
      next_hop:
        description:
        - Next hop IP of the static route.
        type: str
      vrf:
        description:
        - VRF of the static route.
        type: str
      interface:
        description:
        - Interface of the static route.
        type: str
      name:
        description:
        - Name of the static route
        aliases:
        - description
        type: str
      admin_distance:
        description:
        - Admin distance of the static route.
        type: str
      tag:
        description:
        - Set tag of the static route.
        type: str
      track:
        description:
        - Tracked item to depend on for the static route.
        type: str
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
- cisco.ios.ios
"""
EXAMPLES = """
- name: configure static route
  cisco.ios.ios_static_route:
    prefix: 192.168.2.0
    mask: 255.255.255.0
    next_hop: 10.0.0.1

- name: configure black hole in vrf blue depending on tracked item 10
  cisco.ios.ios_static_route:
    prefix: 192.168.2.0
    mask: 255.255.255.0
    vrf: blue
    interface: null0
    track: 10

- name: configure ultimate route with name and tag
  cisco.ios.ios_static_route:
    prefix: 192.168.2.0
    mask: 255.255.255.0
    interface: GigabitEthernet1
    name: hello world
    tag: 100

- name: remove configuration
  cisco.ios.ios_static_route:
    prefix: 192.168.2.0
    mask: 255.255.255.0
    next_hop: 10.0.0.1
    state: absent

- name: Add static route aggregates
  cisco.ios.ios_static_route:
    aggregate:
    - {prefix: 172.16.32.0, mask: 255.255.255.0, next_hop: 10.0.0.8}
    - {prefix: 172.16.33.0, mask: 255.255.255.0, next_hop: 10.0.0.8}

- name: Remove static route aggregates
  cisco.ios.ios_static_route:
    aggregate:
    - {prefix: 172.16.32.0, mask: 255.255.255.0, next_hop: 10.0.0.8}
    - {prefix: 172.16.33.0, mask: 255.255.255.0, next_hop: 10.0.0.8}
    state: absent
"""
RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - ip route 192.168.2.0 255.255.255.0 10.0.0.1
"""
from copy import deepcopy
from re import findall
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_default_spec,
    validate_ip_address,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    get_config,
    load_config,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    ios_argument_spec,
)


def map_obj_to_commands(want, have):
    commands = list()
    for w in want:
        state = w["state"]
        del w["state"]
        # Try to match an existing config with the desired config
        for h in have:
            # Try to match an existing config with the desired config
            if not w.get("admin_distance") and h.get("admin_distance"):
                del h["admin_distance"]
            diff = list(set(w.items()) ^ set(h.items()))
            if not diff:
                break
            # Try to match an existing config with the desired config
            if (
                len(diff) == 2
                and diff[0][0] == diff[1][0] == "name"
                and (not w["name"] or h["name"].startswith(w["name"]))
            ):
                break
        # If no matches found, clear `h`
        else:
            h = None
        command = "ip route"
        prefix = w["prefix"]
        mask = w["mask"]
        vrf = w.get("vrf")
        if vrf:
            command = " ".join((command, "vrf", vrf, prefix, mask))
        else:
            command = " ".join((command, prefix, mask))
        for key in [
            "interface",
            "next_hop",
            "admin_distance",
            "tag",
            "name",
            "track",
        ]:
            if w.get(key):
                if key == "name" and len(w.get(key).split()) > 1:
                    command = " ".join((command, key, '"%s"' % w.get(key)))
                elif key in ("name", "tag", "track"):
                    command = " ".join((command, key, w.get(key)))
                else:
                    command = " ".join((command, w.get(key)))
        if state == "absent" and h:
            commands.append("no %s" % command)
        elif state == "present" and not h:
            commands.append(command)
    return commands


def map_config_to_obj(module):
    obj = []
    out = get_config(module, flags="| include ip route")
    for line in out.splitlines():
        # Split by whitespace but do not split quotes, needed for name parameter
        splitted_line = findall('[^"\\s]\\S*|".+?"', line)
        if splitted_line[2] == "vrf":
            route = {"vrf": splitted_line[3]}
            del splitted_line[:4]  # Removes the words ip route vrf vrf_name
        else:
            route = {}
            del splitted_line[:2]  # Removes the words ip route
        prefix = splitted_line[0]
        mask = splitted_line[1]
        route.update({"prefix": prefix, "mask": mask, "admin_distance": "1"})
        next_word = None
        for word in splitted_line[2:]:
            if next_word:
                route[next_word] = word.strip('"')
                next_word = None
            elif validate_ip_address(word):
                route.update(next_hop=word)
            elif word.isdigit():
                route.update(admin_distance=word)
            elif word in ("tag", "name", "track"):
                next_word = word
            else:
                route.update(interface=word)
        obj.append(route)
    return obj


def map_params_to_obj(module, required_together=None):
    keys = [
        "prefix",
        "mask",
        "state",
        "next_hop",
        "vrf",
        "interface",
        "name",
        "admin_distance",
        "track",
        "tag",
    ]
    obj = []
    aggregate = module.params.get("aggregate")
    if aggregate:
        for item in aggregate:
            route = item.copy()
            for key in keys:
                if route.get(key) is None:
                    route[key] = module.params.get(key)
            route = dict((k, v) for k, v in route.items() if v is not None)
            module._check_required_together(required_together, route)
            obj.append(route)
    else:
        module._check_required_together(required_together, module.params)
        route = dict()
        for key in keys:
            if module.params.get(key) is not None:
                route[key] = module.params.get(key)
        obj.append(route)
    return obj


def main():
    """ main entry point for module execution
    """
    element_spec = dict(
        prefix=dict(type="str"),
        mask=dict(type="str"),
        next_hop=dict(type="str"),
        vrf=dict(type="str"),
        interface=dict(type="str"),
        name=dict(type="str", aliases=["description"]),
        admin_distance=dict(type="str"),
        track=dict(type="str"),
        tag=dict(type="str"),
        state=dict(default="present", choices=["present", "absent"]),
    )
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec["prefix"] = dict(required=True)
    # remove default in aggregate spec, to handle common arguments
    remove_default_spec(aggregate_spec)
    argument_spec = dict(
        aggregate=dict(type="list", elements="dict", options=aggregate_spec)
    )
    argument_spec.update(element_spec)
    argument_spec.update(ios_argument_spec)
    required_one_of = [["aggregate", "prefix"]]
    required_together = [["prefix", "mask"]]
    mutually_exclusive = [["aggregate", "prefix"]]
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    warnings = list()
    result = {"changed": False}
    if warnings:
        result["warnings"] = warnings
    want = map_params_to_obj(module, required_together=required_together)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands(want, have)
    result["commands"] = commands
    if commands:
        if not module.check_mode:
            load_config(module, commands)
        result["changed"] = True
    module.exit_json(**result)


if __name__ == "__main__":
    main()
