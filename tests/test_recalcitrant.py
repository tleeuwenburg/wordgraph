# Copyright 2014 Tennessee Leeuwenburg

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"Test for recalcitrant and obtuse graphs to describe"
from wordgraph.points import Point
import wordgraph

import random
import pytest

from utilities import EPOCH_START, time_values

def test_time_goes_backwards():
    "A valid time series where time changes linearly backwards"
    values = [1.0] * 10
    times = (EPOCH_START-i for i in range(10))
    datapoints = [Point(x=t, y=v) for (v, t) in zip(values, time)]
    features = wordgraph.describe(datapoints)
    assert features is None

def test_random_data():
    "A time series of 50 data points where every value is random"
    rng = random.Random(0)
    values = [rng.random() for i in range(50)]
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert features is None

def test_too_few_points():
    """A time series with too few data points to be analysed.

    Expected to raise an exception.
    """
    with pytest.raises(ValueError):
        features = wordgraph.describe([Point(x=0, y=0)])

def test_nonuniform_time_periods():
    """A time series where time periods are wildly different.

    Expected to raise an exception.
    """
    times = [1, 3, 4, 6, 7, 9, 10]
    datapoints = [Point(x=t, y=1.0) for t in times]
    with pytest.raises(ValueError):
        features = wordgraph.describe(datapoints)
