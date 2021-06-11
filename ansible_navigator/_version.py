""" version

Note:

__version__:

indicates the version of the ansible_navigator applications

__version_collection_doc_cache__:

indicates the version of the schema of the collection doc cache
this is checked during initialization, if the version of the cache
differes from below, the cache will be rebuilt.  This should be
incremented when the schema changes and need not correspond to the
application version, although keeping the major in sync is probably
not a bad idea to minimize the amount of stale docs in the user's cache
"""
__version__ = "1.0.0b1"
__version_collection_doc_cache__ = "1.0"
