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
does the actual analysis.

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


class LinearDistribution(FixedIntervalAnalyser):

    name = "linear"

    def get_validity(self):
        # calculate the line of best fit
        x = list(range(len(self.values)))
        A = np.vstack([x, np.ones(len(x))]).T
        result = np.linalg.lstsq(A, self.values)
        self.gradient, self.constant = result[0]
        print(result)
        return 0.2  # FIXME

    def get_result(self):
        return dict(gradient=self.gradient,
                constant=self.constant)


class NormalDistribution(FixedIntervalAnalyser):

    name = "normal"

    def get_validity(self):

        if len(self.values) >= 8:
            k2, pvalue = stats.normaltest(self.values)
            return pvalue ** 0.5

        else:

            return 0

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


_analysers = [NormalDistribution, RandomDistribution]


def get_best_analyser(values):
    """
    Instantiate a bunch of analysers and return the one
    which suits this data best.
    """
    return sorted((analyser(values=values)
        for analyser in _analysers),
        key=lambda a: a.get_validity())[-1]


def assert_fixed_interval(points):
    x_values = sorted(point.x for point in points)
    assert len(x_values) > 1, "Not enough data points!"
    expected_interval_size = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    for left, right in zip(x_values, x_values[1:]):
        assert abs(1 - ((right - left) / expected_interval_size)) < 0.01, \
            "Intervals on the X axis are not fixed width"


def get_analysis(points):
    assert_fixed_interval(points=points)
    y_values = [point.y for point in sorted(points)]
    analyser = get_best_analyser(values=y_values)
    return dict(p_value=analyser.get_validity(),
            name=analyser.name,
            result=analyser.get_result())
