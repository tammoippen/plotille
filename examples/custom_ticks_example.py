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

from functools import partial

import plotille as plt

# Custom X and Y ticks
#
# You can customize the displayed tick values on the corresponding axis
# by providing callback functions for each.


def default_y_tick(min_, max_):
    # the default behaviour is to show the minimum
    # of the Y-tick range.
    return min_


def mean_y_value(Y, min_, max_):
    ys = [y for y in Y if min_ <= y < max_]
    if ys:
        # if there are some Y values in that range
        # show the average
        return sum(ys) / len(ys)
    else:
        # default is showing the lower end of the range
        return min_


def str_tick(min_, max_):
    return f"{min_ + (max_ - min_) / 2:.3f}"


def main():
    Y = [0, 10, 20, 20, 21, 25, 30, 32, 40, 44, 50] + [51.3] * 10
    X = list(range(len(Y)))

    fig = plt.Figure()
    fig.plot(X, Y)
    fig.set_x_limits(min_=0)
    fig.set_y_limits(min_=0)

    # provide a callback, which is called for every
    # Y-tick. The signature has to conform to `default_y_tick`.
    fig.y_ticks_fkt = default_y_tick
    print(fig.show())

    # to work on the actual data, capture it via
    # lambda or partial
    fig.y_ticks_fkt = partial(mean_y_value, Y)
    print(fig.show())

    # you can also just provide the string data
    fig.y_ticks_fkt = str_tick
    print(fig.show())

    # the same works for the x-ticks
    fig.x_ticks_fkt = str_tick
    print(fig.show())


if __name__ == "__main__":
    main()
