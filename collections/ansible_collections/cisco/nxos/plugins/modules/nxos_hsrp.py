#!/usr/bin/python
from __future__ import absolute_import, division, print_function

__metaclass__ = type

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = """
module: nxos_hsrp
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Manages HSRP configuration on NX-OS switches.
description:
- Manages HSRP configuration on NX-OS switches.
version_added: 1.0.0
author:
- Jason Edelman (@jedelman8)
- Gabriele Gerbino (@GGabriele)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- HSRP feature needs to be enabled first on the system.
- SVIs must exist before using this module.
- Interface must be a L3 port before using this module.
- HSRP cannot be configured on loopback interfaces.
- MD5 authentication is only possible with HSRPv2 while it is ignored if HSRPv1 is
  used instead, while it will not raise any error. Here we allow MD5 authentication
  only with HSRPv2 in order to enforce better practice.
options:
  group:
    description:
    - HSRP group number.
    required: true
    type: str
  interface:
    description:
    - Full name of interface that is being managed for HSRP.
    required: true
    type: str
  version:
    description:
    - HSRP version.
    default: 1
    choices:
    - '1'
    - '2'
    type: str
  priority:
    description:
    - HSRP priority or keyword 'default'.
    type: str
  preempt:
    description:
    - Enable/Disable preempt.
    choices:
    - enabled
    - disabled
    type: str
  vip:
    description:
    - HSRP virtual IP address or keyword 'default'
    type: str
  auth_string:
    description:
    - Authentication string. If this needs to be hidden(for md5 type), the string
      should be 7 followed by the key string. Otherwise, it can be 0 followed by key
      string or just key string (for backward compatibility). For text type, this
      should be just be a key string. if this is 'default', authentication is removed.
    type: str
  auth_type:
    description:
    - Authentication type.
    choices:
    - text
    - md5
    type: str
  state:
    description:
    - Specify desired state of the resource.
    choices:
    - present
    - absent
    default: present
    type: str
"""

EXAMPLES = """
- name: Ensure HSRP is configured with following params on a SVI
  cisco.nxos.nxos_hsrp:
    group: 10
    vip: 10.1.1.1
    priority: 150
    interface: vlan10
    preempt: enabled

- name: Ensure HSRP is configured with following params on a SVI with clear text authentication
  cisco.nxos.nxos_hsrp:
    group: 10
    vip: 10.1.1.1
    priority: 150
    interface: vlan10
    preempt: enabled
    auth_type: text
    auth_string: CISCO

- name: Ensure HSRP is configured with md5 authentication and clear authentication
    string
  cisco.nxos.nxos_hsrp:
    group: 10
    vip: 10.1.1.1
    priority: 150
    interface: vlan10
    preempt: enabled
    auth_type: md5
    auth_string: 0 1234

- name: Ensure HSRP is configured with md5 authentication and hidden authentication
    string
  cisco.nxos.nxos_hsrp:
    group: 10
    vip: 10.1.1.1
    priority: 150
    interface: vlan10
    preempt: enabled
    auth_type: md5
    auth_string: 7 1234

- name: Remove HSRP config for given interface, group, and VIP
  cisco.nxos.nxos_hsrp:
    group: 10
    interface: vlan10
    vip: 10.1.1.1
    state: absent
"""

RETURN = r"""
commands:
    description: commands sent to the device
    returned: always
    type: list
    sample: ["interface vlan10", "hsrp version 2", "hsrp 30", "ip 10.30.1.1"]
"""

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    load_config,
    run_commands,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    get_capabilities,
    nxos_argument_spec,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    get_interface_type,
)
from ansible.module_utils.basic import AnsibleModule


PARAM_TO_DEFAULT_KEYMAP = {
    "vip": None,
    "priority": "100",
    "auth_type": "text",
    "auth_string": "cisco",
}


def apply_key_map(key_map, table):
    new_dict = {}
    for key in table:
        new_key = key_map.get(key)
        if new_key:
            value = table.get(key)
            if value:
                new_dict[new_key] = str(value)
            else:
                new_dict[new_key] = value
    return new_dict


def get_interface_mode(interface, intf_type, module):
    command = "show interface {0} | json".format(interface)
    interface = {}
    mode = "unknown"
    try:
        body = run_commands(module, [command])[0]
    except IndexError:
        return None

    if intf_type in ["ethernet", "portchannel"]:
        interface_table = body["TABLE_interface"]["ROW_interface"]
        mode = str(interface_table.get("eth_mode", "layer3"))
        if mode == "access" or mode == "trunk":
            mode = "layer2"
    elif intf_type == "svi":
        mode = "layer3"
    return mode


def get_hsrp_group(group, interface, module):
    command = "show hsrp group {0} all | json".format(group)
    hsrp = {}

    hsrp_key = {
        "sh_if_index": "interface",
        "sh_group_num": "group",
        "sh_group_version": "version",
        "sh_cfg_prio": "priority",
        "sh_preempt": "preempt",
        "sh_vip": "vip",
        "sh_authentication_type": "auth_type",
        "sh_keystring_attr": "auth_enc",
        "sh_authentication_data": "auth_string",
    }

    try:
        body = run_commands(module, [command])[0]
        hsrp_table = body["TABLE_grp_detail"]["ROW_grp_detail"]
        if "sh_keystring_attr" not in hsrp_table:
            del hsrp_key["sh_keystring_attr"]
        if "unknown enum:" in str(hsrp_table):
            hsrp_table = get_hsrp_group_unknown_enum(
                module, command, hsrp_table
            )
    except (AttributeError, IndexError, TypeError, KeyError):
        return {}

    if isinstance(hsrp_table, dict):
        hsrp_table = [hsrp_table]

    for hsrp_group in hsrp_table:
        parsed_hsrp = apply_key_map(hsrp_key, hsrp_group)

        parsed_hsrp["interface"] = parsed_hsrp["interface"].lower()

        if parsed_hsrp["version"] == "v1":
            parsed_hsrp["version"] = "1"
        elif parsed_hsrp["version"] == "v2":
            parsed_hsrp["version"] = "2"

        if parsed_hsrp["auth_type"] == "md5":
            if parsed_hsrp["auth_enc"] == "hidden":
                parsed_hsrp["auth_enc"] = "7"
            else:
                parsed_hsrp["auth_enc"] = "0"

        if parsed_hsrp["interface"] == interface:
            return parsed_hsrp

    return hsrp


def get_hsrp_group_unknown_enum(module, command, hsrp_table):
    """Some older NXOS images fail to set the attr values when using structured output and
    instead set the values to <unknown enum>. This fallback method is a workaround that
    uses an unstructured (text) request to query the device a second time.
    'sh_preempt' is currently the only attr affected. Add checks for other attrs as needed.
    """
    if "unknown enum:" in hsrp_table["sh_preempt"]:
        cmd = {"output": "text", "command": command.split("|")[0]}
        out = run_commands(module, cmd)[0]
        hsrp_table["sh_preempt"] = (
            "enabled" if ("may preempt" in out) else "disabled"
        )
    return hsrp_table


def get_commands_remove_hsrp(group, interface):
    commands = ["interface {0}".format(interface), "no hsrp {0}".format(group)]
    return commands


def get_commands_config_hsrp(delta, interface, args, existing):
    commands = []

    config_args = {
        "group": "hsrp {group}",
        "priority": "{priority}",
        "preempt": "{preempt}",
        "vip": "{vip}",
    }

    preempt = delta.get("preempt", None)
    group = delta.get("group", None)
    vip = delta.get("vip", None)
    priority = delta.get("priority", None)

    if preempt:
        if preempt == "enabled":
            delta["preempt"] = "preempt"
        elif preempt == "disabled":
            delta["preempt"] = "no preempt"

    if priority:
        if priority == "default":
            if existing and existing.get(
                "priority"
            ) != PARAM_TO_DEFAULT_KEYMAP.get("priority"):
                delta["priority"] = "no priority"
            else:
                del delta["priority"]
        else:
            delta["priority"] = "priority {0}".format(delta["priority"])

    if vip:
        if vip == "default":
            if existing and existing.get("vip") != PARAM_TO_DEFAULT_KEYMAP.get(
                "vip"
            ):
                delta["vip"] = "no ip"
            else:
                del delta["vip"]
        else:
            delta["vip"] = "ip {0}".format(delta["vip"])

    for key in delta:
        command = config_args.get(key, "DNE").format(**delta)
        if command and command != "DNE":
            if key == "group":
                commands.insert(0, command)
            else:
                commands.append(command)
        command = None

    auth_type = delta.get("auth_type", None)
    auth_string = delta.get("auth_string", None)
    auth_enc = delta.get("auth_enc", None)
    if auth_type or auth_string:
        if not auth_type:
            auth_type = args["auth_type"]
        elif not auth_string:
            auth_string = args["auth_string"]
        if auth_string != "default":
            if auth_type == "md5":
                command = "authentication md5 key-string {0} {1}".format(
                    auth_enc, auth_string
                )
                commands.append(command)
            elif auth_type == "text":
                command = "authentication text {0}".format(auth_string)
                commands.append(command)
        else:
            if existing and existing.get(
                "auth_string"
            ) != PARAM_TO_DEFAULT_KEYMAP.get("auth_string"):
                commands.append("no authentication")

    if commands and not group:
        commands.insert(0, "hsrp {0}".format(args["group"]))

    version = delta.get("version", None)
    if version:
        if version == "2":
            command = "hsrp version 2"
        elif version == "1":
            command = "hsrp version 1"
        commands.insert(0, command)
        commands.insert(0, "interface {0}".format(interface))

    if commands:
        if not commands[0].startswith("interface"):
            commands.insert(0, "interface {0}".format(interface))

    return commands


def is_default(interface, module):
    command = "show run interface {0}".format(interface)

    try:
        body = run_commands(module, [command], check_rc=False)[0]
        if "invalid" in body.lower():
            return "DNE"
        else:
            raw_list = body.split("\n")
            if raw_list[-1].startswith("interface"):
                return True
            else:
                return False
    except (KeyError):
        return "DNE"


def validate_config(body, vip, module):
    new_body = "".join(body)
    if "invalid ip address" in new_body.lower():
        module.fail_json(
            msg="Invalid VIP. Possible duplicate IP address.", vip=vip
        )


def main():
    argument_spec = dict(
        group=dict(required=True, type="str"),
        interface=dict(required=True),
        version=dict(choices=["1", "2"], default="1", required=False),
        priority=dict(type="str", required=False),
        preempt=dict(
            type="str", choices=["disabled", "enabled"], required=False
        ),
        vip=dict(type="str", required=False),
        auth_type=dict(choices=["text", "md5"], required=False),
        auth_string=dict(type="str", required=False),
        state=dict(
            choices=["absent", "present"], required=False, default="present"
        ),
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()
    results = dict(changed=False, warnings=warnings)

    interface = module.params["interface"].lower()
    group = module.params["group"]
    version = module.params["version"]
    state = module.params["state"]
    priority = module.params["priority"]
    preempt = module.params["preempt"]
    vip = module.params["vip"]
    auth_type = module.params["auth_type"]
    auth_full_string = module.params["auth_string"]
    auth_enc = "0"
    auth_string = None
    if auth_full_string:
        kstr = auth_full_string.split()
        if len(kstr) == 2:
            auth_enc = kstr[0]
            auth_string = kstr[1]
        elif len(kstr) == 1:
            auth_string = kstr[0]
        else:
            module.fail_json(msg="Invalid auth_string")
        if auth_enc != "0" and auth_enc != "7":
            module.fail_json(msg="Invalid auth_string, only 0 or 7 allowed")

    device_info = get_capabilities(module)
    network_api = device_info.get("network_api", "nxapi")

    intf_type = get_interface_type(interface)
    if intf_type != "ethernet" and network_api == "cliconf":
        if is_default(interface, module) == "DNE":
            module.fail_json(
                msg="That interface does not exist yet. Create " "it first.",
                interface=interface,
            )
        if intf_type == "loopback":
            module.fail_json(
                msg="Loopback interfaces don't support HSRP.",
                interface=interface,
            )

    mode = get_interface_mode(interface, intf_type, module)
    if mode == "layer2":
        module.fail_json(
            msg="That interface is a layer2 port.\nMake it "
            "a layer 3 port first.",
            interface=interface,
        )

    if auth_type or auth_string:
        if not (auth_type and auth_string):
            module.fail_json(
                msg="When using auth parameters, you need BOTH "
                "auth_type AND auth_string."
            )

    args = dict(
        group=group,
        version=version,
        priority=priority,
        preempt=preempt,
        vip=vip,
        auth_type=auth_type,
        auth_string=auth_string,
        auth_enc=auth_enc,
    )

    proposed = dict((k, v) for k, v in args.items() if v is not None)

    existing = get_hsrp_group(group, interface, module)

    # This will enforce better practice with md5 and hsrp version.
    if proposed.get("auth_type", None) == "md5":
        if proposed["version"] == "1":
            module.fail_json(
                msg="It's recommended to use HSRP v2 " "when auth_type=md5"
            )

    elif not proposed.get("auth_type", None) and existing:
        if (
            proposed["version"] == "1" and existing["auth_type"] == "md5"
        ) and state == "present":
            module.fail_json(
                msg="Existing auth_type is md5. It's recommended "
                "to use HSRP v2 when using md5"
            )

    commands = []
    if state == "present":
        delta = dict(set(proposed.items()).difference(existing.items()))
        if delta:
            command = get_commands_config_hsrp(
                delta, interface, args, existing
            )
            commands.extend(command)

    elif state == "absent":
        if existing:
            command = get_commands_remove_hsrp(group, interface)
            commands.extend(command)

    if commands:
        if module.check_mode:
            module.exit_json(**results)
        else:
            load_config(module, commands)

            # validate IP
            if network_api == "cliconf" and state == "present":
                commands.insert(0, "config t")
                body = run_commands(module, commands)
                validate_config(body, vip, module)

            results["changed"] = True

            if "configure" in commands:
                commands.pop(0)

    results["commands"] = commands
    module.exit_json(**results)


if __name__ == "__main__":
    main()
