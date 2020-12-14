from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    Template,
    dict_merge,
)


class NetworkTemplate(object):
    """ The NetworkTemplate class that Resource Module templates
        inherit and use to parse and render config lines.
    """

    def __init__(self, lines=None, tmplt=None, prefix=None):
        self._lines = lines or []
        self._tmplt = tmplt
        self._template = Template()
        self._prefix = prefix or {}

    def _deepformat(self, tmplt, data):
        wtmplt = deepcopy(tmplt)
        if isinstance(tmplt, str):
            res = self._template(
                value=tmplt, variables=data, fail_on_undefined=False
            )
            return res
        if isinstance(tmplt, dict):
            for tkey, tval in tmplt.items():
                ftkey = self._template(tkey, data)
                if ftkey != tkey:
                    wtmplt.pop(tkey)
                if isinstance(tval, dict):
                    wtmplt[ftkey] = self._deepformat(tval, data)
                elif isinstance(tval, list):
                    wtmplt[ftkey] = [self._deepformat(x, data) for x in tval]
                elif isinstance(tval, str):
                    wtmplt[ftkey] = self._deepformat(tval, data)
                    if wtmplt[ftkey] is None:
                        wtmplt.pop(ftkey)
        return wtmplt

    def parse(self):
        """ parse
        """
        result = {}
        shared = {}
        for line in self._lines:
            for parser in self._tmplt.PARSERS:
                cap = re.match(parser["getval"], line)
                if cap:
                    capdict = cap.groupdict()
                    capdict = dict(
                        (k, v) for k, v in capdict.items() if v is not None
                    )
                    if parser.get("shared"):
                        shared = capdict
                    vals = dict_merge(capdict, shared)
                    res = self._deepformat(deepcopy(parser["result"]), vals)
                    result = dict_merge(result, res)
                    break
        return result

    def get_parser(self, name):
        """ get_parsers
        """
        res = [p for p in self._tmplt.PARSERS if p["name"] == name]
        return res[0]

    def _render(self, tmplt, data, negate):
        try:
            if callable(tmplt):
                res = tmplt(data)
            else:
                res = self._template(
                    value=tmplt, variables=data, fail_on_undefined=False
                )
        except KeyError:
            return None

        if res:
            if negate:
                rem = "{0} ".format(self._prefix.get("remove", "no"))
                if isinstance(res, list):
                    cmd = [(rem + each) for each in res]
                    return cmd
                return rem + res
            elif self._prefix.get("set"):
                set_cmd = "{0} ".format(self._prefix.get("set", ""))
                if isinstance(res, list):
                    cmd = [(set_cmd + each) for each in res]
                    return cmd
                return set_cmd + res
        return res

    def render(self, data, parser_name, negate=False):
        """ render
        """
        if negate:
            tmplt = (
                self.get_parser(parser_name).get("remval")
                or self.get_parser(parser_name)["setval"]
            )
        else:
            tmplt = self.get_parser(parser_name)["setval"]
        command = self._render(tmplt, data, negate)
        return command
