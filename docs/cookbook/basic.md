# Basic Plots

Simple plotting examples to get started with plotille.

## __init__

Example: __init__

<div class="terminal-window interactive-example" data-example="__init__">
    <div class="terminal-header">
        <span class="terminal-title">[python3 __init__.py]</span>
        <button class="terminal-run-btn" onclick="runExample('__init__')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-__init__"></textarea>
        </div>
        <div class="terminal-output" id="output-__init__">
            <span class="terminal-prompt">root@plotille:~$ python3 __init__.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## color_example

The MIT License

<div class="terminal-window interactive-example" data-example="color_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 color_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('color_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-color_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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

from plotille import color


def main():
    print(
        color(
            "Do not print colors, if `no_color` is set to True", fg="red", no_color=True
        )
    )
    print(color("You can set a foreground", fg="red"))
    print(color("and a background.", bg="red"))
    print(color("Or both.", fg="black", bg="cyan"))

    print(color("Aside from 4-bit / name colors", fg="green", mode="names"))
    print(
        color(
            "you can also set 8-bit colors / 256-color lookup tables",
            fg=126,
            bg=87,
            mode="byte",
        )
    )
    print(
        color(
            "or go with full 24-bit rgb colors",
            fg=(50, 50, 50),
            bg=(166, 237, 240),
            mode="rgb",
        )
    )

    no_color = os.environ.get("NO_COLOR")
    os.environ["NO_COLOR"] = "1"
    print(
        color("The Environment variable `NO_COLOR` will always strip colors.", fg="red")
    )
    if no_color:
        os.environ["NO_COLOR"] = no_color
    else:
        os.environ.pop("NO_COLOR")

    force_color = os.environ.get("FORCE_COLOR")
    os.environ["FORCE_COLOR"] = "1"
    print(
        color(
            "The Environment variable `FORCE_COLOR` allows to toggle colors,", fg="blue"
        )
    )
    os.environ["FORCE_COLOR"] = "0"
    print(color("setting it to 0, none or false, strips color codes", fg="magenta"))
    os.environ["FORCE_COLOR"] = "1"
    print(color("everything else forces color codes", fg="green"))
    if force_color:
        os.environ["FORCE_COLOR"] = force_color
    else:
        os.environ.pop("FORCE_COLOR")


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-color_example">
            <span class="terminal-prompt">root@plotille:~$ python3 color_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## custom_ticks_example

The MIT License

<div class="terminal-window interactive-example" data-example="custom_ticks_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 custom_ticks_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('custom_ticks_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-custom_ticks_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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
</textarea>
        </div>
        <div class="terminal-output" id="output-custom_ticks_example">
            <span class="terminal-prompt">root@plotille:~$ python3 custom_ticks_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## ellipse_example

The MIT License

<div class="terminal-window interactive-example" data-example="ellipse_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 ellipse_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('ellipse_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-ellipse_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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

    X1, Y1 = plt_data.ellipse(
        x_center=0, y_center=0, x_amplitude=0.5, y_amplitude=0.5, n=20
    )
    fig.plot(X1, Y1)

    print(fig.show(legend=True))

    # first set
    X2, Y2 = plt_data.ellipse(x_center=0, y_center=0)
    fig.plot(X2, Y2)

    X3, Y3 = plt_data.ellipse(
        x_center=0, y_center=0, x_amplitude=0.5, y_amplitude=0.5, n=20
    )
    fig.plot(X3, Y3, label="Ellipse 2")

    print(fig.show(legend=True))

    # second set, offset
    fig.clear()
    X2, Y2 = plt_data.ellipse(x_center=0, y_center=0)
    fig.plot(X2, Y2)
    fig.set_x_limits(min_=-10, max_=10)
    fig.set_y_limits(min_=-10, max_=10)

    for xx in [-4, 0, 4]:
        for yy in [-4, 0, 4]:
            X, Y = plt_data.ellipse(
                x_center=xx, y_center=yy, x_amplitude=1, y_amplitude=1, n=20
            )
            fig.plot(X, Y, label=(f"{xx},{yy}"))

    fig.scatter([4], [4])

    print(fig.show(legend=True))


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-ellipse_example">
            <span class="terminal-prompt">root@plotille:~$ python3 ellipse_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## house_example

The MIT License

<div class="terminal-window interactive-example" data-example="house_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 house_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('house_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-house_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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

from plotille import Canvas

# The underlying canvas-implementation can be used on its own.


def main():
    c = Canvas(width=40, height=20)
    c.rect(0.1, 0.1, 0.6, 0.6)
    c.line(0.1, 0.1, 0.6, 0.6)
    c.line(0.1, 0.6, 0.6, 0.1)
    c.line(0.1, 0.6, 0.35, 0.8)
    c.line(0.35, 0.8, 0.6, 0.6)
    c.text(0.3, 0.5, "hi", color="red")
    c.point(0.35, 0.35, color="blue")
    c.fill_char(0.35, 0.1)
    print(c.plot())


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-house_example">
            <span class="terminal-prompt">root@plotille:~$ python3 house_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## network

The MIT License

<div class="terminal-window interactive-example" data-example="network">
    <div class="terminal-header">
        <span class="terminal-title">[python3 network.py]</span>
        <button class="terminal-run-btn" onclick="runExample('network')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-network"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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
        canvas.point(x=node[0], y=node[1], marker="x")

    for edge in edges:
        from_node = nodes[edge[0]]
        to_node = nodes[edge[1]]
        canvas.line(x0=from_node[0], y0=from_node[1], x1=to_node[0], y1=to_node[1])

    print(canvas.plot())


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-network">
            <span class="terminal-prompt">root@plotille:~$ python3 network.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## olympic_rings_example

The MIT License

<div class="terminal-window interactive-example" data-example="olympic_rings_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 olympic_rings_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('olympic_rings_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-olympic_rings_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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
</textarea>
        </div>
        <div class="terminal-output" id="output-olympic_rings_example">
            <span class="terminal-prompt">root@plotille:~$ python3 olympic_rings_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## performance_example

The MIT License

<div class="terminal-window interactive-example" data-example="performance_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 performance_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('performance_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-performance_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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

from random import random
from time import time

import plotille


def main():
    y = []
    for _ in range(1000):
        y.append(random())
    x = list(range(1000))

    t0 = time()
    for _ in range(100):
        plotille.plot(x, y, height=30, width=60)
    print(f"Took {time() - t0:.3f} sec")


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-performance_example">
            <span class="terminal-prompt">root@plotille:~$ python3 performance_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## scatter_cats_example

The MIT License

<div class="terminal-window interactive-example" data-example="scatter_cats_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 scatter_cats_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('scatter_cats_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-scatter_cats_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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


def main():
    draw_scene([[-36, 108], [-36, 108.2], [-35.1, 108]], [[-35.4, 108]])


def draw_scene(mouse_list, cat_list):
    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    listx = []
    listy = []
    names = []
    for idx, mouse in enumerate(mouse_list):
        listx.append(mouse[0])
        listy.append(mouse[1])
        names.append(f"o MOUSE {idx}")

    fig.text(listy, listx, names, lc="red")

    listx = []
    listy = []
    for cat in cat_list:
        listx.append(cat[0])
        listy.append(cat[1])

    fig.scatter(listy, listx, lc="green", label="Cat", marker="x")

    print(fig.show(legend=True))


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-scatter_cats_example">
            <span class="terminal-prompt">root@plotille:~$ python3 scatter_cats_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## span_example

The MIT License

<div class="terminal-window interactive-example" data-example="span_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 span_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('span_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-span_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-span_example">
            <span class="terminal-prompt">root@plotille:~$ python3 span_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## stock_example

Example: stock_example

<div class="terminal-window interactive-example" data-example="stock_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 stock_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('stock_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-stock_example">import sys
from datetime import datetime, timezone
from random import randint
from time import sleep

import plotille as plt


def new_tick():
    return datetime.now(tz=timezone.utc), randint(0, 100)


def main():
    X = []
    Y = []
    now = datetime.now(tz=timezone.utc)

    while True:
        x, y = new_tick()
        X.append(x)
        Y.append(y)
        fig = plt.Figure()
        fig.width = 40
        fig.height = 20
        fig.plot(X, Y)
        fig.origin = False
        fig.set_x_limits(min_=now)
        fig.set_y_limits(min_=0, max_=100)
        sleep(1)
        print(fig.show())

        if "pytest" in sys.modules:
            break


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-stock_example">
            <span class="terminal-prompt">root@plotille:~$ python3 stock_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>


## wetterdienst_example

The MIT License

<div class="terminal-window interactive-example" data-example="wetterdienst_example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 wetterdienst_example.py]</span>
        <button class="terminal-run-btn" onclick="runExample('wetterdienst_example')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-wetterdienst_example"># The MIT License

# Copyright (c) 2017 - 2025 Tammo Ippen, tammo.ippen@posteo.de

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

# Get data for your own: https://github.com/earthobservations/wetterdienst
# call
# wetterdienst values --provider=dwd --kind=observation \
#                     --parameter=kl --resolution=daily \
#                     --station 1048,4411 \
#                     --date=1970-01-01/2021-01-01 > wetter-data.json

import gzip
import json
import os
from collections import defaultdict
from datetime import datetime

import plotille as plt


def regression(x, y):
    # formula from here:
    # https://devarea.com/linear-regression-with-numpy/
    n = len(x)
    assert n > 0
    assert n == len(y)

    sum_x = sum(x)
    sum_xx = sum(x_ * x_ for x_ in x)
    sum_y = sum(y)
    sum_xy = sum(x_ * y_ for x_, y_ in zip(x, y, strict=True))

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
    b = (sum_y - m * sum_x) / n

    return m, b


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with gzip.open(current_dir + os.sep + "wetter-data.json.gz", "r") as f:
        data = json.load(f)

    # wetterdienst stations --station 1048,4411 \
    #                       --provider dwd \
    #                       --kind observation \
    #                       --parameter kl \
    #                       --resolution daily
    stations = [
        {
            "station_id": "01048",
            "from_date": "1934-01-01T00:00:00.000Z",
            "to_date": "2021-07-04T00:00:00.000Z",
            "height": 228.0,
            "latitude": 51.1278,
            "longitude": 13.7543,
            "name": "Dresden-Klotzsche",
            "state": "Sachsen",
        },
        {
            "station_id": "04411",
            "from_date": "1979-12-01T00:00:00.000Z",
            "to_date": "2021-07-04T00:00:00.000Z",
            "height": 155.0,
            "latitude": 49.9195,
            "longitude": 8.9671,
            "name": "Schaafheim-Schlierbach",
            "state": "Hessen",
        },
    ]
    station_by_id = {st["station_id"]: st for st in stations}

    Xs = defaultdict(list)
    Ys = defaultdict(list)
    for d in data:
        if d["temperature_air_200"] is not None:
            dt = datetime.strptime(d["date"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            name = station_by_id[d["station_id"]]["name"]
            if dt.month == 1 and dt.day == 1:
                Xs[name] += [dt.year]
                Ys[name] += [d["temperature_air_200"] - 273.15]

    fig = plt.Figure()
    fig.width = 120
    fig.height = 30
    fig.set_x_limits(1970, 2021)
    fig.set_y_limits(-18, 12)
    fig.y_label = "Celsius"
    fig.x_label = "Year"

    fig.x_ticks_fkt = lambda min_, max_: f"{int(min_):d}"
    fig.y_ticks_fkt = lambda min_, max_: f"{min_:.3f}"

    markers = ["x", "o"]
    for idx, station in enumerate(Xs.keys()):
        fig.plot(Xs[station], Ys[station], label=station, marker=markers[idx])
        m, b = regression(Xs[station], Ys[station])
        start = m * 1970 + b
        end = m * 2021 + b
        fig.plot([1970, 2021], [start, end], label=f"{station} - regression")

    print("\033[2J")  # clear screen
    print(" " * 50 + "Temperature of two stations in Germany at 1. Januar")
    print(fig.show(legend=True))


if __name__ == "__main__":
    main()
</textarea>
        </div>
        <div class="terminal-output" id="output-wetterdienst_example">
            <span class="terminal-prompt">root@plotille:~$ python3 wetterdienst_example.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>

