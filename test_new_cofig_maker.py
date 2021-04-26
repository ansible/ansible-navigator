

from collections import Counter

from ansible_navigator.configuration import Configuration
from ansible_navigator.configuration import ApplicationConfiguration
from ansible_navigator.utils import get_conf_path

# No - in name
for entry in ApplicationConfiguration.entries:
    assert "-" not in entry.name

# No cli parameters if positional
for entry in ApplicationConfiguration.entries:
    if hasattr(entry, "cli_arguments") and entry.cli_parameters.positional:
        assert entry.short is None
        assert entry.long_override is None

# No _ in settings file
for entry in ApplicationConfiguration.entries:
    if entry.settings_file_path_override is not None:
        assert "_" not in entry.settings_file_path_override


# No duplicate names
values = Counter([entry.name for entry in ApplicationConfiguration.entries])
assert not any(k for (k, v) in values.items() if v > 1)


# No duplicate shorts
values = Counter(
    [
        entry.cli_parameters.short
        for entry in ApplicationConfiguration.entries
        if entry.cli_parameters is not None
    ]
)
assert not any(k for (k, v) in values.items() if v > 1)


conf_path, msgs = get_conf_path(
    filename="ansible-navigator", allowed_extensions=["yml", "yaml", "json"]
)
string = "inventory --senv FOO=BAR"

application_configuration = ApplicationConfiguration

configuration = Configuration(
    application_configuration=application_configuration,
    params=string.split(),
    settings_file_path=conf_path,
    save_as_intitial=True,
)
msgs = configuration.configure()


string = "doc --pt become"

configuration = Configuration(
    application_configuration=application_configuration,
    params=string.split(),
    settings_file_path=conf_path,
    apply_previous_cli=True,
)
msgs = configuration.configure()


print(msgs)
print(application_configuration)
