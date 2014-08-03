import wordgraph

EPOCH_START = 1407109280

def test_monotonic_up_per_second():
    datapoints = []
    for i in range(10):
        datapoints.append((float(i), EPOCH_START + i))
    features = wordgraph.name_things(datapoints)
    assert "" in features
