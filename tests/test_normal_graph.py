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

import math
import pytest
import py
from wordgraph import analysers
from wordgraph.points import Point

def phi(x):
    '''
    Cumulative distribution function for the standard normal distribution

    Taken from the python math docs. Using to avoid a scipy dependency for now -- 
    scipy is very hard to install via pip due to O/S package dependencies. We
    want to support a simple install process if at all possible.

    '''
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


@pytest.mark.parametrize(["y_values", "expected"],
        [([10, 10, 10, 10], 0),
         ([10, 15, 15, 10], 10),
         ([10, 20, 15, 10], 15)])
def test_total_size(y_values, expected):
    points = [Point(i, y) for i, y in enumerate(y_values)]
    nd = analysers.NormalDistribution(points=points)
    assert expected == nd.total_size


@pytest.mark.parametrize(["proportion", "expected"],
        [(0, -5),
         (.5, 1)])
def test_x_value_at(proportion, expected):
    points = [Point(-5, 10),
              Point(-1, 15),
              Point(3, 15),
              Point(7, 10)]
    nd = analysers.NormalDistribution(points=points)
    assert expected == nd.x_value_at(proportion)


def test_zeroes():
    points = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]
    nd = analysers.NormalDistribution(points=points)
    validity = nd.get_validity()
    assert validity == 0


@pytest.mark.parametrize(["mean", "stddev", "offset"],
        [(0, 1, 0),
        # (10, 10, -100),
        # (-100, 1, -0.5)
        ])
def test_normal(mean, stddev, offset):
    # create 100 buckets, from -5.0 to 4.9 inclusive
    x_values = [(.01 * i - 5) for i in range(1001)]
    y_values = [100 * (phi(right) - phi(left))
            for left, right in zip(x_values, x_values[1:])]
    points = [Point(x, y) for x, y in zip(x_values, y_values)]
    analyser = analysers.get_analysis(points=points)
    assert analyser['name'] == 'normal'
