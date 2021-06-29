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
    assert len(x) == len(y)
    for idx1 in range(0, len(x)):
        x1 = x[idx1]
        y1 = y[idx1]
        # ellipse equation: https://en.wikipedia.org/wiki/Ellipse#Shifted_ellipse
        assert (x1 - x_center)**2 / x_amp**2 + (y1 - y_center) ** 2 / y_amp**2 == pytest.approx(1, abs=0.0001)


@pytest.mark.parametrize('angle', [45, 90, 135, 180, 225, 270, 315])
def test_ellipse_rotation(angle):
    x1, y1 = plt_data.ellipse(0, 0, angle=angle, x_amplitude=2, y_amplitude=1, n=100)
    fig1 = plt.Figure()
    fig1.set_x_limits(-2, 2)
    fig1.set_y_limits(-2, 2)
    fig1.plot(x1, y1)
    print(fig1.show())

    x2, y2 = plt_data.ellipse(0, 0, angle=360 - angle, x_amplitude=2, y_amplitude=1, n=100)
    fig2 = plt.Figure()
    fig2.set_x_limits(-2, 2)
    fig2.set_y_limits(-2, 2)
    fig2.plot(x2, y2)
    print(fig2.show())

    assert fig1.show() == fig2.show()


@pytest.mark.parametrize('n', [10, 20, 50, 100])
@pytest.mark.parametrize('radius', [1, 2, 5, 10])
def test_circle(n, radius):
    X1, Y1 = plt_data.ellipse(0, 0, x_amplitude=radius, y_amplitude=radius, n=n)
    X2, Y2 = plt_data.circle(0, 0, radius=radius, n=n)

    for x1, y1, x2, y2 in zip(X1, Y1, X2, Y2):
        assert x1 == pytest.approx(x2, abs=0.000001)
        assert y1 == pytest.approx(y2, abs=0.000001)


@pytest.mark.parametrize('angle', [45, 90, 135, 180, 225, 270, 315])
def test_circle_rotation(angle):
    x1, y1 = plt_data.ellipse(0, 0, angle=angle, x_amplitude=1, y_amplitude=1, n=100)
    fig1 = plt.Figure()
    fig1.set_x_limits(-2, 2)
    fig1.set_y_limits(-2, 2)
    fig1.plot(x1, y1)
    print(fig1.show())

    x2, y2 = plt_data.circle(0, 0, radius=1, n=100)
    fig2 = plt.Figure()
    fig2.set_x_limits(-2, 2)
    fig2.set_y_limits(-2, 2)
    fig2.plot(x2, y2)
    print(fig2.show())

    assert fig1.show() == fig2.show()
