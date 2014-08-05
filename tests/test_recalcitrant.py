# Copyright 2014 Tennessee Leeuwenburg

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"Test for recalcitrant and obtuse graphs to describe"
from wordgraph.points import Point
import wordgraph

import json
import pytest
import py

from tests.lib.compare import assertParagraph


def test_time_goes_backwards():
    """
    A valid time series where time changes linearly backwards.

    Since it's a time series, we expect that we can sort it by time and present in order.
    This will not be true for arbitrary graphs.
    """
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [1.0, 1311836012],
    [2.0, 1311836011],
    [3.0, 1311836010],
    [5.0, 1311836009],
    [6.0, 1311836008]
  ]
}]
    """)

    graph = {'graphite_data': graphite_data}
    full_long = wordgraph.describe(graph, source='graphite')
    expected = '''
    This graph shows the relationship between time and metric.
    The x axis, time, ranges from 28 Jul 2011 06:53:28 to 28 Jul 2011 06:53:32.
    The y axis, metric, ranges from 1.0 to 6.0.
    It contains 1 series.
    The entries series is loosely linear
    '''

    assertParagraph(full_long, expected)


def test_random_graphite_metric():
    "A time series of points where the time is randomly ordered"
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [6.0, 1311836008],
    [1.0, 1311836012],
    [3.0, 1311836010],
    [2.0, 1311836011],
    [5.0, 1311836009]
  ]
}]
    """)

    graph = {'graphite_data': graphite_data}
    full_long = wordgraph.describe(graph, source='graphite')
    expected = '''
    This graph shows the relationship between time and metric.
    The x axis, time, ranges from 28 Jul 2011 06:53:28 to 28 Jul 2011 06:53:32.
    The y axis, metric, ranges from 1.0 to 6.0.
    It contains 1 series.
    The entries series is loosely linear
    '''

    assertParagraph(full_long, expected)


@py.test.mark.xfail  #TODO: This actually has an exception
def test_no_points():
    """A time series no data points."""
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": []
}]
    """)

    graph = {'graphite_data': graphite_data}
    full_long = wordgraph.describe(graph, source='graphite')
    expected = '''Graph invalid, because it contains no data points!'''

    assertParagraph(full_long, expected)

@py.test.mark.foo
def test_single_point():
    """A time series with a single data point."""
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [1.0, 1311836012]
  ]
}]
    """)

    graph = {'graphite_data': graphite_data}
    full_long = wordgraph.describe(graph, source='graphite')
    expected = '''
    This graph shows the relationship between time and metric. 
    The entries series is a single point, with value 1.0 at time 28 Jul 2011 06:53:32. 
    '''

    assertParagraph(full_long, expected)

def test_two_points():
    """A time series with two data points."""
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [1.0, 1311836012],
    [2.0, 1311836009]
  ]
}]
    """)

    graph = {'graphite_data': graphite_data}
    full_long = wordgraph.describe(graph, source='graphite')
    expected = '''
    This graph shows the relationship between time and metric.
    The x axis, time, ranges from 28 Jul 2011 06:53:29 to 28 Jul 2011 06:53:32. 
    The y axis, metric, ranges from 1.0 to 2.0.
    It contains 1 series.
    The entries series is broadly linear
    '''

    assertParagraph(full_long, expected)

@py.test.mark.xfail #TODO: Get aaron to fix this
def test_nonuniform_time_periods():
    """A time series where time periods are wildly different.

    Expected to raise an exception.
    """
    times = [1, 3, 4, 6, 7, 9, 10]
    graph = {'data_points': [Point(x=t, y=1.0) for t in times]}
    with pytest.raises(ValueError):
        full_long = wordgraph.describe(graph)


