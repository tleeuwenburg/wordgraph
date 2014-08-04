"Test for artificially generated and perfect examples of graph features"
import wordgraph

from utilities import time_values

def test_linear_values():
    "Postiive constant value time series in 10, one second increments"
    datapoints = time_values(3.0 for i in range(10))
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_monotonic_up_per_second():
    "Monotonically increasing positive series in 10, one second increments"
    datapoints = time_values(float(i) for i in range(10))
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_monotonic_down_per_second():
    "Monotonically descreasing positive series in 10, one second increments"
    datapoints = time_values(10.0 - i for i in range(10))
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_tent_map():
    """Tent map time series
    
    A 20 second time series in two distinct, 10 second ranges with one second
    increments. First period is monotonically increasing. The second period is
    monotonically decreasing at the same rate.
    """
    values = [float(i) for i in range(10)]
    values.append(11.0)
    values += [10.0 - i for i in range(10)]
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_step_function():
    """Step function time series

    A 20 second time series in two distinct, 10 second ranges with one second
    increments. First period is a positive constant value. The second period is
    a different, positive constant value.
    """
    values = [1.0] * 10
    values += [2.0] * 10
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert "" in features

def test_saw_tooth():
    """A saw tooth time series

    A 25 second time series of 5 distinct periods. Each period exhibits the
    same monotonically increasing positive series. The series resets to the
    initial state on each section boundary.
    """
    values = [1.0 + i for i in range(5)]
    values *= 5
    values.append(1.0)
    datapoints = time_values(values)
    features = wordgraph.describe(datapoints)
    assert "" in features
