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

def test_tent_map():
    values = [float(i) for i in range(10)]
    values.append(11.0)
    values += [10.0 - i for i in range(10)]
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_step_function():
    values = [1.0] * 10
    values += [2.0] * 10
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert "" in features
