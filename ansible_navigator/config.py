"""
Configuration subsystem for ansible-navigator
"""
import os

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from .utils import Sentinel

# TODO: This maybe can/should move to a yaml file in some data (not share) dir
# at some point in the future. In any case, the structure here should mimic what
# we'd expect the yaml file to parse to. Every config option should have a
# default here, ideally.
#
# NOTE!!! If you change any default here, update the documentation file in
#         docs/configuration.rst


def generate_editor_command():
    """generate a command for EDITOR is env var is set"""
    if "EDITOR" in os.environ:
        command = "%s {filename}" % os.environ.get("EDITOR")
    else:
        command = "vi +{line_number} {filename}"
    return command


_DEFAULTS = {
    "ansible-navigator": {
        "container-engine": "podman",
        "doc-plugin-type": "module",
        "editor": {
            "command": generate_editor_command(),
            "console": True,
        },
        "execution-environment": True,
        "execution-environment-image": "quay.io/ansible/ansible-runner:devel",
        "inventory": [],
        "inventory-columns": [],
        "log": {
            "file": "./ansible-navigator.log",
            "level": "info",
        },
        "mode": "interactive",
        "no-osc4": False,
        "pass-environment-variable": [],
        "playbook": "",
        "playbook-artifact": "{playbook_dir}/{playbook_name}-artifact-{ts_utc}.json",
        "set-environment-variable": {},
    },
}

# This maps argparse destination variables to config paths
ROOT = "ansible-navigator"
ARGPARSE_TO_CONFIG = {
    "container_engine": [ROOT, "container-engine"],
    "editor_command": [ROOT, "editor", "command"],
    "editor_console": [ROOT, "editor", "console"],
    "execution_environment": [ROOT, "execution-environment"],
    "execution_environment_image": [ROOT, "execution-environment-image"],
    "inventory": [ROOT, "inventory"],
    "inventory_columns": [ROOT, "inventory-columns"],
    "logfile": [ROOT, "log", "file"],
    "loglevel": [ROOT, "log", "level"],
    "mode": [ROOT, "mode"],
    "pass_environment_variable": [ROOT, "pass-environment-variable"],
    "playbook": [ROOT, "playbook"],
    "playbook_artifact": [ROOT, "playbook-artifact"],
    "set_environment_variable": [ROOT, "set-environment-variable"],
    "no_osc4": [ROOT, "no-osc4"],
    "type": [ROOT, "doc-plugin-type"],
}


class NavigatorConfig:  # pylint: disable=too-few-public-methods
    """
    A simple wrapper around a dict, with a method that handles defaults nicely.
    """

    def __init__(self, dct: Dict):
        self.config = dct

    def get(self, keys: List[str], default: Any = Sentinel) -> Tuple[str, Any]:
        """
        Takes a list of keys that correspond to nested keys in config.
        If the key is found in the config, return the value.
        Otherwise, if a non-Sentinel default is given, return that.
        Lastly look to the internal default config [defined above] and pull
        out the value from there.

        If after all that the key didn't match, throw KeyError.
        """
        current = self.config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                break
        else:
            return "user provided config file", current

        # If we made it here, the config key wasn't found.
        if default is not Sentinel:
            return "argparse default", default

        current = _DEFAULTS
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                break
        else:
            return "default configuration", current

        raise KeyError(keys)
