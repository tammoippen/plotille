# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 Tammo Ippen, tammo.ippen@posteo.de

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

from math import log
import os

from six.moves import zip

from ._canvas import Canvas
from ._util import _hist, _set_limit


def hist(X, bins=40, width=80, log_scale=False, linesep=os.linesep):  # noqa: N803
    '''Create histogram over `X` from left to right

    The values on the left are the center of the bucket, i.e. `(bin[i] + bin[i+1]) / 2`.
    The values on the right are the total counts of this bucket.

    Parameters:
        X: List[float]  The items to count over.
        bins: int       The number of bins to put X entries in (rows).
        width: int      The number of characters for the width (columns).
        log_scale: bool Scale the histogram with `log` function.
        linesep: str    The requested line seperator. default: os.linesep

    Returns:
        str: histogram over `X` from left to right.
    '''
    def _scale(a):
        if log_scale and a > 0:
            return log(a)
        return a

    h, b = _hist(X, bins)
    h_max = _scale(max(h)) or 1

    canvas = ['  bucket   | {} {}'.format('_' * width, 'Total Counts')]
    lasts = ['', '⠂', '⠆', '⠇', '⡇', '⡗', '⡷', '⡿']
    for i in range(bins):
        hight = int(width * 8 * _scale(h[i]) / h_max)
        canvas += ['{:10.5f} | {:{width}s} {}'.format(
            (b[i] + b[i + 1]) / 2,  # use bucket center as representation
            '⣿' * (hight // 8) + lasts[hight % 8],
            h[i],
            width=width)]
    canvas += ['‾' * (10 + 3 + width + 12)]
    return linesep.join(canvas)


def histogram(X, bins=160, width=80, height=40, X_label='X', Y_label='Counts', linesep=os.linesep,  # noqa: N803
              x_min=None, x_max=None, y_min=None, y_max=None):
    '''Create histogram over `X`

    In contrast to `hist`, this is the more `usual` histogram from bottom
    to up. The X-axis represents the values in `X` and the Y-axis is the
    corresponding frequency.

    Parameters:
        X: List[float]  The items to count over.
        bins: int       The number of bins to put X entries in (columns).
        height: int     The number of characters for the height (rows).
        X_label: str    Label for X-axis.
        Y_label: str    Label for Y-axis. max 8 characters.
        linesep: str    The requested line seperator. default: os.linesep
        x_min, x_max: float  Limits for the displayed X values.
        y_min, y_max: float  Limits for the displayed Y values.

    Returns:
        str: histogram over `X`.
    '''
    assert bins > 0
    h, b = _hist(X, bins)

    ymax = 1
    ymin = 0
    if max(h) > 0:
        ymax = max(h) or 1
        # have some space above the plot
        offset = abs(ymax) / 10
        ymax += offset

    ymin = _set_limit(y_min, ymin)
    ymax = _set_limit(y_max, ymax)

    xmin = 0
    xmax = 1
    if len(X) > 0:
        xmin = min(X)
        xmax = max(X)
        # have some space left and right of the plot
        offset = max(abs(xmax), abs(xmin)) / 10
        xmin -= offset
        xmax += offset

    xmin = _set_limit(x_min, xmin)
    xmax = _set_limit(x_max, xmax)

    canvas = Canvas(width, height, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    # how fat will one bar of the histogram be
    x_diff = canvas.dots_between(b[0], 0, b[1], 0)[0] or 1
    bin_size = (b[1] - b[0]) / x_diff

    for i in range(bins):
        if h[i] > 0:
            for j in range(x_diff):
                x_ = b[i] + j * bin_size
                canvas.line(x_, 0, x_, h[i])

    return canvas.plot(x_axis=True, x_label=X_label, y_axis=True, y_label=Y_label, linesep=linesep)


def scatter(X, Y, width=80, height=40, X_label='X', Y_label='Y', linesep=os.linesep,  # noqa: N803
            x_min=None, x_max=None, y_min=None, y_max=None):
    '''Create scatter plot with X , Y values

    Basically plotting without interpolation:
        `plot(X, Y, ... , interp=None)`

    Parameters:
        X: List[float]       X values.
        Y: List[float]       Y values. X and Y must have the same number of entries.
        width: int           The number of characters for the width (columns) of the canvas.
        hight: int           The number of characters for the hight (rows) of the canvas.
        X_label: str         Label for X-axis.
        Y_label: str         Label for Y-axis. max 8 characters.
        linesep: str         The requested line seperator. default: os.linesep
        x_min, x_max: float  Limits for the displayed X values.
        y_min, y_max: float  Limits for the displayed Y values.

    Returns:
        str: scatter plot over `X`, `Y`.
    '''
    return plot(X, Y, width, height, X_label, Y_label, linesep, None, x_min, x_max, y_min, y_max)


def plot(X, Y, width=80, height=40, X_label='X', Y_label='Y', linesep=os.linesep, interp='linear',  # noqa: N803
         x_min=None, x_max=None, y_min=None, y_max=None):
    '''Create plot with X , Y values and linear interpolation between points

    Parameters:
        X: List[float]         X values.
        Y: List[float]         Y values. X and Y must have the same number of entries.
        width: int             The number of characters for the width (columns) of the canvas.
        hight: int             The number of characters for the hight (rows) of the canvas.
        X_label: str           Label for X-axis.
        Y_label: str           Label for Y-axis. max 8 characters.
        linesep: str           The requested line seperator. default: os.linesep
        interp: Optional[str]  Specify interpolation; values None, 'linear'
        x_min, x_max: float    Limits for the displayed X values.
        y_min, y_max: float    Limits for the displayed Y values.

    Returns:
        str: plot over `X`, `Y`.
    '''
    assert len(X) == len(Y)
    assert len(Y_label) <= 8
    assert interp in ('linear', None)

    ymin = 0
    ymax = 1
    if len(Y) > 0:
        ymin = min(Y)
        ymax = max(Y)
        # have some space above and below the plot
        offset = max(abs(ymax), abs(ymin)) / 10
        ymin -= offset
        ymax += offset

    ymin = _set_limit(y_min, ymin)
    ymax = _set_limit(y_max, ymax)

    xmin = 0
    xmax = 1
    if len(X) > 0:
        xmin = min(X)
        xmax = max(X)
        # have some space above and below the plot
        offset = max(abs(xmax), abs(xmin)) / 10
        xmin -= offset
        xmax += offset

    xmin = _set_limit(x_min, xmin)
    xmax = _set_limit(x_max, xmax)

    canvas = Canvas(width, height, xmin, ymin, xmax, ymax)

    # make point iterators
    from_points = zip(X, Y)
    to_points = zip(X, Y)
    try:
        # remove first point of to_points
        next(to_points)
    except StopIteration:
        # empty X, Y
        pass

    # plot points
    for (x0, y0), (x, y) in zip(from_points, to_points):
        canvas.point(x0, y0)

        canvas.point(x, y)
        if interp == 'linear':
            canvas.line(x0, y0, x, y)

    return canvas.plot(x_axis=True, x_label=X_label, y_axis=True, y_label=Y_label, linesep=linesep)
