# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import numpy as np
import plotille


def test_plot():
    x = np.random.normal(size=100)
    print(plotille.plot(x, np.sin(x), height=50))


def test_scatter():
    x = np.random.normal(size=100)
    print(plotille.scatter(x, np.sin(x), height=50))


def test_hist():
    x = np.random.normal(size=10000)
    print(plotille.hist(x))
