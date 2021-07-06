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

from math import cos, pi, sin


def ellipse(x_center, y_center, angle=0,
            x_amplitude=1, y_amplitude=1, n=20):
    r"""Create X and Y values for an ellipse.

        Parameters:
            x_center: float     X-coordinate of the center of the ellipse.
            y_center: float     Y-coordinate of the center of the ellipse.
            angle: float        Rotation angle of the ellipse \in [0 .. 2pi] .
            x_amplitude: float  The radius in X-direction before rotation.
            y_amplitude: float  The radius in Y-direction before rotation.
            n: int              The number of points to return. The ellipse is
                                closed, hence the function actually return n+1 points.

        Returns:
            X, Y: Tuple[List[float], List[float]]
                The X and Y values for the ellipse.
    """
    # see https://en.wikipedia.org/wiki/Ellipse#Parametric_representation
    assert isinstance(n, int)
    assert n > 0
    assert isinstance(x_amplitude, (int, float))
    assert x_amplitude > 0
    assert isinstance(y_amplitude, (int, float))
    assert y_amplitude > 0

    max_ = 2 * pi
    step = max_ / n
    ell_x = []
    ell_y = []
    # rename just to conform to the formula in wiki.
    a = x_amplitude
    b = y_amplitude
    cos_angle = cos(angle)
    sin_angle = sin(angle)

    for i in range(n + 1):
        t = step * i
        x = a * cos_angle * cos(t) - b * sin_angle * sin(t)
        y = a * sin_angle * cos(t) + b * cos_angle * sin(t)

        ell_x.append(x + x_center)
        ell_y.append(y + y_center)

    return ell_x, ell_y


def circle(x_center, y_center, radius, n=20):
    """Create X and Y values for a circle.

       Parameters:
           x_center: float     X-coordinate of the center of the circle.
           y_center: float     Y-coordinate of the center of the circle.
           radius: float       The radius of the circle.
           n: int              The number of points to return. The circle is
                               closed, hence the function actually return n+1 points.

       Returns:
           X, Y: Tuple[List[float], List[float]]
               The X and Y values for the circle.
    """
    assert isinstance(radius, (int, float))
    assert radius > 0
    return ellipse(x_center, y_center, x_amplitude=radius, y_amplitude=radius, n=n)
