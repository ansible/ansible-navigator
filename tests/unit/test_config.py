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
    "dct, keys, default, exp_source, exp_value",
    [
        (
            SAMPLE_CUSTOM_CONFIG,
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            "USER_CFG",
            "emacs -nw +{line_number} {filename}",
        ),
        (
            {},
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            "DEFAULT_CFG",
            "vi +{line_number} {filename}",
        ),
        (
            {},
            ["ansible-navigator", "editor", "command"],
            "nano {filename}",
            "ARGPARSE_DEFAULT",
            "nano {filename}",
        ),
        (
            {"ansible-navigator": {}},
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            "DEFAULT_CFG",
            "vi +{line_number} {filename}",
        ),
    ],
    ids=[
        "valid sample config, valid key",
        "empty config, default default, valid key",
        "empty config, custom default, valid key",
        "config that has some levels but not all the keys we need, valid key",
    ],
)
def test_config_get(dct, keys, default, exp_source, exp_value):
    """
    Test that NavigatorConfig.get() works in the normal case.
    """
    cfg = NavigatorConfig(dct)
    recv_source, recv_value = cfg.get(keys, default)
    assert exp_source == recv_source.name
    assert exp_value == recv_value


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
