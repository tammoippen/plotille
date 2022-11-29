# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2022 Tammo Ippen, tammo.ippen@posteo.de

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

from ._colors import color

# I plot upside down, hence the different order
_xy2dot = [
    [1 << 6, 1 << 7],
    [1 << 2, 1 << 5],
    [1 << 1, 1 << 4],
    [1 << 0, 1 << 3],
]


class Dots(object):
    """A Dots object is responsible for printing requested braille dots and colors

    Dot ordering: \u2800 '⠀' - \u28FF '⣿'' Coding according to ISO/TR 11548-1

        Hence, each dot on or off is 8bit, i.e. 256 posibilities. With dot number
        one being the lsb and 8 is msb:

        idx:  8 7 6 5 4 3 2 1
        bits: 0 0 0 0 0 0 0 0

        Ordering of dots:

        1  4
        2  5
        3  6
        7  8
    """
    def __init__(self, marker=None, fg=None, bg=None, **color_kwargs):
        """Create a Dots object

        Parameters:
            dots: List[int]  With set dots to on; ∈ 1 - 8
            marker: str      Set a marker instead of braille dots.
            fg: str          Color of dots
            bg: str          Color of background
            **color_kwargs:  More arguments to the color-function. See `plotille.color()`.

        Returns:
            Dots
        """
        assert marker is None or len(marker) == 1
        self._dots = 0
        self._marker = marker
        self.fg = fg
        self.bg = bg
        self._color_kwargs = color_kwargs
        if 'mode' not in self._color_kwargs:
            self._color_kwargs['mode'] = 'names'

    @property
    def color_kwargs(self):
        return self._color_kwargs

    @property
    def dots(self):
        assert self._dots.bit_length() <= 8
        dots = []
        x = self._dots
        bit = 1
        while x != 0:
            if x & 1 == 1:
                dots.append(bit)
            bit += 1
            x >>= 1
        return sorted(dots)

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, value):
        assert value is None or isinstance(value, str)
        assert value is None or len(value) == 1
        self._marker = value

    def __repr__(self):
        return 'Dots(dots={}, marker={}, fg={}, bg={}, color_kwargs={})'.format(
            self.dots, self.marker, self.fg, self.bg,
            ' '.join('{}: {}'.format(k, v) for k, v in self.color_kwargs.items()),
        )

    def __str__(self):
        if self.marker:
            res = self.marker
        else:
            res = chr(0x2800 + self._dots)

        return color(res, fg=self.fg, bg=self.bg, **self.color_kwargs)

    def fill(self):
        self._dots = 0xFF

    def clear(self):
        self._dots = 0
        self.marker = None

    def update(self, x, y, set_=True, marker=None):
        """(Un)Set dot at position x, y, with (0, 0) is top left corner.

        Parameters:
            x: int      x-coordinate ∈ [0, 1]
            y: int      y-coordinate ∈ [0, 1, 2, 3]
            set_: bool  True, sets dot, False, removes dot
            marker: str Instead of braille dots set a marker char.
        """

        if set_:
            self._dots |= _xy2dot[y][x]
            if marker:
                self.marker = marker
        else:
            self._dots = self._dots & (_xy2dot[y][x] ^ 0xFF)
            self.marker = None


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

    return chr(code)


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

    code = str(bin(ord(braille) - 0x2800))[2:].rjust(8, '0')

    dots = []
    for i, c in enumerate(code):
        if c == '1':
            dots += [8 - i]

    return sorted(dots)
