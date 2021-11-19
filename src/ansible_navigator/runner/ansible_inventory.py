""" Herewithin lies the ability for ansible-runner
to run the ansible-inventory command
"""

from typing import List
from typing import Optional
from typing import Tuple

from ansible_runner import get_inventory

from .base import Base


class AnsibleInventory(Base):
    # pylint: disable=too-many-arguments
    """abstraction for ansible-inventory command-line"""

    def fetch_inventory(
        self,
        action: str,
        inventories: List,
        response_format: Optional[str] = None,
        host: Optional[str] = None,
        playbook_dir: Optional[str] = None,
        vault_ids: Optional[str] = None,
        vault_password_file: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Run ansible-inventory command and get the inventory related details

        Args:
            action (str): Valid values are one of ``graph``, ``host``, ``list`` \
                          ``graph`` create inventory graph, ``host`` returns specific \
                          host info and works as inventory script and ``list`` output \
                          all hosts info and also works as inventory script.
            inventories (List): List of inventory host path.
            response_format (Optional[str], optional): The output format for response. \
                                                       Valid values can be one of ``json``, \
                                                       ``yaml``, ``toml``. \
                                                       If ``action`` is ``graph`` only allowed \
                                                       value is ``json``.
            host (Optional[str], optional): When ``action`` is set to ``host`` this parameter is \
                                            used to get the host specific information..
            playbook_dir (Optional[str], optional): This parameter is used to sets the relative \
                                                    path for the inventory.
            vault_ids (Optional[str], optional): The vault identity to use.
            vault_password_file (Optional[str], optional): The vault identity to use.

        Returns:
            Tuple[str, str]: Returns a tuple of response and error string (if any).
        """
        return get_inventory(
            action,
            inventories=inventories,
            response_format=response_format,
            host=host,
            playbook_dir=playbook_dir,
            vault_ids=vault_ids,
            vault_password_file=vault_password_file,
            **self._runner_args
        )
