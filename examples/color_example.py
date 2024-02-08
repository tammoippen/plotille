# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2024 Tammo Ippen, tammo.ippen@posteo.de

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

import os

from plotille import color


def main():
    print(color('Do not print colors, if `no_color` is set to True', fg='red', no_color=True))
    print(color('You can set a foreground', fg='red'))
    print(color('and a background.', bg='red'))
    print(color('Or both.', fg='black', bg='cyan'))

    print(color('Asside from 4-bit / name colors', fg='green', mode='names'))
    print(color('you can also set 8-bit colors / 256-color lookup tables', fg=126, bg=87, mode='byte'))
    print(color('or go with full 24-bit rgb colors', fg=(50, 50, 50), bg=(166, 237, 240), mode='rgb'))

    no_color = os.environ.get('NO_COLOR')
    os.environ['NO_COLOR'] = '1'
    print(color('The Environmnet variable `NO_COLOR` will always strip colors.', fg='red'))
    if no_color:
        os.environ['NO_COLOR'] = no_color
    else:
        os.environ.pop('NO_COLOR')

    force_color = os.environ.get('FORCE_COLOR')
    os.environ['FORCE_COLOR'] = '1'
    print(color('The Environmnet variable `FORCE_COLOR` allows to toggle colors,', fg='blue'))
    os.environ['FORCE_COLOR'] = '0'
    print(color('setting it to 0, none or false, strips color codes', fg='magenta'))
    os.environ['FORCE_COLOR'] = '1'
    print(color('everything else forces color codes', fg='green'))
    if force_color:
        os.environ['FORCE_COLOR'] = force_color
    else:
        os.environ.pop('FORCE_COLOR')


if __name__ == '__main__':
    main()
