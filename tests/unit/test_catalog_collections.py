"""Unit tests for catalog collections."""

import multiprocessing

from pathlib import Path
from typing import Any

from ansible_navigator.data.catalog_collections import worker


def test_worker_with_failed_get_docstring() -> None:
    """Test the worker function when get_docstring fails."""
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


def test_worker_with_mocked_get_docstring() -> None:
    """Test the worker function with mocked get_docstring."""
    # def mock_get_docstring(*args, **kwargs):
    #     return (
    #         "Mocked docstring",
    #         "Mocked examples",
    #         "Mocked returndocs",
    #         "Mocked metadata",
    #     )

    # def mock_get_docstring(*args, **kwargs):
    #     raise Exception("Mocked exception")

    # monkeypatch.setattr(
    #     "ansible_navigator.data.catalog_collections.get_docstring",
    #     mock_get_docstring,
    # )

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

    plugin_path, result = completed_queue.get()
    # assert "Mocked docstring" in data[1]
    assert plugin_path == "error"
    assert "FileNotFoundError (get_docstring)" in result[2]

    # Check if the error message is put into the completed_queue
    # assert completed_queue.get() == ("error", ("12345", "tests/fixtures/common/xyz.py", "Exception (get_docstring): Mocked exception"))
