import wordgraph

from utilities import time_values

def test_linear_values():
    datapoints = time_values(3.0 for i in range(10))
    features = wordgraph.describe(datapoints)
    assert "" in features

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

def test_saw_tooth():
    values = [1.0 + i for i in range(5)]
    values *= 5
    values.append(1.0)
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert "" in features
