"""An image introspector."""
from __future__ import annotations

import inspect
import json
import logging
import tempfile

from pathlib import Path

from ansible_navigator.data import image_introspect
from ansible_navigator.runner import Command


logger = logging.getLogger(__name__)


def run(image_name: str, container_engine: str) -> tuple[dict, list[str], int]:
    """Run runner to collect image details.

    :param image_name: The full image name
    :param container_engine: The container engine to use
    :returns: Output, errors and the return code
    """
    errors = []
    python_exec_path = "python3"

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        introspect_source = inspect.getsource(image_introspect)
        file = Path(tmp_dir_name) / "image_introspect.py"
        file.write_text(introspect_source)

        _runner = Command(
            cmdline=[str(file)],
            container_engine=container_engine,
            container_volume_mounts=[f"{tmp_dir_name}:{tmp_dir_name}"],
            executable_cmd=python_exec_path,
            execution_environment_image=image_name,
            execution_environment=True,
            navigator_mode="interactive",
        )
        output, error, return_code = _runner.run()
    if error:
        errors.append(error)
    parse_errors, parsed = parse(output)
    errors.extend(parse_errors)
    return parsed, errors, return_code


def parse(output) -> tuple[list[str], dict]:
    """Load and process the ``json`` output from the image introspection process.

    :param output: The output from the image introspection process
    :returns: The parsed output
    """
    errors = []
    try:
        if not output.startswith("{"):
            _warnings, json_str = output.split("{", 1)
            json_str = "{" + json_str
        else:
            json_str = output
        parsed = json.loads(json_str)
    except (json.decoder.JSONDecodeError, ValueError) as exc:
        errors.append("Unable to extract introspection from stdout")
        errors.append(f"error json loading output: '{exc!s}'")
        errors.append(output)
        return errors, {}

    return errors, parsed
