"""An image introspector."""
import inspect
import json
import logging
import tempfile

from pathlib import Path
from typing import Dict
from typing import Tuple

from ..runner import Command
from . import introspect


logger = logging.getLogger(__name__)


def run(image_name: str, container_engine: str) -> Tuple[Dict, str, int]:
    """Run runner to collect image details.

    :param image_name: The full image name
    :param container_engine: The container engine to use
    :returns: Output, errors and the return code
    """
    python_exec_path = "python3"

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        introspect_source = inspect.getsource(introspect)
        file = Path(tmp_dir_name) / "introspect.py"
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
        # logger.debug(
        #     f"Invoke runner with executable_cmd: {python_exec_path}" + f" and kwargs: {kwargs}",
        # )
        output, error, return_code = _runner.run()
    return parse(output), error, return_code


def parse(output) -> Dict:
    """Load and process the ``json`` output from the image introspection process.

    :param output: The output from the image introspection process
    :returns: The parsed output
    """
    try:
        if not output.startswith("{"):
            _warnings, json_str = output.split("{", 1)
            json_str = "{" + json_str
        else:
            json_str = output
        parsed = json.loads(json_str)
        # self._logger.debug("json loading output succeeded")
    except (json.decoder.JSONDecodeError, ValueError):
        # self._logger.error("Unable to extract introspection from stdout")
        # self._logger.debug("error json loading output: '%s'", str(exc))
        # self._logger.debug(output)
        # self._logger.error(
        #     "Image introspection failed (parsed), the return value was: %s",
        #     output[0:1000],
        # )
        return {}

    # for error in parsed["errors"]:
    #     self._logger.error("%s %s", error["path"], error["error"])
    return parsed
