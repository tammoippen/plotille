import pytest


@pytest.fixture()
def get_canvas(mocker):
    def get():
        canvas = mocker.Mock()
        canvas.point = mocker.Mock()
        canvas.line = mocker.Mock()

        return canvas

    return get
