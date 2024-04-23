"""Unit tests for catalog collections."""
from pathlib import Path

import pytest
import yaml
from ansible.errors import AnsibleError
from ansible.plugins.loader import fragment_loader
from ansible.utils.plugin_docs import get_docstring

from ansible_navigator.cli import cache_scripts
from ansible_navigator.data.catalog_collections import get_doc_withast

# module_content = '''
# DOCUMENTATION = r"""
# ---
# module: vcenter_mod
# short_description: Gather info vCenter extensions
# description:
# - This module can be used to gather information about vCenter extension.
# author:
# - test
# extends_documentation_fragment:
# - community.vmware.vmware.documentation
# """

# EXAMPLES = "Example usage here."
# RETURN = "This function returns a value."
# METADATA = "Author: John Doe"
# '''

plugin_path = Path("tests/fixtures/common/example.py")
collection_name = "microsoft.ad"


def test_catalog_collections() -> None:
    """Import the catalog collections script."""
    cache_scripts()
    with pytest.raises(AnsibleError):
        get_docstring(
            filename=str(plugin_path),
            fragment_loader=fragment_loader,
            collection_name=collection_name,
        )

    with plugin_path.open(mode="r", encoding="utf-8") as f:
        content = f.read()
    doc, examples, returndocs, metadata = get_doc_withast(content)
    doc, examples, returndocs, metadata = (
        yaml.load(value, Loader=yaml.SafeLoader)
        for value in (doc, examples, returndocs, metadata)
    )
    assert examples == "Example usage here."
    assert returndocs == "This function returns a value."
    assert metadata == {'Author': 'John Doe'}
