from numbers import Number

from six.moves import zip

from ._colors import hsl
from ._util import hist


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
            canvas.xmin + self.xmin * xdelta,
            canvas.ymin + self.ymin * ydelta,
            canvas.xmin + self.xmax * xdelta,
            canvas.ymin + self.ymax * ydelta,
            color=color,
        )


class Heat:
    def __init__(self, X, cmap):
        assert len(X)
        assert isinstance(cmap, Colormap)
        len_first = len(X[0])
        assert all(len(x) == len_first for x in X)
        self._X = X
        self.cmap = cmap

    @property
    def X(self):  # noqa: N802
        return self._X

    def write(self, canvas, with_colors, in_fmt):
        assert len(self.X)
        assert canvas.height == len(self.X)
        assert canvas.width == len(self.X[0])

        flat = [x for xs in self.X for x in xs]
        if all(len(pixel) == 3 for pixel in flat):
            # assume rgb
            if all(0 <= v <= 1 for pixel in flat for v in pixel):
                # 0 - 1 values => make 0-255 int values
                flat = [(round(r * 255), round(g * 255), round(b * 255))
                        for r, g, b in flat]
            canvas.image(flat)
        else:
            canvas.image(self.cmap(flat))


class Colormap:
    def __init__(self, name, N=256):
        assert N > 0
        self.name = name
        # red to green
        self.colors = [hsl(120 / N * i, 1.0, 0.5) for i in range(N)]
        self.bad = hsl(0, 0, 0)
        self.over = hsl(0, 0, 1)
        self.under = hsl(0, 0, 1)

    def __call__(self, X):  # noqa: N802
        try:
            return [self._convert(x) for x in X]
        except TypeError:
            # not iterable
            return self._convert(X)

    def _convert(self, x):
        if not isinstance(x, Number):
            return self.bad
        if x < 0:
            return self.under
        if x > 1:
            return self.over
        idx = round(x * (len(self.colors) - 1))
        return self.colors[idx]
