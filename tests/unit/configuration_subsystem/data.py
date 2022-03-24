"""data used by the adjacent tests

Note: Some of these are defined as dictionaries for ease but all should be frozen
before use so they are immutable within the tests
"""


def d2t(dictionary):
    """turn the data dictionary into a frozen set
    so they are immutable
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


CLI_DATA_COLLECTIONS = [
    ("collections -m interactive", {"app": "collections", "mode": "interactive"}),
]
CLI_DATA_CONFIG = [
    ("config", {"app": "config"}),
    ("config dump", {"app": "config", "cmdline": ["dump"]}),
    (
        "config dump -c /tmp/ansible.cfg",
        {"app": "config", "cmdline": ["dump"], "config": "/tmp/ansible.cfg"},
    ),
]
CLI_DATA_DOC = [
    ("doc shell", {"app": "doc", "plugin_name": "shell"}),
    ("doc shell --mode stdout", {"app": "doc", "mode": "stdout", "plugin_name": "shell"}),
    ("doc shell -t become", {"app": "doc", "plugin_name": "shell", "plugin_type": "become"}),
    (
        "doc shell --type become",
        {"app": "doc", "plugin_name": "shell", "plugin_type": "become"},
    ),
]
CLI_DATA_INVENTORY = [
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
CLI_DATA_INVENTORY_COLUMNS = [
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
CLI_DATA_REPLAY = [
    (
        "replay /tmp/part.json -m interactive",
        {"app": "replay", "mode": "interactive", "playbook_artifact_replay": "/tmp/part.json"},
    ),
]
CLI_DATA_RUN = [
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


def cli_data():
    """turn them all into tuples"""
    aggregated = (
        CLI_DATA_COLLECTIONS
        + CLI_DATA_CONFIG
        + CLI_DATA_DOC
        + CLI_DATA_INVENTORY
        + CLI_DATA_INVENTORY_COLUMNS
        + CLI_DATA_REPLAY
        + CLI_DATA_RUN
    )
    frozen = [(cmd, d2t(expected)) for cmd, expected in aggregated]
    return frozen


CLI_DATA = cli_data()

ENV_VAR_DATA = [
    ("ansible_runner_artifact_dir", "/tmp/test1", "/tmp/test1"),
    ("ansible_runner_rotate_artifacts_count", "10", 10),
    ("ansible_runner_timeout", "300", 300),
    ("app", "config", "config"),
    ("cmdline", "--forks 15", ["--forks", "15"]),
    ("collection_doc_cache_path", "/tmp/cache.db", "/tmp/cache.db"),
    ("config", "/tmp/ansible.cfg", "/tmp/ansible.cfg"),
    ("container_engine", "docker", "docker"),
    ("container_options", "--net=host", ["--net=host"]),
    ("display_color", "yellow is the color of a banana", False),
    ("editor_command", "nano_env_var", "nano_env_var"),
    ("editor_console", "false", False),
    ("exec_command", "/bin/foo", "/bin/foo"),
    ("exec_shell", "false", False),
    ("execution_environment", "false", False),
    ("execution_environment_image", "test_image:latest", "test_image:latest"),
    (
        "execution_environment_volume_mounts",
        "/tmp:/test1:Z;/tmp:/test2:z",
        ["/tmp:/test1:Z", "/tmp:/test2:z"],
    ),
    ("help_builder", "false", False),
    ("help_config", "false", False),
    ("help_doc", "false", False),
    ("help_inventory", "false", False),
    ("help_playbook", "false", False),
    ("images_details", "ansible_version,python_version", ["ansible_version", "python_version"]),
    ("inventory", "/tmp/test1.yaml,/tmp/test2.yml", ["/tmp/test1.yaml", "/tmp/test2.yml"]),
    ("inventory_column", "t1,t2,t3", ["t1", "t2", "t3"]),
    ("lint_config", "/tmp/ansible-lint-config.yml", "/tmp/ansible-lint-config.yml"),
    ("lintables", "/tmp/lintables", "/tmp/lintables"),
    ("log_append", "false", False),
    ("log_file", "/tmp/app.log", "/tmp/app.log"),
    ("log_level", "info", "info"),
    ("mode", "interactive", "interactive"),
    ("osc4", "false", False),
    ("pass_environment_variable", "a,b,c", ["a", "b", "c"]),
    ("playbook", "/tmp/site.yaml", "/tmp/site.yaml"),
    ("playbook_artifact_enable", "false", False),
    ("playbook_artifact_replay", "/tmp/load.json", "/tmp/load.json"),
    ("playbook_artifact_save_as", "/tmp/save.json", "/tmp/save.json"),
    ("plugin_name", "shell", "shell"),
    ("plugin_type", "become", "become"),
    ("pull_arguments", "--tls-verify=false", ["--tls-verify=false"]),
    ("pull_policy", "never", "never"),
    ("set_environment_variable", "T1=A,T2=B,T3=C", {"T1": "A", "T2": "B", "T3": "C"}),
    ("settings_sample", "false", False),
    ("settings_schema", "json", "json"),
    ("time_zone", "Japan", "Japan"),
    ("workdir", "/tmp/", "/tmp/"),
]

SETTINGS = [
    ("ansible-navigator_empty.yml", "empty"),
    ("ansible-navigator.yml", "full"),
]
