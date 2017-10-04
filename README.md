# Plotille

[![Build Status](https://travis-ci.org/tammoippen/plotille.svg?branch=master)](https://travis-ci.org/tammoippen/plotille)
[![Coverage Status](https://coveralls.io/repos/github/tammoippen/plotille/badge.svg?branch=master)](https://coveralls.io/github/tammoippen/plotille?branch=master)
[![Tested CPython Versions](https://img.shields.io/badge/cpython-2.7%2C%203.5%2C%203.6%2C%20nightly-brightgreen.svg)](https://img.shields.io/badge/cpython-2.7%2C%203.5%2C%203.6%2C%20nightly-brightgreen.svg)
[![Tested PyPy Versions](https://img.shields.io/badge/pypy-2.7--5.8.0%2C%203.5--5.8.0-brightgreen.svg)](https://img.shields.io/badge/pypy-2.7--5.8.0%2C%203.5--5.8.0-brightgreen.svg)
[![PyPi version](https://img.shields.io/pypi/v/plotille.svg)](https://pypi.python.org/pypi/plotille)
[![PyPi license](https://img.shields.io/pypi/l/plotille.svg)](https://pypi.python.org/pypi/plotille)

Plot, scatter plots and histograms in the terminal using braille dots, with no external dependancies. For good visualization, use a font / terminal with monospaced braille characters.

Install:

```
pipenv install plotille
```

Similar to other libraries:

* like [drawille](https://github.com/asciimoo/drawille), but focused on graphing only – plus X/Y-axis.
* like [termplot](https://github.com/justnoise/termplot), but with braille (finer dots), left to right histogram and linear interpolation for plotting function.
* like [termgraph](https://github.com/sgeisler/termgraph) (not on pypi), but very different style.
* like [terminalplot](https://github.com/kressi/terminalplot), but with braille, X/Y-axis, histogram, linear interpolation.

## Documentation

```python
In [1]: import plotille
In [2]: import numpy as np
In [3]: X = sorted(np.random.normal(size=1000))
```

**Plot:**
```python
In [4]: plotille.plot?
Signature: plot(X, Y, width=80, height=50, X_label='X', Y_label='Y', linesep='\n', interp='linear')
Docstring:
Create plot with X , Y values and linear interpolation between points

Parameters:
    X: List[float]         X values.
    Y: List[float]         Y values. X and Y must have the same number of entries.
    width: int             The number of characters for the width (columns) of the canvas.
    hight: int             The number of characters for the hight (rows) of the canvas.
    X_label: str           Label for X-axis.
    Y_label: str           Label for Y-axis. max 8 characters.
    interp: Optional[str]  Specify interpolation; values None, 'linear'
Returns:
    str: plot over `X`, `Y`.

In [5]: print(plotille.plot(X, np.sin(X), height=50))
```
![Plot example](https://github.com/tammoippen/plotille/blob/master/imgs/plot.png)

**Scatter:**
```python
In [6]: plotille.scatter?
Signature: plotille.scatter(X, Y, width=80, height=50, X_label='X', Y_label='Y', linesep='\n')
Docstring:
Create scatter plot with X , Y values

Parameters:
    X: List[float]  X values.
    Y: List[float]  Y values. X and Y must have the same number of entries.
    width: int      The number of characters for the width (columns) of the canvas.
    hight: int      The number of characters for the hight (rows) of the canvas.
    X_label: str    Label for X-axis.
    Y_label: str    Label for Y-axis. max 8 characters.

Returns:
    str: scatter plot over `X`, `Y`.

In [7]: print(plotille.scatter(X, np.sin(X), height=50))
```
![Plot example](https://github.com/tammoippen/plotille/blob/master/imgs/scatter.png)

**Histogram:**

Inspired by [crappyhist](http://kevinastraight.x10host.com/2013/12/28/python-histograms-from-the-console/).
```python
In [8]: plotille.hist?
Signature: plotille.hist(X, bins=50, width=80, log_scale=False, linesep='\n')
Docstring:
Create histogram over `X`

Parameters:
    X: List[float]  The items to count over.
    bins: int       The number of bins to put X entries in (rows).
    width: int      The number of characters for the width (columns).
    log_scale: bool Scale the histogram with `log` function.

Returns:
    str: histogram over `X` from left to right.

In [9]: print(plotille.hist(np.random.normal(size=10000)))
```
![Histogram example](https://github.com/tammoippen/plotille/blob/master/imgs/hist.png)
