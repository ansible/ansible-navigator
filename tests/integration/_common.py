"""some common functions for the tests
"""
import json
import os
import re
import shutil
import sys

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


def update_fixtures(
    request,
    index,
    received_output,
    comment,
    testname=None,
    additional_information=None,
):
    # pylint: disable=too-many-arguments
    """Used by action plugins to generate the fixtures"""
    dir_path, file_name = fixture_path_from_request(request, index, testname=testname)
    os.makedirs(dir_path, exist_ok=True)
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
        if additional_information["look_fors"]:
            received_output = sanitize_output(received_output)
    fixture["output"] = received_output
    with open(f"{dir_path}/{file_name}", "w", encoding="utf8") as fh:
        json.dump(fixture, fh, indent=4, ensure_ascii=False, sort_keys=False)
        fh.write("\n")


def fixture_path_from_request(request, index, testname=None):
    """build a directory and file path for a test"""
    path_in_fixture_dir = request.node.nodeid.split("::")[0].lstrip("tests/")
    dir_path = os.path.join(defaults.FIXTURES_DIR, path_in_fixture_dir, request.node.originalname)
    if testname:
        dir_path = os.path.join(dir_path, testname)

    file_name = f"{index}.json"
    return dir_path, file_name


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
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore, dirs_exist_ok=dirs_exist_ok)
            else:
                # Will raise a SpecialFileError for unsupported file types
                shutil.copy(srcname, dstname)
        # catch the Error from the recursive ``copytree`` so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        errors.append((src, dst, str(why)))
    if errors:
        raise Error(errors)
