# cspell:ignore ruamel debugpy pydevd
"""Tests for circular imports in all local packages and modules.

This ensures all internal packages can be imported right away without
any need to import some other module before doing so.

This module is based on an idea that ``pytest`` uses for self-testing:
* https://github.com/sanitizers/octomachinery/blob/be18b54/tests/circular_imports_test.py
* https://github.com/pytest-dev/pytest/blob/d18c75b/testing/test_meta.py
* https://twitter.com/codewithanthony/status/1229445110510735361
* https://github.com/aio-libs/aiohttp/blob/master/tests/test_circular_imports.py
"""

from __future__ import annotations

import os
import pkgutil
import subprocess  # Required due to the nature of this test
import sys

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

import ansible_navigator


if TYPE_CHECKING:
    from collections.abc import Generator
    from types import ModuleType


def _find_all_importables(pkg: ModuleType) -> list[str]:
    """Find all importables in the project.

    Args:
        pkg: The package in which importables will be found

    Returns:
        A sorted list of the importables
    """
    return sorted(
        set(
            chain.from_iterable(
                _discover_path_importables(Path(path), pkg.__name__) for path in pkg.__path__
            ),
        ),
    )


def _discover_path_importables(
    pkg_pth: Path,
    pkg_name: str,
) -> Generator[str]:
    """Yield all importables under a given path and package.

    Args:
        pkg_pth: The path to the package to walk
        pkg_name: The name of the package

    Yields:
        Package directory paths
    """
    for dir_path, _dir_names, file_names in os.walk(pkg_pth):
        pkg_dir_path = Path(dir_path)

        if pkg_dir_path.parts[-1] == "__pycache__":
            continue

        if all(Path(_).suffix != ".py" for _ in file_names):
            continue

        rel_pt = pkg_dir_path.relative_to(pkg_pth)
        pkg_pref = ".".join((pkg_name,) + rel_pt.parts)
        yield from (
            pkg_path
            for _, pkg_path, _ in pkgutil.walk_packages(
                (str(pkg_dir_path),),
                prefix=f"{pkg_pref}.",
            )
        )


@pytest.mark.parametrize(
    "import_path",
    _find_all_importables(ansible_navigator),
)
def test_no_warnings(import_path: str) -> None:
    """Verify that exploding importables doesn't explode.

    This is seeking for any import errors including ones caused
    by circular imports.

    DeprecationWarnings related to ``distutils`` in ansible_runner are ignored

    Args:
        import_path: The path to be imported and smoke-checked for
            warnings and crashes
    """
    # Because pkg_resources.declare_namespace warning happens for any namespace
    # package that exists on disk, even if they are imported we need to ignore
    # the generic warning.
    # NOTE: The following is related to the use of pkg_resource in debugpy
    # and triggered when running the tests with vscode in debug mode
    # https://github.com/microsoft/debugpy/issues/1230
    imp_cmd = (
        sys.executable,
        "-W",
        "error",
        # NOTE: The following 2 exclusions are only necessary because
        #       ansible-runner still uses `pkg_resources`
        # NOTE: could not figure out how to ignore this warning only for ansible-runner
        # https://github.com/ansible/ansible-runner/issues/1223
        "-W",
        "ignore: pkg_resources is deprecated as an API:DeprecationWarning",
        "-W",
        "ignore: Deprecated call to `pkg_resources.declare_namespace:DeprecationWarning",
        "-c",
        f"import {import_path!s}",
    )

    subprocess.check_call(imp_cmd)  # Input is trusted, generated above, not external
