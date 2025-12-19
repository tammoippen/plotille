# The MIT License

# Copyright (c) 2017 - 2024 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from collections.abc import Callable, Iterator, Sequence
from datetime import UTC, datetime, timedelta, tzinfo
from itertools import cycle
from typing import Any, Final, Literal, NotRequired, TypedDict

from ._canvas import Canvas
from ._cmaps import Colormap
from ._colors import ColorDefinition, ColorMode, color, rgb2byte
from ._data_metadata import DataMetadata
from ._figure_data import Heat, HeatInput, Histogram, Plot, Span, Text
from ._input_formatter import Converter, Formatter, InputFormatter
from ._util import DataValue, DataValues, mk_timedelta

# TODO documentation!!!
# TODO tests


class _ColorKwargs(TypedDict):
    fg: NotRequired[ColorDefinition]
    bg: NotRequired[ColorDefinition]
    mode: ColorMode
    no_color: NotRequired[bool]
    full_reset: NotRequired[bool]


class Figure:
    """Figure class to compose multiple plots.

    Within a Figure you can easily compose many plots, assign labels to plots
    and define the properties of the underlying Canvas. Possible properties that
    can be defined are:

        width, height: int    Define the number of characters in X / Y direction
                              which are used for plotting.
        x_limits: float       Define the X limits of the reference coordinate system,
                              that will be plottered.
        y_limits: float       Define the Y limits of the reference coordinate system,
                              that will be plottered.
        color_mode: str       Define the used color mode. See `plotille.color()`.
        with_colors: bool     Define, whether to use colors at all.
        background: multiple  Define the background color.
        x_label, y_label: str Define the X / Y axis label.
    """

    _COLOR_SEQ: Final[list[dict[ColorMode, ColorDefinition]]] = [
        {"names": "white", "rgb": (255, 255, 255), "byte": rgb2byte(255, 255, 255)},
        {"names": "red", "rgb": (255, 0, 0), "byte": rgb2byte(255, 0, 0)},
        {"names": "green", "rgb": (0, 255, 0), "byte": rgb2byte(0, 255, 0)},
        {"names": "yellow", "rgb": (255, 255, 0), "byte": rgb2byte(255, 255, 0)},
        {"names": "blue", "rgb": (0, 0, 255), "byte": rgb2byte(0, 0, 255)},
        {"names": "magenta", "rgb": (255, 0, 255), "byte": rgb2byte(255, 0, 255)},
        {"names": "cyan", "rgb": (0, 255, 255), "byte": rgb2byte(0, 255, 255)},
    ]

    def __init__(self) -> None:
        self._color_seq: Iterator[dict[ColorMode, ColorDefinition]] = iter(
            cycle(Figure._COLOR_SEQ)
        )
        self._width: int | None = None
        self._height: int | None = None
        self._x_min: float | None = None
        self._x_max: float | None = None
        self._y_min: float | None = None
        self._y_max: float | None = None
        self._color_kwargs: _ColorKwargs = {"mode": "names"}
        self._with_colors: bool = True
        self._origin: bool = True
        self.linesep: str = os.linesep
        self.background: ColorDefinition = None
        self.x_label: str = "X"
        self.y_label: str = "Y"
        # min, max -> value
        self.y_ticks_fkt: Callable[[float | datetime, float | datetime], float | datetime | str] | None = None
        self.x_ticks_fkt: Callable[[float | datetime, float | datetime], float | datetime | str] | None = None
        self._plots: list[Plot | Histogram] = []
        self._texts: list[Text] = []
        self._spans: list[Span] = []
        self._heats: list[Heat] = []
        self._in_fmt: InputFormatter = InputFormatter()

        # Metadata for axis display formatting
        self._x_display_metadata: DataMetadata | None = None
        self._y_display_metadata: DataMetadata | None = None
        self._x_display_timezone_override: tzinfo | None = None
        self._y_display_timezone_override: tzinfo | None = None

    @property
    def width(self) -> int:
        if self._width is not None:
            return self._width
        return 80

    @width.setter
    def width(self, value: int) -> None:
        if not (isinstance(value, int) and value > 0):
            raise ValueError(f"Invalid width: {value}")
        self._width = value

    @property
    def height(self) -> int:
        if self._height is not None:
            return self._height
        return 40

    @height.setter
    def height(self, value: int) -> None:
        if not (isinstance(value, int) and value > 0):
            raise ValueError(f"Invalid height: {value}")
        self._height = value

    @property
    def color_mode(self) -> ColorMode:
        return self._color_kwargs["mode"]

    @color_mode.setter
    def color_mode(self, value: ColorMode) -> None:
        if value not in ("names", "byte", "rgb"):
            raise ValueError("Only supports: names, byte, rgb!")
        if self._plots != []:
            raise RuntimeError("Change color mode only, when no plots are prepared.")
        self._color_kwargs["mode"] = value

    @property
    def color_full_reset(self) -> bool:
        return self._color_kwargs.get("full_reset", True)

    @color_full_reset.setter
    def color_full_reset(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("Only supports bool.")
        self._color_kwargs["full_reset"] = value

    @property
    def with_colors(self) -> bool:
        """Whether to plot with or without color."""
        return self._with_colors

    @with_colors.setter
    def with_colors(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f'Only bool allowed: "{value}"')
        self._with_colors = value

    @property
    def origin(self) -> bool:
        """Show or not show the origin in the plot."""
        return self._origin

    @origin.setter
    def origin(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Invalid origin: {value}")
        self._origin = value

    def _aggregate_metadata(self, is_height: bool) -> DataMetadata | None:
        """Aggregate metadata from all plots for one axis.

        Determines whether the axis should display as numeric or datetime,
        and validates that all plots have compatible types.

        Args:
            is_height: True for Y-axis, False for X-axis

        Returns:
            DataMetadata for the axis (with display timezone), or None if no plots

        Raises:
            ValueError: If plots have incompatible types on same axis
        """
        # Collect metadata from all plots
        metadatas = []
        for p in self._plots + self._texts:
            if is_height:
                metadatas.append(p.Y_metadata)
            else:
                metadatas.append(p.X_metadata)

        if not metadatas:
            # No plots yet, no metadata to aggregate
            return None

        # Check if all numeric or all datetime (no mixing)
        datetime_flags = {m.is_datetime for m in metadatas}
        if len(datetime_flags) > 1:
            axis_name = "Y" if is_height else "X"
            raise ValueError(
                f"Cannot mix numeric and datetime values on {axis_name}-axis. "
                f"All plots on an axis must use the same data type."
            )

        # All numeric case
        if not metadatas[0].is_datetime:
            return DataMetadata(is_datetime=False, timezone=None)

        # All datetime - validate timezone consistency
        timezones = {m.timezone for m in metadatas}
        has_naive = None in timezones
        has_aware = len(timezones - {None}) > 0

        # Cannot mix naive and aware datetime
        if has_naive and has_aware:
            axis_name = "Y" if is_height else "X"
            raise ValueError(
                f"Cannot mix timezone-naive and timezone-aware datetime on {axis_name}-axis. "
                f"Either all datetimes must have timezones or none must have timezones. "
                f"Found: {timezones}"
            )

        # Pick first encountered timezone as default
        # (User can override with set_x_display_timezone/set_y_display_timezone)
        display_timezone = metadatas[0].timezone

        return DataMetadata(is_datetime=True, timezone=display_timezone)

    def set_x_display_timezone(self, tz: tzinfo | None) -> None:
        """Set display timezone for X-axis labels.

        Use this when you have datetime data with multiple timezones and want
        to display the axis in a specific timezone.

        Args:
            tz: Target timezone (e.g., ZoneInfo("America/New_York"), timezone.utc)
                or None for naive datetime display

        Example:
            from zoneinfo import ZoneInfo
            fig.set_x_display_timezone(ZoneInfo("America/New_York"))
        """
        self._x_display_timezone_override = tz

    def set_y_display_timezone(self, tz: tzinfo | None) -> None:
        """Set display timezone for Y-axis labels.

        Use this when you have datetime data with multiple timezones and want
        to display the axis in a specific timezone.

        Args:
            tz: Target timezone (e.g., ZoneInfo("America/New_York"), timezone.utc)
                or None for naive datetime display

        Example:
            from zoneinfo import ZoneInfo
            fig.set_y_display_timezone(ZoneInfo("UTC"))
        """
        self._y_display_timezone_override = tz

    def _convert_for_display(
        self,
        value: float,
        metadata: DataMetadata,
        tz_override: tzinfo | None = None,
    ) -> float | datetime:
        """Convert normalized float back to original type for display.

        Args:
            value: Normalized float value (timestamp if datetime)
            metadata: Metadata indicating original type
            tz_override: Optional timezone override for datetime display

        Returns:
            float for numeric data, datetime for datetime data
        """
        if not metadata.is_datetime:
            return value

        # Use override if provided, otherwise use metadata timezone
        display_tz = tz_override if tz_override is not None else metadata.timezone

        return datetime.fromtimestamp(value, tz=display_tz)

    def register_label_formatter(self, type_: type[Any], formatter: Formatter) -> None:
        """Register a formatter for labels of a certain type.

        See `plotille._input_formatter` for examples.

        Parameters
        ----------
        type_
            A python type, that can be used for isinstance tests.
        formatter: (val: type_, chars: int, delta, left: bool = False) -> str
            Function that formats `val` into a string.
            chars: int => number of chars you should fill
            delta      => the difference between the smallest and largest X/Y value
            left: bool => align left or right.
        """
        self._in_fmt.register_formatter(type_, formatter)

    def register_float_converter(self, type_: type[Any], converter: Converter) -> None:
        """Register a converter from some type_ to float.

        See `plotille._input_formatter` for examples.

        Parameters
        ----------
        type_
            A python type, that can be used for isinstance tests.
        formatter: (val: type_) -> float
            Function that formats `val` into a float.
        """
        self._in_fmt.register_converter(type_, converter)

    def x_limits(self) -> tuple[float, float]:
        """Get the X-axis limits as normalized floats."""
        return self._limits(self._x_min, self._x_max, False)

    def set_x_limits(
        self, min_: DataValue | None = None, max_: DataValue | None = None
    ) -> None:
        """Set min and max X values for displaying.

        Args:
            min_: Minimum X value (can be datetime or numeric)
            max_: Maximum X value (can be datetime or numeric)

        Note: Values will be normalized to float internally.
        """
        values = [v for v in [min_, max_] if v is not None]
        if values:
            self._x_display_metadata = DataMetadata.from_sequence(values)

        min_float = self._in_fmt.convert(min_) if min_ is not None else None
        max_float = self._in_fmt.convert(max_) if max_ is not None else None

        self._x_min, self._x_max = self._set_limits(
            self._x_min, self._x_max, min_float, max_float
        )

    def y_limits(self) -> tuple[float, float]:
        """Get the Y-axis limits as normalized floats."""
        return self._limits(self._y_min, self._y_max, True)

    def set_y_limits(
        self, min_: DataValue | None = None, max_: DataValue | None = None
    ) -> None:
        """Set min and max Y values for displaying.

        Args:
            min_: Minimum Y value (can be datetime or numeric)
            max_: Maximum Y value (can be datetime or numeric)

        Note: Values will be normalized to float internally.
        """
        values = [v for v in [min_, max_] if v is not None]
        if values:
            self._y_display_metadata = DataMetadata.from_sequence(values)

        min_float = self._in_fmt.convert(min_) if min_ is not None else None
        max_float = self._in_fmt.convert(max_) if max_ is not None else None

        self._y_min, self._y_max = self._set_limits(
            self._y_min, self._y_max, min_float, max_float
        )

    def _set_limits(
        self,
        init_min: float | None,
        init_max: float | None,
        min_: float | None = None,
        max_: float | None = None,
    ) -> tuple[float | None, float | None]:
        """Set limits for an axis.

        All parameters are already normalized to float.

        Args:
            init_min: Current minimum value
            init_max: Current maximum value
            min_: New minimum value (if setting)
            max_: New maximum value (if setting)

        Returns:
            (min, max) tuple of floats or Nones
        """
        values = list(filter(lambda v: v is not None, [init_min, init_max, min_, max_]))
        if not values:
            return None, None

        # All values are floats now, no datetime check needed

        if min_ is not None and max_ is not None:
            if min_ >= max_:
                raise ValueError("min_ is larger or equal than max_.")
            init_min = min_
            init_max = max_
        elif min_ is not None:
            if init_max is not None and min_ >= init_max:
                raise ValueError("Previous max is smaller or equal to new min_.")
            init_min = min_
        elif max_ is not None:
            if init_min is not None and init_min >= max_:
                raise ValueError("Previous min is larger or equal to new max_.")
            init_max = max_
        else:
            init_min = None
            init_max = None

        return init_min, init_max

    def _limits(
        self, low_set: float | None, high_set: float | None, is_height: bool
    ) -> tuple[float, float]:
        """Calculate the limits for an axis.

        Aggregates metadata from all plots and works with normalized float values.

        Args:
            low_set: User-specified minimum value (already converted to float)
            high_set: User-specified maximum value (already converted to float)
            is_height: True for Y-axis, False for X-axis

        Returns:
            (min, max) as floats
        """
        # Aggregate and store metadata for this axis
        metadata = self._aggregate_metadata(is_height)
        if metadata is not None:
            if is_height:
                self._y_display_metadata = metadata
            else:
                self._x_display_metadata = metadata

        if low_set is not None and high_set is not None:
            return low_set, high_set

        # Get limits from normalized data (all floats now)
        low, high = None, None
        for p in self._plots + self._texts:
            if is_height:
                _min, _max = _limit(p.height_vals())
            else:
                _min, _max = _limit(p.width_vals())
            if low is None or high is None:
                low = _min
                high = _max
            else:
                low = min(_min, low)
                high = max(_max, high)

        # Calculate final limits
        result = _choose(low, high, low_set, high_set)
        return result

    def _y_axis(self, ymin: float, ymax: float, label: str = "Y") -> list[str]:
        """Generate Y-axis labels.

        Uses stored metadata to convert float values back to display format
        (datetime or numeric).

        Args:
            ymin: Minimum Y value (as normalized float/timestamp)
            ymax: Maximum Y value (as normalized float/timestamp)
            label: Axis label

        Returns:
            List of formatted axis labels
        """
        if self._y_display_metadata is None:
            self._y_display_metadata = DataMetadata(is_datetime=False, timezone=None)

        delta = abs(ymax - ymin)
        y_delta = delta / self.height

        # Convert delta for display formatting
        delta_display = timedelta(seconds=delta) if self._y_display_metadata.is_datetime else delta

        res = []
        for i in range(self.height):
            value_float = i * y_delta + ymin

            # Convert to display type using metadata
            value_display = self._convert_for_display(
                value_float,
                self._y_display_metadata,
                self._y_display_timezone_override
            )

            if self.y_ticks_fkt:
                value_display = self.y_ticks_fkt(value_display, value_display)  # type: ignore[assignment]

            res += [self._in_fmt.fmt(value_display, delta_display, chars=10) + " | "]

        # add max separately
        value_float = self.height * y_delta + ymin
        value_display = self._convert_for_display(
            value_float,
            self._y_display_metadata,
            self._y_display_timezone_override
        )

        if self.y_ticks_fkt:
            value_display = self.y_ticks_fkt(value_display, value_display)  # type: ignore[assignment]

        res += [self._in_fmt.fmt(value_display, delta_display, chars=10) + " |"]

        ylbl = f"({label})"
        ylbl_left = (10 - len(ylbl)) // 2
        ylbl_right = ylbl_left + len(ylbl) % 2

        res += [" " * (ylbl_left) + ylbl + " " * (ylbl_right) + " ^"]
        return list(reversed(res))

    def _x_axis(
        self, xmin: float, xmax: float, label: str = "X", with_y_axis: bool = False
    ) -> list[str]:
        """Generate X-axis labels.

        Uses stored metadata to convert float values back to display format
        (datetime or numeric).

        Args:
            xmin: Minimum X value (as normalized float/timestamp)
            xmax: Maximum X value (as normalized float/timestamp)
            label: Axis label
            with_y_axis: Whether to add spacing for Y-axis labels

        Returns:
            List of formatted axis labels
        """
        if self._x_display_metadata is None:
            self._x_display_metadata = DataMetadata(is_datetime=False, timezone=None)

        delta = abs(xmax - xmin)
        x_delta = delta / self.width

        # Convert delta for display formatting
        delta_display = timedelta(seconds=delta) if self._x_display_metadata.is_datetime else delta

        starts = ["", ""]
        if with_y_axis:
            starts = ["-" * 11 + "|-", " " * 11 + "| "]
        res = []

        res += [
            starts[0]
            + "|---------" * (self.width // 10)
            + "|"
            + "-" * (self.width % 10)
            + "-> ("
            + label
            + ")",
        ]
        bottom = []

        for i in range(self.width // 10 + 1):
            value_float = i * 10 * x_delta + xmin

            # Convert to display type using metadata
            value_display = self._convert_for_display(
                value_float,
                self._x_display_metadata,
                self._x_display_timezone_override
            )

            if self.x_ticks_fkt:
                value_display = self.x_ticks_fkt(value_display, value_display)  # type: ignore[assignment]

            bottom += [self._in_fmt.fmt(value_display, delta_display, left=True, chars=9)]

        res += [starts[1] + " ".join(bottom)]
        return res

    def clear(self) -> None:
        """Remove all plots, texts and spans from the figure."""
        self._plots = []
        self._texts = []
        self._spans = []
        self._heats = []

    def plot(
        self,
        X: DataValues,
        Y: DataValues,
        lc: ColorDefinition = None,
        interp: Literal["linear"] | None = "linear",
        label: str | None = None,
        marker: str | None = None,
    ) -> None:
        """Create plot with X , Y values.

        Parameters:
            X: List[float]     X values.
            Y: List[float]     Y values. X and Y must have the same number of entries.
            lc: multiple       The line color.
            interp: str        The interpolation method. (None or 'linear').
            label: str         The label for the legend.
            marker: str        Instead of braille dots set a marker char.
        """
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Plot(X, Y, lc, interp, label, marker, self._in_fmt)]

    def scatter(
        self,
        X: DataValues,
        Y: DataValues,
        lc: ColorDefinition = None,
        label: str | None = None,
        marker: str | None = None,
    ) -> None:
        """Create a scatter plot with X , Y values

        Parameters:
            X: List[float]     X values.
            Y: List[float]     Y values. X and Y must have the same number of entries.
            lc: multiple       The line color.
            label: str         The label for the legend.
            marker: str        Instead of braille dots set a marker char.
        """
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Plot(X, Y, lc, None, label, marker, self._in_fmt)]

    def histogram(
        self, X: DataValues, bins: int = 160, lc: ColorDefinition = None
    ) -> None:
        """Compute and plot the histogram over X.

        Parameters:
            X: List[float]     X values.
            bins: int          The number of bins to put X entries in (columns).
            lc: multiple       The line color.
        """
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Histogram(X, bins, lc)]

    def text(
        self,
        X: DataValues,
        Y: DataValues,
        texts: Sequence[str],
        lc: ColorDefinition = None,
    ) -> None:
        """Plot texts at coordinates X, Y.

        Always print the first character of a text at its
        x, y coordinate and continue to the right. Character
        extending the canvas are cut.

        Parameters:
            X: List[float]     X values.
            Y: List[float]     Y values.
            texts: List[str]   Texts to print. X, Y and texts must have the same
                               number of entries.
            lc: multiple       The (text) line color.
        """
        if len(X) > 0:
            self._texts += [Text(X, Y, texts, lc, self._in_fmt)]

    def axvline(
        self, x: float, ymin: float = 0, ymax: float = 1, lc: ColorDefinition = None
    ) -> None:
        """Plot a vertical line at x.

        Parameters:
            x: float       x-coordinate of the vertical line.
                           In the range [0, 1]
            ymin: float    Minimum y-coordinate of the vertical line.
                           In the range [0, 1]
            ymax: float    Maximum y-coordinate of the vertical line.
                           In the range [0, 1]
            lc: multiple   The line color.
        """
        self._spans.append(Span(x, x, ymin, ymax, lc))

    def axvspan(
        self,
        xmin: float,
        xmax: float,
        ymin: float = 0,
        ymax: float = 1,
        lc: ColorDefinition = None,
    ) -> None:
        """Plot a vertical rectangle from (xmin,ymin) to (xmax, ymax).

        Parameters:
            xmin: float    Minimum x-coordinate of the rectangle.
                           In the range [0, 1]
            xmax: float    Maximum x-coordinate of the rectangle.
                           In the range [0, 1]
            ymin: float    Minimum y-coordinate of the rectangle.
                           In the range [0, 1]
            ymax: float    Maximum y-coordinate of the rectangle.
                           In the range [0, 1]
            lc: multiple   The line color.
        """
        self._spans.append(Span(xmin, xmax, ymin, ymax, lc))

    def axhline(
        self, y: float, xmin: float = 0, xmax: float = 1, lc: ColorDefinition = None
    ) -> None:
        """Plot a horizontal line at y.

        Parameters:
            y: float       y-coordinate of the horizontal line.
                           In the range [0, 1]
            x_min: float   Minimum x-coordinate of the vertical line.
                           In the range [0, 1]
            x_max: float   Maximum x-coordinate of the vertical line.
                           In the range [0, 1]
            lc: multiple   The line color.
        """
        self._spans.append(Span(xmin, xmax, y, y, lc))

    def axhspan(
        self,
        ymin: float,
        ymax: float,
        xmin: float = 0,
        xmax: float = 1,
        lc: ColorDefinition = None,
    ) -> None:
        """Plot a horizontal rectangle from (xmin,ymin) to (xmax, ymax).

        Parameters:
            ymin: float    Minimum y-coordinate of the rectangle.
                           In the range [0, 1]
            ymax: float    Maximum y-coordinate of the rectangle.
                           In the range [0, 1]
            xmin: float    Minimum x-coordinate of the rectangle.
                           In the range [0, 1]
            xmax: float    Maximum x-coordinate of the rectangle.
                           In the range [0, 1]
            lc: multiple   The line color.
        """
        self._spans.append(Span(xmin, xmax, ymin, ymax, lc))

    def imgshow(self, X: HeatInput, cmap: str | Colormap | None = None) -> None:
        """Display data as an image, i.e., on a 2D regular raster.

        Parameters:
            X: array-like
                The image data. Supported array shapes are:
                - (M, N): an image with scalar data. The values are mapped
                        to colors using a colormap. The values have to be in
                        the 0-1 (float) range. Out of range, invalid type and
                        None values are handled by the cmap.
                - (M, N, 3): an image with RGB values (0-1 float or 0-255 int).

                The first two dimensions (M, N) define the rows and columns of the
                image.

            cmap: cmapstr or Colormap
                The Colormap instance or registered colormap name used
                to map scalar data to colors. This parameter is ignored
                for RGB data.
        """
        if len(X) > 0:
            self._heats += [Heat(X, cmap)]

    def show(self, legend: bool = False) -> str:
        """Compute the plot.

        Parameters:
            legend: bool   Add the legend? default: False

        Returns:
            plot: str
        """
        xmin, xmax = self.x_limits()
        ymin, ymax = self.y_limits()
        if self._plots and all(isinstance(p, Histogram) for p in self._plots):
            ymin = 0.0

        if self._heats and self._width is None and self._height is None:
            self.height = len(self._heats[0].X)
            self.width = len(self._heats[0].X[0])

        # create canvas
        canvas = Canvas(
            self.width,
            self.height,
            xmin,
            ymin,
            xmax,
            ymax,
            self.background,
            **self._color_kwargs,
        )

        for s in self._spans:
            s.write(canvas, self.with_colors)

        plot_origin = False
        for p in self._plots:
            p.write(canvas, self.with_colors, self._in_fmt)
            if isinstance(p, Plot):
                plot_origin = True

        for t in self._texts:
            t.write(canvas, self.with_colors, self._in_fmt)

        for h in self._heats:
            h.write(canvas)

        if self.origin and plot_origin:
            # print X / Y origin axis
            canvas.line(xmin, 0.0, xmax, 0.0)
            canvas.line(0.0, ymin, 0.0, ymax)

        res = canvas.plot(linesep=self.linesep)

        # add y axis
        yaxis = self._y_axis(ymin, ymax, label=self.y_label)
        res = (
            yaxis[0]
            + self.linesep  # up arrow
            + yaxis[1]
            + self.linesep  # maximum
            + self.linesep.join(
                lbl + line
                for lbl, line in zip(yaxis[2:], res.split(self.linesep), strict=True)
            )
        )

        # add x axis
        xaxis = self._x_axis(xmin, xmax, label=self.x_label, with_y_axis=True)
        res = (
            res
            + self.linesep  # plot
            + self.linesep.join(xaxis)
        )

        if legend:
            res += f"{self.linesep}{self.linesep}Legend:{self.linesep}-------{self.linesep}"
            lines = []
            for i, p in enumerate(self._plots):
                if isinstance(p, Plot):
                    lbl = p.label or f"Label {i}"
                    marker = p.marker or ""
                    lines += [
                        color(
                            f"⠤{marker}⠤ {lbl}",
                            fg=p.lc,
                            mode=self.color_mode,
                            no_color=not self.with_colors,
                        ),
                    ]
            res += self.linesep.join(lines)
        return res


def _limit(values: Sequence[float]) -> tuple[float, float]:
    """Find min and max of normalized float values.

    Args:
        values: Sequence of already-normalized float values

    Returns:
        (min, max) as floats
    """
    min_: float = 0.0
    max_: float = 1.0
    if len(values) > 0:
        min_ = min(values)
        max_ = max(values)

    return min_, max_


def _diff(low: float, high: float) -> float:
    # assert type(low) is type(high)
    if low == high:
        if low == 0:
            return 0.5
        else:
            return abs(low * 0.1)
    else:
        delta = abs(high - low)
        return delta * 0.1


def _default(low_set: float | None, high_set: float | None) -> tuple[float, float]:
    if low_set is None and high_set is None:
        return 0.0, 1.0  # defaults

    if low_set is None and high_set is not None:
        if high_set <= 0:
            return high_set - 1, high_set
        else:
            return 0.0, high_set

    if low_set is not None and high_set is None:
        if low_set >= 1:
            return low_set, low_set + 1
        else:
            return low_set, 1.0

    # Should never get here! => checked in function before
    raise ValueError("Unexpected inputs!")


def _choose(
    low: float | None,
    high: float | None,
    low_set: float | None,
    high_set: float | None,
) -> tuple[float, float]:
    if low is None or high is None:
        # either all are set or none
        assert low is None
        assert high is None
        return _default(low_set, high_set)

    else:  # some data
        if low_set is None and high_set is None:
            # no restrictions from user, use low & high
            diff = _diff(low, high)
            return low - diff, high + diff

        if low_set is None and high_set is not None:
            # user sets high end
            if high_set < low:
                # high is smaller than lowest value
                return high_set - 1, high_set

            diff = _diff(low, high_set)
            return low - diff, high_set

        if low_set is not None and high_set is None:
            # user sets low end
            if low_set > high:
                # low is larger than highest value
                return low_set, low_set + 1

            diff = _diff(low_set, high)
            return low_set, high + diff

        # Should never get here! => checked in function before
        raise ValueError("Unexpected inputs!")
