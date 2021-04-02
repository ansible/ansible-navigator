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


@pytest.fixture
def config():
    return NavigatorConfig(SAMPLE_CUSTOM_CONFIG)


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


# TODO: Maybe move to test_cli.py
@pytest.mark.parametrize(
    "given, argname, expected",
    [
        (
            ["doc", "-t", "callback", "oneline"],
            "type",
            "callback",
        ),
        (
            ["doc", "sudo"],
            "type",
            "become",
        ),
        (
            ["doc", "-t", "become", "sudo"],
            "type",
            "become",
        ),
        (
            ["config"],
            "ee_image",
            "quay.io/ansible/ansible-runner:devel",
        ),
        (
            ["config"],
            "loglevel",
            "critical",
        ),
        (
            ["config", "--loglevel", "debug"],
            "loglevel",
            "debug",
        ),
    ],
    ids=[
        "commandline overrides config file value",
        "config file overrides internal default value",
        "explicitly specifying the default still uses default",
        "internal default value gets picked if not overridden",
        "nested config option default",
        "nested config option override by commandline",
    ],
)
def test_update_args(config, given, argname, expected):
    # Local imports as to not interfere with other tests
    from ansible_navigator.cli_args import CliArgs
    from ansible_navigator.cli import APP_NAME, update_args
    from ansible_navigator.utils import Sentinel

    # Setup -- should maybe move to a fixture?
    parser = CliArgs(APP_NAME).parser
    args, cmdline = parser.parse_known_args(given)
    args.cmdline = cmdline
    args.config = config
    msgs = update_args(args)

    assert getattr(args, argname, Sentinel) == expected
