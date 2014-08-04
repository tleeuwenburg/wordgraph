from wordgraph.points import Point

EPOCH_START = 1407109280

def time_values(values, start=EPOCH_START, increment=1):
    datapoints = []
    for index, value in enumerate(values):
        datapoints.append(Point(x=value, y=start + (increment * index)))
    return datapoints
