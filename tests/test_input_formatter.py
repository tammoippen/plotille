# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from pendulum import datetime, interval
from plotille._input_formatter import InputFormatter


def test_defaults():
    ipf = InputFormatter()

    assert '        1' == ipf.fmt(1, 0)
    assert '1        ' == ipf.fmt(1, 0, left=True)

    assert 1.0 == ipf.convert(1)

    d = datetime(2018, 1, 21, 15, 3, 12, 1234)
    t = interval(hours=1)

    assert ' 15:03:12' == ipf.fmt(d, t)
    assert '15:03:12 ' == ipf.fmt(d, t, left=True)

    assert 1516546992.001234 == ipf.convert(d)

    # no formatter available
    assert 'None' == ipf.fmt(None, 0)
    assert 'hello' == ipf.convert('hello')


def test_register():
    def bool_fmt(val, chars, delta, left=False):
        res = str(val)

        if left:
            return res.ljust(chars)
        else:
            return res.rjust(chars)

    def bool_cvt(val):
        return int(val)

    ipf = InputFormatter()
    ipf.register_formatter(bool, bool_fmt)

    assert '  True' == ipf.fmt(True, chars=6, delta=None)
    assert 'True  ' == ipf.fmt(True, chars=6, delta=None, left=True)

    ipf.register_converter(bool, bool_cvt)

    assert 1 == ipf.convert(True)
    assert 0 == ipf.convert(False)
