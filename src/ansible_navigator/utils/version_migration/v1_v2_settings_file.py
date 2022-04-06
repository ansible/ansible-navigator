"""The v1 to v2 settings file migration."""


from typing import Dict

from ...content_defs import ContentView
from ...content_defs import SerializationFormat
from ..ansi import COLOR
from ..ansi import changed
from ..ansi import info
from ..dot_paths import MergeBehaviors
from ..dot_paths import check_path
from ..dot_paths import get_with_path
from ..dot_paths import move_to_path
from ..dot_paths import place_at_path
from ..serialize import Loader
from ..serialize import serialize_write_file
from ..serialize import yaml
from .definitions import Migration
from .definitions import MigrationStep
from .definitions import MigrationType


class V1V2SettingsFile(Migration):
    """The v1 to v2 settings file migration.

    The ordering of the functions in this class is important.
    It ensures that the migrations are run in the correct order.
    """

    name = "Version 1 to Version 2 settings file format migration"
    migration_type: MigrationType = MigrationType.SETTINGS_FILE

    def __init__(self):
        """Initialize the v1 to v2 settings file migration."""
        super().__init__()
        self.content: Dict = {}

    def run(self, *args, **kwargs) -> None:
        """Perform the v1 to v2 migration.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        if not self.content:
            with self.settings_file_path.open("r", encoding="utf-8") as f:
                try:
                    self.content = yaml.load(f, Loader=Loader)
                except (yaml.scanner.ScannerError, yaml.parser.ParserError):
                    return

        if not self.content:
            return

        # Check if any of the migrations are needed
        if self.check:
            self.run_steps()
            self.was_needed = self.needed_now
            return

        # Not check and wasn't needed
        if not self.was_needed:
            return

        self.run_steps()

        # Something may have gone wrong
        if self.needed_now:
            return

        # Back up the current
        backup = self.settings_file_path.rename(self.settings_file_path.with_suffix(".v1"))
        info(color=COLOR, message=f"Backup: {backup}")

        # Write the new file
        if self.settings_file_path.suffix in (".yml", ".yaml"):
            serialization_format = SerializationFormat.YAML
        elif self.settings_file_path.suffix == ".json":
            serialization_format = SerializationFormat.JSON

        serialize_write_file(
            content=self.content,
            content_view=ContentView.NORMAL,
            file_mode="w",
            file=self.settings_file_path,
            serialization_format=serialization_format,
        )
        changed(color=COLOR, message=f"Updated: {self.settings_file_path}")

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
            return any(("label" in item for item in value))

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
