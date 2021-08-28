# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
import six

from plotille import Canvas

try:
    import numpy as np

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

except ImportError:
    pass


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
    assert 'Canvas(width=40, height=20, xmin=0, ymin=0, xmax=1, ymax=1)' == six.text_type(c)
    assert 'Canvas(width=40, height=20, xmin=0, ymin=0, xmax=1, ymax=1)' == repr(c)


def test_set():
    c = Canvas(1, 1)
    c._set(0, 0)
    assert '⡀' == six.text_type(c._canvas[0][0])
    c._set(0, 0, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(0, 1)
    assert '⠄' == six.text_type(c._canvas[0][0])
    c._set(0, 1, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(0, 2)
    assert '⠂' == six.text_type(c._canvas[0][0])
    c._set(0, 2, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(0, 3)
    assert '⠁' == six.text_type(c._canvas[0][0])
    c._set(0, 3, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(1, 0)
    assert '⢀' == six.text_type(c._canvas[0][0])
    c._set(1, 0, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(1, 1)
    assert '⠠' == six.text_type(c._canvas[0][0])
    c._set(1, 1, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(1, 2)
    assert '⠐' == six.text_type(c._canvas[0][0])
    c._set(1, 2, False)
    assert '⠀' == six.text_type(c._canvas[0][0])

    c._set(1, 3)
    assert '⠈' == six.text_type(c._canvas[0][0])
    c._set(1, 3, False)
    assert '⠀' == six.text_type(c._canvas[0][0])


def test_fill_char():
    c = Canvas(1, 1)

    c.fill_char(0.5, 0.5)
    assert '⣿' == six.text_type(c._canvas[0][0])
    c.fill_char(0.5, 0.5, False)
    assert '⠀' == six.text_type(c._canvas[0][0])


@pytest.mark.parametrize('color', [None, 'red'])
def test_point(color, tty):
    c = Canvas(1, 1)

    c.point(0, 0, color=color)
    prefix = ''
    postfix = ''
    if color:
        prefix = '\x1b[31m'
        postfix = '\x1b[0m'

    assert '{}⡀{}'.format(prefix, postfix) == six.text_type(c._canvas[0][0])
    c.point(0, 0, set_=False, color=color)
    assert '⠀' == six.text_type(c._canvas[0][0])


@pytest.mark.parametrize('color', [None, 'red'])
def test_set_text(color, tty):
    c = Canvas(2, 1)

    c.text(0, 0, 'Hi', color=color)
    prefix = ''
    postfix = ''
    if color:
        prefix = '\x1b[31m'
        postfix = '\x1b[0m'

    assert '{}H{}'.format(prefix, postfix) == six.text_type(c._canvas[0][0])
    assert '{}i{}'.format(prefix, postfix) == six.text_type(c._canvas[0][1])
    c.text(0, 0, 'Hi', False, color=color)
    assert '⠀' == six.text_type(c._canvas[0][0])
    assert '⠀' == six.text_type(c._canvas[0][1])


def test_set_text_keep_dots():
    c = Canvas(2, 1)

    c.fill_char(0, 0)
    assert '⣿' == six.text_type(c._canvas[0][0])

    c.text(0, 0, 'Hi')
    assert 'H' == six.text_type(c._canvas[0][0])
    assert 'i' == six.text_type(c._canvas[0][1])
    c.fill_char(0.5, 0.5, False)
    c.text(0, 0, 'Hi', False)
    assert '⣿' == six.text_type(c._canvas[0][0])
    assert '⠀' == six.text_type(c._canvas[0][1])


def test_set_text_to_long():
    c = Canvas(2, 1)

    c.text(0, 0, 'Hello World')
    assert 'H' == six.text_type(c._canvas[0][0])
    assert 'e' == six.text_type(c._canvas[0][1])
    c.fill_char(0.5, 0.5, False)
    c.text(0, 0, 'Hello World', False)
    assert '⠀' == six.text_type(c._canvas[0][0])
    assert '⠀' == six.text_type(c._canvas[0][1])


@pytest.mark.parametrize('empty', ['', None])
def test_set_text_empty(empty):
    c = Canvas(2, 1)

    c.text(0, 0, empty)
    assert '⠀' == six.text_type(c._canvas[0][0])
    assert '⠀' == six.text_type(c._canvas[0][1])
    c.fill_char(0.5, 0.5, False)
    c.text(0, 0, empty, False)
    assert '⠀' == six.text_type(c._canvas[0][0])
    assert '⠀' == six.text_type(c._canvas[0][1])


@pytest.mark.parametrize('other_color', [None, 'blue'])
def test_unset_keep_color_text(tty, other_color):
    c = Canvas(2, 1)

    c.text(0, 0, 'Hi', color='red')
    prefix = '\x1b[31m'
    postfix = '\x1b[0m'

    assert '{}H{}'.format(prefix, postfix) == six.text_type(c._canvas[0][0])
    assert '{}i{}'.format(prefix, postfix) == six.text_type(c._canvas[0][1])
    c.text(0, 0, 'Hi', False, color=other_color)
    assert '{}⠀{}'.format(prefix, postfix) == six.text_type(c._canvas[0][0])
    assert '{}⠀{}'.format(prefix, postfix) == six.text_type(c._canvas[0][1])


@pytest.mark.parametrize('other_color', [None, 'blue'])
def test_unset_keep_color_dots(tty, other_color):
    c = Canvas(1, 1)

    c.point(0, 0, color='red')
    prefix = '\x1b[31m'
    postfix = '\x1b[0m'

    assert '{}⡀{}'.format(prefix, postfix) == six.text_type(c._canvas[0][0])
    c.point(0, 0, set_=False, color=other_color)
    assert '{}⠀{}'.format(prefix, postfix) == six.text_type(c._canvas[0][0])
