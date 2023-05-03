"""The v1 to v2 settings file migration."""

from __future__ import annotations

from ansible_navigator.utils.dot_paths import MergeBehaviors
from ansible_navigator.utils.dot_paths import check_path
from ansible_navigator.utils.dot_paths import get_with_path
from ansible_navigator.utils.dot_paths import move_to_path
from ansible_navigator.utils.dot_paths import place_at_path

from .definitions import MigrationStep
from .definitions import MigrationType
from .settings_file import SettingsFile


class V1V2SettingsFile(SettingsFile):
    """The v1 to v2 settings file migration.

    The ordering of the functions in this class is important.
    It ensures that the migrations are run in the correct order.
    """

    name = "Version 1 to Version 2 settings file format migration"
    migration_type: MigrationType = MigrationType.SETTINGS_FILE

    def __init__(self):
        """Initialize the v1 to v2 settings file migration."""
        super().__init__()
        self.content: dict = {}
        self._backup_suffix = ".v1"

    @MigrationStep.register(MigrationStep(name="config path"))
    def config_path(self) -> bool:
        """Migrate the config path entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.ansible.config"
        new_path = "ansible-navigator.ansible.config.path"

        exists = check_path(self.content, old_path)
        if not exists:
            return False

        value = get_with_path(self.content, old_path)
        if not isinstance(value, str):
            return False

        if self.check:
            return True

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="documentation"))
    def documentation(self) -> bool:
        """Migrate the documentation entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.documentation"
        new_path = "ansible-navigator.ansible.doc"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="playbook path"))
    def playbook_path(self) -> bool:
        """Migrate the playbook path entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.ansible.playbook"
        new_path = "ansible-navigator.ansible.playbook.path"

        exists = check_path(self.content, old_path)
        if not exists:
            return False

        value = get_with_path(self.content, old_path)
        if not isinstance(value, str):
            return False

        if self.check:
            return True

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="help builder"))
    def help_builder(self) -> bool:
        """Migrate the help-builder entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.help-builder"
        new_path = "ansible-navigator.ansible-builder.help"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="help config"))
    def help_config(self) -> bool:
        """Migrate the help-config entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.help-config"
        new_path = "ansible-navigator.ansible.config.help"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="help doc"))
    def help_doc(self) -> bool:
        """Migrate the help-doc entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.help-doc"
        new_path = "ansible-navigator.ansible.doc.help"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="help inventory"))
    def help_inventory(self) -> bool:
        """Migrate the help-inventory entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.help-inventory"
        new_path = "ansible-navigator.ansible.inventory.help"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="help playbook"))
    def help_playbook(self) -> bool:
        """Migrate the help-playbook entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.help-playbook"
        new_path = "ansible-navigator.ansible.playbook.help"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="inventory paths"))
    def inventories(self) -> bool:
        """Migrate the inventory paths.

        :return: Whether the migration is needed
        """
        old_path = "ansible-navigator.ansible.inventories"
        new_path = "ansible-navigator.ansible.inventory.entries"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=(
                MergeBehaviors.LIST_APPEND,
                MergeBehaviors.LIST_SORT,
                MergeBehaviors.LIST_UNIQUE,
            ),
            content=self.content,
            old_path=old_path,
            new_path=new_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="playbook artifact timestamp"))
    def playbook_artifact(self) -> bool:
        """Migrate the playbook artifact entry.

        :returns: Whether the migration is needed
        """
        path = "ansible-navigator.playbook-artifact.save-as"

        entry_exists = check_path(self.content, path)
        if not entry_exists:
            return False

        value = get_with_path(self.content, path)

        if not isinstance(value, str):
            return False

        if self.check:
            return "ts_utc" in value

        new_value = value.replace("ts_utc", "time_stamp")

        self.content = place_at_path(
            behaviors=tuple(),
            content=self.content,
            path=path,
            value=new_value,
        )
        return False

    @MigrationStep.register(MigrationStep(name="pull-policy"))
    def pull_policy(self) -> bool:
        """Migrate the pull-policy entry.

        :returns: Whether the migration is needed
        """
        old_path = "ansible-navigator.execution-environment.pull-policy"
        new_path = "ansible-navigator.execution-environment.pull.policy"

        exists = check_path(self.content, old_path)
        if self.check or not exists:
            return exists

        self.content = move_to_path(
            behaviors=tuple(),
            content=self.content,
            new_path=new_path,
            old_path=old_path,
        )
        return False

    @MigrationStep.register(MigrationStep(name="volume mount labels"))
    def volume_mount_labels(self) -> bool:
        """Migrate the volume mount labels.

        :returns: Whether the migration is needed
        """
        path = "ansible-navigator.execution-environment.volume-mounts"

        entry_exists = check_path(self.content, path)
        if not entry_exists:
            return False

        value = get_with_path(self.content, path)

        if not isinstance(value, list):
            return False

        if not all(isinstance(item, dict) for item in value):
            return False

        if self.check:
            return any("label" in item for item in value)

        for item in value:
            if "label" in item:
                item["options"] = item.pop("label")

        self.content = place_at_path(
            behaviors=(MergeBehaviors.LIST_LIST_REPLACE,),
            content=self.content,
            path=path,
            value=value,
        )

        return False
