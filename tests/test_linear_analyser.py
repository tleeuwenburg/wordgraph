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
from wordgraph import analysers
from wordgraph.points import Point


@pytest.mark.parametrize(["gradient", "constant"],
        [(0, 3.5),
         (1, 10)])
def test_perfect_linear(gradient, constant):
    """
    First, check we get a perfect validity score for
    straight lines.
    Then ensure that the analyser selector chooses
    the LinearAnalyser for these series.
    """
    points = [Point(i, gradient * i + constant) for i in range(20)]
    ld = analysers.LinearDistribution(points=points)
    assert ld.get_validity() == 1.0

    result = analysers.get_analysis(points=points)
    assert result["name"] == "linear"
    assert result["p_value"] == 1.0


def generate_fuzzy_points():
    gradient = 100
    constant = 0
    for fuzz in range(10):
        points = [Point(i, gradient * i + constant + (.5 - (i % 2)) * fuzz)
                for i in range(20)]
        yield points


def test_fuzz():
    """
    ensure that as the series deviates from a completely straight line,
    that the validity keeps dropping
    """
    validities = [analysers.LinearDistribution(points=points).get_validity()
            for points in generate_fuzzy_points()]
    assert validities == sorted(validities, reverse=True)
