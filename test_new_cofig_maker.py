# sanity check config in tests
# no - in name
# long = name
# value exists

from ansible_navigator.config_maker import ConfigurationMaker

from ansible_navigator.utils import get_conf_path

conf_path, msgs = get_conf_path(filename="ansible-navigator", allowed_extensions=["yml", "yaml", "json"])
string = "doc"
configuration_maker = ConfigurationMaker(settings_file_path=conf_path, params=string.split())

msgs, args = configuration_maker.run()
print(msgs)
print(args)
