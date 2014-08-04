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


"Test for artificially generated and perfect examples of graph features"
import wordgraph

from utilities import time_values

import py

@py.test.mark.xfail
def test_linear_values():
    "Postiive constant value time series in 10, one second increments"
    graph = {'datapoints': time_values(3.0 for i in range(10))}
    full_long_description = wordgraph.describe(datapoints)
    assert full_long_description is not None

@py.test.mark.xfail
def test_monotonic_up_per_second():
    "Monotonically increasing positive series in 10, one second increments"
    graph = {'datapoints': time_values(float(i) for i in range(10))}
    full_long_description = wordgraph.describe(datapoints)
    assert full_long_description is not None

@py.test.mark.xfail
def test_monotonic_down_per_second():
    "Monotonically descreasing positive series in 10, one second increments"
    graph = {'datapoints': time_values(10.0 - i for i in range(10))}
    full_long_description = wordgraph.describe(datapoints)
    assert full_long_description is not None

@py.test.mark.xfail
def test_tent_map():
    """Tent map time series
    
    A 20 second time series in two distinct, 10 second ranges with one second
    increments. First period is monotonically increasing. The second period is
    monotonically decreasing at the same rate.
    """
    values = [float(i) for i in range(10)]
    values.append(11.0)
    values += [10.0 - i for i in range(10)]
    graph = {'datapoints': time_values(values)}
    full_long_description = wordgraph.describe(datapoints)
    assert full_long_description is not None

@py.test.mark.xfail
def test_step_function():
    """Step function time series

    A 20 second time series in two distinct, 10 second ranges with one second
    increments. First period is a positive constant value. The second period is
    a different, positive constant value.
    """
    values = [1.0] * 10
    values += [2.0] * 10
    graph = {'datapoints': time_values(values)}
    full_long_description = wordgraph.describe(datapoints)
    assert full_long_description is not None

@py.test.mark.xfail
def test_saw_tooth():
    """A saw tooth time series

    A 25 second time series of 5 distinct periods. Each period exhibits the
    same monotonically increasing positive series. The series resets to the
    initial state on each section boundary.
    """
    values = [1.0 + i for i in range(5)]
    values *= 5
    values.append(1.0)
    graph = {'datapoints': time_values(values)}
    full_long_description = wordgraph.describe(datapoints)
    assert full_long_description is not None
