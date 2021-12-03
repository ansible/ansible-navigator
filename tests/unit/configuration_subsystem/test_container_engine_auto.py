"""Tests related to the auto detection of the container engine.
"""
import shutil


def test_ce_auto_podman(monkeypatch, generate_config):
    """Ensure podman is the result."""

    def which(arg):
        return arg == "podman"

    monkeypatch.setattr(shutil, "which", which)
    response = generate_config()
    assert response.exit_messages == []
    assert response.application_configuration.container_engine == "podman"


def test_ce_auto_docker(monkeypatch, generate_config):
    """Ensure docker is the result."""

    def which(arg):
        return arg == "docker"

    monkeypatch.setattr(shutil, "which", which)
    response = generate_config()
    assert response.exit_messages == []
    assert response.application_configuration.container_engine == "docker"


def test_ce_auto_none(monkeypatch, generate_config):
    """Ensure error is the result."""

    def which(_arg):
        return False

    monkeypatch.setattr(shutil, "which", which)
    response = generate_config()
    expected = "No container engine could be found"
    assert any(
        expected in exit_msg.message for exit_msg in response.exit_messages
    ), response.exit_messages
