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
from scipy.stats import norm
from wordgraph import analysers
from wordgraph.points import Point

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
