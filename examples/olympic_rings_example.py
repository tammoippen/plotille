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

import plotille
import plotille.data as plt_data

# The module plotille.data contains helper functions for creating interesting
# data. At the moment you can create ellipsis and circles.


def main():
    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    # the olympic rings
    fig.set_x_limits(min_=0, max_=600)
    fig.set_y_limits(min_=0, max_=500)

    centers = []
    centers.append([250, 200, "blue"])
    centers.append([375, 200, "white"])
    centers.append([500, 200, "red"])
    centers.append([310, 250, "yellow"])
    centers.append([435, 250, "green"])
    for ring in centers:
        X, Y = plt_data.circle(x_center=ring[0], y_center=500 - ring[1], radius=50)
        fig.plot(X, Y, lc=ring[2])

    print(fig.show(legend=False))


if __name__ == "__main__":
    main()
