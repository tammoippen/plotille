import math
from numbers import Number

import six
from six.moves import zip

from ._colors import hsl
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


class Colormap:
    """
    Baseclass for all scalar to RGBA mappings.

    Typically, Colormap instances are used to convert data values (floats)
    from the interval ``[0, 1]`` to the RGBA color that the respective
    Colormap represents. For scaling of data into the ``[0, 1]`` interval see
    `Normalize`.
    """
    def __init__(self, name, N=256):
        """
        Parameters
        ----------
        name : str
            The name of the colormap.
        N : int
            The number of rgb quantization levels.
        """
        assert N > 0
        self.name = name
        self._n = N
        self._lut = None
        self.bad = (0, 0, 0)
        self.over = None
        self.under = None

    def _init(self):
        """Generate the lookup table, ``self._lut``."""
        raise NotImplementedError('Abstract class only')

    def __call__(self, X):  # noqa: N802
        """
        Parameters
        ----------
        X : float or iterable of floats
            The data value(s) to convert to RGB.
            For floats, X should be in the interval ``[0.0, 1.0]`` to
            return the RGB values ``X*100`` percent along the Colormap line.

        Returns
        -------
        Tuple of RGB values if X is scalar, otherwise an array of
        RGB values with a shape of ``X.shape + (3, )``.
        """
        try:
            return [self._process_value(x) for x in X]
        except TypeError:
            # not iterable
            return self._process_value(X)

    def _process_value(self, x):
        if not isinstance(x, Number):
            return self.bad
        if x < 0:
            return self.under
        if x > 1:
            return self.over
        idx = round(x * (len(self._lut) - 1))
        return self._lut[idx]


class ListedColormap(Colormap):
    def __init__(self, name, colors):
        super(ListedColormap, self).__init__(name, len(colors))
        self._lut = colors


_default_colormaps = [
    # TODO: names-colormaps ?
    # TODO: byte-colormaps ?
    ListedColormap('grayscale', [(idx, idx, idx) for idx in range(256)]),
    ListedColormap('red2green', [hsl(round(120.0 / 256 * idx), 1.0, 0.5) for idx in range(256)]),
    ListedColormap('green2red', [hsl(120.0 - round(120.0 / 256 * idx), 1.0, 0.5) for idx in range(256)]),
]
_default_colormaps_by_name = {cmap.name: cmap for cmap in _default_colormaps}


class Normalize:
    """A class which, when called, linearly normalizes data into the
    ``[0.0, 1.0]`` interval.
    """
    def __init__(self, vmin, vmax, clip=False):
        """
        Parameters
        ----------
        vmin, vmax : float
            Normalize according to these values.

        clip : bool, default: False
            If ``True`` values falling outside the range ``[vmin, vmax]``,
            are mapped to 0 or 1, whichever is closer, and masked values are
            set to 1.  If ``False`` masked values remain masked.

            Clipping silently defeats the purpose of setting the over, under,
            and masked colors in a colormap, so it is likely to lead to
            surprises; therefore the default is ``clip=False``.

        Notes
        -----
        Returns 0 if ``vmin == vmax``.
        """
        assert vmin is not None
        assert vmax is not None
        assert vmin > vmax, 'minvalue must be less than or equal to maxvalue'
        self.vmin = vmin
        self.vmax = vmax
        self.clip = clip

    def __call__(self, value, clip=None):
        """
        Normalize *value* data in the ``[vmin, vmax]`` interval into the
        ``[0.0, 1.0]`` interval and return it.

        Parameters
        ----------
        value
            Data to normalize.
        clip : bool
            If ``None``, defaults to ``self.clip`` (which defaults to
            ``False``).

        Notes
        -----
        If not already initialized, ``self.vmin`` and ``self.vmax`` are
        initialized using ``self.autoscale_None(value)``.
        """
        if clip is None:
            clip = self.clip

        try:
            return [self._process_value(v, clip) for v in value]
        except TypeError:
            # not iterable
            return self._process_value(value, clip)

    def _process_value(self, value, clip):
        if self.vmin == self.vmax:
            return 0.0
        if not isinstance(value, Number):
            return value

        value *= 1.0
        if math.isnan(value) or math.isinf(value):
            if clip:
                return 1.0
            return value

        value -= self.vmin
        value /= (self.vmax - self.vmin)
        return value


class Heat:
    def __init__(self, X, cmap, norm=None):
        assert len(X)
        assert isinstance(cmap, Colormap)
        len_first = len(X[0])
        assert all(len(x) == len_first for x in X)
        self._X = X

        if isinstance(cmap, six.string_types):
            cmap = _default_colormaps_by_name[cmap]
        self.cmap = cmap

        if norm is None:
            norm = Normalize(min(X), max(X))
        self.norm = norm

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
            canvas.image(self.cmap(self.norm(flat)))
