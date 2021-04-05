import ansible_navigator.yaml as yaml_import


def test_check_yaml_imports():
    assert yaml_import.yaml is not None
    assert yaml_import.Dumper is not None
    assert yaml_import.Loader is not None
