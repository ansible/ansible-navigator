# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from collections import OrderedDict

import pytest

from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.plugins.cli_parsers.xml_parser import (
    CliParser,
)

xmltodict = pytest.importorskip("xmltodict")


class TestXmlParser(unittest.TestCase):
    def test_valid_xml(self):
        xml = "<tag1><tag2 arg='foo'>text</tag2></tag1>"
        xml_dict = OrderedDict(
            tag1=OrderedDict(
                tag2=OrderedDict([("@arg", "foo"), ("#text", "text")])
            )
        )
        task_args = {"text": xml, "parser": {"os": "none"}}
        parser = CliParser(task_args=task_args, task_vars=[], debug=False)

        result = parser.parse()
        self.assertEqual(result["parsed"], xml_dict)

    def test_invalid_xml(self):
        task_args = {"text": "Definitely not XML", "parser": {"os": "none"}}
        parser = CliParser(task_args=task_args, task_vars=[], debug=False)

        result = parser.parse()
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(
            result["errors"][0],
            "XML parser returned an error while parsing. Error: syntax error: line 1, column 0",
        )
