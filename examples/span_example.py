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

import plotille


def cross_at_the_center():
    fig = plotille.Figure()
    fig.set_x_limits(0, 100)
    fig.set_y_limits(0, 100)
    fig.width = 40
    fig.height = 20

    # print a horizontal line in the middle
    fig.axhline(0.5)
    # print a vertical line in the middle
    fig.axvline(0.5)

    print(fig.show())


def boxes():
    fig = plotille.Figure()
    fig.set_x_limits(0, 100)
    fig.set_y_limits(0, 100)
    fig.width = 40
    fig.height = 20

    # print a horizontal box from 20% - 30% height of the frame
    fig.axhspan(0.2, 0.3)
    # print a vertical box from 50% - 80% width of the frame
    fig.axvspan(0.5, 0.8)
    # a box right at the center
    fig.axvspan(0.4, 0.6, 0.4, 0.6)
    # same as above
    # fig.axhspan(0.4, 0.6, 0.4, 0.6)

    print(fig.show())


def main():
    cross_at_the_center()
    boxes()


if __name__ == '__main__':
    main()
