#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: nxos_command
extends_documentation_fragment:
- cisco.nxos.nxos
author: Peter Sprygada (@privateip)
short_description: Run arbitrary command on Cisco NXOS devices
description:
- Sends an arbitrary command to an NXOS node and returns the results read from the
  device.  This module includes an argument that will cause the module to wait for
  a specific condition before returning or timing out if the condition is not met.
version_added: 1.0.0
options:
  commands:
    description:
    - The commands to send to the remote NXOS device.  The resulting output from the
      command is returned.  If the I(wait_for) argument is provided, the module is
      not returned until the condition is satisfied or the number of retires as expired.
    - The I(commands) argument also accepts an alternative form that allows for complex
      values that specify the command to run and the output format to return. This
      can be done on a command by command basis.  The complex argument supports the
      keywords C(command) and C(output) where C(command) is the command to run and
      C(output) is one of 'text' or 'json'.
    - If a command sent to the device requires answering a prompt, it is possible to pass
      a dict containing command, answer and prompt. Common answers are 'y' or "\\r"
      (carriage return, must be double quotes). See examples.
    required: true
    type: list
    elements: raw
  wait_for:
    description:
    - Specifies what to evaluate from the output of the command and what conditionals
      to apply.  This argument will cause the task to wait for a particular conditional
      to be true before moving forward.   If the conditional is not true by the configured
      retries, the task fails.  See examples.
    aliases:
    - waitfor
    type: list
    elements: str
  match:
    description:
    - The I(match) argument is used in conjunction with the I(wait_for) argument to
      specify the match policy.  Valid values are C(all) or C(any).  If the value
      is set to C(all) then all conditionals in the I(wait_for) must be satisfied.  If
      the value is set to C(any) then only one of the values must be satisfied.
    default: all
    choices: ['any', 'all']
    type: str
  retries:
    description:
    - Specifies the number of retries a command should by tried before it is considered
      failed.  The command is run on the target device every retry and evaluated against
      the I(wait_for) conditionals.
    default: 10
    type: int
  interval:
    description:
    - Configures the interval in seconds to wait between retries of the command.  If
      the command does not pass the specified conditional, the interval indicates
      how to long to wait before trying the command again.
    default: 1
    type: int
"""

EXAMPLES = """
- name: run show version on remote devices
  cisco.nxos.nxos_command:
    commands: show version

- name: run show version and check to see if output contains Cisco
  cisco.nxos.nxos_command:
    commands: show version
    wait_for: result[0] contains Cisco

- name: run multiple commands on remote nodes
  cisco.nxos.nxos_command:
    commands:
    - show version
    - show interfaces

- name: run multiple commands and evaluate the output
  cisco.nxos.nxos_command:
    commands:
    - show version
    - show interfaces
    wait_for:
    - result[0] contains Cisco
    - result[1] contains loopback0

- name: run commands and specify the output format
  cisco.nxos.nxos_command:
    commands:
    - command: show version
      output: json

- name: run commands that require answering a prompt
  cisco.nxos.nxos_command:
    commands:
    - configure terminal
    - command: no feature npv
      prompt: Do you want to continue
      answer: y

"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
failed_conditions:
  description: The list of conditionals that have failed
  returned: failed
  type: list
  sample: ['...', '...']
"""
import time

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.parsing import (
    Conditional,
    FailedConditionalError,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    transform_commands,
    to_lines,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.nxos import (
    nxos_argument_spec,
    run_commands,
)


def parse_commands(module, warnings):
    commands = transform_commands(module)

    if module.check_mode:
        for item in list(commands):
            if not item["command"].startswith("show"):
                warnings.append(
                    "Only show commands are supported when using check mode, not "
                    "executing %s" % item["command"]
                )
                commands.remove(item)

    return commands


def to_cli(obj):
    cmd = obj["command"]
    if obj.get("output") == "json":
        cmd += " | json"
    return cmd


def main():
    """entry point for module execution
    """
    argument_spec = dict(
        # { command: <str>, output: <str>, prompt: <str>, response: <str> }
        commands=dict(type="list", required=True, elements="raw"),
        wait_for=dict(type="list", aliases=["waitfor"], elements="str"),
        match=dict(default="all", choices=["any", "all"]),
        retries=dict(default=10, type="int"),
        interval=dict(default=1, type="int"),
    )

    argument_spec.update(nxos_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    warnings = list()
    result = {"changed": False, "warnings": warnings}
    commands = parse_commands(module, warnings)
    wait_for = module.params["wait_for"] or list()

    try:
        conditionals = [Conditional(c) for c in wait_for]
    except AttributeError as exc:
        module.fail_json(msg=to_text(exc))

    retries = module.params["retries"]
    interval = module.params["interval"]
    match = module.params["match"]

    while retries > 0:
        responses = run_commands(module, commands)

        for item in list(conditionals):
            try:
                if item(responses):
                    if match == "any":
                        conditionals = list()
                        break
                    conditionals.remove(item)
            except FailedConditionalError as exc:
                module.fail_json(msg=to_text(exc))

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = "One or more conditional statements have not been satisfied"
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result.update(
        {"stdout": responses, "stdout_lines": list(to_lines(responses))}
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
