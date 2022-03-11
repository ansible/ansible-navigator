"""Tests for circular imports in all local packages and modules.

This ensures all internal packages can be imported right away without
any need to import some other module before doing so.

This module is based on an idea that ``pytest`` uses for self-testing:
* https://github.com/sanitizers/octomachinery/blob/be18b54/tests/circular_imports_test.py
* https://github.com/pytest-dev/pytest/blob/d18c75b/testing/test_meta.py
* https://twitter.com/codewithanthony/status/1229445110510735361
* https://github.com/aio-libs/aiohttp/blob/master/tests/test_circular_imports.py
"""  # noqa: E501
import os
import pkgutil
import subprocess  # noqa: S404 Required due to the nature of this test
import sys

from itertools import chain
from pathlib import Path
from types import ModuleType
from typing import Generator
from typing import List

import pytest

import ansible_navigator


def _find_all_importables(pkg: ModuleType) -> List[str]:
    """Find all importables in the project.

    :param pkg: The package in which importables will be found
    :returns: A sorted list of the importables
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
) -> Generator[str, None, None]:
    """Yield all importables under a given path and package.

    :param pkg_pth: The path to the package to walk
    :param pkg_name: The name of the package
    :yields: Package directory paths
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

    :param import_path: The path to be imported and smoke-checked for warnings and crashes
    """
    imp_cmd = (
        sys.executable,
        "-W",
        "error",
        # NOTE: This exclusion is only necessary because ansible-runner still uses `distutils`
        # NOTE: but this project already aims to target Python 3.10 as well.
        # TODO: Remove this exclusion once the runner issue is addressed.
        # Ref: https://github.com/ansible/ansible-runner/issues/969
        "-W",
        "ignore:The distutils package is deprecated and slated for removal in Python 3.12."
        " Use setuptools or check PEP 632 for potential alternatives:DeprecationWarning:"
        "ansible_runner.config.runner",
        "-c",
        f"import {import_path!s}",
    )

    subprocess.check_call(imp_cmd)  # noqa: S603 Input is trusted, generated above, not external
