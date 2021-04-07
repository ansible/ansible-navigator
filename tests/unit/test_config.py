import pytest

from ansible_navigator.config import NavigatorConfig
from ansible_navigator.utils import Sentinel

SAMPLE_CUSTOM_CONFIG = {
    "ansible-navigator": {
        "editor": {
            "command": "emacs -nw +{line_number} {filename}",
            "console": False,
        },
        "doc-plugin-type": "become",
        "log": {
            "level": "critical",
        },
    },
}


@pytest.mark.parametrize(
    "dct, keys, default, expected",
    [
        (
            SAMPLE_CUSTOM_CONFIG,
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            ("user provided config file", "emacs -nw +{line_number} {filename}"),
        ),
        (
            {},
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            ("default configuration", "vi +{line_number} {filename}"),
        ),
        (
            {},
            ["ansible-navigator", "editor", "command"],
            "nano {filename}",
            ("argparse default", "nano {filename}"),
        ),
        (
            {"ansible-navigator": {}},
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            ("default configuration", "vi +{line_number} {filename}"),
        ),
    ],
    ids=[
        "valid sample config, valid key",
        "empty config, default default, valid key",
        "empty config, custom default, valid key",
        "config that has some levels but not all the keys we need, valid key",
    ],
)
def test_config_get(dct, keys, default, expected):
    """
    Test that NavigatorConfig.get() works in the normal case.
    """
    cfg = NavigatorConfig(dct)
    assert cfg.get(keys, default) == expected


@pytest.mark.parametrize(
    "dct, keys, default, expected",
    [
        (
            SAMPLE_CUSTOM_CONFIG,
            ["ansible-navigator", "editor", "doesnotexist"],
            Sentinel,
            pytest.raises(KeyError),
        ),
    ],
    ids=[
        "valid config, invalid key",
    ],
)
def test_config_get_keyerror(dct, keys, default, expected):
    """
    Test that when everything else fails, including default lookup, we raise
    KeyError as expected.
    """
    with expected:
        cfg = NavigatorConfig(dct)
        assert cfg.get(keys, default)
