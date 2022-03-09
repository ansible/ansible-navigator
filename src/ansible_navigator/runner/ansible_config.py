"""Herein lies the ability for ansible-runner to run the ansible-config command."""

from typing import Optional
from typing import Tuple

from ansible_runner import get_ansible_config

from .base import Base


class AnsibleConfig(Base):
    """Abstraction for ansible-config command-line."""

    def fetch_ansible_config(
        self,
        action: str,
        config_file: Optional[str] = None,
        only_changed: Optional[bool] = None,
    ) -> Tuple[str, str]:
        """Run ansible-config command and get the configuration related details.

        :param action: The configuration fetch action to perform. Valid values are one of
            ``list``, ``dump``, ``view``. The ``list`` action will fetch all the config
            options along with config description, ``dump`` action will fetch all the active
            config and ``view`` action will return the active configuration file view.
        :param config_file: Path to configuration file, defaults to first file found in
            precedence. Defaults to ``None``.
        :param only_changed: The boolean value when set to ``True`` returns only the
            configurations that have changed from the default. This parameter is applicable only
            when ``action`` is set to ``dump``. Defaults to `None`.
        :returns: A tuple of response and error string (if any)
        """
        return get_ansible_config(
            action,
            config_file=config_file,
            only_changed=only_changed,
            **self._runner_args,
        )
