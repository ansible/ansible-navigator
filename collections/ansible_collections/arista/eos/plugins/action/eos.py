#
# (c) 2016 Red Hat Inc.
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

import sys
import copy

from ansible import constants as C
from ansible_collections.arista.eos.plugins.module_utils.network.eos.eos import (
    eos_provider_spec,
)
from ansible_collections.ansible.netcommon.plugins.action.network import (
    ActionModule as ActionNetworkModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    load_provider,
)
from ansible.utils.display import Display

display = Display()


class ActionModule(ActionNetworkModule):
    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split(".")[-1]
        self._config_module = (
            True if module_name in ["eos_config", "config"] else False
        )
        persistent_connection = self._play_context.connection.split(".")[-1]
        warnings = []

        if persistent_connection in ("network_cli", "httpapi"):
            provider = self._task.args.get("provider", {})
            if any(provider.values()):
                display.warning(
                    "provider is unnecessary when using %s and will be ignored"
                    % self._play_context.connection
                )
                del self._task.args["provider"]
            if self._task.args.get("transport"):
                display.warning(
                    "transport is unnecessary when using %s and will be ignored"
                    % self._play_context.connection
                )
                del self._task.args["transport"]
        elif self._play_context.connection == "local":
            provider = load_provider(eos_provider_spec, self._task.args)
            transport = provider["transport"] or "cli"

            display.vvvv(
                "connection transport is %s" % transport,
                self._play_context.remote_addr,
            )

            if transport == "cli":
                pc = copy.deepcopy(self._play_context)
                pc.connection = "ansible.netcommon.network_cli"
                pc.network_os = "arista.eos.eos"
                pc.remote_addr = (
                    provider["host"] or self._play_context.remote_addr
                )
                pc.port = int(
                    provider["port"] or self._play_context.port or 22
                )
                pc.remote_user = (
                    provider["username"] or self._play_context.connection_user
                )
                pc.password = (
                    provider["password"] or self._play_context.password
                )
                pc.private_key_file = (
                    provider["ssh_keyfile"]
                    or self._play_context.private_key_file
                )
                pc.become = provider["authorize"] or False
                if pc.become:
                    pc.become_method = "enable"
                pc.become_pass = provider["auth_pass"]

                connection = self._shared_loader_obj.connection_loader.get(
                    "ansible.netcommon.persistent",
                    pc,
                    sys.stdin,
                    task_uuid=self._task._uuid,
                )

                # TODO: Remove below code after ansible minimal is cut out
                if connection is None:
                    pc.connection = "network_cli"
                    pc.network_os = "eos"
                    connection = self._shared_loader_obj.connection_loader.get(
                        "persistent", pc, sys.stdin, task_uuid=self._task._uuid
                    )

                display.vvv(
                    "using connection plugin %s (was local)" % pc.connection,
                    pc.remote_addr,
                )

                command_timeout = (
                    int(provider["timeout"])
                    if provider["timeout"]
                    else connection.get_option("persistent_command_timeout")
                )
                connection.set_options(
                    direct={"persistent_command_timeout": command_timeout}
                )

                socket_path = connection.run()
                display.vvvv("socket_path: %s" % socket_path, pc.remote_addr)
                if not socket_path:
                    return {
                        "failed": True,
                        "msg": "unable to open shell. Please see: "
                        + "https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell",
                    }

                task_vars["ansible_socket"] = socket_path
                warnings.append(
                    [
                        "connection local support for this module is deprecated and will be removed in version 2.14,"
                        " use connection %s" % pc.connection
                    ]
                )
            else:
                self._task.args["provider"] = ActionModule.eapi_implementation(
                    provider, self._play_context
                )
                warnings.append(
                    [
                        "connection local support for this module is deprecated and will be removed in version 2.14,"
                        " use connection either httpapi or ansible.netcommon.httpapi (whichever is applicable)"
                    ]
                )
        else:
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for this module"
                % self._play_context.connection,
            }

        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if "warnings" in result:
                result["warnings"].extend(warnings)
            else:
                result["warnings"] = warnings
        return result

    @staticmethod
    def eapi_implementation(provider, play_context):
        provider["transport"] = "eapi"

        if provider.get("host") is None:
            provider["host"] = play_context.remote_addr

        if provider.get("port") is None:
            default_port = 443 if provider["use_ssl"] else 80
            provider["port"] = int(play_context.port or default_port)

        if provider.get("timeout") is None:
            provider["timeout"] = C.PERSISTENT_COMMAND_TIMEOUT

        if provider.get("username") is None:
            provider["username"] = play_context.connection_user

        if provider.get("password") is None:
            provider["password"] = play_context.password

        if provider.get("authorize") is None:
            provider["authorize"] = False

        return provider
