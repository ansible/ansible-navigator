"""Ansible-navigator version information."""

try:
    from ._version import version as __version__
except ImportError:  # pragma: no branch
    try:
        from importlib.metadata import version

        __version__ = version("ansible-navigator")
    except Exception:  # noqa: BLE001
        # this is the fallback SemVer version picked by setuptools_scm when tag
        # information is not available.
        __version__ = "0.1.dev1"

__all__ = ("__version__",)
