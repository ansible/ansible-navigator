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
module: nxos_igmp
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Manages IGMP global configuration.
description:
- Manages IGMP global configuration configuration settings.
version_added: 1.0.0
author:
- Jason Edelman (@jedelman8)
- Gabriele Gerbino (@GGabriele)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- When C(state=default), all supported params will be reset to a default state.
- If restart is set to true with other params set, the restart will happen last, i.e.
  after the configuration takes place.
options:
  flush_routes:
    description:
    - Removes routes when the IGMP process is restarted. By default, routes are not
      flushed.
    type: bool
  enforce_rtr_alert:
    description:
    - Enables or disables the enforce router alert option check for IGMPv2 and IGMPv3
      packets.
    type: bool
  restart:
    description:
    - Restarts the igmp process (using an exec config command).
    type: bool
  state:
    description:
    - Manages desired state of the resource.
    default: present
    choices:
    - present
    - default
    type: str
"""
EXAMPLES = """
- name: Default igmp global params (all params except restart)
  cisco.nxos.nxos_igmp:
    state: default

- name: Ensure the following igmp global config exists on the device
  cisco.nxos.nxos_igmp:
    flush_routes: true
    enforce_rtr_alert: true

- name: Restart the igmp process
  cisco.nxos.nxos_igmp:
    restart: true
"""

RETURN = """
updates:
    description: commands sent to the device
    returned: always
    type: list
    sample: ["ip igmp flush-routes"]
"""
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    load_config,
    run_commands,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def get_current(module):
    output = run_commands(
        module, {"command": "show running-config", "output": "text"}
    )
    return {
        "flush_routes": "ip igmp flush-routes" in output[0],
        "enforce_rtr_alert": "ip igmp enforce-router-alert" in output[0],
    }


def get_desired(module):
    return {
        "flush_routes": module.params["flush_routes"],
        "enforce_rtr_alert": module.params["enforce_rtr_alert"],
    }


def main():
    argument_spec = dict(
        flush_routes=dict(type="bool"),
        enforce_rtr_alert=dict(type="bool"),
        restart=dict(type="bool", default=False),
        state=dict(choices=["present", "default"], default="present"),
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()

    current = get_current(module)
    desired = get_desired(module)

    state = module.params["state"]

    commands = list()

    if state == "default":
        if current["flush_routes"]:
            commands.append("no ip igmp flush-routes")
        if current["enforce_rtr_alert"]:
            commands.append("no ip igmp enforce-router-alert")

    elif state == "present":
        ldict = {
            "flush_routes": "flush-routes",
            "enforce_rtr_alert": "enforce-router-alert",
        }
        for arg in ["flush_routes", "enforce_rtr_alert"]:
            if desired[arg] and not current[arg]:
                commands.append("ip igmp {0}".format(ldict.get(arg)))
            elif current[arg] and not desired[arg]:
                commands.append("no ip igmp {0}".format(ldict.get(arg)))

    result = {"changed": False, "updates": commands, "warnings": warnings}

    if commands:
        if not module.check_mode:
            load_config(module, commands)
        result["changed"] = True

    if module.params["restart"]:
        cmd = {"command": "restart igmp", "output": "text"}
        run_commands(module, cmd)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
