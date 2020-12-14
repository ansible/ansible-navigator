# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import tempfile
from ansible.playbook.task import Task
from ansible.template import Templar

from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    MagicMock,
    patch,
)
from ansible_collections.ansible.netcommon.tests.unit.mock.loader import (
    DictDataLoader,
)
from ansible_collections.ansible.netcommon.plugins.action.cli_parse import (
    ActionModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.cli_parser.cli_parserbase import (
    CliParserBase,
)
from ansible.module_utils.connection import (
    ConnectionError as AnsibleConnectionError,
)


class TestCli_Parse(unittest.TestCase):
    def setUp(self):
        task = MagicMock(Task)
        play_context = MagicMock()
        play_context.check_mode = False
        connection = MagicMock()
        fake_loader = DictDataLoader({})
        templar = Templar(loader=fake_loader)
        self._plugin = ActionModule(
            task=task,
            connection=connection,
            play_context=play_context,
            loader=fake_loader,
            templar=templar,
            shared_loader_obj=None,
        )
        self._plugin._task.action = "cli_parse"

    @staticmethod
    def _load_fixture(filename):
        """ Load a fixture from the filesystem

        :param filename: The name of the file to load
        :type filename: str
        :return: The file contents
        :rtype: str
        """
        fixture_name = os.path.join(
            os.path.dirname(__file__), "fixtures", filename
        )
        with open(fixture_name) as fhand:
            return fhand.read()

    def test_fn_debug(self):
        """ Confirm debug doesn't fail and return None
        """
        msg = "some message"
        result = self._plugin._debug(msg)
        self.assertEqual(result, None)

    def test_fn_ail_json(self):
        """ Confirm fail json replaces basic.py in msg
        """
        msg = "text (basic.py)"
        with self.assertRaises(Exception) as error:
            self._plugin._fail_json(msg)
        self.assertEqual("text cli_parse", str(error.exception))

    def test_fn_check_argspec_pass(self):
        """ Confirm a valid argspec passes
        """
        self._plugin._task.args = {
            "text": "text",
            "parser": {
                "name": "ansible.netcommon.pyats",
                "command": "show version",
            },
        }
        result = self._plugin._check_argspec()
        self.assertEqual(result, None)

    def test_fn_check_argspec_fail_no_test_or_command(self):
        """ Confirm failed argpsec w/o text or command
        """
        self._plugin._task.args = {
            "parser": {
                "name": "ansible.netcommon.pyats",
                "command": "show version",
            }
        }
        self._plugin.task_vars = {"ansible_network_os": "cisco.nxos.nxos"}
        with self.assertRaises(Exception) as error:
            self._plugin._check_argspec()
        self.assertEqual(
            "one of the following is required: command, text",
            str(error.exception),
        )

    def test_fn_check_argspec_fail_no_parser_name(self):
        """ Confirm failed argspec no parser name
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {"command": "show version"},
        }
        with self.assertRaises(Exception) as error:
            self._plugin._check_argspec()
        self.assertEqual(
            "missing required arguments: name found in parser",
            str(error.exception),
        )

    def test_fn_extended_check_argspec_parser_name_not_coll(self):
        """ Confirm failed argpsec parser not collection format
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {
                "command": "show version",
                "name": "not_collection_format",
            },
        }
        self._plugin._extended_check_argspec()
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn("including collection", self._plugin._result["msg"])

    def test_fn_extended_check_argspec_missing_tpath_or_command(self):
        """ Confirm failed argpsec missing template_path
        or command when text provided
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {"name": "a.b.c"},
        }
        self._plugin._extended_check_argspec()
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn(
            "provided when parsing text", self._plugin._result["msg"]
        )

    def test_fn_load_parser_pass(self):
        """ Confirm each each of the parsers loads from the filesystem
        """
        parser_names = [
            "json",
            "native",
            "ntc_templates",
            "pyats",
            "textfsm",
            "ttp",
            "xml",
        ]
        for parser_name in parser_names:
            self._plugin._task.args = {
                "text": "anything",
                "parser": {"name": "ansible.netcommon." + parser_name},
            }
            parser = self._plugin._load_parser(task_vars=None)
            self.assertEqual(type(parser).__name__, "CliParser")
            self.assertTrue(hasattr(parser, "parse"))
            self.assertTrue(callable(parser.parse))

    def test_fn_load_parser_fail(self):
        """ Confirm missing parser fails gracefully
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {"name": "a.b.c"},
        }
        parser = self._plugin._load_parser(task_vars=None)
        self.assertIsNone(parser)
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn("No module named", self._plugin._result["msg"])

    def test_fn_set_parser_command_missing(self):
        """ Confirm parser/command is set if missing
        and command provided
        """
        self._plugin._task.args = {
            "command": "anything",
            "parser": {"name": "a.b.c"},
        }
        self._plugin._set_parser_command()
        self.assertEqual(
            self._plugin._task.args["parser"]["command"], "anything"
        )

    def test_fn_set_parser_command_present(self):
        """ Confirm parser/command is not changed if provided
        """
        self._plugin._task.args = {
            "command": "anything",
            "parser": {"command": "something", "name": "a.b.c"},
        }
        self._plugin._set_parser_command()
        self.assertEqual(
            self._plugin._task.args["parser"]["command"], "something"
        )

    def test_fn_set_parser_command_absent(self):
        """ Confirm parser/command is not added
        """
        self._plugin._task.args = {"parser": {}}
        self._plugin._set_parser_command()
        self.assertNotIn("command", self._plugin._task.args["parser"])

    def test_fn_set_text_present(self):
        """ Check task args text is set to stdout
        """
        expected = "output"
        self._plugin._result["stdout"] = expected
        self._plugin._task.args = {}
        self._plugin._set_text()
        self.assertEqual(self._plugin._task.args["text"], expected)

    def test_fn_set_text_absent(self):
        """ Check task args text is set to stdout
        """
        self._plugin._result["stdout"] = None
        self._plugin._task.args = {}
        self._plugin._set_text()
        self.assertNotIn("text", self._plugin._task.args)

    def test_fn_os_from_task_vars(self):
        """ Confirm os is set based on task vars
        """
        checks = [
            ("ansible_network_os", "cisco.nxos.nxos", "nxos"),
            ("ansible_network_os", "NXOS", "nxos"),
            ("ansible_distribution", "Fedora", "fedora"),
            (None, None, ""),
        ]
        for check in checks:
            self._plugin._task_vars = {check[0]: check[1]}
            result = self._plugin._os_from_task_vars()
            self.assertEqual(result, check[2])

    def test_fn_update_template_path_not_exist(self):
        """ Check the creation of the template_path if
        it doesn't exist in the user provided data
        """
        self._plugin._task.args = {
            "parser": {"command": "a command", "name": "a.b.c"}
        }
        self._plugin._task_vars = {"ansible_network_os": "cisco.nxos.nxos"}
        with self.assertRaises(Exception) as error:
            self._plugin._update_template_path("yaml")
        self.assertIn(
            "Could not find or access 'nxos_a_command.yaml'",
            str(error.exception),
        )

    def test_fn_update_template_path_not_exist_os(self):
        """ Check the creation of the template_path if
        it doesn't exist in the user provided data
        name based on os provided in task
        """
        self._plugin._task.args = {
            "parser": {"command": "a command", "name": "a.b.c", "os": "myos"}
        }
        with self.assertRaises(Exception) as error:
            self._plugin._update_template_path("yaml")
        self.assertIn(
            "Could not find or access 'myos_a_command.yaml'",
            str(error.exception),
        )

    def test_fn_update_template_path_mock_find_needle(self):
        """ Check the creation of the template_path
        mock the find needle fn so the template doesn't
        need to be in the default template folder
        """
        template_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "nxos_show_version.yaml"
        )
        self._plugin._find_needle = MagicMock()
        self._plugin._find_needle.return_value = template_path
        self._plugin._task.args = {
            "parser": {"command": "show version", "os": "nxos"}
        }
        self._plugin._update_template_path("yaml")
        self.assertEqual(
            self._plugin._task.args["parser"]["template_path"], template_path
        )

    def test_fn_get_template_contents_pass(self):
        """ Check the retrieval of the template contents
        """
        temp = tempfile.NamedTemporaryFile()
        contents = "abcdef"
        with open(temp.name, "w") as fileh:
            fileh.write(contents)

        self._plugin._task.args = {"parser": {"template_path": temp.name}}
        result = self._plugin._get_template_contents()
        self.assertEqual(result, contents)

    def test_fn_get_template_contents_missing(self):
        """ Check the retrieval of the template contents
        """
        self._plugin._task.args = {"parser": {"template_path": "non-exist"}}
        with self.assertRaises(Exception) as error:
            self._plugin._get_template_contents()
        self.assertIn(
            "Failed to open template 'non-exist'", str(error.exception)
        )

    def test_fn_get_template_contents_not_specified(self):
        """ Check the none when template_path not specified
        """
        self._plugin._task.args = {"parser": {}}
        result = self._plugin._get_template_contents()
        self.assertIsNone(result)

    def test_fn_prune_result_pass(self):
        """ Test the removal of stdout and stdout_lines from the _result
        """
        self._plugin._result["stdout"] = "abc"
        self._plugin._result["stdout_lines"] = "abc"
        self._plugin._prune_result()
        self.assertNotIn("stdout", self._plugin._result)
        self.assertNotIn("stdout_lines", self._plugin._result)

    def test_fn_prune_result_not_exist(self):
        """ Test the removal of stdout and stdout_lines from the _result
        """
        self._plugin._prune_result()
        self.assertNotIn("stdout", self._plugin._result)
        self.assertNotIn("stdout_lines", self._plugin._result)

    def test_fn_run_command_lx_rc0(self):
        """ Check run command for non network
        """
        response = "abc"
        self._plugin._connection.socket_path = None
        self._plugin._low_level_execute_command = MagicMock()
        self._plugin._low_level_execute_command.return_value = {
            "rc": 0,
            "stdout": response,
            "stdout_lines": response,
        }
        self._plugin._task.args = {"command": "ls"}
        self._plugin._run_command()
        self.assertEqual(self._plugin._result["stdout"], response)
        self.assertEqual(self._plugin._result["stdout_lines"], response)

    def test_fn_run_command_lx_rc1(self):
        """ Check run command for non network
        """
        response = "abc"
        self._plugin._connection.socket_path = None
        self._plugin._low_level_execute_command = MagicMock()
        self._plugin._low_level_execute_command.return_value = {
            "rc": 1,
            "stdout": None,
            "stdout_lines": None,
            "stderr": response,
        }
        self._plugin._task.args = {"command": "ls"}
        self._plugin._run_command()
        self.assertTrue(self._plugin._result["failed"])
        self.assertEqual(self._plugin._result["msg"], response)

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_command_network(self, mock_rpc):
        """ Check run command for network
        """
        expected = "abc"
        mock_rpc.return_value = expected
        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        self._plugin._task.args = {"command": "command"}
        self._plugin._run_command()
        self.assertEqual(self._plugin._result["stdout"], expected)
        self.assertEqual(self._plugin._result["stdout_lines"], [expected])

    def test_fn_run_command_not_specified(self):
        """ Check run command for network
        """
        self._plugin._task.args = {"command": None}
        result = self._plugin._run_command()
        self.assertIsNone(result)

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_pass_w_fact(self, mock_rpc):
        """ Check full module run with valid params
        """
        mock_out = self._load_fixture("nxos_show_version.txt")
        mock_rpc.return_value = mock_out
        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        template_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "nxos_show_version.yaml"
        )
        self._plugin._task.args = {
            "command": "show version",
            "parser": {
                "name": "ansible.netcommon.native",
                "template_path": template_path,
            },
            "set_fact": "new_fact",
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result["stdout"], mock_out)
        self.assertEqual(result["stdout_lines"], mock_out.splitlines())
        self.assertEqual(result["parsed"]["version"], "9.2(2)")
        self.assertEqual(
            result["ansible_facts"]["new_fact"]["version"], "9.2(2)"
        )

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_pass_wo_fact(self, mock_rpc):
        """ Check full module run with valid params
        """
        mock_out = self._load_fixture("nxos_show_version.txt")
        mock_rpc.return_value = mock_out
        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        template_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "nxos_show_version.yaml"
        )
        self._plugin._task.args = {
            "command": "show version",
            "parser": {
                "name": "ansible.netcommon.native",
                "template_path": template_path,
            },
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result["stdout"], mock_out)
        self.assertEqual(result["stdout_lines"], mock_out.splitlines())
        self.assertEqual(result["parsed"]["version"], "9.2(2)")
        self.assertNotIn("ansible_facts", result)

    def test_fn_run_fail_argspec(self):
        """ Check full module run with invalid params
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {
                "command": "show version",
                "name": "not_collection_format",
            },
        }
        self._plugin.run(task_vars=None)
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn("including collection", self._plugin._result["msg"])

    def test_fn_run_fail_command(self):
        """ Confirm clean fail with rc 1
        """
        self._plugin._connection.socket_path = None
        self._plugin._low_level_execute_command = MagicMock()
        self._plugin._low_level_execute_command.return_value = {
            "rc": 1,
            "stdout": None,
            "stdout_lines": None,
            "stderr": None,
        }
        self._plugin._task.args = {
            "command": "ls",
            "parser": {"name": "a.b.c"},
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        expected = {
            "failed": True,
            "msg": None,
            "stdout": None,
            "stdout_lines": None,
        }
        self.assertEqual(result, expected)

    def test_fn_run_fail_missing_parser(self):
        """Confirm clean fail with missing parser
        """
        self._plugin._task.args = {"text": None, "parser": {"name": "a.b.c"}}
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result["failed"], True)
        self.assertIn("Error loading parser", result["msg"])

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_pass_empty_parser(self, mock_rpc):
        """ Check full module run with valid params
        """
        mock_out = self._load_fixture("nxos_show_version.txt")
        mock_rpc.return_value = mock_out
        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        template_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "nxos_empty_parser.yaml"
        )
        self._plugin._task.args = {
            "command": "show version",
            "parser": {
                "name": "ansible.netcommon.native",
                "template_path": template_path,
            },
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result["failed"], True)
        self.assertIn("Native parser returned an error", result["msg"])

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_pass_missing_parser_constants(self, mock_rpc):
        """ Check full module run using parser w/o
        DEFAULT_TEMPLATE_EXTENSION or PROVIDE_TEMPLATE_CONTENTS
        defined in the parser
        """
        mock_out = self._load_fixture("nxos_show_version.txt")

        class CliParser(CliParserBase):
            def parse(self, *_args, **kwargs):
                return {"parsed": mock_out}

        self._plugin._load_parser = MagicMock()
        self._plugin._load_parser.return_value = CliParser(None, None, None)

        mock_out = self._load_fixture("nxos_show_version.txt")
        mock_rpc.return_value = mock_out

        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        template_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "nxos_empty_parser.yaml"
        )
        self._plugin._task.args = {
            "command": "show version",
            "parser": {
                "name": "ansible.netcommon.native",
                "template_path": template_path,
            },
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result["stdout"], mock_out)
        self.assertEqual(result["stdout_lines"], mock_out.splitlines())
        self.assertEqual(result["parsed"], mock_out)

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_pass_missing_parser_in_parser(self, mock_rpc):
        """ Check full module run using parser w/o
        a parser function defined in the parser
        defined in the parser
        """
        mock_out = self._load_fixture("nxos_show_version.txt")

        class CliParser(CliParserBase):
            pass

        self._plugin._load_parser = MagicMock()
        self._plugin._load_parser.return_value = CliParser(None, None, None)

        mock_out = self._load_fixture("nxos_show_version.txt")
        mock_rpc.return_value = mock_out

        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        template_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "nxos_empty_parser.yaml"
        )
        self._plugin._task.args = {
            "command": "show version",
            "parser": {
                "name": "ansible.netcommon.native",
                "template_path": template_path,
            },
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=task_vars)
        self.assertIn("Unhandled", str(error.exception))

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_net_device_error(self, mock_rpc):
        """ Check full module run mock error from network device
        """
        msg = "I was mocked"
        mock_rpc.side_effect = AnsibleConnectionError(msg)
        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        self._plugin._task.args = {
            "command": "show version",
            "parser": {"name": "ansible.netcommon.native"},
        }
        task_vars = {"inventory_hostname": "mockdevice"}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result["failed"], True)
        self.assertEqual([msg], result["msg"])
