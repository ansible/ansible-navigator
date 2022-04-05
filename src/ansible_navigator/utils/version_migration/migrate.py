"""The ability to perform migrations."""


from pathlib import Path
from typing import Tuple

from ..ansi import COLOR
from ..ansi import IS_TTY
from ..ansi import blank_line
from ..ansi import info
from ..ansi import prompt_any
from ..ansi import prompt_yn
from ..ansi import success
from ..ansi import warning
from .defintions import MigrationType
from .defintions import migrations


# isort: off
# pylint: disable=unused-import
# Migrations will run in the order they are imported
from . import v1_v2_settings_file

# isort: on


def run_all_migrations(migration_types: Tuple[MigrationType], settings_file_str: str = "") -> None:
    """Run all migrations.

    :param migration_types: Type of migration
    :param settings_file_str: Path to the settings file
    """
    for migration_type in migration_types:
        run_migrations(settings_file_str, migration_type)


def run_migrations(settings_file_str: str, migration_type: MigrationType) -> None:
    """Run migrations of a specifc type.

    :param settings_file_str: Path to the settings file
    :param migration_type: Type of migration
    """
    # pylint: disable=too-many-branches
    migrations_to_run = tuple(
        migration() for migration in migrations if migration.migration_type == migration_type
    )

    for migration in migrations_to_run:
        migration.check = True
        if migration.migration_type == MigrationType.SETTINGS_FILE:
            migration.settings_file_path = Path(settings_file_str)
        migration.run()

    migratable = [migration.name for migration in migrations_to_run if migration.needed_now]

    if migratable:
        tense = "are" if IS_TTY else "were"

        blank_line()
        warning(color=COLOR, message=f"The following version migrations {tense} available:")
        for migration in migrations_to_run:
            if migration.needed_now:
                info(color=COLOR, message=f"  - {migration.name}")

        if not IS_TTY:
            blank_line()
            warning(color=COLOR, message="Migration not possible without a TTY")
            return

        if prompt_yn(message="Do you want to run them all?"):
            for migration in migrations_to_run:
                blank_line()
                warning(color=COLOR, message=f"{migration.name}:")
                migration.check = False
                migration.run()
            if not any(migration.needed_now for migration in migrations_to_run):
                blank_line()
                success(color=COLOR, message="Migration complete")
            else:
                blank_line()
                warning(color=COLOR, message="The following migrations could not be completed:")
                for migration in migrations_to_run:
                    if migration.needed_now:
                        info(color=COLOR, message=f" - {migration.name}")
        else:
            blank_line()
            warning(color=COLOR, message="Migration cancelled")
        blank_line()
        prompt_any(message="Press any key to continue")
