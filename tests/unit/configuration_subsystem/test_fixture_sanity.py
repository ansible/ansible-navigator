"""Some handy tests to ensure the fixture data has
entries for for all entries.
"""
import os

from ansible_navigator._yaml import Loader
from ansible_navigator._yaml import yaml
from ansible_navigator.configuration_subsystem import NavigatorConfiguration

from .data import ENVVAR_DATA
from .defaults import TEST_FIXTURE_DIR


def test_data_no_missing_envvar_data():
    """Ensure the ENVVAR_DATA covers all entries"""
    entry_names = [entry.name for entry in NavigatorConfiguration.entries]
    data_names = [entry[0] for entry in ENVVAR_DATA]
    assert entry_names == data_names


def test_full_settings_file():
    """Test using a full settings file"""
    settings_file_path = os.path.join(TEST_FIXTURE_DIR, "ansible-navigator.yml")
    with open(file=settings_file_path, encoding="utf-8") as file:
        settings_contents = yaml.load(file, Loader=Loader)
    for entry in NavigatorConfiguration.entries:
        path = entry.settings_file_path("ansible-navigator")
        expected = settings_contents
        for key in path.split("."):
            expected = expected[key]
