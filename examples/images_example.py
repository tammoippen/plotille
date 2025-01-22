# The MIT License

# Copyright (c) 2017 - 2024 Tammo Ippen, tammo.ippen@posteo.de

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
except ImportError as e:
    raise Exception("Need to have PIL / pillow installed for this example.") from e

from plotille import Canvas, Figure

current_dir = os.path.dirname(os.path.abspath(__file__))


def canvas_dots():
    # Canvas on its own can draw an image using dots
    img = Image.open(current_dir + "/../imgs/ich.jpg")
    img = img.convert("L")
    img = img.resize((80, 80))
    cvs = Canvas(40, 20)
    cvs.braille_image(img.getdata())

    print("\nImage with braille dots:")
    print(cvs.plot())


def figure_image():
    # Figure can draw an image using the background color of characters
    width = 80
    height = 40
    img = Image.open(current_dir + "/../imgs/ich.jpg")
    img = img.convert("RGB")
    img = img.resize((width, height))
    # we need the data as height x width array of rgb values
    data = img.getdata()
    data = [[data[row * width + col] for col in range(width)] for row in range(height)]

    fig = Figure()
    fig.width = width
    fig.height = height
    # only rgb and byte are supported right now
    fig.color_mode = "byte"

    fig.imgshow(data)

    print("\nImage with rgb values in the background:")
    print(fig.show())


def figure_cmap():
    # Figure can draw an image using the background color of characters
    width = 80
    height = 40
    img = Image.open(current_dir + "/../imgs/ich.jpg")
    # only luminance here
    img = img.convert("L")
    img = img.resize((width, height))
    # we need the data as height x width array of luminance values
    data = img.getdata()
    data = [[data[row * width + col] for col in range(width)] for row in range(height)]

    for cmap in ["gray", "plasma"]:
        fig = Figure()
        fig.width = width
        fig.height = height
        # only rgb and byte are supported right now
        fig.color_mode = "byte"

        print(
            f'\nImage with luminance values only in the background using "{cmap}" cmap:'
        )
        fig.imgshow(data, cmap=cmap)

        print(fig.show())


def figure_cmap_handcrafted():
    # Figure can draw an image using the background color of characters
    width = 80
    height = 40

    data = [[None for col in range(width)] for row in range(height)]

    for x in range(10):
        for y in range(10):
            data[20 - y][40 - x] = 20 - x - y
            data[20 - y][40 + x] = 20 - x - y
            data[20 + y][40 + x] = 20 - x - y
            data[20 + y][40 - x] = 20 - x - y

    for cmap in ["gray", "plasma"]:
        fig = Figure()
        fig.width = width
        fig.height = height
        # only rgb and byte are supported right now
        fig.color_mode = "byte"

        print('\nSome data using color in the background using "{}" cmap:'.format(cmap))
        fig.imgshow(data, cmap=cmap)

        # you can plot whatever you want on top of it
        fig.plot([0, 1], [0, 1])

        print(fig.show())


def main():
    canvas_dots()
    figure_image()
    figure_cmap()
    figure_cmap_handcrafted()


if __name__ == "__main__":
    main()
