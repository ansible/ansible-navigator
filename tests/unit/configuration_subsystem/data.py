"""Data used by the adjacent tests.

Note: Some of these are defined as dictionaries for ease but all should be frozen
before use so they are immutable within the tests
"""

from collections.abc import Generator
from typing import Any

import pytest

from _pytest.mark.structures import ParameterSet


def d2t(dictionary: dict[Any, Any]) -> tuple[Any, ...]:
    """Turn the data dictionary into a frozen set so they are immutable.

    :param dictionary: Data to be a tuple
    :returns: Data dict as a tuple
    """
    return tuple(dictionary.items())


BASE_SHORT_CLI = """
--rad /tmp/test1
--rac 10
--rt 300
--ce docker
--co=--net=host
--dc false
--ecmd vim_base
--econ True
--ee False
--eei test_image:latest
--la false
--lf /tmp/app.log
--ll warning
--osc4 false
--penv FOO
--penv BAR
--pp never
--senv E1=V1
--senv E2=V2
"""

BASE_LONG_CLI = """
--ansible-runner-artifact-dir /tmp/test1
--ansible-runner-rotate-artifacts-count 10
--ansible-runner-timeout 300
--container-engine docker
--container-options=--net=host
--display-color false
--editor-command vim_base
--editor-console True
--execution-environment False
--execution-environment-image test_image:latest
--log-append false
--log-file /tmp/app.log
--log-level warning
--osc4 false
--pass-environment-variable FOO
--pass-environment-variable BAR
--pull-policy never
--set-environment-variable E1=V1
--set-environment-variable E2=V2
"""

BASE_EXPECTED = d2t(
    {
        "ansible_runner_artifact_dir": "/tmp/test1",
        "ansible_runner_rotate_artifacts_count": 10,
        "ansible_runner_timeout": 300,
        "container_engine": "docker",
        "container_options": ["--net=host"],
        "display_color": False,
        "editor_command": "vim_base",
        "editor_console": True,
        "execution_environment": False,
        "execution_environment_image": "test_image:latest",
        "log_append": False,
        "log_file": "/tmp/app.log",
        "log_level": "warning",
        "osc4": False,
        "pass_environment_variable": ["FOO", "BAR"],
        "pull_policy": "never",
        "set_environment_variable": {"E1": "V1", "E2": "V2"},
    },
)


CLI_DATA_COLLECTIONS: list[tuple[str, dict[Any, Any]]] = [
    ("collections -m interactive", {"app": "collections", "mode": "interactive"}),
]
CLI_DATA_CONFIG: list[tuple[str, dict[Any, Any]]] = [
    ("config", {"app": "config"}),
    ("config dump", {"app": "config", "cmdline": ["dump"]}),
    (
        "config dump -c /tmp/ansible.cfg",
        {"app": "config", "cmdline": ["dump"], "config": "/tmp/ansible.cfg"},
    ),
]
CLI_DATA_DOC: list[tuple[str, dict[Any, Any]]] = [
    ("doc shell", {"app": "doc", "plugin_name": "shell"}),
    ("doc shell --mode stdout", {"app": "doc", "mode": "stdout", "plugin_name": "shell"}),
    ("doc shell -t become", {"app": "doc", "plugin_name": "shell", "plugin_type": "become"}),
    (
        "doc shell --type become",
        {"app": "doc", "plugin_name": "shell", "plugin_type": "become"},
    ),
]
CLI_DATA_INVENTORY: list[tuple[str, dict[Any, Any]]] = [
    ("inventory -i /tmp/inv1.yml", {"app": "inventory", "inventory": ["/tmp/inv1.yml"]}),
    (
        "inventory -i /tmp/inv1.yml -m stdout",
        {"app": "inventory", "inventory": ["/tmp/inv1.yml"], "mode": "stdout"},
    ),
    ("inventory -i host1,host2", {"app": "inventory", "inventory": ["host1,host2"]}),
    (
        "inventory -i /tmp/inv1.yml -i /tmp/inv2.yml",
        {"app": "inventory", "inventory": ["/tmp/inv1.yml", "/tmp/inv2.yml"]},
    ),
    ("inventory --inventory /tmp/inv1.yml", {"app": "inventory", "inventory": ["/tmp/inv1.yml"]}),
    (
        "inventory --inventory /tmp/inv1.yml --inventory /tmp/inv2.yml",
        {"app": "inventory", "inventory": ["/tmp/inv1.yml", "/tmp/inv2.yml"]},
    ),
]
CLI_DATA_INVENTORY_COLUMNS: list[tuple[str, dict[Any, Any]]] = [
    (
        "inventory -i /tmp/inv1.yml --ic hv1",
        {"app": "inventory", "inventory": ["/tmp/inv1.yml"], "inventory_column": ["hv1"]},
    ),
    (
        "inventory -i /tmp/inv1.yml -i /tmp/inv2.yml --ic hv1 --ic hv2",
        {
            "app": "inventory",
            "inventory": ["/tmp/inv1.yml", "/tmp/inv2.yml"],
            "inventory_column": ["hv1", "hv2"],
        },
    ),
    (
        "inventory --inventory /tmp/inv1.yml --inventory-column hv1",
        {"app": "inventory", "inventory": ["/tmp/inv1.yml"], "inventory_column": ["hv1"]},
    ),
    (
        (
            "inventory --inventory /tmp/inv1.yml --inventory /tmp/inv2.yml"
            " --inventory-column hv1 --inventory-column hv2"
        ),
        {
            "app": "inventory",
            "inventory": ["/tmp/inv1.yml", "/tmp/inv2.yml"],
            "inventory_column": ["hv1", "hv2"],
        },
    ),
]
CLI_DATA_REPLAY: list[tuple[str, dict[Any, Any]]] = [
    (
        "replay /tmp/part.json -m interactive",
        {"app": "replay", "mode": "interactive", "playbook_artifact_replay": "/tmp/part.json"},
    ),
]
CLI_DATA_RUN: list[tuple[str, dict[Any, Any]]] = [
    ("run /tmp/site.yml", {"app": "run", "playbook": "/tmp/site.yml"}),
    ("run /tmp/site.yml -m stdout", {"app": "run", "mode": "stdout", "playbook": "/tmp/site.yml"}),
    (
        "run /tmp/site.yml --check --diff --forks 50",
        {
            "app": "run",
            "cmdline": ["--check", "--diff", "--forks", "50"],
            "playbook": "/tmp/site.yml",
        },
    ),
    (
        "run /tmp/site.yml -i /tmp/inv1.yml",
        {"app": "run", "playbook": "/tmp/site.yml", "inventory": ["/tmp/inv1.yml"]},
    ),
    (
        "run /tmp/site.yml --inventory /tmp/inv1.yml",
        {"app": "run", "playbook": "/tmp/site.yml", "inventory": ["/tmp/inv1.yml"]},
    ),
    (
        "run /tmp/site.yml -i /tmp/inv1.yml -i /tmp/inv2.yml",
        {
            "app": "run",
            "playbook": "/tmp/site.yml",
            "inventory": ["/tmp/inv1.yml", "/tmp/inv2.yml"],
        },
    ),
    (
        "run /tmp/site.yml --inventory /tmp/inv1.yml --inventory /tmp/inv2.yml",
        {
            "app": "run",
            "playbook": "/tmp/site.yml",
            "inventory": ["/tmp/inv1.yml", "/tmp/inv2.yml"],
        },
    ),
]


def cli_data() -> Generator[ParameterSet, None, None]:
    """Turn them all into tuples.

    :returns: CLI data in tuples
    """
    aggregated = (
        CLI_DATA_COLLECTIONS
        + CLI_DATA_CONFIG
        + CLI_DATA_DOC
        + CLI_DATA_INVENTORY
        + CLI_DATA_INVENTORY_COLUMNS
        + CLI_DATA_REPLAY
        + CLI_DATA_RUN
    )
    frozen = (
        pytest.param(values[0], d2t(values[1]), id=str(index))
        for index, values in enumerate(aggregated)
    )
    return frozen


CLI_DATA = cli_data()

ENV_VAR_DATA = [
    pytest.param("ansible_runner_artifact_dir", "/tmp/test1", "/tmp/test1", id="0"),
    pytest.param("ansible_runner_rotate_artifacts_count", "10", 10, id="1"),
    pytest.param("ansible_runner_timeout", "300", 300, id="2"),
    pytest.param("ansible_runner_write_job_events", "false", False, id="3"),
    pytest.param("app", "config", "config", id="4"),
    pytest.param("cmdline", "--forks 15", ["--forks", "15"], id="5"),
    pytest.param("collection_doc_cache_path", "/tmp/cache.db", "/tmp/cache.db", id="6"),
    pytest.param("config", "/tmp/ansible.cfg", "/tmp/ansible.cfg", id="7"),
    pytest.param("container_engine", "docker", "docker", id="8"),
    pytest.param("container_options", "--net=host", ["--net=host"], id="9"),
    pytest.param("display_color", "yellow is the color of a banana", False, id="10"),
    pytest.param("editor_command", "nano_env_var", "nano_env_var", id="11"),
    pytest.param("editor_console", "false", False, id="12"),
    pytest.param("enable_prompts", "false", False, id="13"),
    pytest.param("exec_command", "/bin/foo", "/bin/foo", id="14"),
    pytest.param("exec_shell", "false", False, id="15"),
    pytest.param("execution_environment", "false", False, id="16"),
    pytest.param("execution_environment_image", "test_image:latest", "test_image:latest", id="17"),
    pytest.param(
        "execution_environment_volume_mounts",
        "/tmp:/test1:Z;/tmp:/test2:z",
        ["/tmp:/test1:Z", "/tmp:/test2:z"],
        id="18",
    ),
    pytest.param("format", "json", "json", id="19"),
    pytest.param("help_builder", "false", False, id="20"),
    pytest.param("help_config", "false", False, id="21"),
    pytest.param("help_doc", "false", False, id="22"),
    pytest.param("help_inventory", "false", False, id="23"),
    pytest.param("help_playbook", "false", False, id="24"),
    pytest.param(
        "images_details",
        "ansible_version,python_version",
        ["ansible_version", "python_version"],
        id="25",
    ),
    pytest.param(
        "inventory",
        "/tmp/test1.yaml,/tmp/test2.yml",
        ["/tmp/test1.yaml", "/tmp/test2.yml"],
        id="26",
    ),
    pytest.param("inventory_column", "t1,t2,t3", ["t1", "t2", "t3"], id="27"),
    pytest.param(
        "lint_config",
        "/tmp/ansible-lint-config.yml",
        "/tmp/ansible-lint-config.yml",
        id="28",
    ),
    pytest.param("lintables", "/tmp/lintables", "/tmp/lintables", id="29"),
    pytest.param("log_append", "false", False, id="30"),
    pytest.param("log_file", "/tmp/app.log", "/tmp/app.log", id="31"),
    pytest.param("log_level", "info", "info", id="32"),
    pytest.param("mode", "interactive", "interactive", id="33"),
    pytest.param("osc4", "false", False, id="34"),
    pytest.param("pass_environment_variable", "a,b,c", ["a", "b", "c"], id="35"),
    pytest.param("playbook", "/tmp/site.yaml", "/tmp/site.yaml", id="36"),
    pytest.param("playbook_artifact_enable", "false", False, id="37"),
    pytest.param("playbook_artifact_replay", "/tmp/load.json", "/tmp/load.json", id="38"),
    pytest.param("playbook_artifact_save_as", "/tmp/save.json", "/tmp/save.json", id="39"),
    pytest.param("plugin_name", "shell", "shell", id="40"),
    pytest.param("plugin_type", "become", "become", id="41"),
    pytest.param("pull_arguments", "--tls-verify=false", ["--tls-verify=false"], id="42"),
    pytest.param("pull_policy", "never", "never", id="43"),
    pytest.param(
        "set_environment_variable",
        "T1=A,T2=B,T3=C",
        {"T1": "A", "T2": "B", "T3": "C"},
        id="44",
    ),
    pytest.param("settings_effective", "false", False, id="45"),
    pytest.param("settings_sample", "false", False, id="46"),
    pytest.param("settings_schema", "json", "json", id="47"),
    pytest.param("settings_sources", "false", False, id="48"),
    pytest.param("time_zone", "Japan", "Japan", id="49"),
    pytest.param("workdir", "/tmp/", "/tmp/", id="50"),
]

SETTINGS = [
    pytest.param("ansible-navigator_empty.yml", "empty", id="empty"),
    pytest.param("ansible-navigator.yml", "full", id="full"),
]
