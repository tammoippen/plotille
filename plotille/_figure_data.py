# The MIT License

# Copyright (c) 2017 - 2024 Tammo Ippen, tammo.ippen@posteo.de

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

from collections.abc import Sequence
from typing import Literal, final

from plotille._canvas import Canvas
from plotille._colors import ColorDefinition
from plotille._data_metadata import DataMetadata
from plotille._input_formatter import InputFormatter

from . import Colormap, _cmaps
from ._util import DataValues, hist


class Plot:
    def __init__(
        self,
        X: DataValues,
        Y: DataValues,
        lc: ColorDefinition,
        interp: Literal["linear"] | None,
        label: str | None,
        marker: str | None,
        formatter: InputFormatter | None = None,
    ) -> None:
        if len(X) != len(Y):
            raise ValueError("X and Y dim have to be the same.")
        if interp not in ("linear", None):
            raise ValueError('Only "linear" and None are allowed values for `interp`.')

        self._formatter = formatter if formatter is not None else InputFormatter()
        self.X_metadata = DataMetadata.from_sequence(X)
        self.Y_metadata = DataMetadata.from_sequence(Y)
        self.X = [self._formatter.convert(x) for x in X]
        self.Y = [self._formatter.convert(y) for y in Y]

        self.lc = lc
        self.interp = interp
        self.label = label
        self.marker = marker

    def width_vals(self) -> list[float]:
        """Return X values as floats for limit calculation."""
        return self.X

    def height_vals(self) -> list[float]:
        """Return Y values as floats for limit calculation."""
        return self.Y

    def write(self, canvas: Canvas, with_colors: bool, in_fmt: InputFormatter) -> None:
        from_points = zip(self.X, self.Y, strict=True)
        to_points = zip(self.X, self.Y, strict=True)

        # remove first point of to_points
        (x0, y0) = next(to_points)

        color = self.lc if with_colors else None

        # print first point
        canvas.point(x0, y0, color=color, marker=self.marker)

        # plot other points and lines
        for (x0, y0), (x, y) in zip(from_points, to_points, strict=False):
            canvas.point(x, y, color=color, marker=self.marker)
            if self.interp == "linear":
                # no marker for interpolated values
                canvas.line(x0, y0, x, y, color=color)


@final
class Histogram:
    def __init__(self, X: DataValues, bins: int, lc: ColorDefinition) -> None:
        frequencies, buckets = hist(X, bins)
        self.X = X
        self.bins = bins
        self.frequencies = frequencies
        self.buckets = buckets
        self.lc = lc

    def width_vals(self) -> DataValues:
        return self.X

    def height_vals(self) -> list[int]:
        return self.frequencies

    def write(self, canvas: Canvas, with_colors: bool, in_fmt: InputFormatter) -> None:
        # how fat will one bar of the histogram be
        x_diff = (
            canvas.dots_between(
                in_fmt.convert(self.buckets[0]), 0, in_fmt.convert(self.buckets[1]), 0
            )[0]
            or 1
        )
        bin_size = (
            in_fmt.convert(self.buckets[1]) - in_fmt.convert(self.buckets[0])
        ) / x_diff

        color = self.lc if with_colors else None
        for i in range(self.bins):
            # for each bucket
            if self.frequencies[i] > 0:
                for j in range(x_diff):
                    # print bar
                    x_ = in_fmt.convert(self.buckets[i]) + j * bin_size

                    if canvas.xmin <= x_ <= canvas.xmax:
                        canvas.line(x_, 0, x_, self.frequencies[i], color=color)


@final
class Text:
    def __init__(
        self,
        X: DataValues,
        Y: DataValues,
        texts: Sequence[str],
        lc: ColorDefinition,
        formatter: InputFormatter | None = None,
    ) -> None:
        if len(X) != len(Y) != len(texts):
            raise ValueError("X, Y and texts dim have to be the same.")

        self._formatter = formatter if formatter is not None else InputFormatter()
        self.X_metadata = DataMetadata.from_sequence(X)
        self.Y_metadata = DataMetadata.from_sequence(Y)
        self.X = [self._formatter.convert(x) for x in X]
        self.Y = [self._formatter.convert(y) for y in Y]
        self.texts = texts
        self.lc = lc

    def width_vals(self) -> list[float]:
        """Return X values as floats for limit calculation."""
        return self.X

    def height_vals(self) -> list[float]:
        """Return Y values as floats for limit calculation."""
        return self.Y

    def write(self, canvas: Canvas, with_colors: bool, in_fmt: InputFormatter) -> None:
        points = zip(self.X, self.Y, self.texts, strict=True)

        color = self.lc if with_colors else None

        # plot texts with color
        for x, y, text in points:
            canvas.text(x, y, text, color=color)


class Span:
    def __init__(
        self,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        lc: ColorDefinition | None = None,
    ):
        if not (0 <= xmin <= xmax <= 1):
            raise ValueError(
                "xmin has to be <= xmax and both have to be within [0, 1]."
            )
        if not (0 <= ymin <= ymax <= 1):
            raise ValueError(
                "ymin has to be <= ymax and both have to be within [0, 1]."
            )
        self.xmin: float = xmin
        self.xmax: float = xmax
        self.ymin: float = ymin
        self.ymax: float = ymax
        self.lc: ColorDefinition | None = lc

    def write(self, canvas: Canvas, with_colors: bool) -> None:
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


HeatInput = Sequence[Sequence[float]] | Sequence[Sequence[Sequence[float]]]


@final
class Heat:
    def __init__(self, X: HeatInput, cmap: str | Colormap | None = None):
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
        self._X: HeatInput = X

        if cmap is None:
            cmap = "viridis"

        if isinstance(cmap, str):
            cmap = _cmaps.cmaps[cmap]()
        self.cmap = cmap

    @property
    def X(self) -> HeatInput:
        return self._X

    def write(self, canvas: Canvas) -> None:
        assert len(self.X)
        assert canvas.height == len(self.X)
        assert canvas.width == len(self.X[0])

        flat = [x for xs in self.X for x in xs]
        try:
            assert all(len(pixel) == 3 for pixel in flat)  # type: ignore[arg-type]
            # assume rgb
            if all(
                isinstance(v, float) and 0 <= v <= 1
                for pixel in flat
                for v in pixel  # type: ignore[union-attr]
            ):
                # 0 - 1 values => make 0-255 int values
                flat = [  # type: ignore[misc]
                    (round(r * 255), round(g * 255), round(b * 255)) for r, g, b in flat
                ]
            canvas.image(flat)  # type: ignore[arg-type]
        except TypeError:
            # cannot call len on a float
            canvas.image(self.cmap(flat))  # type: ignore[arg-type]
