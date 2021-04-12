""" inventory integration tests
"""
import os

from .._common import get_executable_path


def test_inventory_interactive_inventory_list(
    test_fixtures_dir, output_fixture, run_command_using_tmux_session
):
    py_exec = get_executable_path("python")
    cmdline = [
        py_exec,
        "-m",
        "ansible_navigator",
        "inventory",
        "-i",
        os.path.join(test_fixtures_dir, "inventory"),
    ]
    user_interactions = [
        " ".join(cmdline),
        "0",  # test browse groups
        "0",
        "0",
        "0",
        "Escape",
        "Escape",
        "1",
        "0",
        "Escape",
        "Escape",
        "2",
        "0",
        "Escape",
        "Escape",
        "Escape",
        "Escape",
        "1",  # test browse hosts
        "0",
        "Escape",
        "1",
        "Escape",
        "2",
        "1" ":quit",
    ]

    received_output = run_command_using_tmux_session(
        "interactive_inventory_list", user_interactions
    )

    expected_output = output_fixture("interactive", "inventory_list")
    assert expected_output in received_output
