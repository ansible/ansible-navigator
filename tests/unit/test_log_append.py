""" test appending to the log """

from unittest import mock

import ansible_navigator.cli as cli


def test_log_append_true(tmp_path, container_runtime_or_fail):
    """run 5 times, append to log each time"""

    def side_effect(*_args, **_kwargs):
        return None

    repeat = 5
    new_session_msg = "New ansible-navigator instance"
    log_file = tmp_path / "ansible-navigator.log"
    cli_args = [
        "ansible-navigator",
        "--ce",
        container_runtime_or_fail(),
        "--la",
        "true",
        "--lf",
        str(log_file),
        "--ll",
        "info",
    ]
    with mock.patch("sys.argv", cli_args):
        with mock.patch("ansible_navigator.cli.wrapper") as mocked_wrapper:
            mocked_wrapper.side_effect = side_effect
            for _ in range(repeat):
                cli.main()
                # prevent multiple handlers
                cli.logger.handlers.clear()
    assert log_file.read_text().count(new_session_msg) == repeat


def test_log_append_false(tmp_path, container_runtime_or_fail):
    """run 5 times, never append to log each time"""

    def side_effect(*_args, **_kwargs):
        return None

    repeat = 5
    new_session_msg = "New ansible-navigator instance"
    log_file = tmp_path / "ansible-navigator.log"
    cli_args = [
        "ansible-navigator",
        "--ce",
        container_runtime_or_fail(),
        "--la",
        "false",
        "--lf",
        str(log_file),
        "--ll",
        "info",
    ]
    with mock.patch("sys.argv", cli_args):
        with mock.patch("ansible_navigator.cli.wrapper") as mocked_wrapper:
            mocked_wrapper.side_effect = side_effect
            for _ in range(repeat):
                cli.main()
                # prevent multiple handlers
                cli.logger.handlers.clear()
                assert log_file.read_text().count(new_session_msg) == 1
