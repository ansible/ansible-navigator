""" utility func used by adjacent tests
"""

from ansible_navigator.configuration_subsystem.definitions import Entry


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
    """Generate an id for a cli entry"""
    if isinstance(val, str):
        return val
    return ""


def id_for_name(val):
    """Return an id based on entry name"""
    if isinstance(val, Entry):
        return val.name
    return ""


def id_for_settings(val):
    """Generate an id for a settings entry"""
    if val in ["DEFAULT_CFG", "USER_CFG"]:
        return f"others={val}"
    if val == "ansible-navigator_empty.yml":
        return "empty settings file"
    if val == "ansible-navigator.yml":
        return "full settings file"
    return val
