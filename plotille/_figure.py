# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2022 Tammo Ippen, tammo.ippen@posteo.de

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

from ._canvas import Canvas
from ._colors import color, rgb2byte
from ._figure_data import Heat, Histogram, Plot, Span, Text
from ._input_formatter import InputFormatter
from ._util import mk_timedelta, timestamp

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
        {'names': 'white', 'rgb': (255, 255, 255), 'byte': rgb2byte(255, 255, 255)},
        {'names': 'red', 'rgb': (255, 0, 0), 'byte': rgb2byte(255, 0, 0)},
        {'names': 'green', 'rgb': (0, 255, 0), 'byte': rgb2byte(0, 255, 0)},
        {'names': 'yellow', 'rgb': (255, 255, 0), 'byte': rgb2byte(255, 255, 0)},
        {'names': 'blue', 'rgb': (0, 0, 255), 'byte': rgb2byte(0, 0, 255)},
        {'names': 'magenta', 'rgb': (255, 0, 255), 'byte': rgb2byte(255, 0, 255)},
        {'names': 'cyan', 'rgb': (0, 255, 255), 'byte': rgb2byte(0, 255, 255)},
    ]

    def __init__(self):
        self._color_seq = iter(cycle(Figure._COLOR_SEQ))
        self._width = None
        self._height = None
        self._x_min = None
        self._x_max = None
        self._y_min = None
        self._y_max = None
        self._color_kwargs = {'mode': 'names'}
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
        self._heats = []
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
        return self._color_kwargs['mode']

    @color_mode.setter
    def color_mode(self, value):
        if value not in ('names', 'byte', 'rgb'):
            raise ValueError('Only supports: names, byte, rgb!')
        if self._plots != []:
            raise RuntimeError('Change color mode only, when no plots are prepared.')
        self._color_kwargs['mode'] = value

    @property
    def color_full_reset(self):
        return self._color_kwargs.get('full_reset', True)

    @color_full_reset.setter
    def color_full_reset(self, value):
        if not isinstance(value, bool):
            raise ValueError('Only supports bool.')
        self._color_kwargs['full_reset'] = value

    @property
    def with_colors(self):
        """Whether to plot with or without color."""
        return self._with_colors

    @with_colors.setter
    def with_colors(self, value):
        if not isinstance(value, bool):
            raise ValueError('Only bool allowed: "{}"'.format(value))
        self._with_colors = value

    @property
    def origin(self):
        """Show or not show the origin in the plot."""
        return self._origin

    @origin.setter
    def origin(self, value):
        if not isinstance(value, bool):
            raise ValueError('Invalid origin: {}'.format(value))
        self._origin = value

    def register_label_formatter(self, type_, formatter):
        """Register a formatter for labels of a certain type.

        See `plotille._input_formatter` for examples.

        Parameters
        ----------
        type_
            A python typte, that can be used for isinstance tests.
        formatter: (val: type_, chars: int, delta, left: bool = False) -> str
            Function that formats `val` into a string.
            chars: int => number of chars you should fill
            delta      => the difference between the smallest and largest X/Y value
            left: bool => align left or right.
        """
        self._in_fmt.register_formatter(type_, formatter)

    def register_float_converter(self, type_, converter):
        """Register a converter from some type_ to float.

        See `plotille._input_formatter` for examples.

        Parameters
        ----------
        type_
            A python type, that can be used for isinstance tests.
        formatter: (val: type_) -> float
            Function that formats `val` into a float.
        """
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

        res += [
            starts[0]
            + '|---------' * (self.width // 10)
            + '|'
            + '-' * (self.width % 10)
            + '-> (' + label + ')',
        ]
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
        self._heats = []

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
            self._plots += [Plot(X, Y, lc, interp, label, marker)]

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
            self._plots += [Plot(X, Y, lc, None, label, marker)]

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
            self._plots += [Histogram(X, bins, lc)]

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
            self._texts += [Text(X, Y, texts, lc)]

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
        self._spans.append(Span(x, x, ymin, ymax, lc))

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
        self._spans.append(Span(xmin, xmax, ymin, ymax, lc))

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
        self._spans.append(Span(xmin, xmax, y, y, lc))

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
        self._spans.append(Span(xmin, xmax, ymin, ymax, lc))

    def imgshow(self, X, cmap=None):
        """Display data as an image, i.e., on a 2D regular raster.

        Parameters:
            X: array-like
                The image data. Supported array shapes are:
                - (M, N): an image with scalar data. The values are mapped
                        to colors using a colormap. The values have to be in
                        the 0-1 (float) range. Out of range, invalid type and
                        None values are handled by the cmap.
                - (M, N, 3): an image with RGB values (0-1 float or 0-255 int).

                The first two dimensions (M, N) define the rows and columns of the image.

            cmap: cmapstr or Colormap
                The Colormap instance or registered colormap name used
                to map scalar data to colors. This parameter is ignored
                for RGB data.
        """
        if len(X) > 0:
            self._heats += [Heat(X, cmap)]

    def show(self, legend=False):  # noqa: C901 complex (12)
        """Compute the plot.

        Parameters:
            legend: bool   Add the legend? default: False

        Returns:
            plot: str
        """
        xmin, xmax = self.x_limits()
        ymin, ymax = self.y_limits()
        if self._plots and all(isinstance(p, Histogram) for p in self._plots):
            ymin = 0

        if self._heats and self._width is None and self._height is None:
            self.height = len(self._heats[0].X)
            self.width = len(self._heats[0].X[0])

        # create canvas
        canvas = Canvas(self.width, self.height,
                        self._in_fmt.convert(xmin), self._in_fmt.convert(ymin),
                        self._in_fmt.convert(xmax), self._in_fmt.convert(ymax),
                        self.background, **self._color_kwargs)

        for s in self._spans:
            s.write(canvas, self.with_colors)

        plot_origin = False
        for p in self._plots:
            p.write(canvas, self.with_colors, self._in_fmt)
            if isinstance(p, Plot):
                plot_origin = True

        for t in self._texts:
            t.write(canvas, self.with_colors, self._in_fmt)

        for h in self._heats:
            h.write(canvas)

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
            res += '{0}{0}Legend:{0}-------{0}'.format(self.linesep)
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
            res += self.linesep.join(lines)
        return res


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
