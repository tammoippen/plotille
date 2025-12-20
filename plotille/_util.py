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
from datetime import datetime

DataValue = float | int | datetime
"""Basically any datetime like value and any numeric value.

Eventually, you have to add a float_converter for the type, e.g. with Decimal see
test `test_timeseries_decimals`.

There are already converters for numpy numeric and datetime data.
"""
DataValues = Sequence[float | int] | Sequence[datetime]
"""Either a list of numeric data or a list of datetime like data."""


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


def hist(X: Sequence[float], bins: int) -> tuple[list[int], list[float]]:
    """Create histogram similar to `numpy.hist()`

    NOTE: This function expects X to be already normalized to numeric.

    Parameters:
        X: Sequence[float]  Already normalized to float (timestamps if datetime)
        bins: int           The number of bins to put X entries in.

    Returns:
        (counts, bins):
            counts: list[int]  The counts for all bins.
            bins: list[float]  The range for each bin:
                               bin `i` is in [bins[i], bins[i+1])
    """
    assert bins > 0

    if len(X) == 0:
        xmin = 0.0
        xmax = 1.0
    else:
        xmin = float(min(X))
        xmax = float(max(X))

    if xmin == xmax:
        xmin -= 0.5
        xmax += 0.5

    delta = xmax - xmin
    xwidth = delta / bins

    y = [0] * bins
    for x in X:
        delta_x = x - xmin
        x_idx = min(bins - 1, int(delta_x // xwidth))
        y[x_idx] += 1

    return y, [i * xwidth + xmin for i in range(bins + 1)]
