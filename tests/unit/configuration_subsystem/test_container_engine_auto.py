"""Tests related to the auto detection of the container engine."""

import shutil

from typing import Any

import pytest

from .conftest import GenerateConfigCallable


def test_ce_auto_podman(
    monkeypatch: pytest.MonkeyPatch, generate_config: GenerateConfigCallable
) -> None:
    """Ensure podman is the result.

    :param monkeypatch: The monkeypatch fixture
    :param generate_config: The configuration generator fixture
    """

    def which(arg: Any) -> bool:
        return arg == "podman"

    monkeypatch.setattr(shutil, "which", which)
    response = generate_config()
    assert response.exit_messages == []
    assert response.application_configuration.container_engine == "podman"


def test_ce_auto_docker(
    monkeypatch: pytest.MonkeyPatch, generate_config: GenerateConfigCallable
) -> None:
    """Ensure docker is the result.

    :param monkeypatch: The monkeypatch fixture
    :param generate_config: The configuration generator fixture
    """

    def which(arg: Any) -> bool:
        return arg == "docker"

    monkeypatch.setattr(shutil, "which", which)
    response = generate_config()
    assert response.exit_messages == []
    assert response.application_configuration.container_engine == "docker"


def test_ce_auto_none(
    monkeypatch: pytest.MonkeyPatch, generate_config: GenerateConfigCallable
) -> None:
    """Ensure error is the result.

    :param monkeypatch: The monkeypatch fixture
    :param generate_config: The configuration generator fixture
    """

    def which(_arg: Any) -> bool:
        return False

    monkeypatch.setattr(shutil, "which", which)
    response = generate_config()
    expected = "No container engine could be found"
    assert any(
        expected in exit_msg.message for exit_msg in response.exit_messages
    ), response.exit_messages
