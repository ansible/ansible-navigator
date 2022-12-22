# cspell:ignore ecmd
"""Utility functions used by adjacent tests."""

from ansible_navigator.configuration_subsystem.definitions import SettingsEntry


def id_for_base(val):
    """Return an id for a param set."""
    if val is None:
        return "No base params"
    if "editor-command" in val:
        return "Long base params"
    if "ecmd" in val:
        return "Short base params"
    return "Unknown base params"


def id_for_cli(val):
    """Generate an id for a CLI entry."""
    if isinstance(val, str):
        return val
    return ""


def id_for_name(val):
    """Return an id based on entry name."""
    if isinstance(val, SettingsEntry):
        return f"{val.name}"
    return ""


def config_post_process(expected, path):
    """Perform custom post processing on the configuration."""
    if path == "ansible-navigator.execution-environment.volume-mounts":
        parsed_volume_mounts = []
        volume_mounts = expected["ansible-navigator"]["execution-environment"]["volume-mounts"]
        for volume_mount in volume_mounts:
            mount_path = f"{volume_mount['src']}:{volume_mount['dest']}"
            if volume_mount.get("options"):
                mount_path += f":{volume_mount['options']}"
            parsed_volume_mounts.append(mount_path)
        expected["ansible-navigator"]["execution-environment"][
            "volume-mounts"
        ] = parsed_volume_mounts

    return expected
