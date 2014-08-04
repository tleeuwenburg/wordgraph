from wordgraph.points import Point
import wordgraph

EPOCH_START = 1407109280

def time_values(values, start=EPOCH_START, increment=1):
    datapoints = []
    for index, value in enumerate(values):
        datapoints.append(Point(x=value, y=start + (increment * index)))
    return datapoints

def test_monotonic_up_per_second():
    datapoints = time_values(float(i) for i in range(POINTS))
    features = wordgraph.describe(datapoints)
    assert "" in features
