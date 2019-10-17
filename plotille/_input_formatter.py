# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2018 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from collections import OrderedDict
from datetime import date, datetime, time, timedelta
import math

import six

from ._util import roundeven, timestamp


class InputFormatter(object):
    def __init__(self):
        self.formatters = OrderedDict()

        self.formatters[float] = _num_formatter
        for int_type in six.integer_types:
            self.formatters[int_type] = _num_formatter

        self.formatters[date] = _date_formatter
        self.formatters[datetime] = _datetime_formatter

        self.converters = OrderedDict()
        self.converters[float] = _convert_numbers
        for int_type in six.integer_types:
            self.converters[int_type] = _convert_numbers

        self.converters[date] = _convert_date
        self.converters[datetime] = _convert_datetime

        try:
            import numpy as np

            self.converters[np.datetime64] = _convert_np_datetime
            self.formatters[np.datetime64] = _np_datetime_formatter
        except ImportError:  # pragma: nocover
            pass

    def register_formatter(self, t, f):
        self.formatters[t] = f

    def register_converter(self, t, f):
        self.converters[t] = f

    def fmt(self, val, delta, left=False, chars=9):
        for t, f in reversed(self.formatters.items()):
            if isinstance(val, t):
                return f(val, chars=chars, delta=delta, left=left)

        return str(val)

    def convert(self, val):
        for t, f in reversed(self.converters.items()):
            if isinstance(val, t):
                return f(val)

        return val


def _np_datetime_formatter(val, chars, delta, left=False):
    # assert isinstance(val, np.datetime64)
    # assert isinstance(delta, np.timedelta64)

    return _datetime_formatter(val.item(), chars, delta.item(), left)


def _date_formatter(val, chars, delta, left=False):
    assert isinstance(val, date)
    assert isinstance(delta, timedelta)

    val_dt = datetime.combine(val, time.min)
    return _datetime_formatter(val_dt, chars, delta, left)


def _datetime_formatter(val, chars, delta, left=False):
    assert isinstance(val, datetime)
    assert isinstance(delta, timedelta)

    if chars < 8:
        raise ValueError('Not possible to display value "{}" with {} characters!'.format(val, chars))

    res = ''

    if delta.days <= 0:
        # make time representation
        if chars < 15:
            res = '{:02d}:{:02d}:{:02d}'.format(val.hour, val.minute, val.second)
        else:
            res = '{:02d}:{:02d}:{:02d}.{:06d}'.format(val.hour, val.minute, val.second, val.microsecond)
    elif 1 <= delta.days <= 10:
        # make day / time representation
        if chars < 11:
            res = '{:02d}T{:02d}:{:02d}'.format(val.day, val.hour, val.minute)
        else:
            res = '{:02d}T{:02d}:{:02d}:{:02d}'.format(val.day, val.hour, val.minute, val.second)
    else:
        # make date representation
        if chars < 10:
            res = '{:02d}-{:02d}-{:02d}'.format(val.year % 100, val.month, val.day)
        else:
            res = '{:04d}-{:02d}-{:02d}'.format(val.year, val.month, val.day)

    if left:
        return res.ljust(chars)
    else:
        return res.rjust(chars)


def _num_formatter(val, chars, delta, left=False):
    if not (isinstance(val, six.integer_types) or isinstance(val, float)):
        raise ValueError('Only accepting numeric (int/long/float) types, not "{}" of type: {}'.format(val, type(val)))

    if abs(val - roundeven(val)) < 1e-8:  # about float (f32) machine precision
        val = int(roundeven(val))

    if isinstance(val, six.integer_types):
        return _int_formatter(val, chars, left)
    elif isinstance(val, float):
        return _float_formatter(val, chars, left)


def _float_formatter(val, chars, left=False):
    assert isinstance(val, float)
    if math.isinf(val):
        return str(val).ljust(chars) if left else str(val).rjust(chars)
    sign = 1 if val < 0 else 0
    order = 0 if val == 0 else math.log10(abs(val))
    align = '<' if left else ''

    if order >= 0:
        # larger than 1 values or smaller than -1
        digits = math.ceil(order)
        fractionals = int(max(0, chars - 1 - digits - sign))
        if digits + sign > chars:
            return _large_pos(val, chars, left, digits, sign)

        return '{:{}{}.{}f}'.format(val, align, chars, fractionals)
    else:
        # between -1 and 1 values
        order = abs(math.floor(order))

        if order > 4:  # e-04  4 digits
            exp_digits = int(max(2, math.ceil(math.log10(order))))
            exp_digits += 2  # the - sign and the e

            return '{:{}{}.{}e}'.format(val, align, chars, chars - exp_digits - 2 - sign)
        else:
            return '{:{}{}.{}f}'.format(val, align, chars, chars - 2 - sign)


def _int_formatter(val, chars, left=False):
    assert isinstance(val, six.integer_types)
    if val != 0:
        sign = 1 if val < 0 else 0
        digits = math.ceil(math.log10(abs(val)))
        if digits + sign > chars:
            return _large_pos(val, chars, left, digits, sign)
    align = '<' if left else ''
    return '{:{}{}d}'.format(val, align, chars)


def _large_pos(val, chars, left, digits, sign):
    align = '<' if left else ''
    # exponent is always + and has at least two digits (1.3e+06)
    exp_digits = max(2, math.ceil(math.log10(digits)))
    exp_digits += 2  # the + sign and the e
    front_digits = chars - exp_digits - sign
    residual_digits = int(max(0, front_digits - 2))
    if front_digits < 1:
        raise ValueError('Not possible to display value "{}" with {} characters!'.format(val, chars))
    return '{:{}{}.{}e}'.format(val, align, chars, residual_digits)


def _convert_numbers(v):
    assert isinstance(v, float) or isinstance(v, six.integer_types)
    return float(v)


def _convert_np_datetime(v):
    # assert isinstance(v, np.datetime64)
    return timestamp(v.item())


def _convert_date(v):
    assert isinstance(v, date)
    return (v - date.min).days


def _convert_datetime(v):
    assert isinstance(v, datetime)
    return timestamp(v)
