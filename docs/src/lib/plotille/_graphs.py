# The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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
from collections.abc import Sequence
from datetime import timedelta
from math import log
from typing import Literal

from ._colors import ColorDefinition, ColorMode, color
from ._data_metadata import DataMetadata
from ._figure import Figure
from ._input_formatter import InputFormatter
from ._util import DataValue, DataValues
from ._util import hist as compute_hist


def hist_aggregated(
    counts: list[int],
    bins: Sequence[float],
    width: int = 80,
    log_scale: bool = False,
    linesep: str = os.linesep,
    lc: ColorDefinition = None,
    bg: ColorDefinition = None,
    color_mode: ColorMode = "names",
    meta: DataMetadata | None = None,
) -> str:
    """
    Create histogram for aggregated data.

    Parameters:
        counts: List[int]         Counts for each bucket.
        bins: List[float]         Limits for the bins for the provided counts: limits for
                                  bin `i` are `[bins[i], bins[i+1])`.
                                  Hence, `len(bins) == len(counts) + 1`.
        width: int                The number of characters for the width (columns).
        log_scale: bool           Scale the histogram with `log` function.
        linesep: str              The requested line separator. default: os.linesep
        lc: ColorDefinition       Give the line color.
        bg: ColorDefinition       Give the background color.
        color_mode: ColorMode     Specify color input mode; 'names' (default), 'byte' or
                                  'rgb' see plotille.color.__docs__
        meta: DataMetadata | None For conversion of datetime values.
    Returns:
        str: histogram over `X` from left to right.
    """

    def _scale(a: int) -> float | int:
        if log_scale and a > 0:
            return log(a)
        return a

    if meta is None:
        meta = DataMetadata(is_datetime=False)

    h = counts
    b = bins

    ipf = InputFormatter()
    h_max = _scale(max(h)) or 1
    max_ = b[-1]
    min_ = b[0]
    # bins are always normalized to float
    delta = max_ - min_
    delta_display = timedelta(seconds=delta) if meta.is_datetime else delta

    bins_count = len(h)

    canvas = ["        bucket       | {} {}".format("_" * width, "Total Counts")]
    lasts = ["", "⠂", "⠆", "⠇", "⡇", "⡗", "⡷", "⡿"]
    for i in range(bins_count):
        height = int(width * 8 * _scale(h[i]) / h_max)
        canvas += [
            "[{}, {}) | {} {}".format(
                ipf.fmt(
                    meta.convert_for_display(b[i]),
                    delta=delta_display,
                    chars=8,
                    left=True,
                ),
                ipf.fmt(
                    meta.convert_for_display(b[i + 1]),
                    delta=delta_display,
                    chars=8,
                    left=False,
                ),
                color(
                    "⣿" * (height // 8) + lasts[height % 8],
                    fg=lc,
                    bg=bg,
                    mode=color_mode,
                )
                + color(
                    "\u2800" * (width - (height // 8) + int(height % 8 == 0)),
                    bg=bg,
                    mode=color_mode,
                ),
                h[i],
            )
        ]
    canvas += ["‾" * (2 * 8 + 2 + 3 + width + 12)]
    return linesep.join(canvas)


def hist(
    X: DataValues,
    bins: int = 40,
    width: int = 80,
    log_scale: bool = False,
    linesep: str = os.linesep,
    lc: ColorDefinition = None,
    bg: ColorDefinition = None,
    color_mode: ColorMode = "names",
) -> str:
    """Create histogram over `X` from left to right

    The values on the left are the center of the bucket, i.e. `(bin[i] + bin[i+1]) / 2`.
    The values on the right are the total counts of this bucket.

    Parameters:
        X: List[float]       The items to count over.
        bins: int            The number of bins to put X entries in (rows).
        width: int           The number of characters for the width (columns).
        log_scale: bool      Scale the histogram with `log` function.
        linesep: str         The requested line separator. default: os.linesep
        lc: ColorDefinition         Give the line color.
        bg: ColorDefinition         Give the background color.
        color_mode: ColorMode      Specify color input mode; 'names' (default), 'byte' or
                             'rgb' see plotille.color.__docs__

    Returns:
        str: histogram over `X` from left to right.
    """
    # Normalize data to float before computing histogram
    formatter = InputFormatter()
    metadata = DataMetadata.from_sequence(X)
    X_floats = [formatter.convert(x) for x in X]

    counts, bins_list = compute_hist(X_floats, bins)

    # bins_list are floats, use metadata for display
    return hist_aggregated(
        counts=counts,
        bins=bins_list,
        width=width,
        log_scale=log_scale,
        linesep=linesep,
        lc=lc,
        bg=bg,
        color_mode=color_mode,
        meta=metadata,
    )


def histogram(
    X: DataValues,
    bins: int = 160,
    width: int = 80,
    height: int = 40,
    X_label: str = "X",
    Y_label: str = "Counts",
    linesep: str = os.linesep,
    x_min: DataValue | None = None,
    x_max: DataValue | None = None,
    y_min: DataValue | None = None,
    y_max: DataValue | None = None,
    lc: ColorDefinition = None,
    bg: ColorDefinition = None,
    color_mode: ColorMode = "names",
) -> str:
    """Create histogram over `X`

    In contrast to `hist`, this is the more `usual` histogram from bottom
    to up. The X-axis represents the values in `X` and the Y-axis is the
    corresponding frequency.

    Parameters:
        X: List[float]       The items to count over.
        bins: int            The number of bins to put X entries in (columns).
        height: int          The number of characters for the height (rows).
        X_label: str         Label for X-axis.
        Y_label: str         Label for Y-axis. max 8 characters.
        linesep: str         The requested line separator. default: os.linesep
        x_min, x_max: float  Limits for the displayed X values.
        y_min, y_max: float  Limits for the displayed Y values.
        lc: ColorDefinition         Give the line color.
        bg: ColorDefinition         Give the background color.
        color_mode: ColorMode      Specify color input mode; 'names' (default), 'byte' or
                             'rgb' see plotille.color.__docs__

    Returns:
        str: histogram over `X`.
    """
    fig = Figure()
    fig.width = width
    fig.height = height
    fig.x_label = X_label
    fig.y_label = Y_label
    fig.linesep = linesep
    if x_min is not None:
        fig.set_x_limits(min_=x_min)
    if x_max is not None:
        fig.set_x_limits(max_=x_max)
    if y_min is not None:
        fig.set_y_limits(min_=y_min)
    if y_max is not None:
        fig.set_y_limits(max_=y_max)
    fig.background = bg
    fig.color_mode = color_mode

    if lc is None and bg is None:
        fig.with_colors = False

    fig.histogram(X, bins, lc)

    return fig.show()


def scatter(
    X: DataValues,
    Y: DataValues,
    width: int = 80,
    height: int = 40,
    X_label: str = "X",
    Y_label: str = "Y",
    linesep: str = os.linesep,
    x_min: DataValue | None = None,
    x_max: DataValue | None = None,
    y_min: DataValue | None = None,
    y_max: DataValue | None = None,
    lc: ColorDefinition = None,
    bg: ColorDefinition = None,
    color_mode: ColorMode = "names",
    origin: bool = True,
    marker: str | None = None,
) -> str:
    """Create scatter plot with X , Y values

    Basically plotting without interpolation:
        `plot(X, Y, ... , interp=None)`

    Parameters:
        X: List[float]       X values.
        Y: List[float]       Y values. X and Y must have the same number of entries.
        width: int           The number of characters for the width (columns) of the
                             canvas.
        height: int          The number of characters for the hight (rows) of the
                             canvas.
        X_label: str         Label for X-axis.
        Y_label: str         Label for Y-axis. max 8 characters.
        linesep: str         The requested line separator. default: os.linesep
        x_min, x_max: float  Limits for the displayed X values.
        y_min, y_max: float  Limits for the displayed Y values.
        lc: ColorDefinition         Give the line color.
        bg: ColorDefinition         Give the background color.
        color_mode: ColorMode      Specify color input mode; 'names' (default), 'byte' or
                             'rgb' see plotille.color.__docs__
        origin: bool         Whether to print the origin. default: True
        marker: str          Instead of braille dots set a marker char.

    Returns:
        str: scatter plot over `X`, `Y`.
    """
    return plot(
        X,
        Y,
        width,
        height,
        X_label,
        Y_label,
        linesep,
        None,
        x_min,
        x_max,
        y_min,
        y_max,
        lc,
        bg,
        color_mode,
        origin,
        marker,
    )


def plot(
    X: DataValues,
    Y: DataValues,
    width: int = 80,
    height: int = 40,
    X_label: str = "X",
    Y_label: str = "Y",
    linesep: str = os.linesep,
    interp: Literal["linear"] | None = "linear",
    x_min: DataValue | None = None,
    x_max: DataValue | None = None,
    y_min: DataValue | None = None,
    y_max: DataValue | None = None,
    lc: ColorDefinition = None,
    bg: ColorDefinition = None,
    color_mode: ColorMode = "names",
    origin: bool = True,
    marker: str | None = None,
) -> str:
    """Create plot with X , Y values and linear interpolation between points

    Parameters:
        X: List[float]         X values.
        Y: List[float]         Y values. X and Y must have the same number of entries.
        width: int             The number of characters for the width (columns) of the
                               canvas.
        height: int            The number of characters for the hight (rows) of the
                               canvas.
        X_label: str           Label for X-axis.
        Y_label: str           Label for Y-axis. max 8 characters.
        linesep: str           The requested line separator. default: os.linesep
        interp: Optional[str]  Specify interpolation; values None, 'linear'
        x_min, x_max: float    Limits for the displayed X values.
        y_min, y_max: float    Limits for the displayed Y values.
        lc: ColorDefinition           Give the line color.
        bg: ColorDefinition           Give the background color.
        color_mode: ColorMode        Specify color input mode; 'names' (default), 'byte' or
                               'rgb' see plotille.color.__docs__
        origin: bool           Whether to print the origin. default: True
        marker: str            Instead of braille dots set a marker char for actual
                               values.

    Returns:
        str: plot over `X`, `Y`.
    """
    fig = Figure()
    fig.width = width
    fig.height = height
    fig.x_label = X_label
    fig.y_label = Y_label
    fig.linesep = linesep
    fig.origin = origin
    if x_min is not None:
        fig.set_x_limits(min_=x_min)
    if x_max is not None:
        fig.set_x_limits(max_=x_max)
    if y_min is not None:
        fig.set_y_limits(min_=y_min)
    if y_max is not None:
        fig.set_y_limits(max_=y_max)
    fig.background = bg
    fig.color_mode = color_mode

    if lc is None and bg is None:
        fig.with_colors = False

    fig.plot(X, Y, lc, interp, marker=marker)

    return fig.show()
