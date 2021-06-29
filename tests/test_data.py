# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random

import pytest

import plotille as plt
import plotille.data as plt_data


@pytest.mark.parametrize('n', [10, 20, 50, 100])
@pytest.mark.parametrize('x_amp', [1, 2, 5, 10])
@pytest.mark.parametrize('y_amp', [1, 2, 5, 10])
def test_ellipse_formula(n, x_amp, y_amp):
    x_center = random.random()
    y_center = random.random()
    x, y = plt_data.ellipse(x_center, y_center, x_amplitude=x_amp, y_amplitude=y_amp, n=n)
    assert x[0] == pytest.approx(x[-1], abs=0.0001)
    assert y[0] == pytest.approx(y[-1], abs=0.0001)

    assert len(x) == len(y)
    for idx1 in range(0, len(x)):
        x1 = x[idx1]
        y1 = y[idx1]
        # ellipse equation: https://en.wikipedia.org/wiki/Ellipse#Shifted_ellipse
        assert (x1 - x_center)**2 / x_amp**2 + (y1 - y_center) ** 2 / y_amp**2 == pytest.approx(1, abs=0.0001)


@pytest.mark.parametrize('angle', [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75])
def test_ellipse_rotation(angle):
    x1, y1 = plt_data.ellipse(0, 0, angle=angle * math.pi, x_amplitude=2, y_amplitude=1, n=100)
    fig1 = plt.Figure()
    fig1.set_x_limits(-2, 2)
    fig1.set_y_limits(-2, 2)
    fig1.plot(x1, y1)
    print(fig1.show())

    x2, y2 = plt_data.ellipse(0, 0, angle=(2 + angle) * math.pi, x_amplitude=2, y_amplitude=1, n=100)
    fig2 = plt.Figure()
    fig2.set_x_limits(-2, 2)
    fig2.set_y_limits(-2, 2)
    fig2.plot(x2, y2)
    print(fig2.show())

    assert fig1.show() == fig2.show()


@pytest.mark.parametrize('n', [10, 20, 50, 100])
@pytest.mark.parametrize('radius', [1, 2, 5, 10])
def test_circle(n, radius):
    X1, Y1 = plt_data.ellipse(0, 0, x_amplitude=radius, y_amplitude=radius, n=n)  # noqa: N806
    X2, Y2 = plt_data.circle(0, 0, radius=radius, n=n)  # noqa: N806

    for x1, y1, x2, y2 in zip(X1, Y1, X2, Y2):
        assert x1 == pytest.approx(x2, abs=0.000001)
        assert y1 == pytest.approx(y2, abs=0.000001)


@pytest.mark.parametrize('radius', range(1, 11))
def test_circle(radius):
    X, Y = plt_data.circle(0, 0, radius=radius**10, n=100)  # noqa: N806
    # complete
    assert X[0] == pytest.approx(X[-1], abs=0.001)
    assert Y[0] == pytest.approx(Y[-1], abs=0.001)

    for x, y in zip(X, Y):
        assert math.sqrt(x**2 + y**2) == pytest.approx(radius**10, abs=0.001)
        equal = 0
        for x2, y2 in zip(X, Y):
            if x2 == x and y2 == y:
                equal += 1
        assert equal <= 2
