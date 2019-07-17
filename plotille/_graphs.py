# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2018 Tammo Ippen, tammo.ippen@posteo.de

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

from ._colors import color
from ._figure import Figure
from ._input_formatter import InputFormatter
from ._util import hist as compute_hist


def hist(X, bins=40, width=80, log_scale=False, linesep=os.linesep,  # noqa: N803
         lc=None, bg=None, color_mode='names'):
    """Create histogram over `X` from left to right

    The values on the left are the center of the bucket, i.e. `(bin[i] + bin[i+1]) / 2`.
    The values on the right are the total counts of this bucket.

    Parameters:
        X: List[float]  The items to count over.
        bins: int       The number of bins to put X entries in (rows).
        width: int      The number of characters for the width (columns).
        log_scale: bool Scale the histogram with `log` function.
        linesep: str    The requested line seperator. default: os.linesep
        lc: multiple         Give the line color.
        bg: multiple         Give the background color.
        color_mode: str      Specify color input mode; 'names' (default), 'byte' or 'rgb'
                             see plotille.color.__docs__

    Returns:
        str: histogram over `X` from left to right.
    """
    def _scale(a):
        if log_scale and a > 0:
            return log(a)
        return a

    ipf = InputFormatter()
    h, b = compute_hist(X, bins)
    h_max = _scale(max(h)) or 1
    delta = b[-1] - b[0]

    canvas = ['        bucket       | {} {}'.format('_' * width, 'Total Counts')]
    lasts = ['', '⠂', '⠆', '⠇', '⡇', '⡗', '⡷', '⡿']
    for i in range(bins):
        hight = int(width * 8 * _scale(h[i]) / h_max)
        canvas += ['[{}, {}) | {} {}'.format(
            ipf.fmt(b[i], delta=delta, chars=8, left=True),
            ipf.fmt(b[i + 1], delta=delta, chars=8, left=False),
            color('⣿' * (hight // 8) + lasts[hight % 8], fg=lc, bg=bg, mode=color_mode) +
            color('\u2800' * (width - (hight // 8) + int(hight % 8 == 0)), bg=bg, mode=color_mode),
            h[i])]
    canvas += ['‾' * (2*8 + 2 + 3 + width + 12)]
    return linesep.join(canvas)


def histogram(X, bins=160, width=80, height=40, X_label='X', Y_label='Counts', linesep=os.linesep,  # noqa: N803
              x_min=None, x_max=None, y_min=None, y_max=None,
              lc=None, bg=None, color_mode='names'):
    """Create histogram over `X`

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
        lc: multiple         Give the line color.
        bg: multiple         Give the background color.
        color_mode: str      Specify color input mode; 'names' (default), 'byte' or 'rgb'
                             see plotille.color.__docs__

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


def scatter(X, Y, width=80, height=40, X_label='X', Y_label='Y', linesep=os.linesep,  # noqa: N803
            x_min=None, x_max=None, y_min=None, y_max=None,
            lc=None, bg=None, color_mode='names', origin=True):
    """Create scatter plot with X , Y values

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
        lc: multiple         Give the line color.
        bg: multiple         Give the background color.
        color_mode: str      Specify color input mode; 'names' (default), 'byte' or 'rgb'
                             see plotille.color.__docs__
        origin: bool         Whether to print the origin. default: True

    Returns:
        str: scatter plot over `X`, `Y`.
    """
    return plot(X, Y, width, height, X_label, Y_label, linesep, None,
                x_min, x_max, y_min, y_max, lc, bg, color_mode, origin)


def plot(X, Y, width=80, height=40, X_label='X', Y_label='Y', linesep=os.linesep, interp='linear',  # noqa: N803
         x_min=None, x_max=None, y_min=None, y_max=None,
         lc=None, bg=None, color_mode='names', origin=True):
    """Create plot with X , Y values and linear interpolation between points

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
        lc: multiple           Give the line color.
        bg: multiple           Give the background color.
        color_mode: str        Specify color input mode; 'names' (default), 'byte' or 'rgb'
                               see plotille.color.__docs__
        origin: bool           Whether to print the origin. default: True

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

    fig.plot(X, Y, lc, interp)

    return fig.show()
