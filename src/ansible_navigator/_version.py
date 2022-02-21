"""Version information for ansible-navigator.

.. note::

   __version__:

   Indicates the version of the ansible_navigator application.

   __version_collection_doc_cache__:

   Indicates the version of the schema of the collection doc cache
   this is checked during initialization, if the version of the cache
   differs from below, the cache will be rebuilt.  This should be
   incremented when the schema changes and need not correspond to the
   application version, although keeping the major in sync is probably
   not a bad idea to minimize the amount of stale docs in the user's cache
"""
__version__ = "1.1.0a1"
__version_collection_doc_cache__ = "1.0"
