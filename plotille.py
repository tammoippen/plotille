# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

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


from math import floor, log
import os
from sys import version_info


IS_PY3 = version_info[0] == 3

if IS_PY3:
    unichr = chr
    unicode = str


def hist(X, bins=50, width=80, log_scale=False, linesep=os.linesep):  # noqa: N803
    '''Create histogram over `X`

    Parameters:
        X: List[float]  The items to count over.
        bins: int       The number of bins to put X entries in (rows).
        width: int      The number of characters for the width (columns).
        log_scale: bool Scale the histogram with `log` function.

    Returns:
        str: histogram over `X` from left to right.
    '''
    def _scale(a):
        if log_scale:
            return log(a)
        return a

    h, b = _hist(X, bins)
    h_max = _scale(max(h))

    canvas = ['  bucket   | {} {}'.format('_' * width, 'Total Counts')]
    lasts = ['', '⠂', '⠆', '⠇', '⡇', '⡗', '⡷', '⡿']
    for i in range(bins):
        hight = int(width * 8 * _scale(h[i]) / h_max)
        canvas += ['{:10.5f} | {:{width}s} {}'.format(
            b[i],
            '⣿' * (hight // 8) + lasts[hight % 8],
            h[i],
            width=width)]
    canvas += ['{:10.5f} | {}'.format(b[bins], '‾' * width)]
    return linesep.join(canvas)


def scatter(X, Y, width=80, height=50, X_label='X', Y_label='Y', linesep=os.linesep):  # noqa: N803
    '''Create scatter plot with X , Y values

    Parameters:
        X: List[float]  X values.
        Y: List[float]  Y values. X and Y must have the same number of entries.
        width: int      The number of characters for the width (columns) of the canvas.
        hight: int      The number of characters for the hight (rows) of the canvas.
        X_label: str    Label for X-axis.
        Y_label: str    Label for Y-axis. max 8 characters.

    Returns:
        str: scatter plot over `X`, `Y`.
    '''
    assert len(X) == len(Y)
    assert len(Y_label) <= 8

    ymin, ymax = min(Y), max(Y)
    xmin, xmax = min(X), max(X)

    xwidth = abs((xmax - xmin) / width)
    xwidth_p = xwidth / 2
    ywidth = abs((ymax - ymin) / height)
    ywidth_p = ywidth / 4

    canvas = _init(width, height)

    # plot X,Y points
    for x, y in zip(X, Y):
        x_idx = min(width * 2 - 1, int(round((x - xmin) / xwidth_p)))
        y_idx = min(height * 4 - 1, int(round((y - ymin) / ywidth_p)))
        _set(canvas, x_idx, y_idx)

    # add Y-axis
    for i in range(height):
        canvas[i] = ['{:10.5f} | '.format(i * ywidth + ymin)] + canvas[i]
    ylbl = '({})'.format(Y_label)
    ylbl_left = (10 - len(ylbl)) // 2
    ylbl_right = ylbl_left + len(ylbl) % 2
    canvas += [['{:10.5f} | '.format(height * ywidth + ymin)], [' ' * (ylbl_left) + ylbl + ' ' * (ylbl_right) + ' ^']]

    # add X-axis
    canvas = ([[' ' * 11 + '| '] + ['{:<10.5f}'.format(i * xwidth * 10 + xmin) for i in range(width // 10)]] +
              [['-' * 11 + '|-' + '|---------' * (width // 10) + '> (' + X_label + ')']] +
              canvas)
    return linesep.join([''.join(row) for row in reversed(canvas)])


def plot(X, Y, width=80, height=50, X_label='X', Y_label='Y', linesep=os.linesep):  # noqa: N803
    '''Create plot with X , Y values and linear interpolation between points

    Parameters:
        X: List[float]  X values.
        Y: List[float]  Y values. X and Y must have the same number of entries.
        width: int      The number of characters for the width (columns) of the canvas.
        hight: int      The number of characters for the hight (rows) of the canvas.
        X_label: str    Label for X-axis.
        Y_label: str    Label for Y-axis. max 8 characters.

    Returns:
        str: plot over `X`, `Y`.
    '''
    ymin, ymax = min(Y), max(Y)
    xmin, xmax = min(X), max(X)
    xwidth = abs((xmax - xmin) / width)
    xwidth_p = xwidth / 2
    ywidth = abs((ymax - ymin) / height)
    ywidth_p = ywidth / 4

    canvas = _init(width, height)

    # plot X,Y points
    # first point
    points = sorted(zip(X, Y))
    x0, y0 = points[0]
    x0_idx = min(width * 2 - 1, int(round((x0 - xmin) / xwidth_p)))
    y0_idx = min(height * 4 - 1, int(round((y0 - ymin) / ywidth_p)))
    _set(canvas, x0_idx, y0_idx)

    # subsequent points
    for x, y in points[1:]:
        x_idx = min(width * 2 - 1, int(round((x - xmin) / xwidth_p)))
        y_idx = min(height * 4 - 1, int(round((y - ymin) / ywidth_p)))
        _set(canvas, x_idx, y_idx)

        # plot between points
        m = 0
        if x_idx - x0_idx:
            m = (y_idx - y0_idx) / (x_idx - x0_idx)

        m_inv = 0
        if y_idx - y0_idx:
            m_inv = (x_idx - x0_idx) / (y_idx - y0_idx)

        # left/right
        if -0.5 < m < 0.5:
            for i in range(1, x_idx - x0_idx):
                yb = min(y_idx, y0_idx + int(round(m * i)))
                xb = x0_idx + i
                _set(canvas, xb, yb)
        else:
            for i in range(1, abs(y_idx - y0_idx)):
                yb = y0_idx + _sign(m) * i
                xb = min(x_idx, x0_idx + int(abs(round(m_inv * i))))
                _set(canvas, xb, yb)

        # store last
        x0_idx, y0_idx = x_idx, y_idx

    # add Y-axis
    for i in range(height):
        canvas[i] = ['{:10.5f} | '.format(i * ywidth + ymin)] + canvas[i]
    ylbl = '({})'.format(Y_label)
    ylbl_left = (10 - len(ylbl)) // 2
    ylbl_right = ylbl_left + len(ylbl) % 2
    canvas += [['{:10.5f} | '.format(height * ywidth + ymin)], [' ' * (ylbl_left) + ylbl + ' ' * (ylbl_right) + ' ^']]

    # add X-axis
    canvas = ([[' ' * 11 + '| '] + ['{:<10.5f}'.format(i * 10 * xwidth + xmin) for i in range(width // 10)]] +
              [['-' * 11 + '|-' + '|---------' * (width // 10) + '> (' + X_label + ')']] +
              canvas)
    return linesep.join([''.join(row) for row in reversed(canvas)])


def _sign(a):
    '''Return sign of `a`

    Parameters:
        a: float/int

    Returns:
        int: 1 if `a` is positive, -1 otherwise
    '''
    return int(a > 0) - int(a < 0)


def _hist(X, bins):  # noqa: N803
    '''Create histogram similar to `numpy.hist()`

    Parameters:
        X: List[float]  The items to count over.
        bins: int       The number of bins to put X entries in.

    Returns:
        (counts, bins):
            counts: List[int]  The counts for all bins.
            bins: List[float]  The range for each bin: bin `i` is in [bins[i], bins[i+1])
    '''
    xmin, xmax = min(X), max(X)
    xwidth = abs((xmax - xmin) / bins)

    y = [0] * bins
    for x in X:
        x_idx = min(bins - 1, int(floor((x - xmin) / xwidth)))
        y[x_idx] += 1

    return y, [i * xwidth + xmin for i in range(bins + 1)]


def _braille_from(dots):
    '''Unicode character for braille with given dots set

    See https://en.wikipedia.org/wiki/Braille_Patterns#Identifying.2C_naming_and_ordering
    for dot to braille encoding.

    Parameters:
        dots: List[int]  All dots that should be set. Allowed dots are 1,2,3,4,5,6,7,8

    Returns:
        unicode: braille sign with given dots set. \u2800 - \u28ff
    '''
    bin_code = ['0'] * 8
    for i in dots:
        bin_code[8 - i] = '1'

    code = 0x2800 + int(''.join(bin_code), 2)

    return unichr(code)


def _dots_from(braille):
    '''Get set dots from given

    See https://en.wikipedia.org/wiki/Braille_Patterns#Identifying.2C_naming_and_ordering
    for braille to dot decoding.

    Parameters:
        braille: unicode  Braille character in \u2800 - \u28ff

    Returns:
        List[int]: dots that are set in braille sign
    '''
    assert 0x2800 <= ord(braille) <= 0x28ff

    code = unicode(bin(ord(braille) - 0x2800))[2:].rjust(8, '0')

    dots = []
    for i, c in enumerate(code):
        if c == '1':
            dots += [8 - i]

    return sorted(dots)


def _braille_set(b, x, y):
    '''Set dot at position x, y, with (0, 0) is top left corner.

    Parameters:
        b: unicode  Braille character in \u2800 - \u28ff
        x: int      x-coordinate \in [0, 1]
        y: int      y-coordinate \in [0, 1, 2, 3]

    Returns:
        unicode: braille sign with given dot set (other dots are unchanged).
    '''
    dots = _dots_from(b)
    xy2dot = [[7, 8],  # I plot upside down, hence the different order
              [3, 6],
              [2, 5],
              [1, 4]]
    return _braille_from(dots + [xy2dot[y][x]])


def _set(canvas, x, y):
    '''Put a dot into the canvas at (x, y)

    Canvas is a list of list of unicode chars in \u2800 - \u28ff.
    Width of canvas (x): num chars in inner list times 2 dots
    Height of canvas (y): num of inner list times 4 dots
    Top left of canvas is (0, 0).

    This function modifies the canvas directly!

    Parameters:
        canvas: List[List[unichr]]  Canvas to plot in.
        x: int                      x-coordinate (width) on canvas.
        y: int                      y-coordinate (hight) on canvas.
    '''
    x_c, x_p = x // 2, x % 2
    y_c, y_p = y // 4, y % 4

    b = canvas[y_c][x_c]
    b = _braille_set(b, x_p, y_p)
    canvas[y_c][x_c] = b


def _init(width, height):
    return [['\u2800'] * width for i_ in range(height)]
