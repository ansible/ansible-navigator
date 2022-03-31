"""A test inventory plugin."""
from ansible.plugins.inventory import BaseInventoryPlugin


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


class InventoryModule(BaseInventoryPlugin):
    """A test inventory plugin."""

    NAME = "test.test.test"

    def verify_file(self, path):
        """Return true/false if this is possibly a valid file for this plugin to consume.

        :param path: Path to inventory file
        :return: True if valid, False if not
        """
        valid = False
        if super().verify_file(path):
            if path.endswith(("test_inventory.yaml", "test_inventory.yml")):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source.

        :param inventory: Inventory object
        :param loader: Loader object
        :param path: Path to inventory source
        :param cache: Cache or not
        """
        super().parse(inventory, loader, path, cache)
        self.inventory.add_host("from.test.plugin")
