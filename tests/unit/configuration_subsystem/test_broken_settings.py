"""test using broken settings files
"""
import os


def test_broken_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for broken settings file"""
    response = generate_config(setting_file_name="ansible-navigator_broken.yml")
    assert len(response.errors) == 1
    error = "Errors encountered when loading settings file:"
    assert response.errors[0].startswith(error)


def test_garbage_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for garbage settings file"""
    response = generate_config(setting_file_name=os.path.abspath(__file__))
    error = "but failed to load it."
    assert response.errors[0].endswith(error), response.errors
