import statistics
from scipy import stats


class FixedIntervalAnalyser():
    """
    Given a series of y-values, associated
    with fixed x-axis increments, provide
    analysis of it.
    """
    def __init__(self, values):
        self.values = values

    def get_validity(self):
        """
        Returns a float representing how well
        this analyser can describe these values.
        1 represents a perfect fit, 0 represents no
        fit.
        """
        raise NotImplementedError()

    def get_result(self):
        """
        Returns a (jsonable) representation of the
        values using this analyser.
        """
        return NotImplementedError()


class NormalDistribution(FixedIntervalAnalyser):
    def get_validity(self):
        k2, pvalue = stats.normaltest(self.values)
        return pvalue ** 0.5

    def get_result(self):
        return dict(mean=statistics.mean(self.values),
                stdev=statistics.stdev(self.values))


class RandomDistribution(FixedIntervalAnalyser):
    """
    No meaninful pattern in the data.
    """
    def get_validity(self):
        return 0.1

    def get_result(self):
        return dict()  # nothing meaningful


_analysers = [NormalDistribution, RandomDistribution]


def get_best_analyser(values):
    """
    Instantiate a bunch of analysers and return the one
    which suits this data best.
    """
    return sorted((analyser for analyser in _analysers(values=values)),
            key=lambda a: a.get_validity())[-1]


def assert_fixed_interval(points):
    x_values = sorted(point.x for point in points)
    assert len(x_values) > 1, "Not enough data points!"
    expected_interval_size = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    for left, right in zip(x_values, x_values[1:]):
        assert right - left / expected_interval_size < 0.01, \
                "Intervals on the X axis are not fixed width"


def get_analysis(points):
    assert_fixed_interval(points=points)
    y_values = [point.y for point in sorted(points)]
    analyser = get_best_analyser(values=y_values)
    return dict(analyser=analyser.__class__.__name__,
            result=analyser.get_result(values=y_values))
