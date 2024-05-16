"""Unit tests for catalog collections."""

import multiprocessing

from pathlib import Path
from typing import Any

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
