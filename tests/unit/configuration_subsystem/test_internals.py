"""Test the internals of a NavigatorConfiguration"""

import os

from .defaults import TEST_FIXTURE_DIR


def test_settings_file_path_provided(generate_config):
    """Test a settings file path is stored in the internals when provided"""
    settings_file = "ansible-navigator.yml"
    settings_file_path = os.path.join(TEST_FIXTURE_DIR, settings_file)
    response = generate_config(setting_file_name="ansible-navigator.yml")
    assert response.application_configuration.internals.settings_file_path == settings_file_path


def test_settings_file_path_not_provided(generate_config):
    """Test a settings file path is stored in the internals as None"""
    response = generate_config()
    assert response.application_configuration.internals.settings_file_path is None
