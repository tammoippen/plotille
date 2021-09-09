from random import random

import pytest

from plotille._canvas import Canvas
from plotille._cmaps import cmaps
from plotille._figure_data import Heat


@pytest.mark.parametrize('mode', ['rgb', 'byte'])
@pytest.mark.parametrize('name', cmaps.keys())
def test_heat_by_name(tty, name, mode):
    width = 20
    height = 20
    xs = []
    for y in range(height):
        row = []
        y_val = (1.0 * y - height / 2) / height
        for x in range(width):
            x_val = (1.0 * x - width / 2) / width
            row.append(-1 * (x_val * x_val + y_val * y_val))
        xs.append(row)

    heat = Heat(xs, cmap=name)
    cvs = Canvas(width, height, mode=mode)

    heat.write(cvs)

    # print()
    # print(cvs.plot())


@pytest.mark.parametrize('mode', ['rgb', 'byte'])
@pytest.mark.parametrize('name', cmaps.keys())
def test_heat_by_cmap(tty, name, mode):
    width = 20
    height = 20
    xs = []
    for y in range(height):
        row = []
        y_val = (1.0 * y - height / 2) / height
        for x in range(width):
            x_val = (1.0 * x - width / 2) / width
            row.append(-1 * (x_val * x_val + y_val * y_val))
        xs.append(row)

    heat = Heat(xs, cmap=cmaps[name])
    cvs = Canvas(width, height, mode=mode)

    heat.write(cvs)

    # print()
    # print(cvs.plot())


@pytest.mark.parametrize('mode', ['rgb', 'byte'])
@pytest.mark.parametrize('normalized', [True, False])
def test_heat_of_image(tty, mode, normalized):
    width = 20
    height = 20
    xs = []
    for y in range(height):
        row = []
        y_val = y / height
        for x in range(width):
            x_val = x / width
            rgb = [y_val, x_val, random()]
            if not normalized:
                rgb = list(map(lambda z: round(z * 255), rgb))
            row.append(rgb)
        xs.append(row)

    heat = Heat(xs)
    cvs = Canvas(width, height, mode=mode)

    heat.write(cvs)

    # print()
    # print(cvs.plot())
