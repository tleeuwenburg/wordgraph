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

from collections import defaultdict
import random
import pytest
from wordgraph import describe


@pytest.mark.parametrize(["mean", "stddev", "offset"],
        [(0, 1, 0),
         (10, 10, -100),
         (-100, 1, -0.5)])
def test_normal(mean, stddev, offset):
    n_datapoints = 1000
    points = set(random.gauss(mu=mean, sigma=stddev)
            for i in range(n_datapoints))
    step_size = stddev / 10
    frequency_count = defaultdict(int)
    for point in points:
        frequency_count[point % step_size] += 1

    assert "???" == describe(data=frequency_count.items())
