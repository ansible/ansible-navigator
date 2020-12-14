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
module: nxos_ospf
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: (deprecated, removed after 2022-06-01) Manages configuration
  of an ospf instance.
description:
- Manages configuration of an ospf instance.
version_added: 1.0.0
author: Gabriele Gerbino (@GGabriele)
deprecated:
  alternative: nxos_ospfv2 and nxos_ospfv3
  why: Updated modules released with more functionality.
  removed_at_date: '2022-06-01'
options:
  ospf:
    description:
    - Name of the ospf instance.
    required: true
    type: str
  state:
    description:
    - Determines whether the config should be present or not on the device.
    required: false
    default: present
    choices:
    - present
    - absent
    type: str

"""

EXAMPLES = """
- cisco.nxos.nxos_ospf:
    ospf: 1
    state: present
"""

RETURN = """
commands:
    description: commands sent to the device
    returned: always
    type: list
    sample: ["router ospf 1"]
"""

import re
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


PARAM_TO_COMMAND_KEYMAP = {"ospf": "router ospf"}


def get_value(config, module):
    splitted_config = config.splitlines()
    value_list = []
    REGEX = r"^router ospf\s(?P<ospf>\S+).*"
    for line in splitted_config:
        value = ""
        if "router ospf" in line:
            try:
                match_ospf = re.match(REGEX, line, re.DOTALL)
                ospf_group = match_ospf.groupdict()
                value = ospf_group["ospf"]
            except AttributeError:
                value = ""
            if value:
                value_list.append(value)

    return value_list


def get_existing(module):
    existing = {}
    config = str(get_config(module))

    value = get_value(config, module)
    if value:
        existing["ospf"] = value
    return existing


def state_present(module, proposed, candidate):
    commands = ["router ospf {0}".format(proposed["ospf"])]
    candidate.add(commands, parents=[])


def state_absent(module, proposed, candidate):
    commands = ["no router ospf {0}".format(proposed["ospf"])]
    candidate.add(commands, parents=[])


def main():
    argument_spec = dict(
        ospf=dict(required=True, type="str"),
        state=dict(
            choices=["present", "absent"], default="present", required=False
        ),
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()
    result = dict(changed=False, warnings=warnings)

    state = module.params["state"]
    ospf = str(module.params["ospf"])

    existing = get_existing(module)
    proposed = dict(ospf=ospf)

    if not existing:
        existing_list = []
    else:
        existing_list = existing["ospf"]

    candidate = CustomNetworkConfig(indent=3)
    if state == "present" and ospf not in existing_list:
        state_present(module, proposed, candidate)
    if state == "absent" and ospf in existing_list:
        state_absent(module, proposed, candidate)

    if candidate:
        candidate = candidate.items_text()
        load_config(module, candidate)
        result["changed"] = True
        result["commands"] = candidate

    else:
        result["commands"] = []
    module.exit_json(**result)


if __name__ == "__main__":
    main()
