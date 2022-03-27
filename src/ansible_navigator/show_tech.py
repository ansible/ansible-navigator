"""Produce a diagnostics report in json format."""
import datetime
import json
import sys
import traceback

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Union

from pkg_resources import working_set

from .command_runner import Command
from .command_runner import CommandRunner
from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import to_effective
from .configuration_subsystem import to_sources
from .image_manager import introspect
from .image_manager import introspector
from .utils.functions import ExitMessage
from .utils.functions import LogMessage
from .utils.functions import now_iso
from .utils.functions import shlex_join
from .utils.serialize import Loader
from .utils.serialize import yaml


class C:  # pylint: disable=invalid-name
    """Color constants."""

    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    END = "\033[0m"


JSONTypes = Union[bool, int, str, Dict, List]


def failed(message: str):
    """Output failure information to the console.

    :param message: The message to output
    """
    print(f"{C.RED}{message}{C.END}")


def success(message: str):
    """Output success information to the console.

    :param message: The message to output
    """
    print(f"{C.GREEN}{message}{C.END}")


def warning(message: str):
    """Output warning information to the console.

    :param message: The message to output
    """
    print(f"{C.YELLOW}{message}{C.END}")


def working(message: str):
    """Output working information to the console.

    :param message: The message to output
    """
    print(f"{C.GREY}{message}{C.END}", end="", flush=True)


@dataclass
class Collector:
    """Data class for a collector."""

    name: str

    def start(self):
        """Output information to the console."""
        information = f"Collecting {self.name} information".ljust(50, ".")
        working(information)

    def fail(self, duration: float) -> None:
        """Output information to the console.

        :param duration: The duration of the collection
        """
        information = f"\rCollecting {self.name} failed ({duration:.2f}s)\033[K"
        failed(information)

    def finish(self, duration: float) -> None:
        """Output information to the console.

        :param duration: The duration of the collection
        """
        information = f"\r{self.name.capitalize()} information collected. ({duration:.2f}s)\033[K"
        success(information)


@dataclass
class Diagnostics:
    """Data class for the diagnostics."""

    # pylint: disable=too-many-instance-attributes

    __WARNING__: Dict[str, JSONTypes]  # pylint: disable=invalid-name
    basics: Dict[str, JSONTypes]
    container_engines: Dict[str, JSONTypes]
    execution_environment: Dict[str, JSONTypes]
    initialization: Dict[str, JSONTypes]
    local_system: Dict[str, JSONTypes]
    python_packages: Dict[str, JSONTypes]
    settings: Dict[str, JSONTypes]
    settings_file: Dict[str, JSONTypes]


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
        global DIAGNOSTIC_FAILURES  # pylint: disable=global-statement
        start = datetime.datetime.now()
        collector = func.__collector__
        collector.start()
        try:
            result = func(*args, **kwargs)
            duration = (datetime.datetime.now() - start).total_seconds()
            collector.finish(duration=duration)
        except Exception as error:  # pylint: disable=broad-except
            result = {"error": str(error) + "\n" + traceback.format_exc()}
            duration = (datetime.datetime.now() - start).total_seconds()
            collector.fail(duration=duration)
            DIAGNOSTIC_FAILURES += 1
        result["duration"] = duration
        return result

    return wrapper


class ShowTech:
    """Show tech."""

    WARNING = "The following output may contain sensitive data, please review it carefully."

    def __init__(
        self,
        args: ApplicationConfiguration,
        messages: List[LogMessage],
        exit_messages: List[ExitMessage],
    ):
        """Initialize the ShowTech class.

        :param args: The current settings
        :param messages: The messages to log
        :param exit_messages: The exit messages to log
        """
        self._args = args
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
        warning(self.WARNING)
        diagnostics = Diagnostics(
            __WARNING__=self._warning(),
            basics=self._basics(),
            container_engines=self._container_engines(),
            execution_environment=self._execution_environment(),
            initialization=self._initialization(),
            local_system=self._local_system(),
            python_packages=self._python_packages(),
            settings=self._settings(),
            settings_file=self._settings_file(),
        )
        time = now_iso("local")
        path = Path(f"show_tech_{time}.json")
        path.write_text(json.dumps(asdict(diagnostics), indent=4, sort_keys=True), encoding="utf-8")
        message = f"\nDiagnostics written to: {path}."
        if DIAGNOSTIC_FAILURES > 0:
            warning(message)
        else:
            success(message)
        sys.exit(0)

    @diagnostic_runner
    @register(Collector(name="warning"))
    def _warning(self) -> Dict[str, JSONTypes]:
        """Add a warning.

        :returns: The warning
        """
        return {"message": self.WARNING}

    @diagnostic_runner
    @register(Collector(name="basic"))
    def _basics(self) -> Dict[str, JSONTypes]:
        """Add basic information.

        :returns: The basic information
        """
        return {
            "application_name": self._args.application_name,
            "application_version": str(self._args.application_version),
            "action_packages": list(self._args.internals.action_packages),
            "original_command": shlex_join(sys.argv),
            "settings_file_path": str(self._args.internals.settings_file_path),
            "settings_source": str(self._args.internals.settings_source),
            "share_directory": self._args.internals.share_directory,
        }

    @diagnostic_runner
    @register(Collector(name="container engines"))
    def _container_engines(self) -> Dict[str, JSONTypes]:
        """Add container engines.

        :returns: The container engines
        """
        commands = [
            Command(identity="podman", command="podman --version", post_process=lambda c: c),
            Command(identity="docker", command="docker --version", post_process=lambda c: c),
        ]
        CommandRunner().run_single_proccess(commands)
        engines: Dict[str, JSONTypes] = {}
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
    def _execution_environment(self) -> Dict[str, JSONTypes]:
        """Add execution environment information.

        :returns: The execution environment information
        """
        details, errors, return_code = introspector.run(
            image_name=self._args.execution_environment_image,
            container_engine=self._args.container_engine,
        )
        details = {"details": details, "errors": errors, "return_code": return_code}
        return details

    @diagnostic_runner
    @register(Collector(name="initialization"))
    def _initialization(self) -> Dict[str, JSONTypes]:
        """Add initialization information.

        :returns: The initialization information
        """
        return {
            "messages": [msg.message for msg in self._messages],
            "exit_messages": [msg.message for msg in self._exit_messages],
        }

    @staticmethod
    @diagnostic_runner
    @register(Collector(name="local system"))
    def _local_system() -> Dict[str, JSONTypes]:
        """Add local system information.

        :returns: The local system information
        """
        results = introspect.main(serialize=False)
        if results:
            sections = {"errors": results.pop("errors")}
            for section, information in results.items():
                # pylint: disable=invalid-sequence-index
                sections[section] = information["details"]
            return sections
        return {}

    @staticmethod
    @diagnostic_runner
    @register(Collector(name="python packages"))
    def _python_packages() -> Dict[str, JSONTypes]:
        """Add python packages information.

        :returns: The python packages information
        """
        return {
            i.key: {"location": i.location, "name": i.key, "version": i.version}
            for i in working_set  # pylint: disable=not-an-iterable
        }

    @diagnostic_runner
    @register(Collector(name="settings"))
    def _settings(self) -> Dict[str, JSONTypes]:
        """Add settings information.

        :returns: The settings information
        """
        return {
            "effective": to_effective(self._args),
            "sources": to_sources(self._args),
        }

    @diagnostic_runner
    @register(Collector(name="settings file"))
    def _settings_file(self) -> Dict[str, JSONTypes]:
        """Add settings file information.

        :returns: The settings file information
        """
        if self._args.internals.settings_file_path:
            contents = Path(self._args.internals.settings_file_path).read_text(encoding="utf-8")
            return yaml.load(contents, Loader=Loader)
        return {}
