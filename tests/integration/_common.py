"""some common functions for the tests
"""
import json
import os
import re
import shutil
import sys

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pytest

from .. import defaults


def get_executable_path(name):
    """get the path of an executable"""
    if name == "python":
        exec_path = sys.executable
    else:
        exec_path = shutil.which(name)
    if not exec_path:
        raise ValueError(f"{name} executable not found")
    return exec_path


def retrieve_fixture_for_step(
    request: pytest.FixtureRequest,
    step_index: int,
    test_name: Optional[str] = None,
) -> List[str]:
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
    received_output: List[str],
    comment: str,
    testname: Optional[str] = None,
    additional_information: Optional[Dict[str, Union[List[str], bool]]] = None,
    zfill_index: int = 1,
):
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
        if additional_information.get("present"):
            received_output = sanitize_output(received_output)
    fixture["output"] = received_output
    with fixture_path.open(mode="w", encoding="utf8") as fh:
        json.dump(fixture, fh, indent=4, ensure_ascii=False, sort_keys=False)
        fh.write("\n")


def fixture_path_from_request(
    request: pytest.FixtureRequest,
    index: int,
    testname: Optional[str] = None,
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


def generate_test_log_dir(unique_test_id):
    """Generate a log directory for a test given it's request"""
    user = os.environ.get("USER")
    if user == "zuul":
        directory = os.path.join(
            "/",
            "home",
            "zuul",
            "zuul-output",
            "logs",
            "ansible-navigator",
            unique_test_id,
        )
    else:
        directory = os.path.join("./", ".test_logs", unique_test_id)
    os.makedirs(directory, exist_ok=True)
    return directory


class Error(EnvironmentError):
    """pass through err"""


def sanitize_output(output):
    """Sanitize test output that may be environment specific or unique per run."""
    re_uuid = re.compile(
        "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        re.IGNORECASE,
    )
    re_home = re.compile("(/Users|/home)/(?!runner)[a-z,0-9]*/")
    for idx, line in enumerate(output):
        new_line = re.sub(re_uuid, "00000000-0000-0000-0000-000000000000", line)

        new_line = re.sub(re_home, "/home/user/", new_line)
        output[idx] = new_line
    return output


def copytree(src, dst, symlinks=False, ignore=None, dirs_exist_ok=False):
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
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

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
        except EnvironmentError as why:
            errors.append((source_path, destination_path, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        errors.append((src, dst, str(why)))
    if errors:
        raise Error(errors)
