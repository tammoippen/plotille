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

import colorsys
import os
import sys


def color(text, fg=None, bg=None, mode='names', no_color=False, full_reset=True):  # noqa: C901 complex (12)
    """Surround `text` with control characters for coloring

    c.f. http://en.wikipedia.org/wiki/ANSI_escape_code

    There are 3 color modes possible:
        - `names`:  corresponds to 3/4 bit encoding; provide colors as lower case
                    with underscore names, e.g. 'red', 'bright_green'
        - `byte`: corresponds to 8-bit encoding; provide colors as int ∈ [0, 255];
                  compare 256-color lookup table
        - `rgb`: corresponds to 24-bit encoding; provide colors either in 3- or 6-character
                 hex encoding or provide as a list / tuple with three ints (∈ [0, 255] each)

    With `fg` you can specify the foreground, i.e. text color, and with `bg` you
    specify the background color. The resulting `text` also gets the `RESET` signal
    at the end, s.t. no coloring swaps over to following text!

    Make sure to set the colors corresponding to the `mode`, otherwise you get
    `ValueErrors`.

    If you do not want a foreground or background color, leave the corresponding
    paramter `None`. If both are `None`, you get `text` directly.

    When you stick to mode `names` and only use the none `bright_` versions,
    the color control characters conform to ISO 6429 and the ANSI Escape sequences
    as defined in http://ascii-table.com/ansi-escape-sequences.php.

    Color names for mode `names` are:
        black red green yellow blue magenta cyan white     <- ISO 6429
        bright_black bright_red bright_green bright_yellow
        bright_blue bright_magenta bright_cyan bright_white
    (trying other names will raise ValueError)

    If you want to use colorama (https://pypi.python.org/pypi/colorama), you should
    also stick to the ISO 6429 colors.

    The environment variables `NO_COLOR` (https://no-color.org/) and `FORCE_COLOR`
    (only toggle; see https://nodejs.org/api/tty.html#tty_writestream_getcolordepth_env)
    have some influence on color output.

    If you do not run in a TTY, e.g. pipe to some other program or redirect output
    into a file, color codes are stripped as well.

    Parameters:
        text: str        Some text to surround.
        fg: multiple     Specify the foreground / text color.
        bg: multiple     Specify the background color.
        color_mode: str  Specify color input mode; 'names' (default), 'byte' or 'rgb'
        no_color: bool   Remove color optionally. default=False
        full_reset: bool Reset all codes or only color codes. default=True

    Returns:
        str: `text` enclosed with corresponding coloring controls
    """
    if fg is None and bg is None:
        return text

    if no_color or os.environ.get('NO_COLOR'):
        #  https://no-color.org/
        return text

    # similar to https://nodejs.org/api/tty.html#tty_writestream_getcolordepth_env
    # except for only on or of
    force_color = os.environ.get('FORCE_COLOR')
    if force_color:
        force_color = force_color.strip().lower()
        if force_color in ('0', 'false', 'none'):
            return text

    if not force_color and not _isatty():
        # only color if tty (not a redirect / pipe)
        return text

    start = ''
    if mode == 'names':
        start = _names(fg, bg)
    elif mode == 'byte':
        start = _byte(fg, bg)
    elif mode == 'rgb':
        if isinstance(fg, str):
            fg = _hex2rgb(fg)
        if isinstance(bg, str):
            bg = _hex2rgb(bg)

        start = _rgb(fg, bg)
    else:
        raise ValueError('Invalid mode "{}". Use one of "names", "byte" or "rgb".'.format(mode))

    assert start
    res = start + text
    if full_reset:
        return res + '\x1b[0m'
    else:
        return res + '\x1b[39;49m'


def hsl(hue, saturation, lightness):
    """Convert HSL color space into RGB color space.

    In contrast to colorsys.hls_to_rgb, this works directly in
    360 deg Hue and give RGB values in the range of 0 to 255.

    Parameters:
        hue: float         Position in the spectrum. 0 to 360.
        saturation: float  Color saturation. 0 to 1.
        lightness: float   Color lightness. 0 to 1.
    """
    assert 0 <= hue <= 360
    assert 0 <= saturation <= 1
    assert 0 <= lightness <= 1

    r, g, b = colorsys.hls_to_rgb(hue / 360.0, lightness, saturation)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def rgb2byte(r, g, b):
    """Convert RGB values into an index for the byte color-mode.

    Parameters:
        r: int    Red value. Between 0 and 255.
        g: int    Green value. Between 0 and 255.
        b: int    Blue value. Between 0 and 255.

    Returns
        idx: int  Index of approximate color in the byte color-mode.
    """
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255

    if r == g == b < 244:
        # gray:
        gray_idx = _value_to_index(min(238, r), off=8, steps=10)
        return gray_idx + 232

    # here we also have some gray values ...
    r_idx = _value_to_index(r)
    g_idx = _value_to_index(g)
    b_idx = _value_to_index(b)

    return 16 + 36 * r_idx + 6 * g_idx + b_idx


def _value_to_index(v, off=55, steps=40):
    idx = (v - off) / steps
    if idx < 0:
        return 0
    return int(round(idx))


def _isatty():
    return sys.stdout.isatty()


def _names(fg, bg):
    """3/4 bit encoding part

    c.f. https://en.wikipedia.org/wiki/ANSI_escape_code#3.2F4_bit

    Parameters:

    """
    if not (fg is None or fg in _FOREGROUNDS):
        raise ValueError('Invalid color name fg = "{}"'.format(fg))
    if not (bg is None or bg in _BACKGROUNDS):
        raise ValueError('Invalid color name bg = "{}"'.format(bg))

    fg_ = _FOREGROUNDS.get(fg, '')
    bg_ = _BACKGROUNDS.get(bg, '')

    return _join_codes(fg_, bg_)


def _byte(fg, bg):
    """8-bite encoding part

    c.f. https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    """
    if not (fg is None or (isinstance(fg, int) and 0 <= fg <= 255)):
        raise ValueError('Invalid fg = {}. Allowed int in [0, 255].'.format(fg))
    if not (bg is None or (isinstance(bg, int) and 0 <= bg <= 255)):
        raise ValueError('Invalid bg = {}. Allowed int in [0, 255].'.format(bg))

    fg_ = ''
    if fg is not None:
        fg_ = '38;5;' + str(fg)
    bg_ = ''
    if bg is not None:
        bg_ = '48;5;' + str(bg)

    return _join_codes(fg_, bg_)


def _hex2rgb(h):
    """Transform rgb hex representation into rgb tuple of ints representation"""
    assert isinstance(h, str)
    if h.lower().startswith('0x'):
        h = h[2:]
    if len(h) == 3:
        return (int(h[0] * 2, base=16), int(h[1] * 2, base=16), int(h[2] * 2, base=16))
    if len(h) == 6:
        return (int(h[0:2], base=16), int(h[2:4], base=16), int(h[4:6], base=16))

    raise ValueError('Invalid hex RGB value.')


def _rgb(fg, bg):
    """24-bit encoding part

    c.f. https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
    """
    if not (fg is None or (isinstance(fg, (list, tuple)) and len(fg) == 3) and all(0 <= f <= 255 for f in fg)):
        raise ValueError('Foreground fg either None or 3-tuple: {}'.format(fg))
    if not (bg is None or (isinstance(bg, (list, tuple)) and len(bg) == 3) and all(0 <= b <= 255 for b in bg)):
        raise ValueError('Foreground fg either None or 3-tuple: {}'.format(bg))

    fg_ = ''
    if fg is not None:
        fg_ = '38;2;' + ';'.join(map(str, fg))
    bg_ = ''
    if bg is not None:
        bg_ = '48;2;' + ';'.join(map(str, bg))

    return _join_codes(fg_, bg_)


def _join_codes(fg, bg):
    """Join `fg` and `bg` with ; and surround with correct esc sequence."""
    colors = ';'.join(filter(lambda c: len(c) > 0, (fg, bg)))
    if colors:
        return '\x1b[' + colors + 'm'

    return ''


_BACKGROUNDS = {
    'black': '40',
    'red': '41',
    'green': '42',
    'yellow': '43',
    'blue': '44',
    'magenta': '45',
    'cyan': '46',
    'white': '47',
    'bright_black': '100',
    'bright_red': '101',
    'bright_green': '102',
    'bright_yellow': '103',
    'bright_blue': '104',
    'bright_magenta': '105',
    'bright_cyan': '106',
    'bright_white': '107',
    'bright_black_old': '1;40',
    'bright_red_old': '1;41',
    'bright_green_old': '1;42',
    'bright_yellow_old': '1;43',
    'bright_blue_old': '1;44',
    'bright_magenta_old': '1;45',
    'bright_cyan_old': '1;46',
    'bright_white_old': '1;47',
}

_FOREGROUNDS = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
    'bright_black': '90',
    'bright_red': '91',
    'bright_green': '92',
    'bright_yellow': '93',
    'bright_blue': '94',
    'bright_magenta': '95',
    'bright_cyan': '96',
    'bright_white': '97',
    'bright_black_old': '1;30',
    'bright_red_old': '1;31',
    'bright_green_old': '1;32',
    'bright_yellow_old': '1;33',
    'bright_blue_old': '1;34',
    'bright_magenta_old': '1;35',
    'bright_cyan_old': '1;36',
    'bright_white_old': '1;37',
}
