# Copyright 2014 Nicholas Farrell

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Analysers are used to process a single series, and
produce structured output describing the series.

As a user of this module, you will usually simply invoke
get_analysis(points).

Analysers do not care about things like axis labels; they
only need to find the best way of representing the data in
the graph.

The analysers' results are language agnostic, and will be
translated into natural language elsewhere.

To add a new analyser, simply subclass the FixedIntervalAnalyser and
implement the two methods. get_validity() will be used to asses which
analyser is most suitable for describing the data, while get_result()
does the actual analysis. Then add it to the list of analysers.

Note that the values passed into the analysers are just the y-values;
you should not need to know the x-values, and you can assume the x distance
between consecutive points is constant.

"""


import statistics
from scipy import stats
import numpy as np


class FixedIntervalAnalyser():
    """
    Given a series of y-values, associated
    with fixed x-axis increments, provide
    analysis of it.
    """
    def __init__(self, points):
        self.points = sorted((point for point in points), key=lambda p: p.x)

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

    def __str__(self):
        return "{0} [{1}]".format(self.name, self.get_validity())


class LinearDistribution(FixedIntervalAnalyser):

    name = "linear"

    def get_validity(self):
        # calculate the line of best fit
        x = [p.x for p in self.points]
        A = np.vstack([x, np.ones(len(x))]).T
        result = np.linalg.lstsq(A, [p.y for p in self.points])
        self.gradient, self.constant = result[0]
        print(result)
        return 0.2  # FIXME

    def get_result(self):
        return dict(gradient=self.gradient,
                constant=self.constant)


class NormalDistribution(FixedIntervalAnalyser):

    name = "normal"

    def _interpolate_at(self, x_value):
        """
        Given a potentially very blocky graph, interpolate
        a y value at an arbitrary x value across the graph.
        """
        left_point = None
        for point in self.points:
            if point.x <= x_value:
                left_point = point
            else:
                right_point = point
                proportion_across = (x_value - left_point.x) \
                        / (right_point.x - left_point.x)
                return (left_point.y +
                        proportion_across * (right_point.y - left_point.y))
        assert False, "Fallen off the end of the graph"

    def _cumulative_at(self, x_value):
        """
        What proportion of the total area covered by the graph
        is to the left of this x value?
        """
        raise NotImplementedError()


    def x_value_at(self, proportion):
        """
        What is the x value which places this proportion of
        the graph to the left of this place?
        """
        raise NotImplementedError()

    def _estimate_stddev(self):
        """
        Sample the cumulative distribution at a number of points,
        and use that to estimate the standard deviation
        """
        assert self.mean is not None
        return (
                (self.mean - self.x_value_at(.015)) / 2 +
                (self.mean - self.x_value_at(.16))
                (self.x_value_at(.83) - self.mean)
                (self.x_value_at(.985) - self.mean) / 2
                ) / 4


    def generate_idealised_normal(self):
        """
        Using the original x values of the input data,
        return a new set of points which as based on the
        assumed mean and stddev
        """
        #return (Point(point.x, ???) for point in self.points)
        pass


    def get_validity(self):
        """
        (hacky) approach:
        Assuming that we do have a normal distribution.
        Then compare the theoretical cumulative normal distribution
        to the actual distribution at various points, and base
        the overall score on the overall deviation.

        We will assume the X values start at 0 and increment by 1
        for each point in the series.
        """
        self.mean = self.x_value_at(.5)
        self.stddev = self._estimate_stddev()
        ideal_points = self.generate_idealised_normal()
        badness = set()
        n_dev = -3
        while n_dev <= 3:
            #badness.add(abs(cnd(n_dev) -
            n_dev += .05

    def get_result(self):
        return dict(mean=statistics.mean(self.values),
                stdev=statistics.stdev(self.values))


class RandomDistribution(FixedIntervalAnalyser):
    """
    No meaninful pattern in the data.
    """

    name = "random"

    def get_validity(self):
        return 0.1

    def get_result(self):
        return dict()  # nothing meaningful


_analysers = [#NormalDistribution,
        RandomDistribution,
        LinearDistribution]


def get_best_analyser(values):
    """
    Instantiate a bunch of analysers and return the one
    which suits this data best.
    """
    candidates = sorted(
            (analyser(values) for analyser in _analysers),
            key=lambda a: a.get_validity())
    print([str(c) for c in candidates])
    return candidates[-1]


def assert_fixed_interval(points):
    x_values = sorted(point.x for point in points)
    if len(x_values) <= 1:
        raise ValueError("Not enough data points!")
    expected_interval_size = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    for left, right in zip(x_values, x_values[1:]):
        if abs(1 - ((right - left) / expected_interval_size)) > 0.01:
           raise ValueError("Intervals on the X axis are not fixed width")


def get_analysis(points):
    try:
        assert_fixed_interval(points=points)
    except ValueError as ex:
        return dict(name="Unprocessable",
                result=str(ex))
    y_values = [point.y for point in sorted(points)]
    analyser = get_best_analyser(points)
    return dict(p_value=analyser.get_validity(),
            name=analyser.name,
            min_y_value=min(y_values),
            result=analyser.get_result())
