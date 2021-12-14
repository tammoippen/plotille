# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2021 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

try:
    from PIL import Image
except ImportError:
    raise Exception('Need to have PIL / pillow installed for this example.')

from plotille import Canvas, hsl


current_dir = os.path.dirname(os.path.abspath(__file__))


def logo():
    # Canvas on its own can draw an image using dots
    img = Image.open(current_dir + '/../imgs/logo.png')
    img = img.convert('L')
    img = img.resize((270, 120))
    cvs = Canvas(135, 30, background=hsl(0, 0, 0.8), mode='rgb')
    cvs.braille_image(img.getdata(), inverse=True, color=hsl(0, 0.5, 0.4))

    print(cvs.plot())


def main():
    logo()


if __name__ == '__main__':
    main()
