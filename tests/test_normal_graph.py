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


import random
import pytest
from wordgraph import analysers
from wordgraph.points import Point


@pytest.mark.parametrize(["mean", "stddev", "offset"],
        [(0, 1, 0),
         (10, 10, -100),
         (-100, 1, -0.5)])
def test_normal(mean, stddev, offset):
    minimum = mean - 50 * stddev
    maximum = mean + 49 * stddev
    step = stddev / 10
    x_value = minimum
    frequency_count = dict()
    while x_value <= maximum:
        frequency_count[x_value] = 0
        x_value += step

    n_datapoints = 10000
    for i in range(n_datapoints):
        value = random.gauss(mu=mean, sigma=stddev)
        x_value = min(x for x in frequency_count if x >= value)
        if x_value < minimum or x_value > maximum:
            continue
        frequency_count[x_value] += 1

    points = [Point(x, y) for x, y in frequency_count.items()]

    assert "???" == analysers.get_analysis(points=points)
