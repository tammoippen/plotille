# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2021 Tammo Ippen, tammo.ippen@posteo.de

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

from datetime import timedelta
from itertools import cycle
import os

from six.moves import zip

from ._canvas import Canvas
from ._colors import color
from ._input_formatter import InputFormatter
from ._util import hist, mk_timedelta, timestamp

# TODO documentation!!!
# TODO tests


class Figure(object):
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
    _COLOR_SEQ = [
        {'names': 'white', 'rgb': (255, 255, 255), 'byte': 0X7},
        {'names': 'red', 'rgb': (255, 0, 0), 'byte': 0x1},
        {'names': 'green', 'rgb': (0, 255, 0), 'byte': 0x2},
        {'names': 'yellow', 'rgb': (255, 255, 0), 'byte': 0x3},
        {'names': 'blue', 'rgb': (0, 0, 255), 'byte': 0x4},
        {'names': 'magenta', 'rgb': (255, 0, 255), 'byte': 0x5},
        {'names': 'cyan', 'rgb': (0, 255, 255), 'byte': 0x6},
    ]

    def __init__(self):
        self._color_seq = iter(cycle(Figure._COLOR_SEQ))
        self._width = None
        self._height = None
        self._x_min = None
        self._x_max = None
        self._y_min = None
        self._y_max = None
        self._color_mode = None
        self._with_colors = True
        self._origin = True
        self.linesep = os.linesep
        self.background = None
        self.x_label = 'X'
        self.y_label = 'Y'
        # min, max -> value
        self.y_ticks_fkt = None
        self.x_ticks_fkt = None
        self._plots = []
        self._texts = []
        self._spans = []
        self._in_fmt = InputFormatter()

    @property
    def width(self):
        if self._width is not None:
            return self._width
        return 80

    @width.setter
    def width(self, value):
        if not (isinstance(value, int) and value > 0):
            raise ValueError('Invalid width: {}'.format(value))
        self._width = value

    @property
    def height(self):
        if self._height is not None:
            return self._height
        return 40

    @height.setter
    def height(self, value):
        if not (isinstance(value, int) and value > 0):
            raise ValueError('Invalid height: {}'.format(value))
        self._height = value

    @property
    def color_mode(self):
        if self._color_mode is not None:
            return self._color_mode
        return 'names'

    @color_mode.setter
    def color_mode(self, value):
        if value not in ('names', 'byte', 'rgb'):
            raise ValueError('Only supports: names, byte, rgb!')
        if self._plots != []:
            raise RuntimeError('Change color mode only, when no plots are prepared.')
        self._color_mode = value

    @property
    def with_colors(self):
        return self._with_colors

    @with_colors.setter
    def with_colors(self, value):
        if not isinstance(value, bool):
            raise ValueError('Only bool allowed: "{}"'.format(value))
        self._with_colors = value

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        if not isinstance(value, bool):
            raise ValueError('Invalid origin: {}'.format(value))
        self._origin = value

    def register_label_formatter(self, type_, formatter):
        self._in_fmt.register_formatter(type_, formatter)

    def register_float_converter(self, type_, converter):
        self._in_fmt.register_converter(type_, converter)

    def x_limits(self):
        return self._limits(self._x_min, self._x_max, False)

    def set_x_limits(self, min_=None, max_=None):
        """Set min and max X values for displaying."""
        self._x_min, self._x_max = self._set_limits(self._x_min, self._x_max, min_, max_)

    def y_limits(self):
        return self._limits(self._y_min, self._y_max, True)

    def set_y_limits(self, min_=None, max_=None):
        """Set min and max Y values for displaying."""
        self._y_min, self._y_max = self._set_limits(self._y_min, self._y_max, min_, max_)

    def _set_limits(self, init_min, init_max, min_=None, max_=None):
        if min_ is not None and max_ is not None:
            if min_ >= max_:
                raise ValueError('min_ is larger or equal than max_.')
            init_min = min_
            init_max = max_
        elif min_ is not None:
            if init_max is not None and min_ >= init_max:
                raise ValueError('Previous max is smaller or equal to new min_.')
            init_min = min_
        elif max_ is not None:
            if init_min is not None and init_min >= max_:
                raise ValueError('Previous min is larger or equal to new max_.')
            init_max = max_
        else:
            init_min = None
            init_max = None

        return init_min, init_max

    def _limits(self, low_set, high_set, is_height):
        if low_set is not None and high_set is not None:
            return low_set, high_set

        low, high = None, None
        for p in self._plots + self._texts:
            if is_height:
                _min, _max = _limit(p.height_vals())
            else:
                _min, _max = _limit(p.width_vals())
            if low is None:
                low = _min
                high = _max

            low = min(_min, low)
            high = max(_max, high)

        return _choose(low, high, low_set, high_set)

    def _y_axis(self, ymin, ymax, label='Y'):
        delta = abs(ymax - ymin)
        if isinstance(delta, timedelta):
            y_delta = mk_timedelta(timestamp(delta) / self.height)
        else:
            y_delta = delta / self.height

        res = []
        for i in range(self.height):
            value = i * y_delta + ymin
            if self.y_ticks_fkt:
                value = self.y_ticks_fkt(value, value + y_delta)
            res += [self._in_fmt.fmt(value, abs(ymax - ymin), chars=10) + ' | ']

        # add max separately
        value = self.height * y_delta + ymin
        if self.y_ticks_fkt:
            value = self.y_ticks_fkt(value, value + y_delta)
        res += [self._in_fmt.fmt(value, abs(ymax - ymin), chars=10) + ' |']

        ylbl = '({})'.format(label)
        ylbl_left = (10 - len(ylbl)) // 2
        ylbl_right = ylbl_left + len(ylbl) % 2

        res += [' ' * (ylbl_left) + ylbl + ' ' * (ylbl_right) + ' ^']
        return list(reversed(res))

    def _x_axis(self, xmin, xmax, label='X', with_y_axis=False):
        delta = abs(xmax - xmin)
        if isinstance(delta, timedelta):
            x_delta = mk_timedelta(timestamp(delta) / self.width)
        else:
            x_delta = delta / self.width
        starts = ['', '']
        if with_y_axis:
            starts = ['-' * 11 + '|-', ' ' * 11 + '| ']
        res = []

        res += [starts[0] + '|---------' * (self.width // 10) + '|-> (' + label + ')']
        bottom = []

        for i in range(self.width // 10 + 1):
            value = i * 10 * x_delta + xmin
            if self.x_ticks_fkt:
                value = self.x_ticks_fkt(value, value + x_delta)
            bottom += [self._in_fmt.fmt(value, delta, left=True, chars=9)]

        res += [starts[1] + ' '.join(bottom)]
        return res

    def clear(self):
        """Remove all plots, texts and spans from the figure."""
        self._plots = []
        self._texts = []
        self._spans = []

    def plot(self, X, Y, lc=None, interp='linear', label=None, marker=None):
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
            self._plots += [Plot.create(X, Y, lc, interp, label, marker)]

    def scatter(self, X, Y, lc=None, label=None, marker=None):
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
            self._plots += [Plot.create(X, Y, lc, None, label, marker)]

    def histogram(self, X, bins=160, lc=None):
        """Compute and plot the histogram over X.

        Paramaters:
            X: List[float]     X values.
            bins: int          The number of bins to put X entries in (columns).
            lc: multiple       The line color.
        """
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Histogram.create(X, bins, lc)]

    def text(self, X, Y, texts, lc=None):
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
            self._texts += [Text.create(X, Y, texts, lc)]

    def axvline(self, x, ymin=0, ymax=1, lc=None):
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
        self._spans.append(Span.create(x, x, ymin, ymax, lc))

    def axvspan(self, xmin, xmax, ymin=0, ymax=1, lc=None):
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
        self._spans.append(Span.create(xmin, xmax, ymin, ymax, lc))

    def axhline(self, y, xmin=0, xmax=1, lc=None):
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
        self._spans.append(Span.create(xmin, xmax, y, y, lc))

    def axhspan(self, ymin, ymax, xmin=0, xmax=1, lc=None):
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
        self._spans.append(Span.create(xmin, xmax, ymin, ymax, lc))

    def show(self, legend=False):
        """Compute the plot.

        Parameters:
            legend: bool   Add the legend? default: False

        Returns:
            plot: str
        """
        xmin, xmax = self.x_limits()
        ymin, ymax = self.y_limits()
        if all(isinstance(p, Histogram) for p in self._plots):
            ymin = 0
        # create canvas
        canvas = Canvas(self.width, self.height,
                        self._in_fmt.convert(xmin), self._in_fmt.convert(ymin),
                        self._in_fmt.convert(xmax), self._in_fmt.convert(ymax),
                        self.background, self.color_mode)

        for s in self._spans:
            s.write(canvas, self.with_colors)

        plot_origin = False
        for p in self._plots:
            p.write(canvas, self.with_colors, self._in_fmt)
            if isinstance(p, Plot):
                plot_origin = True

        for t in self._texts:
            t.write(canvas, self.with_colors, self._in_fmt)

        if self.origin and plot_origin:
            # print X / Y origin axis
            canvas.line(self._in_fmt.convert(xmin), 0, self._in_fmt.convert(xmax), 0)
            canvas.line(0, self._in_fmt.convert(ymin), 0, self._in_fmt.convert(ymax))

        res = canvas.plot(linesep=self.linesep)

        # add y axis
        yaxis = self._y_axis(ymin, ymax, label=self.y_label)
        res = (
            yaxis[0] + self.linesep  # up arrow
            + yaxis[1] + self.linesep  # maximum
            + self.linesep.join(lbl + line for lbl, line in zip(yaxis[2:], res.split(self.linesep)))
        )

        # add x axis
        xaxis = self._x_axis(xmin, xmax, label=self.x_label, with_y_axis=True)
        res = (
            res + self.linesep  # plot
            + self.linesep.join(xaxis)
        )

        if legend:
            res += '\n\nLegend:\n-------\n'
            lines = []
            for i, p in enumerate(self._plots):
                if isinstance(p, Plot):
                    lbl = p.label or 'Label {}'.format(i)
                    marker = p.marker or ''
                    lines += [
                        color(
                            '⠤{}⠤ {}'.format(marker, lbl),
                            fg=p.lc,
                            mode=self.color_mode,
                            no_color=not self.with_colors,
                        ),
                    ]
            res += '\n'.join(lines)
        return res


class Plot:
    def __init__(self, X, Y, lc, interp, label, marker):
        self._X = X
        self._Y = Y
        self._lc = lc
        self._interp = interp
        self._label = label
        self._marker = marker

    @property
    def X(self):  # noqa: N802
        return self._X

    @property
    def Y(self):  # noqa: N802
        return self._Y

    @property
    def lc(self):
        return self._lc

    @property
    def interp(self):
        return self._interp

    @property
    def label(self):
        return self._label

    @property
    def marker(self):
        return self._marker

    @classmethod
    def create(cls, X, Y, lc, interp, label, marker):
        if len(X) != len(Y):
            raise ValueError('X and Y dim have to be the same.')
        if interp not in ('linear', None):
            raise ValueError('Only "linear" and None are allowed values for `interp`.')

        return cls(X, Y, lc, interp, label, marker)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.Y

    def write(self, canvas, with_colors, in_fmt):
        # make point iterators
        from_points = zip(map(in_fmt.convert, self.X), map(in_fmt.convert, self.Y))
        to_points = zip(map(in_fmt.convert, self.X), map(in_fmt.convert, self.Y))

        # remove first point of to_points
        (x0, y0) = next(to_points)

        color = self.lc if with_colors else None

        # print first point
        canvas.point(x0, y0, color=color, marker=self.marker)

        # plot other points and lines
        for (x0, y0), (x, y) in zip(from_points, to_points):
            canvas.point(x, y, color=color, marker=self.marker)
            if self.interp == 'linear':
                # no marker for interpolated values
                canvas.line(x0, y0, x, y, color=color)


class Histogram:
    def __init__(self, X, bins, frequencies, buckets, lc):
        self._X = X
        self._bins = bins
        self._frequencies = frequencies
        self._buckets = buckets
        self._lc = lc

    @property
    def X(self):  # noqa: N802
        return self._X

    @property
    def bins(self):
        return self._bins

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def buckets(self):
        return self._buckets

    @property
    def lc(self):
        return self._lc

    @classmethod
    def create(cls, X, bins, lc):
        frequencies, buckets = hist(X, bins)

        return cls(X, bins, frequencies, buckets, lc)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.frequencies

    def write(self, canvas, with_colors, in_fmt):
        # how fat will one bar of the histogram be
        x_diff = (canvas.dots_between(in_fmt.convert(self.buckets[0]), 0,
                                      in_fmt.convert(self.buckets[1]), 0)[0] or 1)
        bin_size = (in_fmt.convert(self.buckets[1]) - in_fmt.convert(self.buckets[0])) / x_diff

        color = self.lc if with_colors else None
        for i in range(self.bins):
            # for each bucket
            if self.frequencies[i] > 0:
                for j in range(x_diff):
                    # print bar
                    x_ = in_fmt.convert(self.buckets[i]) + j * bin_size

                    if canvas.xmin <= x_ <= canvas.xmax:
                        canvas.line(x_, 0,
                                    x_, self.frequencies[i],
                                    color=color)


class Text:
    def __init__(self, X, Y, texts, lc):
        self._X = X
        self._Y = Y
        self._texts = texts
        self._lc = lc

    @property
    def X(self):  # noqa: N802
        return self._X

    @property
    def Y(self):  # noqa: N802
        return self._Y

    @property
    def texts(self):
        return self._texts

    @property
    def lc(self):
        return self._lc

    @classmethod
    def create(cls, X, Y, texts, lc):
        if len(X) != len(Y) != len(texts):
            raise ValueError('X, Y and texts dim have to be the same.')

        return cls(X, Y, texts, lc)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.Y

    def write(self, canvas, with_colors, in_fmt):
        # make point iterator
        points = zip(map(in_fmt.convert, self.X), map(in_fmt.convert, self.Y), self.texts)

        color = self.lc if with_colors else None

        # plot texts with color
        for x, y, text in points:
            canvas.text(x, y, text, color=color)


class Span:
    def __init__(self, xmin, xmax, ymin, ymax, lc):
        assert 0 <= xmin <= xmax <= 1
        assert 0 <= ymin <= ymax <= 1
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax
        self._lc = lc

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def ymin(self):
        return self._ymin

    @property
    def ymax(self):
        return self._ymax

    @property
    def lc(self):
        return self._lc

    @classmethod
    def create(cls, xmin, xmax, ymin, ymax, lc=None):
        if not (0 <= xmin <= xmax <= 1):
            raise ValueError('xmin has to be <= xmax and both have to be within [0, 1].')
        if not (0 <= ymin <= ymax <= 1):
            raise ValueError('ymin has to be <= ymax and both have to be within [0, 1].')

        return cls(xmin, xmax, ymin, ymax, lc)

    def write(self, canvas, with_colors):
        color = self.lc if with_colors else None

        # plot texts with color
        xdelta = canvas.xmax_inside - canvas.xmin
        assert xdelta > 0

        ydelta = canvas.ymax_inside - canvas.ymin
        assert ydelta > 0

        canvas.rect(
            self.xmin * (canvas.xmin + xdelta),
            self.ymin * (canvas.ymin + ydelta),
            self.xmax * (canvas.xmin + xdelta),
            self.ymax * (canvas.ymin + ydelta),
            color=color,
        )


def _limit(values):
    _min = 0
    _max = 1
    if len(values) > 0:
        _min = min(values)
        _max = max(values)

    return (_min, _max)


def _diff(low, high):
    if low == high:
        if low == 0:
            return 0.5
        else:
            return abs(low * 0.1)
    else:
        delta = abs(high - low)
        if isinstance(delta, timedelta):
            return mk_timedelta(timestamp(delta) * 0.1)
        else:
            return delta * 0.1


def _default(low_set, high_set):
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


def _choose(low, high, low_set, high_set):
    no_data = low is None and high is None
    if no_data:
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
