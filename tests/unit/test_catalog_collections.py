"""Unit tests for catalog collections."""

import multiprocessing

from pathlib import Path
from unittest.mock import patch

from ansible_navigator.data.catalog_collections import worker


@patch("ansible_navigator.data.catalog_collections.get_docstring")
def test_worker_with_failed_get_docstring(mock_get_docstring):
    """Test the worker function when get_docstring fails."""
    # Create the queues
    pending_queue = multiprocessing.Queue()
    completed_queue = multiprocessing.Queue()

    plugin_path = Path("tests/fixtures/common/example.py")
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
