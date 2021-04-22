""" run integration tests
"""
import os

from ..._common import ActionRunTest


def test_run_stdout(test_fixtures_dir) -> None:
    """test 'run' to stdout"""
    actionruntest = ActionRunTest("run")
    actionruntest._app_args["playbook"] = os.path.join(
        test_fixtures_dir,
        "integration",
        "actions",
        "run",
        "ping.yml",
    )
    actionruntest._app_args["inventory"] = []
    out, _err = actionruntest.run_action_stdout()
    assert "TASK [ensure we can run a ping task]" in out
    assert "ok=1" in out


def test_run_ansible_cfg_same_dir(test_fixtures_dir) -> None:
    """ensure 'run' action finds correct ansible.cfg"""
    cwd = os.getcwd()
    fixture_dir = os.path.join(
        test_fixtures_dir,
        "integration",
        "actions",
        "run",
        "ansible_cfg_same_dir",
    )
    os.chdir(fixture_dir)
    actionruntest = ActionRunTest("run")
    actionruntest._app_args["playbook"] = os.path.join(
        fixture_dir,
        "playbooks",
        "pb.yml",
    )
    actionruntest._app_args["inventory"] = []
    try:
        out, err = actionruntest.run_action_stdout(
            [
                "-t",
                "hi",
            ]
        )
    finally:
        os.chdir(cwd)
    assert "ran with hi tag" in out
    assert "ran with bye tag" not in out
    assert "ERROR!" not in err
