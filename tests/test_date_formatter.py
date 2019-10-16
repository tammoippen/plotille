# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import date, timedelta
import pytest

from plotille._input_formatter import _convert_date, _date_formatter


@pytest.fixture()
def date_a():
    return date(2019, 1, 2)


@pytest.fixture()
def day():
    return timedelta(days=1)


def test_days(date_a, day):
    assert ' 19-01-02' == _date_formatter(date_a, chars=9, delta=day*15)
    assert '19-01-02 ' == _date_formatter(date_a, chars=9, delta=day*15, left=True)

    assert '  2019-01-02' == _date_formatter(date_a, chars=12, delta=day*15)
    assert '2019-01-02  ' == _date_formatter(date_a, chars=12, delta=day*15, left=True)

    with pytest.raises(ValueError):
        _date_formatter(date_a, chars=7, delta=day*15)


def test_converter(date_a):
    assert (date_a - date(1970, 1, 1)).days == _convert_date(date_a)
