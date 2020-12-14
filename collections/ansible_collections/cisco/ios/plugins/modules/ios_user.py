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
module: ios_user
author: Trishna Guha (@trishnaguha)
short_description: Manage the aggregate of local users on Cisco IOS device
description:
- This module provides declarative management of the local usernames configured on
  network devices. It allows playbooks to manage either individual usernames or the
  aggregate of usernames in the current running config. It also supports purging usernames
  from the configuration that are not explicitly defined.
version_added: 1.0.0
notes:
- Tested against IOS 15.6
options:
  aggregate:
    description:
    - The set of username objects to be configured on the remote Cisco IOS device.
      The list entries can either be the username or a hash of username and properties.
      This argument is mutually exclusive with the C(name) argument.
    aliases:
    - users
    - collection
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - The username to be configured on the Cisco IOS device. This argument accepts
          a string value and is mutually exclusive with the C(aggregate) argument. Please
          note that this option is not same as C(provider username).
        type: str
        required: true
      configured_password:
        description:
        - The password to be configured on the Cisco IOS device. The password needs to
          be provided in clear and it will be encrypted on the device. Please note that
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
      password_type:
        description:
        - This argument determines whether a 'password' or 'secret' will be configured.
        choices:
        - secret
        - password
        type: str
      hashed_password:
        description:
        - This option allows configuring hashed passwords on Cisco IOS devices.
        type: dict
        suboptions:
          type:
            description:
            - Specifies the type of hash (e.g., 5 for MD5, 8 for PBKDF2, etc.)
            - For this to work, the device needs to support the desired hash type
            type: int
            required: true
          value:
            description:
            - The actual hashed password to be configured on the device
            required: true
            type: str
      privilege:
        description:
        - The C(privilege) argument configures the privilege level of the user when logged
          into the system. This argument accepts integer values in the range of 1 to 15.
        type: int
      view:
        description:
        - Configures the view for the username in the device running configuration. The
          argument accepts a string value defining the view name. This argument does not
          check if the view has been configured on the device.
        aliases:
        - role
        type: str
      sshkey:
        description:
        - Specifies one or more SSH public key(s) to configure for the given username.
        - This argument accepts a valid SSH key value.
        type: list
        elements: str
      nopassword:
        description:
        - Defines the username without assigning a password. This will allow the user
          to login to the system without being authenticated by a password.
        type: bool
      state:
        description:
        - Configures the state of the username definition as it relates to the device
          operational configuration. When set to I(present), the username(s) should be
          configured in the device active configuration and when set to I(absent) the
          username(s) should not be in the device active configuration
        choices:
        - present
        - absent
        type: str
  name:
    description:
    - The username to be configured on the Cisco IOS device. This argument accepts
      a string value and is mutually exclusive with the C(aggregate) argument. Please
      note that this option is not same as C(provider username).
    type: str
  configured_password:
    description:
    - The password to be configured on the Cisco IOS device. The password needs to
      be provided in clear and it will be encrypted on the device. Please note that
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
  password_type:
    description:
    - This argument determines whether a 'password' or 'secret' will be configured.
    default: secret
    choices:
    - secret
    - password
    type: str
  hashed_password:
    description:
    - This option allows configuring hashed passwords on Cisco IOS devices.
    type: dict
    suboptions:
      type:
        description:
        - Specifies the type of hash (e.g., 5 for MD5, 8 for PBKDF2, etc.)
        - For this to work, the device needs to support the desired hash type
        type: int
        required: true
      value:
        description:
        - The actual hashed password to be configured on the device
        required: true
        type: str
  privilege:
    description:
    - The C(privilege) argument configures the privilege level of the user when logged
      into the system. This argument accepts integer values in the range of 1 to 15.
    type: int
  view:
    description:
    - Configures the view for the username in the device running configuration. The
      argument accepts a string value defining the view name. This argument does not
      check if the view has been configured on the device.
    aliases:
    - role
    type: str
  sshkey:
    description:
    - Specifies one or more SSH public key(s) to configure for the given username.
    - This argument accepts a valid SSH key value.
    type: list
    elements: str
  nopassword:
    description:
    - Defines the username without assigning a password. This will allow the user
      to login to the system without being authenticated by a password.
    type: bool
  purge:
    description:
    - Instructs the module to consider the resource definition absolute. It will remove
      any previously configured usernames on the device with the exception of the
      `admin` user (the current defined set of users).
    type: bool
    default: false
  state:
    description:
    - Configures the state of the username definition as it relates to the device
      operational configuration. When set to I(present), the username(s) should be
      configured in the device active configuration and when set to I(absent) the
      username(s) should not be in the device active configuration
    default: present
    choices:
    - present
    - absent
    type: str
extends_documentation_fragment:
- cisco.ios.ios
"""
EXAMPLES = """
- name: create a new user
  cisco.ios.ios_user:
    name: ansible
    nopassword: true
    sshkey: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    state: present

- name: create a new user with multiple keys
  cisco.ios.ios_user:
    name: ansible
    sshkey:
    - "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    - "{{ lookup('file', '~/path/to/public_key') }}"
    state: present

- name: remove all users except admin
  cisco.ios.ios_user:
    purge: yes

- name: remove all users except admin and these listed users
  cisco.ios.ios_user:
    aggregate:
    - name: testuser1
    - name: testuser2
    - name: testuser3
    purge: yes

- name: set multiple users to privilege level 15
  cisco.ios.ios_user:
    aggregate:
    - name: netop
    - name: netend
    privilege: 15
    state: present

- name: set user view/role
  cisco.ios.ios_user:
    name: netop
    view: network-operator
    state: present

- name: Change Password for User netop
  cisco.ios.ios_user:
    name: netop
    configured_password: '{{ new_password }}'
    update_password: always
    state: present

- name: Aggregate of users
  cisco.ios.ios_user:
    aggregate:
    - name: ansibletest2
    - name: ansibletest3
    view: network-admin

- name: Add a user specifying password type
  cisco.ios.ios_user:
    name: ansibletest4
    configured_password: '{{ new_password }}'
    password_type: password

- name: Add a user with MD5 hashed password
  cisco.ios.ios_user:
    name: ansibletest5
    hashed_password:
      type: 5
      value: $3$8JcDilcYgFZi.yz4ApaqkHG2.8/

- name: Delete users with aggregate
  cisco.ios.ios_user:
    aggregate:
    - name: ansibletest1
    - name: ansibletest2
    - name: ansibletest3
    state: absent
"""
RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - username ansible secret password
    - username admin secret admin
"""
import base64
import hashlib
import re
from copy import deepcopy
from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_default_spec,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    get_config,
    load_config,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    ios_argument_spec,
)
from ansible.module_utils.six import iteritems


def validate_privilege(value, module):
    if value and not 1 <= value <= 15:
        module.fail_json(
            msg="privilege must be between 1 and 15, got %s" % value
        )


def user_del_cmd(username):
    return {
        "command": "no username %s" % username,
        "prompt": "This operation will remove all username related configurations with same name",
        "answer": "y",
        "newline": False,
    }


def sshkey_fingerprint(sshkey):
    # IOS will accept a MD5 fingerprint of the public key
    # and is easier to configure in a single line
    # we calculate this fingerprint here
    if not sshkey:
        return None
    if " " in sshkey:
        # ssh-rsa AAA...== comment
        keyparts = sshkey.split(" ")
        keyparts[1] = (
            hashlib.md5(base64.b64decode(keyparts[1])).hexdigest().upper()
        )
        return " ".join(keyparts)
    else:
        # just the key, assume rsa type
        return (
            "ssh-rsa %s"
            % hashlib.md5(base64.b64decode(sshkey)).hexdigest().upper()
        )


def map_obj_to_commands(updates, module):
    commands = list()
    update_password = module.params["update_password"]
    password_type = module.params["password_type"]

    def needs_update(want, have, x):
        return want.get(x) and want.get(x) != have.get(x)

    def add(command, want, x):
        command.append("username %s %s" % (want["name"], x))

    def add_hashed_password(command, want, x):
        command.append(
            "username %s secret %s %s"
            % (want["name"], x.get("type"), x.get("value"))
        )

    def add_ssh(command, want, x=None):
        command.append("ip ssh pubkey-chain")
        if x:
            command.append("username %s" % want["name"])
            for item in x:
                command.append("key-hash %s" % item)
            command.append("exit")
        else:
            command.append("no username %s" % want["name"])
        command.append("exit")

    for update in updates:
        want, have = update
        if want["state"] == "absent":
            if have["sshkey"]:
                add_ssh(commands, want)
            else:
                commands.append(user_del_cmd(want["name"]))
        if needs_update(want, have, "view"):
            add(commands, want, "view %s" % want["view"])
        if needs_update(want, have, "privilege"):
            add(commands, want, "privilege %s" % want["privilege"])
        if needs_update(want, have, "sshkey"):
            add_ssh(commands, want, want["sshkey"])
        if needs_update(want, have, "configured_password"):
            if update_password == "always" or not have:
                if have and password_type != have["password_type"]:
                    module.fail_json(
                        msg="Can not have both a user password and a user secret."
                        + " Please choose one or the other."
                    )
                add(
                    commands,
                    want,
                    "%s %s" % (password_type, want["configured_password"]),
                )
        if needs_update(want, have, "hashed_password"):
            add_hashed_password(commands, want, want["hashed_password"])
        if needs_update(want, have, "nopassword"):
            if want["nopassword"]:
                add(commands, want, "nopassword")
            else:
                add(commands, want, user_del_cmd(want["name"]))
    return commands


def parse_view(data):
    match = re.search("view (\\S+)", data, re.M)
    if match:
        return match.group(1)


def parse_sshkey(data, user):
    sshregex = "username %s(\\n\\s+key-hash .+$)+" % user
    sshcfg = re.search(sshregex, data, re.M)
    key_list = []
    if sshcfg:
        match = re.findall(
            "key-hash (\\S+ \\S+(?: .+)?)$", sshcfg.group(), re.M
        )
        if match:
            key_list = match
    return key_list


def parse_privilege(data):
    match = re.search("privilege (\\S+)", data, re.M)
    if match:
        return int(match.group(1))


def parse_password_type(data):
    type = None
    if data and data.split()[-3] in ["password", "secret"]:
        type = data.split()[-3]
    return type


def map_config_to_obj(module):
    data = get_config(module, flags=["| section username"])
    match = re.findall("(?:^(?:u|\\s{2}u))sername (\\S+)", data, re.M)
    if not match:
        return list()
    instances = list()
    for user in set(match):
        regex = "username %s .+$" % user
        cfg = re.findall(regex, data, re.M)
        cfg = "\n".join(cfg)
        obj = {
            "name": user,
            "state": "present",
            "nopassword": "nopassword" in cfg,
            "configured_password": None,
            "hashed_password": None,
            "password_type": parse_password_type(cfg),
            "sshkey": parse_sshkey(data, user),
            "privilege": parse_privilege(cfg),
            "view": parse_view(cfg),
        }
        instances.append(obj)
    return instances


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
    # validate the param value (if validator func exists)
    validator = globals().get("validate_%s" % key)
    if all((value, validator)):
        validator(value, module)
    return value


def map_params_to_obj(module):
    users = module.params["aggregate"]
    if not users:
        if not module.params["name"] and module.params["purge"]:
            return list()
        elif not module.params["name"]:
            module.fail_json(msg="username is required")
        else:
            aggregate = [{"name": module.params["name"]}]
    else:
        aggregate = list()
        for item in users:
            if not isinstance(item, dict):
                aggregate.append({"name": item})
            elif "name" not in item:
                module.fail_json(msg="name is required")
            else:
                aggregate.append(item)
    objects = list()
    for item in aggregate:
        get_value = partial(get_param_value, item=item, module=module)
        item["configured_password"] = get_value("configured_password")
        item["hashed_password"] = get_value("hashed_password")
        item["nopassword"] = get_value("nopassword")
        item["privilege"] = get_value("privilege")
        item["view"] = get_value("view")
        item["sshkey"] = render_key_list(get_value("sshkey"))
        item["state"] = get_value("state")
        objects.append(item)
    return objects


def render_key_list(ssh_keys):
    key_list = []
    if ssh_keys:
        for item in ssh_keys:
            key_list.append(sshkey_fingerprint(item))
    return key_list


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
    hashed_password_spec = dict(
        type=dict(type="int", required=True),
        value=dict(no_log=True, required=True),
    )
    element_spec = dict(
        name=dict(),
        configured_password=dict(no_log=True),
        hashed_password=dict(
            no_log=True, type="dict", options=hashed_password_spec
        ),
        nopassword=dict(type="bool"),
        update_password=dict(
            default="always", choices=["on_create", "always"]
        ),
        password_type=dict(default="secret", choices=["secret", "password"]),
        privilege=dict(type="int"),
        view=dict(aliases=["role"]),
        sshkey=dict(type="list", elements="str"),
        state=dict(default="present", choices=["present", "absent"]),
    )
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec["name"] = dict(required=True)
    # remove default in aggregate spec, to handle common arguments
    remove_default_spec(aggregate_spec)
    argument_spec = dict(
        aggregate=dict(
            type="list",
            elements="dict",
            options=aggregate_spec,
            aliases=["users", "collection"],
        ),
        purge=dict(type="bool", default=False),
    )
    argument_spec.update(element_spec)
    argument_spec.update(ios_argument_spec)
    mutually_exclusive = [
        ("name", "aggregate"),
        ("nopassword", "hashed_password", "configured_password"),
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    warnings = list()
    result = {"changed": False, "warnings": warnings}
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands(update_objects(want, have), module)
    if module.params["purge"]:
        want_users = [x["name"] for x in want]
        have_users = [x["name"] for x in have]
        for item in set(have_users).difference(want_users):
            if item != "admin":
                commands.append(user_del_cmd(item))
    result["commands"] = commands
    if commands:
        if not module.check_mode:
            load_config(module, commands)
        result["changed"] = True
    module.exit_json(**result)


if __name__ == "__main__":
    main()
