"""Unit tests for catalog collections."""

import multiprocessing

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock  # pylint: disable=preferred-module
from unittest.mock import patch  # pylint: disable=preferred-module

from ansible_navigator.data.catalog_collections import retrieve_collections_paths
from ansible_navigator.data.catalog_collections import run_command
from ansible_navigator.data.catalog_collections import worker


def test_worker_with_failed_get_docstring() -> None:
    """Test worker function.

    Test worker function when get_docstring fails and
     get_doc_withast method is used to parse the content.
    """
    # Create the queues
    pending_queue: multiprocessing.Queue[Any] = multiprocessing.Queue()
    completed_queue: multiprocessing.Queue[Any] = multiprocessing.Queue()

    plugin_path = Path("tests/fixtures/common/module_1.py")
    collection_name = "microsoft.ad"
    checksum = "12345"

    # Add an entry to the pending queue
    entry = collection_name, checksum, plugin_path
    pending_queue.put(entry)

    # Add a None entry to signal the end of processing
    pending_queue.put(None)

    worker(pending_queue, completed_queue)

    plugin_path, data = completed_queue.get()
    assert "vCenter" in data[1]


def test_worker_with_invalid_plugin_path() -> None:
    """Test the worker function when get_docstring has invalid plugin_path."""
    pending_queue: multiprocessing.Queue[Any] = multiprocessing.Queue()
    completed_queue: multiprocessing.Queue[Any] = multiprocessing.Queue()

    plugin_path = Path("tests/fixtures/common/xyz.py")
    collection_name = "microsoft.ad"
    checksum = "12345"

    # Add an entry to the pending queue
    entry = collection_name, checksum, plugin_path
    pending_queue.put(entry)

    # Add a None entry to signal the end of processing
    pending_queue.put(None)

    worker(pending_queue, completed_queue)

    plugin_path, data = completed_queue.get()
    assert plugin_path == "error"
    assert "FileNotFoundError (get_docstring)" in data[2]


@patch("ansible_navigator.data.catalog_collections.subprocess.run")
def test_run_command_without_shell(mock_subprocess: MagicMock) -> None:
    """Test that run_command executes without shell=True.

    Args:
        mock_subprocess: Mock subprocess.run
    """
    # Mock successful command execution
    mock_process = MagicMock()
    mock_process.stdout = "test output"
    mock_subprocess.return_value = mock_process

    cmd = ["ansible-config", "dump"]
    result = run_command(cmd)

    # Verify subprocess.run was called with shell=False
    mock_subprocess.assert_called_once()
    call_args = mock_subprocess.call_args
    assert call_args[0][0] == cmd
    assert call_args[1]["shell"] is False
    assert result == {"stdout": "test output"}


@patch("ansible_navigator.data.catalog_collections.subprocess.run")
def test_run_command_handles_permission_error(mock_subprocess: MagicMock) -> None:
    """Test that run_command handles PermissionError gracefully.

    Args:
        mock_subprocess: Mock subprocess.run
    """
    mock_subprocess.side_effect = PermissionError(1, "Operation not permitted", "/bin/sh")

    cmd = ["ansible-config", "dump"]
    result = run_command(cmd)

    assert "error" in result
    assert "PermissionError" in result["error"]


@patch("ansible_navigator.data.catalog_collections.run_command")
def test_retrieve_collections_paths_without_pipe(mock_run_command: MagicMock) -> None:
    """Test that retrieve_collections_paths doesn't use shell pipes.

    Args:
        mock_run_command: Mock run_command function
    """
    config_output = """ANSIBLE_COW_ACCEPTLIST(default) = ['bud-frogs', 'bunny']
COLLECTIONS_PATHS(default) = ['/home/user/.ansible/collections', '/usr/share/ansible/collections']
DEFAULT_FORKS(default) = 5"""

    mock_run_command.return_value = {"stdout": config_output}

    result = retrieve_collections_paths()

    mock_run_command.assert_called_once_with(["ansible-config", "dump"])

    assert "result" in result
    assert isinstance(result["result"], list)
    assert "/home/user/.ansible/collections" in result["result"]
    assert "/usr/share/ansible/collections" in result["result"]


@patch("ansible_navigator.data.catalog_collections.run_command")
def test_retrieve_collections_paths_not_found(mock_run_command: MagicMock) -> None:
    """Test retrieve_collections_paths when COLLECTIONS_PATHS is not in output.

    Args:
        mock_run_command: Mock run_command function
    """
    # Mock ansible-config dump output without COLLECTIONS_PATHS
    config_output = """ANSIBLE_COW_ACCEPTLIST(default) = ['bud-frogs', 'bunny']
DEFAULT_FORKS(default) = 5"""

    mock_run_command.return_value = {"stdout": config_output}

    result = retrieve_collections_paths()

    # Verify an error is returned
    assert "error" in result
    assert "COLLECTIONS_PATHS not found" in result["error"]
