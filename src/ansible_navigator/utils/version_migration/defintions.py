"""Common defintions for a version migration."""

import time

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

from ..ansi import COLOR
from ..ansi import failed
from ..ansi import success
from ..ansi import working


class MigrationType(Enum):
    """Enum for the type of migration."""

    SETTINGS_FILE = "settings"
    UNKNOWN = "unknown"


T = TypeVar("T")


@dataclass
class MigrationStep(Generic[T]):
    """Data class for a migration step."""

    name: str
    """The name of the migration step."""
    needed: bool = False
    """Whether the migration is needed."""
    function_name: Optional[str] = None
    """The name of the function to call."""

    def start(self):
        """Output start information to the console."""
        message = f"Migrating '{self.name}'"
        information = f"{message:.<60}"
        working(color=COLOR, message=information)

    def fail(self, duration: float) -> None:
        """Output fail information to the console.

        :param duration: The duration of the collection
        """
        message = f"Migration of '{self.name}' failed"
        information = f"{message:.<60}{duration:.2f}s"
        failed(color=COLOR, message=information)

    def finish(self, duration: float) -> None:
        """Output finish information to the console.

        :param duration: The duration of the collection
        """
        message = f"Migration of '{self.name}' completed"
        information = f"{message:.<60}{duration:.2f}s"

        success(color=COLOR, message=information)

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


@dataclass
class Migration:
    """Data class for a migration."""

    check: bool = False
    """Whether the migration is needed."""
    name = "Migration base class"
    """The name of the migration."""
    migration_type: MigrationType = MigrationType.UNKNOWN
    """The type of migration."""
    settings_file_path: Path = Path()
    """The path to the settings file."""
    was_needed: bool = False
    """Whether the migration was needed."""

    def __init_subclass__(cls, *args, **kwargs):
        """Register the migration steps.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        super().__init_subclass__(*args, **kwargs)
        migrations.append(cls)

    @property
    def migration_steps(self) -> Tuple[MigrationStep, ...]:
        """Return the registered diagnostics.

        :returns: The registered diagnostics
        """
        steps: List[MigrationStep] = []
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
        return any((step.needed for step in self.migration_steps))

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
        if isinstance(step.function_name, str):
            if not self.check:
                step.start()
                start = time.time()
            try:
                step.needed = getattr(self, step.function_name)(*args, **kwargs)
            except Exception:  # pylint: disable=broad-except
                raise
                if not self.check:
                    step.fail(time.time() - start)
                    return
            if not self.check:
                step.finish(time.time() - start)

    def run_steps(self, *args, **kwargs) -> None:
        """Run all registered migration steps.

        :param args: The positional arguments
        :param kwargs: The keyword arguments
        """
        for step in self.migration_steps:
            self.run_step(step, *args, **kwargs)


Migrations = List[Type[Migration]]
migrations: Migrations = []
