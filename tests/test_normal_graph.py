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
