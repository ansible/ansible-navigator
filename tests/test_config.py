import pytest

from ansible_navigator.config import NavigatorConfig
from ansible_navigator.utils import Sentinel


SAMPLE_CUSTOM_CONFIG = {
    "ansible-navigator": {
        "editor": {
            "command": "emacs -nw +{line_number} {filename}",
            "console": False,
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
            "emacs -nw +{line_number} {filename}",
        ),
        (
            {},
            ["ansible-navigator", "editor", "command"],
            Sentinel,
            "vi +{line_number} {filename}",
        ),
        (
            {},
            ["ansible-navigator", "editor", "command"],
            "nano {filename}",
            "nano {filename}",
        ),
        (
            {"ansible-navigator": {}},
            ["ansible-navigator", "editor", "command"],
            Sentinel,
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
def test_config_get(dct, keys, default, expected):
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
    with expected:
        cfg = NavigatorConfig(dct)
        assert cfg.get(keys, default)
