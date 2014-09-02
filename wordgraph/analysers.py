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

UNPROCESSABLE = "Unprocessable"

try:
    import statistics
except ImportError:
    try:
        import backports.statistics as statistics
    except ImportError:
        print("Continuing unsafely. Upgrade to python 3.4! Could not find module 'statistics")

import math
import numpy as np


def phi(x):
    '''
    Cumulative distribution function for the standard normal distribution.
    
    Note -- this expects the standard deviation normalisation to have already
    been done outside of this fn.

    Taken from the python math docs. Using to avoid a scipy dependency for now -- 
    scipy is very hard to install via pip due to O/S package dependencies. We
    want to support a simple install process if at all possible.

    '''
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

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
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        par = np.polyfit(x_values, y_values, 1, full=True)

        self.gradient = par[0][0]
        self.constant = par[0][1]

        residuals = np.var([(self.gradient * point.x + self.constant - point.y)
            for point in self.points])
        # variance = np.var(y_values)
        # Rsqr = np.round(1 - residuals / variance, decimals=2)
        return 1 - residuals

    def get_result(self):
        return dict(gradient=self.gradient,
                constant=self.constant)


class NormalDistribution(FixedIntervalAnalyser):

    name = "normal"

    _total_size = None
    _minimum_y = None

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

    @property
    def total_size(self):
        if self._total_size is None:
            self._cumulative_size = dict()
            self._minimum_y = min(point.y for point in self.points)

            previous_point = None
            for point in self.points:
                if previous_point is None:
                    self._cumulative_size[point.x] = 0
                else:
                    self._cumulative_size[point.x] = self._cumulative_size[previous_point.x] + .5 * (point.x - previous_point.x) * (max(point.y, previous_point.y) - min(point.y, previous_point.y)) + (min(point.y, previous_point.y) - self._minimum_y)
                previous_point = point
            self._total_size = self._cumulative_size[point.x]
        return self._total_size

    def x_value_at(self, proportion):
        """
        What is the x value which places this proportion of
        the graph to the left of this place?
        """
        assert 0 <= proportion <= 1
        target_size = self.total_size * proportion
        sizes = sorted(self._cumulative_size.items())
        for left, right in zip(sizes, sizes[1:]):
            left_x, left_size = left
            right_x, right_size = right
            if target_size > right_size:
                continue
            if left_size == right_size:
                return (right_x + left_x) / 2.
            proportion_across = (target_size - left_size) / (right_size - left_size)
            return left_x + (right_x - left_x) * proportion_across

    def _estimate_stddev(self):
        """
        Sample the cumulative distribution at a number of points,
        and use that to estimate the standard deviation
        """
        if self.mean == None:
            # There might be only a single element
            return 0
        result = ((self.mean - self.x_value_at(.015)) / 2 +
                  (self.mean - self.x_value_at(.16)) +
                  (self.x_value_at(.83) - self.mean) +
                  (self.x_value_at(.985) - self.mean) / 2) / 4
        return result


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
        y_scale = max(point.y for point in self.points) \
            - min(point.y for point in self.points)
        if self.stddev == 0:
            return 0

        # ideal_cumulative = dict(
        #         (point.x, stats.norm.cdf((point.x - self.mean) / self.stddev))
        #     for point in self.points)

        cum_points = [(point.x, phi((point.x - self.mean) / self.stddev)) for point in self.points]
        ideal_cumulative = dict(cum_points)

        devtest = [(point.x, ideal_cumulative[point.x],
            (self._cumulative_size[point.x] / self.total_size),
            y_scale) for point in self.points]

        deviations = [(point.x, abs(ideal_cumulative[point.x] -
            (self._cumulative_size[point.x] / self.total_size))
            ) for point in self.points]
        average_deviation = sum(abs(d[1]) for d in deviations) / len(self.points)
        return abs(1 - average_deviation)

    def get_result(self):
        return dict(mean=self.mean, stdev=self.stddev)


class RandomDistribution(FixedIntervalAnalyser):
    """
    No meaninful pattern in the data.
    """

    name = "random"

    def get_validity(self):
        return 0.1

    def get_result(self):
        return dict()  # nothing meaningful


_analysers = [NormalDistribution,
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
    if len(x_values) < 1:
        raise ValueError("it contains no data points!")
    if len(x_values) == 1:
        pass
    else:
        expected_interval_size = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
        for left, right in zip(x_values, x_values[1:]):
            if abs(1 - ((right - left) / expected_interval_size)) > 0.01:
               raise ValueError("Intervals on the X axis are not fixed width")


def get_analysis(points):
    try:
        assert_fixed_interval(points=points)
    except ValueError as ex:
        return dict(name=UNPROCESSABLE,
                result=str(ex))
    y_values = [point.y for point in sorted(points)]
    analyser = get_best_analyser(points)
    return dict(p_value=analyser.get_validity(),
            name=analyser.name,
            min_y_value=min(y_values),
            result=analyser.get_result())
