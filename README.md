# Plotille

[![CircleCI](https://circleci.com/gh/tammoippen/plotille.svg?style=svg)](https://circleci.com/gh/tammoippen/plotille)
[![codecov](https://codecov.io/gh/tammoippen/plotille/branch/master/graph/badge.svg?token=OGWI832JNM)](https://codecov.io/gh/tammoippen/plotille)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tammoippen/plotille.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tammoippen/plotille/context:python)
[![Tested CPython Versions](https://img.shields.io/badge/cpython-2.7%2C%203.6%2C%203.7%2C%203.8%2C%203.9-brightgreen.svg)](https://img.shields.io/badge/cpython-2.7%2C%203.6%2C%203.7%2C%203.8%2C%203.8-brightgreen.svg)
[![Tested PyPy Versions](https://img.shields.io/badge/pypy-2.7--7.3%2C%203.6--7.3%2C%203.7--7.3-brightgreen.svg)](https://img.shields.io/badge/pypy-2.7--7.3%2C%203.6--7.3%2C%203.7--7.3-brightgreen.svg)
[![PyPi version](https://img.shields.io/pypi/v/plotille.svg)](https://pypi.python.org/pypi/plotille)
[![Downloads](https://pepy.tech/badge/plotille/month)](https://pepy.tech/project/plotille)
[![PyPi license](https://img.shields.io/pypi/l/plotille.svg)](https://pypi.python.org/pypi/plotille)

Plot, scatter plots and histograms in the terminal using braille dots, with (almost) no dependancies. Plot with color or make complex figures - similar to a very small sibling to matplotlib. Or use the canvas to plot dots and lines yourself.

Install:

```sh
pip install plotille
```

Similar to other libraries:

* like [drawille](https://github.com/asciimoo/drawille), but focused on graphing – plus X/Y-axis.
* like [termplot](https://github.com/justnoise/termplot), but with braille (finer dots), left to right histogram and linear interpolation for plotting function.
* like [termgraph](https://github.com/sgeisler/termgraph) (not on pypi), but very different style.
* like [terminalplot](https://github.com/kressi/terminalplot), but with braille, X/Y-axis, histogram, linear interpolation.

Basic support for timeseries plotting is provided with release 3.2: for any `X` or `Y` values you can also add `datetime.datetime`, `pendulum.datetime` or `numpy.datetime64` values. Labels are generated respecting the difference of `x_limits` and `y_limits`.

## Documentation

```python
In [1]: import plotille
In [2]: import numpy as np
In [3]: X = np.sort(np.random.normal(size=1000))
```

### Figure

To construct plots the recomended way is to use a `Figure`:

```python
In [12]: plotille.Figure?
Init signature: plotille.Figure()
Docstring:
Figure class to compose multiple plots.

Within a Figure you can easily compose many plots, assign labels to plots
and define the properties of the underlying Canvas. Possible properties that
can be defined are:

    width, height: int    Define the number of characters in X / Y direction
                          which are used for plotting.
    x_limits: float       Define the X limits of the reference coordinate system,
                          that will be plottered.
    y_limits: float       Define the Y limits of the reference coordinate system,
                          that will be plottered.
    color_mode: str       Define the used color mode. See `plotille.color()`.
    with_colors: bool     Define, whether to use colors at all.
    background: multiple  Define the background color.
    x_label, y_label: str Define the X / Y axis label.
```

Basically, you create a `Figure`, define the properties and add your plots. Using the `show()` function, the `Figure` generates the plot using a new canvas:

```python
In [13] fig = plotille.Figure()
In [14] fig.width = 60
In [15] fig.height = 30
In [16] fig.set_x_limits(min_=-3, max_=3)
In [17] fig.set_y_limits(min_=-1, max_=1)
In [18] fig.color_mode = 'byte'
In [19] fig.plot([-0.5, 1], [-1, 1], lc=25, label='First line')
In [20] fig.scatter(X, np.sin(X), lc=100, label='sin')
In [21] fig.plot(X, (X+2)**2 , lc=200, label='square')
In [22] print(fig.show(legend=True))
```

![Example figure](https://github.com/tammoippen/plotille/raw/master/imgs/figure.png)

The available plotting functions are:

```python
# create a plot with linear interpolation between points
Figure.plot(self, X, Y, lc=None, interp='linear', label=None, marker=None)
# create a scatter plot with no interpolation between points
Figure.scatter(self, X, Y, lc=None, label=None, marker=None)
# create a histogram over X
Figure.histogram(self, X, bins=160, lc=None)
# print texts at coordinates X, Y
Figure.text(self, X, Y, texts, lc=None)

# The following functions use relative coordinates on the canvas
# i.e. all coordinates are \in [0, 1]
# plot a vertical line at x
Figure.axvline(self, x, ymin=0, ymax=1, lc=None)
# plot a vertical rectangle from (xmin,ymin) to (xmax, ymax).
Figure.axvspan(self, xmin, xmax, ymin=0, ymax=1, lc=None)
# plot a horizontal line at y
Figure.axhline(self, y, xmin=0, xmax=1, lc=None)
# plot a horizontal rectangle from (xmin,ymin) to (xmax, ymax).
Figure.axhspan(self, ymin, ymax, xmin=0, xmax=1, lc=None)
```

Other interesting functions are:

```python
# remove all plots, texts and spans from the figure
Figure.clear(self)
# Create a canvas, plot the registered plots and return the string for displaying the plot
Figure.show(self, legend=False)
```

### Graphing

There are some utility functions for fast graphing of single plots.

#### Plot

```python
In [4]: plotille.plot?
Signature:
plotille.plot(
    X,
    Y,
    width=80,
    height=40,
    X_label='X',
    Y_label='Y',
    linesep='\n',
    interp='linear',
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    lc=None,
    bg=None,
    color_mode='names',
    origin=True,
    marker=None,
)
Docstring:
Create plot with X , Y values and linear interpolation between points

Parameters:
    X: List[float]         X values.
    Y: List[float]         Y values. X and Y must have the same number of entries.
    width: int             The number of characters for the width (columns) of the canvas.
    hight: int             The number of characters for the hight (rows) of the canvas.
    X_label: str           Label for X-axis.
    Y_label: str           Label for Y-axis. max 8 characters.
    linesep: str           The requested line seperator. default: os.linesep
    interp: Optional[str]  Specify interpolation; values None, 'linear'
    x_min, x_max: float    Limits for the displayed X values.
    y_min, y_max: float    Limits for the displayed Y values.
    lc: multiple           Give the line color.
    bg: multiple           Give the background color.
    color_mode: str        Specify color input mode; 'names' (default), 'byte' or 'rgb'
                           see plotille.color.__docs__
    origin: bool           Whether to print the origin. default: True
    marker: str            Instead of braille dots set a marker char for actual values.

Returns:
    str: plot over `X`, `Y`.

In [5]: print(plotille.plot(X, np.sin(X), height=30, width=60))
```

![Example plot](https://github.com/tammoippen/plotille/raw/master/imgs/plot.png)

#### Scatter

```python
In [6]: plotille.scatter?
Signature:
plotille.scatter(
    X,
    Y,
    width=80,
    height=40,
    X_label='X',
    Y_label='Y',
    linesep='\n',
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    lc=None,
    bg=None,
    color_mode='names',
    origin=True,
    marker=None,
)
Docstring:
Create scatter plot with X , Y values

Basically plotting without interpolation:
    `plot(X, Y, ... , interp=None)`

Parameters:
    X: List[float]       X values.
    Y: List[float]       Y values. X and Y must have the same number of entries.
    width: int           The number of characters for the width (columns) of the canvas.
    hight: int           The number of characters for the hight (rows) of the canvas.
    X_label: str         Label for X-axis.
    Y_label: str         Label for Y-axis. max 8 characters.
    linesep: str         The requested line seperator. default: os.linesep
    x_min, x_max: float  Limits for the displayed X values.
    y_min, y_max: float  Limits for the displayed Y values.
    lc: multiple         Give the line color.
    bg: multiple         Give the background color.
    color_mode: str      Specify color input mode; 'names' (default), 'byte' or 'rgb'
                         see plotille.color.__docs__
    origin: bool         Whether to print the origin. default: True
    marker: str          Instead of braille dots set a marker char.

Returns:
    str: scatter plot over `X`, `Y`.

In [7]: print(plotille.scatter(X, np.sin(X), height=30, width=60))
```

![Example scatter](https://github.com/tammoippen/plotille/raw/master/imgs/scatter.png)

#### Hist

Inspired by [crappyhist](http://kevinastraight.x10host.com/2013/12/28/python-histograms-from-the-console/) (link is gone, but I made a [gist](https://gist.github.com/tammoippen/4474e838e969bf177155231ebba52386)).

```python
In [8]: plotille.hist?
Signature:
plotille.hist(
    X,
    bins=40,
    width=80,
    log_scale=False,
    linesep='\n',
    lc=None,
    bg=None,
    color_mode='names',
)
Docstring:
Create histogram over `X` from left to right

The values on the left are the center of the bucket, i.e. `(bin[i] + bin[i+1]) / 2`.
The values on the right are the total counts of this bucket.

Parameters:
    X: List[float]       The items to count over.
    bins: int            The number of bins to put X entries in (rows).
    width: int           The number of characters for the width (columns).
    log_scale: bool      Scale the histogram with `log` function.
    linesep: str         The requested line seperator. default: os.linesep
    lc: multiple         Give the line color.
    bg: multiple         Give the background color.
    color_mode: str      Specify color input mode; 'names' (default), 'byte' or 'rgb'
                         see plotille.color.__docs__

Returns:
    str: histogram over `X` from left to right.

In [9]: print(plotille.hist(np.random.normal(size=10000)))
```

![Example hist](https://github.com/tammoippen/plotille/raw/master/imgs/hist.png)

#### Histogram

There is also another more 'usual' histogram function available:

```python
In [10]: plotille.histogram?
Signature:
plotille.histogram(
    X,
    bins=160,
    width=80,
    height=40,
    X_label='X',
    Y_label='Counts',
    linesep='\n',
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    lc=None,
    bg=None,
    color_mode='names',
)
Docstring:
Create histogram over `X`

In contrast to `hist`, this is the more `usual` histogram from bottom
to up. The X-axis represents the values in `X` and the Y-axis is the
corresponding frequency.

Parameters:
    X: List[float]       The items to count over.
    bins: int            The number of bins to put X entries in (columns).
    height: int          The number of characters for the height (rows).
    X_label: str         Label for X-axis.
    Y_label: str         Label for Y-axis. max 8 characters.
    linesep: str         The requested line seperator. default: os.linesep
    x_min, x_max: float  Limits for the displayed X values.
    y_min, y_max: float  Limits for the displayed Y values.
    lc: multiple         Give the line color.
    bg: multiple         Give the background color.
    color_mode: str      Specify color input mode; 'names' (default), 'byte' or 'rgb'
                         see plotille.color.__docs__

Returns:
    str: histogram over `X`.

In [11]: print(plotille.histogram(np.random.normal(size=10000)))
```

![Example histogram](https://github.com/tammoippen/plotille/raw/master/imgs/histogram.png)

### Canvas

The underlying plotting area is modeled as the `Canvas` class:

```python
In [12]: plotille.Canvas?
Init signature:
plotille.Canvas(
    width,
    height,
    xmin=0,
    ymin=0,
    xmax=1,
    ymax=1,
    background=None,
    color_mode='names',
)
Docstring:
A canvas object for plotting braille dots

A Canvas object has a `width` x `height` characters large canvas, in which it
can plot indivitual braille point, lines out of braille points, rectangles,...
Since a full braille character has 2 x 4 dots (⣿), the canvas has `width` * 2, `height` * 4
dots to plot into in total.

It maintains two coordinate systems: a reference system with the limits (xmin, ymin)
in the lower left corner to (xmax, ymax) in the upper right corner is transformed
into the canvas discrete, i.e. dots, coordinate system (0, 0) to (`width` * 2, `height` * 4).
It does so transparently to clients of the Canvas, i.e. all plotting functions
only accept coordinates in the reference system. If the coordinates are outside
the reference system, they are not plotted.
Init docstring:
Initiate a Canvas object

Parameters:
    width: int            The number of characters for the width (columns) of the canvas.
    hight: int            The number of characters for the hight (rows) of the canvas.
    xmin, ymin: float     Lower left corner of reference system.
    xmax, ymax: float     Upper right corner of reference system.
    background: multiple  Background color of the canvas.
    color_mode: str       The color-mode for all colors of this canvas; either 'names' (default)
                          'rgb' or 'byte'. See `plotille.color()`.

Returns:
    Canvas object
```

The most interesting functions are:

*point:*

```python
In [11]: plotille.Canvas.point?
Signature: plotille.Canvas.point(self, x, y, set_=True, color=None, marker=None)
Docstring:
Put a point into the canvas at (x, y) [reference coordinate system]

Parameters:
    x: float         x-coordinate on reference system.
    y: float         y-coordinate on reference system.
    set_: bool       Whether to plot or remove the point.
    color: multiple  Color of the point.
    marker: str      Instead of braille dots set a marker char.
```

*line:*

```python
In [14]: plotille.Canvas.line?
Signature: plotille.Canvas.line(self, x0, y0, x1, y1, set_=True, color=None)
Docstring:
Plot line between point (x0, y0) and (x1, y1) [reference coordinate system].

Parameters:
    x0, y0: float    Point 0
    x1, y1: float    Point 1
    set_: bool       Whether to plot or remove the line.
    color: multiple  Color of the line.
```

*rect:*

```python
In [15]: plotille.Canvas.rect?
Signature: plotille.Canvas.rect(self, xmin, ymin, xmax, ymax, set_=True, color=None)
Docstring:
Plot rectangle with bbox (xmin, ymin) and (xmax, ymax) [reference coordinate system].

Parameters:
    xmin, ymin: float  Lower left corner of rectangle.
    xmax, ymax: float  Upper right corner of rectangle.
    set_: bool         Whether to plot or remove the rect.
    color: multiple    Color of the rect.
```

*text:*

```python
In [16]: plotille.Canvas.text?
Signature: plotille.Canvas.text(self, x, y, text, set_=True, color=None)
Docstring:
Put some text into the canvas at (x, y) [reference coordinate system]

Parameters:
    x: float         x-coordinate on reference system.
    y: float         y-coordinate on reference system.
    set_: bool       Whether to set the text or clear the characters.
    text: str        The text to add.
    color: multiple  Color of the point.
```

*plot:*

```python
In [16]: plotille.Canvas.plot?
Signature: plotille.Canvas.plot(self, linesep='\n')
Docstring:
Transform canvas into `print`-able string

Parameters:
    linesep: str  The requested line seperator. default: os.linesep

Returns:
    unicode: The canvas as a string.
```

You can use it for example to plot a house in the terminal:

```python
In [17]: c = Canvas(width=40, height=20)
In [18]: c.rect(0.1, 0.1, 0.6, 0.6)
In [19]: c.line(0.1, 0.1, 0.6, 0.6)
In [20]: c.line(0.1, 0.6, 0.6, 0.1)
In [21]: c.line(0.1, 0.6, 0.35, 0.8)
In [22]: c.line(0.35, 0.8, 0.6, 0.6)
In [23]: print(c.plot())
```

![House](https://github.com/tammoippen/plotille/raw/master/imgs/house.png)

## Stargazers over time

[![Stargazers over time](https://starchart.cc/tammoippen/plotille.svg)](https://starchart.cc/tammoippen/plotille)
