""" fixtures """
import os
import pytest

from ._common import container_runtime_or_fail

EXECUTION_MODES = ["interactive", "stdout"]


@pytest.fixture(scope="session")
def test_fixtures_dir():
    """the test fixture directory"""
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")


@pytest.fixture(scope="session", name="container_runtime_or_fail")
def fixture_container_runtime_or_fail():
    """check if container runtime is available"""
    yield container_runtime_or_fail


@pytest.fixture
def patch_curses(monkeypatch):
    """patch curses so it doesn't Traceback during tests"""
    # pylint: disable=import-outside-toplevel
    import curses

    monkeypatch.setattr(curses, "cbreak", lambda: None)
    monkeypatch.setattr(curses, "nocbreak", lambda: None)
    monkeypatch.setattr(curses, "endwin", lambda: None)


@pytest.fixture(scope="session")
def os_indendent_tmp():
    """
    this attempts to ensure the length of the /tmp
    is the same between MacOS and Linux
    otherwise ansible-navigator column widths can vary
    """
    tmp_real = os.path.realpath("/tmp")
    if tmp_real == "/private/tmp":
        an_tmp = os.path.join(tmp_real, "an")
    else:
        an_tmp = os.path.join("/tmp", "private", "an")

    os.makedirs(an_tmp, exist_ok=True)
    return an_tmp
