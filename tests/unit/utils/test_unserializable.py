"""Tests for content that cannot be serialized."""

from __future__ import annotations

from collections import deque

import pytest

from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.utils.serialize import serialize
from tests.defaults import id_func


content_views = pytest.mark.parametrize(
    argnames="content_view",
    argvalues=ContentView.__members__.items(),
    ids=id_func,
)

serialization_formats = pytest.mark.parametrize(
    argnames="serialization_format",
    argvalues=SerializationFormat.__members__.items(),
    ids=id_func,
)


@serialization_formats
@content_views
def test_custom_class(
    content_view: tuple[str, ContentView],
    serialization_format: tuple[str, SerializationFormat],
) -> None:
    """Ensure an error is provided when something can't be serialized.

    A typing error does not exist here because the content is Dict[str, Any].

    Args:
        content_view: The content view
        serialization_format: The serialization format
    """

    class CustomClass:
        """An empty custom class."""

    content = {"foo": CustomClass()}
    serialized = str(
        serialize(
            content=content,
            content_view=content_view[1],
            serialization_format=serialization_format[1],
        ),
    )
    assert (
        f"The requested content could not be converted to {serialization_format[0]!s}."
        in serialized
    )


@serialization_formats
@content_views
def test_deque(
    content_view: tuple[str, ContentView],
    serialization_format: tuple[str, SerializationFormat],
) -> None:
    """Ensure an error is provided when something can't be serialized.

    A typing error exists here, because tuple is not a ``utils.serialize.ContentType``.

    Args:
        content_view: The content view
        serialization_format: The serialization format
    """
    content = deque([1, 2, 3])
    serialized = str(
        serialize(
            content=content,  # type:ignore[arg-type]
            content_view=content_view[1],
            serialization_format=serialization_format[1],
        ),
    )
    assert (
        f"The requested content could not be converted to {serialization_format[0]!s}."
        in serialized
    )
