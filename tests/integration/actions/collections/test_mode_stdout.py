"""Collection related tests run using subprocess."""

import json

import pytest

from ansible_navigator.utils.serialize import SafeLoader
from ansible_navigator.utils.serialize import yaml
from tests.defaults import FIXTURES_COLLECTION_PATH
from tests.integration._common import Parameter
from tests.integration.conftest import CliRunner


@pytest.mark.parametrize("cwd", [True, False], ids=["adjacent", "not_adjacent"])
@pytest.mark.parametrize("exec_env", [True, False], ids=["ee", "no_ee"])
@pytest.mark.parametrize("stdout_format", ["json", "yaml"], ids=["json", "yaml"])
def test_stdout_output(
    cwd: bool,
    exec_env: bool,
    stdout_format: str,
    cli_runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test the json output for collections.

    :param cwd: Whether to change the working directory.
    :param exec_env: Whether to use the execution environment.
    :param stdout_format: The output format.
    :param cli_runner: The CliRunner fixture.
    :param monkeypatch: The monkeypatch fixture.
    """
    # Either cd to the collection parent or set the env var.
    if cwd:
        cd_to = FIXTURES_COLLECTION_PATH.parent
    else:
        cd_to = None
        monkeypatch.setenv("ANSIBLE_COLLECTIONS_PATH", str(FIXTURES_COLLECTION_PATH))

    cli_runner.parameters = (
        Parameter(name="app", value="collections"),
        Parameter(name="execution_environment", value=exec_env),
        Parameter(name="format", value=stdout_format),
    )
    cli_runner.cwd = cd_to
    stdout, stderr, exit_code = cli_runner.run()

    assert not exit_code
    assert not stderr

    if stdout_format == "json":
        collection_data = json.loads(s=stdout)
    elif stdout_format == "yaml":
        collection_data = yaml.load(stream=stdout, Loader=SafeLoader)

    test_collections = [
        collection
        for collection in collection_data["collections"]
        if collection["known_as"].startswith("company_name.coll_")
    ]
    assert len(test_collections) == 2
    if exec_env:
        assert {collection["type"] for collection in test_collections} == {"bind_mount"}
