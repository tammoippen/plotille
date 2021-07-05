# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 - 2021 Tammo Ippen, tammo.ippen@posteo.de

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

# Get data for your own: https://github.com/earthobservations/wetterdienst
# call
# wetterdienst values --provider=dwd --kind=observation \
#                     --parameter=kl --resolution=daily \
#                     --station 1048,4411 \
#                     --date=1970-01-01/2021-01-01 > wetter-data.json

from collections import defaultdict
from datetime import datetime
import gzip
import json
import os

import plotille as plt


def regression(x, y):
    # number of observations/points
    n = len(x)
    assert n > 0
    assert n == len(y)

    # mean of x and y vector
    m_x = sum(x) / n
    m_y = sum(y) / n

    # calculating cross-deviation and deviation about x
    xy = 0
    xx = 0
    for idx in range(n):
        xy += y[idx] * x[idx]
        xx += x[idx] * x[idx]
    xy -= n * m_y * m_x
    xx -= n * m_x * m_x

    # calculating regression coefficients
    m = xy / xx
    b = m_y - m * m_x

    return m, b


current_dir = os.path.dirname(__file__)

with gzip.open(current_dir + os.sep + 'wetter-data.json.gz', 'r') as f:
    data = json.load(f)

# wetterdienst stations --station 1048,4411 \
#                       --provider dwd \
#                       --kind observation \
#                       --parameter kl \
#                       --resolution daily
stations = [
    {
        'station_id': '01048',
        'from_date': '1934-01-01T00:00:00.000Z',
        'to_date': '2021-07-04T00:00:00.000Z',
        'height': 228.0,
        'latitude': 51.1278,
        'longitude': 13.7543,
        'name': 'Dresden-Klotzsche',
        'state': 'Sachsen',
    },
    {
        'station_id': '04411',
        'from_date': '1979-12-01T00:00:00.000Z',
        'to_date': '2021-07-04T00:00:00.000Z',
        'height': 155.0,
        'latitude': 49.9195,
        'longitude': 8.9671,
        'name': 'Schaafheim-Schlierbach',
        'state': 'Hessen',
    },
]
station_by_id = {st['station_id']: st for st in stations}


Xs = defaultdict(list)
Ys = defaultdict(list)
for d in data:
    if d['temperature_air_200'] is not None:
        dt = datetime.strptime(d['date'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        name = station_by_id[d['station_id']]['name']
        if dt.month == 1 and dt.day == 1:
            Xs[name] += [dt.year]
            Ys[name] += [d['temperature_air_200'] - 273.15]

fig = plt.Figure()
fig.width = 120
fig.height = 30
fig.set_x_limits(1970, 2021)
fig.set_y_limits(-18, 12)
fig.y_label = 'Celsius'
fig.x_label = 'Year'

fig.x_ticks_fkt = lambda min_, max_: '{:d}'.format(int(min_))
fig.y_ticks_fkt = lambda min_, max_: '{:.3f}'.format(min_)

for station in Xs.keys():
    fig.plot(Xs[station], Ys[station], label=station)
    m, b = regression(Xs[station], Ys[station])
    start = m * 1970 + b
    end = m * 2021 + b
    fig.plot([1970, 2021], [start, end], label='{} - regression'.format(station))

print('\033[2J')  # clear screen
print(' ' * 50 + 'Temperatur of two stations in Germany at 1. Januar')
print(fig.show(legend=True))
