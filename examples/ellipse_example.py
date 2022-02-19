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

import plotille
import plotille.data as plt_data

# The module plotille.data contains helper functions for creating interesting
# data. At the moment you can create ellipsis and circles.


def main():
    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    X1, Y1 = plt_data.ellipse(x_center=0, y_center=0, x_amplitude=0.5, y_amplitude=0.5, n=20)  # noqa: N806
    fig.plot(X1, Y1)

    print(fig.show(legend=True))

    # first set
    X2, Y2 = plt_data.ellipse(x_center=0, y_center=0)  # noqa: N806
    fig.plot(X2, Y2)

    X3, Y3 = plt_data.ellipse(x_center=0, y_center=0, x_amplitude=0.5, y_amplitude=0.5, n=20)  # noqa: N806
    fig.plot(X3, Y3, label='Ellipse 2')

    print(fig.show(legend=True))

    # second set, offset
    fig.clear()
    X2, Y2 = plt_data.ellipse(x_center=0, y_center=0)  # noqa: N806
    fig.plot(X2, Y2)
    fig.set_x_limits(min_=-10, max_=10)
    fig.set_y_limits(min_=-10, max_=10)

    for xx in [-4, 0, 4]:
        for yy in [-4, 0, 4]:
            X, Y = plt_data.ellipse(x_center=xx, y_center=yy, x_amplitude=1, y_amplitude=1, n=20)  # noqa: N806
            fig.plot(X, Y, label=('{},{}'.format(xx, yy)))

    fig.scatter([4], [4])

    print(fig.show(legend=True))


if __name__ == '__main__':
    main()
