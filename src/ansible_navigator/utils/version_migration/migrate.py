"""The ability to perform migrations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ansible_navigator.utils.ansi import COLOR
from ansible_navigator.utils.ansi import IS_TTY
from ansible_navigator.utils.ansi import blank_line
from ansible_navigator.utils.ansi import info
from ansible_navigator.utils.ansi import prompt_enter
from ansible_navigator.utils.ansi import prompt_yn
from ansible_navigator.utils.ansi import success
from ansible_navigator.utils.ansi import warning

from .definitions import MigrationType
from .definitions import migrations


# isort: off
# pylint: disable=unused-import
# Migrations will run in the order they are imported
from .v1_v2_settings_file import V1V2SettingsFile  # noqa: F401

# isort: on


def run_all_migrations(migration_types: tuple[MigrationType], settings_file_str: str = "") -> None:
    """Run all migrations.

    Args:
        migration_types: Type of migration
        settings_file_str: Path to the settings file
    """
    for migration_type in migration_types:
        run_migrations(settings_file_str, migration_type)


def _collect_migrations(
    settings_file_str: str,
    migration_type: MigrationType,
) -> list[Any]:
    """Instantiate, configure, and check-run migrations of a given type.

    Args:
        settings_file_str: Path to the settings file.
        migration_type: Type of migration.

    Returns:
        The list of configured migration instances.
    """
    migrations_to_run = [
        migration()
        for migration in migrations
        if getattr(migration, "migration_type", None) == migration_type
    ]
    for migration in migrations_to_run:
        migration.check = True
        if getattr(migration, "migration_type", None) == MigrationType.SETTINGS_FILE:
            migration.settings_file_path = Path(settings_file_str)
        migration.run()
    return migrations_to_run


def _display_needed_migrations(migrations_to_run: list[Any]) -> None:
    """Display the list of needed migrations.

    Args:
        migrations_to_run: The list of migration instances.
    """
    tense = "are" if IS_TTY else "were"
    blank_line()
    warning(color=COLOR, message=f"The following version migrations {tense} required:")
    for migration in migrations_to_run:
        if migration.needed_now:
            info(color=COLOR, message=f"  - {migration.name}")


def _execute_migrations(migrations_to_run: list[Any]) -> None:
    """Run migrations and report success or failure.

    Args:
        migrations_to_run: The list of migration instances.
    """
    for migration in migrations_to_run:
        blank_line()
        info(color=COLOR, message=f"{migration.name}:")
        migration.check = False
        migration.run()
    if not any(migration.needed_now for migration in migrations_to_run):
        blank_line()
        success(color=COLOR, message="Migration complete")
    else:
        blank_line()
        warning(
            color=COLOR,
            message="The following version migrations could not be completed:",
        )
        for migration in migrations_to_run:
            if migration.needed_now:
                info(color=COLOR, message=f" - {migration.name}")


def run_migrations(settings_file_str: str, migration_type: MigrationType) -> None:
    """Run migrations of a specific type.

    Args:
        settings_file_str: Path to the settings file
        migration_type: Type of migration
    """
    migrations_to_run = _collect_migrations(settings_file_str, migration_type)
    migratable = [migration.name for migration in migrations_to_run if migration.needed_now]

    if not migratable:
        return

    _display_needed_migrations(migrations_to_run)

    if not IS_TTY:
        blank_line()
        warning(color=COLOR, message="Migration not possible without a TTY")
        return

    if prompt_yn(message="Do you want to run them all?"):
        _execute_migrations(migrations_to_run)
    else:
        blank_line()
        warning(color=COLOR, message="Migration cancelled")
    blank_line()
    prompt_enter()
