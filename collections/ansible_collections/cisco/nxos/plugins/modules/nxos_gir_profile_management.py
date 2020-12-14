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
module: nxos_gir_profile_management
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Create a maintenance-mode or normal-mode profile for GIR.
description:
- Manage a maintenance-mode or normal-mode profile with configuration commands that
  can be applied during graceful removal or graceful insertion.
version_added: 1.0.0
author:
- Gabriele Gerbino (@GGabriele)
notes:
- Tested against NXOSv 7.3.(0)D1(1) on VIRL
- C(state=absent) removes the whole profile.
options:
  commands:
    description:
    - List of commands to be included into the profile.
    type: list
    elements: str
  mode:
    description:
    - Configure the profile as Maintenance or Normal mode.
    required: true
    choices:
    - maintenance
    - normal
    type: str
  state:
    description:
    - Specify desired state of the resource.
    default: present
    choices:
    - present
    - absent
    type: str
"""

EXAMPLES = """
# Create a maintenance-mode profile
- cisco.nxos.nxos_gir_profile_management:
    mode: maintenance
    commands:
    - router eigrp 11
    - isolate

# Remove the maintenance-mode profile
- cisco.nxos.nxos_gir_profile_management:
    mode: maintenance
    state: absent
"""

RETURN = """
proposed:
    description: list of commands passed into module.
    returned: verbose mode
    type: list
    sample: ["router eigrp 11", "isolate"]
existing:
    description: list of existing profile commands.
    returned: verbose mode
    type: list
    sample: ["router bgp 65535","isolate","router eigrp 10","isolate",
            "diagnostic bootup level complete"]
end_state:
    description: list of profile entries after module execution.
    returned: verbose mode
    type: list
    sample: ["router bgp 65535","isolate","router eigrp 10","isolate",
            "diagnostic bootup level complete","router eigrp 11", "isolate"]
updates:
    description: commands sent to the device
    returned: always
    type: list
    sample: ["configure maintenance profile maintenance-mode",
             "router eigrp 11","isolate"]
changed:
    description: check to see if a change was made on the device
    returned: always
    type: bool
    sample: true
"""


from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    get_config,
    load_config,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    CustomNetworkConfig,
)


def get_existing(module):
    existing = []
    netcfg = CustomNetworkConfig(indent=2, contents=get_config(module))

    if module.params["mode"] == "maintenance":
        parents = ["configure maintenance profile maintenance-mode"]
    else:
        parents = ["configure maintenance profile normal-mode"]

    config = netcfg.get_section(parents)
    if config:
        existing = config.splitlines()
        existing = [cmd.strip() for cmd in existing]
        existing.pop(0)

    return existing


def state_present(module, existing, commands):
    cmds = list()
    if existing == commands:
        # Idempotent case
        return cmds
    cmds.extend(commands)
    if module.params["mode"] == "maintenance":
        cmds.insert(0, "configure maintenance profile maintenance-mode")
    else:
        cmds.insert(0, "configure maintenance profile normal-mode")

    return cmds


def state_absent(module, existing, commands):
    if module.params["mode"] == "maintenance":
        cmds = ["no configure maintenance profile maintenance-mode"]
    else:
        cmds = ["no configure maintenance profile normal-mode"]
    return cmds


def invoke(name, *args, **kwargs):
    func = globals().get(name)
    if func:
        return func(*args, **kwargs)


def main():
    argument_spec = dict(
        commands=dict(required=False, type="list", elements="str"),
        mode=dict(required=True, choices=["maintenance", "normal"]),
        state=dict(choices=["absent", "present"], default="present"),
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()

    state = module.params["state"]
    commands = module.params["commands"] or []

    if state == "absent" and commands:
        module.fail_json(msg="when state is absent, no command can be used.")

    existing = invoke("get_existing", module)
    end_state = existing
    changed = False

    result = {}
    cmds = []
    if state == "present" or (state == "absent" and existing):
        cmds = invoke("state_%s" % state, module, existing, commands)

        if module.check_mode:
            module.exit_json(changed=True, commands=cmds)
        else:
            if cmds:
                load_config(module, cmds)
                changed = True
                end_state = invoke("get_existing", module)

    result["changed"] = changed
    if module._verbosity > 0:
        end_state = invoke("get_existing", module)
        result["end_state"] = end_state
        result["existing"] = existing
        result["proposed"] = commands
        result["updates"] = cmds

    result["warnings"] = warnings

    module.exit_json(**result)


if __name__ == "__main__":
    main()
