""" load libyaml or pyyaml ldumper """
# pylint: disable=unused-import
import yaml  # noqa: F401

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore # noqa: F401

try:
    from yaml import CLoader as Loader
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import Loader  # type: ignore # noqa: F401
    from yaml import SafeLoader  # type: ignore # noqa: F401
