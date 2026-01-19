"""Tests for data type metadata tracking."""

from datetime import datetime, timedelta, timezone

import pytest

from plotille._data_metadata import DataMetadata


def test_metadata_for_numeric_data():
    """Numeric data should be marked as non-datetime."""
    meta = DataMetadata.from_value(42)
    assert not meta.is_datetime
    assert meta.timezone is None


def test_metadata_for_datetime_data():
    """Datetime data should be marked as datetime."""
    dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    meta = DataMetadata.from_value(dt)
    assert meta.is_datetime
    assert meta.timezone is timezone.utc


def test_metadata_for_naive_datetime():
    """Naive datetime (no timezone) should have None timezone."""
    dt = datetime(2024, 1, 1, 12, 0, 0)
    meta = DataMetadata.from_value(dt)
    assert meta.is_datetime
    assert meta.timezone is None


def test_metadata_for_float():
    """Float data should be marked as non-datetime."""
    meta = DataMetadata.from_value(3.14)
    assert not meta.is_datetime
    assert meta.timezone is None


def test_metadata_from_sequence_numeric():
    """Should detect numeric sequence."""
    meta = DataMetadata.from_sequence([1, 2, 3, 4, 5])
    assert not meta.is_datetime
    assert meta.timezone is None


def test_metadata_from_sequence_datetime():
    """Should detect datetime sequence."""
    dts = [
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2024, 1, 2, tzinfo=timezone.utc),
    ]
    meta = DataMetadata.from_sequence(dts)
    assert meta.is_datetime
    assert meta.timezone is timezone.utc


def test_metadata_from_empty_sequence():
    """Empty sequence should default to numeric."""
    meta = DataMetadata.from_sequence([])
    assert not meta.is_datetime
    assert meta.timezone is None


def test_metadata_mixed_aware_native_timezones_raises():
    """Mixed timezones with aware and native should raise an error."""
    dts = [
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2024, 1, 2),  # naive
    ]
    with pytest.raises(ValueError, match="timezone"):
        DataMetadata.from_sequence(dts)


def test_metadata_mixed_timezones_raises():
    """Mixed timezones should raise an error."""
    dts = [
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2024, 1, 2, tzinfo=timezone(timedelta(hours=-7))),
    ]
    meta = DataMetadata.from_sequence(dts)
    assert meta.is_datetime
    assert meta.timezone == timezone.utc
