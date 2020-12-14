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
module: ios_lldp
author: Ganesh Nalawade (@ganeshrn)
short_description: Manage LLDP configuration on Cisco IOS network devices.
description:
- This module provides declarative management of LLDP service on Cisco IOS network
  devices.
version_added: 1.0.0
notes:
- Tested against IOS 15.2
options:
  state:
    description:
    - State of the LLDP configuration. If value is I(present) lldp will be enabled
      else if it is I(absent) it will be disabled.
    default: present
    choices:
    - present
    - absent
    - enabled
    - disabled
    type: str
extends_documentation_fragment:
- cisco.ios.ios
"""
EXAMPLES = """
- name: Enable LLDP service
  cisco.ios.ios_lldp:
    state: present

- name: Disable LLDP service
  cisco.ios.ios_lldp:
    state: absent
"""
RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - lldp run
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    load_config,
    run_commands,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    ios_argument_spec,
)


def has_lldp(module):
    output = run_commands(module, ["show lldp"])
    is_lldp_enable = False
    if len(output) > 0 and "LLDP is not enabled" not in output[0]:
        is_lldp_enable = True
    return is_lldp_enable


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        state=dict(
            default="present",
            choices=["present", "absent", "enabled", "disabled"],
        )
    )
    argument_spec.update(ios_argument_spec)
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
        commands.append("no lldp run")
    elif module.params["state"] == "present" and not HAS_LLDP:
        commands.append("lldp run")
    result["commands"] = commands
    if commands:
        if not module.check_mode:
            load_config(module, commands)
        result["changed"] = True
    module.exit_json(**result)


if __name__ == "__main__":
    main()
