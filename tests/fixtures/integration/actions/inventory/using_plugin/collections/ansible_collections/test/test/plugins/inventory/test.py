"""A test inventory plugin."""

from typing import Any
from click import Path
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.inventory.data import InventoryData


DOCUMENTATION = """
    name: test.test.test
    plugin_type: inventory
    short_description: Test inventory source
    description:
        - Test inventory source
    options:
        plugin:
            description: token that ensures this is a source file for the 'csv' plugin
            required: True
            choices: ['test.test.test']

"""

EXAMPLES = """
 """


class InventoryModule(BaseInventoryPlugin):  # type: ignore[misc]
    """A test inventory plugin."""

    NAME = "test.test.test"

    def verify_file(self, path: str) -> bool:
        """Return true/false if this is possibly a valid file for this plugin to consume.

        Args:
            path: Path to inventory file

        Returns:
            True if valid, False if not
        """
        valid = False
        if super().verify_file(path):
            if path.endswith(("test_inventory.yaml", "test_inventory.yml")):
                valid = True
        return valid

    def parse(self, inventory: InventoryData, loader: Any, path: str, cache: bool = True) -> None:
        """Parse the inventory source.

        Args:
            inventory: Inventory object
            loader: Loader object
            path: Path to inventory source
            cache: Cache or not
        """
        super().parse(inventory, loader, path, cache)
        self.inventory.add_host("from.test.plugin")
