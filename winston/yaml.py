""" load libyaml or pyyaml ldumper """
# pylint: disable=unused-import
import yaml

try:
    from yaml import CDumper as Dumper  # type: ignore
except ImportError:
    from yaml import Dumper  # type: ignore
