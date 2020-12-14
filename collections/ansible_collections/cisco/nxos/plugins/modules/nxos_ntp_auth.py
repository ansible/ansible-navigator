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
module: nxos_ntp_auth
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Manages NTP authentication.
description:
- Manages NTP authentication.
version_added: 1.0.0
author:
- Jason Edelman (@jedelman8)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- If C(state=absent), the module will remove the given key configuration if it exists.
- If C(state=absent) and C(authentication=on), authentication will be turned off.
options:
  key_id:
    description:
    - Authentication key identifier (numeric).
    type: str
  md5string:
    description:
    - MD5 String.
    type: str
  auth_type:
    description:
    - Whether the given md5string is in cleartext or has been encrypted. If in cleartext,
      the device will encrypt it before storing it.
    default: text
    choices:
    - text
    - encrypt
    type: str
  trusted_key:
    description:
    - Whether the given key is required to be supplied by a time source for the device
      to synchronize to the time source.
    choices:
    - 'false'
    - 'true'
    default: 'false'
    type: str
  authentication:
    description:
    - Turns NTP authentication on or off.
    choices:
    - "on"
    - "off"
    type: str
  state:
    description:
    - Manage the state of the resource.
    default: present
    choices:
    - present
    - absent
    type: str
"""

EXAMPLES = """
# Basic NTP authentication configuration
- cisco.nxos.nxos_ntp_auth:
    key_id: 32
    md5string: hello
    auth_type: text
"""

RETURN = """
commands:
    description: command sent to the device
    returned: always
    type: list
    sample: ["ntp authentication-key 32 md5 helloWorld 0", "ntp trusted-key 32"]
"""


import re

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    load_config,
    run_commands,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule


def execute_show_command(command, module):
    if "show run" not in command:
        command = {"command": command, "output": "json"}
    else:
        command = {"command": command, "output": "text"}

    return run_commands(module, [command])


def flatten_list(command_lists):
    flat_command_list = []
    for command in command_lists:
        if isinstance(command, list):
            flat_command_list.extend(command)
        else:
            flat_command_list.append(command)
    return flat_command_list


def get_ntp_auth(module):
    command = "show ntp authentication-status"

    body = execute_show_command(command, module)[0]
    ntp_auth_str = body["authentication"]

    if "enabled" in ntp_auth_str:
        ntp_auth = True
    else:
        ntp_auth = False

    return ntp_auth


def get_ntp_trusted_key(module):
    trusted_key_list = []
    command = "show run | inc ntp.trusted-key"

    trusted_key_str = execute_show_command(command, module)[0]
    if trusted_key_str:
        trusted_keys = trusted_key_str.splitlines()

    else:
        trusted_keys = []

    for line in trusted_keys:
        if line:
            trusted_key_list.append(str(line.split()[2]))

    return trusted_key_list


def get_ntp_auth_key(key_id, module):
    authentication_key = {}
    command = "show run | inc ntp.authentication-key.{0}".format(key_id)
    auth_regex = (
        r".*ntp\sauthentication-key\s(?P<key_id>\d+)\s"
        r"md5\s(?P<md5string>\S+)\s(?P<atype>\S+).*"
    )

    body = execute_show_command(command, module)[0]

    try:
        match_authentication = re.match(auth_regex, body, re.DOTALL)
        group_authentication = match_authentication.groupdict()
        authentication_key["key_id"] = group_authentication["key_id"]
        authentication_key["md5string"] = group_authentication["md5string"]
        if group_authentication["atype"] == "7":
            authentication_key["auth_type"] = "encrypt"
        else:
            authentication_key["auth_type"] = "text"
    except (AttributeError, TypeError):
        authentication_key = {}

    return authentication_key


def get_ntp_auth_info(key_id, module):
    auth_info = get_ntp_auth_key(key_id, module)
    trusted_key_list = get_ntp_trusted_key(module)
    auth_power = get_ntp_auth(module)

    if key_id in trusted_key_list:
        auth_info["trusted_key"] = "true"
    else:
        auth_info["trusted_key"] = "false"

    if auth_power:
        auth_info["authentication"] = "on"
    else:
        auth_info["authentication"] = "off"

    return auth_info


def auth_type_to_num(auth_type):
    if auth_type == "encrypt":
        return "7"
    else:
        return "0"


def set_ntp_auth_key(
    key_id, md5string, auth_type, trusted_key, authentication
):
    ntp_auth_cmds = []
    if key_id and md5string:
        auth_type_num = auth_type_to_num(auth_type)
        ntp_auth_cmds.append(
            "ntp authentication-key {0} md5 {1} {2}".format(
                key_id, md5string, auth_type_num
            )
        )

    if trusted_key == "true":
        ntp_auth_cmds.append("ntp trusted-key {0}".format(key_id))
    elif trusted_key == "false":
        ntp_auth_cmds.append("no ntp trusted-key {0}".format(key_id))

    if authentication == "on":
        ntp_auth_cmds.append("ntp authenticate")
    elif authentication == "off":
        ntp_auth_cmds.append("no ntp authenticate")

    return ntp_auth_cmds


def remove_ntp_auth_key(
    key_id, md5string, auth_type, trusted_key, authentication
):
    auth_remove_cmds = []
    if key_id:
        auth_type_num = auth_type_to_num(auth_type)
        auth_remove_cmds.append(
            "no ntp authentication-key {0} md5 {1} {2}".format(
                key_id, md5string, auth_type_num
            )
        )

    if authentication:
        auth_remove_cmds.append("no ntp authenticate")
    return auth_remove_cmds


def main():
    argument_spec = dict(
        key_id=dict(type="str"),
        md5string=dict(type="str"),
        auth_type=dict(choices=["text", "encrypt"], default="text"),
        trusted_key=dict(choices=["true", "false"], default="false"),
        authentication=dict(choices=["on", "off"]),
        state=dict(choices=["absent", "present"], default="present"),
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()

    key_id = module.params["key_id"]
    md5string = module.params["md5string"]
    auth_type = module.params["auth_type"]
    trusted_key = module.params["trusted_key"]
    authentication = module.params["authentication"]
    state = module.params["state"]

    if key_id:
        if not trusted_key and not md5string:
            module.fail_json(msg="trusted_key or md5string MUST be specified")

    args = dict(
        key_id=key_id,
        md5string=md5string,
        auth_type=auth_type,
        trusted_key=trusted_key,
        authentication=authentication,
    )

    changed = False
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    existing = get_ntp_auth_info(key_id, module)
    end_state = existing

    delta = dict(set(proposed.items()).difference(existing.items()))

    commands = []
    if state == "present":
        if delta:
            command = set_ntp_auth_key(
                key_id,
                md5string,
                delta.get("auth_type"),
                delta.get("trusted_key"),
                delta.get("authentication"),
            )
            if command:
                commands.append(command)
    elif state == "absent":
        auth_toggle = None
        if existing.get("authentication") == "on":
            auth_toggle = True
        if not existing.get("key_id"):
            key_id = None
        command = remove_ntp_auth_key(
            key_id, md5string, auth_type, trusted_key, auth_toggle
        )
        if command:
            commands.append(command)

    cmds = flatten_list(commands)
    if cmds:
        if module.check_mode:
            module.exit_json(changed=True, commands=cmds)
        else:
            load_config(module, cmds)
            end_state = get_ntp_auth_info(key_id, module)
            delta = dict(set(end_state.items()).difference(existing.items()))
            if delta or (len(existing) != len(end_state)):
                changed = True
            if "configure" in cmds:
                cmds.pop(0)

    results = {}
    results["proposed"] = proposed
    results["existing"] = existing
    results["updates"] = cmds
    results["changed"] = changed
    results["warnings"] = warnings
    results["end_state"] = end_state

    module.exit_json(**results)


if __name__ == "__main__":
    main()
