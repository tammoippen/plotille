


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

import random

import plotille


def main():
    nodes = [(0, 0), (9, 0), (0, 9), (9, 9)]
    for _ in range(10):
        nodes.append((random.randint(0, 9), random.randint(0, 9)))

    edges = []
    for _ in range(5):
        from_ = random.randint(0, len(nodes) - 1)
        to_ = random.randint(0, len(nodes) - 1)
        if from_ == to_:
            to_ = (from_ + 1) % len(nodes)
        edges.append((from_, to_))

    canvas = plotille.Canvas(width=50, height=20, xmax=10, ymax=10)

    for node in nodes:
        canvas.point(x=node[0], y=node[1], marker='x')

    for edge in edges:
        from_node = nodes[edge[0]]
        to_node = nodes[edge[1]]
        canvas.line(
            x0=from_node[0], y0=from_node[1],
            x1=to_node[0], y1=to_node[1],
        )

    print(canvas.plot())


if __name__ == '__main__':
    main()
