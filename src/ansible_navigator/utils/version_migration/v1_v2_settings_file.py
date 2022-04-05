"""The v1 to v2 settings file migration."""


from dataclasses import dataclass
from dataclasses import field
from typing import Dict

from ...content_defs import ContentView
from ...content_defs import SerializationFormat
from ..ansi import COLOR
from ..ansi import info
from ..dot_paths import MergeBehaviors
from ..dot_paths import check_path
from ..dot_paths import get_with_path
from ..dot_paths import move_to_path
from ..dot_paths import place_at_path
from ..serialize import Loader
from ..serialize import serialize_write_file
from ..serialize import yaml
from .defintions import Migration
from .defintions import MigrationStep
from .defintions import MigrationType


@dataclass
class V1V2SettingsFile(Migration):
    """The v1 to v2 settings file migration.

    The ordering of the functions in this class is important.
    It ensures that the migrations are run in the correct order.
    """

    content: Dict = field(default_factory=dict)
    name = "Version 1 to Version 2 settings file format migration"
    migration_type: MigrationType = MigrationType.SETTINGS_FILE

    def run(self, *args, **kwargs) -> None:
        """Perform the v1 to v2 migration.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        with self.settings_file_path.open("r", encoding="utf-8") as f:
            self.content = yaml.load(f, Loader=Loader)

        if self.check:
            self.run_steps()
            self.was_needed = self.needed_now
            return

        self.run_steps()

        # Not check mode and no migration needed, write file
        if self.was_needed and not self.needed_now:
            # Backup the settings file
            backup = self.settings_file_path.rename(self.settings_file_path.with_suffix(".v1"))
            info(color=COLOR, message=f"Backup {backup}")
            serialize_write_file(
                content=self.content,
                content_view=ContentView.NORMAL,
                file_mode="w",
                file=self.settings_file_path,
                serialization_format=SerializationFormat.YAML,
            )
            info(color=COLOR, message=f"Updated: {self.settings_file_path}")
        return

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
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return check_path(self.content, old_path)

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=(
                MergeBehaviors.LIST_APPEND,
                MergeBehaviors.LIST_SORT,
                MergeBehaviors.LIST_UNIQUE,
            ),
        )
        return False

    @MigrationStep.register(MigrationStep(name="playbook artifact"))
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

        if self.check:
            return exists

        if not exists:
            return False

        self.content = move_to_path(
            content=self.content,
            old_path=old_path,
            new_path=new_path,
            behaviors=tuple(),
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
            return any(("label" in item for item in value))

        for item in value:
            if "label" in item:
                item["options"] = item.pop("label")

        self.content = place_at_path(
            behaviors=tuple(),
            content=self.content,
            path=path,
            value=value,
        )

        return False
