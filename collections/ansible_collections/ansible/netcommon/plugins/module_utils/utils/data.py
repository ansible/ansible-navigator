#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
"""
Utils functions for handle data formatting
"""
import sys
import json

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_native

try:
    HAS_LXML = True
    from lxml.etree import fromstring, XMLSyntaxError
    from lxml import etree

except ImportError:
    HAS_LXML = False
    from xml.etree.ElementTree import fromstring

    if sys.version_info < (2, 7):
        from xml.parsers.expat import ExpatError as XMLSyntaxError
    else:
        from xml.etree.ElementTree import ParseError as XMLSyntaxError


try:
    import xmltodict

    HAS_XMLTODICT = True
except ImportError:
    HAS_XMLTODICT = False


def validate_and_normalize_data(data, fmt=None):
    """
    This function validates the data for given format (fmt).
    If the fmt is None it tires to guess the data format.
    Currently support data format checks are
    1) xml
    2) json
    3) xpath
    :param data: The data which should be validated and normalised.
    :param fmt: This is an optional argument which indicated the format
    of the data. Valid values are "xml", "json" and "xpath". If the value
    is None the format of the data will be guessed and returned in the output.
    :return:
        *  If the format identified is XML it parses the xml data and returns
           a tuple of lxml.etree.Element class object and the data format type
           which is "xml" in this case.

        *  If the format identified is JSON it parses the json data and returns
           a tuple of dict object and the data format type
           which is "json" in this case.

        *  If the format identified is XPATH it parses the XPATH data and returns
           a tuple of etree.XPath class object and the data format type
           which is "xpath" in this case. For this type lxml library is required
           to be installed.
    """
    if data is None:
        return None, None

    if isinstance(data, string_types):
        data = data.strip()
        if (data.startswith("<") and data.endswith(">")) or fmt == "xml":
            try:
                result = fromstring(data)
                if fmt and fmt != "xml":
                    raise Exception(
                        "Invalid format '%s'. Expected format is 'xml' for data '%s'"
                        % (fmt, data)
                    )
                return result, "xml"
            except XMLSyntaxError as exc:
                if fmt == "xml":
                    raise Exception(
                        "'%s' XML validation failed with error '%s'"
                        % (
                            data,
                            to_native(exc, errors="surrogate_then_replace"),
                        )
                    )
                pass
            except Exception as exc:
                error = "'%s' recognized as XML but was not valid." % data
                raise Exception(
                    error + to_native(exc, errors="surrogate_then_replace")
                )
        else:
            try:
                result = json.loads(data)
                if fmt and fmt != "json":
                    raise Exception(
                        "Invalid format '%s'. Expected format is 'json' for data '%s'"
                        % (fmt, data)
                    )
                return result, "json"
            except (TypeError, json.decoder.JSONDecodeError) as exc:
                if fmt == "json":
                    raise Exception(
                        "'%s' JSON validation failed with error '%s'"
                        % (
                            data,
                            to_native(exc, errors="surrogate_then_replace"),
                        )
                    )
                pass
            except Exception as exc:
                error = "'%s' recognized as JSON but was not valid." % data
                raise Exception(
                    error + to_native(exc, errors="surrogate_then_replace")
                )

            try:
                if not HAS_LXML:
                    raise Exception(missing_required_lib("lxml"))

                result = etree.XPath(data)
                if fmt and fmt != "xpath":
                    raise Exception(
                        "Invalid format '%s'. Expected format is 'xpath' for data '%s'"
                        % (fmt, data)
                    )
                return result, "xpath"
            except etree.XPathSyntaxError as exc:
                if fmt == "xpath":
                    raise Exception(
                        "'%s' XPath validation failed with error '%s'"
                        % (
                            data,
                            to_native(exc, errors="surrogate_then_replace"),
                        )
                    )
                pass
            except Exception as exc:
                error = "'%s' recognized as Xpath but was not valid." % data
                raise Exception(
                    error + to_native(exc, errors="surrogate_then_replace")
                )

    elif isinstance(data, dict):
        if fmt and fmt != "json":
            raise Exception(
                "Invalid format '%s'. Expected format is 'json' for data '%s'"
                % (fmt, data)
            )

        try:
            result = json.loads(json.dumps(data))
            return result, "json"
        except (TypeError, json.decoder.JSONDecodeError) as exc:
            raise Exception(
                "'%s' JSON validation failed with error '%s'"
                % (data, to_native(exc, errors="surrogate_then_replace"))
            )
        except Exception as exc:
            error = "'%s' recognized as JSON but was not valid." % data
            raise Exception(
                error + to_native(exc, errors="surrogate_then_replace")
            )

    return data, "None"


def xml_to_dict(data):
    if not HAS_XMLTODICT:
        msg = (
            "xml to dict conversion requires 'xmltodict' for given data %s ."
            % data
        )
        raise Exception(msg + missing_required_lib("xmltodict"))

    try:
        return xmltodict.parse(data, dict_constructor=dict)
    except Exception as exc:
        error = (
            "'xmltodict' returned the following error when converting %s to dict. "
            % data
        )
        raise Exception(
            error + to_native(exc, errors="surrogate_then_replace")
        )


def dict_to_xml(data, full_document=False):
    """
    Converts dict object to a valid XML string
    :param data: Python dict object
    :param full_document: When set to True the will have exactly one root.
    :return: Valid XML string
    """
    if not HAS_XMLTODICT:
        msg = (
            "dict to xml conversion requires 'xmltodict' for given data %s ."
            % data
        )
        raise Exception(msg + missing_required_lib("xmltodict"))

    try:
        return xmltodict.unparse(data, full_document=full_document)
    except Exception as exc:
        error = (
            "'xmltodict' returned the following error when converting %s to xml. "
            % data
        )
        raise Exception(
            error + to_native(exc, errors="surrogate_then_replace")
        )
