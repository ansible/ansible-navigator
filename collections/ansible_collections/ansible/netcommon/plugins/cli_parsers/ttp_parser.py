"""
ttp parser

This is the ttp parser for use with the cli_parse module and action plugin
https://github.com/dmulyalin/ttp
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import missing_required_lib
from ansible_collections.ansible.netcommon.plugins.module_utils.cli_parser.cli_parserbase import (
    CliParserBase,
)

try:
    from ttp import ttp

    HAS_TTP = True
except ImportError:
    HAS_TTP = False


class CliParser(CliParserBase):
    """ The ttp parser class
    Convert raw text to structured data using ttp
    """

    DEFAULT_TEMPLATE_EXTENSION = "ttp"
    PROVIDE_TEMPLATE_CONTENTS = False

    @staticmethod
    def _check_reqs():
        """ Check the prerequisites for the ttp parser

        :return dict: A dict with errors or a template_path
        """
        errors = []

        if not HAS_TTP:
            errors.append(missing_required_lib("ttp"))

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
            parser = ttp(
                data=cli_output,
                template=self._task_args.get("parser").get("template_path"),
                vars=self._task_args.get("parser")
                .get("vars", {})
                .get("ttp_vars", {}),
                **self._task_args.get("parser")
                .get("vars", {})
                .get("ttp_init", {})
            )
            parser.parse(one=True)
            results = parser.result(
                **self._task_args.get("parser")
                .get("vars", {})
                .get("ttp_results", {})
            )
        except Exception as exc:
            msg = "Template Text Parser returned an error while parsing. Error: {err}"
            return {"errors": [msg.format(err=to_native(exc))]}
        return {"parsed": results}
