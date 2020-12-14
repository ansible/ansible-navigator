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
module: ios_banner
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: Manage multiline banners on Cisco IOS devices
description:
- This will configure both login and motd banners on remote devices running Cisco
  IOS.  It allows playbooks to add or remote banner text from the active running configuration.
version_added: 1.0.0
extends_documentation_fragment:
- cisco.ios.ios
notes:
- Tested against IOS 15.6
options:
  banner:
    description:
    - Specifies which banner should be configured on the remote device. In Ansible
      2.4 and earlier only I(login) and I(motd) were supported.
    required: true
    choices:
    - login
    - motd
    - exec
    - incoming
    - slip-ppp
    type: str
  text:
    description:
    - The banner text that should be present in the remote device running configuration.  This
      argument accepts a multiline string, with no empty lines. Requires I(state=present).
    type: str
  state:
    description:
    - Specifies whether or not the configuration is present in the current devices
      active running configuration.
    default: present
    type: str
    choices:
    - present
    - absent
"""
EXAMPLES = """
- name: configure the login banner
  cisco.ios.ios_banner:
    banner: login
    text: |
      this is my login banner
      that contains a multiline
      string
    state: present

- name: remove the motd banner
  cisco.ios.ios_banner:
    banner: motd
    state: absent

- name: Configure banner from file
  cisco.ios.ios_banner:
    banner: motd
    text: "{{ lookup('file', './config_partial/raw_banner.cfg') }}"
    state: present
"""
RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - banner login
    - this is my login banner
    - that contains a multiline
    - string
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    get_config,
    load_config,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    ios_argument_spec,
)
from re import search, M


def map_obj_to_commands(updates, module):
    commands = list()
    want, have = updates
    state = module.params["state"]
    if state == "absent" and "text" in have.keys() and have["text"]:
        commands.append("no banner %s" % module.params["banner"])
    elif state == "present":
        if want["text"] and (want["text"] != have.get("text")):
            banner_cmd = "banner %s" % module.params["banner"]
            banner_cmd += " @\n"
            banner_cmd += want["text"].strip("\n")
            banner_cmd += "\n@"
            commands.append(banner_cmd)
    return commands


def map_config_to_obj(module):
    """
    This function gets the banner config without stripping any whitespaces,
    and then fetches the required banner from it.
    :param module:
    :return: banner config dict object.
    """
    out = get_config(
        module, flags="| begin banner %s" % module.params["banner"]
    )
    if out:
        regex = "banner " + module.params["banner"] + " ^C\n"
        if search("banner " + module.params["banner"], out, M):
            output = str((out.split(regex))[1].split("^C\n")[0])
        else:
            output = None
    else:
        output = None
    obj = {"banner": module.params["banner"], "state": "absent"}
    if output:
        obj["text"] = output
        obj["state"] = "present"
    return obj


def map_params_to_obj(module):
    text = module.params["text"]
    return {
        "banner": module.params["banner"],
        "text": text,
        "state": module.params["state"],
    }


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        banner=dict(
            required=True,
            choices=["login", "motd", "exec", "incoming", "slip-ppp"],
        ),
        text=dict(),
        state=dict(default="present", choices=["present", "absent"]),
    )
    argument_spec.update(ios_argument_spec)
    required_if = [("state", "present", ("text",))]
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True,
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
        if not module.check_mode:
            load_config(module, commands)
        result["changed"] = True
    module.exit_json(**result)


if __name__ == "__main__":
    main()
