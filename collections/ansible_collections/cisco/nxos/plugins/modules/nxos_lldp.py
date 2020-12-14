#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: nxos_lldp
author: Ganesh Nalawade (@ganeshrn)
short_description: (deprecated, removed after 2022-06-01) Manage LLDP
  configuration on Cisco NXOS network devices.
description:
- This module provides declarative management of LLDP service on Cisco NXOS network
  devices.
version_added: 1.0.0
deprecated:
  alternative: nxos_lldp_global
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
notes:
- Tested against NXOSv 7.0(3)I5(1).
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
- cisco.nxos.nxos


"""

EXAMPLES = """
- name: Enable LLDP service
  cisco.nxos.nxos_lldp:
    state: present

- name: Disable LLDP service
  cisco.nxos.nxos_lldp:
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - feature lldp
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    get_config,
    load_config,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
)


def has_lldp(module):
    output = get_config(module, ["| section lldp"])
    is_lldp_enable = False
    if output and "feature lldp" in output:
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

    argument_spec.update(nxos_argument_spec)

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
        commands.append("no feature lldp")
    elif module.params["state"] == "present" and not HAS_LLDP:
        commands.append("feature lldp")

    result["commands"] = commands

    if commands:
        # On N35 A8 images, some features return a yes/no prompt
        # on enablement or disablement. Bypass using terminal dont-ask
        commands.insert(0, "terminal dont-ask")
        if not module.check_mode:
            load_config(module, commands)

        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
