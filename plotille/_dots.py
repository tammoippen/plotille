# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2018 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import six

from ._colors import color


class Dots(object):
    """A Dots object is responsible for printing requested braille dots and colors

    Dot ordering: \u2800 '⠀' - \u28FF '⣿'' Coding according to ISO/TR 11548-1

        Hence, each dot on or off is 8bit, i.e. 256 posibilities. With dot number
        one being the msb and 8 is lsb:

        idx:  1 2 3 4 5 6 7 8
        bits: 0 0 0 0 0 0 0 0

        Ordering of dots:

        1  4
        2  5
        3  6
        7  8
    """
    def __init__(self, dots=None, fg=None, bg=None, color_mode='names'):
        """Create a Dots object

        Parameters:
            dots: List[int]  With set dots to on; ∈ 1 - 8
            fg: str          Color of dots
            bg: str          Color of background
            color_mode: str  Define the used color mode. See `plotille.color()`.

        Returns:
            Dots
        """
        if dots is None:
            dots = []
        self.dots = dots
        self.fg = fg
        self.bg = bg
        self._mode = color_mode

    @property
    def mode(self):
        return self._mode

    @property
    def dots(self):
        return list(self._dots)

    @dots.setter
    def dots(self, value):
        assert isinstance(value, (list, tuple))
        assert all(map(lambda x: 1 <= x <= 8, value))
        self._dots = list(value)

    def __repr__(self):
        return 'Dots(dots={}, fg={}, bg={}, color_mode={})'.format(self.dots, self.fg, self.bg, self.mode)

    def __str__(self):
        res = braille_from(self.dots)

        return color(res, fg=self.fg, bg=self.bg, mode=self.mode)

    def fill(self):
        self.dots = [1, 2, 3, 4, 5, 6, 7, 8]

    def clear(self):
        self.dots = []

    def update(self, x, y, set_=True):
        """(Un)Set dot at position x, y, with (0, 0) is top left corner.

        Parameters:
            x: int      x-coordinate ∈ [0, 1]
            y: int      y-coordinate ∈ [0, 1, 2, 3]
            set_: bool  True, sets dot, False, removes dot
        """
        xy2dot = [[7, 8],  # I plot upside down, hence the different order
                  [3, 6],
                  [2, 5],
                  [1, 4]]
        if set_:
            self.dots = sorted(set(self.dots) | {xy2dot[y][x]})
        else:
            idx = xy2dot[y][x]
            if idx in self._dots:
                self._dots.remove(idx)


def braille_from(dots):
    """Unicode character for braille with given dots set

    See https://en.wikipedia.org/wiki/Braille_Patterns#Identifying.2C_naming_and_ordering
    for dot to braille encoding.

    Parameters:
        dots: List[int]  All dots that should be set. Allowed dots are 1,2,3,4,5,6,7,8

    Returns:
        unicode: braille sign with given dots set. \u2800 - \u28ff
    """
    bin_code = ['0'] * 8
    for i in dots:
        bin_code[8 - i] = '1'

    code = 0x2800 + int(''.join(bin_code), 2)

    return six.unichr(code)


def dots_from(braille):
    """Get set dots from given

    See https://en.wikipedia.org/wiki/Braille_Patterns#Identifying.2C_naming_and_ordering
    for braille to dot decoding.

    Parameters:
        braille: unicode  Braille character in \u2800 - \u28ff

    Returns:
        List[int]: dots that are set in braille sign
    """
    assert 0x2800 <= ord(braille) <= 0x28ff

    code = six.text_type(bin(ord(braille) - 0x2800))[2:].rjust(8, '0')

    dots = []
    for i, c in enumerate(code):
        if c == '1':
            dots += [8 - i]

    return sorted(dots)
