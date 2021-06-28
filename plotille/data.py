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


def ellipse(x_center, y_center, angle=0,
            x_amplitude=1, y_amplitude=1, n=20):
    assert isinstance(n, int)
    assert isinstance(x_amplitude, (int, float))
    assert n > 0

    max_ = 2 * math.pi
    step = max_ / n
    ell_x = []
    ell_y = []
    rot_matrix = [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
    for i in range(n + 1):
        t = step * i
        x = x_amplitude * math.cos(t)
        y = y_amplitude * math.sin(t)
        # do the rotation
        x = x * rot_matrix[0][0] + y * rot_matrix[0][1]
        y = x * rot_matrix[1][0] + y * rot_matrix[1][1]

        ell_x.append(x + x_center)
        ell_y.append(y + y_center)

    return ell_x, ell_y


def circle(x_center, y_center, radius, n=20):
    return ellipse(x_center, y_center, x_amplitude=radius, y_amplitude=radius)
