import pytest

import ansible_navigator.yaml as yaml_import


@pytest.mark.parametrize('input_val, expected', [
    ('test string', 'test string\n...\n'),
    ('test\nstring', '''|-
  test
  string
'''),
    ('\r\ntest\r\nstring\r\n', '''|-
  test
  string
'''),
    ('test\n\tstring', '''|-
  test
          string
'''),
], ids=[
    'simple string no block',
    'newline',
    'leading and trailing newlines',
    'expand tabs',
])
def test_human_dumper(input_val, expected):
    actual = yaml_import.yaml.dump(input_val, default_flow_style=False, Dumper=yaml_import.HumanDumper)
    assert actual == expected
