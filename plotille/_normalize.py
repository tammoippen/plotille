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

import math
from numbers import Number


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
        assert vmin <= vmax, 'minvalue must be less than or equal to maxvalue'
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
