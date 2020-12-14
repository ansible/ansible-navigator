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
"""
The module file for ios_lacp
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: ios_lacp
short_description: LACP resource module
description: This module provides declarative management of Global LACP on Cisco IOS
  network devices.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL.
options:
  config:
    description: The provided configurations.
    type: dict
    suboptions:
      system:
        description: This option sets the default system parameters for LACP.
        type: dict
        suboptions:
          priority:
            description:
            - LACP priority for the system.
            - Refer to vendor documentation for valid values.
            type: int
            required: true
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show lacp sys-id).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - rendered
    - parsed
    - gathered
    default: merged
"""

EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# vios#show lacp sys-id
# 32768, 5e00.0000.8000

- name: Merge provided configuration with device configuration
  cisco.ios.ios_lacp:
    config:
      system:
        priority: 123
    state: merged

# After state:
# ------------
#
# vios#show lacp sys-id
# 123, 5e00.0000.8000

# Using replaced
#
# Before state:
# -------------
#
# vios#show lacp sys-id
# 500, 5e00.0000.8000

- name: Replaces Global LACP configuration
  cisco.ios.ios_lacp:
    config:
      system:
        priority: 123
    state: replaced

# After state:
# ------------
#
# vios#show lacp sys-id
# 123, 5e00.0000.8000

# Using Deleted
#
# Before state:
# -------------
#
# vios#show lacp sys-id
# 500, 5e00.0000.8000

- name: Delete Global LACP attribute
  cisco.ios.ios_lacp:
    state: deleted

# After state:
# -------------
#
# vios#show lacp sys-id
# 32768, 5e00.0000.8000

# Using Gathered

# Before state:
# -------------
#
# vios#show lacp sys-id
# 123, 5e00.0000.8000

- name: Gather listed LACP with provided configurations
  cisco.ios.ios_lacp:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": {
#         "system": {
#             "priority": 500
#         }
#     }

# After state:
# ------------
#
# vios#show lacp sys-id
# 123, 5e00.0000.8000

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_lacp:
    config:
      system:
        priority: 123
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "lacp system-priority 10"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# lacp system-priority 123

- name: Parse the commands for provided configuration
  cisco.ios.ios_lacp:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": {
#         "system": {
#             "priority": 123
#         }
#     }

"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['lacp system-priority 10']
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.lacp.lacp import (
    LacpArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.lacp.lacp import (
    Lacp,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]

    mutually_exclusive = [("config", "running_config")]

    module = AnsibleModule(
        argument_spec=LacpArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Lacp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
