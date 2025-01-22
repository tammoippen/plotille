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
from typing import Any, Union


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


def _pendulum_to_native(x: Any) -> Any:
    if "pendulum.datetime.DateTime" in str(type(x)):
        return datetime.fromisoformat(x.isoformat())
    return x


def hist(
    X: Sequence[Union[float, datetime]], bins: int
) -> tuple[list[int], list[Union[float, datetime]]]:
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

    X = [_numpy_to_native(_pendulum_to_native(x)) for x in X]

    xmin = min(X) if len(X) > 0 else 0.0
    xmax = max(X) if len(X) > 0 else 1.0
    if xmin == xmax:  # what about dame datetimes?
        xmin -= 0.5
        xmax += 0.5

    delta = xmax - xmin
    is_datetime = False
    if isinstance(delta, timedelta):
        is_datetime = True
        delta = delta.total_seconds()

    xwidth = delta / bins

    y = [0] * bins
    for x in X:
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
