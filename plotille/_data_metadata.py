"""Metadata tracking for data type conversions.

When we normalize datetime values to float (timestamps), we need to remember
that they were originally datetimes so we can format them correctly later.
"""

from collections.abc import Sequence
from datetime import datetime, tzinfo
from typing import Any, final

from ._util import DataValue


@final
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
            return cls(is_datetime=False, timezone=None)

        metadatas = [cls.from_value(v) for v in sequence]
        datetime_flags = {m.is_datetime for m in metadatas}

        if len(datetime_flags) > 1:
            raise ValueError("Cannot mix numeric and datetime values.")

        if not metadatas[0].is_datetime:
            return DataMetadata(is_datetime=False, timezone=None)

        timezones = {m.timezone for m in metadatas}
        has_naive = None in timezones
        has_aware = len(timezones - {None}) > 0

        if has_naive and has_aware:
            raise ValueError("Cannot mix timezone-naive and timezone-aware datetime.")

        # Pick first encountered timezone as default
        display_timezone = metadatas[0].timezone

        return DataMetadata(is_datetime=True, timezone=display_timezone)

    def convert_for_display(
        self, value: float, tz_override: tzinfo | None = None
    ) -> DataValue:
        """Convert normalized float back to original type for display.

        Args:
            value: Normalized float value (timestamp if datetime)
            tz_override: Optional timezone override for datetime display

        Returns:
            float for numeric data, datetime for datetime data
        """
        if not self.is_datetime:
            # if not datetime, we assume we have some numeric value ... no conversion there
            return value  # type: ignore[return-value]

        display_tz = tz_override or self.timezone

        return datetime.fromtimestamp(value, tz=display_tz)
