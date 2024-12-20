


import inspect
import os

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


@pytest.fixture()
def cleandoc():
    def f(s):
        return inspect.cleandoc(s).replace('\n', os.linesep)

    return f
