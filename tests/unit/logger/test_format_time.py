"""Tests for Formatter.formatTime with missing timezone data."""

from __future__ import annotations

import logging
import zoneinfo

import pytest

from ansible_navigator.logger import Formatter


@pytest.fixture(name="log_record")
def log_record_fixture() -> logging.LogRecord:
    """Create a log record for testing.

    Returns:
        A log record with a fixed timestamp
    """
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="test message",
        args=(),
        exc_info=None,
    )
    record.created = 1700000000.0
    return record


def test_utc_uses_builtin(log_record: logging.LogRecord) -> None:
    """Test that UTC bypasses zoneinfo and uses datetime.timezone.utc.

    Args:
        log_record: The log record fixture
    """
    formatter = Formatter(time_zone="UTC")
    result = formatter.formatTime(log_record)

    assert "+00:00" in result
    assert "2023-11-14" in result


def test_utc_works_without_tzdata(
    monkeypatch: pytest.MonkeyPatch,
    log_record: logging.LogRecord,
) -> None:
    """Test that UTC works even when zoneinfo.ZoneInfo would raise.

    Args:
        monkeypatch: The monkey patch fixture
        log_record: The log record fixture
    """
    monkeypatch.setattr(
        "ansible_navigator.logger.zoneinfo.ZoneInfo",
        _raise_zone_info_not_found,
    )
    formatter = Formatter(time_zone="UTC")
    result = formatter.formatTime(log_record)

    assert "+00:00" in result


def test_local_timezone(log_record: logging.LogRecord) -> None:
    """Test that local timezone works without zoneinfo.

    Args:
        log_record: The log record fixture
    """
    formatter = Formatter(time_zone="local")
    result = formatter.formatTime(log_record)

    assert "2023-11-14" in result


def test_fallback_on_missing_tzdata(
    monkeypatch: pytest.MonkeyPatch,
    log_record: logging.LogRecord,
) -> None:
    """Test that a non-UTC timezone falls back to UTC when tzdata is missing.

    Args:
        monkeypatch: The monkey patch fixture
        log_record: The log record fixture
    """
    monkeypatch.setattr(
        "ansible_navigator.logger.zoneinfo.ZoneInfo",
        _raise_zone_info_not_found,
    )
    formatter = Formatter(time_zone="America/New_York")
    result = formatter.formatTime(log_record)

    assert "+00:00" in result


def test_valid_non_utc_timezone(log_record: logging.LogRecord) -> None:
    """Test that a valid non-UTC timezone works normally.

    Args:
        log_record: The log record fixture
    """
    if "Japan" not in zoneinfo.available_timezones():
        pytest.skip("tzdata not available")

    formatter = Formatter(time_zone="Japan")
    result = formatter.formatTime(log_record)

    assert "+09:00" in result


def _raise_zone_info_not_found(key: str) -> None:
    """Simulate missing tzdata by raising ZoneInfoNotFoundError.

    Args:
        key: The timezone key

    Raises:
        zoneinfo.ZoneInfoNotFoundError: Always
    """
    raise zoneinfo.ZoneInfoNotFoundError(key)
