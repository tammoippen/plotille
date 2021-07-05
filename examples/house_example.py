# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2021 Tammo Ippen, tammo.ippen@posteo.de

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

from plotille import Canvas


# The underlying canvas-implementation can be used on its own.

def main():
    c = Canvas(width=40, height=20)
    c.rect(0.1, 0.1, 0.6, 0.6)
    c.line(0.1, 0.1, 0.6, 0.6)
    c.line(0.1, 0.6, 0.6, 0.1)
    c.line(0.1, 0.6, 0.35, 0.8)
    c.line(0.35, 0.8, 0.6, 0.6)
    c.text(0.3, 0.5, 'hi', color='red')
    c.point(0.35, 0.35, color='blue')
    c.fill_char(0.35, 0.1)
    print(c.plot())


if __name__ == '__main__':
    main()
