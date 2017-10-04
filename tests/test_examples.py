# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import numpy as np
import plotille


def test_plot():
    x = sorted(np.random.normal(size=1000))
    print()
    print(plotille.plot(list(x), list(np.sin(x)), height=50))


def test_scatter():
    x = np.random.normal(size=1000)
    print()
    print(plotille.scatter(list(x), list(np.sin(x)), height=50))


def test_hist():
    x = np.random.normal(size=10000)
    print()
    print(plotille.hist(list(x)))


def test_np_plot():
    x = sorted(np.random.normal(size=1000))
    print()
    print(plotille.plot(x, np.sin(x), height=50))


def test_np_scatter():
    x = np.random.normal(size=1000)
    print()
    print(plotille.scatter(x, np.sin(x), height=50))


def test_np_hist():
    x = np.random.normal(size=10000)
    print()
    print(plotille.hist(x))


def test_hist_log():
    x = np.random.normal(size=10000)
    print()
    print(plotille.hist(x, log_scale=True))


def test_empty_plot():
    print()
    print(plotille.plot([], [], height=50))


def test_empty_scatter():
    print()
    print(plotille.scatter([], [], height=50))


def test_empty_hist():
    print()
    print(plotille.hist([]))
