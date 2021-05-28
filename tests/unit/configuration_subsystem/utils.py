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
        return f" {val.name} "
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


def config_post_process(expected, path):
    if path == "ansible-navigator.execution-environment.volume-mounts":
        parsed_volume_mounts = []
        volume_mounts = expected["ansible-navigator"]["execution-environment"]["volume-mounts"]
        for vm in volume_mounts:
            mount_path = f"{vm['src']}:{vm['dest']}"
            if vm.get("label"):
                mount_path += f":{vm['label']}"
            parsed_volume_mounts.append(mount_path)
        expected["ansible-navigator"]["execution-environment"][
            "volume-mounts"
        ] = parsed_volume_mounts

    return expected
