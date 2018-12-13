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

from os import linesep

import six

from ._dots import Dots
from ._util import roundeven


class Canvas(object):
    """A canvas object for plotting braille dots

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
    """
    def __init__(self, width, height, xmin=0, ymin=0, xmax=1, ymax=1, background=None, color_mode='names'):
        """Initiate a Canvas object

        Parameters:
            width: int            The number of characters for the width (columns) of the canvas.
            hight: int            The number of characters for the hight (rows) of the canvas.
            xmin, ymin: float     Lower left corner of reference system.
            xmax, ymax: float     Upper right corner of reference system.
            background: multiple  Background color of the canvas.
            color_mode: str       The color-mode for all colors of this canvas; either 'names' (default)
                                  'rgb' or 'byte'. See `plotille.color()`.

        Returns:
            Canvas object
        """
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
        self._canvas = [[Dots(bg=background, color_mode=color_mode) for j_ in range(width)] for i_ in range(height)]

    def __str__(self):
        return 'Canvas(width={}, height={}, xmin={}, ymin={}, xmax={}, ymax={})'.format(
            self.width, self.height, self.xmin, self.ymin, self.xmax, self.ymax,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def width(self):
        """Number of characters in X direction"""
        return self._width

    @property
    def height(self):
        """Number of characters in Y direction"""
        return self._height

    @property
    def xmin(self):
        """Get xmin coordinate of reference coordinate system."""
        return self._xmin

    @property
    def ymin(self):
        """Get ymin coordinate of reference coordinate system."""
        return self._ymin

    @property
    def xmax(self):
        """Get xmax coordinate of reference coordinate system."""
        return self._xmax

    @property
    def ymax(self):
        """Get ymax coordinate of reference coordinate system."""
        return self._ymax

    def _transform_x(self, x):
        return int(roundeven((x - self.xmin) / self._x_delta_pt))

    def _transform_y(self, y):
        return int(roundeven((y - self.ymin) / self._y_delta_pt))

    def _set(self, x_idx, y_idx, set_=True, color=None):
        """Put a dot into the canvas at (x_idx, y_idx) [canvas coordinate system]

        Parameters:
            x: int           x-coordinate on canvas.
            y: int           y-coordinate on canvas.
            set_: bool       Whether to plot or remove the point.
            color: multiple  Color of the point.
        """
        x_c, x_p = x_idx // 2, x_idx % 2
        y_c, y_p = y_idx // 4, y_idx % 4

        if 0 <= x_c < self.width and 0 <= y_c < self.height:
            self._canvas[y_c][x_c].update(x_p, y_p, set_)
            if color:
                self._canvas[y_c][x_c].fg = color

    def dots_between(self, x0, y0, x1, y1):
        """Number of dots between (x0, y0) and (x1, y1).

        Parameters:
            x0, y0: float  Point 0
            x1, y1: float  Point 1

        Returns:
            (int, int): dots in (x, y) direction
        """
        x0_idx = self._transform_x(x0)
        y0_idx = self._transform_y(y0)
        x1_idx = self._transform_x(x1)
        y1_idx = self._transform_y(y1)

        return x1_idx - x0_idx, y1_idx - y0_idx

    def point(self, x, y, set_=True, color=None):
        """Put a point into the canvas at (x, y) [reference coordinate system]

        Parameters:
            x: float         x-coordinate on reference system.
            y: float         y-coordinate on reference system.
            set_: bool       Whether to plot or remove the point.
            color: multiple  Color of the point.
        """
        x_idx = self._transform_x(x)
        y_idx = self._transform_y(y)
        self._set(x_idx, y_idx, set_, color)

    def fill_char(self, x, y, set_=True):
        """Fill the complete character at the point (x, y) [reference coordinate system]

        Parameters:
            x: float    x-coordinate on reference system.
            y: float    y-coordinate on reference system.
            set_: bool  Whether to plot or remove the point.
        """
        x_idx = self._transform_x(x)
        y_idx = self._transform_y(y)

        x_c = x_idx // 2
        y_c = y_idx // 4

        if set_:
            self._canvas[y_c][x_c].fill()
        else:
            self._canvas[y_c][x_c].clear()

    def line(self, x0, y0, x1, y1, set_=True, color=None):
        """Plot line between point (x0, y0) and (x1, y1) [reference coordinate system].

        Parameters:
            x0, y0: float    Point 0
            x1, y1: float    Point 1
            set_: bool       Whether to plot or remove the line.
            color: multiple  Color of the line.
        """
        x0_idx = self._transform_x(x0)
        y0_idx = self._transform_y(y0)
        self._set(x0_idx, y0_idx, set_, color)

        x1_idx = self._transform_x(x1)
        y1_idx = self._transform_y(y1)
        self._set(x1_idx, y1_idx, set_, color)

        x_diff = x1_idx - x0_idx
        y_diff = y1_idx - y0_idx
        steps = max(abs(x_diff), abs(y_diff))
        for i in range(1, steps):
            xb = x0_idx + int(roundeven(x_diff / steps * i))
            yb = y0_idx + int(roundeven(y_diff / steps * i))
            self._set(xb, yb, set_, color)

    def rect(self, xmin, ymin, xmax, ymax, set_=True, color=None):
        """Plot rectangle with bbox (xmin, ymin) and (xmax, ymax) [reference coordinate system].

        Parameters:
            xmin, ymin: float  Lower left corner of rectangle.
            xmax, ymax: float  Upper right corner of rectangle.
            set_: bool         Whether to plot or remove the rect.
            color: multiple    Color of the rect.
        """
        assert xmin <= xmax
        assert ymin <= ymax
        self.line(xmin, ymin, xmin, ymax, set_, color)
        self.line(xmin, ymax, xmax, ymax, set_, color)
        self.line(xmax, ymax, xmax, ymin, set_, color)
        self.line(xmax, ymin, xmin, ymin, set_, color)

    def plot(self, linesep=linesep):
        """Transform canvas into `print`-able string

        Parameters:
            linesep: str  The requested line seperator. default: os.linesep

        Returns:
            unicode: The canvas as a string.
        """

        return linesep.join(''.join(map(six.text_type, row))
                            for row in reversed(self._canvas))
