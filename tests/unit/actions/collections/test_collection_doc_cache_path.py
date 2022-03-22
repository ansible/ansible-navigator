"""Test the use of ``collection-doc-cache-path`` through to runner."""
import shlex

from pathlib import Path
from typing import NamedTuple

import pytest

from ansible_navigator import cli


class TstData(NamedTuple):
    """Store test data."""

    description: str
    path: str


DOC_CACHE_PATHS = (
    TstData(description="cwd", path="./cache.db"),
    TstData(description="tmp dir", path="../cache.db"),
)


def _id_description(value):
    """Generate id for a test"""
    return value.description


class DuplicateMountException(RuntimeError):
    """An exception specific to the duplicate mount test for collections."""


@pytest.mark.parametrize("doc_cache_path", DOC_CACHE_PATHS, ids=_id_description)
@pytest.mark.usefixtures("patch_curses")
def test_for_duplicates_sources(
    doc_cache_path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    mocker,
):
    """Ensure duplicate volume mounts are not passed to runner.

    :param doc_cache_path: The test data
    :param patch_curses: Fixture to patch curses so it doesn't traceback
    :param monkeypatch: The monkeypatch fixture
    :param arg_collector: The fixture used to collect argument passed to a function
    """
    working_dir = tmp_path / "working_dir"
    working_dir.mkdir()
    cdc_full_path = working_dir / doc_cache_path.path
    command = f"ansible-navigator collections '--cdcp={cdc_full_path!s}' --pp never"
    monkeypatch.setattr("sys.argv", shlex.split(command))
    run_cmd_mocked = mocker.patch(
        "ansible_navigator.runner.command.run_command",
        side_effect=DuplicateMountException,
    )
    monkeypatch.chdir(working_dir)
    monkeypatch.setenv("ANSIBLE_NAVIGATOR_ALLOW_UI_TRACEBACK", "true")
    with pytest.raises(DuplicateMountException):
        cli.main()
    _args, kwargs = run_cmd_mocked.call_args
    host_cwd = Path(kwargs["host_cwd"])
    mounts = kwargs["container_volume_mounts"]
    sources = [Path(mount.split(":")[0]).parents[0] for mount in mounts]
    assert host_cwd not in sources
