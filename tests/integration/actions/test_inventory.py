""" inventory integration tests
"""
import os

from .._common import get_executable_path


def test_inventory_interactive_inventory_list(test_fixtures_dir, output_fixture, run_command_tmux_session):
    py_exec = get_executable_path("python")
    cmdline= [
        py_exec,
        "-m",
        "ansible_navigator",
        "inventory",
        "-i",
        os.path.join(test_fixtures_dir, "inventory"),
    ]
    user_interactions = [" ".join(cmdline), "0", "0", "0", "0", ":quit"]

    received_output = run_command_tmux_session("interactive_inventory_list", user_interactions)

    expected_output = output_fixture("interactive", "inventory_list")
    assert expected_output in received_output
