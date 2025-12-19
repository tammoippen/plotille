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

import math
from collections.abc import Sequence
from datetime import datetime, timedelta
from numbers import Real
from typing import Any, TypeAlias, TypeGuard

try:
    import numpy as np

    DatetimeLike: TypeAlias = np.datetime64 | datetime
except ImportError:
    DatetimeLike: TypeAlias = datetime  # type: ignore[misc,no-redef]

# Legacy types - used only for public API compatibility
# These allow users to pass datetime or numeric values to plot functions
# Internally, everything is normalized to float
DataValue = Real | DatetimeLike
DataValues = Sequence[Real] | Sequence[DatetimeLike]

# New internal types - what we actually work with after normalization
NormalizedValue: TypeAlias = float
NormalizedValues: TypeAlias = Sequence[float]


def roundeven(x: float) -> float:
    """Round to next even integer number in case of `X.5`

    Parameters:
        x: float  The number to round.

    Returns:
        int: floor(x)       if x - floor(x) < 0.5
             ceil(x)        if x - floor(x) > 0.5
             next even of x if x - floor(x) == 0.5
    """
    if math.isinf(x) or math.isnan(x):
        return x  # same behaviour as in python2
    return round(x)


def is_datetimes(xs: Sequence[DataValue]) -> TypeGuard[Sequence[DatetimeLike]]:
    is_datetime = None
    for x in xs:
        if is_datetime is None:
            is_datetime = isinstance(x, DatetimeLike)
        elif is_datetime != isinstance(x, DatetimeLike):
            raise TypeError("Mixed types in sequence.")
    return is_datetime or False


def _numpy_to_native(x: Any) -> Any:
    # cf. https://numpy.org/doc/stable/reference/generated/numpy.ndarray.item.html
    if (
        "<class 'numpy." in str(type(x)) or "<type 'numpy." in str(type(x))
    ) and callable(x.item):
        return x.item()
    return x


def hist(
    X: Sequence[float], bins: int, is_datetime: bool = False
) -> tuple[list[int], list[float]]:
    """Create histogram similar to `numpy.hist()`

    NOTE: This function now expects X to be already normalized to float.
    The is_datetime parameter indicates if the original data was datetime.

    Parameters:
        X: Sequence[float]  Already normalized to float (timestamps if datetime)
        bins: int           The number of bins to put X entries in.
        is_datetime: bool   Whether original data was datetime (for bucket calculation)

    Returns:
        (counts, bins):
            counts: list[int]  The counts for all bins.
            bins: list[float]  The range for each bin (as floats/timestamps)
    """
    assert bins > 0

    # Convert numpy scalars to native types to avoid overflow
    xs = [_numpy_to_native(x) for x in X]

    if len(xs) == 0:
        xmin = 0.0
        xmax = 1.0
    else:
        xmin = float(min(xs))
        xmax = float(max(xs))

    if xmin == xmax:
        xmin -= 0.5
        xmax += 0.5

    delta = xmax - xmin
    xwidth = delta / bins

    y = [0] * bins
    for x in xs:
        delta_x = x - xmin
        x_idx = min(bins - 1, int(delta_x // xwidth))
        y[x_idx] += 1

    return y, [i * xwidth + xmin for i in range(bins + 1)]


def mk_timedelta(v: float) -> timedelta:
    seconds = int(v)
    microseconds = int((v - seconds) * 1e6)
    return timedelta(seconds=seconds, microseconds=microseconds)
