# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2021 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

try:
    from PIL import Image
except ImportError:
    raise Exception('Need to have PIL / pillow installed for this example.')
try:
    import numpy as np
except ImportError:
    raise Exception('Need to have numpy installed for this example.')

from plotille import Canvas, Figure, hist, hsl
from plotille.data import circle


current_dir = os.path.dirname(os.path.abspath(__file__))
X = np.random.normal(size=10000)
width = 12
height = 10
spacer = ' '


def extend_plot_lines(lines):
    lines[0] += spacer * 20
    lines[1] += spacer * 20
    for idx in range(2, len(lines) - 2):
        lines[idx] += spacer * 7

    return lines


def int_formatter(val, chars, delta, left):
    return '{:{}{}}'.format(int(val), '<' if left else '>', chars)


def logo():
    # Canvas on its own can draw an image using dots
    img = Image.open(current_dir + '/../imgs/logo.png')
    img = img.convert('L')
    img = img.resize((270, 120))
    cvs = Canvas(135, 30, background=hsl(0, 0, 0.8), mode='rgb')
    cvs.braille_image(img.getdata(), inverse=True, color=hsl(0, 0.5, 0.4))

    indent = ' ' * 6
    print(indent + cvs.plot().replace(os.linesep, os.linesep + indent))


def histogram():
    fig = Figure()
    fig.width = width
    fig.height = height
    fig.color_mode = 'rgb'
    fig.register_label_formatter(float, int_formatter)

    fig.histogram(X, lc=hsl(17, 1, 0.8))

    lines = extend_plot_lines(fig.show().split(os.linesep))

    return lines


def crappyhist():
    lines = hist(X, bins=12, width=12, lc=hsl(285, 1, 0.74), color_mode='rgb').split(os.linesep)

    lines[1] += spacer
    return lines


def plot():
    fig = Figure()
    fig.width = width
    fig.height = height
    fig.set_y_limits(-2, 2)
    fig.color_mode = 'rgb'
    fig.register_label_formatter(float, int_formatter)

    x1 = np.random.normal(size=10)
    fig.scatter(list(range(len(x1))), x1, lc=hsl(122, 0.55, 0.43), marker='o')
    fig.plot([0, 9], [2, 0], lc=hsl(237, 1, 0.75), marker='x')

    x2 = np.linspace(0, 9, 20)
    fig.plot(x2, 0.25 * np.sin(x2) - 1, lc=hsl(70, 1, 0.5))

    fig.text([5], [1], ['Hi'], lc=hsl(0, 0, 0.7))

    fig.axvline(1, lc=hsl(0, 1, 0.5))

    lines = extend_plot_lines(fig.show().split(os.linesep))

    return lines


def heat():
    fig = Figure()
    fig.width = width
    fig.height = height
    fig.set_y_limits(-2, 2)
    fig.set_x_limits(-2, 2)
    fig.color_mode = 'rgb'
    fig.origin = False
    fig.register_label_formatter(float, int_formatter)

    xy = circle(0, 0, 1.5)
    fig.plot(xy[0], xy[1])

    img = []
    for _ in range(height):
        img += [[None] * width]

    img[int(height / 2)][int(width / 2)] = 1

    img[int(height / 2) - 2][int(width / 2) - 1] = 0.8
    img[int(height / 2) - 2][int(width / 2)] = 0.7
    img[int(height / 2) - 1][int(width / 2) - 1] = 0.2
    img[int(height / 2)    ][int(width / 2) - 1] = 0.2  # noqa: E202
    img[int(height / 2) + 1][int(width / 2) - 1] = 0.3
    img[int(height / 2) - 1][int(width / 2) + 1] = 0.4
    img[int(height / 2)    ][int(width / 2) + 1] = 0.8  # noqa: E202
    img[int(height / 2) + 1][int(width / 2) + 1] = 0.7
    img[int(height / 2) - 1][int(width / 2)] = 0.7
    img[int(height / 2) + 1][int(width / 2)] = 0.8
    # img[int(height / 2)-1][int(width / 2)] = 1
    # img[int(height / 2)][int(width / 2)] = 1

    fig.imgshow(img, cmap='magma')

    lines = extend_plot_lines(fig.show().split(os.linesep))

    return lines


def main():
    print('\n\n')
    logo()
    print()
    for lines in zip(histogram(), plot(), heat(), crappyhist()):
        print(' '.join(lines))
    print('\n\n')


if __name__ == '__main__':
    main()
