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
module: nxos_user
extends_documentation_fragment:
- cisco.nxos.nxos
author: Peter Sprygada (@privateip)
short_description: Manage the collection of local users on Nexus devices
description:
- This module provides declarative management of the local usernames configured on
  Cisco Nexus devices.  It allows playbooks to manage either individual usernames
  or the collection of usernames in the current running config.  It also supports
  purging usernames from the configuration that are not explicitly defined.
version_added: 1.0.0
options:
  aggregate:
    description:
    - The set of username objects to be configured on the remote Cisco Nexus device.  The
      list entries can either be the username or a hash of username and properties.  This
      argument is mutually exclusive with the C(name) argument.
    aliases:
    - users
    - collection
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - The username to be configured on the remote Cisco Nexus device.  This argument
          accepts a string value and is mutually exclusive with the C(aggregate) argument.
        type: str
      configured_password:
        description:
        - The password to be configured on the network device. The password needs to be
          provided in cleartext and it will be encrypted on the device. Please note that
          this option is not same as C(provider password).
        type: str
      update_password:
        description:
        - Since passwords are encrypted in the device running config, this argument will
          instruct the module when to change the password.  When set to C(always), the
          password will always be updated in the device and when set to C(on_create) the
          password will be updated only if the username is created.
        choices:
        - on_create
        - always
        type: str
      roles:
        description:
        - The C(role) argument configures the role for the username in the device running
          configuration.  The argument accepts a string value defining the role name.  This
          argument does not check if the role has been configured on the device.
        aliases:
        - role
        type: list
        elements: str
      sshkey:
        description:
        - The C(sshkey) argument defines the SSH public key to configure for the username.  This
          argument accepts a valid SSH key value.
        type: str
      state:
        description:
        - The C(state) argument configures the state of the username definition as it
         relates to the device operational configuration.  When set to I(present), the
         username(s) should be configured in the device active configuration and when
         set to I(absent) the username(s) should not be in the device active configuration
        choices:
        - present
        - absent
        type: str
  name:
    description:
    - The username to be configured on the remote Cisco Nexus device.  This argument
      accepts a string value and is mutually exclusive with the C(aggregate) argument.
    type: str
  configured_password:
    description:
    - The password to be configured on the network device. The password needs to be
      provided in cleartext and it will be encrypted on the device. Please note that
      this option is not same as C(provider password).
    type: str
  update_password:
    description:
    - Since passwords are encrypted in the device running config, this argument will
      instruct the module when to change the password.  When set to C(always), the
      password will always be updated in the device and when set to C(on_create) the
      password will be updated only if the username is created.
    default: always
    choices:
    - on_create
    - always
    type: str
  roles:
    description:
    - The C(role) argument configures the role for the username in the device running
      configuration.  The argument accepts a string value defining the role name.  This
      argument does not check if the role has been configured on the device.
    aliases:
    - role
    type: list
    elements: str
  sshkey:
    description:
    - The C(sshkey) argument defines the SSH public key to configure for the username.  This
      argument accepts a valid SSH key value.
    type: str
  purge:
    description:
    - The C(purge) argument instructs the module to consider the resource definition
      absolute.  It will remove any previously configured usernames on the device
      with the exception of the `admin` user which cannot be deleted per nxos constraints.
    type: bool
    default: no
  state:
    description:
    - The C(state) argument configures the state of the username definition as it
      relates to the device operational configuration.  When set to I(present), the
      username(s) should be configured in the device active configuration and when
      set to I(absent) the username(s) should not be in the device active configuration
    default: present
    choices:
    - present
    - absent
    type: str
"""

EXAMPLES = """
- name: create a new user
  cisco.nxos.nxos_user:
    name: ansible
    sshkey: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    state: present

- name: remove all users except admin
  cisco.nxos.nxos_user:
    purge: yes

- name: set multiple users role
  cisco.nxos.nxos_user:
    aggregate:
    - name: netop
    - name: netend
    role: network-operator
  state: present
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - name ansible
    - name ansible password password
"""
import re

from copy import deepcopy
from functools import partial

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    run_commands,
    load_config,
    get_config,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_default_spec,
    to_list,
)

BUILTIN_ROLES = [
    "network-admin",
    "network-operator",
    "vdc-admin",
    "vdc-operator",
    "priv-15",
    "priv-14",
    "priv-13",
    "priv-12",
    "priv-11",
    "priv-10",
    "priv-9",
    "priv-8",
    "priv-7",
    "priv-6",
    "priv-5",
    "priv-4",
    "priv-3",
    "priv-2",
    "priv-1",
    "priv-0",
]


def get_custom_roles(module):
    return re.findall(
        r"^role name (\S+)",
        get_config(module, flags=["| include '^role name'"]),
        re.M,
    )


def validate_roles(value, module):
    valid_roles = BUILTIN_ROLES + get_custom_roles(module)
    for item in value:
        if item not in valid_roles:
            module.fail_json(msg="invalid role specified")


def map_obj_to_commands(updates, module):
    commands = list()
    update_password = module.params["update_password"]

    for update in updates:
        want, have = update

        def needs_update(x):
            return want.get(x) and (want.get(x) != have.get(x))

        def add(x):
            return commands.append("username %s %s" % (want["name"], x))

        def remove(x):
            return commands.append("no username %s %s" % (want["name"], x))

        def configure_roles():
            if want["roles"]:
                if have:
                    for item in set(have["roles"]).difference(want["roles"]):
                        remove("role %s" % item)

                    for item in set(want["roles"]).difference(have["roles"]):
                        add("role %s" % item)
                else:
                    for item in want["roles"]:
                        add("role %s" % item)

                return True
            return False

        if want["state"] == "absent":
            commands.append("no username %s" % want["name"])
            continue

        roles_configured = False
        if want["state"] == "present" and not have:
            roles_configured = configure_roles()
            if not roles_configured:
                commands.append("username %s" % want["name"])

        if needs_update("configured_password"):
            if update_password == "always" or not have:
                add("password %s" % want["configured_password"])

        if needs_update("sshkey"):
            add("sshkey %s" % want["sshkey"])

        if not roles_configured:
            configure_roles()

    return commands


def parse_password(data):
    if not data.get("remote_login"):
        return "<PASSWORD>"


def parse_roles(data):
    configured_roles = None
    if "TABLE_role" in data:
        configured_roles = data.get("TABLE_role")["ROW_role"]

    roles = list()
    if configured_roles:
        for item in to_list(configured_roles):
            roles.append(item["role"])
    return roles


def map_config_to_obj(module):
    out = run_commands(
        module, [{"command": "show user-account", "output": "json"}]
    )
    data = out[0]

    objects = list()

    for item in to_list(data["TABLE_template"]["ROW_template"]):
        objects.append(
            {
                "name": item["usr_name"],
                "configured_password": parse_password(item),
                "sshkey": item.get("sshkey_info"),
                "roles": parse_roles(item),
                "state": "present",
            }
        )
    return objects


def get_param_value(key, item, module):
    # if key doesn't exist in the item, get it from module.params
    if not item.get(key):
        value = module.params[key]

    # if key does exist, do a type check on it to validate it
    else:
        value_type = module.argument_spec[key].get("type", "str")
        type_checker = module._CHECK_ARGUMENT_TYPES_DISPATCHER[value_type]
        type_checker(item[key])
        value = item[key]

    return value


def map_params_to_obj(module):
    aggregate = module.params["aggregate"]
    if not aggregate:
        if not module.params["name"] and module.params["purge"]:
            return list()
        elif not module.params["name"]:
            module.fail_json(msg="username is required")
        else:
            collection = [{"name": module.params["name"]}]
    else:
        collection = list()
        for item in aggregate:
            if not isinstance(item, dict):
                collection.append({"name": item})
            elif "name" not in item:
                module.fail_json(msg="name is required")
            else:
                collection.append(item)

    objects = list()

    for item in collection:
        get_value = partial(get_param_value, item=item, module=module)
        item.update(
            {
                "configured_password": get_value("configured_password"),
                "sshkey": get_value("sshkey"),
                "roles": get_value("roles"),
                "state": get_value("state"),
            }
        )

        for key, value in iteritems(item):
            if value:
                # validate the param value (if validator func exists)
                validator = globals().get("validate_%s" % key)
                if all((value, validator)):
                    validator(value, module)

        objects.append(item)

    return objects


def update_objects(want, have):
    updates = list()
    for entry in want:
        item = next((i for i in have if i["name"] == entry["name"]), None)
        if all((item is None, entry["state"] == "present")):
            updates.append((entry, {}))
        elif item:
            for key, value in iteritems(entry):
                if value and value != item[key]:
                    updates.append((entry, item))
    return updates


def main():
    """ main entry point for module execution
    """
    element_spec = dict(
        name=dict(),
        configured_password=dict(no_log=True),
        update_password=dict(
            default="always", choices=["on_create", "always"]
        ),
        roles=dict(type="list", aliases=["role"], elements="str"),
        sshkey=dict(),
        state=dict(default="present", choices=["present", "absent"]),
    )

    aggregate_spec = deepcopy(element_spec)

    # remove default in aggregate spec, to handle common arguments
    remove_default_spec(aggregate_spec)

    argument_spec = dict(
        aggregate=dict(
            type="list",
            elements="dict",
            options=aggregate_spec,
            aliases=["collection", "users"],
        ),
        purge=dict(type="bool", default=False),
    )

    argument_spec.update(element_spec)
    argument_spec.update(nxos_argument_spec)

    mutually_exclusive = [("name", "aggregate")]

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    result = {"changed": False, "warnings": []}

    want = map_params_to_obj(module)
    have = map_config_to_obj(module)

    commands = map_obj_to_commands(update_objects(want, have), module)

    if module.params["purge"]:
        want_users = [x["name"] for x in want]
        have_users = [x["name"] for x in have]
        for item in set(have_users).difference(want_users):
            if item != "admin":
                item = item.replace("\\", "\\\\")
                commands.append("no username %s" % item)

    result["commands"] = commands

    # the nxos cli prevents this by rule so capture it and display
    # a nice failure message
    if "no username admin" in commands:
        module.fail_json(msg="cannot delete the `admin` account")

    if commands:
        if not module.check_mode:
            responses = load_config(module, commands)
            for resp in responses:
                if resp.lower().startswith("wrong password"):
                    module.fail_json(msg=resp)
                else:
                    result["warnings"].extend(
                        [
                            x[9:]
                            for x in resp.splitlines()
                            if x.startswith("WARNING: ")
                        ]
                    )

        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
