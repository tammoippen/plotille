# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from plotille import plot


def test_constant_y():
    print(plot([1, 4], [0.5, 0.5]))


def test_constant_x():
    print(plot([0.5, 0.5], [1, 4]))


def test_constant_x_y():
    print(plot([0.5, 0.5], [0.5, 0.5]))
