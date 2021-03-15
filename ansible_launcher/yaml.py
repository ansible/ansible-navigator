""" load libyaml or pyyaml ldumper """
# pylint: disable=unused-import
import yaml

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # type: ignore
