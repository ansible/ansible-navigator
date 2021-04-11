""" inventory integration tests
"""
import os

from .._common import execute_command


def test_inventory_interactive_inventory_list(test_fixtures_dir, output_fixture):
    cmdline_arg = [
        "-m",
        "ansible_navigator",
        "inventory",
        "-i",
        os.path.join(test_fixtures_dir, "inventory"),
    ]
    user_interactions = [":0\r", ":0\r", ":0\r", ":0\r", ":quit\r"]
    expected_patterns = ["help", "help", "help", "help", "help"]
    received_output = execute_command(
        cmdline_arg, user_interactions, expected_patterns, sanitize=True
    )
    expected_output = output_fixture("interactive", "inventory_list")

    assert received_output == expected_output
