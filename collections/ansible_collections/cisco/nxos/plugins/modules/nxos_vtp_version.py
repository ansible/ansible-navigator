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
module: nxos_vtp_version
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Manages VTP version configuration.
description:
- Manages VTP version configuration.
version_added: 1.0.0
author:
- Gabriele Gerbino (@GGabriele)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- VTP feature must be active on the device to use this module.
- This module is used to manage only VTP version.
- Use this in combination with M(cisco.nxos.nxos_vtp_password) and M(cisco.nxos.nxos_vtp_version)
  to fully manage VTP operations.
options:
  version:
    description:
    - VTP version number.
    required: true
    choices:
    - '1'
    - '2'
    type: str
"""
EXAMPLES = """
# ENSURE VTP VERSION IS 2
- cisco.nxos.nxos_vtp_version:
    version: 2
    host: '{{ inventory_hostname }}'
    username: '{{ un }}'
    password: '{{ pwd }}'
"""

RETURN = """
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"version": "2"}
existing:
    description:
        - k/v pairs of existing vtp
    returned: always
    type: dict
    sample: {"domain": "testing", "version": "1", "vtp_password": "\"}
end_state:
    description: k/v pairs of vtp after module execution
    returned: always
    type: dict
    sample: {"domain": "testing", "version": "2", "vtp_password": "\"}
updates:
    description: command sent to the device
    returned: always
    type: list
    sample: ["vtp version 2"]
changed:
    description: check to see if a change was made on the device
    returned: always
    type: bool
    sample: true
"""
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    load_config,
    run_commands,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    get_capabilities,
)
from ansible.module_utils.basic import AnsibleModule
import re


def execute_show_command(command, module, output="json"):
    cmds = [{"command": command, "output": output}]
    body = run_commands(module, cmds)
    return body


def flatten_list(command_lists):
    flat_command_list = []
    for command in command_lists:
        if isinstance(command, list):
            flat_command_list.extend(command)
        else:
            flat_command_list.append(command)
    return flat_command_list


def get_vtp_config(module):
    command = "show vtp status"
    body = execute_show_command(command, module, "text")[0]
    vtp_parsed = {}

    if body:
        version_regex = r".*VTP version running\s+:\s+(?P<version>\d).*"
        domain_regex = r".*VTP Domain Name\s+:\s+(?P<domain>\S+).*"

        try:
            match_version = re.match(version_regex, body, re.DOTALL)
            version = match_version.groupdict()["version"]
        except AttributeError:
            version = ""

        try:
            match_domain = re.match(domain_regex, body, re.DOTALL)
            domain = match_domain.groupdict()["domain"]
        except AttributeError:
            domain = ""

        if domain and version:
            vtp_parsed["domain"] = domain
            vtp_parsed["version"] = version
            vtp_parsed["vtp_password"] = get_vtp_password(module)

    return vtp_parsed


def get_vtp_password(module):
    command = "show vtp password"
    output = "json"
    cap = get_capabilities(module)["device_info"]["network_os_model"]
    if re.search(r"Nexus 6", cap):
        output = "text"

    body = execute_show_command(command, module, output)[0]

    if output == "json":
        password = body.get("passwd", "")
    else:
        password = ""
        rp = r"VTP Password: (\S+)"
        mo = re.search(rp, body)
        if mo:
            password = mo.group(1)

    return str(password)


def main():
    argument_spec = dict(
        version=dict(type="str", choices=["1", "2"], required=True)
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()

    version = module.params["version"]

    existing = get_vtp_config(module)
    end_state = existing

    args = dict(version=version)

    changed = False
    proposed = dict((k, v) for k, v in args.items() if v is not None)
    delta = dict(set(proposed.items()).difference(existing.items()))

    commands = []
    if delta:
        commands.append(["vtp version {0}".format(version)])

    cmds = flatten_list(commands)
    if cmds:
        if module.check_mode:
            module.exit_json(changed=True, commands=cmds)
        else:
            changed = True
            load_config(module, cmds)
            end_state = get_vtp_config(module)
            if "configure" in cmds:
                cmds.pop(0)

    results = {}
    results["proposed"] = proposed
    results["existing"] = existing
    results["end_state"] = end_state
    results["updates"] = cmds
    results["changed"] = changed
    results["warnings"] = warnings

    module.exit_json(**results)


if __name__ == "__main__":
    main()
