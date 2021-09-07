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

from numbers import Number

from . import _cmaps_data


class Colormap:
    """
    Baseclass for all scalar to RGB mappings.

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


cmaps = {}
for (name, data) in (
    ('magma', _cmaps_data.magma_data),
    ('inferno', _cmaps_data.inferno_data),
    ('plasma', _cmaps_data.plasma_data),
    ('viridis', _cmaps_data.viridis_data),
    ('jet', _cmaps_data.jet_data),
    ('copper', _cmaps_data.copper_data),
):
    cmaps[name] = ListedColormap(
        colors=[(round(255 * r), round(255 * g), round(255 * b))for r, g, b in data], name=name,
    )

cmaps['gray'] = ListedColormap(
    name='gray', colors=[(idx, idx, idx) for idx in range(256)],
)

# for more, have a look at https://matplotlib.org/stable/tutorials/colors/colormaps.html
