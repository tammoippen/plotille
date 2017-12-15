# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import combinations

from plotille._dots import braille_from, Dots, dots_from
import six


def test_update():
    d = Dots()

    assert d.dots == []
    assert d.fg is None
    assert d.bg is None
    assert d.mode == 'names'

    d.update(0, 0)
    assert d.dots == [7]

    d.update(1, 0)
    assert d.dots == [7, 8]

    d.update(1, 0)
    assert d.dots == [7, 8]

    d.update(0, 1)
    assert d.dots == [3, 7, 8]

    d.update(1, 1)
    assert d.dots == [3, 6, 7, 8]

    d.update(0, 2)
    assert d.dots == [2, 3, 6, 7, 8]

    d.update(1, 2)
    assert d.dots == [2, 3, 5, 6, 7, 8]

    d.update(0, 3)
    assert d.dots == [1, 2, 3, 5, 6, 7, 8]

    d.update(1, 3)
    assert d.dots == [1, 2, 3, 4, 5, 6, 7, 8]

    d.clear()
    assert d.dots == []

    d.fill()
    assert d.dots == [1, 2, 3, 4, 5, 6, 7, 8]


def test_unset():
    d = Dots()

    d.fill()
    assert d.dots == [1, 2, 3, 4, 5, 6, 7, 8]

    d.update(0, 0, set_=False)
    assert d.dots == [1, 2, 3, 4, 5, 6, 8]

    d.update(0, 0, set_=False)
    assert d.dots == [1, 2, 3, 4, 5, 6, 8]

    d.update(1, 0, set_=False)
    assert d.dots == [1, 2, 3, 4, 5, 6]

    d.update(0, 1, set_=False)
    assert d.dots == [1, 2, 4, 5, 6]

    d.update(1, 1, set_=False)
    assert d.dots == [1, 2, 4, 5]

    d.update(0, 2, set_=False)
    assert d.dots == [1, 4, 5]

    d.update(1, 2, set_=False)
    assert d.dots == [1, 4]

    d.update(0, 3, set_=False)
    assert d.dots == [4]

    d.update(1, 3, set_=False)
    assert d.dots == []


def test_print():
    d = Dots()

    d.update(0, 0)
    assert '⡀' == six.text_type(d)
    d.update(0, 0, False)
    assert '⠀' == six.text_type(d)

    d.update(0, 1)
    assert '⠄' == six.text_type(d)
    d.update(0, 1, False)
    assert '⠀' == six.text_type(d)

    d.update(0, 2)
    assert '⠂' == six.text_type(d)
    d.update(0, 2, False)
    assert '⠀' == six.text_type(d)

    d.update(0, 3)
    assert '⠁' == six.text_type(d)
    d.update(0, 3, False)
    assert '⠀' == six.text_type(d)

    d.update(1, 0)
    assert '⢀' == six.text_type(d)
    d.update(1, 0, False)
    assert '⠀' == six.text_type(d)

    d.update(1, 1)
    assert '⠠' == six.text_type(d)
    d.update(1, 1, False)
    assert '⠀' == six.text_type(d)

    d.update(1, 2)
    assert '⠐' == six.text_type(d)
    d.update(1, 2, False)
    assert '⠀' == six.text_type(d)

    d.update(1, 3)
    assert '⠈' == six.text_type(d)
    d.update(1, 3, False)
    assert '⠀' == six.text_type(d)


def test_braille_dots_from():
    idxs = [1, 2, 3, 4, 5, 6, 7, 8]

    found = set()
    for r in range(0, 9):
        for s in combinations(idxs, r):
            c = braille_from(s)
            assert c not in found
            found |= {c}
            assert 0x2800 <= ord(c) <= 0x28ff
            s_ = dots_from(c)

            assert len(s) == len(s_)
            assert set(s) == set(s_)
