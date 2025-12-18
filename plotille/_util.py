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
from collections.abc import Collection
from datetime import datetime, timedelta
from typing import Any

DataValue = float | int | datetime
DataValues = Collection[float | int] | Collection[datetime]


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


def _numpy_to_native(x: Any) -> Any:
    # cf. https://numpy.org/doc/stable/reference/generated/numpy.ndarray.item.html
    if (
        "<class 'numpy." in str(type(x)) or "<type 'numpy." in str(type(x))
    ) and callable(x.item):
        return x.item()
    return x


def hist(X: DataValues, bins: int) -> tuple[list[int], list[float] | list[datetime]]:
    """Create histogram similar to `numpy.hist()`

    Parameters:
        X: List[float|datetime]  The items to count over.
        bins: int                The number of bins to put X entries in.

    Returns:
        (counts, bins):
            counts: List[int]  The counts for all bins.
            bins: List[float]  The range for each bin:
                                bin `i` is in [bins[i], bins[i+1])
    """
    assert bins > 0

    xs = [_numpy_to_native(x) for x in X]

    if len(xs) == 0:
        xmin = 0.0
        xmax = 1.0
    else:
        xmin = min(xs)
        xmax = max(xs)

    is_datetime = isinstance(xmax, datetime)
    assert not is_datetime or isinstance(xmin, datetime)

    if xmin == xmax:
        if is_datetime:
            xmin -= timedelta(seconds=1)
            xmax += timedelta(seconds=1)
        else:
            xmin -= 0.5
            xmax += 0.5

    delta = xmax - xmin
    if isinstance(delta, timedelta):
        delta = delta.total_seconds()

    xwidth = delta / bins

    y = [0] * bins
    for x in xs:
        delta = x - xmin
        if isinstance(delta, timedelta):
            delta = delta.total_seconds()
        x_idx = min(bins - 1, int(delta // xwidth))
        y[x_idx] += 1

    if is_datetime:
        xwidth = mk_timedelta(xwidth)

    return y, [i * xwidth + xmin for i in range(bins + 1)]


def mk_timedelta(v: float) -> timedelta:
    seconds = int(v)
    microseconds = int((v - seconds) * 1e6)
    return timedelta(seconds=seconds, microseconds=microseconds)
