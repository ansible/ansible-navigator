# this is a virtual module that is entirely implemented server side
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: telnet
short_description: Executes a low-down and dirty telnet command
description:
- Executes a low-down and dirty telnet command, not going through the module subsystem.
- This is mostly to be used for enabling ssh on devices that only have telnet enabled
  by default.
version_added: 1.0.0
options:
  command:
    description:
    - List of commands to be executed in the telnet session.
    required: true
    type: list
    elements: str
    aliases:
    - commands
  host:
    description:
    - The host/target on which to execute the command
    required: false
    type: str
    default: remote_addr
  user:
    description:
    - The user for login
    required: false
    type: str
    default: remote_user
  password:
    description:
    - The password for login
    type: str
  port:
    description:
    - Remote port to use
    type: int
    default: 23
  timeout:
    description:
    - timeout for remote operations
    type: int
    default: 120
  prompts:
    description:
    - List of prompts expected before sending next command
    required: false
    type: list
    elements: str
    default:
    - $
  login_prompt:
    description:
    - Login or username prompt to expect
    required: false
    type: str
    default: 'login: '
  password_prompt:
    description:
    - Login or username prompt to expect
    required: false
    type: str
    default: 'Password: '
  pause:
    description:
    - Seconds to pause between each command issued
    required: false
    type: int
    default: 1
  send_newline:
    description:
    - Sends a newline character upon successful connection to start the terminal session.
    required: false
    type: bool
    default: false
notes:
- The C(environment) keyword does not work with this task
author:
- Ansible Core Team
"""

EXAMPLES = """
- name: send configuration commands to IOS
  ansible.netcommon.telnet:
    user: cisco
    password: cisco
    login_prompt: 'Username: '
    prompts:
    - '[>#]'
    command:
    - terminal length 0
    - configure terminal
    - hostname ios01

- name: run show commands
  ansible.netcommon.telnet:
    user: cisco
    password: cisco
    login_prompt: 'Username: '
    prompts:
    - '[>#]'
    command:
    - terminal length 0
    - show version
"""

RETURN = """
output:
    description: output of each command is an element in this list
    type: list
    returned: always
    sample: [ 'success', 'success', '', 'warning .. something' ]
"""
