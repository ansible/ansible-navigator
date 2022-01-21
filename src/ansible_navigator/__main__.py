"""A runpy entry point for ansible-navigator.

This makes it possible to invoke CLI
via :command:`python -m ansible_navigator`.
"""
from .cli import main


if __name__ == "__main__":
    main()
