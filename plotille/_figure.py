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

from collections import namedtuple
from itertools import cycle
import os

from six.moves import zip

from ._canvas import Canvas
from ._colors import color
from ._util import _hist

# TODO documentation!!!
# TODO tests
# TODO individuel limits


class Figure(object):
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
        self._x_limit = None
        self._y_limit = None
        self._color_mode = None
        self.linesep = os.linesep
        self.background = None
        self.x_label = 'X'
        self.y_label = 'Y'
        self._plots = list()

    @property
    def width(self):
        if self._width is not None:
            return self._width
        return 80

    @width.setter
    def width(self, value):
        assert isinstance(value, int) and value > 0
        self._width = value

    @property
    def height(self):
        if self._height is not None:
            return self._height
        return 40

    @height.setter
    def height(self, value):
        assert isinstance(value, int) and value > 0
        self._height = value

    @property
    def color_mode(self):
        if self._color_mode is not None:
            return self._color_mode
        return 'names'

    @color_mode.setter
    def color_mode(self, value):
        assert value in ('names', 'byte', 'rgb'), 'Only supports: names, byte, rgb!'
        assert self._plots == [], 'Change color mode only, when no plots are prepared.'
        self._color_mode = value

    # X limits
    @property
    def x_limits(self):
        if self._x_limit is not None:
            return self._x_limit

        if not self._plots:
            return 0.0, 1.0

        low, high = None, None
        for p in self._plots:
            _min, _max = Figure._limit(p.width_vals())
            if low is None:
                low = _min
                high = _max

            low = min(_min, low)
            high = max(_max, high)

        return low, high

    @x_limits.setter
    def x_limits(self, value):
        assert isinstance(value, (list, tuple))
        assert value[0] < value[1]
        self._x_limit = value

    # Y limits
    @property
    def y_limits(self):
        if self._y_limit is not None:
            return self._y_limit

        if not self._plots:
            return 0.0, 1.0

        low, high = None, None
        for p in self._plots:
            _min, _max = Figure._limit(p.height_vals())
            if low is None:
                low = _min
                high = _max

            low = min(_min, low)
            high = max(_max, high)

        return low, high

    @y_limits.setter
    def y_limits(self, value):
        assert isinstance(value, (list, tuple))
        assert value[0] < value[1]
        self._y_limit = value

    @staticmethod
    def _limit(values):
        _min = 0
        _max = 1
        if len(values) > 0:
            _min = min(values)
            _max = max(values)

        return (_min, _max)

    def clear(self):
        self._plots.clear()

    def plot(self, X, Y, lc=None, interp='linear', label=None):  # noqa: N803
        if lc is None:
            lc = next(self._color_seq)[self.color_mode]
        self._plots += [Plot(X, Y, lc, interp, label)]

    def scatter(self, X, Y, lc=None, label=None):  # noqa: N803
        if lc is None:
            lc = next(self._color_seq)[self.color_mode]
        self._plots += [Plot(X, Y, lc, None, label)]

    def histogram(self, X, bins=160, lc=None):  # noqa: N803
        if lc is None:
            lc = next(Figure._COLOR_SEQ)[self.color_mode]
        self._plots += [Histogram(X, bins, lc)]

    def show(self, legend=False):
        xmin, xmax = self.x_limits
        ymin, ymax = self.y_limits
        # create canvas
        canvas = Canvas(self.width, self.height,
                        xmin, ymin, xmax, ymax,
                        self.background, self.color_mode)

        plot_origin = False
        for p in self._plots:
            p.write(canvas)
            if isinstance(p, Plot):
                plot_origin = True

        if plot_origin:
            # print X / Y origin axis
            canvas.line(xmin, 0, xmax, 0)
            canvas.line(0, ymin, 0, ymax)

        plt = canvas.plot(x_axis=True, x_label=self.x_label, y_axis=True,
                          y_label=self.y_label, linesep=self.linesep)

        if legend:
            plt += '\n\nLegend:\n-------\n'
            plt += '\n'.join([
                color('⠤⠤ {}'.format(p.label if p.label is not None
                                     else 'Label {}'.format(i)),
                      fg=p.lc, mode=self.color_mode)
                for i, p in enumerate(self._plots)
                if isinstance(p, Plot)
            ])
        return plt


class Plot(namedtuple('Plot', ['X', 'Y', 'lc', 'interp', 'label'])):
    def __init__(self, *args, **kwargs):
        super(Plot, self).__init__()
        assert len(self.X) == len(self.Y)
        assert self.interp in ('linear', None)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.Y

    def write(self, canvas):
        # make point iterators
        from_points = zip(self.X, self.Y)
        to_points = zip(self.X, self.Y)
        try:
            # remove first point of to_points
            next(to_points)
        except StopIteration:
            # empty X, Y
            pass

        # plot points
        for (x0, y0), (x, y) in zip(from_points, to_points):
            canvas.point(x0, y0, color=self.lc)

            canvas.point(x, y, color=self.lc)
            if self.interp == 'linear':
                canvas.line(x0, y0, x, y, color=self.lc)


class Histogram(namedtuple('Histogram', ['X', 'bins', 'lc'])):
    def __init__(self, *args, **kwargs):
        super(Histogram, self).__init__()
        self.frequencies, self.buckets = _hist(self.X, self.bins)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.frequencies

    def write(self, canvas):
        # how fat will one bar of the histogram be
        x_diff = canvas.dots_between(self.buckets[0], 0, self.buckets[1], 0)[0] or 1
        bin_size = (self.buckets[1] - self.buckets[0]) / x_diff

        for i in range(self.bins):
            # for each bucket
            if self.frequencies[i] > 0:
                for j in range(x_diff):
                    # print bar
                    x_ = self.buckets[i] + j * bin_size

                    if canvas.xmin <= x_ <= canvas.xmax:
                        canvas.line(x_, 0,
                                    x_, self.frequencies[i],
                                    color=self.lc)
