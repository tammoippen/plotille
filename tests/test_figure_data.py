import pytest

from plotille._canvas import Canvas
from plotille._cmaps import cmaps
from plotille._figure_data import Heat


@pytest.mark.parametrize('name', cmaps.keys())
def test_heat_by_name(tty, name):
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
    cvs = Canvas(width, height, mode='rgb')

    heat.write(cvs, True, None)

    # print()
    # print(cvs.plot())


@pytest.mark.parametrize('name', cmaps.keys())
def test_heat_by_cmap(tty, name):
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
    cvs = Canvas(width, height, mode='rgb')

    heat.write(cvs, True, None)

    # print()
    # print(cvs.plot())
