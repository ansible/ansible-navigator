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

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    patch,
    MagicMock,
)
from ansible_collections.ansible.netcommon.plugins.modules import cli_config
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)
from .cli_module import TestCliModule


class TestCliConfigModule(TestCliModule):

    module = cli_config

    def setUp(self):
        super(TestCliConfigModule, self).setUp()

        self.mock_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.modules.cli_config.Connection"
        )
        self.get_connection = self.mock_connection.start()

        self.conn = self.get_connection()
        self.conn.get_capabilities.return_value = "{}"

    def tearDown(self):
        super(TestCliConfigModule, self).tearDown()

        self.mock_connection.stop()

    @patch(
        "ansible_collections.ansible.netcommon.plugins.modules.cli_config.run"
    )
    def test_cli_config_backup_returns__backup__(self, run_mock):
        args = dict(backup=True)
        set_module_args(args)

        run_mock.return_value = {}

        result = self.execute_module()
        self.assertIn("__backup__", result)

    def test_cli_config_onbox_diff(self):
        self.conn.get_capabilities.return_value = (
            '{"device_operations": {"supports_onbox_diff": true}}'
        )
        set_module_args({"config": "set interface eth0 ip address dhcp"})
        self.execute_module()
        self.conn.edit_config.assert_called_once_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=None,
            comment=None,
        )

    def test_cli_config_generate_diff(self):
        self.conn.get_capabilities.return_value = (
            '{"device_operations": {"supports_generate_diff": true}}'
        )
        diff = MagicMock()
        diff.get.side_effect = ["set interface eth0 ip address dhcp", None]
        self.conn.get_diff.return_value = diff
        set_module_args({"config": "set interface eth0 ip address dhcp"})
        self.execute_module(
            changed=True, commands=["set interface eth0 ip address dhcp"]
        )
        self.conn.edit_config.assert_called_once_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=None,
            comment=None,
        )

        diff.get.side_effect = [None, "new banner"]
        self.conn.get_diff.return_value = diff
        set_module_args({"config": "set banner\nnew banner"})
        self.execute_module(changed=True)
        self.conn.edit_banner.assert_called_once_with(
            candidate='"new banner"', commit=True
        )

    def test_cli_config_replace(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true,
                "supports_replace": true
            }
        }"""
        self.conn.edit_config.return_value = {
            "diff": "set interface eth0 ip address dhcp"
        }

        args = {"config": "set interface eth0 ip address dhcp"}

        args["replace"] = True
        set_module_args(args)
        self.execute_module(changed=True)
        self.conn.edit_config.assert_called_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=True,
            comment=None,
        )

        args["replace"] = False
        set_module_args(args)
        self.execute_module(changed=True)
        self.conn.edit_config.assert_called_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=False,
            comment=None,
        )

    def test_cli_config_replace_unsupported(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true,
                "supports_replace": false
            }
        }"""

        args = {
            "config": "set interface eth0 ip address dhcp",
            "replace": True,
        }
        set_module_args(args)
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"], "Option replace is not supported on this platform"
        )

    def test_cli_config_replace_unspecified(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true
            }
        }"""

        args = {
            "config": "set interface eth0 ip address dhcp",
            "replace": True,
        }
        set_module_args(args)
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"],
            "This platform does not specify whether replace is supported or not. Please report an issue against this platform's cliconf plugin.",
        )

    def test_cli_config_rollback(self):
        self.conn.rollback.return_value = {
            "diff": "set interface eth0 ip address dhcp"
        }

        args = {"rollback": 123456}
        set_module_args(args)
        self.execute_module(changed=True)

        self.conn.rollback.return_value = {}
        set_module_args(args)
        self.execute_module(changed=False)
