"""Test fixture sanity.

Some handy tests to ensure the fixture data has
entries for for all entries.
"""

from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import yaml

from .data import ENV_VAR_DATA
from .defaults import TEST_FIXTURE_DIR


def test_data_no_missing_env_var_data() -> None:
    """Ensure the ENV_VAR_DATA covers all entries."""
    entry_names = [entry.name for entry in NavigatorConfiguration.entries]
    data_names = [entry.values[0] for entry in ENV_VAR_DATA]
    assert entry_names == data_names


def test_full_settings_file() -> None:
    """Test using a full settings file."""
    settings_file_path = TEST_FIXTURE_DIR / "ansible-navigator.yml"
    with settings_file_path.open(encoding="utf-8") as fh:
        settings_contents = yaml.load(fh, Loader=Loader)
    for entry in NavigatorConfiguration.entries:
        path = entry.settings_file_path("ansible-navigator")
        expected = settings_contents
        for key in path.split("."):
            expected = expected[key]
