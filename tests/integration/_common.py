""" some common funcs for the tests
"""
import os
import sys
import json

from distutils.spawn import find_executable

from .. import defaults


def get_executable_path(name):
    """get the path of an executable"""
    if name == "python":
        exec_path = sys.executable
    else:
        exec_path = find_executable(name)
    if not exec_path:
        raise ValueError(f"{name} executable not found")
    return exec_path


def update_fixtures(request, index, received_output, comment, testname=None):
    """Used by action plugins to generate the fixtures"""
    dir_path, file_name = fixture_path_from_request(request, index, testname=testname)
    os.makedirs(dir_path, exist_ok=True)
    fixture = {
        "name": request.node.name,
        "index": index,
        "comment": comment,
        "output": received_output,
    }
    with open(f"{dir_path}/{file_name}", "w", encoding="utf8") as outfile:
        json.dump(fixture, outfile, indent=4, ensure_ascii=False, sort_keys=False)


def fixture_path_from_request(request, index, testname=None):
    """build a dir and file path for a test"""
    path_in_fixture_dir = request.node.nodeid.split("::")[0].lstrip("tests/")
    dir_path = os.path.join(defaults.FIXTURES_DIR, path_in_fixture_dir, request.node.originalname)
    if testname:
        dir_path = os.path.join(dir_path, testname)

    file_name = f"{index}.json"
    return dir_path, file_name


def container_runtime_or_fail():
    """find a container runtime, prefer podman
    fail if neither available"""
    # pylint: disable=import-outside-toplevel
    import subprocess

    for runtime in ("podman", "docker"):
        try:
            subprocess.run([runtime, "-v"], check=False)
            return runtime
        except FileNotFoundError:
            pass
    raise Exception("container runtime required")


def generate_test_log_dir(unique_test_id):
    """Generate a log directory for a test given it's request"""
    user = os.environ.get("USER")
    if user == "zuul":
        directory = os.path.join(
            "/", "home", "zuul", "zuul-output", "logs", "anible-navigator", unique_test_id
        )
    else:
        directory = os.path.join("./", ".test_logs", unique_test_id)
    os.makedirs(directory, exist_ok=True)
    return directory
