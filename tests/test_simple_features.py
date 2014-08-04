from wordgraph.points import Point
import wordgraph

EPOCH_START = 1407109280

def time_values(values, start=EPOCH_START, increment=1):
    datapoints = []
    for index, value in enumerate(values):
        datapoints.append(Point(x=value, y=start + (increment * index)))
    return datapoints

def test_monotonic_up_per_second():
    datapoints = time_values(float(i) for i in range(10))
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_monotonic_down_per_second():
    datapoints = time_values(10.0 - i for i in range(10))
    features = wordgraph.describe(datapoints)
    assert "" in features
