"""The ansible-navigator application.

This is a transitional configuration during the migration
from the hardcoded __version__ in _version to
version being populated during the build.
"""

try:
    from ._version import __version__
except ImportError:
    try:
        from ._version import version
    except ImportError:
        __version__ = "source"
