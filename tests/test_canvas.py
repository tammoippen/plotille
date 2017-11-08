# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import numpy as np
from plotille import Canvas
import pytest


def test_invalids():
    with pytest.raises(AssertionError):
        Canvas(0, 0)

    with pytest.raises(AssertionError):
        Canvas(1.0, 1.0)

    with pytest.raises(AssertionError):
        Canvas(1, 1, xmin=1, xmax=0)

    with pytest.raises(AssertionError):
        Canvas(1, 1, ymin=1, ymax=0)


def test_str():
    c = Canvas(40, 20)
    assert 'Canvas(width=40, height=20, xmin=0, ymin=0, xmax=1, ymax=1)' == str(c)
    assert 'Canvas(width=40, height=20, xmin=0, ymin=0, xmax=1, ymax=1)' == repr(c)


def test_transform():
    c = Canvas(40, 20)

    assert 0 == c._transform_x(0)
    assert 0 == c._transform_y(0)

    assert 40 * 2 == c._transform_x(1)
    assert 20 * 4 == c._transform_y(1)

    assert 40 == c._transform_x(0.5)
    assert 20 * 2 == c._transform_y(0.5)

    for v in np.random.random(100):
        assert 0 <= c._transform_x(v) <= 40 * 2
        assert isinstance(c._transform_x(v), int)

        assert 0 <= c._transform_y(v) <= 20 * 4
        assert isinstance(c._transform_y(v), int)

    assert -40 == c._transform_x(-0.5)
    assert -20 * 2 == c._transform_y(-0.5)

    assert 40 * 2 + 40 == c._transform_x(1.5)
    assert 20 * 4 + 20 * 2 == c._transform_y(1.5)


def test_set():
    c = Canvas(1, 1)
    c._set(0, 0)
    assert '⡀' == c._canvas[0][0]
    c._set(0, 0, False)
    assert '⠀' == c._canvas[0][0]

    c._set(0, 1)
    assert '⠄' == c._canvas[0][0]
    c._set(0, 1, False)
    assert '⠀' == c._canvas[0][0]

    c._set(0, 2)
    assert '⠂' == c._canvas[0][0]
    c._set(0, 2, False)
    assert '⠀' == c._canvas[0][0]

    c._set(0, 3)
    assert '⠁' == c._canvas[0][0]
    c._set(0, 3, False)
    assert '⠀' == c._canvas[0][0]

    c._set(1, 0)
    assert '⢀' == c._canvas[0][0]
    c._set(1, 0, False)
    assert '⠀' == c._canvas[0][0]

    c._set(1, 1)
    assert '⠠' == c._canvas[0][0]
    c._set(1, 1, False)
    assert '⠀' == c._canvas[0][0]

    c._set(1, 2)
    assert '⠐' == c._canvas[0][0]
    c._set(1, 2, False)
    assert '⠀' == c._canvas[0][0]

    c._set(1, 3)
    assert '⠈' == c._canvas[0][0]
    c._set(1, 3, False)
    assert '⠀' == c._canvas[0][0]


def test_fill_char():
    c = Canvas(1, 1)

    c.fill_char(0.5, 0.5)
    assert '⣿' == c._canvas[0][0]
    c.fill_char(0.5, 0.5, False)
    assert '⠀' == c._canvas[0][0]
