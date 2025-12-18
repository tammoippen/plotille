"""Metadata tracking for data type conversions.

When we normalize datetime values to float (timestamps), we need to remember
that they were originally datetimes so we can format them correctly later.
"""

from collections.abc import Sequence
from datetime import datetime, tzinfo
from typing import Any


class DataMetadata:
    """Tracks whether data was originally datetime and timezone info.

    Attributes:
        is_datetime: True if the original data was datetime-like
        timezone: The timezone if datetime was timezone-aware, else None
    """

    def __init__(self, is_datetime: bool, timezone: tzinfo | None = None) -> None:
        self.is_datetime = is_datetime
        self.timezone = timezone

    @classmethod
    def from_value(cls, value: Any) -> "DataMetadata":
        """Create metadata from a single value.

        Args:
            value: Any value (datetime, numeric, etc.)

        Returns:
            DataMetadata instance
        """
        if isinstance(value, datetime):
            return cls(is_datetime=True, timezone=value.tzinfo)
        # For numeric types, numpy datetime64, etc.
        # Check if it has a dtype attribute (numpy)
        if hasattr(value, "dtype") and "datetime" in str(value.dtype):
            # numpy datetime64 - these don't have timezone in the same way
            return cls(is_datetime=True, timezone=None)
        return cls(is_datetime=False, timezone=None)

    @classmethod
    def from_sequence(cls, sequence: Sequence[Any]) -> "DataMetadata":
        """Create metadata from a sequence of values.

        All values in the sequence should have the same type.

        Args:
            sequence: Sequence of values

        Returns:
            DataMetadata instance

        Raises:
            ValueError: If sequence contains mixed timezones
        """
        if len(sequence) == 0:
            # Empty sequence defaults to numeric
            return cls(is_datetime=False, timezone=None)

        # Check first element
        first_meta = cls.from_value(sequence[0])

        if not first_meta.is_datetime:
            # Numeric data - no need to check timezone
            return first_meta

        # For datetime data, verify all elements have same timezone
        timezones = set()
        for value in sequence:
            if isinstance(value, datetime):
                timezones.add(value.tzinfo)

        if len(timezones) > 1:
            raise ValueError(
                f"All datetime values must have the same timezone. "
                f"Found: {timezones}"
            )

        return cls(is_datetime=True, timezone=first_meta.timezone)

    def __repr__(self) -> str:
        if self.is_datetime:
            tz_info = f", timezone={self.timezone}" if self.timezone else ""
            return f"DataMetadata(is_datetime=True{tz_info})"
        return "DataMetadata(is_datetime=False)"
