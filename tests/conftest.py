# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest


@pytest.fixture()
def get_canvas(mocker):
    def get():
        canvas = mocker.Mock()
        canvas.point = mocker.Mock()
        canvas.line = mocker.Mock()

        return canvas

    return get


@pytest.fixture()
def tty(mocker):
    mocker.patch('plotille._colors._isatty', return_value=True)


@pytest.fixture()
def notty(mocker):
    mocker.patch('plotille._colors._isatty', return_value=False)
