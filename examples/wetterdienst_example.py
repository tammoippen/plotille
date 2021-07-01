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
#                     --date=1969-01-01/2020-01-01 > wetter-data.json

from collections import defaultdict
from datetime import datetime
import gzip
import json
import os

import plotille as plt

current_dir = os.path.dirname(__file__)

with gzip.open(current_dir + os.sep + 'wetter-data.json.gz', 'r') as f:
    data = json.load(f)

Xs = defaultdict(list)
Ys = defaultdict(list)
for d in data:
    if d['temperature_air_200'] is not None:
        dt = datetime.strptime(d['date'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
        Xs[d['station_id']] += [dt]
        Ys[d['station_id']] += [d['temperature_air_200']]

fig = plt.Figure()
fig.width = 80
fig.height = 20
fig.y_label = 'Kelvin'
fig.x_label = 'Year/month'

fig.x_ticks_fkt = lambda min_, max_: min_.strftime('%Y-%m')

for station_id in Xs.keys():
    fig.scatter(Xs[station_id], Ys[station_id], label=station_id)

print(fig.show(legend=True))
