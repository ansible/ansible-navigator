# cspell: ignore fspath
"""Common functions for the tests."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pytest

from tests import defaults


def get_executable_path(name: str) -> str:
    """Get the path of an executable.

    :param name: The name of the executable
    :raises ValueError: If the executable is not found
    :returns: The path of the executable
    """
    if name == "python":
        return sys.executable
    exec_path = shutil.which(name)
    if not exec_path:
        raise ValueError(f"{name} executable not found")
    return exec_path


def retrieve_fixture_for_step(
    request: pytest.FixtureRequest,
    step_index: int,
    test_name: str | None = None,
) -> list[str]:
    """Retrieve a fixture based on the test request and step index.

    :param request: The current test request
    :param step_index: The index of the current step in a set of TUI interactions
    :param test_name: A test name to add to the fixture path if needed
    :returns: The specific test step fixture
    """
    fixture_path = fixture_path_from_request(request, step_index, test_name)
    with fixture_path.open(encoding="utf-8") as fh:
        expected_output = json.load(fh)["output"]
    return expected_output


def update_fixtures(
    request: pytest.FixtureRequest,
    index: int,
    received_output: list[str],
    comment: str,
    testname: str | None = None,
    additional_information: dict[str, list[str] | bool] | None = None,
    zfill_index: int = 1,
) -> None:
    # pylint: disable=too-many-arguments
    """Write out a test fixture.

    :param request: Test request
    :param index: The test index
    :param received_output: Tmux screen contents
    :param comment: Comment to add to the fixture
    :param testname: Test name
    :param additional_information: Additional information to include in the fixture
    :param zfill_index: Pad the index with zeros
    """
    fixture_path = fixture_path_from_request(
        request=request,
        index=index,
        testname=testname,
        zfill_index=zfill_index,
    )
    fixture_path.parent.mkdir(parents=True, exist_ok=True)
    regex = "(/Users|/home).*?/tests/fixtures"
    name = re.sub(regex, "/tests/fixtures", request.node.name)
    name.replace("docker", "podman")
    fixture = {
        "name": name,
        "index": index,
        "comment": comment,
    }
    if additional_information is not None:
        fixture["additional_information"] = additional_information
    received_output_list = sanitize_output(received_output)
    fixture["output"] = received_output_list
    with fixture_path.open(mode="w", encoding="utf8") as fh:
        json.dump(fixture, fh, indent=4, ensure_ascii=False, sort_keys=False)
        fh.write("\n")


def fixture_path_from_request(
    request: pytest.FixtureRequest,
    index: int,
    testname: str | None = None,
    suffix: str = ".json",
    zfill_index: int = 1,
) -> Path:
    """Build a fixture path for a test.

    :param request: Test request
    :param index: Test index
    :param testname: Test name, used as a subdirectory
    :param suffix: The fixture file suffix
    :param zfill_index: Pad the index with zeros
    :returns: The path to the fixture
    """
    path_in_fixture_dir = request.node.nodeid.split("::")[0].lstrip("tests/")
    dir_path = Path(defaults.FIXTURES_DIR, path_in_fixture_dir, request.node.originalname)
    if testname:
        dir_path = dir_path / testname

    file_name = Path(str(index).zfill(zfill_index) + suffix)
    return dir_path / file_name


def generate_test_log_dir(request: pytest.FixtureRequest) -> Path:
    """Return a log directory for a test given it's request.

    :param request: The test request
    :returns: The path for the log file
    """
    test_path = Path(request.path)
    test_parts = list(test_path.parts)
    test_parts[test_parts.index("tests")] = ".test_logs"

    # Clean the test name to be a valid path
    test_name = re.sub(r"[^\w\s-]", "_", request.node.name.lower())
    test_name = re.sub(r"[-\s]+", "-", test_name).strip("-_")

    path = Path(*test_parts) / test_name

    path.mkdir(parents=True, exist_ok=True)
    return path / "ansible-navigator.log"


class Error(EnvironmentError):
    """Pass through error."""


def sanitize_output(output: list[str]) -> list[str]:
    """Sanitize test output that may be environment specific or unique per run.

    :param output: The output to sanitize
    :returns: The sanitized output
    """
    re_uuid = re.compile(
        "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        re.IGNORECASE,
    )
    re_home = re.compile("(/Users|/home)/(?!runner)[a-z,0-9]*/")
    re_python_version = re.compile(r"python3\.\d{2}")
    for idx, line in enumerate(output):
        new_line = re.sub(re_uuid, "00000000-0000-0000-0000-000000000000", line)
        new_line = re.sub(re_home, "/home/user/", new_line)
        new_line = re.sub(re_python_version, "python3.XX", new_line)
        output[idx] = new_line
    return output


def copytree(
    src: str,
    dst: str,
    symlinks: bool = False,
    ignore: Callable | None = None,
    dirs_exist_ok: bool = False,
):
    """Recursively copy a directory tree using copy2().

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional ``symlinks`` flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.

    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by ``copytree()``, and `names` which is the list of
    `src` contents, as returned by ``os.listdir()``:

        callable(src, names) -> ignored_names

    Since ``copytree()`` is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.

    :param src: Source directory
    :param dst: Destination directory
    :param symlinks: Copy symlinks
    :param ignore: Callable to ignore files
    :param dirs_exist_ok: Do not raise an exception if the destination directory exists
    :raises Error: If an error occurs
    """
    names = os.listdir(src)
    ignored_names = ignore(src, names) if ignore is not None else set()

    os.makedirs(dst, exist_ok=dirs_exist_ok)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        source_path = os.path.join(src, name)
        destination_path = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(source_path):
                source_link = os.readlink(source_path)
                os.symlink(source_link, destination_path)
            elif os.path.isdir(source_path):
                copytree(
                    source_path,
                    destination_path,
                    symlinks,
                    ignore,
                    dirs_exist_ok=dirs_exist_ok,
                )
            else:
                # Will raise a SpecialFileError for unsupported file types
                shutil.copy(source_path, destination_path)
        # catch the Error from the recursive ``copytree`` so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((source_path, destination_path, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        errors.append((src, dst, str(why)))
    if errors:
        raise Error(errors)


@dataclass
class Parameter:
    """Simple class to contain a name and parameter.

    Used with CliRunner in conftest.py
    """

    name: str
    value: bool | str | list | Path
