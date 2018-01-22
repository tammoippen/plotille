# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from plotille._input_formatter import _num_formatter
import pytest


def test_small_int():
    assert '        13' == _num_formatter(13, chars=10, delta=0)
    assert '        13' == _num_formatter(13.0000, chars=10, delta=0)
    assert '13        ' == _num_formatter(13, left=True, chars=10, delta=0)
    assert '    13' == _num_formatter(13, chars=6, delta=0)
    assert '123456' == _num_formatter(123456, chars=6, delta=0)


def test_negative_int():
    assert '       -13' == _num_formatter(-13, chars=10, delta=0)
    assert '       -13' == _num_formatter(-13.0000, chars=10, delta=0)
    assert '-13       ' == _num_formatter(-13, left=True, chars=10, delta=0)
    assert '   -13' == _num_formatter(-13, chars=6, delta=0)
    assert '-123456' == _num_formatter(-123456, chars=7, delta=0)


def test_large_int():
    assert '1234567890' == _num_formatter(1234567890, chars=10, delta=0)
    assert '1234567890' == _num_formatter(1234567890.0000, chars=10, delta=0)
    assert '1234567890' == _num_formatter(1234567890, left=True, chars=10, delta=0)

    assert '1.235e+09' == _num_formatter(1234567890, chars=9, delta=0)  # round
    assert '1.23e+09' == _num_formatter(1234567890, chars=8, delta=0)
    assert '1.2e+09' == _num_formatter(1234567890, chars=7, delta=0)
    assert ' 1e+09' == _num_formatter(1234567890, chars=6, delta=0)
    assert '1e+09' == _num_formatter(1234567890, chars=5, delta=0)

    with pytest.raises(ValueError):
        _num_formatter(1234567890, chars=4, delta=0)


def test_large_neg_int():
    assert '-234567890' == _num_formatter(-234567890, chars=10, delta=0)
    assert '-234567890' == _num_formatter(-234567890.0000, chars=10, delta=0)
    assert '-234567890' == _num_formatter(-234567890, left=True, chars=10, delta=0)

    assert '-1.235e+09' == _num_formatter(-1234567890, chars=10, delta=0)   # round
    assert '-1.23e+09' == _num_formatter(-1234567890, chars=9, delta=0)
    assert '-1.2e+09' == _num_formatter(-1234567890, chars=8, delta=0)
    assert ' -1e+09' == _num_formatter(-1234567890, chars=7, delta=0)
    assert '-1e+09' == _num_formatter(-1234567890, chars=6, delta=0)

    with pytest.raises(ValueError):
        _num_formatter(-1234567890, chars=5, delta=0)


def test_very_large_int():
    assert '1.235e+123' == _num_formatter(1.234567890e123, chars=10, delta=0)
    assert '1.235e+123' == _num_formatter(1.234567890e123, left=True, chars=10, delta=0)

    assert '1.23e+123' == _num_formatter(1.234567890e123, chars=9, delta=0)
    assert '1.2e+123' == _num_formatter(1.234567890e123, chars=8, delta=0)
    assert ' 1e+123' == _num_formatter(1.234567890e123, chars=7, delta=0)
    assert '1e+123' == _num_formatter(1.234567890e123, chars=6, delta=0)

    with pytest.raises(ValueError):
        _num_formatter(1.234567890e123, chars=5, delta=0)


def test_very_large_neg_int():
    assert '-2.35e+123' == _num_formatter(-2.34567890e123, chars=10, delta=0)
    assert '-2.35e+123' == _num_formatter(-2.34567890e123, left=True, chars=10, delta=0)

    assert '-2.3e+123' == _num_formatter(-2.34567890e123, chars=9, delta=0)
    assert ' -2e+123' == _num_formatter(-2.34567890e123, chars=8, delta=0)
    assert '-2e+123' == _num_formatter(-2.34567890e123, chars=7, delta=0)

    with pytest.raises(ValueError):
        _num_formatter(-2.34567890e123, chars=6, delta=0)


def test_floats():
    assert '1234.56000' == _num_formatter(1234.56, chars=10, delta=0)
    assert '123400.560' == _num_formatter(123400.56, chars=10, delta=0)
    assert '12340000.6' == _num_formatter(12340000.56, chars=10, delta=0)  # round
    assert ' 123400001' == _num_formatter(123400000.56, chars=10, delta=0)
    assert '1234000001' == _num_formatter(1234000000.56, chars=10, delta=0)
    assert '1.2340e+10' == _num_formatter(12340000004.56, chars=10, delta=0)


def test_neg_floats():
    assert '-1234.5600' == _num_formatter(-1234.56, chars=10, delta=0)
    assert '-123400.56' == _num_formatter(-123400.56, chars=10, delta=0)
    assert ' -12340001' == _num_formatter(-12340000.56, chars=10, delta=0)  # round
    assert '-123400001' == _num_formatter(-123400000.56, chars=10, delta=0)
    assert '-1.234e+09' == _num_formatter(-1234000004.56, chars=10, delta=0)


def test_small_floats():
    assert '0.12345600' == _num_formatter(0.123456, chars=10, delta=0)
    assert '0.01234560' == _num_formatter(0.0123456, chars=10, delta=0)
    assert '0.00123456' == _num_formatter(0.00123456, chars=10, delta=0)
    assert '0.00012346' == _num_formatter(0.000123456, chars=10, delta=0)
    assert '1.2346e-05' == _num_formatter(0.0000123456, chars=10, delta=0)


def test_small_neg_floats():
    assert '-0.1234560' == _num_formatter(-0.123456, chars=10, delta=0)
    assert '-0.0123456' == _num_formatter(-0.0123456, chars=10, delta=0)
    assert '-0.0012346' == _num_formatter(-0.00123456, chars=10, delta=0)
    assert '-0.0001235' == _num_formatter(-0.000123456, chars=10, delta=0)
    assert '-1.235e-05' == _num_formatter(-0.0000123456, chars=10, delta=0)


def test_edge():
    assert '         1' == _num_formatter(1.0, chars=10, delta=0)
    assert '        -1' == _num_formatter(-1.0, chars=10, delta=0)
    assert '1         ' == _num_formatter(1.0, left=True, chars=10, delta=0)
    assert '-1        ' == _num_formatter(-1.0, left=True, chars=10, delta=0)

    assert '         0' == _num_formatter(0, chars=10, delta=0)
    assert '         0' == _num_formatter(0.0, chars=10, delta=0)
    assert '0         ' == _num_formatter(-0, left=True, chars=10, delta=0)
    assert '0         ' == _num_formatter(-0.0, left=True, chars=10, delta=0)

    assert '         0' == _num_formatter(1e-1234, chars=10, delta=0)
    assert '0         ' == _num_formatter(-1e-1234, left=True, chars=10, delta=0)

    assert '       inf' == _num_formatter(2.1e1234, chars=10, delta=0)
    assert '      -inf' == _num_formatter(-2.1e1234, chars=10, delta=0)
    assert 'inf       ' == _num_formatter(2.1e1234, chars=10, left=True, delta=0)
    assert '-inf      ' == _num_formatter(-2.1e1234, chars=10, left=True, delta=0)

    with pytest.raises(ValueError):
        _num_formatter('hello', chars=10, delta=0)
