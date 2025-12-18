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

import os

import numpy as np

import plotille as plt

# Compare with issue https://github.com/tammoippen/plotille/issues/38


def main():
    x = np.linspace(0, 1, 100)
    rows = 5
    columns = 40

    y = 2 * x
    plot1 = plt.plot(
        x,
        y,
        lc="red",
        height=rows,
        width=columns,
        X_label="x",
        Y_label="T",
        x_min=0,
        x_max=1,
        y_min=np.min(y),
        y_max=np.max(y),
    )

    y = np.exp(-x)
    plot2 = plt.plot(
        x,
        y,
        lc="green",
        height=rows,
        width=columns,
        X_label="t",
        Y_label="T",
        x_min=0,
        x_max=1,
        y_min=np.min(y),
        y_max=np.max(y),
    )

    print(plot1)
    print(plot2)
    print()

    lines = plot1.split(os.linesep)
    # last line is actually visually longest
    max_line = len(lines[-1])

    # Arrow up
    lines[0] += " " * (max_line - len(lines[0])) + "| "
    # max value line
    lines[1] += " " * (max_line - len(lines[1])) + "| "
    # canvas
    # y-axis takes up 13 characters
    for row_idx in range(rows):
        lines[2 + row_idx] += " " * (max_line - 13 - columns) + "| "
    # x-axis
    lines[-2] += " " * (max_line - len(lines[-2])) + "| "
    lines[-1] += " " * (max_line - len(lines[-1])) + "| "

    plot = (os.linesep).join(
        l1 + l2 for (l1, l2) in zip(lines, plot2.split(os.linesep), strict=True)
    )

    print(plot)


if __name__ == "__main__":
    main()
