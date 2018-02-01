# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from pendulum import datetime, interval
from plotille._input_formatter import _convert_datetime, _datetime_formatter
import pytest


@pytest.fixture()
def date():
    return datetime(2018, 1, 21, 15, 3, 12, 1234)


@pytest.fixture()
def day():
    return interval(days=1)


@pytest.fixture()
def hour():
    return interval(hours=1)


def test_days(date, day):
    assert ' 18-01-21' == _datetime_formatter(date, chars=9, delta=day*15)
    assert '18-01-21 ' == _datetime_formatter(date, chars=9, delta=day*15, left=True)

    assert '  2018-01-21' == _datetime_formatter(date, chars=12, delta=day*15)
    assert '2018-01-21  ' == _datetime_formatter(date, chars=12, delta=day*15, left=True)

    with pytest.raises(ValueError):
        _datetime_formatter(date, chars=7, delta=day*15)


def test_day_times(date, day):
    assert ' 21T15:03' == _datetime_formatter(date, chars=9, delta=day*5)
    assert '21T15:03 ' == _datetime_formatter(date, chars=9, delta=day*5, left=True)

    assert ' 21T15:03:12' == _datetime_formatter(date, chars=12, delta=day*5)
    assert '21T15:03:12 ' == _datetime_formatter(date, chars=12, delta=day*5, left=True)

    with pytest.raises(ValueError):
        _datetime_formatter(date, chars=7, delta=day*5)


def test_times(date, hour):
    assert ' 15:03:12' == _datetime_formatter(date, chars=9, delta=hour*5)
    assert '15:03:12 ' == _datetime_formatter(date, chars=9, delta=hour*5, left=True)

    assert ' 15:03:12.001234' == _datetime_formatter(date, chars=16, delta=hour*5)
    assert '15:03:12.001234 ' == _datetime_formatter(date, chars=16, delta=hour*5, left=True)

    with pytest.raises(ValueError):
        _datetime_formatter(date, chars=7, delta=hour*5)


def test_converter(date):
    assert date.timestamp() == _convert_datetime(date)
