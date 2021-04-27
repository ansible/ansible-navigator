""" utility func used by adjacent tests
"""
import os
from copy import deepcopy


from ansible_navigator.configuration import ApplicationConfiguration
from ansible_navigator.configuration import Configuration

from ansible_navigator.configuration.definitions import Entry

from ansible_navigator.yaml import yaml
from ansible_navigator.yaml import Loader

from ...defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "unit", "configuration")


def generate_config(params=None, setting_file_name=None):
    """Generate a configuration given a settings file"""
    if params is None:
        params = []

    if setting_file_name:
        settings_file_path = os.path.join(TEST_FIXTURE_DIR, setting_file_name)
        with open(settings_file_path) as file:
            settings_contents = yaml.load(file, Loader=Loader)
    else:
        settings_file_path = None
        settings_contents = {}

    application_configuration = deepcopy(ApplicationConfiguration)
    configuration = Configuration(
        application_configuration=application_configuration,
        params=params,
        settings_file_path=settings_file_path,
    )
    configuration.configure()
    return application_configuration, settings_contents


def generate_params_from_entries(setting_file_name):
    """Generate params from a configurations' entries"""
    application_configuration, settings_contents = generate_config(
        setting_file_name=setting_file_name
    )
    argvalues = [(entry, settings_contents) for entry in application_configuration.entries]
    ids = [entry.name for entry in application_configuration.entries]
    return argvalues, ids


def id_for_base(val):
    """Return an id for a param set"""
    if val is None:
        return "No base params"
    if "editor-command" in val:
        return "Long base params"
    if "ecmd" in val:
        return "Short base params"
    return "Unknown base params"


def id_for_cli(val):
    if isinstance(val, str):
        return val
    return ""


def id_for_name(val):
    """Return an id based on entry name"""
    if isinstance(val, Entry):
        return val.name
    return ""


def id_for_settings(val):
    if val in ["DEFAULT_CFG", "USER_CFG"]:
        return f"others={val}"
    if val == "ansible-navigator_empty.yml":
        return "empty settings file"
    if val == "ansible-navigator.yml":
        return "full settings file"
    return val
