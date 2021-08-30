# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
import six

from plotille import Canvas

try:
    import numpy as np
    have_numpy = True
except ImportError:
    have_numpy = False

try:
    from PIL import Image
    have_pillow = True
except ImportError:
    have_pillow = False


@pytest.mark.skipif(not have_numpy, reason='No numpy installed.')
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


@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
def test_braille_image():
    img = Image.open('imgs/ich.jpg')
    img = img.convert('L')
    img = img.resize((80, 80))
    cvs = Canvas(40, 20)
    cvs.braille_image(img.getdata())

    expected = """\
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠛⠙⢿⠿⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠁⠀⠀⠀⠹⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⣀⣴⣶⣾⣶⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠉⠀⠀⠀⠀⣠⣿⣿⣾⣿⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡀⠀⠀⠀⢠⣿⢿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠙
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡴⣡⣶⣦⣉⣿⣿⡟⠋⢀⣤⠄⠀⡀⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣧
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠧⠀⠀⢠⣿⢃⡔⠚⣤⢌⣿⣷⣤⣿⠇⡀⠁⠀⠐⠀⠀⡀⠙⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡂⣄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⡦⠀⠁⠀⠀⣀⠀⠀⠁⠀⢹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣧⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠃⠈⠠⣤⡄⠤⠀⠀⠀⠈⣻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⠆⠹⢿⣿⣿⣿⣇⢈⠉⢉⡑⣄⡀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠰⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠸⣿⠿⠉⢀⣨⣟⡁⠉⠃⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠈⠻⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⡏⢲⣚⣛⡛⠻⠿⣶⣀⠃⠀⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡻⣿⣿⣿⣿⣿⡷⣿⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠘⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠀⠃⠀⠀⢻⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘
⣿⣿⣿⣿⣿⣿⣿⠿⠛⣻⣿⣿⡟⠀⠀⠀⠠⣀⠈⠉⠁⡠⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⡿⠿⠛⠉⠀⠀⠀⠻⣿⣿⣳⡄⠀⠀⠀⠙⠿⠻⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

    assert expected == cvs.plot()

    cvs.braille_image(img.getdata(), set_=False)
    # empty canvas
    assert '\n'.join(['⠀' * 40] * 20) == cvs.plot()


@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
@pytest.mark.parametrize('threshold', range(20, 255, 10))
def test_braille_image_thresholds(threshold):
    img = Image.open('imgs/ich.jpg')
    img = img.convert('L')
    img = img.resize((80, 80))
    cvs = Canvas(40, 20)
    cvs.braille_image(img.getdata(), threshold=threshold)

    assert '\n'.join(['⠀' * 40] * 20) != cvs.plot()
    print()
    print(cvs.plot())

    cvs.braille_image(img.getdata(), threshold=threshold, set_=False)
    # empty canvas
    assert '\n'.join(['⠀' * 40] * 20) == cvs.plot()


@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
def test_braille_image_inverse():
    img = Image.open('imgs/ich.jpg')
    img = img.convert('L')
    img = img.resize((80, 80))
    cvs = Canvas(40, 20)
    cvs.braille_image(img.getdata(), inverse=True)

    expected = """\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣤⣦⡀⣀⡀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣾⣿⣿⣿⣆⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⠿⠋⠉⠁⠉⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⣿⣿⣿⣿⠟⠀⠀⠁⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢿⣿⣿⣿⡟⠀⡀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣦
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⢋⠞⠉⠙⠶⠀⠀⢠⣴⡿⠛⣻⣿⢿⣶⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠘
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⣿⣿⡟⠀⡼⢫⣥⠛⡳⠀⠈⠛⠀⣸⢿⣾⣿⣯⣿⣿⢿⣦⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢽⠻⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⢙⣿⣾⣿⣿⠿⣿⣿⣾⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣷⣼⣷⣟⠛⢻⣛⣿⣿⣿⣷⠄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⣹⣆⡀⠀⠀⠀⠸⡷⣶⡶⢮⠻⢿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣏⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣇⠀⣀⣶⡿⠗⠠⢾⣶⣼⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢰⡍⠥⠤⢤⣄⣀⠉⠿⣼⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⢄⠀⠀⠀⠀⠀⢈⠀⣏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣧⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⣼⣿⣿⡄⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⠀⠀⠀⠀⠀⠀⠀⣀⣤⠄⠀⠀⢠⣿⣿⣿⣟⠿⣷⣶⣾⢟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢀⣀⣤⣶⣿⣿⣿⣄⠀⠀⠌⢻⣿⣿⣿⣦⣀⣄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""

    assert expected == cvs.plot()

    cvs.braille_image(img.getdata(), inverse=True, set_=False)
    # empty canvas
    assert '\n'.join(['⠀' * 40] * 20) == cvs.plot()


@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
@pytest.mark.parametrize('threshold', range(20, 255, 10))
def test_braille_image_inverse_thresholds(threshold):
    img = Image.open('imgs/ich.jpg')
    img = img.convert('L')
    img = img.resize((80, 80))
    cvs = Canvas(40, 20)
    cvs.braille_image(img.getdata(), threshold=threshold, inverse=True)

    assert '\n'.join(['⠀' * 40] * 20) != cvs.plot()

    cvs.braille_image(img.getdata(), threshold=threshold, inverse=True, set_=False)
    # empty canvas
    assert '\n'.join(['⠀' * 40] * 20) == cvs.plot()


@pytest.mark.parametrize('r', [0, 50, 100, 123, 255])
@pytest.mark.parametrize('g', [0, 50, 100, 123, 255])
@pytest.mark.parametrize('b', [0, 50, 100, 123, 255])
def test_image_one_px(tty, r, g, b):
    cvs = Canvas(1, 1, mode='rgb')
    cvs.image([(r, g, b)])

    assert '\x1b[48;2;{};{};{}m⠀\x1b[0m'.format(r, g, b) == cvs.plot()

    cvs.image([(r, g, b)], set_=False)
    # empty canvas
    assert '⠀' == cvs.plot()


def test_image_rgb(tty):
    img = Image.open('imgs/ich.jpg')
    img = img.convert('RGB')
    img = img.resize((40, 40))
    cvs = Canvas(40, 40, mode='rgb')
    cvs.image(img.getdata())

    assert '\n'.join(['⠀' * 40] * 40) != cvs.plot()

    print()
    print(cvs.plot())

    cvs.image(img.getdata(), set_=False)
    # empty canvas
    assert '\n'.join(['⠀' * 40] * 40) == cvs.plot()


def test_image_byte(tty):
    img = Image.open('imgs/ich.jpg')
    img = img.convert('RGB')
    img = img.resize((40, 40))
    cvs = Canvas(40, 40, mode='byte')
    cvs.image(img.getdata())

    assert '\n'.join(['⠀' * 40] * 40) != cvs.plot()

    print()
    print(cvs.plot())

    cvs.image(img.getdata(), set_=False)
    # empty canvas
    assert '\n'.join(['⠀' * 40] * 40) == cvs.plot()
