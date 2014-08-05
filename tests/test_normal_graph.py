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


import pytest
import py
from scipy.stats import norm
from wordgraph import analysers
from wordgraph.points import Point


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


@py.test.mark.xfail
def test_zeroes():
    points = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]
    nd = analysers.NormalDistribution(points=points)
    validity = nd.get_validity()
    assert False, validity



@py.test.mark.xfail #TODO: I don't know what this is supposed to do!
@pytest.mark.parametrize(["mean", "stddev", "offset"],
        [(0, 1, 0),
         (10, 10, -100),
         (-100, 1, -0.5)])
def test_normal(mean, stddev, offset):
    # create 100 buckets, from -5.0 to 4.9 inclusive
    x_values = [(.01 * i - 5) for i in range(1001)]
    y_values = [(norm.cdf(right) - norm.cdf(left))
            for left, right in zip(x_values, x_values[1:])]
    points = [Point(x, y) for x, y in zip(x_values, y_values)]
    assert "???" == analysers.get_analysis(points=points)
