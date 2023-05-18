"""Common definitions for a version migration."""
from __future__ import annotations

import contextlib

from enum import Enum
from pathlib import Path
from typing import Callable
from typing import Generic
from typing import TypeVar

from ansible_navigator.utils.ansi import COLOR
from ansible_navigator.utils.ansi import changed
from ansible_navigator.utils.ansi import failed
from ansible_navigator.utils.ansi import subtle
from ansible_navigator.utils.ansi import working


class MigrationType(Enum):
    """Enum for the type of migration."""

    SETTINGS_FILE = "settings"
    """Migration of the settings file."""


T = TypeVar("T")


class MigrationStep(Generic[T]):
    """Data class for a migration step."""

    def __init__(self, name: str) -> None:
        """Initialize a migration step.

        :param name: The name of the migration step
        """
        self.name: str = name
        """The name of the migration step"""
        self.needed: bool = False
        """Whether the migration step is needed"""
        self.function_name: str | None = None
        """The name of the function to call"""

    def print_start(self):
        """Output start information to the console."""
        message = f"Migrating '{self.name}'"
        information = f"{message:.<60}"
        working(color=COLOR, message=information)

    def print_failed(self) -> None:
        """Output fail information to the console."""
        message = f"Migration of '{self.name}'"
        information = f"{message:.<60}Failed"
        failed(color=COLOR, message=information)

    def print_updated(self) -> None:
        """Output updated information to the console."""
        message = f"Migration of '{self.name}'"
        information = f"{message:.<60}Updated"

        changed(color=COLOR, message=information)

    def print_not_needed(self) -> None:
        """Output not needed information to the console."""
        message = f"Migration of '{self.name}'"
        information = f"{message:.<60}Not needed"

        subtle(color=COLOR, message=information)

    @classmethod
    def register(cls: T, migration_step: T) -> Callable:
        """Register the migration step.

        :param migration_step: The migration step to register
        :return: The registered migration step
        """

        def wrapper(func):
            """Add the dunder collector to the func.

            :param func: The function to decorate
            :returns: The decorated function
            """
            migration_step.function_name = func.__name__
            func.__migration_step__ = migration_step
            return func

        return wrapper


class Migration:
    """Data class for a migration."""

    name = "Migration base class"
    """The name of the migration."""

    def __init__(self) -> None:
        """Initialize the migration."""
        self.check: bool = False
        """Whether the migration is needed."""
        self.settings_file_path: Path
        """The path of the settings file."""
        self.was_needed: bool = False
        """Whether the migration was needed."""

    def __init_subclass__(cls, *args, **kwargs):
        """Register the migration steps.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        super().__init_subclass__(*args, **kwargs)
        migrations.append(cls)

    @property
    def migration_steps(self) -> tuple[MigrationStep, ...]:
        """Return the registered diagnostics.

        :returns: The registered diagnostics
        """
        steps: list[MigrationStep] = []
        for func_name in vars(self.__class__):
            if func_name.startswith("_"):
                continue
            if hasattr(getattr(self, func_name), "__migration_step__"):
                step = getattr(self, func_name).__migration_step__
                steps.append(step)
        return tuple(steps)

    @property
    def needed_now(self) -> bool:
        """Return whether the migration is needed.

        :returns: Whether the migration is needed
        """
        return any(step.needed for step in self.migration_steps)

    def run(self, *args, **kwargs) -> None:
        """Run the migration.

        :param args: The positional arguments
        :param kwargs: The keyword arguments
        """

    def run_step(self, step: MigrationStep, *args, **kwargs) -> None:
        """Run the migration step.

        :param step: The migration step to run
        :param args: The positional arguments
        :param kwargs: The keyword arguments
        """
        if not isinstance(step.function_name, str):
            return
        function = getattr(self, step.function_name)
        if self.check:
            try:
                step.needed = function(*args, **kwargs)
            except Exception:  # noqa: BLE001
                step.needed = False
            return

        if not step.needed:
            step.print_not_needed()
            return

        step.print_start()
        with contextlib.suppress(Exception):
            step.needed = function(*args, **kwargs)

        if step.needed:
            step.print_failed()
        else:
            step.print_updated()
        return

    def run_steps(self, *args, **kwargs) -> None:
        """Run all registered migration steps.

        :param args: The positional arguments
        :param kwargs: The keyword arguments
        """
        for step in self.migration_steps:
            self.run_step(step, *args, **kwargs)


Migrations = list[type[Migration]]
migrations: Migrations = []
