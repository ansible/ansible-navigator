"""
textfsm parser

This is the textfsm parser for use with the cli_parse module and action plugin
https://github.com/google/textfsm
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import missing_required_lib
from ansible_collections.ansible.netcommon.plugins.module_utils.cli_parser.cli_parserbase import (
    CliParserBase,
)

try:
    import textfsm

    HAS_TEXTFSM = True
except ImportError:
    HAS_TEXTFSM = False


class CliParser(CliParserBase):
    """ The textfsm parser class
    Convert raw text to structured data using textfsm
    """

    DEFAULT_TEMPLATE_EXTENSION = "textfsm"
    PROVIDE_TEMPLATE_CONTENTS = False

    @staticmethod
    def _check_reqs():
        """ Check the prerequisites for the textfsm parser

        :return dict: A dict with errors or a template_path
        """
        errors = []

        if not HAS_TEXTFSM:
            errors.append(missing_required_lib("textfsm"))

        return {"errors": errors}

    def parse(self, *_args, **_kwargs):
        """ Std entry point for a cli_parse parse execution

        :return: Errors or parsed text as structured data
        :rtype: dict

        :example:

        The parse function of a parser should return a dict:
        {"errors": [a list of errors]}
        or
        {"parsed": obj}
        """
        cli_output = self._task_args.get("text")
        res = self._check_reqs()
        if res.get("errors"):
            return {"errors": res.get("errors")}

        try:
            template = open(self._task_args.get("parser").get("template_path"))
        except IOError as exc:
            return {"error": to_native(exc)}

        re_table = textfsm.TextFSM(template)
        fsm_results = re_table.ParseText(cli_output)

        results = list()
        for item in fsm_results:
            results.append(dict(zip(re_table.header, item)))

        return {"parsed": results}
