from typing import Any, Dict, List

from .utils import Sentinel

# TODO: This maybe can/should move to a yaml file in some data (not share) dir
# at some point in the future. In any case, the structure here should mimic what
# we'd expect the yaml file to parse to. Every config option should have a
# default here.
_DEFAULTS = {
    "ansible-navigator": {
        "editor": {
            "command": "vi +{line_number} {filename}",
            "console": True,
        },
    },
}


class NavigatorConfig:
    def __init__(self, dct: Dict):
        self.config = dct

    def get(self, keys: List[str], default: Any = Sentinel) -> Any:
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
            return current

        # If we made it here, the config key wasn't found.
        if default is not Sentinel:
            return default

        current = _DEFAULTS
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                break
        else:
            return current

        raise KeyError(keys)
