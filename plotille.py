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

from copy import copy
from math import floor, log
import os
from sys import version_info


IS_PY3 = version_info[0] == 3

if IS_PY3:
    unichr = chr
    unicode = str
    izip = zip
    roundeven = round
else:
    from itertools import izip

    def roundeven(x):
        x_r = round(x)
        if abs(x_r - x) == 0.5:
            return 2.0 * round(x / 2)
        return x_r


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
    from_points = izip(X, Y)
    to_points = izip(X, Y)
    try:
        # remove first point of to_points
        next(to_points)
    except StopIteration:
        # empty X, Y
        pass

    # plot points
    for (x0, y0), (x, y) in izip(from_points, to_points):
        canvas.point(x0, y0)

        canvas.point(x, y)
        if interp == 'linear':
            canvas.line(x0, y0, x, y)

    return canvas.plot(x_axis=True, x_label=X_label, y_axis=True, y_label=Y_label, linesep=linesep)


class Canvas(object):
    '''A canvas object for plotting braille dots

    A Canvas object has a `width` x `height` characters large canvas, in which it
    can plot indivitual braille point, lines out of braille points, rectangles,...
    Since a full braille character has 2 x 4 dots (⣿), the canvas has `width` * 2, `height` * 4
    dots to plot into in total.

    It maintains two coordinate systems: a reference system with the limits (xmin, ymin)
    in the lower left corner to (xmax, ymax) in the upper right corner is transformed
    into the canvas discrete, i.e. dots, coordinate system (0, 0) to (`width` * 2, `height` * 4).
    It does so transparently to clients of the Canvas, i.e. all plotting functions
    only accept coordinates in the reference system. If the coordinates are outside
    the reference system, they are not plotted.
    '''
    def __init__(self, width, height, xmin=0, ymin=0, xmax=1, ymax=1):
        '''Initiate a Canvas object

        Parameters:
            width: int         The number of characters for the width (columns) of the canvas.
            hight: int         The number of characters for the hight (rows) of the canvas.
            xmin, ymin: float  Lower left corner of reference system.
            xmax, ymax: float  Upper right corner of reference system.

        Reurns:
            Canvas object
        '''
        assert isinstance(width, int), '`width` has to be of type `int`'
        assert isinstance(height, int), '`height` has to be of type `int`'
        assert width > 0, '`width` has to be greater than 0'
        assert height > 0, '`height` has to be greater than 0'
        assert isinstance(xmin, (int, float))
        assert isinstance(xmax, (int, float))
        assert isinstance(ymin, (int, float))
        assert isinstance(ymax, (int, float))
        assert xmin < xmax, 'xmin ({}) has to be smaller than xmax ({})'.format(xmin, xmax)
        assert ymin < ymax, 'ymin ({}) has to be smaller than ymax ({})'.format(ymin, ymax)

        # characters in X / Y direction
        self._width = width
        self._height = height
        # the X / Y limits of the canvas, i.e. (0, 0) in canvas is (xmin,ymin) and
        # (width-1, height-1) in canvas is (xmax, ymax)
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax
        # value of x/y between one character
        self._x_delta = abs((xmax - xmin) / width)
        self._y_delta = abs((ymax - ymin) / height)
        # value of x/y between one point
        self._x_delta_pt = self._x_delta / 2
        self._y_delta_pt = self._y_delta / 4
        # the canvas to print in
        self._canvas = [['\u2800'] * width for i_ in range(height)]

    def __str__(self):
        return 'Canvas(width={}, height={}, xmin={}, ymin={}, xmax={}, ymax={})'.format(
            self.width, self.height, self.xmin, self.ymin, self.xmax, self.ymax
        )

    def __repr__(self):
        return self.__str__()

    @property
    def width(self):
        '''Number of characters in X direction'''
        return self._width

    @property
    def height(self):
        '''Number of characters in Y direction'''
        return self._height

    @property
    def xmin(self):
        '''Get xmin coordinate of reference coordinate system.'''
        return self._xmin

    @property
    def ymin(self):
        '''Get ymin coordinate of reference coordinate system.'''
        return self._ymin

    @property
    def xmax(self):
        '''Get xmax coordinate of reference coordinate system.'''
        return self._xmax

    @property
    def ymax(self):
        '''Get ymax coordinate of reference coordinate system.'''
        return self._ymax

    def _transform_x(self, x):
        return int(roundeven((x - self.xmin) / self._x_delta_pt))

    def _transform_y(self, y):
        return int(roundeven((y - self.ymin) / self._y_delta_pt))

    def _set(self, x_idx, y_idx, set_=True):
        '''Put a dot into the canvas at (x_idx, y_idx) [canvas coordinate system]

        Parameters:
            x: int      x-coordinate on canvas.
            y: int      y-coordinate on canvas.
            set_: bool  Whether to plot or remove the point.
        '''
        x_c, x_p = x_idx // 2, x_idx % 2
        y_c, y_p = y_idx // 4, y_idx % 4

        if 0 <= x_c < self.width and 0 <= y_c < self.height:
            b = self._canvas[y_c][x_c]
            b = _braille(b, x_p, y_p, set_)
            self._canvas[y_c][x_c] = b

    def dots_between(self, x0, y0, x1, y1):
        '''Number of dots between (x0, y0) and (x1, y1).

        Parameters:
            x0, y0: float  Point 0
            x1, y1: float  Point 1

        Returns:
            (int, int): dots in (x, y) direction
        '''
        x0_idx = self._transform_x(x0)
        y0_idx = self._transform_y(y0)
        x1_idx = self._transform_x(x1)
        y1_idx = self._transform_y(y1)

        return x1_idx - x0_idx, y1_idx - y0_idx

    def point(self, x, y, set_=True):
        '''Put a point into the canvas at (x, y) [reference coordinate system]

        Parameters:
            x: float    x-coordinate on reference system.
            y: float    y-coordinate on reference system.
            set_: bool  Whether to plot or remove the point.
        '''
        x_idx = self._transform_x(x)
        y_idx = self._transform_y(y)
        self._set(x_idx, y_idx, set_)

    def fill_char(self, x, y, set_=True):
        '''Fill the complete character at the point (x, y) [reference coordinate system]

        Parameters:
            x: float    x-coordinate on reference system.
            y: float    y-coordinate on reference system.
            set_: bool  Whether to plot or remove the point.
        '''
        x_idx = self._transform_x(x)
        y_idx = self._transform_y(y)

        x_c = x_idx // 2
        y_c = y_idx // 4

        if set_:
            self._canvas[y_c][x_c] = '⣿'
        else:
            self._canvas[y_c][x_c] = '\u2800'

    def line(self, x0, y0, x1, y1, set_=True):
        '''Plot line between point (x0, y0) and (x1, y1) [reference coordinate system].

        Parameters:
            x0, y0: float  Point 0
            x1, y1: float  Point 1
            set_: bool     Whether to plot or remove the line.
        '''
        x0_idx = self._transform_x(x0)
        y0_idx = self._transform_y(y0)
        self._set(x0_idx, y0_idx, set_)

        x1_idx = self._transform_x(x1)
        y1_idx = self._transform_y(y1)
        self._set(x1_idx, y1_idx, set_)

        x_diff = x1_idx - x0_idx
        y_diff = y1_idx - y0_idx
        steps = max(abs(x_diff), abs(y_diff))
        for i in range(1, steps):
            xb = x0_idx + int(roundeven(x_diff / steps * i))
            yb = y0_idx + int(roundeven(y_diff / steps * i))
            self._set(xb, yb, set_)

    def rect(self, xmin, ymin, xmax, ymax, set_=True):
        '''Plot rectangle with bbox (xmin, ymin) and (xmax, ymax) [reference coordinate system].

        Parameters:
            xmin, ymin: float  Lower left corner of rectangle.
            xmax, ymax: float  Upper right corner of rectangle.
            set_: bool         Whether to plot or remove the rect.
        '''
        assert xmin <= xmax
        assert ymin <= ymax
        self.line(xmin, ymin, xmin, ymax, set_)
        self.line(xmin, ymax, xmax, ymax, set_)
        self.line(xmax, ymax, xmax, ymin, set_)
        self.line(xmax, ymin, xmin, ymin, set_)

    def plot(self, x_axis=False, y_axis=False, y_label='Y', x_label='X', linesep=os.linesep):
        '''Transform canvas into `print`-able string

        Parameters:
            x_axis: bool  Add a X-axis at the bottom.
            y_axis: bool  Add a Y-axis to the left.
            y_label: str  Label for Y-axis. max 8 characters.
            x_label: str  Label for X-axis.
            linesep: str  The requested line seperator. default: os.linesep

        Returns:
            unicode: The cancas as a string.
        '''
        res = copy(self._canvas)
        if y_axis:
            # add Y-axis
            for i in range(self.height):
                res[i] = ['{:10.5f} | '.format(i * self._y_delta + self._ymin)] + res[i]
            ylbl = '({})'.format(y_label)
            ylbl_left = (10 - len(ylbl)) // 2
            ylbl_right = ylbl_left + len(ylbl) % 2
            res += [['{:10.5f} |'.format(self.height * self._y_delta + self._ymin)],
                    [' ' * (ylbl_left) + ylbl + ' ' * (ylbl_right) + ' ^']]

        if x_axis:
            # add X-axis
            starts = ['', '']
            if y_axis:
                starts = [' ' * 11 + '| ', '-' * 11 + '|-']
            res = ([[starts[0]] + ['{:<10.5f}'.format(i * 10 * self._x_delta + self._xmin)
                                   for i in range(self.width // 10 + 1)]] +
                   [[starts[1] + '|---------' * (self.width // 10) + '|-> (' + x_label + ')']] +
                   res)
        return linesep.join([''.join(row) for row in reversed(res)])


def _set_limit(limit, orig):
    if limit is not None:
        assert isinstance(limit, (int, float))
        return limit
    return orig


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


def _braille(b, x, y, set_=True):
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
    if set_:
        dots.append(xy2dot[y][x])
    else:
        idx = xy2dot[y][x]
        if idx in dots:
            dots.remove(idx)
    return _braille_from(dots)


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
    xmin = min(X) if len(X) > 0 else 0
    xmax = max(X) if len(X) > 0 else 1
    xwidth = abs((xmax - xmin) / bins)

    y = [0] * bins
    for x in X:
        x_idx = min(bins - 1, int(floor((x - xmin) / xwidth)))
        y[x_idx] += 1

    return y, [i * xwidth + xmin for i in range(bins + 1)]
