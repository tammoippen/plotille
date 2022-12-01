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

from . import _cmaps
from ._util import hist


class Plot:
    def __init__(self, X, Y, lc, interp, label, marker):
        if len(X) != len(Y):
            raise ValueError('X and Y dim have to be the same.')
        if interp not in ('linear', None):
            raise ValueError('Only "linear" and None are allowed values for `interp`.')

        self.X = X
        self.Y = Y
        self.lc = lc
        self.interp = interp
        self.label = label
        self.marker = marker

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
    def __init__(self, X, bins, lc):
        frequencies, buckets = hist(X, bins)
        self.X = X
        self.bins = bins
        self.frequencies = frequencies
        self.buckets = buckets
        self.lc = lc

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
        if len(X) != len(Y) != len(texts):
            raise ValueError('X, Y and texts dim have to be the same.')

        self.X = X
        self.Y = Y
        self.texts = texts
        self.lc = lc

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
    def __init__(self, xmin, xmax, ymin, ymax, lc=None):
        if not (0 <= xmin <= xmax <= 1):
            raise ValueError('xmin has to be <= xmax and both have to be within [0, 1].')
        if not (0 <= ymin <= ymax <= 1):
            raise ValueError('ymin has to be <= ymax and both have to be within [0, 1].')
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.lc = lc

    def write(self, canvas, with_colors):
        color = self.lc if with_colors else None

        # plot texts with color
        xdelta = canvas.xmax_inside - canvas.xmin
        assert xdelta > 0

        ydelta = canvas.ymax_inside - canvas.ymin
        assert ydelta > 0

        canvas.rect(
            canvas.xmin + self.xmin * xdelta,
            canvas.ymin + self.ymin * ydelta,
            canvas.xmin + self.xmax * xdelta,
            canvas.ymin + self.ymax * ydelta,
            color=color,
        )


class Heat:
    def __init__(self, X, cmap=None):
        """Initialize a Heat-class.

        Parameters
        ----------
        X: array-like
            The image data. Supported array shapes are:
            - (M, N): an image with scalar data. The values are mapped
                      to colors using a colormap. The values have to be in
                      the 0-1 (float) range. Out of range, invalid type and
                      None values are handled by the cmap.
            - (M, N, 3): an image with RGB values (0-1 float or 0-255 int).

            The first two dimensions (M, N) define the rows and columns of the image.

        cmap: cmapstr or Colormap, default: 'viridis'
            The Colormap instance or registered colormap name used
            to map scalar data to colors. This parameter is ignored
            for RGB data.
        """
        assert len(X)
        assert cmap is None or isinstance(cmap, (str, _cmaps.Colormap))
        len_first = len(X[0])
        assert all(len(x) == len_first for x in X)
        self._X = X

        if cmap is None:
            cmap = 'viridis'

        if isinstance(cmap, str):
            cmap = _cmaps.cmaps[cmap]()
        self.cmap = cmap

    @property
    def X(self):  # noqa: N802
        return self._X

    def write(self, canvas):
        assert len(self.X)
        assert canvas.height == len(self.X)
        assert canvas.width == len(self.X[0])

        flat = [x for xs in self.X for x in xs]
        try:
            assert all(len(pixel) == 3 for pixel in flat)
            # assume rgb
            if all(0 <= v <= 1 for pixel in flat for v in pixel):
                # 0 - 1 values => make 0-255 int values
                flat = [(round(r * 255), round(g * 255), round(b * 255))
                        for r, g, b in flat]
            canvas.image(flat)
        except TypeError:
            # cannot call len on a float
            canvas.image(self.cmap(flat))
