"""Produce a diagnostics report in json format."""
from __future__ import annotations

import datetime
import sys
import traceback

from collections.abc import Iterator
from dataclasses import asdict
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path
from sys import stdout
from typing import Any
from typing import Callable
from typing import Union

from .command_runner import Command
from .command_runner import CommandRunner
from .configuration_subsystem import Constants
from .configuration_subsystem import to_effective
from .configuration_subsystem import to_sources
from .configuration_subsystem.definitions import ApplicationConfiguration
from .data import image_introspect
from .image_manager import introspector
from .utils import ansi
from .utils.compatibility import importlib_metadata
from .utils.definitions import ExitMessage
from .utils.definitions import LogMessage
from .utils.functions import now_iso
from .utils.functions import shlex_join
from .utils.serialize import Loader
from .utils.serialize import write_diagnostics_json
from .utils.serialize import yaml


JSONTypes = Union[bool, int, str, dict, list[Any]]


@dataclass
class Collector:
    """Data class for a collector."""

    name: str

    def start(self, color: bool):
        """Output start information to the console.

        :param color: Whether to color the message
        """
        message = f"Collecting {self.name} information"
        information = f"{message:.<60}"
        ansi.working(color=color, message=information)

    def fail(self, color: bool, duration: float) -> None:
        """Output fail information to the console.

        :param color: Whether to color the message
        :param duration: The duration of the collection
        """
        message = f"{self.name.capitalize()} information collection failed"
        information = f"{message:.<60}{duration:.2f}s"
        ansi.failed(color=color, message=information)

    def finish(self, color: bool, duration: float) -> None:
        """Output finish information to the console.

        :param color: Whether to color the message
        :param duration: The duration of the collection
        """
        message = f"{self.name.capitalize()} information collected"
        information = f"{message:.<60}{duration:.2f}s"

        # information = f"{message:<.50}{duration_message:>.7}"
        ansi.success(color=color, message=information)


@dataclass
class Diagnostics:
    """Data class for the diagnostics."""

    # pylint: disable=too-many-instance-attributes

    __WARNING__: dict[str, JSONTypes]
    basics: dict[str, JSONTypes]
    container_engines: dict[str, JSONTypes]
    execution_environment: dict[str, JSONTypes]
    initialization: dict[str, JSONTypes]
    local_system: dict[str, JSONTypes]
    logs: dict[str, JSONTypes]
    python_packages: dict[str, JSONTypes]
    settings: dict[str, JSONTypes]
    settings_file: dict[str, JSONTypes]


def register(collector: Collector):
    """Register a collector.

    :param collector: The collector to register
    :returns: The decorator
    """

    def decorator(func):
        """Add the dunder collector to the func.

        :param func: The function to decorate
        :returns: The decorated function
        """
        func.__collector__ = collector
        return func

    return decorator


DIAGNOSTIC_FAILURES = 0


class FailedCollectionError(Exception):
    """Exception for a failed collection."""

    def __init__(self, errors):
        """Initialize the exception.

        :param errors: The errors
        """
        super().__init__()
        self.errors = errors


def diagnostic_runner(func):
    """Wrap and run a collector.

    :param func: The function to wrap
    :returns: The decorator
    """

    def wrapper(*args, **kwargs):
        """Wrap and run the collector.

        :param args: The positional arguments
        :param kwargs: The keyword arguments
        :returns: The result of the function with elapsed or error information
        """
        global DIAGNOSTIC_FAILURES
        start = datetime.datetime.now()
        color = args[0].color
        collector = func.__collector__
        collector.start(color=color)
        try:
            result = func(*args, **kwargs)
            duration = (datetime.datetime.now() - start).total_seconds()
            collector.finish(color=color, duration=duration)
        except FailedCollectionError as error:
            # A collector exception, has data
            result = error.errors
            duration = (datetime.datetime.now() - start).total_seconds()
            collector.fail(color=color, duration=duration)
            DIAGNOSTIC_FAILURES += 1
        except Exception as error:  # noqa: BLE001
            # Any other exception, has no data
            result = {"error": str(error) + "\n" + traceback.format_exc()}
            duration = (datetime.datetime.now() - start).total_seconds()
            collector.fail(color=color, duration=duration)
            DIAGNOSTIC_FAILURES += 1
        result["duration"] = round(duration)
        return result

    return wrapper


class DiagnosticsCollector:
    """The diagnostics collector."""

    WARNING = "The following output may contain sensitive data, please review it carefully."

    def __init__(
        self,
        args: ApplicationConfiguration,
        messages: list[LogMessage],
        exit_messages: list[ExitMessage],
    ):
        """Initialize the ShowTech class.

        :param args: The current settings
        :param messages: The messages to log
        :param exit_messages: The exit messages to log
        """
        self._args = args
        self.color = args.display_color and stdout.isatty()
        self._messages = messages
        self._exit_messages = exit_messages

    @property
    def registered(self) -> Iterator[Callable]:
        """Return the registered diagnostics.

        :returns: The registered diagnostics
        """
        return (getattr(self, f) for f in dir(self) if hasattr(getattr(self, f), "registration"))

    def run(self) -> None:
        """Collect as much information as possible about everything and dump to a json file."""
        ansi.warning(color=self.color, message=self.WARNING)
        diagnostics = Diagnostics(
            __WARNING__=self._warning(),
            basics=self._basics(),
            container_engines=self._container_engines(),
            execution_environment=self._execution_environment(),
            initialization=self._initialization(),
            local_system=self._local_system(),
            logs=self._log_collector(),
            python_packages=self._python_packages(),
            settings=self._settings(),
            settings_file=self._settings_file(),
        )

        time = now_iso("local")
        file_name = f"diagnostics-{time}.json"
        path = f"{Path.home()}/{file_name}"
        mode = 0o600
        write_diagnostics_json(path, mode, asdict(diagnostics))
        message = f"\nDiagnostics written to: {path}"

        if DIAGNOSTIC_FAILURES > 0:
            ansi.warning(color=self.color, message=message)
        else:
            ansi.success(color=self.color, message=message)
        sys.exit(0)

    @diagnostic_runner
    @register(Collector(name="warning"))
    def _warning(self) -> dict[str, JSONTypes]:
        """Add a warning.

        :returns: The warning
        """
        return {"message": self.WARNING}

    @diagnostic_runner
    @register(Collector(name="basic"))
    def _basics(self) -> dict[str, JSONTypes]:
        """Add basic information.

        :returns: The basic information
        """
        return {
            "application_name": self._args.application_name,
            "application_version": str(self._args.application_version),
            "action_packages": list(self._args.internals.action_packages),
            "cache_path": str(self._args.internals.cache_path),
            "collection_doc_cache": str(self._args.internals.collection_doc_cache),
            "original_command": shlex_join(sys.argv),
            "settings_file_path": str(self._args.internals.settings_file_path),
            "settings_source": str(self._args.internals.settings_source),
        }

    @diagnostic_runner
    @register(Collector(name="container engines"))
    def _container_engines(self) -> dict[str, JSONTypes]:
        """Add container engines.

        :returns: The container engines
        """
        commands = [
            Command(identity="podman", command="podman --version", post_process=lambda c: c),
            Command(identity="docker", command="docker --version", post_process=lambda c: c),
        ]
        CommandRunner().run_single_process(commands)
        engines: dict[str, JSONTypes] = {}
        for command in commands:
            engines[command.identity] = {
                "return_code": command.return_code,
                "selected": bool(self._args.container_engine == command.identity),
                "stdout": command.stdout,
                "stderr": command.stderr,
            }
        return engines

    @diagnostic_runner
    @register(Collector(name="execution environment"))
    def _execution_environment(self) -> dict[str, JSONTypes]:
        """Add execution environment information.

        :raises FailedCollectionError: If the collection process fails
        :returns: The execution environment information
        """
        if self._args.entry("container_engine").value.source is Constants.DEFAULT_CFG:
            return {"errors": "No container engine available or found"}

        details, errors, return_code = introspector.run(
            image_name=self._args.execution_environment_image,
            container_engine=self._args.container_engine,
        )
        details = {"details": details, "errors": errors, "return_code": return_code}
        if errors or not details:
            raise FailedCollectionError(details)
        return details

    @diagnostic_runner
    @register(Collector(name="initialization"))
    def _initialization(self) -> dict[str, JSONTypes]:
        """Add initialization information.

        :returns: The initialization information
        """
        return {
            "messages": [msg.message for msg in self._messages],
            "exit_messages": [msg.message for msg in self._exit_messages],
        }

    @diagnostic_runner
    @register(Collector(name="log"))
    def _log_collector(self) -> dict[str, JSONTypes]:
        """Add log collector information.

        :returns: The log collector information
        """
        logs: list[JSONTypes] = []
        cwd_log = Path("./ansible-navigator.log")
        if cwd_log.exists():
            contents = cwd_log.read_text(encoding="utf-8").splitlines()
            log = {
                "name": str(cwd_log),
                "contents": contents,
                "date": cwd_log.stat().st_mtime,
            }
            logs.append(log)
        settings_log = Path(self._args.log_file)
        if cwd_log != settings_log and settings_log.exists():
            contents = settings_log.read_text(encoding="utf-8").splitlines()
            log = {
                "name": str(settings_log),
                "contents": contents,
                "date": settings_log.stat().st_mtime,
            }
            logs.append(log)
        return {"found": bool(logs), "logs": logs}

    @diagnostic_runner
    @register(Collector(name="local system"))
    def _local_system(self) -> dict[str, JSONTypes]:
        """Add local system information.

        :raises FailedCollectionError: If the collection process fails
        :returns: The local system information
        """
        results = image_introspect.main(serialize=False)
        if not results:
            raise FailedCollectionError(results)
        if results.get("errors"):
            raise FailedCollectionError(results["errors"])
        return {"details": results}

    @diagnostic_runner
    @register(Collector(name="python packages"))
    def _python_packages(self) -> dict[str, JSONTypes]:
        """Add python packages information.

        :returns: The python packages information
        """
        pkgs = importlib_metadata.packages_distributions()
        meta: dict[str, Any] = {}
        for _python_name, pkg_names in pkgs.items():
            for pkg_name in pkg_names:
                if pkg_name not in meta:
                    meta[pkg_name] = importlib_metadata.metadata(pkg_name).json
                    spec = find_spec(pkg_name)
                    if spec:
                        meta[pkg_name]["location"] = spec.origin
                    meta[pkg_name]["requires"] = importlib_metadata.distribution(pkg_name).requires
        return meta

    @diagnostic_runner
    @register(Collector(name="settings"))
    def _settings(self) -> dict[str, JSONTypes]:
        """Add settings information.

        :returns: The settings information
        """
        return {
            "effective": to_effective(self._args),
            "sources": to_sources(self._args),
        }

    @diagnostic_runner
    @register(Collector(name="settings file"))
    def _settings_file(self) -> dict[str, JSONTypes]:
        """Add settings file information.

        :returns: The settings file information
        """
        contents: dict[str, JSONTypes] = {}
        if self._args.internals.settings_file_path:
            text = Path(self._args.internals.settings_file_path).read_text(encoding="utf-8")
            contents = yaml.load(text, Loader=Loader)
        return {"contents": contents}
