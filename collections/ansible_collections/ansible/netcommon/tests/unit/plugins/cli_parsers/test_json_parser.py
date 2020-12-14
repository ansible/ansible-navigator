# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.plugins.cli_parsers.json_parser import (
    CliParser,
)


class TestJsonParser(unittest.TestCase):
    def test_json_parser(self):
        test_value = {
            "string": "This is a string",
            "list": ["This", "is", "a", "list"],
            "bool": True,
            "int": 27,
            "dict": {
                "This": "string",
                "is": ["l", "i", "s", "t"],
                "a": True,
                "dict": 42,
            },
        }
        task_args = {"text": json.dumps(test_value)}
        parser = CliParser(task_args=task_args, task_vars=[], debug=False)

        result = parser.parse()
        self.assertEqual(result, {"parsed": test_value})

    def test_invalid_json(self):
        task_args = {"text": "Definitely not JSON"}
        parser = CliParser(task_args=task_args, task_vars=[], debug=False)

        result = parser.parse()
        # Errors are different between Python 2 and 3, so we have to be a bit roundabout.
        self.assertEqual(len(result), 1)
        assert "errors" in result
        self.assertEqual(len(result["errors"]), 1)
