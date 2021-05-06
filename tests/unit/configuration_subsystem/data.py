""" data used by the adjacent tests

Note: Some of these are defined as dictionaries for ease but all should be frozen
before use so they are immutable within the tests
"""


def d2t(dyct):
    """turn the data dictionary into a frozenset
    so they are immutable
    """
    return tuple(dyct.items())


BASE_SHORT_CLI = """
--ce docker
--ecmd vim_base
--econ True
--ee False
--eei test_image
--lf /tmp/app.log
--ll warning
--osc4 false
--penv FOO
--penv BAR
--senv E1=V1
--senv E2=V2
"""

BASE_LONG_CLI = """
--container-engine docker
--editor-command vim_base
--editor-console True
--execution-environment False
--execution-environment-image test_image
--log-file /tmp/app.log
--log-level warning
--osc4 false
--pass-environment-variable FOO
--pass-environment-variable BAR
--set-environment-variable E1=V1
--set-environment-variable E2=V2
"""

BASE_EXPECTED = d2t(
    {
        "container_engine": "docker",
        "editor_command": "vim_base",
        "editor_console": True,
        "execution_environment": False,
        "execution_environment_image": "test_image",
        "log_file": "/tmp/app.log",
        "log_level": "warning",
        "osc4": False,
        "pass_environment_variable": ["FOO", "BAR"],
        "set_environment_variable": {"E1": "V1", "E2": "V2"},
    }
)


CLI_DATA_COLLECTIONS = [
    ("collections -m interactive", {"app": "collections", "mode": "interactive"}),
]
CLI_DATA_CONFIG = [
    ("config", {"app": "config"}),
    ("config dump", {"app": "config", "cmdline": ["dump"]}),
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
CLI_DATA_LOAD = [
    (
        "load /tmp/part.json -m interactive",
        {"app": "load", "mode": "interactive", "playbook_artifact_load": "/tmp/part.json"},
    )
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
        CLI_DATA_COLLECTIONS  # type: ignore
        + CLI_DATA_CONFIG  # type: ignore
        + CLI_DATA_DOC  # type: ignore
        + CLI_DATA_INVENTORY  # type: ignore
        + CLI_DATA_INVENTORY_COLUMNS  # type: ignore
        + CLI_DATA_LOAD  # type: ignore
        + CLI_DATA_RUN  # type: ignore
    )
    frozen = [(cmd, d2t(expected)) for cmd, expected in aggregated]
    return frozen


CLI_DATA = cli_data()

ENVVAR_DATA = [
    ("app", "config", "config"),
    ("cmdline", "--forks 15", ["--forks", "15"]),
    ("collection_doc_cache_path", "/tmp/cache.db", "/tmp/cache.db"),
    ("container_engine", "docker", "docker"),
    ("editor_command", "nano_envvar", "nano_envvar"),
    ("editor_console", "false", False),
    ("execution_environment", "false", False),
    ("execution_environment_image", "test_image", "test_image"),
    ("inventory", "/tmp/test1.yaml,/tmp/test2.yml", ["/tmp/test1.yaml", "/tmp/test2.yml"]),
    ("inventory_column", "t1,t2,t3", ["t1", "t2", "t3"]),
    ("log_file", "/tmp/app.log", "/tmp/app.log"),
    ("log_level", "info", "info"),
    ("mode", "stdout", "stdout"),
    ("osc4", "false", False),
    ("pass_environment_variable", "a,b,c", ["a", "b", "c"]),
    ("playbook", "/tmp/site.yaml", "/tmp/site.yaml"),
    ("playbook_artifact_enable", "false", False),
    ("playbook_artifact_load", "/tmp/load.json", "/tmp/load.json"),
    ("playbook_artifact_save_as", "/tmp/save.json", "/tmp/save.json"),
    ("plugin_name", "shell", "shell"),
    ("plugin_type", "become", "become"),
    ("set_environment_variable", "T1=A,T2=B,T3=C", {"T1": "A", "T2": "B", "T3": "C"}),
]

SETTINGS = [
    ("ansible-navigator_empty.yml", "empty"),
    ("ansible-navigator.yml", "full"),
]
