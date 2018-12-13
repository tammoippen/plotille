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

import sys

import six


def color(text, fg=None, bg=None, mode='names', no_color=False):
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

    Parameters:
        text: str        Some text to surround.
        fg: multiple     Specify the foreground / text color.
        bg: multiple     Specify the background color.
        color_mode: str  Specify color input mode; 'names' (default), 'byte' or 'rgb'
        no_color: bool   Remove color optionally. default=False

    Returns:
        str: `text` enclosed with corresponding coloring controls
    """
    if fg is None and bg is None:
        return text

    if not _isatty() or no_color:
        # only color if tty (not a redirect / pipe)
        return text

    start = ''
    if mode == 'names':
        start = _names(fg, bg)
    elif mode == 'byte':
        start = _byte(fg, bg)
    elif mode == 'rgb':
        if isinstance(fg, six.string_types):
            fg = _hex2rgb(fg)
        if isinstance(bg, six.string_types):
            bg = _hex2rgb(bg)

        start = _rgb(fg, bg)
    else:
        raise ValueError('Invalid mode "{}". Use one of "names", "byte" or "rgb".'.format(mode))

    if start:
        return start + text + '\x1b[0m'

    # should not be reachable


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
        fg_ = '38;5;' + six.text_type(fg)
    bg_ = ''
    if bg is not None:
        bg_ = '48;5;' + six.text_type(bg)

    return _join_codes(fg_, bg_)


def _hex2rgb(h):
    """Transform rgb hex representation into rgb tuple of ints representation"""
    assert isinstance(h, six.string_types)
    if h.lower().startswith('0x'):
        h = h[2:]
    if len(h) == 3:
        return (int(h[0]*2, base=16), int(h[1]*2, base=16), int(h[2]*2, base=16))
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
        fg_ = '38;2;' + ';'.join(map(six.text_type, fg))
    bg_ = ''
    if bg is not None:
        bg_ = '48;2;' + ';'.join(map(six.text_type, bg))

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
    'bright_black': '1;30',
    'bright_red': '1;31',
    'bright_green': '1;32',
    'bright_yellow': '1;33',
    'bright_blue': '1;34',
    'bright_magenta': '1;35',
    'bright_cyan': '1;36',
    'bright_white': '1;37',
}
