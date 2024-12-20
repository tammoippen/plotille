


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

import plotille


def main():
    draw_scene([[-36, 108], [-36, 108.2], [-35.1, 108]], [[-35.4, 108]])


def draw_scene(mouse_list, cat_list):
    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    listx = []
    listy = []
    names = []
    for idx, mouse in enumerate(mouse_list):
        listx.append(mouse[0])
        listy.append(mouse[1])
        names.append('o MOUSE {}'.format(idx))

    fig.text(listy, listx, names, lc='red')

    listx = []
    listy = []
    for cat in cat_list:
        listx.append(cat[0])
        listy.append(cat[1])

    fig.scatter(listy, listx, lc='green', label='Cat', marker='x')

    print(fig.show(legend=True))


if __name__ == '__main__':
    main()
