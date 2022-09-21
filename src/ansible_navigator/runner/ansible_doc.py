"""Herein lies the ability for ansible-runner to run the ansible-doc command."""

from __future__ import annotations

from typing import Any

from ansible_runner import get_plugin_docs

from .base import Base


class AnsibleDoc(Base):
    # pylint: disable=too-many-arguments
    """An interface to ``ansible-runner`` for running the ``ansible-doc`` command."""

    def fetch_plugin_doc(
        self,
        plugin_names: list,
        plugin_type: str | None = None,
        response_format: str | None = "json",
        snippet: bool | None = None,
        playbook_dir: str | None = None,
        module_path: str | None = None,
    ) -> tuple[dict[Any, Any] | str, dict[Any, Any] | str]:
        """Run ``ansible-doc`` command and get the plugin docs related details.

        :param plugin_names: The name of the plugins to get docs
        :param plugin_type: The type of the plugin mentioned in plugins_names
            Valid values are ``become``, ``cache``, ``callback``, ``cliconf``, ``connection``,
            ``httpapi``, ``inventory``, ``lookup``, ``netconf``, ``shell``, ``vars``,
            ``module``, ``strategy``. If the value is not provided it defaults to ``module``.
        :param response_format: The output format for response. Valid values can be one of
            ``json`` or ``human`` and the response is either json string or plain text in human
            readable format. Defaults to ``json``.
        :param snippet: Show playbook snippet for specified plugin(s)
        :param playbook_dir: This parameter is used to sets the relative path to handle playbook
            adjacent installed plugins
        :param module_path: This parameter is prepend colon-separated path(s) to module library
            (default=~/.ansible/plugins/modules: /usr/share/ansible/plugins/modules).
        :returns: A tuple of response and error string. If the value of ``response_format`` is
            ``json`` it returns a python dictionary object.
        """
        return get_plugin_docs(
            plugin_names,
            plugin_type=plugin_type,
            response_format=response_format,
            snippet=snippet,
            playbook_dir=playbook_dir,
            module_path=module_path,
            **self._runner_args,
        )
