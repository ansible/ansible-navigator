# sanity check config in tests
# no - in name
# value exists
# if positional, check for nargs, long_override=None, short=None

from ansible_navigator.configuration import Configuration
from ansible_navigator.configuration import ApplicationConfiguration
from ansible_navigator.utils import get_conf_path

for entry in ApplicationConfiguration.entries:
    assert "-" not in entry.name
    if hasattr(entry, "cli_arguments") and entry.cli_parameters.positional:
        assert entry.short is None
        assert entry.long_override is None
        if entry.settings_file_path_override is not None:
                assert "_" not in entry.settings_file_path_override



conf_path, msgs = get_conf_path(filename="ansible-navigator", allowed_extensions=["yml", "yaml", "json"])
string = "inventory"
configuration = Configuration(application_configuration=ApplicationConfiguration, params=string.split(), settings_file_path=conf_path, )

msgs, args = configuration.configure()
print(msgs)
print(args)
