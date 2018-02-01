# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from random import choice

import plotille._colors as clr
import pytest


def test_color_edges(mocker, tty):
    assert '' == clr.color('')
    assert '' == clr.color('', 'black', 'red', no_color=True)

    with pytest.raises(ValueError):
        clr.color('', 'black', 'red', mode='NAME')  # wrong mode

    mocker.patch('plotille._colors._isatty', return_value=False)
    assert '' == clr.color('', 'black', 'red')


def test_names(tty):
    assert '' == clr._names(None, None)
    assert '\x1b[30m' == clr._names('black', None)
    assert '\x1b[30;40m' == clr._names('black', 'black')

    names = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    for i, fg in enumerate(names):
        assert '\x1b[{}m'.format(30 + i) == clr._names(fg, None)
        assert '\x1b[1;{}m'.format(30 + i) == clr._names('bright_' + fg, None)

        assert '\x1b[{}m \x1b[0m'.format(30 + i) == clr.color(' ', fg, None)
        assert '\x1b[1;{}m \x1b[0m'.format(30 + i) == clr.color(' ', 'bright_' + fg, None)

        for j, bg in enumerate(names):
            assert '\x1b[{}m'.format(40 + j) == clr._names(None, bg)
            assert '\x1b[{}m'.format(100 + j) == clr._names(None, 'bright_' + bg)

            assert '\x1b[{}m \x1b[0m'.format(40 + j) == clr.color(' ', None, bg)
            assert '\x1b[{}m \x1b[0m'.format(100 + j) == clr.color(' ', None, 'bright_' + bg)

            assert '\x1b[{};{}m'.format(30 + i, 40 + j) == clr._names(fg, bg)
            assert '\x1b[1;{};{}m'.format(30 + i, 100 + j) == clr._names('bright_' + fg, 'bright_' + bg)

            assert '\x1b[{};{}m \x1b[0m'.format(30 + i, 40 + j) == clr.color(' ', fg, bg)
            assert '\x1b[1;{};{}m \x1b[0m'.format(30 + i, 100 + j) == clr.color(' ', 'bright_' + fg, 'bright_' + bg)

    with pytest.raises(ValueError):
        clr._names('olive', None)

    with pytest.raises(ValueError):
        clr._names(None, 'olive')


def test_bytes(tty):
    assert '' == clr._byte(None, None)
    assert '\x1b[38;5;0m' == clr._byte(0, None)
    assert '\x1b[38;5;0;48;5;0m' == clr._byte(0, 0)

    for fg in range(0, 256):
        assert '\x1b[38;5;{}m'.format(fg) == clr._byte(fg, None)
        assert '\x1b[38;5;{}m \x1b[0m'.format(fg) == clr.color(' ', fg, None, mode='byte')

        for bg in range(0, 256):
            assert '\x1b[48;5;{}m'.format(bg) == clr._byte(None, bg)
            assert '\x1b[48;5;{}m \x1b[0m'.format(bg) == clr.color(' ', None, bg, mode='byte')

            assert '\x1b[38;5;{};48;5;{}m'.format(fg, bg) == clr._byte(fg, bg)
            assert '\x1b[38;5;{};48;5;{}m \x1b[0m'.format(fg, bg) == clr.color(' ', fg, bg, mode='byte')

    with pytest.raises(ValueError):
        clr._byte(-15, None)

    with pytest.raises(ValueError):
        clr._byte(256, None)

    with pytest.raises(ValueError):
        clr._byte('25', None)

    with pytest.raises(ValueError):
        clr._byte(None, -15)

    with pytest.raises(ValueError):
        clr._byte(None, 256)

    with pytest.raises(ValueError):
        clr._byte(None, '25')


def test_hex2rgb():
    good = list(range(0, 256))

    for i in range(100):
        r, g, b = choice(good), choice(good), choice(good)

        h = '{}{}{}'.format(
            hex(r)[2:].rjust(2, str('0')),
            hex(g)[2:].rjust(2, str('0')),
            hex(b)[2:].rjust(2, str('0')),
        )

        assert (r, g, b) == clr._hex2rgb(h)
        assert (r, g, b) == clr._hex2rgb('0x' + h)

    for i in range(16):
        h = hex(i)[2:]
        c = int(h + h, base=16)

        assert (c, c, c) == clr._hex2rgb(h + h + h)
        assert (c, c, c) == clr._hex2rgb('0x' + h + h + h)

    with pytest.raises(ValueError):
        clr._hex2rgb('absd')


def test_rgb(tty):
    assert '' == clr._rgb(None, None)
    assert '\x1b[38;2;0;0;0m' == clr._rgb((0, 0, 0), None)
    assert '\x1b[38;2;0;0;0;48;2;0;0;0m' == clr._rgb((0, 0, 0), (0, 0, 0))

    for fg in range(0, 256):
        assert '\x1b[38;2;{};{};{}m'.format(fg, fg, fg) == clr._rgb((fg, fg, fg), None)
        assert '\x1b[38;2;{};{};{}m \x1b[0m'.format(fg, fg, fg) == clr.color(' ', (fg, fg, fg), None, mode='rgb')

        fgh = hex(fg)[2:].rjust(2, str('0'))
        assert '\x1b[38;2;{};{};{}m \x1b[0m'.format(fg, fg, fg) == clr.color(' ', fgh + fgh + fgh, None, mode='rgb')
        assert ('\x1b[38;2;{};{};{}m \x1b[0m'.format(fg, fg, fg) ==
                clr.color(' ', '0x' + fgh + fgh + fgh, None, mode='rgb'))

        for bg in range(0, 256):
            assert '\x1b[48;2;{};{};{}m'.format(bg, bg, bg) == clr._rgb(None, (bg, bg, bg))
            assert '\x1b[48;2;{};{};{}m \x1b[0m'.format(bg, bg, bg) == clr.color(' ', None, (bg, bg, bg), mode='rgb')

            bgh = hex(bg)[2:].rjust(2, str('0'))
            assert '\x1b[48;2;{};{};{}m \x1b[0m'.format(bg, bg, bg) == clr.color(' ', None, bgh + bgh + bgh, mode='rgb')
            assert ('\x1b[48;2;{};{};{}m \x1b[0m'.format(bg, bg, bg) ==
                    clr.color(' ', None, '0x' + bgh + bgh + bgh, mode='rgb'))

            assert ('\x1b[38;2;{};{};{};48;2;{};{};{}m'.format(fg, fg, fg, bg, bg, bg) ==
                    clr._rgb((fg, fg, fg), (bg, bg, bg)))
            assert ('\x1b[38;2;{};{};{};48;2;{};{};{}m \x1b[0m'.format(fg, fg, fg, bg, bg, bg) ==
                    clr.color(' ', (fg, fg, fg), (bg, bg, bg), mode='rgb'))

    with pytest.raises(ValueError):
        clr._rgb(-15, None)

    with pytest.raises(ValueError):
        clr._rgb((-1, 1, 1), None)

    with pytest.raises(ValueError):
        clr._rgb((1, 1), None)

    with pytest.raises(ValueError):
        clr._rgb(None, -15)

    with pytest.raises(ValueError):
        clr._rgb(None, (-1, 1, 1))

    with pytest.raises(ValueError):
        clr._rgb(None, (1, 1))
