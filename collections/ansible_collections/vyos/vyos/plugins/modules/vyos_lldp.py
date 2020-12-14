#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
#
# This file is part of Ansible by Red Hat
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
module: vyos_lldp
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage LLDP configuration
  on VyOS network devices
description:
- This module provides declarative management of LLDP service on VyOS network devices.
version_added: 1.0.0
deprecated:
  alternative: vyos_lldp_global
  why: Updated modules released with more functionality.
  removed_at_date: '2022-06-01'
notes:
- Tested against VYOS 1.1.7
options:
  interfaces:
    description:
    - Name of the interfaces.
    type: list
    elements: str
  state:
    description:
    - State of the link aggregation group.
    default: present
    choices:
    - present
    - absent
    - enabled
    - disabled
    type: str
extends_documentation_fragment:
- vyos.vyos.vyos


"""

EXAMPLES = """
- name: Enable LLDP service
  vyos.vyos.vyos_lldp:
    state: present

- name: Disable LLDP service
  vyos.vyos.vyos_lldp:
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - set service lldp
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.vyos import (
    get_config,
    load_config,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.vyos import (
    vyos_argument_spec,
)


def has_lldp(module):
    config = get_config(module).splitlines()

    if "set service 'lldp'" in config or "set service lldp" in config:
        return True
    else:
        return False


def main():
    """main entry point for module execution"""
    argument_spec = dict(
        interfaces=dict(type="list", elements="str"),
        state=dict(
            default="present",
            choices=["present", "absent", "enabled", "disabled"],
        ),
    )

    argument_spec.update(vyos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()

    result = {"changed": False}

    if warnings:
        result["warnings"] = warnings

    HAS_LLDP = has_lldp(module)

    commands = []

    if module.params["state"] == "absent" and HAS_LLDP:
        commands.append("delete service lldp")
    elif module.params["state"] == "present" and not HAS_LLDP:
        commands.append("set service lldp")

    result["commands"] = commands

    if commands:
        commit = not module.check_mode
        load_config(module, commands, commit=commit)
        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
