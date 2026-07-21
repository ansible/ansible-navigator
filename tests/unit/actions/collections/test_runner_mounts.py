"""Unit tests for collections runner mounts."""

from copy import deepcopy
from pathlib import Path

from ansible_navigator.actions.collections import Action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


def _base_args(tmp_path: Path):
    args = deepcopy(NavigatorConfiguration)
    args.entry("container_engine").value.current = "container"
    args.entry("execution_environment").value.current = True
    args.entry("execution_environment_image").value.current = "ghcr.io/example/demo:latest"
    args.entry("collection_doc_cache_path").value.current = str(tmp_path / "external-cache.db")
    args.entry("playbook").value.current = str(tmp_path / "site.yml")
    args.internals.cache_path = tmp_path / "cache"
    args.internals.cache_path.mkdir()
    (tmp_path / "site.yml").write_text("- hosts: localhost\n")
    (tmp_path / "collections").mkdir()
    return args


def test_collections_runner_mounts_do_not_use_selinux_labels_for_container(mocker, tmp_path) -> None:
    args = _base_args(tmp_path)
    fake_runner = mocker.patch("ansible_navigator.actions.collections.Command")
    fake_runner.return_value.run.return_value = ("", "", 0)

    action = Action(args=args)
    action._collection_cache_path = str(tmp_path / "collection-cache.db")
    action._run_runner()

    mounts = fake_runner.call_args.kwargs["container_volume_mounts"]
    assert all(not mount.endswith(":z") for mount in mounts)


def test_collections_runner_mounts_keep_selinux_labels_for_docker(mocker, tmp_path) -> None:
    args = _base_args(tmp_path)
    args.entry("container_engine").value.current = "docker"
    fake_runner = mocker.patch("ansible_navigator.actions.collections.Command")
    fake_runner.return_value.run.return_value = ("", "", 0)

    action = Action(args=args)
    action._collection_cache_path = str(tmp_path / "collection-cache.db")
    action._run_runner()

    mounts = fake_runner.call_args.kwargs["container_volume_mounts"]
    assert any(mount.endswith(":z") for mount in mounts)
