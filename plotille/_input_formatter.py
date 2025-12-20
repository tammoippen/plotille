# The MIT License

# Copyright (c) 2017 - 2024 Tammo Ippen, tammo.ippen@posteo.de

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

import math
from collections import OrderedDict
from collections.abc import Callable
from datetime import date, datetime, time, timedelta
from typing import Any, Protocol

from ._util import roundeven


def _numpy_to_native(x: Any) -> Any:
    # cf. https://numpy.org/doc/stable/reference/generated/numpy.ndarray.item.html
    if (
        "<class 'numpy." in str(type(x)) or "<type 'numpy." in str(type(x))
    ) and callable(x.item):
        return x.item()
    return x


class Formatter(Protocol):
    def __call__(self, val: Any, chars: int, delta: Any, left: bool) -> str: ...


Converter = Callable[[Any], int | float | datetime]


class InputFormatter:
    def __init__(self) -> None:
        self.formatters: OrderedDict[type, Formatter] = OrderedDict()

        self.formatters[float] = _num_formatter
        self.formatters[int] = _num_formatter

        self.formatters[date] = _date_formatter
        self.formatters[datetime] = _datetime_formatter

        self.formatters[str] = _text_formatter

        self.converters: OrderedDict[type, Converter] = OrderedDict()
        self.converters[float] = _convert_numbers
        self.converters[int] = _convert_numbers

        self.converters[date] = _convert_date
        self.converters[datetime] = _convert_datetime

        try:
            import numpy as np

            self.converters[np.datetime64] = _convert_np_datetime
            self.formatters[np.datetime64] = _np_datetime_formatter
        except ImportError:  # pragma: nocover
            pass

    def register_formatter(self, t: type, f: Formatter) -> None:
        self.formatters[t] = f

    def register_converter(self, t: type, f: Converter) -> None:
        self.converters[t] = f

    def fmt(self, val: Any, delta: Any, left: bool = False, chars: int = 9) -> str:
        val = _numpy_to_native(val)
        for t, f in reversed(self.formatters.items()):
            if isinstance(val, t):
                return f(val, chars=chars, delta=delta, left=left)

        return str(val)

    def convert(self, val: Any) -> Any:
        for t, f in reversed(self.converters.items()):
            if isinstance(val, t):
                return f(val)

        return val


def _np_datetime_formatter(val: Any, chars: int, delta: Any, left: bool = False) -> str:
    # assert isinstance(val, np.datetime64)
    # assert isinstance(delta, np.timedelta64)

    return _datetime_formatter(val.item(), chars, delta.item(), left)


def _date_formatter(val: date, chars: int, delta: timedelta, left: bool = False) -> str:
    assert isinstance(val, date)
    assert isinstance(delta, timedelta)

    val_dt = datetime.combine(val, time.min)
    return _datetime_formatter(val_dt, chars, delta, left)


def _datetime_formatter(
    val: datetime, chars: int, delta: timedelta, left: bool = False
) -> str:
    assert isinstance(val, datetime)
    assert isinstance(delta, timedelta)

    if chars < 8:
        raise ValueError(
            f'Not possible to display value "{val}" with {chars} characters!'
        )

    res = ""

    if delta.days <= 0:
        # make time representation
        if chars < 15:
            res = f"{val.hour:02d}:{val.minute:02d}:{val.second:02d}"
        else:
            res = f"{val.hour:02d}:{val.minute:02d}:{val.second:02d}.{val.microsecond:06d}"
    elif 1 <= delta.days <= 10:
        # make day / time representation
        if chars < 11:
            res = f"{val.day:02d}T{val.hour:02d}:{val.minute:02d}"
        else:
            res = f"{val.day:02d}T{val.hour:02d}:{val.minute:02d}:{val.second:02d}"
    # make date representation
    elif chars < 10:
        res = f"{val.year % 100:02d}-{val.month:02d}-{val.day:02d}"
    else:
        res = f"{val.year:04d}-{val.month:02d}-{val.day:02d}"

    if left:
        return res.ljust(chars)
    else:
        return res.rjust(chars)


def _num_formatter(
    val: int | float, chars: int, delta: int | float, left: bool = False
) -> str:
    if not isinstance(val, (int, float)):
        raise TypeError(
            "Only accepting numeric (int/long/float) "
            f'types, not "{val}" of type: {type(val)}'
        )

    # about float (f32) machine precision
    if abs(val - roundeven(val)) < 1e-8:
        val = int(roundeven(val))

    if isinstance(val, int):
        return _int_formatter(val, chars, left)
    elif isinstance(val, float):
        return _float_formatter(val, chars, left)
    # unreachable


def _float_formatter(val: float, chars: int, left: bool = False) -> str:
    assert isinstance(val, float)
    if math.isinf(val):
        return str(val).ljust(chars) if left else str(val).rjust(chars)
    sign = 1 if val < 0 else 0
    order = 0 if val == 0 else math.log10(abs(val))
    align = "<" if left else ""

    if order >= 0:
        # larger than 1 values or smaller than -1
        digits = math.ceil(order)
        fractionals = int(max(0, chars - 1 - digits - sign))
        if digits + sign > chars:
            return _large_pos(val, chars, left, digits, sign)

        return "{:{}{}.{}f}".format(val, align, chars, fractionals)
    else:
        # between -1 and 1 values
        order = abs(math.floor(order))

        if order > 4:  # e-04  4 digits
            exp_digits = int(max(2, math.ceil(math.log10(order))))
            exp_digits += 2  # the - sign and the e

            return "{:{}{}.{}e}".format(
                val, align, chars, chars - exp_digits - 2 - sign
            )
        else:
            return "{:{}{}.{}f}".format(val, align, chars, chars - 2 - sign)


def _int_formatter(val: int, chars: int, left: bool = False) -> str:
    assert isinstance(val, int)
    if val != 0:
        sign = 1 if val < 0 else 0
        digits = math.ceil(math.log10(abs(val)))
        if digits + sign > chars:
            return _large_pos(val, chars, left, digits, sign)
    align = "<" if left else ""
    return "{:{}{}d}".format(val, align, chars)


def _large_pos(val: float | int, chars: int, left: bool, digits: int, sign: int) -> str:
    align = "<" if left else ""
    # exponent is always + and has at least two digits (1.3e+06)
    exp_digits = max(2, math.ceil(math.log10(digits)))
    exp_digits += 2  # the + sign and the e
    front_digits = chars - exp_digits - sign
    residual_digits = int(max(0, front_digits - 2))
    if front_digits < 1:
        raise ValueError(
            f'Not possible to display value "{val}" with {chars} characters!'
        )
    return "{:{}{}.{}e}".format(val, align, chars, residual_digits)


def _text_formatter(val: str, chars: int, delta: str, left: bool = False) -> str:
    if left:
        return val[:chars].ljust(chars)
    else:
        return val[:chars].rjust(chars)


def _convert_numbers(v: float | int) -> float:
    assert isinstance(v, float) or isinstance(v, int)
    return v


def _convert_np_datetime(v: Any) -> float:
    # assert isinstance(v, np.datetime64)
    v = v.item().timestamp()
    assert isinstance(v, float)
    return v


def _convert_date(v: date) -> int:
    assert isinstance(v, date)
    return (v - date.min).days


def _convert_datetime(v: datetime) -> float:
    assert isinstance(v, datetime)
    return v.timestamp()
