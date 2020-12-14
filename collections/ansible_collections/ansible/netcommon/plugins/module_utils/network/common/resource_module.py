from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_empties,
    to_list,
    get_from_dict,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network import (
    get_resource_connection,
)


class ResourceModule(object):  # pylint: disable=R0902
    """ Base class for Network Resource Modules
    """

    ACTION_STATES = ["merged", "replaced", "overridden", "deleted"]

    def __init__(self, *_args, **kwargs):
        self._empty_fact_val = kwargs.get("empty_fact_val", [])
        self._facts_module = kwargs.get("facts_module", None)
        self._gather_subset = kwargs.get("gather_subset", ["!all", "!min"])
        self._module = kwargs.get("module", None)
        self._resource = kwargs.get("resource", None)
        self._tmplt = kwargs.get("tmplt", None)

        self._connection = None
        self.state = self._module.params["state"]
        self.want = remove_empties(self._module.params).get(
            "config", self._empty_fact_val
        )
        # Error out if empty config is passed for following states
        if (
            self.state in ("overridden", "merged", "replaced", "rendered")
            and not self.want
        ):
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    self.state
                )
            )

        self.before = self.gather_current()
        self.have = deepcopy(self.before)
        self.changed = False
        self.commands = []
        self.warnings = []

        self._get_connection()

    def gather_current(self):
        data = None
        if self.state == "rendered":
            return self._empty_fact_val
        elif self.state == "parsed":
            data = self._module.params["running_config"]
            if not data:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
        return deepcopy(self.get_facts(self._empty_fact_val, data=data))

    @property
    def result(self):
        """ Compute the final result
        """
        result = {"warnings": self.warnings}
        if self.state not in self.ACTION_STATES:
            if self.state == "gathered":
                result["gathered"] = self.before
            elif self.state == "parsed":
                result["parsed"] = self.before
            elif self.state == "rendered":
                result["rendered"] = self.commands
        else:
            result["commands"] = self.commands
            result["before"] = self.before
            if self.commands:
                result["after"] = self.get_facts(self._empty_fact_val)
        result["changed"] = self.changed
        return result

    def addcmd(self, data, tmplt, negate=False):
        """ addcmd
        """
        command = self._tmplt.render(data, tmplt, negate)
        if command:
            self.commands.extend(to_list(command))

    def addcmd_first_found(self, data, tmplts, negate=False):
        """ addcmd first found
        """
        for pname in tmplts:
            before = len(self.commands)
            self.addcmd(data, pname, negate)
            if len(self.commands) != before:
                break

    def get_facts(self, empty_val=None, data=None):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        if empty_val is None:
            empty_val = []
        facts, _warnings = self._facts_module.get_facts(
            legacy_facts_type=self._gather_subset,
            resource_facts_type=[self._resource],
            data=data,
        )
        facts = facts["ansible_network_resources"].get(self._resource)
        if not facts:
            return empty_val
        return facts

    def _get_connection(self):
        if self.state not in ["rendered", "parsed"]:
            if self._connection:
                return self._connection
            self._connection = get_resource_connection(self._module)
            return self._connection
        return None

    def compare(self, parsers, want=None, have=None):
        """ Run through all the parsers and compare
            the want and have dicts
        """
        if want is None:
            want = self.want
        if have is None:
            have = self.have
        for parser in to_list(parsers):
            compval = self._tmplt.get_parser(parser).get("compval")
            if not compval:
                compval = parser
            inw = get_from_dict(want, compval)
            inh = get_from_dict(have, compval)

            if isinstance(inw, dict) and inw.get("set") is False and not inh:
                continue

            if inw is not None and inw != inh:
                if isinstance(inw, bool):
                    if inw is False and inh is None:
                        continue
                    self.addcmd(want, parser, not inw)
                else:
                    self.addcmd(want, parser, False)
            elif inw is None and inh is not None:
                if isinstance(inh, bool):
                    self.addcmd(have, parser, inh)
                else:
                    self.addcmd(have, parser, True)

    def run_commands(self):
        """ Send commands to the device
        """
        if self.commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(self.commands)
            self.changed = True
