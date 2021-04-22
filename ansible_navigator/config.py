"""
Configuration subsystem for ansible-navigator
"""
import json
import os
import pkgutil

from argparse import ArgumentParser
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from yaml.scanner import ScannerError

from .utils import Sentinel, Singleton, env_var_is_file_path, get_conf_path
from .yaml import yaml, SafeLoader


def generate_editor_command():
    """generate a command for EDITOR is env var is set"""
    if "EDITOR" in os.environ:
        command = "%s {filename}" % os.environ.get("EDITOR")
    else:
        command = "vi +{line_number} {filename}"
    return command


# Contains default values for config options that cannot be expressed in yaml
_DEFAULT_OVERRIDES = {
    'editor-command': generate_editor_command(),
}


def _to_config_list(value: Any) -> Optional[List[str]]:
    """convert a config def to a list of strings"""
    if value is None:
        return value

    if not isinstance(value, list):
        value = [str(value)]

    return [str(v) for v in value]


def _to_config_str(value: Any) -> str:
    """convert a config def to string like value"""
    if value is None:
        raise ValueError("required value is not set")

    if isinstance(value, list):
        value = '. '.join(value)

    if not isinstance(value, str):
        raise ValueError("value is not a string or list of strings")

    value = value.strip()
    if not value.endswith('.'):
        value += '.'

    return value


def _validate_config_dict(value: Any, mandatory: Set, optional: Set, found: List[str]):
    """validates a config dict definition and sets all missing optional keys with a default of None"""
    error_key = " -> ".join(found)
    if not isinstance(value, dict):
        raise ValueError(f"{error_key} def is not a dict")

    actual_keys = set(value.keys())

    missing_keys = mandatory.difference(actual_keys)
    if missing_keys:
        raise ValueError(f"{error_key} def missing mandatory keys: {', '.join(missing_keys)}")

    extra_keys = actual_keys.difference(mandatory.union(optional))
    if extra_keys:
        raise ValueError(f"{error_key} def has extra keys: {', '.join(extra_keys)}")

    missing_optional = optional.difference(actual_keys)
    for missing in missing_optional:
        value[missing] = None


def _get_navigator_config_path() -> Tuple['NavigatorConfigSource', Optional[str]]:
    """gets the user defined config file path if available"""
    config_path = None
    # Check if the conf path is set via an env var
    cfg_env_var = "ANSIBLE_NAVIGATOR_CONFIG"
    env_config_path, _ = env_var_is_file_path(cfg_env_var, "config")

    # Check well know locations
    found_config_path, _ = get_conf_path(
        "ansible-navigator", allowed_extensions=["yml", "yaml", "json"]
    )

    # Pick the envar set first, followed by found, followed by leave as none
    if env_config_path is not None:
        return NavigatorConfigSource.ENVIRONMENT, env_config_path

    elif found_config_path is not None:
        return NavigatorConfigSource.WELL_KNOWN_LOCATION, found_config_path

    else:
        return NavigatorConfigSource.NOT_FOUND, None


def _load_navigator_config(path: str) -> Dict:
    """loads the user defined config file"""
    config = {}
    if path is not None:
        with open(path.encode('utf-8'), "r") as config_fh:
            if path.endswith(".json"):
                try:
                    config = json.load(config_fh)
                except (TypeError, json.decoder.JSONDecodeError) as exe:
                    raise TypeError(f"Invalid JSON config found in file '{path}'. "
                                    f"Failed with '{exe!s}'") from exe
            else:
                try:
                    config = yaml.load(config_fh, Loader=SafeLoader)
                except ScannerError as exe:
                    raise TypeError(f"Invalid YAML config found in file '{path}'. "
                                    f"Failed with '{exe!s}'") from exe

    return config


def _load_config_defs() -> Dict[str, Any]:
    """loads the config definition file, validates and sets the same default values"""
    raw_data = pkgutil.get_data('ansible_navigator.data', 'config.yml')
    config = yaml.load(raw_data.decode('utf-8'), Loader=SafeLoader)

    if not isinstance(config, dict):
        raise ValueError("builtin config.yml is a properly formed config definition file")

    # TODO: Add deprecated and version_added
    mandatory_keys = {'description'}
    optional_keys = {'default', 'choices', 'type', 'elements', 'config', 'env', 'cli'}

    for key, value in config.items():
        _validate_config_dict(value, mandatory_keys, optional_keys, [key])

        # Set sane defaults for the root keys
        if value['type'] is None:
            value['type'] = 'str'

        if key in _DEFAULT_OVERRIDES:
            value['default'] = _DEFAULT_OVERRIDES[key]

        elif value['default'] is None:
            if value['type'] == 'list':
                value['default'] = []
            elif value['type'] == 'dict':
                value['default'] = {}
            else:
                value['default'] = Sentinel

        if value['config'] is None:
            value['config'] = []

        if value['env'] is None:
            value['env'] = []

        if value['cli'] is None:
            value['cli'] = []

        # Convert description to a string
        try:
            value['description'] = _to_config_str(value['description'])
        except ValueError as e:
            raise ValueError(f"{key} -> description def is invalid: {e!s}") from None

        value['choices'] = _to_config_list(value['choices'])

        # Validate the type options are valid
        valid_types = ['bool', 'dict', 'list', 'str']
        if value['type'] not in valid_types:
            raise ValueError(f"{key} -> type def {value['type']!s} is invalid: "
                             f"expecting {', '.join(valid_types)}")

        if value['elements'] and value['elements'] not in valid_types:
            raise ValueError(f"{key} -> elements def {value['elements']!s} is invalid: "
                             f"expecting {', '.join(valid_types)}")
        if value['elements'] is not None and value['type'] != 'list':
            raise ValueError(f"{key} -> elements def cannot be set when type is not list")

        # Validate the config/env/cli defs
        config_value = value['config']
        if not isinstance(config_value, list):
            raise ValueError(f"{key} -> config def is not a list")
        for entry in config_value:
            _validate_config_dict(entry, {'section', 'name'}, set(), [key, 'config'])
            entry['name'] = _to_config_str(entry['name'])
            entry['section'] = _to_config_list(entry['section'])

        env_value = value['env']
        if not isinstance(env_value, list):
            raise ValueError(f"{key} -> env def is not a list")
        for entry in env_value:
            _validate_config_dict(entry, {'name'}, set(), [key, 'env'])
            entry['name'] = str(entry['name'])

        cli_value = value['cli']
        if not isinstance(cli_value, list):
            raise ValueError(f"{key} -> cli def is not a list")
        for entry in cli_value:
            _validate_config_dict(entry, {'name'}, set(), [key, 'cli'])
            entry['name'] = str(entry['name'])

        # Used by argparse to store the arguments to the property with this value
        value['cli_dest'] = key.lower().replace('-', '_')

    return config


class NavigatorConfigSource(Enum):
    """defines the config path source"""
    NOT_FOUND = "no config file found"
    ENVIRONMENT = "ANSIBLE_NAVIGATOR_CONFIG environment value"
    WELL_KNOWN_LOCATION = "well known folder location"


class NavigatorOptionSource(Enum):
    """defines the config option value source"""
    NOT_FOUND = "value was not defined in any option"
    DEFAULT = "default configuration value"
    USER_CFG = "user provided configuration file"
    ENVIRONMENT = "user provided environment variable"
    CLI = "user provided cli argument"


class _ConfigValue:

    def __init__(self, name: str, definition: Dict[str, Any], config: Dict):
        self.name = name
        self._type = definition['type']
        self._elements = definition['elements']
        self._config_def = definition['config']
        self._env_def = definition['env']
        self._cli_def = definition['cli']

        self._values = {
            NavigatorOptionSource.DEFAULT: definition['default']
        }
        for config_def in self._config_def:
            keys = config_def['section']
            keys.append(config_def['name'])

            current_val = config
            for k in keys:
                if not isinstance(current_val, dict):
                    # TODO: Add warning once logging is in place
                    break

                if k not in current_val:
                    current_val = Sentinel
                    break

                current_val = current_val[k]

            if current_val != Sentinel:
                self._set_value(NavigatorOptionSource.USER_CFG, current_val)

        all_env = os.environ
        for env_def in self._env_def:
            if env_def['name'] in all_env:
                self._set_value(NavigatorOptionSource.ENVIRONMENT, os.environ[env_def['name']])
                break

    def get_value(self, sources: List[NavigatorOptionSource]) -> Tuple[NavigatorOptionSource, Any]:
        # Precedence is cli > env > config
        for source in sources:
            if source in self._values:
                return source, self._values[source]

        else:
            return NavigatorOptionSource.NOT_FOUND, Sentinel

    def _set_value(self, source: NavigatorOptionSource, value: Any):
        # FIXME: Validate/cast type/elements
        self._values[source] = value


class NavigatorConfig(metaclass=Singleton):
    """
    Global Navigator config that reads config values from the config file, environment, and cli arguments.
    """

    def __init__(self):
        self._config_source, self._config_path = _get_navigator_config_path()
        self._config = _load_navigator_config(self._config_path) if self._config_path else {}

        self._def = _load_config_defs()
        self._values: Dict[str, _ConfigValue] = {n: _ConfigValue(n, v, self._config) for n, v in self._def.items()}

    def get(self, name: str, default: Any = Sentinel,
            sources: Optional[List[NavigatorOptionSource]] = None) -> Tuple[NavigatorOptionSource, Any]:
        """
        Gets the value of the config option specified by name.
        If the key is found in the config, return the value.
        Otherwise, if a non-Sentinel default is given, return that.
        If after all that the key didn't match or the value wasn't found in
        the sources specified, throw KeyError.

        :param name: The config option name that corresponds with the option
            key in config.yml.
        :type name: str
        :param default: The default value to use if the name isn't a valid
            config or the config wasn't defined in the sources specified.
        :type default: Any
        :param sources: A list of sources to search in, defaults to all sources.
        :type sources: Optional[List[NavigatorOptionSource]]
        :return: The value of the config option specified.
        :rtype: Tuple[NavigatorOptionSource, Any]
        """
        if name not in self._values:
            if default == Sentinel:
                raise KeyError(name)

            return default

        if sources is None:
            sources = [
                NavigatorOptionSource.CLI,
                NavigatorOptionSource.ENVIRONMENT,
                NavigatorOptionSource.USER_CFG,
                NavigatorOptionSource.DEFAULT,
            ]

        source, value = self._values[name].get_value(sources)
        if value == Sentinel:
            if default == Sentinel:
                raise KeyError(name)

            value = default

        return source, value

    def add_argparse_argument(self, name: str, parser: ArgumentParser):
        """
        Gets the argparse definition for the config option specified.

        :param name: The config name to add as an argument.
        :type name: str
        :param parser: The argparse parser to add the config argument to
        :type parser: ArgumentParser
        """
        if name not in self._values:
            raise KeyError(name)

        definition = self._def[name]

        args = [d['name'] for d in definition['cli']]
        kwargs = {
            'help': definition['description'],
            'default': Sentinel,
            'dest': definition['cli_dest'],
        }
        # TODO: add type=path that parses the value as an absolute path (_abs_user_path)
        # TODO: type to validate the input, e.g. bool == str2bool
        # TODO: type=dict should be list with KEY=value
        # TODO: type=list should have nargs="+"
        # TODO: type=list should maybe have action='append'
        # TODO: playbook had nargs="?"

        # TODO: better logic for removing dest on positional args
        if not any([n for n in args if n.startswith('-')]):
            del kwargs['dest']

        if definition['choices']:
            kwargs['choices'] = definition['choices']

        parser.add_argument(*args, **kwargs)
