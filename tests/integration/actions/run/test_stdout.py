""" run integration tests
"""
import os

from .base import RunActionRunTest


def test_run_stdout(test_fixtures_dir) -> None:
    """test 'run' to stdout"""
    actionruntest = RunActionRunTest("run")
    out, _err = actionruntest.run_action_stdout(
        [os.path.join(test_fixtures_dir, "integration", "actions", "run", "ping.yml")]
    )
    assert "TASK [ensure we can run a ping task]" in out
    assert "ok=1" in out


def test_run_ansible_cfg_same_dir(test_fixtures_dir) -> None:
    """ensure 'run' action finds correct ansible.cfg"""
    cwd = os.getcwd()
    fixture_dir = os.path.join(
        test_fixtures_dir, "integration", "actions", "run", "ansible_cfg_same_dir"
    )
    os.chdir(fixture_dir)
    actionruntest = RunActionRunTest("run")
    out, err = actionruntest.run_action_stdout([os.path.join("playbooks", "pb.yml"), "-t", "hi"])
    os.chdir(cwd)
    assert "ran with hi tag" in out
    assert "ran with bye tag" not in out
    assert "ERROR!" not in err
