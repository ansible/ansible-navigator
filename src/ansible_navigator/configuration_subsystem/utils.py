"""Utilities related to the configuration subsystem."""
from typing import Dict
from typing import Union


SettingsFileSample = Dict[str, Union[Dict, str]]


def create_settings_file_sample(
    settings_path: str,
    placeholder: str = "",
) -> SettingsFileSample:
    """Generate a settings file sample.

    :param settings_path: The dot delimited settings file path for a settings entry
    :param placeholder: String used to identify the placement of a settings value
    :returns: A sample of the settings file
    """
    if "." not in settings_path:
        return {settings_path: placeholder}
    key, remainder = settings_path.split(".", 1)
    return {key: create_settings_file_sample(remainder, placeholder)}
