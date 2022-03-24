"""Tests for content that cannot be serialized."""
from collections import deque
from typing import Tuple

import pytest

from ansible_navigator.content_defs import ContentView
from ansible_navigator.utils.serialize import SerializationFormat
from ansible_navigator.utils.serialize import serialize


content_views = pytest.mark.parametrize(
    argnames="content_view",
    argvalues=ContentView.__members__.items(),
    ids=ContentView.__members__,
)

serialization_formats = pytest.mark.parametrize(
    argnames="serialization_format",
    argvalues=SerializationFormat.__members__.items(),
    ids=SerializationFormat.__members__,
)


@serialization_formats
@content_views
def test_custom_class(
    content_view: Tuple[str, ContentView],
    serialization_format: Tuple[str, SerializationFormat],
):
    """Ensure an error is provided when something can't be serialized.

    A typing error does not exist here because the content is Dict[str, Any].

    :param content_view: The content view
    :param serialization_format: The serialization format
    """

    class CustomClass:
        """An empty custom class."""

    content = {"foo": CustomClass()}
    serialized = serialize(
        content=content,
        content_view=content_view[1],
        serialization_format=serialization_format[1],
    )
    assert (
        f"The requested content could not be converted to {serialization_format[0]!s}."
        in serialized
    )


@serialization_formats
@content_views
def test_deque(
    content_view: Tuple[str, ContentView],
    serialization_format: Tuple[str, SerializationFormat],
):
    """Ensure an error is provided when something can't be serialized.

    A typing error exists here, because tuple is not a ``utils.serialize.ContentType``.

    :param content_view: The content view
    :param serialization_format: The serialization format
    """
    content = deque([1, 2, 3])
    serialized = serialize(
        content=content,  # type:ignore[arg-type]
        content_view=content_view[1],
        serialization_format=serialization_format[1],
    )
    assert (
        f"The requested content could not be converted to {serialization_format[0]!s}."
        in serialized
    )
